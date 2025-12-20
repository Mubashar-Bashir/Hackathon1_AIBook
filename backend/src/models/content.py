"""
Content Models for RAG System

This module defines the data models for book content and text chunks used in the RAG system.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import uuid


# SQLAlchemy models
class BookContent:
    __tablename__ = 'book_contents'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content_text = Column(Text, nullable=False)  # Raw content
    source_type = Column(String, default='web_page')  # 'web_page', 'pdf', 'markdown'
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    metadata = Column(JSON)  # Additional metadata like author, tags, etc.

    # Relationship
    text_chunks = relationship("TextChunk", back_populates="book_content")


class TextChunk:
    __tablename__ = 'text_chunks'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_id = Column(String, ForeignKey('book_contents.id'), nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    token_count = Column(Integer, nullable=False)
    embedding_id = Column(String, nullable=True)  # ID in the vector database (if already embedded)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    book_content = relationship("BookContent", back_populates="text_chunks")


# Pydantic models for API requests/responses
class BookContentBase(BaseModel):
    url: str
    title: str
    content: str
    source_type: str = 'web_page'  # 'web_page', 'pdf', 'markdown'
    metadata: Optional[dict] = None


class BookContentCreate(BookContentBase):
    pass


class BookContentResponse(BaseModel):
    id: str
    url: str
    title: str
    content: str
    source_type: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class TextChunkBase(BaseModel):
    content_id: str
    chunk_text: str
    chunk_index: int
    token_count: int
    embedding_id: Optional[str] = None
    metadata: Optional[dict] = None


class TextChunkCreate(TextChunkBase):
    pass


class TextChunkResponse(BaseModel):
    id: str
    content_id: str
    chunk_text: str
    chunk_index: int
    token_count: int
    embedding_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ContentReference(BaseModel):
    """Model representing a reference to content in search results"""
    content_id: str
    url: str
    title: str
    snippet: str  # Short preview of the content
    relevance_score: float  # How relevant this content is to the query
    position: int  # Position in the search results