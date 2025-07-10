from typing import Optional, List
from pydantic import BaseModel


class CatBreedResponse(BaseModel):
    """Schema for cat breed response."""
    id: str
    name: str
    description: Optional[str] = None
    temperament: Optional[str] = None
    origin: Optional[str] = None
    life_span: Optional[str] = None
    wikipedia_url: Optional[str] = None
    image_url: Optional[str] = None
    adaptability: Optional[int] = None
    affection_level: Optional[int] = None
    child_friendly: Optional[int] = None
    dog_friendly: Optional[int] = None
    energy_level: Optional[int] = None
    grooming: Optional[int] = None
    health_issues: Optional[int] = None
    intelligence: Optional[int] = None
    shedding_level: Optional[int] = None
    social_needs: Optional[int] = None
    stranger_friendly: Optional[int] = None
    vocalisation: Optional[int] = None


class CatBreedSearchParams(BaseModel):
    """Schema for cat breed search parameters."""
    q: Optional[str] = None  # Search query
    limit: Optional[int] = 10
    attach_breed: Optional[int] = 0
