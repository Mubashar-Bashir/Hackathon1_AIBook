from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# SQLAlchemy models
class User:
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    background = Column(String, nullable=False)  # 'beginner', 'intermediate', 'expert'
    password_hash = Column(String, nullable=False)  # Hashed password
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    preferences = Column(Text)  # JSON string for user preferences

    # Relationship
    chat_sessions = relationship("ChatSession", back_populates="user")

# Pydantic models for API requests/responses
class UserBase(BaseModel):
    email: str
    name: str
    background: str  # 'beginner', 'intermediate', 'expert'

class UserCreate(UserBase):
    password: str  # In a real app, this would be handled separately for security

class UserUpdate(BaseModel):
    name: Optional[str] = None
    background: Optional[str] = None  # 'beginner', 'intermediate', 'expert'
    preferences: Optional[dict] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    background: str
    preferences: Optional[dict] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    user_id: str
    email: str
    name: str
    background: str
    session_token: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    name: str
    background: str
    preferences: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True