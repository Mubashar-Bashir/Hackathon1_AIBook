#!/usr/bin/env python3
"""
Test script specifically for the streaming functionality
"""
from fastapi.testclient import TestClient
from main import app

# Remove middleware for testing
app.user_middleware = []
app.middleware_stack = app.build_middleware_stack()

def test_streaming_endpoint():
    """Test the streaming endpoint specifically"""
    client = TestClient(app)

    # Test data that matches the API contract (ChatbotQueryRequest model)
    test_data = {
        "query": "What is Physical AI?",
        "context_type": "full_book",
        "selected_text": None,
        "user_id": None
    }

    print("Testing streaming endpoint with correct field names...")
    response = client.post("/api/chatbot/stream-query", json=test_data)

    print(f"Status: {response.status_code}")
    print(f"Content type: {response.headers.get('content-type')}")
    print(f"Response length: {len(response.content)}")

    if response.status_code == 200:
        content_str = response.content.decode('utf-8')
        print(f"Response content: {content_str[:500]}...")
        print("✅ Streaming endpoint test passed!")
        return True
    else:
        print(f"❌ Streaming endpoint test failed with status {response.status_code}")
        print(f"Response: {response.text}")
        return False

def test_regular_endpoint():
    """Test the regular endpoint to see if there are any issues"""
    client = TestClient(app)

    # Test data with correct field names according to ChatbotQueryRequest
    test_data = {
        "query": "What is Physical AI?",
        "context_type": "full_book",
        "selected_text": None,
        "user_id": None
    }

    print("\nTesting regular endpoint with correct field names...")
    response = client.post("/api/chatbot/query", json=test_data)

    print(f"Status: {response.status_code}")
    if response.content:
        print(f"Response: {response.text[:200]}...")

    if response.status_code == 200:
        print("✅ Regular endpoint test passed!")
        return True
    else:
        print(f"❌ Regular endpoint test failed with status {response.status_code}")
        return False

if __name__ == "__main__":
    print("Testing RAG streaming functionality...\n")

    streaming_success = test_streaming_endpoint()
    regular_success = test_regular_endpoint()

    print(f"\nResults:")
    print(f"Streaming endpoint: {'✅ PASS' if streaming_success else '❌ FAIL'}")
    print(f"Regular endpoint: {'✅ PASS' if regular_success else '❌ FAIL'}")

    if streaming_success:
        print("\n🎉 Streaming functionality is working correctly!")
    else:
        print("\n❌ Streaming functionality needs fixes")