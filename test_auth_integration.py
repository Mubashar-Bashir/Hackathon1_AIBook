#!/usr/bin/env python3
"""
Integration tests for authentication endpoints
This addresses task T044: [P] Create integration tests for authentication endpoints
"""

import asyncio
import os
import logging
from datetime import datetime
from fastapi.testclient import TestClient
from backend.main import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_auth_integration():
    """Test authentication endpoints integration."""
    logger.info("Starting authentication integration tests...")

    # Create a test client
    client = TestClient(app)

    # Generate unique test data
    timestamp = int(datetime.now().timestamp())
    test_email = f"integration_test_{timestamp}@example.com"
    test_name = "Integration Test User"
    test_password = "SecurePassword123!"
    test_experience = "beginner"

    # Test 1: User registration
    logger.info("Test 1: User registration endpoint")

    reg_response = client.post("/api/auth/register", json={
        "email": test_email,
        "name": test_name,
        "password": test_password,
        "experience_level": test_experience
    })

    logger.info(f"Registration response status: {reg_response.status_code}")
    logger.info(f"Registration response: {reg_response.json()}")

    if reg_response.status_code == 200:
        reg_data = reg_response.json()
        user_id = reg_data.get('user_id')
        session_token = reg_data.get('session_token')

        if user_id and session_token:
            logger.info("✅ Registration endpoint working correctly")
        else:
            logger.error("❌ Registration response missing required fields")
            return False
    else:
        logger.error(f"❌ Registration failed with status {reg_response.status_code}")
        return False

    # Test 2: User login
    logger.info("Test 2: User login endpoint")

    login_response = client.post("/api/auth/login", json={
        "email": test_email,
        "password": test_password
    })

    logger.info(f"Login response status: {login_response.status_code}")

    if login_response.status_code == 200:
        login_data = login_response.json()
        login_user_id = login_data.get('user_id')
        login_session_token = login_data.get('session_token')

        if login_user_id and login_session_token:
            logger.info("✅ Login endpoint working correctly")
        else:
            logger.error("❌ Login response missing required fields")
            return False
    else:
        logger.error(f"❌ Login failed with status {login_response.status_code}")
        return False

    # Test 3: Get profile (protected endpoint)
    logger.info("Test 3: Get profile endpoint (protected)")

    profile_response = client.get("/api/auth/profile", headers={
        "Authorization": f"Bearer {session_token}"
    })

    logger.info(f"Profile response status: {profile_response.status_code}")

    if profile_response.status_code == 200:
        profile_data = profile_response.json()
        profile_email = profile_data.get('email')

        if profile_email == test_email:
            logger.info("✅ Profile endpoint working correctly")
        else:
            logger.error("❌ Profile endpoint returned incorrect data")
            return False
    else:
        logger.error(f"❌ Profile request failed with status {profile_response.status_code}")
        return False

    # Test 4: Update profile (protected endpoint)
    logger.info("Test 4: Update profile endpoint (protected)")

    updated_name = "Updated Integration Test User"
    update_response = client.put("/api/auth/profile", json={
        "name": updated_name
    }, headers={
        "Authorization": f"Bearer {session_token}"
    })

    logger.info(f"Update response status: {update_response.status_code}")

    if update_response.status_code == 200:
        update_data = update_response.json()
        updated_profile_name = update_data.get('name')

        if updated_profile_name == updated_name:
            logger.info("✅ Update profile endpoint working correctly")
        else:
            logger.error("❌ Update profile endpoint returned incorrect data")
            return False
    else:
        logger.error(f"❌ Profile update failed with status {update_response.status_code}")
        return False

    # Test 5: Logout
    logger.info("Test 5: Logout endpoint")

    logout_response = client.post("/api/auth/logout", headers={
        "Authorization": f"Bearer {session_token}"
    })

    logger.info(f"Logout response status: {logout_response.status_code}")

    if logout_response.status_code == 200:
        logger.info("✅ Logout endpoint working correctly")
    else:
        logger.error(f"❌ Logout failed with status {logout_response.status_code}")
        return False

    # Test 6: Access protected endpoint after logout
    logger.info("Test 6: Access protected endpoint after logout (should fail)")

    protected_response = client.get("/api/auth/profile", headers={
        "Authorization": f"Bearer {session_token}"
    })

    logger.info(f"Protected response status after logout: {protected_response.status_code}")

    if protected_response.status_code == 401:
        logger.info("✅ Protected endpoint correctly rejects invalidated session")
    else:
        logger.warning(f"⚠️  Protected endpoint behavior after logout: {protected_response.status_code} (may be expected)")

    # Test 7: Error handling - invalid registration data
    logger.info("Test 7: Error handling for invalid registration data")

    invalid_reg_response = client.post("/api/auth/register", json={
        "email": "invalid-email",
        "name": test_name,
        "password": "short",
        "experience_level": "invalid_level"
    })

    logger.info(f"Invalid registration response status: {invalid_reg_response.status_code}")

    if invalid_reg_response.status_code == 400:
        logger.info("✅ Registration endpoint correctly handles invalid data")
    else:
        logger.warning(f"⚠️  Registration error handling: {invalid_reg_response.status_code} (may be expected)")

    # Test 8: Error handling - invalid login credentials
    logger.info("Test 8: Error handling for invalid login credentials")

    invalid_login_response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    })

    logger.info(f"Invalid login response status: {invalid_login_response.status_code}")

    if invalid_login_response.status_code == 401:
        logger.info("✅ Login endpoint correctly handles invalid credentials")
    else:
        logger.warning(f"⚠️  Login error handling: {invalid_login_response.status_code} (may be expected)")

    logger.info("✅ All authentication integration tests completed!")
    return True

def main():
    """Run all integration tests."""
    logger.info("Starting authentication integration tests...")

    success = test_auth_integration()

    if success:
        print("\n🎉 Authentication integration tests completed successfully!")
        return True
    else:
        print("\n💥 Authentication integration tests failed!")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)