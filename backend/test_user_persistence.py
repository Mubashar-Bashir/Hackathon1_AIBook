"""Test script to verify user data persistence in Neon database."""

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
    logger.info("Starting user data persistence verification test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db, get_db_session
    from src.models.user import User
    from sqlalchemy import select

    # Initialize database
    await init_db()

    # Create auth service instance
    auth_service = AuthService()

    # Test data
    test_email = f"persistence_test_{uuid.uuid4().hex[:8]}@example.com"
    test_name = "Persistence Test User"
    test_password = "SecurePassword123!"
    test_experience_level = "intermediate"
    test_preferences = {"theme": "dark", "notifications": True, "language": "en"}

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

    # Verify the user exists in the database directly
    db_gen = get_db_session()
    db = await db_gen.__anext__()  # Get the session from the generator
    try:
        # Query the user directly from the database
        result = await db.execute(select(User).filter_by(id=user_id))
        user_from_db = result.scalars().first()

        if not user_from_db:
            logger.error("User was not found in database after registration")
            return False

        # Verify all fields are correctly stored
        checks_passed = True
        if user_from_db.email != test_email:
            logger.error(f"Email mismatch: expected {test_email}, got {user_from_db.email}")
            checks_passed = False
        if user_from_db.name != test_name:
            logger.error(f"Name mismatch: expected {test_name}, got {user_from_db.name}")
            checks_passed = False
        if user_from_db.experience_level != test_experience_level:
            logger.error(f"Experience level mismatch: expected {test_experience_level}, got {user_from_db.experience_level}")
            checks_passed = False
        if user_from_db.is_active != True:
            logger.error(f"Active status mismatch: expected True, got {user_from_db.is_active}")
            checks_passed = False
        if user_from_db.is_verified != False:
            logger.error(f"Verified status mismatch: expected False, got {user_from_db.is_verified}")
            checks_passed = False
        if not user_from_db.password_hash:
            logger.error("Password hash is empty")
            checks_passed = False
        if not user_from_db.created_at:
            logger.error("Created at timestamp is missing")
            checks_passed = False
        if user_from_db.updated_at != user_from_db.created_at:  # Initially should be the same
            logger.warning(f"Updated at ({user_from_db.updated_at}) != Created at ({user_from_db.created_at})")

        if checks_passed:
            logger.info("All user data fields verified successfully in database")
        else:
            logger.error("Some user data fields failed verification")
            return False

        # Test updating user profile
        logger.info("Testing user profile update...")
        updated_name = "Updated Persistence Test User"
        updated_experience = "advanced"

        # Use the auth service to update the profile
        update_result = await auth_service.update_user_profile(
            user_id=user_id,
            update_data={
                "name": updated_name,
                "experience_level": updated_experience,
                "preferences": test_preferences
            }
        )

        if not update_result:
            logger.error("User profile update failed")
            return False

        # Verify the update in database
        result = await db.execute(select(User).filter_by(id=user_id))
        updated_user = result.scalars().first()

        if updated_user.name != updated_name:
            logger.error(f"Name update failed: expected {updated_name}, got {updated_user.name}")
            return False
        if updated_user.experience_level != updated_experience:
            logger.error(f"Experience level update failed: expected {updated_experience}, got {updated_user.experience_level}")
            return False
        if updated_user.updated_at > updated_user.created_at:
            logger.info("Updated timestamp is correctly greater than created timestamp")
        else:
            logger.error("Updated timestamp is not greater than created timestamp")
            return False

        logger.info("User profile update verified successfully")

        # Test getting user profile via auth service
        logger.info("Testing get user profile via auth service...")
        profile_result = await auth_service.get_user_profile(user_id)

        if not profile_result:
            logger.error("Failed to retrieve user profile via auth service")
            return False

        if profile_result.email != test_email:
            logger.error(f"Profile email mismatch: expected {test_email}, got {profile_result.email}")
            return False
        if profile_result.name != updated_name:
            logger.error(f"Profile name mismatch: expected {updated_name}, got {profile_result.name}")
            return False
        if profile_result.experience_level != updated_experience:
            logger.error(f"Profile experience level mismatch: expected {updated_experience}, got {profile_result.experience_level}")
            return False

        logger.info("User profile retrieval verified successfully")

        # Test user authentication after updates
        logger.info("Testing user authentication after updates...")
        auth_result = await auth_service.authenticate_user(
            email=test_email,
            password=test_password
        )

        if not auth_result:
            logger.error("User authentication failed after updates")
            return False

        if auth_result["user_id"] != user_id:
            logger.error(f"Authentication user ID mismatch: expected {user_id}, got {auth_result['user_id']}")
            return False

        logger.info("User authentication verified successfully after updates")

    finally:
        await db_gen.aclose()

    logger.info("All user data persistence tests passed!")
    return True

async def test_user_data_consistency():
    """Test data consistency across different operations."""
    logger.info("Starting user data consistency test...")

    # Import after setup
    from src.services.auth_service import AuthService
    from src.utils.database import init_db, get_db_session
    from src.models.user import User
    from sqlalchemy import select

    # Create auth service instance
    auth_service = AuthService()

    # Test data
    test_email = f"consistency_test_{uuid.uuid4().hex[:8]}@example.com"
    test_name = "Consistency Test User"
    test_password = "SecurePassword123!"
    test_experience_level = "beginner"

    # Register a user
    registration_result = await auth_service.register_user(
        email=test_email,
        name=test_name,
        password=test_password,
        experience_level=test_experience_level
    )

    if not registration_result:
        logger.error("User registration failed for consistency test")
        return False

    user_id = registration_result["user_id"]
    logger.info(f"User registered for consistency test. User ID: {user_id}")

    # Get the user profile multiple times to check consistency
    profile1 = await auth_service.get_user_profile(user_id)
    profile2 = await auth_service.get_user_profile(user_id)
    profile3 = await auth_service.get_user_profile(user_id)

    if not all([profile1, profile2, profile3]):
        logger.error("Failed to retrieve user profile multiple times")
        return False

    # Check that all profiles are identical
    if profile1.email != profile2.email or profile2.email != profile3.email:
        logger.error("Email is inconsistent across profile retrievals")
        return False
    if profile1.name != profile2.name or profile2.name != profile3.name:
        logger.error("Name is inconsistent across profile retrievals")
        return False
    if profile1.experience_level != profile2.experience_level or profile2.experience_level != profile3.experience_level:
        logger.error("Experience level is inconsistent across profile retrievals")
        return False

    logger.info("User data consistency verified across multiple retrievals")

    # Check that the data in the database is also consistent
    db_gen = get_db_session()
    db = await db_gen.__anext__()  # Get the session from the generator
    try:
        result = await db.execute(select(User).filter_by(id=user_id))
        db_user = result.scalars().first()

        if db_user.email != profile1.email:
            logger.error("Database email doesn't match service email")
            return False
        if db_user.name != profile1.name:
            logger.error("Database name doesn't match service name")
            return False
        if db_user.experience_level != profile1.experience_level:
            logger.error("Database experience level doesn't match service experience level")
            return False

        logger.info("Database consistency verified with service data")
    finally:
        await db_gen.aclose()

    return True

async def main():
    """Main function to run user data persistence tests."""
    logger.info("Starting user data persistence verification tests...")

    # Run the persistence test
    persistence_success = await test_user_data_persistence()
    consistency_success = await test_user_data_consistency() if persistence_success else False

    logger.info(f"User data persistence test: {'PASS' if persistence_success else 'FAIL'}")
    logger.info(f"User data consistency test: {'PASS' if consistency_success else 'FAIL'}")

    overall_success = persistence_success and consistency_success
    logger.info(f"Overall user data persistence: {'PASS' if overall_success else 'FAIL'}")

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)