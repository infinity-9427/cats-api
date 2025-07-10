from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.user import User


class UserRepositoryInterface(ABC):
    """Interface for user repository."""
    
    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """Get all users."""
        pass
    
    @abstractmethod
    async def username_exists(self, username: str) -> bool:
        """Check if username exists."""
        pass
