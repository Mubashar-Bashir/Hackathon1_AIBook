import hashlib
import secrets
import logging
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from ..models.user import UserResponse
from ..utils.database import get_db_session
from ..config import settings
import uuid

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

    async def register_user(self, email: str, name: str, password: str, experience_level: str) -> Optional[Dict[str, Any]]:
        """Register a new user with custom authentication integration."""
        logger.info(f"Attempting to register user: {email}")
        try:
            from sqlalchemy.exc import IntegrityError
            from ..models.user import UserCreate, UserResponse, User
            from sqlalchemy import select
            import re

            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not email or not re.match(email_pattern, email):
                logger.warning(f"Registration failed: Invalid email format: {email}")
                return None

            # Validate password strength (basic validation)
            if len(password) < 8:
                logger.warning(f"Registration failed: Password too short: {email}")
                return None

            # Validate experience level
            valid_experience_levels = ["beginner", "intermediate", "expert"]
            if experience_level not in valid_experience_levels:
                logger.warning(f"Registration failed: Invalid experience level: {experience_level} for user: {email}")
                return None

            # Validate name
            if not name or len(name.strip()) == 0:
                logger.warning(f"Registration failed: Invalid name: {email}")
                return None

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                # Check if user already exists
                result = await db.execute(select(User).filter_by(email=email))
                existing_user = result.scalars().first()

                if existing_user:
                    logger.warning(f"Registration failed: User already exists: {email}")
                    return None  # User already exists

                # Hash the password
                hashed_password = self.hash_password(password)
                logger.debug(f"Password hashed for user: {email}")

                # Create new user
                new_user = User(
                    email=email,
                    name=name,
                    experience_level=experience_level,
                    password_hash=hashed_password,
                    preferences="{}"  # Default empty preferences
                )

                db.add(new_user)
                await db.commit()
                await db.refresh(new_user)
                logger.info(f"User registered successfully: {email}")

                # Generate session token
                session_token = self.generate_session_token()
                logger.debug(f"Session token generated for user: {email}")

                # Create session record in the database
                from ..models.session import Session
                from datetime import datetime, timedelta
                session_expires = datetime.utcnow() + timedelta(days=7)  # 1 week expiry

                session_record = Session(
                    user_id=new_user.id,
                    session_token=session_token,
                    expires_at=session_expires
                )

                db.add(session_record)
                await db.commit()
                logger.info(f"Session record created for user: {email}")

                return {
                    "user_id": new_user.id,
                    "email": new_user.email,
                    "name": new_user.name,
                    "experience_level": new_user.experience_level,
                    "session_token": session_token,
                    "created_at": new_user.created_at
                }
            finally:
                # Close the session properly
                await db_gen.aclose()
        except IntegrityError as e:
            logger.error(f"Database integrity error during registration for {email}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error registering user {email}: {e}")
            return None

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with custom authentication integration."""
        logger.info(f"Attempting to authenticate user: {email}")
        try:
            from sqlalchemy import select
            from ..models.user import User
            import re

            # Validate email format
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not email or not re.match(email_pattern, email):
                logger.warning(f"Authentication failed: Invalid email format: {email}")
                return None

            # Validate password
            if not password:
                logger.warning(f"Authentication failed: Empty password for user: {email}")
                return None

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                result = await db.execute(select(User).filter_by(email=email))
                user = result.scalars().first()

                if not user:
                    logger.warning(f"Authentication failed: User not found: {email}")
                    return None

                if not self.verify_password(password, user.password_hash):
                    logger.warning(f"Authentication failed: Invalid password for user: {email}")
                    return None

                logger.info(f"User authenticated successfully: {email}")

                # Generate session token
                session_token = self.generate_session_token()
                logger.debug(f"Session token generated for authenticated user: {email}")

                # Create session record in the database
                from ..models.session import Session
                from datetime import datetime, timedelta
                session_expires = datetime.utcnow() + timedelta(days=7)  # 1 week expiry

                session_record = Session(
                    user_id=user.id,
                    session_token=session_token,
                    expires_at=session_expires
                )

                db.add(session_record)
                await db.commit()
                logger.info(f"Session record created for authenticated user: {email}")

                return {
                    "user_id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "experience_level": user.experience_level,
                    "session_token": session_token,
                    "created_at": user.created_at
                }
            finally:
                # Close the session properly
                await db_gen.aclose()
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None

    async def get_user_profile(self, user_id: str) -> Optional[UserResponse]:
        """Get user profile information."""
        logger.debug(f"Getting user profile for user_id: {user_id}")
        try:
            from sqlalchemy import select
            from ..models.user import User, UserResponse

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                result = await db.execute(select(User).filter_by(id=user_id))
                user = result.scalars().first()

                if not user:
                    logger.warning(f"User profile not found for user_id: {user_id}")
                    return None

                logger.debug(f"User profile retrieved for user_id: {user_id}")
                # Handle preferences - it's stored as a string in DB but should be returned as a dict
                preferences_dict = {}
                if user.preferences:
                    try:
                        # Try to parse as JSON if it's a string
                        if isinstance(user.preferences, str):
                            preferences_dict = json.loads(user.preferences) if user.preferences.strip() else {}
                        else:
                            preferences_dict = user.preferences
                    except json.JSONDecodeError:
                        # If JSON parsing fails, use as-is or empty dict
                        preferences_dict = {}

                return UserResponse(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    username=user.username,
                    experience_level=user.experience_level,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    preferences=preferences_dict,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    last_login=user.last_login
                )
            finally:
                # Close the session properly
                await db_gen.aclose()
        except Exception as e:
            logger.error(f"Error getting user profile for user_id {user_id}: {e}")
            return None

    async def update_user_profile(self, user_id: str, update_data: Dict[str, Any]) -> Optional[UserResponse]:
        """Update user profile information."""
        logger.debug(f"Updating user profile for user_id: {user_id}")
        try:
            from sqlalchemy import select
            from ..models.user import User, UserResponse

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                # Get current user
                result = await db.execute(select(User).filter_by(id=user_id))
                user = result.scalars().first()

                if not user:
                    logger.warning(f"Cannot update profile: User not found for user_id: {user_id}")
                    return None

                # Update user fields
                original_data = {
                    'name': user.name,
                    'experience_level': user.experience_level,
                    'username': user.username,
                    'preferences': user.preferences,
                    'is_active': user.is_active,
                    'is_verified': user.is_verified,
                    'last_login': user.last_login
                }

                if 'name' in update_data and update_data['name']:
                    user.name = update_data['name']
                if 'experience_level' in update_data and update_data['experience_level']:
                    user.experience_level = update_data['experience_level']
                if 'username' in update_data and update_data['username']:
                    user.username = update_data['username']
                if 'preferences' in update_data:
                    user.preferences = str(update_data['preferences'])
                if 'is_active' in update_data:
                    user.is_active = update_data['is_active']
                if 'is_verified' in update_data:
                    user.is_verified = update_data['is_verified']
                if 'last_login' in update_data:
                    user.last_login = update_data['last_login']

                await db.commit()
                await db.refresh(user)

                logger.info(f"User profile updated successfully for user_id: {user_id}")
                logger.debug(f"Profile updated from {original_data} to {update_data}")

                # Handle preferences - it's stored as a string in DB but should be returned as a dict
                preferences_dict = {}
                if user.preferences:
                    try:
                        # Try to parse as JSON if it's a string
                        if isinstance(user.preferences, str):
                            preferences_dict = json.loads(user.preferences) if user.preferences.strip() else {}
                        else:
                            preferences_dict = user.preferences
                    except json.JSONDecodeError:
                        # If JSON parsing fails, use as-is or empty dict
                        preferences_dict = {}

                return UserResponse(
                    id=user.id,
                    email=user.email,
                    name=user.name,
                    username=user.username,
                    experience_level=user.experience_level,
                    is_active=user.is_active,
                    is_verified=user.is_verified,
                    preferences=preferences_dict,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                    last_login=user.last_login
                )
            finally:
                # Close the session properly
                await db_gen.aclose()
        except Exception as e:
            logger.error(f"Error updating user profile for user_id {user_id}: {e}")
            return None

    async def validate_session_token(self, token: str) -> Optional[str]:
        """Validate a session token and return the associated user ID."""
        logger.debug(f"Validating session token")
        try:
            from sqlalchemy import select
            from datetime import datetime
            from ..models.session import Session

            # Basic validation: check if token is reasonably long and formatted properly
            if not token or len(token) < 32:
                logger.warning("Session token validation failed: Invalid token format")
                return None

            # Get database session using the dependency
            db_gen = get_db_session()
            db = await db_gen.__anext__()  # Get the session from the generator

            try:
                # Query the sessions table for the token
                result = await db.execute(
                    select(Session)
                    .filter_by(session_token=token)
                    .filter(Session.expires_at > datetime.utcnow())
                )
                session = result.scalars().first()

                if session and session.expires_at > datetime.utcnow():
                    logger.info(f"Session token validation successful for user_id: {session.user_id}")
                    return session.user_id  # Return the associated user_id if valid
                else:
                    logger.warning("Session token validation failed: Token not found or expired")

                return None  # Token not found or expired
            finally:
                # Close the session properly
                await db_gen.aclose()
        except Exception as e:
            logger.error(f"Error validating session token: {e}")
            return None

# Global instance
auth_service = AuthService()