from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.sql import func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


# SQLAlchemy model
class VerificationToken:
    __tablename__ = 'verification_tokens'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    token = Column(String, unique=True, nullable=False)
    token_type = Column(String, nullable=False)  # 'email_verification', 'password_reset'
    expires_at = Column(DateTime, nullable=False)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


# Pydantic models for API requests/responses
class VerificationTokenBase(BaseModel):
    user_id: str
    token: str
    token_type: str  # 'email_verification', 'password_reset'
    expires_at: datetime


class VerificationTokenCreate(BaseModel):
    user_id: str
    token_type: str  # 'email_verification', 'password_reset'


class VerificationTokenResponse(BaseModel):
    id: str
    user_id: str
    token: str
    token_type: str
    expires_at: datetime
    used_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True