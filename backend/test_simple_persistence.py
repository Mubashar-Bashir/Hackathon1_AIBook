"""Simple test to verify user data persistence in Neon database."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_user_data_persistence():
    """Test that user data is properly persisted and can be retrieved."""
    logger.info("Starting simple user data persistence verification test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test data
    test_email = f"simple_persist_test_{uuid.uuid4().hex[:8]}@example.com"
    test_name = "Simple Persistence Test User"
    test_password = "SecurePassword123!"
    test_experience_level = "beginner"

    logger.info(f"Creating test user: {test_email}")

    # Register a user
    registration_result = await auth_service.register_user(
        email=test_email,
        name=test_name,
        password=test_password,
        experience_level=test_experience_level
    )

    if not registration_result:
        logger.error("User registration failed")
        return False

    user_id = registration_result["user_id"]
    logger.info(f"User registered successfully. User ID: {user_id}")

    # Verify the user can be retrieved via the auth service
    profile_result = await auth_service.get_user_profile(user_id)

    if not profile_result:
        logger.error("Failed to retrieve user profile via auth service")
        return False

    # Verify the retrieved data matches what we stored
    if profile_result.email != test_email:
        logger.error(f"Email mismatch: expected {test_email}, got {profile_result.email}")
        return False
    if profile_result.name != test_name:
        logger.error(f"Name mismatch: expected {test_name}, got {profile_result.name}")
        return False
    if profile_result.experience_level != test_experience_level:
        logger.error(f"Experience level mismatch: expected {test_experience_level}, got {profile_result.experience_level}")
        return False

    logger.info("User data retrieved and verified successfully!")

    # Test that the user can be authenticated
    auth_result = await auth_service.authenticate_user(
        email=test_email,
        password=test_password
    )

    if not auth_result:
        logger.error("User authentication failed")
        return False

    if auth_result["user_id"] != user_id:
        logger.error(f"Authentication user ID mismatch: expected {user_id}, got {auth_result['user_id']}")
        return False

    logger.info("User authentication verified successfully!")

    # Test updating the user profile
    updated_name = "Updated Simple Persistence Test User"
    update_result = await auth_service.update_user_profile(
        user_id=user_id,
        update_data={"name": updated_name}
    )

    if not update_result:
        logger.error("User profile update failed")
        return False

    # Verify the update
    updated_profile = await auth_service.get_user_profile(user_id)
    if updated_profile.name != updated_name:
        logger.error(f"Name update failed: expected {updated_name}, got {updated_profile.name}")
        return False

    logger.info("User profile update verified successfully!")

    logger.info("All simple user data persistence tests passed!")
    return True

async def main():
    """Main function to run simple user data persistence test."""
    logger.info("Starting simple user data persistence verification test...")

    # Run the persistence test
    success = await test_user_data_persistence()

    logger.info(f"Simple user data persistence test: {'PASS' if success else 'FAIL'}")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)