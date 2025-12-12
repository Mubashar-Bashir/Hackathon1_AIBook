"""Test script to verify session management and expiration handling."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
import uuid

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_session_management():
    """Test session management and expiration handling."""
    logger.info("Starting session management and expiration handling test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db, get_db_session
    from src.models.session import Session
    from sqlalchemy import select

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test 1: Register a user and verify session is created
    logger.info("Testing user registration and session creation...")
    test_email = f"session_test_{uuid.uuid4().hex[:8]}@example.com"
    registration_result = await auth_service.register_user(
        email=test_email,
        name="Session Test User",
        password="SecurePassword123!",
        experience_level="beginner"
    )

    if not registration_result:
        logger.error("Test 1 failed: User registration failed")
        return False

    user_id = registration_result["user_id"]
    session_token = registration_result["session_token"]

    # Verify session was created in database
    db_gen = get_db_session()
    db = await db_gen.__anext__()
    try:
        result = await db.execute(select(Session).filter_by(user_id=user_id))
        sessions = result.scalars().all()

        if len(sessions) == 0:
            logger.error("Test 1 failed: No session created for user")
            return False

        session = sessions[0]
        if session.session_token != session_token:
            logger.error("Test 1 failed: Session token mismatch")
            return False

        if session.expires_at < datetime.utcnow():
            logger.error("Test 1 failed: Session already expired")
            return False

        logger.info(f"✓ Test 1 passed: Session created with expiry {session.expires_at}")
    finally:
        await db_gen.aclose()

    # Test 2: Validate valid session token
    logger.info("Testing valid session token validation...")
    validated_user_id = await auth_service.validate_session_token(session_token)
    if validated_user_id != user_id:
        logger.error("Test 2 failed: Valid session token not validated correctly")
        return False

    logger.info("✓ Test 2 passed: Valid session token validated correctly")

    # Test 3: Validate invalid session token
    logger.info("Testing invalid session token validation...")
    invalid_result = await auth_service.validate_session_token("invalid_token_1234567890")
    if invalid_result is not None:
        logger.error("Test 3 failed: Invalid session token should not be validated")
        return False

    logger.info("✓ Test 3 passed: Invalid session token correctly rejected")

    # Test 4: Test session expiration
    logger.info("Testing session expiration handling...")
    from sqlalchemy import text

    # Manually expire the session in the database to test expiration handling
    db_gen = get_db_session()
    db = await db_gen.__anext__()
    try:
        # Update the session to have an expired time
        expired_time = datetime.utcnow() - timedelta(hours=1)  # 1 hour ago
        result = await db.execute(
            text("UPDATE sessions SET expires_at = :expired_time WHERE session_token = :token"),
            {"expired_time": expired_time, "token": session_token}
        )
        await db.commit()

        # Verify the session is now expired
        expired_validation = await auth_service.validate_session_token(session_token)
        if expired_validation is not None:
            logger.error("Test 4 failed: Expired session token should not be validated")
            return False

        logger.info("✓ Test 4 passed: Expired session token correctly rejected")
    finally:
        await db_gen.aclose()

    # Test 5: Create a new valid session for further testing
    logger.info("Testing login creates new valid session...")
    login_result = await auth_service.authenticate_user(
        email=test_email,
        password="SecurePassword123!"
    )

    if not login_result:
        logger.error("Test 5 failed: User login failed")
        return False

    if login_result["user_id"] != user_id:
        logger.error("Test 5 failed: Login returned wrong user ID")
        return False

    new_session_token = login_result["session_token"]

    # Verify the new session is valid
    validated_new_user_id = await auth_service.validate_session_token(new_session_token)
    if validated_new_user_id != user_id:
        logger.error("Test 5 failed: New session token not validated correctly")
        return False

    # Verify the new session is in the database and not expired
    db_gen = get_db_session()
    db = await db_gen.__anext__()
    try:
        result = await db.execute(select(Session).filter_by(session_token=new_session_token))
        new_session = result.scalars().first()

        if not new_session:
            logger.error("Test 5 failed: New session not found in database")
            return False

        if new_session.expires_at < datetime.utcnow():
            logger.error("Test 5 failed: New session already expired")
            return False

        logger.info(f"✓ Test 5 passed: New session created with expiry {new_session.expires_at}")
    finally:
        await db_gen.aclose()

    # Test 6: Multiple concurrent sessions for same user
    logger.info("Testing multiple concurrent sessions for same user...")
    # Log in again to create another session
    another_login_result = await auth_service.authenticate_user(
        email=test_email,
        password="SecurePassword123!"
    )

    if not another_login_result:
        logger.error("Test 6 failed: Second login failed")
        return False

    another_session_token = another_login_result["session_token"]

    # Both sessions should be valid
    first_valid = await auth_service.validate_session_token(new_session_token)
    second_valid = await auth_service.validate_session_token(another_session_token)

    if not first_valid or not second_valid:
        logger.error("Test 6 failed: Both sessions should be valid")
        return False

    # Check database to confirm both sessions exist
    db_gen = get_db_session()
    db = await db_gen.__anext__()
    try:
        result = await db.execute(select(Session).filter_by(user_id=user_id))
        all_sessions = result.scalars().all()

        if len(all_sessions) < 2:
            logger.error("Test 6 failed: Should have multiple sessions for same user")
            return False

        logger.info(f"✓ Test 6 passed: User has {len(all_sessions)} active sessions")
    finally:
        await db_gen.aclose()

    # Test 7: Session token format validation
    logger.info("Testing session token format validation...")
    invalid_formats = [
        "",  # Empty
        "short",  # Too short
        "a" * 10,  # Still too short
        "a" * 31,  # Just under minimum
        None  # None
    ]

    for invalid_format in invalid_formats:
        try:
            result = await auth_service.validate_session_token(invalid_format)
            if result is not None:
                logger.error(f"Test 7 failed: Invalid format '{invalid_format}' should not validate")
                return False
        except:
            # If it throws an exception, that's also acceptable behavior for invalid input
            pass

    logger.info("✓ Test 7 passed: Invalid session token formats correctly rejected")

    # Test 8: Test session cleanup of expired sessions (optional advanced test)
    logger.info("Testing expired session cleanup...")
    # Create an expired session manually to test cleanup
    db_gen = get_db_session()
    db = await db_gen.__anext__()
    try:
        from src.models.session import Session
        expired_session = Session(
            user_id=user_id,
            session_token="expired_test_token_12345",
            expires_at=datetime.utcnow() - timedelta(days=1)  # Expired yesterday
        )
        db.add(expired_session)
        await db.commit()

        # Try to validate it - should fail
        expired_check = await auth_service.validate_session_token("expired_test_token_12345")
        if expired_check is not None:
            logger.error("Test 8 failed: Expired session should not validate")
            return False

        logger.info("✓ Test 8 passed: Expired sessions correctly rejected")
    except Exception as e:
        logger.error(f"Test 8 failed with error: {e}")
        return False
    finally:
        await db_gen.aclose()

    logger.info("All session management and expiration handling tests passed!")
    return True

async def main():
    """Main function to run session management tests."""
    logger.info("Starting session management and expiration handling tests...")

    # Run the session management tests
    success = await test_session_management()

    logger.info(f"Session management and expiration handling test: {'PASS' if success else 'FAIL'}")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)