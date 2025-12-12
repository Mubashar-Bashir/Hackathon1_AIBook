"""Test script to debug session validation for protected endpoints."""

import asyncio
import os
import sys
import logging
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from datetime import datetime

# Add the backend directory to the path so we can import from src
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def test_session_validation_for_protected_endpoints():
    """Test session validation for protected endpoints."""
    logger.info("Starting session validation debug test for protected endpoints...")

    # Import after setup
    from main import app
    from src.services.auth_service import AuthService

    # Create a test client
    client = TestClient(app)

    # First, register a user to test with
    logger.info("Registering test user...")
    register_response = client.post("/api/auth/register", json={
        "email": "session_test@example.com",
        "name": "Session Test User",
        "password": "SecurePassword123!",
        "experience_level": "beginner"
    })

    if register_response.status_code != 200:
        logger.error(f"User registration failed: {register_response.status_code}, {register_response.text}")
        return False

    register_data = register_response.json()
    session_token = register_data["session_token"]
    user_id = register_data["user_id"]
    logger.info(f"User registered successfully. User ID: {user_id}")

    # Test accessing a protected endpoint with valid session token
    logger.info("Testing access to protected endpoint with valid session token...")
    profile_response = client.get("/api/auth/profile",
                                  headers={"Authorization": f"Bearer {session_token}"})

    if profile_response.status_code == 200:
        logger.info("Access to protected endpoint successful with valid token")
        profile_data = profile_response.json()
        logger.info(f"Retrieved profile: {profile_data['email']}")
    else:
        logger.error(f"Access to protected endpoint failed with valid token: {profile_response.status_code}, {profile_response.text}")
        return False

    # Test accessing a protected endpoint with invalid session token
    logger.info("Testing access to protected endpoint with invalid session token...")
    invalid_response = client.get("/api/auth/profile",
                                  headers={"Authorization": "Bearer invalid_token_1234567890"})

    if invalid_response.status_code == 401:
        logger.info("Correctly rejected invalid session token")
    else:
        logger.error(f"Should have rejected invalid session token: {invalid_response.status_code}, {invalid_response.text}")
        return False

    # Test accessing a protected endpoint without authorization header
    logger.info("Testing access to protected endpoint without authorization header...")
    no_auth_response = client.get("/api/auth/profile")

    if no_auth_response.status_code == 401:
        logger.info("Correctly rejected request without authorization header")
    else:
        logger.error(f"Should have rejected request without authorization header: {no_auth_response.status_code}, {no_auth_response.text}")
        return False

    # Test accessing a protected endpoint with malformed authorization header
    logger.info("Testing access to protected endpoint with malformed authorization header...")
    malformed_response = client.get("/api/auth/profile",
                                   headers={"Authorization": "InvalidFormatToken"})

    if malformed_response.status_code == 401:
        logger.info("Correctly rejected malformed authorization header")
    else:
        logger.error(f"Should have rejected malformed authorization header: {malformed_response.status_code}, {malformed_response.text}")
        return False

    # Test the /me endpoint (another protected endpoint)
    logger.info("Testing /me endpoint with valid session token...")
    me_response = client.get("/api/auth/me",
                             headers={"Authorization": f"Bearer {session_token}"})

    if me_response.status_code == 200:
        logger.info("Access to /me endpoint successful with valid token")
        me_data = me_response.json()
        logger.info(f"Retrieved /me data: {me_data['email']}")
    else:
        logger.error(f"Access to /me endpoint failed with valid token: {me_response.status_code}, {me_response.text}")
        return False

    logger.info("All session validation tests passed!")
    return True

async def main():
    """Main function to run session validation tests."""
    logger.info("Starting session validation debugging tests...")

    # Run the session validation test
    success = await test_session_validation_for_protected_endpoints()

    logger.info(f"Session validation test: {'PASS' if success else 'FAIL'}")

    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)