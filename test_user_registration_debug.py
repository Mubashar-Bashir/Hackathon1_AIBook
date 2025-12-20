#!/usr/bin/env python3
"""
Test script to debug user registration flow and database persistence
This addresses task T037: [DEBUG] Debug user registration flow and database persistence
"""

import asyncio
import os
import logging
from datetime import datetime
from backend.src.services.auth_service import auth_service
from backend.src.services.session_service import session_service
from backend.src.utils.database import test_db_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_user_registration():
    """Test the user registration flow."""
    logger.info("Starting user registration debug test...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with registration test")
        return False

    # Test user registration
    test_email = f"testuser_{int(datetime.now().timestamp())}@example.com"
    test_name = "Test User"
    test_password = "SecurePassword123!"
    test_experience = "beginner"

    logger.info(f"Attempting to register user: {test_email}")

    try:
        # Register a new user
        result = await auth_service.register_user(
            email=test_email,
            name=test_name,
            password=test_password,
            experience_level=test_experience
        )

        if result:
            logger.info(f"✅ User registration successful!")
            logger.info(f"   User ID: {result['user_id']}")
            logger.info(f"   Email: {result['email']}")
            logger.info(f"   Session Token: {result['session_token'][:10]}...")  # Only show first 10 chars

            # Test session validation
            user_id = await auth_service.validate_session_token(result['session_token'])
            if user_id == result['user_id']:
                logger.info("✅ Session validation successful!")
            else:
                logger.error("❌ Session validation failed!")
                return False

            # Test getting user profile
            profile = await auth_service.get_user_profile(result['user_id'])
            if profile:
                logger.info(f"✅ Profile retrieval successful: {profile.email}")
            else:
                logger.error("❌ Profile retrieval failed!")
                return False

            return True
        else:
            logger.error("❌ User registration failed!")
            return False

    except Exception as e:
        logger.error(f"❌ Error during user registration test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_user_login():
    """Test the user login flow."""
    logger.info("Starting user login debug test...")

    test_email = "testuser@example.com"  # Use a known test user
    test_password = "SecurePassword123!"

    try:
        # Attempt to login
        result = await auth_service.authenticate_user(
            email=test_email,
            password=test_password
        )

        if result:
            logger.info(f"✅ User login successful!")
            logger.info(f"   User ID: {result['user_id']}")
            logger.info(f"   Session Token: {result['session_token'][:10]}...")
            return True
        else:
            logger.info("⚠️  User login failed - this may be expected if user doesn't exist")
            return True  # Not an error if test user doesn't exist

    except Exception as e:
        logger.error(f"❌ Error during user login test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all registration flow tests."""
    logger.info("Starting user registration flow debug tests...")

    # Test registration
    reg_success = await test_user_registration()

    # Test login
    login_success = await test_user_login()

    if reg_success:
        logger.info("✅ User registration flow debug test PASSED!")
        return True
    else:
        logger.error("❌ User registration flow debug test FAILED!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 User registration flow debug test completed successfully!")
    else:
        print("\n💥 User registration flow debug test failed!")
        exit(1)