from typing import Optional
from pydantic import BaseModel, Field, field_validator, field_serializer
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    first_name: str = Field(..., min_length=1, max_length=50, description="First name")
    last_name: str = Field(..., min_length=1, max_length=50, description="Last name")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")
    email: Optional[str] = None
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserResponse(BaseModel):
    """Schema for user response."""
    id: Optional[str] = None
    first_name: str
    last_name: str
    username: str
    email: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    @field_serializer('created_at', 'updated_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str
    password: str


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Schema for token data (useful for token validation)."""
    username: Optional[str] = None
    expires_at: Optional[datetime] = None


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request (for future use)."""
    refresh_token: str


class TokenInfo(BaseModel):
    """Schema for token information (for future debugging/admin purposes)."""
    username: str
    expires_at: datetime
    issued_at: datetime
    is_valid: bool
    
    @field_serializer('expires_at', 'issued_at')
    def serialize_datetime(self, value: datetime) -> str:
        """Serialize datetime to ISO format string."""
        return value.isoformat()
