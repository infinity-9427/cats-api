from typing import List, Optional
import httpx
from app.models.cat import CatBreed
from app.schemas.cat import CatBreedResponse, CatBreedSearchParams
from app.core.config import settings


class CatService:
    """Service layer for cat breed operations."""
    
    def __init__(self):
        self.base_url = settings.CATS_API_BASE_URL
        self.api_key = settings.CATS_API_KEY
        self.headers = {"x-api-key": self.api_key}
    
    def _convert_to_response(self, breed_data: dict) -> CatBreedResponse:
        """Convert API response to CatBreedResponse."""
        image_url = None
        if breed_data.get("image"):
            image_url = breed_data["image"].get("url")
        elif breed_data.get("reference_image_id"):
            image_url = f"https://cdn2.thecatapi.com/images/{breed_data['reference_image_id']}.jpg"
        
        return CatBreedResponse(
            id=breed_data.get("id", ""),
            name=breed_data.get("name", ""),
            description=breed_data.get("description"),
            temperament=breed_data.get("temperament"),
            origin=breed_data.get("origin"),
            life_span=breed_data.get("life_span"),
            wikipedia_url=breed_data.get("wikipedia_url"),
            image_url=image_url,
            adaptability=breed_data.get("adaptability"),
            affection_level=breed_data.get("affection_level"),
            child_friendly=breed_data.get("child_friendly"),
            dog_friendly=breed_data.get("dog_friendly"),
            energy_level=breed_data.get("energy_level"),
            grooming=breed_data.get("grooming"),
            health_issues=breed_data.get("health_issues"),
            intelligence=breed_data.get("intelligence"),
            shedding_level=breed_data.get("shedding_level"),
            social_needs=breed_data.get("social_needs"),
            stranger_friendly=breed_data.get("stranger_friendly"),
            vocalisation=breed_data.get("vocalisation")
        )
    
    async def get_all_breeds(self) -> List[CatBreedResponse]:
        """Get all cat breeds."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/breeds",
                headers=self.headers
            )
            response.raise_for_status()
            breeds_data = response.json()
            
            return [self._convert_to_response(breed) for breed in breeds_data]
    
    async def get_breed_by_id(self, breed_id: str) -> Optional[CatBreedResponse]:
        """Get specific breed by ID."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/breeds/{breed_id}",
                headers=self.headers
            )
            
            if response.status_code in [404, 400]:
                return None
                
            response.raise_for_status()
            breed_data = response.json()
            
            return self._convert_to_response(breed_data)
    
    async def search_breeds(self, search_params: CatBreedSearchParams) -> List[CatBreedResponse]:
        """Search cat breeds."""
        params = {}
        if search_params.q:
            params["q"] = search_params.q
        if search_params.limit:
            params["limit"] = search_params.limit
        if search_params.attach_breed:
            params["attach_breed"] = search_params.attach_breed
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/breeds/search",
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            breeds_data = response.json()
            
            return [self._convert_to_response(breed) for breed in breeds_data]
