#!/usr/bin/env python3
"""
Test script to validate database connection with Neon
This addresses task T036: [DEBUG] Test database connection with Neon using asyncpg
"""

import asyncio
import os
import logging
from backend.src.utils.database import test_db_connection, init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    """Test the Neon database connection."""
    logger.info("Starting Neon database connection test...")

    # Check if NEON_DATABASE_URL is set
    neon_url = os.getenv("NEON_DATABASE_URL")
    if not neon_url:
        logger.error("NEON_DATABASE_URL environment variable not set!")
        logger.info("Please set the NEON_DATABASE_URL environment variable before running this test.")
        return False

    logger.info(f"Using database URL: {neon_url[:50]}...")  # Only show first 50 chars for security

    try:
        # Test the connection
        success = await test_db_connection()
        if success:
            logger.info("✅ Database connection test PASSED!")

            # Try to initialize the database (create tables if they don't exist)
            logger.info("Initializing database tables...")
            await init_db()
            logger.info("✅ Database tables initialized successfully!")

            return True
        else:
            logger.error("❌ Database connection test FAILED!")
            return False
    except Exception as e:
        logger.error(f"❌ Error during database connection test: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Neon database connection test completed successfully!")
    else:
        print("\n💥 Neon database connection test failed!")
        exit(1)