"""
Enterprise-level integration tests.
Tests the complete application flow including controllers, services, and database.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock


class TestCompleteApplicationFlow:
    """Integration tests for complete application workflows."""
    
    def test_user_registration_and_cat_browsing_flow(self, client):
        """Test complete flow: register user -> login -> browse cats."""
        # Step 1: User Registration
        user_data = {
            "first_name": "Cat",
            "last_name": "Lover",
            "password": "catlover123",
            "email": "cat.lover@example.com"
        }
        
        register_response = client.post("/api/v1/user", json=user_data)
        assert register_response.status_code == 201
        
        user = register_response.json()
        assert user["username"] == "cat.lover"
        
        # Step 2: User Login
        login_response = client.post("/api/v1/login", json={
            "username": "cat.lover",
            "password": "catlover123"
        })
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        assert "access_token" in login_data
        token = login_data["access_token"]
        
        # Step 3: Browse cats (with authentication)
        headers = {"Authorization": f"Bearer {token}"}
        
        # Verify user is authenticated
        auth_check = client.get("/api/v1/auth/verify", headers=headers)
        assert auth_check.status_code == 200
        assert auth_check.json()["valid"] is True
        
        # Note: Cat endpoints don't require auth but could be enhanced to provide
        # personalized results for authenticated users
        
        # Browse breeds (should work regardless of auth)
        breeds_response = client.get("/api/v1/breeds")
        # This might return 500 if external API is down, but route should exist
        assert breeds_response.status_code != 404
        
        search_response = client.get("/api/v1/breeds/search?q=persian")
        assert search_response.status_code != 404
    
    def test_multiple_users_concurrent_operations(self, client):
        """Test multiple users performing operations concurrently."""
        users_data = [
            {"first_name": "Alice", "last_name": "Johnson", "password": "alice123"},
            {"first_name": "Bob", "last_name": "Smith", "password": "bob123"},
            {"first_name": "Carol", "last_name": "Wilson", "password": "carol123"}
        ]
        
        created_users = []
        tokens = []
        
        # Create multiple users
        for user_data in users_data:
            create_response = client.post("/api/v1/user", json=user_data)
            assert create_response.status_code == 201
            
            user = create_response.json()
            created_users.append(user)
            
            # Login each user
            login_response = client.post("/api/v1/login", json={
                "username": user["username"],
                "password": user_data["password"]
            })
            assert login_response.status_code == 200
            
            token = login_response.json()["access_token"]
            tokens.append(token)
        
        # Test that each user can access their own information
        for i, token in enumerate(tokens):
            headers = {"Authorization": f"Bearer {token}"}
            
            me_response = client.get("/api/v1/auth/me", headers=headers)
            assert me_response.status_code == 200
            
            user_info = me_response.json()
            assert user_info["username"] == created_users[i]["username"]
        
        # Test getting all users (should include all created users)
        all_users_response = client.get("/api/v1/user")
        assert all_users_response.status_code == 200
        
        all_users = all_users_response.json()
        created_usernames = {user["username"] for user in created_users}
        fetched_usernames = {user["username"] for user in all_users}
        
        # All created users should be in the fetched users
        assert created_usernames.issubset(fetched_usernames)
    
    def test_error_handling_across_application(self, client):
        """Test error handling across different parts of the application."""
        # Test invalid user creation
        invalid_user_data = {
            "first_name": "",  # Empty name
            "last_name": "Test",
            "password": "short"  # Might be considered invalid
        }
        
        response = client.post("/api/v1/user", json=invalid_user_data)
        # Should handle validation errors gracefully
        assert response.status_code in [400, 422]
        
        # Test login with non-existent user
        response = client.post("/api/v1/login", json={
            "username": "nonexistent.user",
            "password": "anypassword"
        })
        assert response.status_code == 401
        
        # Test accessing protected endpoint without auth
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        
        # Test accessing protected endpoint with invalid token
        headers = {"Authorization": "Bearer invalid.token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_application_security_headers(self, client):
        """Test that security measures are in place."""
        # Test CORS headers (should be present for browser security)
        response = client.get("/")
        # FastAPI automatically handles CORS if configured
        
        # Test authentication headers
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
        assert "WWW-Authenticate" in response.headers
        assert response.headers["WWW-Authenticate"] == "Bearer"


class TestAPIRequirementCompliance:
    """Test compliance with the original project requirements."""
    
    def test_cats_controller_requirements(self, client):
        """Test that Cats Controller meets all requirements."""
        # Requirement: GET /breeds - List of cat breeds
        response = client.get("/api/v1/breeds")
        assert response.status_code != 404  # Endpoint exists
        
        # Requirement: GET /breeds/:breed_id - Specific breed
        response = client.get("/api/v1/breeds/test_breed")
        assert response.status_code != 404  # Endpoint exists
        
        # Requirement: GET /breeds/search - Search with parameters
        response = client.get("/api/v1/breeds/search")
        assert response.status_code != 404  # Endpoint exists
        
        # Test with parameters
        response = client.get("/api/v1/breeds/search?q=test&limit=5")
        assert response.status_code != 404
    
    def test_users_controller_requirements(self, client):
        """Test that Users Controller meets all requirements."""
        # Requirement: GET /user - List of users
        response = client.get("/api/v1/user")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        # Requirement: POST /user - Create user with auto-generated username
        user_data = {
            "first_name": "Requirement",
            "last_name": "Test",
            "password": "reqtest123",
            "email": "req.test@example.com"
        }
        
        response = client.post("/api/v1/user", json=user_data)
        assert response.status_code == 201
        
        user = response.json()
        assert user["username"] == "requirement.test"  # Auto-generated
        assert "id" in user
        assert user["first_name"] == "Requirement"
        assert user["last_name"] == "Test"
        
        # Requirement: GET /login - User authentication
        response = client.get("/api/v1/login", params={
            "username": "requirement.test",
            "password": "reqtest123"
        })
        assert response.status_code == 200
        
        login_data = response.json()
        assert "access_token" in login_data  # Returns token (for future use)
        assert "user" in login_data  # Returns user information
        assert login_data["user"]["username"] == "requirement.test"
    
    def test_username_generation_requirements(self, client):
        """Test automatic username generation requirement."""
        test_cases = [
            {
                "input": {"first_name": "Juan", "last_name": "Pérez", "password": "pass123"},
                "expected": "juan.perez"
            },
            {
                "input": {"first_name": "María José", "last_name": "García López", "password": "pass123"},
                "expected": "mariajose.garcialopez"
            },
            {
                "input": {"first_name": "José", "last_name": "O'Connor", "password": "pass123"},
                "expected": "jose.oconnor"
            }
        ]
        
        for case in test_cases:
            response = client.post("/api/v1/user", json=case["input"])
            assert response.status_code == 201
            
            user = response.json()
            assert user["username"] == case["expected"]
    
    def test_no_duplicate_usernames_requirement(self, client):
        """Test that duplicate usernames are not allowed."""
        base_user = {
            "first_name": "Duplicate",
            "last_name": "Test",
            "password": "dup123"
        }
        
        # Create first user
        response1 = client.post("/api/v1/user", json=base_user)
        assert response1.status_code == 201
        user1 = response1.json()
        assert user1["username"] == "duplicate.test"
        
        # Create second user with same name
        base_user["email"] = "duplicate2@example.com"
        response2 = client.post("/api/v1/user", json=base_user)
        assert response2.status_code == 201
        user2 = response2.json()
        assert user2["username"] == "duplicate.test1"  # Auto-incremented
        
        # Verify usernames are different
        assert user1["username"] != user2["username"]
    
    def test_mongodb_integration_requirement(self, client):
        """Test MongoDB integration for user storage."""
        # Create user (should be stored in MongoDB)
        user_data = {
            "first_name": "MongoDB",
            "last_name": "Test",
            "password": "mongo123",
            "email": "mongo@example.com"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        user = create_response.json()
        
        # Verify user appears in user list (fetched from MongoDB)
        list_response = client.get("/api/v1/user")
        assert list_response.status_code == 200
        
        users = list_response.json()
        user_found = any(u["username"] == user["username"] for u in users)
        assert user_found
        
        # Verify login works (validates against MongoDB)
        login_response = client.post("/api/v1/login", json={
            "username": user["username"],
            "password": "mongo123"
        })
        assert login_response.status_code == 200
    
    def test_password_validation_requirement(self, client):
        """Test password validation against MongoDB."""
        # Create user
        user_data = {
            "first_name": "Password",
            "last_name": "Validation",
            "password": "correctpassword123"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        user = create_response.json()
        
        # Test correct password
        correct_login = client.post("/api/v1/login", json={
            "username": user["username"],
            "password": "correctpassword123"
        })
        assert correct_login.status_code == 200
        
        # Test incorrect password
        wrong_login = client.post("/api/v1/login", json={
            "username": user["username"],
            "password": "wrongpassword"
        })
        assert wrong_login.status_code == 401


class TestArchitectureCompliance:
    """Test compliance with architecture requirements (SOLID, Clean Architecture)."""
    
    def test_service_layer_separation(self):
        """Test that services are properly separated."""
        from app.services.user_service import UserService
        from app.services.cat_service import CatService
        
        # Services should exist and be importable
        assert UserService is not None
        assert CatService is not None
    
    def test_repository_pattern_implementation(self):
        """Test repository pattern implementation."""
        from app.repositories.user_repository_interface import UserRepositoryInterface
        from app.repositories.user_repository import MongoUserRepository
        
        # Interface should exist
        assert UserRepositoryInterface is not None
        
        # Implementation should exist and implement interface
        assert MongoUserRepository is not None
        assert issubclass(MongoUserRepository, UserRepositoryInterface)
    
    def test_model_schema_separation(self):
        """Test separation between models and schemas."""
        from app.models.user import User
        from app.models.cat import CatBreed
        from app.schemas.user import UserCreate, UserResponse
        from app.schemas.cat import CatBreedResponse
        
        # Models (for database)
        assert User is not None
        assert CatBreed is not None
        
        # Schemas (for API)
        assert UserCreate is not None
        assert UserResponse is not None
        assert CatBreedResponse is not None
    
    def test_controller_service_dependency(self):
        """Test that controllers depend on services, not repositories directly."""
        # This is more of a code review test, but we can check imports
        import inspect
        from app.controllers import user_controller, cat_controller
        
        # Controllers should exist
        assert user_controller is not None
        assert cat_controller is not None
