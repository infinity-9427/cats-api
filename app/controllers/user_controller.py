from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, TokenInfo
from app.services.user_service import UserService
from app.repositories.user_repository import MongoUserRepository
from app.core.database import get_database
from app.core.security import create_access_token, get_current_user_username, require_authentication, get_token_payload
from datetime import timedelta, datetime
from app.core.config import settings


router = APIRouter(prefix="/api/v1", tags=["users"])


async def get_user_service():
    """Dependency to get user service."""
    database = await get_database()
    user_repository = MongoUserRepository(database)
    return UserService(user_repository)


@router.get("/user", response_model=List[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """Get all users."""
    return await user_service.get_all_users()


@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    try:
        return await user_service.create_user(user_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/login", response_model=Token)
async def login_user_get(
    username: str = Query(..., description="Username"),
    password: str = Query(..., description="Password"),
    user_service: UserService = Depends(get_user_service)
):
    """Login user and return JWT token (GET method for convenience)."""
    user = await user_service.authenticate_user(username, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.post("/login", response_model=Token)
async def login_user_post(
    user_login: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Login user and return JWT token (POST method - REST standard)."""
    user = await user_service.authenticate_user(user_login.username, user_login.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user
    )


@router.get("/auth/verify", response_model=dict)
async def verify_token(
    current_user: Optional[str] = Depends(get_current_user_username)
):
    """Verify if the current token is valid (useful for frontend)."""
    if current_user:
        return {
            "valid": True,
            "username": current_user,
            "message": "Token is valid"
        }
    else:
        return {
            "valid": False,
            "username": None,
            "message": "No valid token provided"
        }


@router.get("/auth/me", response_model=UserResponse)
async def get_current_user(
    current_user: str = Depends(require_authentication),
    user_service: UserService = Depends(get_user_service)
):
    """Get current user information (requires authentication)."""
    user = await user_service.get_user_by_username(current_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/auth/token-info", response_model=TokenInfo)
async def get_token_info(
    current_user: str = Depends(require_authentication),
    user_service: UserService = Depends(get_user_service)
):
    """Get token information (for debugging/admin purposes)."""
    # This would typically get the token from the Authorization header
    # For now, we'll create a basic response
    return TokenInfo(
        username=current_user,
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        issued_at=datetime.utcnow(),
        is_valid=True
    )
