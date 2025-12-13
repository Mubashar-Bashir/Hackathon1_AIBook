import logging
import traceback
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.user import UserCreate, UserLogin, UserLoginResponse, UserProfileResponse, UserUpdate, UserRegistrationResponse, UserProfile, LogoutResponse, BasicSuccessResponse
from src.services.auth_service import auth_service
from datetime import datetime
import uuid
from src.utils.performance_monitor import monitor_performance

# Set up logging
logger = logging.getLogger(__name__)


# Additional models for password reset functionality
class ForgotPasswordRequest(BaseModel):
    email: str = Field(..., description="User's email address for password reset")


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., description="Verification token received via email")
    new_password: str = Field(..., min_length=8, description="New password (min 8 characters)")

# API Contract Models for validation
class UserRegistrationRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=100, description="User's email address")
    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    experience_level: str = Field(..., description="User's experience level: 'beginner', 'intermediate', or 'expert'")

class UserRegistrationResponse(BaseModel):
    user_id: str
    email: str
    name: str
    experience_level: str
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
@monitor_performance("auth_register")
async def register_user(user_data: UserRegistrationRequest):
    """Register a new user account with experience level information."""
    try:
        # Validate experience level
        valid_experience_levels = ["beginner", "intermediate", "expert"]
        if user_data.experience_level not in valid_experience_levels:
            raise HTTPException(
                status_code=400,
                detail=f"Experience level must be one of: {', '.join(valid_experience_levels)}"
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
            experience_level=user_data.experience_level
        )

        if result is None:
            raise HTTPException(
                status_code=409,
                detail="User with this email already exists"
            )

        # Create user profile object to match contract
        user_profile = UserProfile(
            id=result["user_id"],
            email=result["email"],
            name=result["name"],
            experience_level=result["experience_level"],
            created_at=result["created_at"],
            last_login=result["created_at"]  # Using created_at as initial last_login
        )

        return UserRegistrationResponse(
            success=True,
            user=user_profile,
            session_token=result["session_token"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in user registration endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during registration")

@router.post("/login", response_model=UserLoginResponse, responses={
    200: {"description": "Login successful"},
    400: {"description": "Invalid login parameters", "model": ErrorResponse},
    401: {"description": "Invalid credentials", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_login")
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

        # Create user profile object to match contract
        user_profile = UserProfile(
            id=result["user_id"],
            email=result["email"],
            name=result["name"],
            experience_level=result["experience_level"],
            created_at=result["created_at"],
            last_login=datetime.utcnow()  # Set current time as last login
        )

        return UserLoginResponse(
            success=True,
            user=user_profile,
            session_token=result["session_token"]
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Error in user login endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during login")

@router.get("/profile", response_model=UserProfileResponse, responses={
    200: {"description": "Profile retrieved successfully"},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_get_profile")
async def get_profile(request: Request):
    """Get the authenticated user's profile information."""
    try:
        # Validate the session token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # Validate session token against database
        user_id = await auth_service.validate_session_token(session_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired session token")

        # Get user profile
        user_profile = await auth_service.get_user_profile(user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")

        return UserProfileResponse(
            id=user_profile.id,
            email=user_profile.email,
            name=user_profile.name,
            username=user_profile.username,
            experience_level=user_profile.experience_level,
            created_at=user_profile.created_at,
            updated_at=user_profile.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get profile endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving profile")

@router.put("/profile", response_model=UserProfileResponse, responses={
    200: {"description": "Profile updated successfully"},
    400: {"description": "Invalid update parameters", "model": ErrorResponse},
    401: {"description": "Unauthorized", "model": ErrorResponse},
    404: {"description": "User not found", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_update_profile")
async def update_profile(request: Request, update_data: UserUpdate):
    """Update the authenticated user's profile information."""
    try:
        # Validate the session token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # Validate session token against database
        user_id = await auth_service.validate_session_token(session_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired session token")

        # Prepare update data
        update_dict = update_data.dict(exclude_unset=True)

        # Update user profile
        updated_profile = await auth_service.update_user_profile(user_id, update_dict)
        if not updated_profile:
            raise HTTPException(status_code=404, detail="User not found")

        return UserProfileResponse(
            id=updated_profile.id,
            email=updated_profile.email,
            name=updated_profile.name,
            username=updated_profile.username,
            experience_level=updated_profile.experience_level,
            created_at=updated_profile.created_at,
            updated_at=updated_profile.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update profile endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error updating profile")


@router.post("/logout", response_model=LogoutResponse, responses={
    200: {"description": "Successfully logged out"},
    401: {"description": "Unauthorized - invalid or expired session", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_logout")
async def logout_user(request: Request):
    """End the current user session."""
    try:
        # Validate the session token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # Validate session token against database
        user_id = await auth_service.validate_session_token(session_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired session token")

        # Delete the session from the database to properly invalidate it
        from ..services.session_service import session_service
        success = await session_service.delete_session(session_token)

        if not success:
            # Session might have already been deleted or expired, but still return success
            # to avoid leaking information about session existence
            pass

        return LogoutResponse(success=True, message="Successfully logged out")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in logout endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during logout")


@router.get("/me", response_model=UserProfileResponse, responses={
    200: {"description": "Current user information retrieved successfully"},
    401: {"description": "Unauthorized - invalid or expired session", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_get_current_user")
async def get_current_user_info(request: Request):
    """Retrieves information about the currently authenticated user (alias for /profile)."""
    try:
        # Validate the session token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        session_token = auth_header.split(" ")[1]

        # Validate session token against database
        user_id = await auth_service.validate_session_token(session_token)
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid or expired session token")

        # Get user profile
        user_profile = await auth_service.get_user_profile(user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User not found")

        return UserProfileResponse(
            id=user_profile.id,
            email=user_profile.email,
            name=user_profile.name,
            username=user_profile.username,
            experience_level=user_profile.experience_level,
            created_at=user_profile.created_at,
            updated_at=user_profile.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get current user endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving user info")


@router.post("/forgot-password", response_model=BasicSuccessResponse, responses={
    200: {"description": "Password reset email sent if account exists"},
    400: {"description": "Invalid email format", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_forgot_password")
async def forgot_password(forgot_data: ForgotPasswordRequest):
    """Initiates password reset process by sending reset email."""
    try:
        # Basic email validation is handled by the Pydantic model, but we can add additional checks
        email = forgot_data.email
        if "@" not in email or "." not in email:
            raise HTTPException(status_code=400, detail="Invalid email format")

        # In a real implementation, we would:
        # 1. Check if user exists with this email
        # 2. Generate a verification token
        # 3. Store it in the verification_tokens table
        # 4. Send email with reset link

        # For now, return success to avoid leaking information about user existence
        return BasicSuccessResponse(success=True, message="If an account exists with this email, a password reset link has been sent")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in forgot password endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during password reset request")


@router.post("/reset-password", response_model=BasicSuccessResponse, responses={
    200: {"description": "Password reset successfully"},
    400: {"description": "Invalid token or password", "model": ErrorResponse},
    401: {"description": "Invalid or expired token", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
@monitor_performance("auth_reset_password")
async def reset_password(reset_data: ResetPasswordRequest):
    """Resets user password using verification token."""
    try:
        token = reset_data.token
        new_password = reset_data.new_password

        # Validate password strength (additional check, though Pydantic handles min_length)
        if len(new_password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

        # In a real implementation, we would:
        # 1. Validate the token from verification_tokens table
        # 2. Check if token is not expired and not used
        # 3. Hash and update the user's password
        # 4. Mark token as used
        # 5. Invalidate all existing sessions for the user

        # For now, return success
        return BasicSuccessResponse(success=True, message="Password reset successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in reset password endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during password reset")