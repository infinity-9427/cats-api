from typing import Optional
from pydantic import BaseModel, Field, field_serializer
from datetime import datetime, timezone


class User(BaseModel):
    """User model for database storage."""
    id: Optional[str] = Field(default=None, alias="_id")
    first_name: str
    last_name: str
    username: str
    password: str
    email: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    model_config = {
        "populate_by_name": True,
    }
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()
