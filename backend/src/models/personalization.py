from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# SQLAlchemy models
class ChapterPersonalization:
    __tablename__ = 'chapter_personalizations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chapter_id = Column(String, nullable=False)  # References textbook chapter
    user_background = Column(String, nullable=False)  # 'beginner', 'intermediate', 'expert'
    personalized_content = Column(Text, nullable=False)  # Personalized chapter content
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Pydantic models for API requests/responses
class PersonalizationBase(BaseModel):
    chapter_id: str
    user_background: str  # 'beginner', 'intermediate', 'expert'
    personalized_content: str

class PersonalizationCreate(PersonalizationBase):
    pass

class PersonalizationUpdate(BaseModel):
    personalized_content: Optional[str] = None

class PersonalizationResponse(BaseModel):
    id: str
    chapter_id: str
    user_background: str
    personalized_content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ApplyPersonalizationRequest(BaseModel):
    content: str
    user_background: Optional[str] = None  # If not provided, will use user's default background
    personalization_type: Optional[str] = "all"  # 'simplification', 'elaboration', 'examples', 'all'

class ApplyPersonalizationResponse(BaseModel):
    original_content: str
    personalized_content: str
    user_background: str
    personalization_type: str
    timestamp: datetime

class GetPersonalizedChapterResponse(BaseModel):
    chapter_id: str
    original_title: str
    original_content: str
    personalized_title: Optional[str] = None
    personalized_content: Optional[str] = None
    background_level: str
    personalization_applied: bool
    timestamp: datetime