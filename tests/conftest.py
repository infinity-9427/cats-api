import pytest
import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
from app.core.database import get_database
from app.services.user_service import UserService
from app.services.cat_service import CatService
from app.repositories.user_repository import MongoUserRepository
from app.schemas.user import UserCreate, UserResponse
from main import app
from tests.database_cleanup import sync_clean_database


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client():
    """Create a test client with clean database."""
    # Clean database before each test
    sync_clean_database()
    
    with TestClient(app) as test_client:
        yield test_client
        
    # Clean database after each test
    sync_clean_database()


@pytest.fixture
async def test_db():
    """Create a test database for integration tests."""
    # Use a different database for testing
    test_client = AsyncIOMotorClient(settings.DATABASE_URL)
    test_database = test_client.cats_api_test
    
    yield test_database
    
    # Clean up test database
    await test_client.drop_database("cats_api_test")
    test_client.close()


@pytest.fixture
def mock_user_repository():
    """Create a mock user repository for unit tests."""
    class MockUserRepository:
        def __init__(self):
            self.users = {}
            self.usernames = set()
        
        async def create_user(self, user):
            if user.username in self.usernames:
                raise ValueError(f"Username '{user.username}' already exists")
            user.id = f"test_id_{len(self.users) + 1}"
            self.users[user.id] = user
            self.usernames.add(user.username)
            return user
        
        async def get_user_by_username(self, username):
            for user in self.users.values():
                if user.username == username:
                    return user
            return None
        
        async def get_all_users(self):
            return list(self.users.values())
        
        async def username_exists(self, username):
            return username in self.usernames
    
    return MockUserRepository()


@pytest.fixture
def user_service(mock_user_repository):
    """Create a user service with mock repository."""
    return UserService(mock_user_repository)


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "first_name": "John",
        "last_name": "Doe",
        "password": "password123",
        "email": "john.doe@example.com"
    }


@pytest.fixture
def sample_user_create(sample_user_data):
    """Sample UserCreate object for testing."""
    return UserCreate(**sample_user_data)


@pytest.fixture
async def created_user(user_service, sample_user_create):
    """Create a user for testing."""
    return await user_service.create_user(sample_user_create)


@pytest.fixture
def auth_headers():
    """Generate authentication headers for testing."""
    def _auth_headers(token: str):
        return {"Authorization": f"Bearer {token}"}
    return _auth_headers
