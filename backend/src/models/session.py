from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid

# Import the Base from the database module to ensure all models use the same Base instance
from ..utils.database import Base


# SQLAlchemy model
class Session(Base):
    __tablename__ = 'sessions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    session_token = Column(String, unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)


# Pydantic models for API requests/responses
class SessionBase(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime


class SessionCreate(BaseModel):
    user_id: str
    session_token: str
    expires_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class SessionResponse(BaseModel):
    id: str
    user_id: str
    session_token: str
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    class Config:
        from_attributes = True