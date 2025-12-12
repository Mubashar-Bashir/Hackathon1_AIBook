from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import uuid


# SQLAlchemy model
class Account:
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    provider_id = Column(String, nullable=False)
    provider_name = Column(String, nullable=False)  # 'google', 'github', etc.
    provider_account_id = Column(String, nullable=False)
    access_token = Column(Text, nullable=True)  # Encrypted
    refresh_token = Column(Text, nullable=True)  # Encrypted
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


# Pydantic models for API requests/responses
class AccountBase(BaseModel):
    user_id: str
    provider_id: str
    provider_name: str
    provider_account_id: str


class AccountCreate(BaseModel):
    user_id: str
    provider_id: str
    provider_name: str
    provider_account_id: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None


class AccountResponse(BaseModel):
    id: str
    user_id: str
    provider_id: str
    provider_name: str
    provider_account_id: str
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True