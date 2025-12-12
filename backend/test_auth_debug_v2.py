"""Test script to debug user registration flow and database persistence."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_user_registration():
    """Test user registration flow and database persistence."""
    logger.info("Starting user registration debug test...")

    # Import here to avoid circular imports during initialization
    from src.utils.database import init_db, Base, get_db_session, async_engine
    from src.models.user import User
    from src.services.auth_service import AuthService

    # Initialize database tables
    logger.info("Initializing database tables...")
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test user data
    test_email = "testuser@example.com"
    test_name = "Test User"
    test_password = "SecurePassword123!"
    test_experience_level = "beginner"

    logger.info(f"Attempting to register user: {test_email}")

    # Register a user
    registration_result = await auth_service.register_user(
        email=test_email,
        name=test_name,
        password=test_password,
        experience_level=test_experience_level
    )

    if registration_result:
        logger.info(f"User registration successful: {registration_result}")

        # Verify user was persisted in database
        db_gen = get_db_session()
        db = await db_gen.__anext__()  # Get the session from the generator
        try:
            from sqlalchemy import select
            result = await db.execute(select(User).filter_by(id=registration_result["user_id"]))
            user = result.scalars().first()
            if user:
                logger.info(f"User found in database: {user.email}")
                return True
            else:
                logger.error("User was not persisted in database")
                return False
        finally:
            await db_gen.aclose()
    else:
        logger.error("User registration failed")
        return False

async def test_user_login():
    """Test user login flow and session token generation."""
    logger.info("Starting user login debug test...")

    # Create auth service instance
    from src.services.auth_service import AuthService
    auth_service = AuthService()

    # Test login with the registered user
    test_email = "testuser@example.com"
    test_password = "SecurePassword123!"

    logger.info(f"Attempting to authenticate user: {test_email}")

    login_result = await auth_service.authenticate_user(
        email=test_email,
        password=test_password
    )

    if login_result:
        logger.info(f"User login successful: {login_result}")
        return True
    else:
        logger.error("User login failed")
        return False

async def test_session_validation():
    """Test session validation for protected endpoints."""
    logger.info("Starting session validation debug test...")

    # Create auth service instance
    from src.services.auth_service import AuthService
    auth_service = AuthService()

    # Test with a valid session token (from login result)
    # For this test, we'll use the token from the login test
    # This would typically come from a successful login

    # Since we can't easily test without a valid token in this isolated test,
    # we'll just verify the validation function works
    test_token = "invalid_token_for_test"

    logger.info(f"Attempting to validate session token: {test_token}")

    user_id = await auth_service.validate_session_token(test_token)

    if user_id is None:
        logger.info("Session validation correctly rejected invalid token")
        return True
    else:
        logger.error("Session validation should have failed for invalid token")
        return False

async def main():
    """Main function to run all tests."""
    logger.info("Starting authentication flow debugging tests...")

    # Import after setup
    from src.utils.database import test_db_connection

    # Test database connection first
    logger.info("Testing database connection...")
    db_success = await test_db_connection()
    if not db_success:
        logger.error("Database connection failed, aborting tests")
        return False

    # Run tests
    registration_success = await test_user_registration()
    login_success = await test_user_login() if registration_success else False
    session_success = await test_session_validation()

    # Summary
    logger.info("Test Results:")
    logger.info(f"User Registration: {'PASS' if registration_success else 'FAIL'}")
    logger.info(f"User Login: {'PASS' if login_success else 'FAIL'}")
    logger.info(f"Session Validation: {'PASS' if session_success else 'FAIL'}")

    all_passed = registration_success and login_success and session_success
    logger.info(f"Overall: {'PASS' if all_passed else 'FAIL'}")

    return all_passed

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)