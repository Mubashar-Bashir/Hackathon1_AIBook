"""Test script to verify authentication flows with proper error handling."""

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
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_authentication_error_handling():
    """Test authentication flows with proper error handling."""
    logger.info("Starting authentication error handling test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test 1: Registration with invalid email format
    logger.info("Testing registration with invalid email format...")
    invalid_email_result = await auth_service.register_user(
        email="invalid-email",
        name="Invalid Email User",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if invalid_email_result is not None:
        logger.error("Registration should have failed with invalid email")
        return False
    logger.info("✓ Registration correctly failed with invalid email format")

    # Test 2: Registration with weak password
    logger.info("Testing registration with weak password...")
    weak_password_result = await auth_service.register_user(
        email="weakpass@example.com",
        name="Weak Password User",
        password="weak",  # Too short
        experience_level="beginner"
    )
    if weak_password_result is not None:
        logger.error("Registration should have failed with weak password")
        return False
    logger.info("✓ Registration correctly failed with weak password")

    # Test 3: Registration with invalid experience level
    logger.info("Testing registration with invalid experience level...")
    invalid_exp_result = await auth_service.register_user(
        email="invalidexp@example.com",
        name="Invalid Exp User",
        password="SecurePassword123!",
        experience_level="invalid_level"
    )
    if invalid_exp_result is not None:
        logger.error("Registration should have failed with invalid experience level")
        return False
    logger.info("✓ Registration correctly failed with invalid experience level")

    # Test 4: Register a valid user
    valid_email = f"valid_user_{uuid.uuid4().hex[:8]}@example.com"
    logger.info(f"Registering valid user: {valid_email}...")
    valid_registration = await auth_service.register_user(
        email=valid_email,
        name="Valid User",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if not valid_registration:
        logger.error("Valid registration failed")
        return False
    logger.info("✓ Valid user registration successful")

    # Test 5: Registration with duplicate email
    logger.info("Testing registration with duplicate email...")
    duplicate_result = await auth_service.register_user(
        email=valid_email,
        name="Duplicate User",
        password="AnotherPassword123!",
        experience_level="intermediate"
    )
    if duplicate_result is not None:
        logger.error("Registration should have failed with duplicate email")
        return False
    logger.info("✓ Registration correctly failed with duplicate email")

    # Test 6: Login with wrong password
    logger.info("Testing login with wrong password...")
    wrong_password_result = await auth_service.authenticate_user(
        email=valid_email,
        password="WrongPassword123!"
    )
    if wrong_password_result is not None:
        logger.error("Login should have failed with wrong password")
        return False
    logger.info("✓ Login correctly failed with wrong password")

    # Test 7: Login with non-existent email
    logger.info("Testing login with non-existent email...")
    non_existent_result = await auth_service.authenticate_user(
        email="nonexistent@example.com",
        password="AnyPassword123!"
    )
    if non_existent_result is not None:
        logger.error("Login should have failed with non-existent email")
        return False
    logger.info("✓ Login correctly failed with non-existent email")

    # Test 8: Get profile for non-existent user
    logger.info("Testing get profile for non-existent user...")
    fake_user_id = str(uuid.uuid4())
    profile_result = await auth_service.get_user_profile(fake_user_id)
    if profile_result is not None:
        logger.error("Get profile should have failed for non-existent user")
        return False
    logger.info("✓ Get profile correctly failed for non-existent user")

    # Test 9: Update profile for non-existent user
    logger.info("Testing update profile for non-existent user...")
    update_result = await auth_service.update_user_profile(
        user_id=fake_user_id,
        update_data={"name": "Updated Name"}
    )
    if update_result is not None:
        logger.error("Update profile should have failed for non-existent user")
        return False
    logger.info("✓ Update profile correctly failed for non-existent user")

    # Test 10: Validate invalid session token
    logger.info("Testing validate invalid session token...")
    invalid_token_result = await auth_service.validate_session_token("invalid_token")
    if invalid_token_result is not None:
        logger.error("Session validation should have failed for invalid token")
        return False
    logger.info("✓ Session validation correctly failed for invalid token")

    # Test 11: Test session expiration (if applicable)
    logger.info("Testing authentication flow error handling - all tests passed!")
    return True

async def test_edge_cases():
    """Test edge cases for authentication error handling."""
    logger.info("Starting edge case testing...")

    # Import after setup
    from src.services.auth_service import AuthService

    # Create auth service instance
    auth_service = AuthService()

    # Test with empty strings
    logger.info("Testing with empty strings...")
    try:
        empty_email_result = await auth_service.register_user(
            email="",
            name="Empty Email User",
            password="SecurePassword123!",
            experience_level="beginner"
        )
        if empty_email_result is not None:
            logger.error("Registration should have failed with empty email")
            return False
        logger.info("✓ Registration correctly failed with empty email")
    except Exception as e:
        logger.info(f"✓ Registration failed as expected with empty email: {e}")

    try:
        empty_name_result = await auth_service.register_user(
            email=f"emptyname_{uuid.uuid4().hex[:8]}@example.com",
            name="",  # Empty name
            password="SecurePassword123!",
            experience_level="beginner"
        )
        if empty_name_result is not None:
            logger.error("Registration should have failed with empty name")
            return False
        logger.info("✓ Registration correctly failed with empty name")
    except Exception as e:
        logger.info(f"✓ Registration failed as expected with empty name: {e}")

    # Test with None values
    logger.info("Testing with None values...")
    try:
        none_result = await auth_service.register_user(
            email=None,
            name="None Email User",
            password="SecurePassword123!",
            experience_level="beginner"
        )
        if none_result is not None:
            logger.error("Registration should have failed with None email")
            return False
        logger.info("✓ Registration correctly failed with None email")
    except Exception as e:
        logger.info(f"✓ Registration failed as expected with None email: {e}")

    return True

async def main():
    """Main function to run authentication error handling tests."""
    logger.info("Starting authentication error handling tests...")

    # Run the authentication error handling test
    auth_error_success = await test_authentication_error_handling()
    edge_case_success = await test_edge_cases() if auth_error_success else False

    logger.info(f"Authentication error handling test: {'PASS' if auth_error_success else 'FAIL'}")
    logger.info(f"Edge case handling test: {'PASS' if edge_case_success else 'FAIL'}")

    overall_success = auth_error_success and edge_case_success
    logger.info(f"Overall authentication error handling: {'PASS' if overall_success else 'FAIL'}")

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)