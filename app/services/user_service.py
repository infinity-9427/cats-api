import re
import bcrypt
import hashlib
import time
from typing import List, Optional
from datetime import datetime, timezone
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository_interface import UserRepositoryInterface


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


class UserService:
    """Service layer for user operations."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    def _generate_username(self, first_name: str, last_name: str) -> str:
        """Generate username from first and last name."""
        # Remove accents and special characters, convert to lowercase
        import unicodedata
        
        # Normalize and remove accents
        first_normalized = unicodedata.normalize('NFD', first_name)
        first_clean = ''.join(c for c in first_normalized if unicodedata.category(c) != 'Mn')
        first_clean = re.sub(r'[^a-zA-Z]', '', first_clean.lower())
        
        last_normalized = unicodedata.normalize('NFD', last_name)
        last_clean = ''.join(c for c in last_normalized if unicodedata.category(c) != 'Mn')
        last_clean = re.sub(r'[^a-zA-Z]', '', last_clean.lower())
        
        # Take first word of last name if it has multiple words
        last_words = last_clean.split()
        if last_words:
            last_clean = last_words[0]
        
        # Create base username
        username = f"{first_clean}.{last_clean}"
        
        # Handle edge case where names are empty after cleaning
        if not first_clean or not last_clean:
            timestamp = str(int(time.time()))
            username = f"user{timestamp}"
        
        return username
    
    async def _get_unique_username(self, base_username: str) -> str:
        """Get unique username by adding numbers if needed."""
        username = base_username
        counter = 1
        
        while await self.user_repository.username_exists(username):
            if counter <= 999:
                username = f"{base_username}{counter}"
            else:
                # If we've tried 999 variations, add timestamp and hash for uniqueness
                timestamp = str(int(time.time()))
                hash_suffix = hashlib.md5(f"{base_username}{timestamp}".encode()).hexdigest()[:6]
                username = f"{base_username}.{hash_suffix}"
            counter += 1
            
            # Safety check to prevent infinite loop
            if counter > 1000:
                timestamp = str(int(time.time()))
                hash_suffix = hashlib.md5(f"{base_username}{timestamp}{counter}".encode()).hexdigest()[:8]
                username = f"user.{hash_suffix}"
                break
        
        return username
    
    async def create_user(self, user_create: UserCreate) -> UserResponse:
        """Create a new user."""
        try:
            # Generate username
            base_username = self._generate_username(user_create.first_name, user_create.last_name)
            unique_username = await self._get_unique_username(base_username)
            
            # Hash password
            hashed_password = get_password_hash(user_create.password)
            
            # Create user model
            user = User(
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                username=unique_username,
                password=hashed_password,
                email=user_create.email,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            # Save to database with retry logic for race conditions
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    created_user = await self.user_repository.create_user(user)
                    break
                except Exception as e:
                    if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                        if attempt < max_retries - 1:
                            # Regenerate username if duplicate found
                            unique_username = await self._get_unique_username(base_username)
                            user.username = unique_username
                            continue
                        else:
                            raise ValueError(f"Failed to create unique username after {max_retries} attempts")
                    else:
                        raise e
            else:
                raise ValueError("Failed to create user after maximum retries")
            
            # Return response
            return UserResponse(
                id=created_user.id,
                first_name=created_user.first_name,
                last_name=created_user.last_name,
                username=created_user.username,
                email=created_user.email,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at
            )
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")
    
    async def get_all_users(self) -> List[UserResponse]:
        """Get all users."""
        users = await self.user_repository.get_all_users()
        return [
            UserResponse(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            for user in users
        ]
    
    async def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        """Authenticate user with username and password."""
        user = await self.user_repository.get_user_by_username(username)
        
        if not user:
            return None
        
        if not verify_password(password, user.password):
            return None
        
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    async def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        """Get user by username."""
        user = await self.user_repository.get_user_by_username(username)
        
        if not user:
            return None
        
        return UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
