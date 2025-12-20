"""
RAG Pipeline Models

This module contains models shared between content service and monitoring service
to avoid circular dependencies.
"""

from pydantic import BaseModel
from typing import Optional

class ContentProcessingResult(BaseModel):
    """Result of content processing operation"""
    content_id: str
    url: str
    title: str
    chunks_processed: int
    status: str
    error: Optional[str] = None