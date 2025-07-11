import pytest
import asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings
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
    from fastapi.testclient import TestClient
    
    # Clean database before each test
    sync_clean_database()
    
    # Create TestClient with lifespan events enabled
    with TestClient(app) as test_client:
        yield test_client
        
    # Clean database after each test
    sync_clean_database()
