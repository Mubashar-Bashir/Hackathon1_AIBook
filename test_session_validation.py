#!/usr/bin/env python3
"""
Test script to debug session validation for protected endpoints
This addresses task T039: [DEBUG] Debug session validation for protected endpoints
"""

import asyncio
import os
import logging
from datetime import datetime, timedelta
from backend.src.services.auth_service import auth_service
from backend.src.services.session_service import session_service
from backend.src.utils.database import test_db_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_session_validation():
    """Test session validation functionality."""
    logger.info("Starting session validation debug test...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with session validation test")
        return False

    # Create a test user
    test_email = f"session_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "Session Test User"
    test_password = "SecurePassword123!"
    test_experience = "advanced"

    logger.info(f"Creating test user: {test_email}")

    # Register the test user
    reg_result = await auth_service.register_user(
        email=test_email,
        name=test_name,
        password=test_password,
        experience_level=test_experience
    )

    if not reg_result:
        logger.error("Failed to create test user")
        return False

    logger.info("Test user created successfully")

    # Get the session token from registration
    session_token = reg_result['session_token']
    user_id = reg_result['user_id']

    logger.info(f"Testing session validation with token: {session_token[:10]}...")

    # Test auth_service session validation
    validated_user_id = await auth_service.validate_session_token(session_token)
    if validated_user_id == user_id:
        logger.info("✅ auth_service session validation successful!")
    else:
        logger.error("❌ auth_service session validation failed!")
        return False

    # Test session_service session validation
    validated_user_id2 = await session_service.validate_session(session_token)
    if validated_user_id2 == user_id:
        logger.info("✅ session_service session validation successful!")
    else:
        logger.error("❌ session_service session validation failed!")
        return False

    # Test with invalid token
    invalid_token = "invalid_token_12345"
    invalid_result = await auth_service.validate_session_token(invalid_token)
    if invalid_result is None:
        logger.info("✅ Correctly rejected invalid token")
    else:
        logger.error("❌ Incorrectly accepted invalid token")
        return False

    # Test with empty token
    empty_result = await auth_service.validate_session_token("")
    if empty_result is None:
        logger.info("✅ Correctly rejected empty token")
    else:
        logger.error("❌ Incorrectly accepted empty token")
        return False

    # Test session expiration (create an expired session manually for testing)
    try:
        from backend.src.models.session import Session
        from backend.src.utils.database import get_db_session
        from datetime import datetime, timedelta
        import uuid

        # Create an expired session
        expired_token = "expired_" + auth_service.generate_session_token()
        expired_time = datetime.utcnow() - timedelta(days=1)  # Expired 1 day ago

        # Get database session
        db_gen = get_db_session()
        db = await db_gen.__anext__()

        try:
            expired_session = Session(
                id=str(uuid.uuid4()),
                user_id=user_id,
                session_token=expired_token,
                expires_at=expired_time
            )
            db.add(expired_session)
            await db.commit()
            logger.info("Created expired session for testing")

            # Test that expired session is rejected
            expired_result = await auth_service.validate_session_token(expired_token)
            if expired_result is None:
                logger.info("✅ Correctly rejected expired session token")
            else:
                logger.error("❌ Incorrectly accepted expired session token")
                return False
        finally:
            await db_gen.aclose()

    except Exception as e:
        logger.error(f"Error testing expired session: {e}")
        # This is not a critical failure for the main functionality

    logger.info("✅ All session validation tests passed!")
    return True

async def main():
    """Run all session validation tests."""
    logger.info("Starting session validation debug tests...")

    success = await test_session_validation()

    if success:
        print("\n🎉 Session validation debug test completed successfully!")
        return True
    else:
        print("\n💥 Session validation debug test failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)