"""Test script to test database connection with Neon using asyncpg."""

import asyncio
import os
import logging
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get database URL from environment or use default
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

async def test_db_connection():
    """Test database connection with Neon using asyncpg."""
    logger.info(f"Testing database connection to: {DATABASE_URL}")

    # Create engine with connection testing parameters
    engine = create_async_engine(
        DATABASE_URL,
        echo=True,  # Enable SQL logging for debugging
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,    # Recycle connections every 5 minutes
        connect_args={
            "server_settings": {
                "application_name": "AIBook-Auth-Service-Test",
            },
            "ssl": "require"  # SSL setting for asyncpg
        }
    )

    try:
        # Test the connection
        async with engine.connect() as conn:
            logger.info("Connecting to database...")
            result = await conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            if row and row.test == 1:
                logger.info("✓ Database connection successful!")
                return True
            else:
                logger.error("✗ Database connection test failed: unexpected result")
                return False
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False
    finally:
        # Dispose of the engine
        await engine.dispose()

async def main():
    """Main function to run the database connection test."""
    logger.info("Starting database connection test...")
    success = await test_db_connection()

    if success:
        logger.info("Database connection test completed successfully!")
    else:
        logger.error("Database connection test failed!")

    return success

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())

    # Exit with appropriate code
    exit(0 if success else 1)