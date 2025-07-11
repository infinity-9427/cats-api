from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.user_service import UserService
from app.repositories.user_repository import MongoUserRepository
from app.core.database import get_database
from app.core.security import create_access_token, require_authentication
from datetime import timedelta
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


@router.post("/login", response_model=Token)
async def login_user(
    user_login: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Login user and return JWT token."""
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
