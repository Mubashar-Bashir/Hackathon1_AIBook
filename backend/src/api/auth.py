from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.user import UserCreate, UserLogin, UserLoginResponse, UserProfileResponse, UserUpdate
from src.services.auth_service import auth_service
from datetime import datetime
import uuid

# API Contract Models for validation
class UserRegistrationRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=100, description="User's email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    background: str = Field(..., description="User's experience level: 'beginner', 'intermediate', or 'expert'")

class UserRegistrationResponse(BaseModel):
    user_id: str
    email: str
    name: str
    background: str
    session_token: str
    created_at: datetime

class ErrorResponse(BaseModel):
    error: str
    code: str

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserRegistrationResponse, responses={
    200: {"description": "User registered successfully"},
    400: {"description": "Invalid registration parameters", "model": ErrorResponse},
    409: {"description": "User already exists", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def register_user(user_data: UserRegistrationRequest):
    """Register a new user account with background information."""
    try:
        # Validate background level
        valid_backgrounds = ["beginner", "intermediate", "expert"]
        if user_data.background not in valid_backgrounds:
            raise HTTPException(
                status_code=400,
                detail=f"Background must be one of: {', '.join(valid_backgrounds)}"
            )

        # Validate email format (basic validation)
        if "@" not in user_data.email or "." not in user_data.email:
            raise HTTPException(
                status_code=400,
                detail="Invalid email format"
            )

        # Validate password strength (basic validation)
        if len(user_data.password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long"
            )

        # Attempt to register the user
        result = await auth_service.register_user(
            email=user_data.email,
            name=user_data.name,
            password=user_data.password,
            background=user_data.background
        )

        if result is None:
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists"
            )

        return UserRegistrationResponse(
            user_id=result["user_id"],
            email=result["email"],
            name=result["name"],
            background=result["background"],
            session_token=result["session_token"],
            created_at=result["created_at"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in user registration endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during registration")

@router.post("/login", response_model=UserLoginResponse, responses={
    200: {"description": "Login successful"},
    400: {"description": "Invalid login parameters", "model": ErrorResponse},
    401: {"description": "Invalid credentials", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def login_user(login_data: UserLogin):
    """Authenticate a user and return a session token."""
    try:
        # Attempt to authenticate the user
        result = await auth_service.authenticate_user(
            email=login_data.email,
            password=login_data.password
        )

        if result is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        return UserLoginResponse(
            user_id=result["user_id"],
            email=result["email"],
            name=result["name"],
            background=result["background"],
            session_token=result["session_token"],
            created_at=result["created_at"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in user login endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during login")

from src.api.auth_deps import get_current_user

@router.get("/profile", response_model=UserProfileResponse, responses={
    200: {"description": "Profile retrieved successfully"},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_profile(current_user=Depends(get_current_user)):
    """Get the authenticated user's profile information."""
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not authenticated")

        # Return the user profile data
        return UserProfileResponse(
            user_id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            background=current_user.background,
            preferences=current_user.preferences if current_user.preferences else {},
            created_at=current_user.created_at,
            updated_at=current_user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get profile endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving profile")

@router.put("/profile", response_model=UserProfileResponse, responses={
    200: {"description": "Profile updated successfully"},
    400: {"description": "Invalid update parameters", "model": ErrorResponse},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def update_profile(current_user=Depends(get_current_user), update_data: UserUpdate = None):
    """Update the authenticated user's profile information."""
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not authenticated")

        # Update the user profile using the auth service
        update_dict = update_data.dict(exclude_unset=True)
        updated_user = await auth_service.update_user_profile(current_user.id, update_dict)

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Return the updated user profile data
        return UserProfileResponse(
            user_id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            background=updated_user.background,
            preferences=updated_user.preferences if updated_user.preferences else {},
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update profile endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error updating profile")


@router.post("/logout", responses={
    200: {"description": "Logout successful"},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def logout_user(request: Request):
    """Logout the authenticated user and invalidate their session token."""
    try:
        # Validate the session token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # Attempt to logout the user (invalidate session)
        success = await auth_service.logout_user(session_token)

        if success:
            return {"message": "Successfully logged out"}
        else:
            raise HTTPException(status_code=500, detail="Error during logout process")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in logout endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during logout")