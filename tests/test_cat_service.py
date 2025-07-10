import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.cat_service import CatService
from app.schemas.cat import CatBreedSearchParams


@pytest.mark.asyncio
async def test_get_all_breeds():
    """Test getting all cat breeds."""
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
        }
    ]
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        cat_service = CatService()
        breeds = await cat_service.get_all_breeds()
        
        assert len(breeds) == 1
        assert breeds[0].id == "abys"
        assert breeds[0].name == "Abyssinian"
        assert breeds[0].origin == "Egypt"


@pytest.mark.asyncio
async def test_get_breed_by_id():
    """Test getting a specific breed by ID."""
    mock_response_data = {
        "id": "abys",
        "name": "Abyssinian",
        "description": "The Abyssinian is easy to care for...",
        "temperament": "Active, Energetic, Independent",
        "origin": "Egypt"
    }
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        mock_response.status_code = 200
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        cat_service = CatService()
        breed = await cat_service.get_breed_by_id("abys")
        
        assert breed is not None
        assert breed.id == "abys"
        assert breed.name == "Abyssinian"


@pytest.mark.asyncio
async def test_get_breed_by_id_not_found():
    """Test getting a breed that doesn't exist."""
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        cat_service = CatService()
        breed = await cat_service.get_breed_by_id("nonexistent")
        
        assert breed is None


@pytest.mark.asyncio
async def test_search_breeds():
    """Test searching for cat breeds."""
    mock_response_data = [
        {
            "id": "abys",
            "name": "Abyssinian",
            "description": "The Abyssinian is easy to care for...",
            "origin": "Egypt"
        }
    ]
    
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status = MagicMock()
        
        mock_context = AsyncMock()
        mock_context.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_context
        
        cat_service = CatService()
        search_params = CatBreedSearchParams(q="Abyssinian", limit=5)
        breeds = await cat_service.search_breeds(search_params)
        
        assert len(breeds) == 1
        assert breeds[0].name == "Abyssinian"
