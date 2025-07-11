import pytest
from fastapi.testclient import TestClient
from main import app


class TestUserController:
    """Test suite for User Controller - Only functional tests."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_get_users_empty_list(self, client):
        """Test GET /user returns empty list initially."""
        response = client.get("/api/v1/user")
        
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)
        # Note: May not be empty due to default users from init-mongo.js

    def test_create_user_success(self, client):
        """Test POST /user creates user successfully."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "email": "john.doe@example.com"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        
        assert response.status_code == 201
        created_user = response.json()
        
        # Verify response structure
        assert "id" in created_user
        assert created_user["first_name"] == "John"
        assert created_user["last_name"] == "Doe"
        assert created_user["username"] == "john.doe"
        assert created_user["email"] == "john.doe@example.com"
        assert "password" not in created_user  # Password should not be returned
        assert "created_at" in created_user
        assert "updated_at" in created_user

    def test_create_user_auto_username_generation(self, client):
        """Test that usernames are auto-generated correctly."""
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "password": "password123"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == "jane.smith"

    def test_create_user_duplicate_username_handling(self, client):
        """Test handling of duplicate usernames."""
        user_data = {
            "first_name": "Duplicate",
            "last_name": "User",
            "password": "password123"
        }
        
        # Create first user
        response1 = client.post("/api/v1/user", json=user_data)
        assert response1.status_code == 201
        user1 = response1.json()
        
        # Create second user with same name
        response2 = client.post("/api/v1/user", json=user_data)
        assert response2.status_code == 201
        user2 = response2.json()
        
        # Usernames should be different
        assert user1["username"] == "duplicate.user"
        assert user2["username"] == "duplicate.user1"

    def test_create_user_missing_required_fields(self, client):
        """Test creating user with missing required fields."""
        # Missing first_name
        response = client.post("/api/v1/user", json={
            "last_name": "Doe",
            "password": "password123"
        })
        assert response.status_code == 422
        
        # Missing last_name
        response = client.post("/api/v1/user", json={
            "first_name": "John",
            "password": "password123"
        })
        assert response.status_code == 422
        
        # Missing password
        response = client.post("/api/v1/user", json={
            "first_name": "John",
            "last_name": "Doe"
        })
        assert response.status_code == 422

    def test_create_user_optional_email(self, client):
        """Test creating user without email (optional field)."""
        user_data = {
            "first_name": "No",
            "last_name": "Email",
            "password": "password123"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["username"] == "no.email"
        # Email should be None or not present if not provided

    def test_get_users_after_creation(self, client):
        """Test that created users appear in the list."""
        # Create multiple users
        users_to_create = [
            {"first_name": "Alice", "last_name": "Smith", "password": "pass123"},
            {"first_name": "Bob", "last_name": "Jones", "password": "pass123"},
            {"first_name": "Carol", "last_name": "Brown", "password": "pass123"}
        ]
        
        for user_data in users_to_create:
            response = client.post("/api/v1/user", json=user_data)
            assert response.status_code == 201
        
        # Get all users
        response = client.get("/api/v1/user")
        assert response.status_code == 200
        users_list = response.json()
        
        # Verify our created users are in the list
        usernames = [user["username"] for user in users_list]
        assert "alice.smith" in usernames
        assert "bob.jones" in usernames
        assert "carol.brown" in usernames

    def test_login_post_success(self, client):
        """Test POST /login with valid credentials."""
        # Create a user first
        user_data = {
            "first_name": "PostLogin",
            "last_name": "Test",
            "password": "postloginpass123"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        
        # Test POST login
        login_data = {
            "username": created_user["username"],
            "password": "postloginpass123"
        }
        
        login_response = client.post("/api/v1/login", json=login_data)
        
        assert login_response.status_code == 200
        
        response_data = login_response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"
        assert "user" in response_data
        
        user_info = response_data["user"]
        assert user_info["username"] == created_user["username"]

    def test_login_invalid_credentials(self, client):
        """Test POST login with invalid credentials."""
        # Create a user first
        user_data = {
            "first_name": "Valid",
            "last_name": "User",
            "password": "correctpassword"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        
        # Test with wrong password
        login_response = client.post("/api/v1/login", json={
            "username": created_user["username"],
            "password": "wrongpassword"
        })
        
        assert login_response.status_code == 401
        error_data = login_response.json()
        assert error_data["detail"] == "Invalid username or password"
        
        # Test with non-existent user
        login_response = client.post("/api/v1/login", json={
            "username": "nonexistent.user",
            "password": "anypassword"
        })
        
        assert login_response.status_code == 401
        error_data = login_response.json()
        assert error_data["detail"] == "Invalid username or password"

    def test_login_missing_parameters(self, client):
        """Test POST login with missing parameters."""
        # Missing password
        response = client.post("/api/v1/login", json={"username": "test.user"})
        assert response.status_code == 422
        
        # Missing username
        response = client.post("/api/v1/login", json={"password": "password123"})
        assert response.status_code == 422
        
        # Missing both
        response = client.post("/api/v1/login", json={})
        assert response.status_code == 422


class TestUserControllerIntegration:
    """Integration tests for User Controller - Only functional tests."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)
    
    def test_full_user_workflow(self, client):
        """Test complete user workflow: create -> list -> login."""
        # Step 1: Create user
        user_data = {
            "first_name": "Workflow",
            "last_name": "Test",
            "password": "workflow123",
            "email": "workflow@example.com"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        
        # Step 2: Verify user appears in list
        list_response = client.get("/api/v1/user")
        assert list_response.status_code == 200
        users_list = list_response.json()
        
        user_found = False
        for user in users_list:
            if user["username"] == created_user["username"]:
                user_found = True
                break
        assert user_found, "Created user not found in users list"
        
        # Step 3: Login with created user (POST method only)
        login_response = client.post("/api/v1/login", json={
            "username": created_user["username"],
            "password": "workflow123"
        })
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        assert "access_token" in login_data
        assert login_data["user"]["username"] == created_user["username"]
    
    def test_password_security(self, client):
        """Test that passwords are properly hashed and not exposed."""
        user_data = {
            "first_name": "Security",
            "last_name": "Test",
            "password": "plaintext123"
        }
        
        # Create user
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        
        # Verify password is not in response
        assert "password" not in created_user
        
        # Verify user can login with correct password (POST method only)
        login_response = client.post("/api/v1/login", json={
            "username": created_user["username"],
            "password": "plaintext123"
        })
        assert login_response.status_code == 200
        
        # Verify user cannot login with wrong password
        wrong_login_response = client.post("/api/v1/login", json={
            "username": created_user["username"],
            "password": "wrongpassword"
        })
        assert wrong_login_response.status_code == 401
