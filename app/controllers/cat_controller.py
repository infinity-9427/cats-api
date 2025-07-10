from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas.cat import CatBreedResponse, CatBreedSearchParams
from app.services.cat_service import CatService


router = APIRouter(prefix="/api/v1", tags=["breeds"])


def get_cat_service():
    """Dependency to get cat service."""
    return CatService()


@router.get("/breeds/search", response_model=List[CatBreedResponse])
async def search_breeds(
    q: Optional[str] = Query(None, description="Search query"),
    limit: Optional[int] = Query(10, description="Limit results", ge=1, le=100),
    attach_breed: Optional[int] = Query(0, description="Attach breed information"),
    cat_service: CatService = Depends(get_cat_service)
):
    """Search cat breeds."""
    try:
        search_params = CatBreedSearchParams(
            q=q,
            limit=limit,
            attach_breed=attach_breed
        )
        return await cat_service.search_breeds(search_params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching breeds: {str(e)}"
        )


@router.get("/breeds/{breed_id}", response_model=CatBreedResponse)
async def get_breed_by_id(
    breed_id: str,
    cat_service: CatService = Depends(get_cat_service)
):
    """Get specific breed by ID."""
    try:
        breed = await cat_service.get_breed_by_id(breed_id)
        if not breed:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Breed with ID '{breed_id}' not found"
            )
        return breed
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching breed: {str(e)}"
        )


@router.get("/breeds", response_model=List[CatBreedResponse])
async def get_all_breeds(cat_service: CatService = Depends(get_cat_service)):
    """Get all cat breeds."""
    try:
        return await cat_service.get_all_breeds()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching cat breeds: {str(e)}"
        )
