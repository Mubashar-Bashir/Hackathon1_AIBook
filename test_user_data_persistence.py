#!/usr/bin/env python3
"""
Test script to verify user data persistence in Neon database
This addresses task T040: [DEBUG] Verify user data persistence in Neon database
"""

import asyncio
import os
import logging
from datetime import datetime
from backend.src.services.auth_service import auth_service
from backend.src.utils.database import test_db_connection
from sqlalchemy import select

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_user_data_persistence():
    """Test user data persistence in the database."""
    logger.info("Starting user data persistence verification...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with data persistence test")
        return False

    # Create a test user
    test_email = f"persistence_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "Persistence Test User"
    test_password = "SecurePassword123!"
    test_experience = "beginner"
    test_username = f"testuser_{int(datetime.now().timestamp())}"

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

    user_id = reg_result['user_id']
    logger.info(f"Test user created successfully with ID: {user_id}")

    # Verify the user exists in the database by querying directly
    try:
        from backend.src.models.user import User
        from backend.src.utils.database import get_db_session

        # Get database session
        db_gen = get_db_session()
        db = await db_gen.__anext__()

        try:
            # Query the user directly from the database
            result = await db.execute(select(User).filter_by(id=user_id))
            user_from_db = result.scalars().first()

            if user_from_db:
                logger.info("✅ User found in database directly")
                logger.info(f"   Email: {user_from_db.email}")
                logger.info(f"   Name: {user_from_db.name}")
                logger.info(f"   Experience: {user_from_db.experience_level}")
                logger.info(f"   Created: {user_from_db.created_at}")

                # Verify data integrity
                checks_passed = 0
                total_checks = 0

                total_checks += 1
                if user_from_db.email == test_email:
                    logger.info("✅ Email correctly persisted")
                    checks_passed += 1
                else:
                    logger.error(f"❌ Email mismatch: expected {test_email}, got {user_from_db.email}")

                total_checks += 1
                if user_from_db.name == test_name:
                    logger.info("✅ Name correctly persisted")
                    checks_passed += 1
                else:
                    logger.error(f"❌ Name mismatch: expected {test_name}, got {user_from_db.name}")

                total_checks += 1
                if user_from_db.experience_level == test_experience:
                    logger.info("✅ Experience level correctly persisted")
                    checks_passed += 1
                else:
                    logger.error(f"❌ Experience level mismatch: expected {test_experience}, got {user_from_db.experience_level}")

                total_checks += 1
                if user_from_db.password_hash and len(user_from_db.password_hash) > 10:  # Should be hashed
                    logger.info("✅ Password correctly hashed and persisted")
                    checks_passed += 1
                else:
                    logger.error(f"❌ Password not properly hashed: {user_from_db.password_hash}")

                total_checks += 1
                if user_from_db.id == user_id:
                    logger.info("✅ User ID correctly persisted")
                    checks_passed += 1
                else:
                    logger.error(f"❌ User ID mismatch: expected {user_id}, got {user_from_db.id}")

                if checks_passed == total_checks:
                    logger.info(f"✅ All {total_checks} data integrity checks passed!")
                else:
                    logger.error(f"❌ Only {checks_passed}/{total_checks} data integrity checks passed")
                    return False

            else:
                logger.error("❌ User not found in database directly")
                return False

        finally:
            await db_gen.aclose()

    except Exception as e:
        logger.error(f"❌ Error querying user from database: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test updating user data and verifying persistence
    logger.info("Testing user data update and persistence...")

    update_data = {
        'name': 'Updated Test User',
        'username': test_username,
        'experience_level': 'intermediate'
    }

    updated_profile = await auth_service.update_user_profile(user_id, update_data)
    if updated_profile:
        logger.info("✅ User profile updated successfully")

        # Verify the update in the database
        db_gen = get_db_session()
        db = await db_gen.__anext__()

        try:
            result = await db.execute(select(User).filter_by(id=user_id))
            updated_user = result.scalars().first()

            if updated_user:
                update_checks_passed = 0
                total_update_checks = 0

                total_update_checks += 1
                if updated_user.name == 'Updated Test User':
                    logger.info("✅ Updated name correctly persisted")
                    update_checks_passed += 1
                else:
                    logger.error(f"❌ Updated name not persisted correctly: {updated_user.name}")

                total_update_checks += 1
                if updated_user.username == test_username:
                    logger.info("✅ Updated username correctly persisted")
                    update_checks_passed += 1
                else:
                    logger.error(f"❌ Updated username not persisted correctly: {updated_user.username}")

                total_update_checks += 1
                if updated_user.experience_level == 'intermediate':
                    logger.info("✅ Updated experience level correctly persisted")
                    update_checks_passed += 1
                else:
                    logger.error(f"❌ Updated experience level not persisted correctly: {updated_user.experience_level}")

                if update_checks_passed == total_update_checks:
                    logger.info(f"✅ All {total_update_checks} update integrity checks passed!")
                else:
                    logger.error(f"❌ Only {update_checks_passed}/{total_update_checks} update integrity checks passed")
                    return False

            else:
                logger.error("❌ Updated user not found in database")
                return False

        finally:
            await db_gen.aclose()

    else:
        logger.error("❌ User profile update failed")
        return False

    logger.info("✅ User data persistence verification completed successfully!")
    return True

async def main():
    """Run all user data persistence tests."""
    logger.info("Starting user data persistence verification tests...")

    success = await test_user_data_persistence()

    if success:
        print("\n🎉 User data persistence verification completed successfully!")
        return True
    else:
        print("\n💥 User data persistence verification failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)