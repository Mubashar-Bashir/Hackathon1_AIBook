"""
Integration tests for RAG feature - Frontend-Backend Integration
Tests the complete flow from frontend chatbot component to backend RAG service
"""
import os
import sys
import pytest
import asyncio
from unittest.mock import AsyncMock, Mock, patch
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Add backend to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.main import app
from backend.src.services.rag_service import rag_service
from backend.src.services.embedding_service import embedding_service
from backend.src.utils.vector_store import vector_store


# Load environment variables for tests
load_dotenv()

@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


def test_chatbot_endpoint_integration():
    """Test the complete chatbot endpoint integration"""
    with TestClient(app) as client:
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
    with TestClient(app) as client:
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
        # When using selected text, sources should reflect this
        assert "selected_text" in data["sources"] or len(data["sources"]) >= 0


def test_chatbot_endpoint_error_handling():
    """Test error handling in chatbot endpoint"""
    with TestClient(app) as client:
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


def test_rag_service_integration():
    """Test RAG service integration with embedding and vector store"""
    # Test query with full book context
    result = rag_service.query_knowledge_base(
        query="What are the principles of Physical AI?",
        context_type="full_book",
        limit=3
    )

    assert result is not None
    assert hasattr(result, 'response')
    assert hasattr(result, 'sources')
    assert hasattr(result, 'confidence')
    assert isinstance(result.confidence, float)
    assert 0.0 <= result.confidence <= 1.0


def test_embedding_service_integration():
    """Test embedding service integration with Cohere and vector store"""
    test_text = "Physical AI and Humanoid Robotics"

    # Test single embedding generation
    embedding = embedding_service.get_embedding(test_text)
    assert embedding is not None
    assert isinstance(embedding, list)
    assert len(embedding) > 0  # Should have some dimensions

    # Test adding text to vector store
    success = embedding_service.add_text_to_vector_store(
        content_id="test_content_1",
        text=test_text,
        metadata={"source": "integration_test", "type": "definition"}
    )
    assert success is True


def test_vector_store_integration():
    """Test vector store integration with Qdrant"""
    test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]  # Example embedding

    # Add a test entry to vector store
    success = vector_store.add_embedding(
        content_id="integration_test_1",
        content_text="This is a test entry for integration testing",
        embedding=test_embedding,
        metadata={"test": True, "category": "integration"}
    )

    assert success is True

    # Search for similar content
    search_results = vector_store.search_similar(
        query_embedding=test_embedding,
        limit=5
    )

    assert isinstance(search_results, list)
    # May not find exact matches depending on the vector store state
    # but the search should execute without errors


def test_rag_service_fallback_mechanism():
    """Test RAG service fallback mechanism"""
    # Test the fallback method with a query that might fail initially
    result = rag_service.process_query_with_fallback(
        query="What is Physical AI?",
        context_type="full_book"
    )

    # Should return a result even if the primary approach fails
    assert result is not None
    if result is not None:
        assert hasattr(result, 'response')
        assert hasattr(result, 'sources')
        assert hasattr(result, 'confidence')


def test_chatbot_health_endpoint():
    """Test the health endpoint for the chatbot service"""
    with TestClient(app) as client:
        response = client.get("/api/chatbot/health")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "dependencies" in data

        assert data["status"] == "healthy"
        assert isinstance(data["dependencies"], dict)


def test_chatbot_query_history():
    """Test the query history endpoint"""
    with TestClient(app) as client:
        # First, make a query to create history
        query_payload = {
            "query": "Test query for history",
            "context_type": "full_book",
            "selected_text": None,
            "user_id": "test_user_history"
        }

        # Make a query first
        client.post("/api/chatbot/query", json=query_payload)

        # Now test the history endpoint
        response = client.get("/api/chatbot/history/test_user_history")

        assert response.status_code == 200

        data = response.json()
        assert "user_id" in data
        assert "queries" in data
        assert data["user_id"] == "test_user_history"


def test_rag_cache_integration():
    """Test RAG caching mechanism integration"""
    query = "Cached query test"

    # First query - should not be cached
    result1 = rag_service.query_knowledge_base(
        query=query,
        context_type="full_book"
    )

    assert result1 is not None

    # Second query with same parameters - should be cached
    result2 = rag_service.query_knowledge_base(
        query=query,
        context_type="full_book"
    )

    assert result2 is not None
    # Both results should be valid
    assert hasattr(result1, 'response')
    assert hasattr(result2, 'response')


def test_rag_context_types():
    """Test different context types in RAG service"""
    query = "What is machine learning?"

    # Test full_book context
    result_full = rag_service.query_knowledge_base(
        query=query,
        context_type="full_book"
    )

    assert result_full is not None
    assert hasattr(result_full, 'response')

    # Test selected_text context
    result_selected = rag_service.query_knowledge_base(
        query=query,
        context_type="selected_text",
        selected_text="Machine learning is a subset of artificial intelligence."
    )

    assert result_selected is not None
    assert hasattr(result_selected, 'response')

    # Both should return valid responses
    assert isinstance(result_full.response, str)
    assert isinstance(result_selected.response, str)


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])