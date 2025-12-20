from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# SQLAlchemy models
class ChatSession:
    __tablename__ = 'chat_sessions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey('users.id'), nullable=True)  # Nullable for anonymous sessions
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    context_type = Column(String, default='full_book')  # 'full_book', 'selected_text', 'custom'
    selected_text = Column(Text, nullable=True)  # For selected text context
    metadata = Column(JSON)  # Additional session metadata

    # Relationship
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    user = relationship("User", back_populates="chat_sessions")


class ChatMessage:
    __tablename__ = 'chat_messages'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey('chat_sessions.id'), nullable=False)
    sender_type = Column(String, nullable=False)  # 'user' or 'bot'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, server_default=func.now())
    metadata = Column(JSON)  # Additional message metadata (sources, confidence, etc.)

    # Relationship
    session = relationship("ChatSession", back_populates="messages")


# Pydantic models for API requests/responses
class ChatMessageBase(BaseModel):
    session_id: str
    sender_type: str  # 'user' or 'bot'
    content: str
    metadata: Optional[dict] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    sender_type: str
    content: str
    timestamp: datetime
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    user_id: Optional[str] = None
    context_type: Optional[str] = 'full_book'  # 'full_book', 'selected_text', 'custom'
    selected_text: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionResponse(BaseModel):
    id: str
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    context_type: str
    selected_text: Optional[str]
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class ChatQueryRequest(BaseModel):
    query: str
    context_type: str = 'full_book'  # 'full_book', 'selected_text'
    selected_text: Optional[str] = None
    session_id: Optional[str] = None  # If not provided, creates a new session


class ChatQueryResponse(BaseModel):
    response: str
    sources: List[str] = []
    session_id: str
    query_id: str
    confidence_score: Optional[float] = 0.0

    class Config:
        from_attributes = True