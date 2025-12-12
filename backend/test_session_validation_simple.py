"""Simple test to debug session validation functionality."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_session_validation_direct():
    """Test session validation functionality directly."""
    logger.info("Starting direct session validation test...")

    # Import the auth service
    from src.services.auth_service import AuthService
    from src.utils.database import init_db

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    import uuid
    # First, register and login a user to get a valid token
    unique_email = f"session_test_{uuid.uuid4().hex[:8]}@example.com"
    logger.info(f"Registering test user with email: {unique_email}...")
    registration_result = await auth_service.register_user(
        email=unique_email,
        name="Session Test User",
        password="SecurePassword123!",
        experience_level="beginner"
    )

    if not registration_result:
        logger.error("User registration failed")
        return False

    user_id = registration_result["user_id"]
    valid_session_token = registration_result["session_token"]
    logger.info(f"User registered successfully. User ID: {user_id}")

    # Test valid session token
    logger.info("Testing valid session token...")
    validated_user_id = await auth_service.validate_session_token(valid_session_token)
    if validated_user_id == user_id:
        logger.info("Valid session token correctly validated")
    else:
        logger.error(f"Valid session token failed validation. Expected: {user_id}, Got: {validated_user_id}")
        return False

    # Test invalid session token
    logger.info("Testing invalid session token...")
    invalid_token_result = await auth_service.validate_session_token("invalid_token_1234567890")
    if invalid_token_result is None:
        logger.info("Invalid session token correctly rejected")
    else:
        logger.error(f"Invalid session token should have been rejected. Got: {invalid_token_result}")
        return False

    # Test short/invalid format token
    logger.info("Testing short/invalid format token...")
    short_token_result = await auth_service.validate_session_token("short")
    if short_token_result is None:
        logger.info("Short token correctly rejected")
    else:
        logger.error(f"Short token should have been rejected. Got: {short_token_result}")
        return False

    # Test empty token
    logger.info("Testing empty token...")
    empty_token_result = await auth_service.validate_session_token("")
    if empty_token_result is None:
        logger.info("Empty token correctly rejected")
    else:
        logger.error(f"Empty token should have been rejected. Got: {empty_token_result}")
        return False

    # Test None token
    logger.info("Testing None token...")
    none_token_result = await auth_service.validate_session_token(None)
    if none_token_result is None:
        logger.info("None token correctly rejected")
    else:
        logger.error(f"None token should have been rejected. Got: {none_token_result}")
        return False

    logger.info("All session validation tests passed!")
    return True

async def main():
    """Main function to run session validation tests."""
    logger.info("Starting direct session validation debugging tests...")

    # Run the session validation test
    success = await test_session_validation_direct()

    logger.info(f"Session validation test: {'PASS' if success else 'FAIL'}")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)