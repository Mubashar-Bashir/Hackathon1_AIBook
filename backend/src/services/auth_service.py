import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ..models.user import UserResponse
from ..utils.database import get_db_session
from ..config import settings
import uuid

class AuthService:
    def __init__(self):
        self.session_timeout = 3600 * 24 * 7  # 1 week in seconds

    def hash_password(self, password: str) -> str:
        """Hash a password with a salt."""
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}:{pwdhash.hex()}"

    def verify_password(self, password: str, stored_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            salt, pwdhash = stored_password.split(':')
            computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return secrets.compare_digest(computed_hash.hex(), pwdhash)
        except Exception:
            return False

    def generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(32)

    async def register_user(self, email: str, name: str, password: str, background: str) -> Optional[Dict[str, Any]]:
        """Register a new user with BetterAuth integration."""
        try:
            from sqlalchemy.exc import IntegrityError
            from ..models.user import UserCreate, UserResponse
            from sqlalchemy import select

            # Import here to avoid circular dependencies
            from ..utils.database import Base
            async with get_db_session() as db:
                # Check if user already exists
                result = await db.execute(select(Base.classes.users).filter_by(email=email))
                existing_user = result.scalars().first()

                if existing_user:
                    return None  # User already exists

                # Hash the password
                hashed_password = self.hash_password(password)

                # Create new user
                new_user = Base.classes.users(
                    id=str(uuid.uuid4()),
                    email=email,
                    name=name,
                    background=background,
                    password_hash=hashed_password,  # Note: This assumes we add password_hash to User model
                    preferences="{}"  # Default empty preferences
                )

                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)

                # Generate session token
                session_token = self.generate_session_token()

                return {
                    "user_id": new_user.id,
                    "email": new_user.email,
                    "name": new_user.name,
                    "background": new_user.background,
                    "session_token": session_token,
                    "created_at": new_user.created_at
                }
        except Exception as e:
            print(f"Error registering user: {e}")
            return None

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with BetterAuth integration."""
        try:
            from sqlalchemy import select
            from ..utils.database import Base

            async with get_db_session() as db:
                result = await db.execute(select(Base.classes.users).filter_by(email=email))
                user = result.scalars().first()

                if not user or not self.verify_password(password, user.password_hash):
                    return None

                # Generate session token
                session_token = self.generate_session_token()

                return {
                    "user_id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "background": user.background,
                    "session_token": session_token,
                    "created_at": user.created_at
                }
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return None

    async def get_user_profile(self, user_id: str) -> Optional[UserResponse]:
        """Get user profile information."""
        try:
            from sqlalchemy import select
            from ..utils.database import Base

            async with get_db_session() as db:
                result = await db.execute(select(Base.classes.users).filter_by(id=user_id))
                user = result.scalars().first()

                if not user:
                    return None

                return UserResponse(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    background=user.background,
                    preferences=user.preferences,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None

    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Optional[UserResponse]:
        """Update user profile information."""
        try:
            from sqlalchemy import select, update
            from ..utils.database import Base

            async with get_db_session() as db:
                # Get current user
                result = await db.execute(select(Base.classes.users).filter_by(id=user_id))
                user = result.scalars().first()

                if not user:
                    return None

                # Update user fields
                if 'name' in update_data and update_data['name']:
                    user.name = update_data['name']
                if 'background' in update_data and update_data['background']:
                    user.background = update_data['background']
                if 'preferences' in update_data:
                    user.preferences = str(update_data['preferences'])

                await db.commit()
                await db.refresh(user)

                return UserResponse(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    background=user.background,
                    preferences=user.preferences,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                )
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return None

# Global instance
auth_service = AuthService()