from fastapi import Request, HTTPException, Depends
from typing import Dict, Any, Optional
import jwt
from ..config import settings
from ..services.auth_service import auth_service
from ..models.user import UserResponse


async def get_current_user(request: Request) -> Optional[UserResponse]:
    """
    Dependency to get the current authenticated user from the request.

    Args:
        request: FastAPI request object containing headers

    Returns:
        UserResponse object if authenticated, None otherwise
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    token = auth_header.split(" ")[1]

    try:
        # Validate the token format
        if len(token) < 10:  # Basic validation
            raise HTTPException(
                status_code=401,
                detail="Invalid token format"
            )

        # Use the auth service to validate the session token and get user info
        user = await auth_service.validate_session_token(token)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired session token"
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error validating session token: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error validating authentication token"
        )


async def require_authentication(request: Request) -> bool:
    """
    Dependency to require authentication for protected endpoints.

    Args:
        request: FastAPI request object

    Returns:
        True if authenticated, raises HTTPException otherwise
    """
    user = await get_current_user(request)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )
    return True