#!/usr/bin/env python3
"""
Test script to test authentication flows with proper error handling
This addresses task T041: [DEBUG] Test authentication flows with proper error handling
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

async def test_error_handling():
    """Test authentication flows with proper error handling."""
    logger.info("Starting authentication error handling tests...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with error handling tests")
        return False

    # Test 1: Registration with invalid data
    logger.info("Test 1: Registration with invalid data")

    # Test registration with invalid email
    invalid_email_result = await auth_service.register_user(
        email="invalid-email",
        name="Test User",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if invalid_email_result is None:
        logger.info("✅ Correctly rejected invalid email format")
    else:
        logger.error("❌ Incorrectly accepted invalid email format")
        return False

    # Test registration with short password
    short_password_result = await auth_service.register_user(
        email="valid@example.com",
        name="Test User",
        password="short",
        experience_level="beginner"
    )
    if short_password_result is None:
        logger.info("✅ Correctly rejected short password")
    else:
        logger.error("❌ Incorrectly accepted short password")
        return False

    # Test registration with invalid experience level
    invalid_exp_result = await auth_service.register_user(
        email="valid@example.com",
        name="Test User",
        password="SecurePassword123!",
        experience_level="invalid_level"
    )
    if invalid_exp_result is None:
        logger.info("✅ Correctly rejected invalid experience level")
    else:
        logger.error("❌ Incorrectly accepted invalid experience level")
        return False

    # Test registration with empty name
    empty_name_result = await auth_service.register_user(
        email="valid@example.com",
        name="",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if empty_name_result is None:
        logger.info("✅ Correctly rejected empty name")
    else:
        logger.error("❌ Incorrectly accepted empty name")
        return False

    # Create a valid user for further testing
    test_email = f"error_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "Error Test User"
    test_password = "SecurePassword123!"
    test_experience = "beginner"

    valid_reg_result = await auth_service.register_user(
        email=test_email,
        name=test_name,
        password=test_password,
        experience_level=test_experience
    )

    if not valid_reg_result:
        logger.error("Failed to create valid test user")
        return False

    logger.info("Valid test user created successfully")

    # Test 2: Registration with duplicate email
    duplicate_result = await auth_service.register_user(
        email=test_email,  # Same email as existing user
        name="Another User",
        password="AnotherPassword123!",
        experience_level="intermediate"
    )
    if duplicate_result is None:
        logger.info("✅ Correctly rejected duplicate email registration")
    else:
        logger.error("❌ Incorrectly allowed duplicate email registration")
        return False

    # Test 3: Login with invalid credentials
    logger.info("Test 3: Login with invalid credentials")

    # Login with non-existent email
    invalid_login_result = await auth_service.authenticate_user(
        email="nonexistent@example.com",
        password="AnyPassword123!"
    )
    if invalid_login_result is None:
        logger.info("✅ Correctly rejected login with non-existent email")
    else:
        logger.error("❌ Incorrectly accepted login with non-existent email")
        return False

    # Login with wrong password
    wrong_password_result = await auth_service.authenticate_user(
        email=test_email,
        password="WrongPassword123!"
    )
    if wrong_password_result is None:
        logger.info("✅ Correctly rejected login with wrong password")
    else:
        logger.error("❌ Incorrectly accepted login with wrong password")
        return False

    # Login with empty email
    empty_email_result = await auth_service.authenticate_user(
        email="",
        password="AnyPassword123!"
    )
    if empty_email_result is None:
        logger.info("✅ Correctly rejected login with empty email")
    else:
        logger.error("❌ Incorrectly accepted login with empty email")
        return False

    # Login with empty password
    empty_password_result = await auth_service.authenticate_user(
        email=test_email,
        password=""
    )
    if empty_password_result is None:
        logger.info("✅ Correctly rejected login with empty password")
    else:
        logger.error("❌ Incorrectly accepted login with empty password")
        return False

    # Test 4: Profile access with invalid tokens
    logger.info("Test 4: Profile access with invalid tokens")

    # Try to get profile with invalid token
    from backend.src.services.auth_service import auth_service
    invalid_profile = await auth_service.get_user_profile("invalid_user_id")
    if invalid_profile is None:
        logger.info("✅ Correctly handled invalid user ID for profile access")
    else:
        logger.error("❌ Incorrectly returned profile for invalid user ID")
        return False

    # Test 5: Session validation with invalid tokens
    logger.info("Test 5: Session validation with invalid tokens")

    invalid_session = await auth_service.validate_session_token("invalid_token")
    if invalid_session is None:
        logger.info("✅ Correctly rejected invalid session token")
    else:
        logger.error("❌ Incorrectly accepted invalid session token")
        return False

    # Test with empty token
    empty_session = await auth_service.validate_session_token("")
    if empty_session is None:
        logger.info("✅ Correctly rejected empty session token")
    else:
        logger.error("❌ Incorrectly accepted empty session token")
        return False

    # Test with short token
    short_token = await auth_service.validate_session_token("short")
    if short_token is None:
        logger.info("✅ Correctly rejected short session token")
    else:
        logger.error("❌ Incorrectly accepted short session token")
        return False

    logger.info("✅ All error handling tests passed!")
    return True

async def main():
    """Run all error handling tests."""
    logger.info("Starting authentication error handling tests...")

    success = await test_error_handling()

    if success:
        print("\n🎉 Authentication error handling tests completed successfully!")
        return True
    else:
        print("\n💥 Authentication error handling tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)