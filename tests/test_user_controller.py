"""
Enterprise-level tests for User Controller.
Tests all user endpoints according to requirements:
- GET /user - List users
- POST /user - Create user with auto-generated username
- GET /login - User authentication
"""

import pytest
import json
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate


class TestUserController:
    """Test suite for User Controller endpoints."""
    
    def test_get_users_empty_list(self, client):
        """Test GET /user returns empty list initially."""
        response = client.get("/api/v1/user")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_user_success(self, client):
        """Test POST /user creates user successfully."""
        user_data = {
            "first_name": "María",
            "last_name": "González",
            "password": "securepass123",
            "email": "maria.gonzalez@example.com"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        
        assert response.status_code == 201
        
        user = response.json()
        assert user["first_name"] == "María"
        assert user["last_name"] == "González"
        assert user["username"] == "maria.gonzalez"
        assert user["email"] == "maria.gonzalez@example.com"
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user
        assert "password" not in user  # Password should not be returned
    
    def test_create_user_auto_username_generation(self, client):
        """Test automatic username generation from names."""
        test_cases = [
            {
                "input": {"first_name": "José", "last_name": "Da Silva", "password": "pass123"},
                "expected_username": "jose.dasilva"
            },
            {
                "input": {"first_name": "Ana María", "last_name": "Pérez Gómez", "password": "pass123"},
                "expected_username": "anamaria.perezgomez"
            },
            {
                "input": {"first_name": "John", "last_name": "O'Connor", "password": "pass123"},
                "expected_username": "john.oconnor"
            }
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/user", json=case["input"])
            
            assert response.status_code == 201
            user = response.json()
            assert user["username"] == case["expected_username"]
    
    def test_create_user_duplicate_username_handling(self, client):
        """Test handling of duplicate usernames."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "email": "john1@example.com"
        }
        
        # Create first user
        response1 = client.post("/api/v1/user", json=user_data)
        assert response1.status_code == 201
        user1 = response1.json()
        assert user1["username"] == "john.doe"
        
        # Create second user with same name
        user_data["email"] = "john2@example.com"
        response2 = client.post("/api/v1/user", json=user_data)
        assert response2.status_code == 201
        user2 = response2.json()
        assert user2["username"] == "john.doe1"
        
        # Create third user with same name
        user_data["email"] = "john3@example.com"
        response3 = client.post("/api/v1/user", json=user_data)
        assert response3.status_code == 201
        user3 = response3.json()
        assert user3["username"] == "john.doe2"
    
    def test_create_user_missing_required_fields(self, client):
        """Test user creation with missing required fields."""
        test_cases = [
            {"last_name": "Doe", "password": "pass123"},  # Missing first_name
            {"first_name": "John", "password": "pass123"},  # Missing last_name
            {"first_name": "John", "last_name": "Doe"},  # Missing password
        ]
        
        for user_data in test_cases:
            response = client.post("/api/v1/user", json=user_data)
            assert response.status_code == 422  # Validation error
    
    def test_create_user_optional_email(self, client):
        """Test user creation without email (optional field)."""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "password": "password123"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        
        assert response.status_code == 201
        user = response.json()
        assert user["username"] == "test.user"
        assert user["email"] is None
    
    def test_get_users_after_creation(self, client):
        """Test GET /user after creating users."""
        # Create multiple users
        users_data = [
            {"first_name": "Alice", "last_name": "Smith", "password": "pass123"},
            {"first_name": "Bob", "last_name": "Jones", "password": "pass456"},
            {"first_name": "Carol", "last_name": "Brown", "password": "pass789"}
        ]
        
        created_users = []
        for user_data in users_data:
            response = client.post("/api/v1/user", json=user_data)
            assert response.status_code == 201
            created_users.append(response.json())
        
        # Get all users
        response = client.get("/api/v1/user")
        assert response.status_code == 200
        
        users_list = response.json()
        assert len(users_list) >= 3  # At least the 3 we created
        
        # Verify our created users are in the list
        usernames = [user["username"] for user in users_list]
        assert "alice.smith" in usernames
        assert "bob.jones" in usernames
        assert "carol.brown" in usernames
    
    def test_login_get_success(self, client):
        """Test GET /login with valid credentials."""
        # Create a user first
        user_data = {
            "first_name": "Login",
            "last_name": "Test",
            "password": "loginpass123",
            "email": "login.test@example.com"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        
        # Test login
        login_response = client.get(
            "/api/v1/login",
            params={"username": created_user["username"], "password": "loginpass123"}
        )
        
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        assert "access_token" in login_data
        assert login_data["token_type"] == "bearer"
        assert "user" in login_data
        
        user_info = login_data["user"]
        assert user_info["username"] == created_user["username"]
        assert user_info["first_name"] == "Login"
        assert user_info["last_name"] == "Test"
        assert "password" not in user_info  # Password should not be returned
    
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
        """Test login with invalid credentials."""
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
        login_response = client.get(
            "/api/v1/login",
            params={"username": created_user["username"], "password": "wrongpassword"}
        )
        
        assert login_response.status_code == 401
        error_data = login_response.json()
        assert error_data["detail"] == "Invalid username or password"
        
        # Test with non-existent user
        login_response = client.get(
            "/api/v1/login",
            params={"username": "nonexistent.user", "password": "anypassword"}
        )
        
        assert login_response.status_code == 401
        error_data = login_response.json()
        assert error_data["detail"] == "Invalid username or password"
    
    def test_login_missing_parameters(self, client):
        """Test login with missing parameters."""
        # Missing password
        response = client.get("/api/v1/login", params={"username": "test.user"})
        assert response.status_code == 422
        
        # Missing username
        response = client.get("/api/v1/login", params={"password": "password123"})
        assert response.status_code == 422
        
        # Missing both
        response = client.get("/api/v1/login")
        assert response.status_code == 422


class TestUserControllerIntegration:
    """Integration tests for User Controller."""
    
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
        
        # Step 3: Login with created user
        login_response = client.get(
            "/api/v1/login",
            params={"username": created_user["username"], "password": "workflow123"}
        )
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
        
        # Verify user can login with correct password
        login_response = client.get(
            "/api/v1/login",
            params={"username": created_user["username"], "password": "plaintext123"}
        )
        assert login_response.status_code == 200
        
        # Verify user cannot login with wrong password
        wrong_login_response = client.get(
            "/api/v1/login",
            params={"username": created_user["username"], "password": "wrongpassword"}
        )
        assert wrong_login_response.status_code == 401
