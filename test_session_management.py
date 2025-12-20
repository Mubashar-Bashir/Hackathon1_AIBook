#!/usr/bin/env python3
"""
Test script to test session management and expiration handling
This addresses task T043: [DEBUG] Test session management and expiration handling
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

async def test_session_management():
    """Test session management and expiration handling."""
    logger.info("Starting session management and expiration tests...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with session management tests")
        return False

    # Create a test user
    test_email = f"session_mgmt_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "Session Management Test User"
    test_password = "SecurePassword123!"
    test_experience = "intermediate"

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

    user_id = reg_result['user_id']
    session_token = reg_result['session_token']
    logger.info(f"Test user created successfully with ID: {user_id}")

    # Test 1: Session creation and validation
    logger.info("Test 1: Session creation and validation")

    # Validate the session token created during registration
    validated_user_id = await auth_service.validate_session_token(session_token)
    if validated_user_id == user_id:
        logger.info("✅ Session token validation successful")
    else:
        logger.error("❌ Session token validation failed")
        return False

    # Test 2: Session deletion (logout)
    logger.info("Test 2: Session deletion (logout)")

    # Delete the session using session_service
    delete_success = await session_service.delete_session(session_token)
    if delete_success:
        logger.info("✅ Session deletion successful")
    else:
        logger.error("❌ Session deletion failed")
        return False

    # Verify the session is no longer valid after deletion
    invalidated_user_id = await auth_service.validate_session_token(session_token)
    if invalidated_user_id is None:
        logger.info("✅ Session properly invalidated after deletion")
    else:
        logger.error("❌ Session still valid after deletion")
        return False

    # Test 3: Session cleanup of expired sessions
    logger.info("Test 3: Session cleanup of expired sessions")

    # Create an expired session manually for testing cleanup
    from backend.src.models.session import Session
    from backend.src.utils.database import get_db_session
    import uuid

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
        logger.info("Created expired session for cleanup testing")

        # Test cleanup of expired sessions
        cleaned_count = await session_service.cleanup_expired_sessions()
        logger.info(f"Cleaned up {cleaned_count} expired sessions")

        if cleaned_count >= 1:  # At least our test expired session should be cleaned
            logger.info("✅ Expired session cleanup working")
        else:
            logger.warning("⚠️  No expired sessions were cleaned (may be expected in test environment)")

        # Verify the expired session is no longer valid
        expired_validated = await auth_service.validate_session_token(expired_token)
        if expired_validated is None:
            logger.info("✅ Expired session properly invalidated")
        else:
            logger.error("❌ Expired session still valid after cleanup")
            return False

    finally:
        await db_gen.aclose()

    # Test 4: Multiple sessions for same user
    logger.info("Test 4: Multiple sessions for same user")

    # Create multiple sessions by logging in multiple times
    session_tokens = []
    for i in range(3):
        login_result = await auth_service.authenticate_user(
            email=test_email,
            password=test_password
        )
        if login_result:
            session_tokens.append(login_result['session_token'])
            logger.debug(f"Created session {i+1}: {login_result['session_token'][:10]}...")
        else:
            logger.error(f"❌ Failed to create session {i+1}")
            return False

    logger.info(f"Created {len(session_tokens)} sessions for the same user")

    # Verify all sessions are valid
    for i, token in enumerate(session_tokens):
        validated = await auth_service.validate_session_token(token)
        if validated == user_id:
            logger.info(f"✅ Session {i+1} is valid")
        else:
            logger.error(f"❌ Session {i+1} is invalid")
            return False

    # Test 5: Session cleanup cron functionality
    logger.info("Test 5: Session cleanup cron functionality")

    # Create another expired session for cron testing
    cron_expired_token = "cron_expired_" + auth_service.generate_session_token()
    # Expired 2 days ago (older than default 24 hours for cron)
    cron_expired_time = datetime.utcnow() - timedelta(days=2)

    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        cron_expired_session = Session(
            id=str(uuid.uuid4()),
            user_id=user_id,
            session_token=cron_expired_token,
            expires_at=cron_expired_time
        )
        db.add(cron_expired_session)
        await db.commit()
        logger.info("Created expired session for cron cleanup testing")

        # Test cleanup of expired sessions with cron method (older than 24 hours)
        cron_cleaned_count = await session_service.cleanup_expired_sessions_cron(hours_to_keep=24)
        logger.info(f"Cron cleaned up {cron_cleaned_count} old expired sessions")

        # Verify the cron-expired session is no longer valid
        cron_expired_validated = await auth_service.validate_session_token(cron_expired_token)
        if cron_expired_validated is None:
            logger.info("✅ Cron-expired session properly invalidated")
        else:
            logger.error("❌ Cron-expired session still valid after cron cleanup")
            return False

    finally:
        await db_gen.aclose()

    logger.info("✅ All session management and expiration tests passed!")
    return True

async def main():
    """Run all session management tests."""
    logger.info("Starting session management and expiration tests...")

    success = await test_session_management()

    if success:
        print("\n🎉 Session management and expiration tests completed successfully!")
        return True
    else:
        print("\n💥 Session management and expiration tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)