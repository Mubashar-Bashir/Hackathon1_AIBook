from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# Import the Base from the database module to ensure all models use the same Base instance
from ..utils.database import Base

# SQLAlchemy models
class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=True)  # Optional username
    password_hash = Column(String, nullable=False)  # Hashed password
    experience_level = Column(String, nullable=False)  # 'beginner', 'intermediate', 'expert'
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    preferences = Column(Text)  # JSON string for user preferences

# Pydantic models for API requests/responses
class UserBase(BaseModel):
    email: str
    name: str
    experience_level: str  # 'beginner', 'intermediate', 'expert'

class UserCreate(UserBase):
    password: str  # In a real app, this would be handled separately for security

class UserUpdate(BaseModel):
    name: Optional[str] = None
    experience_level: Optional[str] = None  # 'beginner', 'intermediate', 'expert'
    preferences: Optional[dict] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    username: Optional[str] = None
    experience_level: str
    is_active: bool = True
    is_verified: bool = False
    preferences: Optional[dict] = {}
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    success: bool
    user: 'UserProfile'
    session_token: str

    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    id: str
    email: str
    name: str
    username: Optional[str] = None
    experience_level: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRegistrationResponse(BaseModel):
    success: bool
    user: UserProfile
    session_token: str

    class Config:
        from_attributes = True


class LogoutResponse(BaseModel):
    success: bool
    message: str

    class Config:
        from_attributes = True


class BasicSuccessResponse(BaseModel):
    success: bool
    message: Optional[str] = None

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    id: str
    email: str
    name: str
    username: Optional[str] = None
    experience_level: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True