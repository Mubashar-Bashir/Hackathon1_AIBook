from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.personalization import ApplyPersonalizationRequest, ApplyPersonalizationResponse, GetPersonalizedChapterResponse
from src.services.personalization_service import personalization_service
from datetime import datetime
import uuid

# API Contract Models for validation
class GetPersonalizedChapterRequest(BaseModel):
    background: Optional[str] = Field(default=None, description="Override user's background ('beginner', 'intermediate', 'expert')")

class ApplyPersonalizationResponseModel(BaseModel):
    original_content: str
    personalized_content: str
    user_background: str
    personalization_type: str
    timestamp: datetime

class GetPersonalizedChapterResponseModel(BaseModel):
    chapter_id: str
    original_title: str
    original_content: str
    personalized_title: Optional[str]
    personalized_content: Optional[str]
    background_level: str
    personalization_applied: bool
    timestamp: datetime

class GetUserBackgroundResponse(BaseModel):
    user_id: str
    background: str
    preferences: dict
    timestamp: datetime

class ErrorResponse(BaseModel):
    error: str
    code: str

router = APIRouter(prefix="/api/personalization", tags=["personalization"])

@router.get("/chapter/{chapter_id}", response_model=GetPersonalizedChapterResponseModel, responses={
    200: {"description": "Personalized chapter retrieved successfully"},
    400: {"description": "Invalid parameters", "model": ErrorResponse},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_personalized_chapter(chapter_id: str, request: Request, background: Optional[str] = None):
    """Get personalized content for a specific chapter based on the user's background."""
    try:
        # Validate background if provided
        if background:
            valid_backgrounds = ["beginner", "intermediate", "expert"]
            if background not in valid_backgrounds:
                raise HTTPException(
                    status_code=400,
                    detail=f"Background must be one of: {', '.join(valid_backgrounds)}"
                )

        # In a real implementation, we would validate the session token here
        # For this example, we'll simulate with a default background
        user_background = background or "intermediate"  # Would come from authenticated user in real implementation

        result = await personalization_service.get_personalized_chapter(
            chapter_id=chapter_id,
            user_background=user_background
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Error generating personalized content"
            )

        return GetPersonalizedChapterResponseModel(
            chapter_id=result["chapter_id"],
            original_title=result["original_title"],
            original_content=result["original_content"],
            personalized_title=result["personalized_title"],
            personalized_content=result["personalized_content"],
            background_level=result["background_level"],
            personalization_applied=result["personalization_applied"],
            timestamp=result["timestamp"]
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get personalized chapter endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving personalized chapter")

@router.post("/apply", response_model=ApplyPersonalizationResponseModel, responses={
    200: {"description": "Content personalized successfully"},
    400: {"description": "Invalid parameters", "model": ErrorResponse},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def apply_personalization(request: ApplyPersonalizationRequest):
    """Apply personalization to provided content based on user background."""
    try:
        # Validate background if provided
        if request.user_background:
            valid_backgrounds = ["beginner", "intermediate", "expert"]
            if request.user_background not in valid_backgrounds:
                raise HTTPException(
                    status_code=400,
                    detail=f"Background must be one of: {', '.join(valid_backgrounds)}"
                )

        # Validate personalization type
        valid_types = ["simplification", "elaboration", "examples", "all"]
        if request.personalization_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Personalization type must be one of: {', '.join(valid_types)}"
            )

        # In a real implementation, user_background would come from authenticated user
        # For this example, we'll use the value from the request or default to intermediate
        user_background = request.user_background or "intermediate"

        result = await personalization_service.apply_personalization(
            ApplyPersonalizationRequest(
                content=request.content,
                user_background=user_background,
                personalization_type=request.personalization_type
            )
        )

        if not result:
            raise HTTPException(
                status_code=500,
                detail="Error generating personalized content"
            )

        return ApplyPersonalizationResponseModel(
            original_content=result.original_content,
            personalized_content=result.personalized_content,
            user_background=result.user_background,
            personalization_type=result.personalization_type,
            timestamp=result.timestamp
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in apply personalization endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error applying personalization")

@router.get("/user-background", response_model=GetUserBackgroundResponse, responses={
    200: {"description": "User background retrieved successfully"},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_user_background(request: Request):
    """Get the current user's background information."""
    try:
        # In a real implementation, we would validate the session token here
        # and retrieve the user's background from the database
        # For this example, we'll return mock data
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        # Mock user data for example
        return GetUserBackgroundResponse(
            user_id="mock-user-id",
            background="intermediate",
            preferences={"theme": "light", "language": "en"},
            timestamp=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get user background endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving user background")