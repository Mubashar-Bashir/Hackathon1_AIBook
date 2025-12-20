#!/usr/bin/env python3
"""
Database integration tests for user persistence
This addresses task T045: [P] Create database integration tests for user persistence
"""

import asyncio
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import select
from backend.src.models.user import User
from backend.src.models.session import Session
from backend.src.services.auth_service import auth_service
from backend.src.utils.database import get_db_session, test_db_connection, init_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_database_integration():
    """Test database integration for user persistence."""
    logger.info("Starting database integration tests for user persistence...")

    # First, test database connection
    logger.info("Testing database connection...")
    db_connected = await test_db_connection()
    if not db_connected:
        logger.error("Database connection failed - cannot proceed with database integration tests")
        return False

    # Initialize database tables
    logger.info("Initializing database tables...")
    try:
        await init_db()
        logger.info("✅ Database tables initialized successfully")
    except Exception as e:
        logger.error(f"❌ Error initializing database tables: {e}")
        return False

    # Test 1: Direct database operations
    logger.info("Test 1: Direct database operations")

    # Create a user directly through the database
    test_email = f"db_integration_test_{int(datetime.now().timestamp())}@example.com"
    test_name = "DB Integration Test User"
    test_experience = "advanced"

    # Hash the password manually for direct DB insertion
    password_hash = auth_service.hash_password("SecurePassword123!")

    # Get database session
    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        # Create user directly in database
        import uuid

        new_user = User(
            id=str(uuid.uuid4()),
            email=test_email,
            name=test_name,
            experience_level=test_experience,
            password_hash=password_hash
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        logger.info(f"✅ User created directly in database: {new_user.id}")

        # Verify the user can be retrieved directly from database
        result = await db.execute(select(User).filter_by(email=test_email))
        retrieved_user = result.scalars().first()

        if retrieved_user and retrieved_user.email == test_email:
            logger.info("✅ User successfully retrieved from database")
        else:
            logger.error("❌ User not found in database after creation")
            return False

    except Exception as e:
        logger.error(f"❌ Error in direct database operations: {e}")
        return False
    finally:
        await db_gen.aclose()

    # Test 2: Service-layer operations and database persistence
    logger.info("Test 2: Service-layer operations and database persistence")

    # Use auth service to create another user
    service_email = f"service_integration_test_{int(datetime.now().timestamp())}@example.com"
    service_name = "Service Integration Test User"
    service_password = "SecurePassword123!"
    service_experience = "intermediate"

    reg_result = await auth_service.register_user(
        email=service_email,
        name=service_name,
        password=service_password,
        experience_level=service_experience
    )

    if not reg_result:
        logger.error("❌ Failed to create user through auth service")
        return False

    service_user_id = reg_result['user_id']
    logger.info(f"✅ User created through auth service: {service_user_id}")

    # Verify the user exists in database through direct query
    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        result = await db.execute(select(User).filter_by(id=service_user_id))
        service_user = result.scalars().first()

        if service_user and service_user.email == service_email:
            logger.info("✅ Service-created user found in database")
        else:
            logger.error("❌ Service-created user not found in database")
            return False

    finally:
        await db_gen.aclose()

    # Test 3: Session creation and persistence
    logger.info("Test 3: Session creation and persistence")

    # The registration above should have created a session
    # Let's create another session using session_service
    from backend.src.services.session_service import session_service

    session_result = await session_service.create_session(
        user_id=service_user_id,
        ip_address="127.0.0.1",
        user_agent="Integration Test Agent"
    )

    if session_result:
        logger.info(f"✅ Session created through session service: {session_result['id']}")
    else:
        logger.error("❌ Failed to create session through session service")
        return False

    # Verify session exists in database
    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        result = await db.execute(select(Session).filter_by(user_id=service_user_id))
        sessions = result.scalars().all()

        if len(sessions) > 0:
            logger.info(f"✅ Found {len(sessions)} sessions for user in database")
        else:
            logger.error("❌ No sessions found for user in database")
            return False

    finally:
        await db_gen.aclose()

    # Test 4: Data consistency between service and database
    logger.info("Test 4: Data consistency between service and database")

    # Get user profile through service
    profile = await auth_service.get_user_profile(service_user_id)
    if not profile:
        logger.error("❌ Failed to retrieve user profile through service")
        return False

    logger.info(f"✅ Retrieved user profile through service: {profile.email}")

    # Get user directly from database
    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        result = await db.execute(select(User).filter_by(id=service_user_id))
        db_user = result.scalars().first()

        if db_user:
            # Compare key fields
            consistency_checks = 0
            total_checks = 0

            total_checks += 1
            if profile.email == db_user.email:
                logger.info("✅ Email consistency: service ↔ database")
                consistency_checks += 1
            else:
                logger.error(f"❌ Email inconsistency: {profile.email} vs {db_user.email}")

            total_checks += 1
            if profile.name == db_user.name:
                logger.info("✅ Name consistency: service ↔ database")
                consistency_checks += 1
            else:
                logger.error(f"❌ Name inconsistency: {profile.name} vs {db_user.name}")

            total_checks += 1
            if profile.experience_level == db_user.experience_level:
                logger.info("✅ Experience level consistency: service ↔ database")
                consistency_checks += 1
            else:
                logger.error(f"❌ Experience level inconsistency: {profile.experience_level} vs {db_user.experience_level}")

            if consistency_checks == total_checks:
                logger.info(f"✅ All {total_checks} consistency checks passed!")
            else:
                logger.error(f"❌ Only {consistency_checks}/{total_checks} consistency checks passed")
                return False

        else:
            logger.error("❌ User not found in database during consistency check")
            return False

    finally:
        await db_gen.aclose()

    # Test 5: Transaction integrity
    logger.info("Test 5: Transaction integrity")

    # Test that invalid operations are properly rolled back
    from sqlalchemy.exc import IntegrityError

    db_gen = get_db_session()
    db = await db_gen.__anext__()

    try:
        # Try to create a user with duplicate email (should fail)
        duplicate_user = User(
            id=str(uuid.uuid4()),
            email=test_email,  # Use email from first test user
            name="Duplicate Test User",
            experience_level="beginner",
            password_hash=auth_service.hash_password("AnotherPassword123!")
        )

        db.add(duplicate_user)
        await db.commit()  # This should fail due to unique constraint

        # If we get here, the constraint didn't work properly
        logger.error("❌ Database constraint failed - allowed duplicate email")
        return False

    except IntegrityError:
        # This is expected - the constraint should prevent duplicate emails
        await db.rollback()
        logger.info("✅ Database constraint properly prevented duplicate email")
    except Exception as e:
        logger.error(f"❌ Unexpected error during transaction test: {e}")
        return False
    finally:
        await db_gen.aclose()

    logger.info("✅ All database integration tests passed!")
    return True

async def main():
    """Run all database integration tests."""
    logger.info("Starting database integration tests for user persistence...")

    success = await test_database_integration()

    if success:
        print("\n🎉 Database integration tests completed successfully!")
        return True
    else:
        print("\n💥 Database integration tests failed!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    if not success:
        exit(1)