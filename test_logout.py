"""
Test script to verify logout functionality
"""
import asyncio
import requests
import json

BASE_URL = "http://localhost:8000"  # Adjust to your server URL

def test_logout_functionality():
    print("Testing logout functionality...")

    # Register a test user
    print("1. Registering a test user...")
    register_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123",
        "background": "beginner"
    }

    try:
        register_response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"Registration response: {register_response.status_code}")
        if register_response.status_code == 200:
            register_data = register_response.json()
            token = register_data['session_token']
            user_id = register_data['user_id']
            print(f"User registered successfully. Token: {token[:10]}...")
        else:
            print(f"Registration failed: {register_response.text}")
            return False
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

    # Try to access a protected endpoint (get profile)
    print("\n2. Testing access to protected endpoint...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        profile_response = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        print(f"Profile access response: {profile_response.status_code}")
        if profile_response.status_code == 200:
            print("Successfully accessed profile with valid token")
        else:
            print(f"Failed to access profile: {profile_response.text}")
            return False
    except Exception as e:
        print(f"Error accessing profile: {e}")
        return False

    # Perform logout
    print("\n3. Performing logout...")
    try:
        logout_response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print(f"Logout response: {logout_response.status_code}")
        if logout_response.status_code == 200:
            print("Successfully logged out")
        else:
            print(f"Logout failed: {logout_response.text}")
            return False
    except Exception as e:
        print(f"Error during logout: {e}")
        return False

    # Try to access the protected endpoint again - should fail now
    print("\n4. Testing access to protected endpoint after logout...")
    try:
        profile_response_after_logout = requests.get(f"{BASE_URL}/api/auth/profile", headers=headers)
        print(f"Profile access after logout response: {profile_response_after_logout.status_code}")
        if profile_response_after_logout.status_code == 401:
            print("Successfully blocked access after logout (token invalidated)")
            print("Logout functionality is working correctly!")
            return True
        else:
            print(f"Unexpected response after logout: {profile_response_after_logout.text}")
            return False
    except Exception as e:
        print(f"Error testing access after logout: {e}")
        return False

if __name__ == "__main__":
    print("Starting logout functionality test...")
    success = test_logout_functionality()
    if success:
        print("\n✅ All tests passed! Logout functionality is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")