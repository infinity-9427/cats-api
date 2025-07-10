from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class CatBreed(BaseModel):
    """Cat breed model from The Cat API."""
    id: str
    name: str
    description: Optional[str] = None
    temperament: Optional[str] = None
    origin: Optional[str] = None
    country_code: Optional[str] = None
    country_codes: Optional[str] = None
    life_span: Optional[str] = None
    indoor: Optional[int] = None
    lap: Optional[int] = None
    alt_names: Optional[str] = None
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
    experimental: Optional[int] = None
    hairless: Optional[int] = None
    natural: Optional[int] = None
    rare: Optional[int] = None
    rex: Optional[int] = None
    suppressed_tail: Optional[int] = None
    short_legs: Optional[int] = None
    wikipedia_url: Optional[str] = None
    hypoallergenic: Optional[int] = None
    reference_image_id: Optional[str] = None
    image: Optional[Dict[str, Any]] = None
    weight: Optional[Dict[str, str]] = None
    
    model_config = {"extra": "allow"}
