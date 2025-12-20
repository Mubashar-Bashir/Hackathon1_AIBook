"""
Integration tests for RAG feature - Frontend-Backend Integration
Tests the complete flow from frontend chatbot component to backend RAG service
These tests mock external dependencies to avoid requiring actual API keys
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Mock external dependencies before importing the app
def create_mock_modules():
    """Create mock modules to prevent actual initialization"""
    modules_to_mock = [
        'qdrant_client',
        'qdrant_client.http',
        'qdrant_client.http.models',
        'qdrant_client.models',
        'cohere',
        'google.generativeai',
        'google.generativeai.types',
        'backend.src.utils.vector_store',
        'backend.src.services.embedding_service',
        'backend.src.services.rag_service',
        'backend.src.services.cache_service'
    ]

    for module_name in modules_to_mock:
        sys.modules[module_name] = Mock()

# Create mocks before importing
create_mock_modules()

# Now import the app with mocked dependencies
from backend.main import app


def test_chatbot_endpoint_integration():
    """Test the complete chatbot endpoint integration with mocked dependencies"""
    # Mock the external services and startup event
    with patch('backend.main.qdrant_client') as mock_qdrant, \
         patch('backend.main.co') as mock_cohere, \
         patch('backend.main.gemini_model') as mock_genai_model, \
         patch('backend.main.startup_event'):

        # Setup mocks
        mock_qdrant.recreate_collection.return_value = None
        mock_qdrant.get_collection.side_effect = Exception("Collection doesn't exist")
        mock_qdrant.create_collection.return_value = None
        mock_qdrant.upsert.return_value = None
        mock_qdrant.search.return_value = []

        # Mock Cohere embedding response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_cohere.embed.return_value = mock_embed_response

        # Mock Gemini response
        mock_genai_response = Mock()
        mock_genai_response.text = "This is a test response from the AI model."
        mock_genai_model.generate_content.return_value = mock_genai_response

        client = TestClient(app)

        # Test data for the RAG query
        payload = {
            "query": "What is Physical AI?",
            "context_type": "full_book",
            "selected_text": None,
            "user_id": "test_user_123"
        }

        response = client.post("/api/chatbot/query", json=payload)

        # Verify response structure and status
        assert response.status_code == 200

        data = response.json()
        assert "id" in data
        assert "query" in data
        assert "response" in data
        assert "sources" in data
        assert "confidence" in data
        assert "timestamp" in data

        # Verify query was correctly processed
        assert data["query"] == "What is Physical AI?"
        assert isinstance(data["response"], str)
        assert isinstance(data["sources"], list)
        assert isinstance(data["confidence"], float)
        assert 0.0 <= data["confidence"] <= 1.0


def test_chatbot_endpoint_with_selected_text():
    """Test chatbot endpoint with selected text context"""
    # Mock the external services and startup event
    with patch('backend.main.qdrant_client') as mock_qdrant, \
         patch('backend.main.co') as mock_cohere, \
         patch('backend.main.gemini_model') as mock_genai_model, \
         patch('backend.main.startup_event'):

        # Setup mocks
        mock_qdrant.recreate_collection.return_value = None
        mock_qdrant.get_collection.side_effect = Exception("Collection doesn't exist")
        mock_qdrant.create_collection.return_value = None
        mock_qdrant.upsert.return_value = None
        mock_qdrant.search.return_value = []

        # Mock Cohere embedding response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_cohere.embed.return_value = mock_embed_response

        # Mock Gemini response
        mock_genai_response = Mock()
        mock_genai_response.text = "This is a response based on the selected text."
        mock_genai_model.generate_content.return_value = mock_genai_response

        client = TestClient(app)

        payload = {
            "query": "Explain this concept",
            "context_type": "selected_text",
            "selected_text": "Physical AI combines principles of physics with artificial intelligence to create systems that interact with the physical world.",
            "user_id": "test_user_123"
        }

        response = client.post("/api/chatbot/query", json=payload)

        assert response.status_code == 200

        data = response.json()
        assert data["query"] == "Explain this concept"
        assert isinstance(data["response"], str)


def test_chatbot_endpoint_error_handling():
    """Test error handling in chatbot endpoint"""
    # Mock the external services and startup event
    with patch('backend.main.qdrant_client') as mock_qdrant, \
         patch('backend.main.co') as mock_cohere, \
         patch('backend.main.gemini_model') as mock_genai_model, \
         patch('backend.main.startup_event'):

        # Setup mocks
        mock_qdrant.recreate_collection.return_value = None
        mock_qdrant.get_collection.side_effect = Exception("Collection doesn't exist")
        mock_qdrant.create_collection.return_value = None
        mock_qdrant.upsert.return_value = None
        mock_qdrant.search.return_value = []

        # Mock Cohere embedding response
        mock_embed_response = Mock()
        mock_embed_response.embeddings = [[0.1, 0.2, 0.3]]
        mock_cohere.embed.return_value = mock_embed_response

        # Mock Gemini response
        mock_genai_response = Mock()
        mock_genai_response.text = "Test response"
        mock_genai_model.generate_content.return_value = mock_genai_response

        client = TestClient(app)

        # Test with empty query
        payload = {
            "query": "",
            "context_type": "full_book",
            "selected_text": None
        }

        response = client.post("/api/chatbot/query", json=payload)
        assert response.status_code == 400

        # Test with invalid context type
        payload = {
            "query": "Test query",
            "context_type": "invalid_context",
            "selected_text": None
        }

        response = client.post("/api/chatbot/query", json=payload)
        assert response.status_code == 400


def test_chatbot_health_endpoint():
    """Test the health endpoint for the chatbot service"""
    # Mock the external services for startup
    with patch('backend.main.qdrant_client') as mock_qdrant, \
         patch('backend.main.startup_event'):

        mock_qdrant.recreate_collection.return_value = None
        mock_qdrant.get_collection.side_effect = Exception("Collection doesn't exist")
        mock_qdrant.create_collection.return_value = None

        client = TestClient(app)
        response = client.get("/api/chatbot/health")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "dependencies" in data

        assert data["status"] == "healthy"
        assert isinstance(data["dependencies"], dict)


def test_main_health_endpoint():
    """Test the main health endpoint"""
    # Mock the external services for startup
    with patch('backend.main.qdrant_client') as mock_qdrant, \
         patch('backend.main.startup_event'):

        mock_qdrant.recreate_collection.return_value = None
        mock_qdrant.get_collection.side_effect = Exception("Collection doesn't exist")
        mock_qdrant.create_collection.return_value = None

        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert data["service"] == "textbook-backend"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])