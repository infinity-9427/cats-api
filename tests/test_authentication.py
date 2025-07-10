"""
Enterprise-level tests for Authentication System.
Tests JWT token generation, validation, and security features.
"""

import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.core.security import (
    create_access_token,
    verify_token,
    get_token_payload,
    is_token_valid,
    create_access_token_with_claims
)
from app.core.config import settings


class TestAuthenticationEndpoints:
    """Test suite for authentication endpoints."""
    
    def test_auth_verify_with_valid_token(self, client):
        """Test /auth/verify with valid token."""
        # Create a user and login
        user_data = {
            "first_name": "Auth",
            "last_name": "Test",
            "password": "authtest123"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        
        login_response = client.post("/api/v1/login", json={
            "username": "auth.test",
            "password": "authtest123"
        })
        assert login_response.status_code == 200
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test verify endpoint
        response = client.get("/api/v1/auth/verify", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
        assert data["username"] == "auth.test"
        assert "Token is valid" in data["message"]
    
    def test_auth_verify_without_token(self, client):
        """Test /auth/verify without token."""
        response = client.get("/api/v1/auth/verify")
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert data["username"] is None
        assert "No valid token provided" in data["message"]
    
    def test_auth_verify_with_invalid_token(self, client):
        """Test /auth/verify with invalid token."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/verify", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is False
        assert data["username"] is None
    
    def test_auth_me_with_valid_token(self, client):
        """Test /auth/me with valid token."""
        # Create user and login
        user_data = {
            "first_name": "Me",
            "last_name": "Test",
            "password": "metest123",
            "email": "me.test@example.com"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        
        login_response = client.post("/api/v1/login", json={
            "username": "me.test",
            "password": "metest123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test me endpoint
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        user = response.json()
        assert user["username"] == "me.test"
        assert user["first_name"] == "Me"
        assert user["last_name"] == "Test"
        assert user["email"] == "me.test@example.com"
        assert "password" not in user
    
    def test_auth_me_without_token(self, client):
        """Test /auth/me without token."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Authentication required"
    
    def test_auth_me_with_invalid_token(self, client):
        """Test /auth/me with invalid token."""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid or expired token"
    
    def test_auth_token_info_with_valid_token(self, client):
        """Test /auth/token-info with valid token."""
        # Create user and login
        user_data = {
            "first_name": "Token",
            "last_name": "Info",
            "password": "tokeninfo123"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        login_response = client.post("/api/v1/login", json={
            "username": "token.info",
            "password": "tokeninfo123"
        })
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test token info endpoint
        response = client.get("/api/v1/auth/token-info", headers=headers)
        
        assert response.status_code == 200
        token_info = response.json()
        assert token_info["username"] == "token.info"
        assert token_info["is_valid"] is True
        assert "expires_at" in token_info
        assert "issued_at" in token_info


class TestJWTTokenFunctionality:
    """Test suite for JWT token creation and validation."""
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        username = "testuser"
        token = create_access_token(data={"sub": username})
        
        assert isinstance(token, str)
        assert len(token) > 50  # JWT tokens are typically longer
        
        # Token should have 3 parts separated by dots
        parts = token.split('.')
        assert len(parts) == 3
    
    def test_verify_token_valid(self):
        """Test token verification with valid token."""
        username = "testuser"
        token = create_access_token(data={"sub": username})
        
        verified_username = verify_token(token)
        assert verified_username == username
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        invalid_token = "invalid.token.string"
        verified_username = verify_token(invalid_token)
        assert verified_username is None
    
    def test_get_token_payload(self):
        """Test getting token payload."""
        username = "testuser"
        token = create_access_token(data={"sub": username})
        
        payload = get_token_payload(token)
        assert payload is not None
        assert payload["sub"] == username
        assert "exp" in payload
    
    def test_is_token_valid(self):
        """Test token validity checking."""
        username = "testuser"
        # Create token with much longer expiration for testing
        longer_expiration = timedelta(hours=24)
        token = create_access_token(
            data={"sub": username}, 
            expires_delta=longer_expiration
        )
        
        # Valid token
        assert is_token_valid(token) is True
        
        # Invalid token
        assert is_token_valid("invalid.token") is False
    
    def test_token_expiration(self):
        """Test token expiration functionality."""
        username = "testuser"
        
        # Create token with very short expiration
        short_expiration = timedelta(milliseconds=100)
        token = create_access_token(
            data={"sub": username},
            expires_delta=short_expiration
        )
        
        # Wait for token to expire
        import time
        time.sleep(0.2)  # Wait 200ms for 100ms token to expire
        
        # Token should now be invalid
        assert is_token_valid(token) is False
    
    def test_create_token_with_additional_claims(self):
        """Test creating token with additional claims."""
        username = "adminuser"
        additional_claims = {
            "role": "admin",
            "permissions": ["read", "write", "delete"]
        }
        
        token = create_access_token_with_claims(
            username=username,
            additional_claims=additional_claims
        )
        
        payload = get_token_payload(token)
        assert payload is not None
        assert payload["sub"] == username
        assert payload["role"] == "admin"
        assert payload["permissions"] == ["read", "write", "delete"]
    
    def test_token_algorithm_security(self):
        """Test that tokens use secure algorithm."""
        # This test ensures we're using HS256 algorithm
        assert settings.ALGORITHM == "HS256"
        
        username = "securitytest"
        token = create_access_token(data={"sub": username})
        
        # Verify the token header specifies HS256
        import base64
        import json
        
        header_b64 = token.split('.')[0]
        # Add padding if needed
        header_b64 += '=' * (4 - len(header_b64) % 4)
        header_json = base64.urlsafe_b64decode(header_b64)
        header = json.loads(header_json)
        
        assert header["alg"] == "HS256"
        assert header["typ"] == "JWT"


class TestAuthenticationSecurity:
    """Test suite for authentication security features."""
    
    def test_password_not_in_responses(self, client):
        """Test that passwords are never returned in responses."""
        user_data = {
            "first_name": "Security",
            "last_name": "Test",
            "password": "securepassword123",
            "email": "security@example.com"
        }
        
        # Create user
        create_response = client.post("/api/v1/user", json=user_data)
        assert create_response.status_code == 201
        user = create_response.json()
        assert "password" not in user
        
        # Login
        login_response = client.post("/api/v1/login", json={
            "username": "security.test",
            "password": "securepassword123"
        })
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert "password" not in login_data["user"]
        
        # Get current user
        token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        me_response = client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert "password" not in me_data
    
    def test_token_bearer_format(self, client):
        """Test that tokens require Bearer format."""
        user_data = {
            "first_name": "Bearer",
            "last_name": "Test",
            "password": "bearertest123"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        login_response = client.post("/api/v1/login", json={
            "username": "bearer.test",
            "password": "bearertest123"
        })
        token = login_response.json()["access_token"]
        
        # Test with proper Bearer format
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200
        
        # Test without Bearer prefix
        headers = {"Authorization": token}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_sql_injection_protection(self, client):
        """Test protection against SQL injection in login."""
        # Test SQL injection attempts in username
        malicious_usernames = [
            "admin'; DROP TABLE users; --",
            "' OR '1'='1",
            "admin' OR 1=1 --",
            "'; DELETE FROM users; --"
        ]
        
        for username in malicious_usernames:
            response = client.post("/api/v1/login", json={
                "username": username,
                "password": "anypassword"
            })
            # Should return 401 (not found/invalid) not 500 (error)
            assert response.status_code == 401
    
    def test_rate_limiting_simulation(self, client):
        """Test multiple failed login attempts."""
        # Create a user
        user_data = {
            "first_name": "Rate",
            "last_name": "Limit",
            "password": "correctpassword"
        }
        
        create_response = client.post("/api/v1/user", json=user_data)
        username = create_response.json()["username"]
        
        # Simulate multiple failed attempts
        for i in range(5):
            response = client.post("/api/v1/login", json={
                "username": username,
                "password": "wrongpassword"
            })
            assert response.status_code == 401
        
        # Correct password should still work (no account lockout implemented yet)
        response = client.post("/api/v1/login", json={
            "username": username,
            "password": "correctpassword"
        })
        assert response.status_code == 200


class TestAuthenticationIntegration:
    """Integration tests for complete authentication workflows."""
    
    def test_complete_authentication_workflow(self, client):
        """Test complete user registration -> login -> authenticated access workflow."""
        # Step 1: Register user
        user_data = {
            "first_name": "Complete",
            "last_name": "Workflow",
            "password": "workflow123",
            "email": "complete@example.com"
        }
        
        register_response = client.post("/api/v1/user", json=user_data)
        assert register_response.status_code == 201
        user = register_response.json()
        
        # Step 2: Login
        login_response = client.post("/api/v1/login", json={
            "username": user["username"],
            "password": "workflow123"
        })
        assert login_response.status_code == 200
        
        login_data = login_response.json()
        token = login_data["access_token"]
        
        # Step 3: Use token for authenticated requests
        headers = {"Authorization": f"Bearer {token}"}
        
        # Verify token
        verify_response = client.get("/api/v1/auth/verify", headers=headers)
        assert verify_response.status_code == 200
        assert verify_response.json()["valid"] is True
        
        # Get current user
        me_response = client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["username"] == user["username"]
        
        # Get token info
        token_info_response = client.get("/api/v1/auth/token-info", headers=headers)
        assert token_info_response.status_code == 200
        token_info = token_info_response.json()
        assert token_info["username"] == user["username"]
        assert token_info["is_valid"] is True
    
    def test_multiple_users_authentication(self, client):
        """Test authentication with multiple users."""
        users_data = [
            {"first_name": "User1", "last_name": "Test", "password": "pass123"},
            {"first_name": "User2", "last_name": "Test", "password": "pass456"},
            {"first_name": "User3", "last_name": "Test", "password": "pass789"}
        ]
        
        tokens = []
        
        for user_data in users_data:
            # Create user
            create_response = client.post("/api/v1/user", json=user_data)
            assert create_response.status_code == 201
            user = create_response.json()
            
            # Login
            login_response = client.post("/api/v1/login", json={
                "username": user["username"],
                "password": user_data["password"]
            })
            assert login_response.status_code == 200
            
            token = login_response.json()["access_token"]
            tokens.append((user["username"], token))
        
        # Test that each token works for its respective user
        for username, token in tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/api/v1/auth/me", headers=headers)
            assert response.status_code == 200
            user_data = response.json()
            assert user_data["username"] == username
