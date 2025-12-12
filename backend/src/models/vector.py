from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# Pydantic models for vector embeddings
class VectorEmbeddingBase(BaseModel):
    content_id: str
    content_text: str
    embedding_vector: List[float]
    model_used: str

class VectorEmbeddingCreate(VectorEmbeddingBase):
    pass

class VectorEmbeddingResponse(BaseModel):
    id: str
    content_id: str
    content_text: str
    model_used: str
    created_at: datetime

    class Config:
        from_attributes = True