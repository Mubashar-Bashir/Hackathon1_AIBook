import os
import logging
from typing import AsyncGenerator
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from contextlib import asynccontextmanager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Async engine for async operations with debugging
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Enable SQL logging for debugging
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args={
        "server_settings": {
            "application_name": "AIBook-Auth-Service",
        }
    }
)

# Async session factory
async_session_local = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

async def get_db_session():
    """Dependency function to get database session with comprehensive error handling"""
    async with async_session_local() as session:
        logger.debug("Database session created")
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {str(e)}")
            try:
                await session.rollback()
            except Exception as rollback_error:
                logger.error(f"Error during rollback: {str(rollback_error)}")
            raise
        finally:
            try:
                await session.close()
                logger.debug("Database session closed")
            except Exception as close_error:
                logger.error(f"Error closing database session: {str(close_error)}")

async def test_db_connection():
    """Test database connection with debugging"""
    try:
        async with async_engine.connect() as conn:
            logger.info("Testing database connection...")
            result = await conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

# Add a function to initialize the database
async def init_db():
    """Initialize the database with tables"""
    try:
        # Import models to ensure they are registered with Base before table creation
        from ..models.user import User
        from ..models.session import Session

        logger.info("Initializing database tables...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise