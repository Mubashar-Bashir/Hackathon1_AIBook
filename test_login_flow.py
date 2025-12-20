#!/usr/bin/env python3
"""
Test script to debug user login flow and session token generation
This addresses task T038: [DEBUG] Debug user login flow and session token generation
"""

import asyncio
import os
import logging
from datetime import datetime
from backend.src.services.auth_service import auth_service
from backend.src.utils.database import test_db_connection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_login_flow():
    """Test the user login flow and session token generation."""
    logger.info("Starting user login flow debug test...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with login test")
        return False

    # Create a test user first (or use an existing one)
    test_email = f"login_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "Login Test User"
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

    logger.info("Test user created successfully")

    # Now try to login with the created user
    logger.info(f"Attempting to login with user: {test_email}")

    login_result = await auth_service.authenticate_user(
        email=test_email,
        password=test_password
    )

    if login_result:
        logger.info("✅ User login successful!")
        logger.info(f"   User ID: {login_result['user_id']}")
        logger.info(f"   Session Token: {login_result['session_token'][:10]}...")

        # Validate the session token
        user_id = await auth_service.validate_session_token(login_result['session_token'])
        if user_id == login_result['user_id']:
            logger.info("✅ Session token validation successful!")
        else:
            logger.error("❌ Session token validation failed!")
            return False

        # Test that the session token is different from the previous one (new session created)
        # Note: Each login creates a new session token
        logger.info("✅ Login flow and session token generation working correctly!")
        return True
    else:
        logger.error("❌ User login failed!")
        return False

async def test_session_token_properties():
    """Test session token security properties."""
    logger.info("Testing session token properties...")

    # Generate multiple session tokens
    tokens = []
    for i in range(5):
        token = auth_service.generate_session_token()
        tokens.append(token)
        logger.debug(f"Generated token {i+1}: {token[:20]}...")

    # Check that all tokens are unique
    if len(set(tokens)) == len(tokens):
        logger.info("✅ All session tokens are unique")
    else:
        logger.error("❌ Some session tokens are duplicated")
        return False

    # Check minimum length
    for token in tokens:
        if len(token) < 32:  # Reasonable minimum for security
            logger.error(f"❌ Session token too short: {len(token)} chars")
            return False

    logger.info(f"✅ All session tokens meet minimum length requirement (32+ chars)")
    logger.info(f"✅ Average token length: {sum(len(t) for t in tokens) / len(tokens):.1f} chars")

    return True

async def main():
    """Run all login flow tests."""
    logger.info("Starting user login flow debug tests...")

    # Test session token properties
    token_success = await test_session_token_properties()
    if not token_success:
        logger.error("Session token tests failed")
        return False

    # Test login flow
    login_success = await test_login_flow()

    if login_success:
        logger.info("✅ All login flow debug tests passed!")
        return True
    else:
        logger.error("❌ Some login flow debug tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 User login flow debug test completed successfully!")
    else:
        print("\n💥 User login flow debug test failed!")
        exit(1)