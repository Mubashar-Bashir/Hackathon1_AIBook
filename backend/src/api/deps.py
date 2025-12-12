from fastapi import Request, HTTPException, Depends
from typing import Optional
from ..services.auth_service import auth_service


async def get_current_user(request: Request):
    """
    Dependency to get the current authenticated user from the request.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = auth_header.split(" ")[1]

    user_id = await auth_service.validate_session_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired session token")

    # Get user profile using the user_id
    user_profile = await auth_service.get_user_profile(user_id)
    if not user_profile:
        raise HTTPException(status_code=401, detail="User not found")

    return user_profile


# Alias for consistency with common FastAPI patterns
get_current_active_user = get_current_user