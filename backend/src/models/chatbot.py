from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# Pydantic models for API requests/responses
class ChatbotQueryBase(BaseModel):
    query_text: str
    context_type: Optional[str] = "full_book"  # 'full_book', 'current_page', or 'selected_text'
    selected_text: Optional[str] = None
    user_id: Optional[str] = None

class ChatbotQueryCreate(ChatbotQueryBase):
    pass

class ChatbotResponseBase(BaseModel):
    query_id: str
    response_text: str
    sources: List[str] = []
    confidence_score: Optional[float] = 0.0

class ChatbotResponseCreate(ChatbotResponseBase):
    pass

class ChatbotQueryResponse(BaseModel):
    id: str
    query: str
    response: str
    sources: List[str]
    confidence: float
    timestamp: datetime

    class Config:
        from_attributes = True