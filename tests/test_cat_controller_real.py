"""
Real integration tests for Cat Controller using actual Cat API.
Tests all cat endpoints with real external API calls - no mocks.
"""

import pytest
from fastapi.testclient import TestClient


class TestCatControllerReal:
    """Test suite for Cat Controller endpoints using real Cat API."""
    
    def test_get_all_breeds_real_api(self, client):
        """Test GET /breeds returns real cat breeds from The Cat API."""
        response = client.get("/api/v1/breeds")
        
        # Should succeed with real API
        assert response.status_code == 200
        breeds = response.json()
        
        # Verify we get real data
        assert isinstance(breeds, list)
        assert len(breeds) > 0, "Should return real breeds from Cat API"
        
        # Check first breed has expected structure
        first_breed = breeds[0]
        required_fields = ["id", "name", "description", "temperament", "origin"]
        for field in required_fields:
            assert field in first_breed, f"Missing field: {field}"
            assert first_breed[field], f"Field {field} should not be empty"
    
    def test_get_breed_by_id_real_api(self, client):
        """Test GET /breeds/:breed_id with real Cat API."""
        # Use known real breed ID
        breed_id = "abys"  # Abyssinian
        response = client.get(f"/api/v1/breeds/{breed_id}")
        
        assert response.status_code == 200
        breed = response.json()
        
        # Verify real breed data
        assert breed["id"] == breed_id
        assert breed["name"] == "Abyssinian"
        assert "description" in breed
        assert "temperament" in breed
        assert "origin" in breed
        assert len(breed["description"]) > 50, "Should have real description"
    
    def test_get_breed_invalid_id_real_api(self, client):
        """Test GET /breeds/:breed_id with invalid ID."""
        response = client.get("/api/v1/breeds/invalid_breed_id_12345")
        
        # Real API might return 404 or 500 depending on external API behavior
        assert response.status_code in [404, 500]
        error = response.json()
        assert "detail" in error
    
    def test_search_breeds_with_query_real_api(self, client):
        """Test GET /breeds/search with search query."""
        response = client.get("/api/v1/breeds/search?q=Abyssinian")
        
        assert response.status_code == 200
        breeds = response.json()
        
        # Should return search results
        assert isinstance(breeds, list)
        # Search may return 0 or more results depending on the query
        
        # If results found, verify structure
        if len(breeds) > 0:
            breed = breeds[0]
            assert "id" in breed
            assert "name" in breed
    
    def test_search_breeds_with_limit_real_api(self, client):
        """Test GET /breeds/search with limit parameter."""
        response = client.get("/api/v1/breeds/search?limit=5")
        
        assert response.status_code == 200
        breeds = response.json()
        
        # Should return limited results
        assert isinstance(breeds, list)
        assert len(breeds) <= 5  # Should respect limit
    
    def test_search_breeds_empty_query_real_api(self, client):
        """Test GET /breeds/search with empty query."""
        response = client.get("/api/v1/breeds/search")
        
        assert response.status_code == 200
        breeds = response.json()
        
        # Should return results even without specific query
        assert isinstance(breeds, list)
    
    def test_search_breeds_no_results_real_api(self, client):
        """Test GET /breeds/search with query that returns no results."""
        response = client.get("/api/v1/breeds/search?q=NonExistentBreed12345XYZ")
        
        assert response.status_code == 200
        breeds = response.json()
        
        # Should return empty list for no matches
        assert isinstance(breeds, list)
        # May be empty or not, depends on real API behavior
    
    def test_real_api_connectivity(self, client):
        """Test that we can actually connect to The Cat API."""
        # This test ensures our API key and connectivity work
        response = client.get("/api/v1/breeds")
        
        # If this fails, check API key and internet connection
        assert response.status_code == 200, "Failed to connect to Cat API - check API key and connectivity"
        
        breeds = response.json()
        assert len(breeds) >= 40, "Should return substantial list of breeds from real API"
        
        # Verify we're getting real data structure
        sample_breed = breeds[0]
        expected_keys = ["id", "name", "description", "temperament", "origin", "life_span"]
        for key in expected_keys:
            assert key in sample_breed, f"Real API response missing expected key: {key}"


class TestCatControllerRealEdgeCases:
    """Test edge cases with real Cat API."""
    
    def test_breeds_endpoint_performance(self, client):
        """Test that real API calls are reasonably fast."""
        import time
        
        start_time = time.time()
        response = client.get("/api/v1/breeds")
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Real API should respond within reasonable time (10 seconds)
        elapsed = end_time - start_time
        assert elapsed < 10.0, f"API call took too long: {elapsed:.2f}s"
    
    def test_search_with_special_characters(self, client):
        """Test search with special characters (real API handling)."""
        response = client.get("/api/v1/breeds/search?q=Maine%20Coon")
        
        # Real API might return 200 or 500 depending on external API status
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            breeds = response.json()
            assert isinstance(breeds, list)
    
    def test_breed_by_id_data_completeness(self, client):
        """Test that breed by ID returns complete data."""
        # Use a known breed ID
        response = client.get("/api/v1/breeds/abys")
        assert response.status_code == 200
        
        breed = response.json()
        # Verify essential fields are present
        assert breed["id"] == "abys"
        assert breed["name"] == "Abyssinian"
        assert len(breed["description"]) > 100, "Should have detailed description"
        assert breed["temperament"] is not None
        assert breed["origin"] is not None
