"""
Enterprise-level unit tests for User Service.
Tests business logic and service layer functionality.
"""

import pytest
from datetime import datetime, timezone
from app.services.user_service import UserService, get_password_hash, verify_password
from app.schemas.user import UserCreate
from app.repositories.user_repository_interface import UserRepositoryInterface


class MockUserRepository(UserRepositoryInterface):
    """Mock repository for testing User Service."""
    
    def __init__(self):
        self.users = []
        self.usernames = set()
    
    async def create_user(self, user):
        if user.username in self.usernames:
            raise ValueError(f"Username '{user.username}' already exists")
        user.id = str(len(self.users) + 1)
        self.users.append(user)
        self.usernames.add(user.username)
        return user
    
    async def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    async def get_all_users(self):
        return self.users
    
    async def username_exists(self, username):
        return username in self.usernames


class TestUserService:
    """Test suite for User Service business logic."""
    
    @pytest.fixture
    def mock_repository(self):
        return MockUserRepository()
    
    @pytest.fixture
    def user_service(self, mock_repository):
        return UserService(mock_repository)
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service):
        """Test successful user creation."""
        user_create = UserCreate(
            first_name="John",
            last_name="Doe",
            password="password123",
            email="john@example.com"
        )
        
        user_response = await user_service.create_user(user_create)
        
        assert user_response.first_name == "John"
        assert user_response.last_name == "Doe"
        assert user_response.username == "john.doe"
        assert user_response.email == "john@example.com"
        assert user_response.id is not None
        assert isinstance(user_response.created_at, datetime)
        assert isinstance(user_response.updated_at, datetime)
    
    @pytest.mark.asyncio
    async def test_create_user_without_email(self, user_service):
        """Test user creation without email."""
        user_create = UserCreate(
            first_name="Jane",
            last_name="Smith",
            password="password123"
        )
        
        user_response = await user_service.create_user(user_create)
        
        assert user_response.username == "jane.smith"
        assert user_response.email is None
    
    @pytest.mark.asyncio
    async def test_username_generation_basic(self, user_service):
        """Test basic username generation."""
        # Test internal method directly
        username = user_service._generate_username("Ana María", "Pérez Gómez")
        assert username == "anamaria.perezgomez"
        
        username = user_service._generate_username("José", "Da Silva")
        assert username == "jose.dasilva"
        
        username = user_service._generate_username("John", "O'Connor")
        assert username == "john.oconnor"
    
    @pytest.mark.asyncio
    async def test_username_generation_special_characters(self, user_service):
        """Test username generation with special characters."""
        test_cases = [
            ("José-María", "García-López", "josemaria.garcialopez"),
            ("Anne", "d'Arc", "anne.darc"),
            ("Jean-Paul", "Saint-Exupéry", "jeanpaul.saintexupery"),
            ("François", "Müller", "francois.muller")
        ]
        
        for first_name, last_name, expected in test_cases:
            username = user_service._generate_username(first_name, last_name)
            assert username == expected
    
    @pytest.mark.asyncio
    async def test_unique_username_generation(self, user_service):
        """Test unique username generation when duplicates exist."""
        # Create first user
        user_create1 = UserCreate(
            first_name="John",
            last_name="Doe",
            password="password123"
        )
        user1 = await user_service.create_user(user_create1)
        assert user1.username == "john.doe"
        
        # Create second user with same name
        user_create2 = UserCreate(
            first_name="John",
            last_name="Doe",
            password="password456"
        )
        user2 = await user_service.create_user(user_create2)
        assert user2.username == "john.doe1"
        
        # Create third user with same name
        user_create3 = UserCreate(
            first_name="John",
            last_name="Doe",
            password="password789"
        )
        user3 = await user_service.create_user(user_create3)
        assert user3.username == "john.doe2"
    
    @pytest.mark.asyncio
    async def test_get_all_users(self, user_service):
        """Test getting all users."""
        # Initially empty
        users = await user_service.get_all_users()
        assert len(users) == 0
        
        # Create multiple users
        for i in range(3):
            user_create = UserCreate(
                first_name=f"User{i}",
                last_name="Test",
                password=f"password{i}"
            )
            await user_service.create_user(user_create)
        
        users = await user_service.get_all_users()
        assert len(users) == 3
        
        usernames = [user.username for user in users]
        # The username generation strips digits from names, so User0 becomes "user"
        assert "user.test" in usernames
        assert "user.test1" in usernames  # Second user gets number suffix
        assert "user.test2" in usernames  # Third user gets number suffix
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, user_service):
        """Test successful user authentication."""
        # Create user
        user_create = UserCreate(
            first_name="Auth",
            last_name="Test",
            password="securepassword"
        )
        created_user = await user_service.create_user(user_create)
        
        # Test authentication
        authenticated_user = await user_service.authenticate_user("auth.test", "securepassword")
        
        assert authenticated_user is not None
        assert authenticated_user.username == "auth.test"
        assert authenticated_user.first_name == "Auth"
        assert authenticated_user.last_name == "Test"
    
    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, user_service):
        """Test authentication with wrong password."""
        # Create user
        user_create = UserCreate(
            first_name="Auth",
            last_name="Test",
            password="correctpassword"
        )
        await user_service.create_user(user_create)
        
        # Test with wrong password
        authenticated_user = await user_service.authenticate_user("auth.test", "wrongpassword")
        assert authenticated_user is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent(self, user_service):
        """Test authentication with non-existent user."""
        authenticated_user = await user_service.authenticate_user("nonexistent.user", "password")
        assert authenticated_user is None
    
    @pytest.mark.asyncio
    async def test_get_user_by_username_success(self, user_service):
        """Test getting user by username."""
        # Create user
        user_create = UserCreate(
            first_name="Find",
            last_name="Me",
            password="password123"
        )
        created_user = await user_service.create_user(user_create)
        
        # Find user
        found_user = await user_service.get_user_by_username("find.me")
        
        assert found_user is not None
        assert found_user.username == "find.me"
        assert found_user.first_name == "Find"
        assert found_user.last_name == "Me"
    
    @pytest.mark.asyncio
    async def test_get_user_by_username_not_found(self, user_service):
        """Test getting non-existent user by username."""
        found_user = await user_service.get_user_by_username("nonexistent.user")
        assert found_user is None
    
    @pytest.mark.asyncio
    async def test_error_handling_in_user_creation(self, user_service):
        """Test error handling during user creation."""
        # Create a user first
        user_create = UserCreate(
            first_name="Error",
            last_name="Test",
            password="password123"
        )
        await user_service.create_user(user_create)
        
        # Mock repository to raise an error
        async def mock_create_user_error(user):
            raise Exception("Database connection failed")
        
        user_service.user_repository.create_user = mock_create_user_error
        
        # Try to create another user
        user_create2 = UserCreate(
            first_name="Error2",
            last_name="Test",
            password="password456"
        )
        
        with pytest.raises(ValueError, match="Error creating user"):
            await user_service.create_user(user_create2)


class TestPasswordSecurity:
    """Test password hashing and verification functions."""
    
    def test_password_hashing(self):
        """Test password hashing functionality."""
        password = "mySecurePassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        
        # Hash should start with bcrypt identifier
        assert hashed.startswith("$2b$")
        
        # Hash should be consistent length
        assert len(hashed) == 60
    
    def test_password_verification(self):
        """Test password verification functionality."""
        password = "testPassword456"
        hashed = get_password_hash(password)
        
        # Correct password should verify
        assert verify_password(password, hashed) is True
        
        # Wrong password should not verify
        assert verify_password("wrongPassword", hashed) is False
        
        # Empty password should not verify
        assert verify_password("", hashed) is False
    
    def test_different_passwords_different_hashes(self):
        """Test that different passwords produce different hashes."""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2
    
    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "samePassword"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to random salt
        assert hash1 != hash2
        
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
