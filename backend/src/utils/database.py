import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

# Database configuration
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Async engine for async operations
async_engine = create_async_engine(DATABASE_URL)

# Async session factory
async_session_local = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

async def get_db_session():
    """Dependency function to get database session"""
    async with async_session_local() as session:
        yield session