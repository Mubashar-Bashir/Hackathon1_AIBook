from fastapi.testclient import TestClient
from main import app
from src.services.rag_service import rag_service

# Remove middleware for testing
app.user_middleware = []
app.middleware_stack = app.build_middleware_stack()

def test_simple():
    client = TestClient(app)
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    if response.content:
        print(f"Response: {response.json()}")
    else:
        print("Empty response body")

def test_streaming():
    """Test the streaming functionality directly"""
    print("\nTesting RAG streaming functionality...")

    query = "What is Physical AI?"
    print(f"Query: {query}")
    print("Streaming response:")
    print("-" * 40)

    try:
        # Test the streaming function
        stream_gen = rag_service.stream_query_response(query)

        for i, chunk in enumerate(stream_gen):
            print(f"Chunk {i+1}: {chunk}")
            if chunk.get('done', False):
                print("Stream completed!")
                break

        print("-" * 40)
        print("Streaming test completed successfully!")

    except Exception as e:
        print(f"Error during streaming test: {e}")
        import traceback
        traceback.print_exc()

def test_streaming_endpoint():
    """Test the streaming endpoint via TestClient"""
    print("\nTesting streaming endpoint...")

    client = TestClient(app)

    # Test data for streaming endpoint
    test_data = {
        "query": "What is Physical AI?",
        "context_type": "full_book",
        "selected_text": None
    }

    try:
        response = client.post("/api/chatbot/stream-query", json=test_data)
        print(f"Streaming endpoint status: {response.status_code}")
        print(f"Response type: {type(response.content)}")
        print(f"Response length: {len(response.content)}")

        # For SSE responses, we might need to handle differently
        if response.content:
            content_str = response.content.decode('utf-8')
            print(f"Response preview: {content_str[:200]}...")

    except Exception as e:
        print(f"Error testing streaming endpoint: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
    test_streaming()
    test_streaming_endpoint()