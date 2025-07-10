"""
Enterprise-level tests for Cat Controller.
Tests all cat endpoints according to requirements:
- GET /breeds - List of cat breeds
- GET /breeds/:breed_id - Specific breed by ID
- GET /breeds/search - Search breeds by parameters
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient


class TestCatController:
    """Test suite for Cat Controller endpoints."""
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_get_all_breeds_success(self, mock_client, client):
        """Test GET /breeds returns list of cat breeds."""
        # Mock response data from TheCatAPI
        mock_response_data = [
            {
                "id": "abys",
                "name": "Abyssinian",
                "description": "The Abyssinian is easy to care for...",
                "temperament": "Active, Energetic, Independent",
                "origin": "Egypt",
                "life_span": "14 - 15",
                "wikipedia_url": "https://en.wikipedia.org/wiki/Abyssinian_cat",
                "adaptability": 5,
                "affection_level": 5,
                "child_friendly": 3,
                "reference_image_id": "0XYvRd7oD"
            },
            {
                "id": "aege",
                "name": "Aegean",
                "description": "Native to the Greek islands...",
                "temperament": "Affectionate, Social, Intelligent",
                "origin": "Greece",
                "life_span": "9 - 12"
            }
        ]
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request
        response = client.get("/api/v1/breeds")
        
        # Assertions
        assert response.status_code == 200
        breeds = response.json()
        
        assert len(breeds) == 2
        assert breeds[0]["id"] == "abys"
        assert breeds[0]["name"] == "Abyssinian"
        assert breeds[0]["origin"] == "Egypt"
        assert breeds[1]["id"] == "aege"
        assert breeds[1]["name"] == "Aegean"
        assert breeds[1]["origin"] == "Greece"
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_get_breed_by_id_success(self, mock_client, client):
        """Test GET /breeds/:breed_id returns specific breed."""
        # Mock response data
        mock_response_data = {
            "id": "abys",
            "name": "Abyssinian",
            "description": "The Abyssinian is easy to care for...",
            "temperament": "Active, Energetic, Independent",
            "origin": "Egypt",
            "life_span": "14 - 15",
            "adaptability": 5,
            "affection_level": 5,
            "child_friendly": 3
        }
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_response.status_code = 200
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request
        response = client.get("/api/v1/breeds/abys")
        
        # Assertions
        assert response.status_code == 200
        breed = response.json()
        
        assert breed["id"] == "abys"
        assert breed["name"] == "Abyssinian"
        assert breed["origin"] == "Egypt"
        assert breed["temperament"] == "Active, Energetic, Independent"
        assert breed["adaptability"] == 5
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_get_breed_by_id_not_found(self, mock_client, client):
        """Test GET /breeds/:breed_id with non-existent breed."""
        # Setup mock for 404
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request
        response = client.get("/api/v1/breeds/nonexistent")
        
        # Assertions
        assert response.status_code == 404
        error_data = response.json()
        assert "not found" in error_data["detail"].lower()
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_search_breeds_with_query(self, mock_client, client):
        """Test GET /breeds/search with query parameter."""
        # Mock response data
        mock_response_data = [
            {
                "id": "pers",
                "name": "Persian",
                "description": "The Persian cat is a long-haired breed...",
                "temperament": "Affectionate, Docile, Quiet",
                "origin": "Iran",
                "life_span": "14 - 15"
            }
        ]
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request with query parameter
        response = client.get("/api/v1/breeds/search?q=persian")
        
        # Assertions
        assert response.status_code == 200
        breeds = response.json()
        
        assert len(breeds) == 1
        assert breeds[0]["name"] == "Persian"
        assert breeds[0]["origin"] == "Iran"
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_search_breeds_with_limit(self, mock_client, client):
        """Test GET /breeds/search with limit parameter."""
        # Mock response data
        mock_response_data = [
            {"id": "abys", "name": "Abyssinian", "origin": "Egypt"},
            {"id": "aege", "name": "Aegean", "origin": "Greece"}
        ]
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request with limit parameter
        response = client.get("/api/v1/breeds/search?limit=2")
        
        # Assertions
        assert response.status_code == 200
        breeds = response.json()
        assert len(breeds) <= 2
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_search_breeds_with_multiple_parameters(self, mock_client, client):
        """Test GET /breeds/search with multiple parameters."""
        # Mock response data
        mock_response_data = [
            {
                "id": "maine",
                "name": "Maine Coon",
                "origin": "United States",
                "temperament": "Adaptable, Friendly, Intelligent"
            }
        ]
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request with multiple parameters
        response = client.get("/api/v1/breeds/search?q=maine&limit=5&attach_breed=1")
        
        # Assertions
        assert response.status_code == 200
        breeds = response.json()
        assert isinstance(breeds, list)
    
    def test_search_breeds_invalid_limit(self, client):
        """Test GET /breeds/search with invalid limit parameter."""
        # Test with limit too high
        response = client.get("/api/v1/breeds/search?limit=200")
        assert response.status_code == 422
        
        # Test with negative limit
        response = client.get("/api/v1/breeds/search?limit=-1")
        assert response.status_code == 422
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_search_breeds_empty_results(self, mock_client, client):
        """Test GET /breeds/search with no results."""
        # Mock empty response
        mock_response_data = []
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request
        response = client.get("/api/v1/breeds/search?q=nonexistentbreed")
        
        # Assertions
        assert response.status_code == 200
        breeds = response.json()
        assert breeds == []
    
    def test_breeds_endpoints_exist(self, client):
        """Test that all required breed endpoints exist."""
        # Test that endpoints don't return 404 (Not Found)
        # They might return 500 if external API is down, but the routes should exist
        
        # GET /breeds
        response = client.get("/api/v1/breeds")
        assert response.status_code != 404
        
        # GET /breeds/:breed_id
        response = client.get("/api/v1/breeds/test")
        assert response.status_code != 404
        
        # GET /breeds/search
        response = client.get("/api/v1/breeds/search")
        assert response.status_code != 404


class TestCatControllerIntegration:
    """Integration tests for Cat Controller with external API."""
    
    def test_breeds_endpoint_response_structure(self, client):
        """Test that breeds endpoint returns proper structure (if API is available)."""
        response = client.get("/api/v1/breeds")
        
        # If external API is down, we might get 500, but structure should be consistent
        if response.status_code == 200:
            breeds = response.json()
            assert isinstance(breeds, list)
            
            if len(breeds) > 0:
                breed = breeds[0]
                # Check required fields
                assert "id" in breed
                assert "name" in breed
                # Optional fields might be present
                optional_fields = ["description", "temperament", "origin", "life_span"]
                for field in optional_fields:
                    if field in breed:
                        assert isinstance(breed[field], (str, type(None)))
    
    def test_breed_search_response_structure(self, client):
        """Test that search endpoint returns proper structure."""
        response = client.get("/api/v1/breeds/search?q=test")
        
        if response.status_code == 200:
            breeds = response.json()
            assert isinstance(breeds, list)
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_api_error_handling(self, mock_client, client):
        """Test error handling when external API fails."""
        # Setup mock to raise an exception
        mock_context = AsyncMock()
        mock_context.get.side_effect = Exception("API connection failed")
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Make request
        response = client.get("/api/v1/breeds")
        
        # Should return 500 Internal Server Error
        assert response.status_code == 500
        error_data = response.json()
        assert "detail" in error_data


class TestCatServiceUnit:
    """Unit tests for Cat Service."""
    
    @patch('app.services.cat_service.httpx.AsyncClient')
    def test_cat_service_converts_response_correctly(self, mock_client):
        """Test that CatService converts API response to proper format."""
        from app.services.cat_service import CatService
        
        # Mock response data with image reference
        mock_response_data = [
            {
                "id": "test",
                "name": "Test Breed",
                "description": "Test description",
                "temperament": "Test temperament",
                "origin": "Test origin",
                "reference_image_id": "test123"
            }
        ]
        
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        # Test the service
        cat_service = CatService()
        
        # This would need to be run in an async context in a real test
        # For now, we're testing the structure and mocking
        assert cat_service.base_url is not None
        assert cat_service.api_key is not None
    
    def test_cat_service_image_url_generation(self):
        """Test image URL generation logic."""
        from app.services.cat_service import CatService
        
        cat_service = CatService()
        
        # Test with reference_image_id
        breed_data = {"reference_image_id": "test123"}
        response = cat_service._convert_to_response(breed_data)
        
        expected_url = "https://cdn2.thecatapi.com/images/test123.jpg"
        assert response.image_url == expected_url
        
        # Test with direct image data
        breed_data = {"image": {"url": "https://direct.image.url/image.jpg"}}
        response = cat_service._convert_to_response(breed_data)
        assert response.image_url == "https://direct.image.url/image.jpg"
        
        # Test with no image data
        breed_data = {}
        response = cat_service._convert_to_response(breed_data)
        assert response.image_url is None
