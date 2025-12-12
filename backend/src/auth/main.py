"""
Custom Authentication Configuration for AIBook Platform
"""
import os
from typing import Optional
from datetime import datetime, timedelta
import secrets
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
import uuid


class CustomAuthConfig:
    """
    Configuration class for custom authentication system
    """
    def __init__(self):
        self.secret_key = os.getenv("BETTER_AUTH_SECRET", secrets.token_urlsafe(32))
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")

        # Database settings
        self.neon_database_url = os.getenv("NEON_DATABASE_URL", "")

        # Security settings
        self.password_min_length = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
        self.require_strong_password = os.getenv("REQUIRE_STRONG_PASSWORD", "true").lower() == "true"
        self.max_login_attempts = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        self.lockout_duration_minutes = int(os.getenv("LOCKOUT_DURATION_MINUTES", "30"))

    def hash_password(self, password: str) -> str:
        """
        Hash a password with a salt using PBKDF2
        """
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
        return f"{salt}:{pwdhash.hex()}"

    def verify_password(self, password: str, stored_password: str) -> bool:
        """
        Verify a password against its hash
        """
        try:
            salt, pwdhash = stored_password.split(':')
            computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000)
            return secrets.compare_digest(computed_hash.hex(), pwdhash)
        except Exception:
            return False

    def generate_session_token(self) -> str:
        """
        Generate a secure session token
        """
        return secrets.token_urlsafe(32)

    def generate_verification_token(self) -> str:
        """
        Generate a secure verification token
        """
        return secrets.token_urlsafe(32)


# Global instance of the auth configuration
auth_config = CustomAuthConfig()


# SQLAlchemy models for authentication
Base = declarative_base()


class User(Base):
    """
    User model for the authentication system
    """
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=True)  # Optional username
    password_hash = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)  # 'beginner', 'intermediate', 'expert'
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)


class Session(Base):
    """
    Session model for managing user sessions
    """
    __tablename__ = 'sessions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)


class Account(Base):
    """
    Account model for linking external authentication providers
    """
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)  # 'google', 'github', etc.
    provider_account_id = Column(String, nullable=False)
    access_token = Column(Text, nullable=True)  # Encrypted
    refresh_token = Column(Text, nullable=True)  # Encrypted
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class VerificationToken(Base):
    """
    Verification token model for account verification and password reset
    """
    __tablename__ = 'verification_tokens'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    token_type = Column(String, nullable=False)  # 'email_verification', 'password_reset'
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())