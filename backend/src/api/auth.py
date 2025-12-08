from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel, Field
from ...models.user import UserCreate, UserLogin, UserLoginResponse, UserProfileResponse, UserUpdate
from ...services.auth_service import auth_service
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

@router.get("/profile", response_model=UserProfileResponse, responses={
    200: {"description": "Profile retrieved successfully"},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_profile(request: Request):
    """Get the authenticated user's profile information."""
    try:
        # This is a simplified implementation - in a real app, you'd validate the session token
        # from the Authorization header or cookies
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # In a real implementation, you would validate the session token against a database
        # For this example, we'll skip validation and return a mock user
        # This requires proper session management that would be implemented in a full system

        # For now, we'll return an error indicating that proper session validation
        # needs to be implemented
        raise HTTPException(status_code=501, detail="Session validation not fully implemented in this example")
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
async def update_profile(request: Request, update_data: UserUpdate):
    """Update the authenticated user's profile information."""
    try:
        # This is a simplified implementation - in a real app, you'd validate the session token
        # from the Authorization header or cookies
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # For this example, we'll use a mock user ID
        # In a real implementation, you would look up the user ID from the session token
        raise HTTPException(status_code=501, detail="Session validation not fully implemented in this example")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in update profile endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error updating profile")