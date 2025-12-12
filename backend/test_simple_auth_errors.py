"""Simple test to verify authentication error handling."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
import uuid

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_simple_auth_errors():
    """Test basic authentication error handling."""
    logger.info("Starting simple authentication error handling test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test 1: Invalid email format
    result1 = await auth_service.register_user(
        email="invalid-email",
        name="Test User",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if result1 is not None:
        logger.error("Test 1 failed: Invalid email should be rejected")
        return False
    logger.info("✓ Test 1 passed: Invalid email correctly rejected")

    # Test 2: Weak password
    result2 = await auth_service.register_user(
        email="test@example.com",
        name="Test User",
        password="weak",
        experience_level="beginner"
    )
    if result2 is not None:
        logger.error("Test 2 failed: Weak password should be rejected")
        return False
    logger.info("✓ Test 2 passed: Weak password correctly rejected")

    # Test 3: Invalid experience level
    result3 = await auth_service.register_user(
        email="test@example.com",
        name="Test User",
        password="SecurePassword123!",
        experience_level="invalid_level"
    )
    if result3 is not None:
        logger.error("Test 3 failed: Invalid experience level should be rejected")
        return False
    logger.info("✓ Test 3 passed: Invalid experience level correctly rejected")

    # Test 4: Empty name
    result4 = await auth_service.register_user(
        email="test@example.com",
        name="",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if result4 is not None:
        logger.error("Test 4 failed: Empty name should be rejected")
        return False
    logger.info("✓ Test 4 passed: Empty name correctly rejected")

    # Test 5: Valid registration should work
    valid_email = f"valid_test_{uuid.uuid4().hex[:8]}@example.com"
    result5 = await auth_service.register_user(
        email=valid_email,
        name="Valid User",
        password="SecurePassword123!",
        experience_level="beginner"
    )
    if result5 is None:
        logger.error("Test 5 failed: Valid registration should succeed")
        return False
    logger.info("✓ Test 5 passed: Valid registration succeeded")

    # Test 6: Invalid email in login
    result6 = await auth_service.authenticate_user(
        email="invalid-email",
        password="any_password"
    )
    if result6 is not None:
        logger.error("Test 6 failed: Invalid email in login should be rejected")
        return False
    logger.info("✓ Test 6 passed: Invalid email in login correctly rejected")

    # Test 7: Valid login should work
    result7 = await auth_service.authenticate_user(
        email=valid_email,
        password="SecurePassword123!"
    )
    if result7 is None:
        logger.error("Test 7 failed: Valid login should succeed")
        return False
    logger.info("✓ Test 7 passed: Valid login succeeded")

    logger.info("All authentication error handling tests passed!")
    return True

async def main():
    """Main function to run simple authentication error handling test."""
    logger.info("Starting simple authentication error handling tests...")

    success = await test_simple_auth_errors()

    logger.info(f"Simple authentication error handling test: {'PASS' if success else 'FAIL'}")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)