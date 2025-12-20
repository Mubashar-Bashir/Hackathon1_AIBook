import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
from src.api.chatbot import router
from main import app  # main.py contains the FastAPI app
from src.models.chatbot import ChatbotQueryResponse
from datetime import datetime
import json


# Create a test-specific app instance that has middleware reset
from src.middleware.rate_limit import rate_limiter

# Reset rate limiter for tests to avoid conflicts
rate_limiter.requests_registry.clear()


class TestChatbotAPI:
    """Test cases for the chatbot API endpoints."""

    @pytest.fixture
    def client(self):
        """Create a test client for the API."""
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_query_chatbot_success(self, client):
        """Test successful chatbot query."""
        # Mock the RAG service
        with patch('src.api.chatbot.rag_service') as mock_rag_service:
            # Create a mock response
            mock_response = ChatbotQueryResponse(
                id="test_response_id",
                query="Test query",
                response="This is a test response",
                sources=["source1", "source2"],
                confidence=0.85,
                timestamp=datetime.utcnow()
            )

            mock_rag_service.process_query_with_enhanced_reasoning.return_value = mock_response

            response = client.post(
                "/api/chatbot/query",
                json={
                    "query": "What is Physical AI?",
                    "context_type": "full_book"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["response"] == "This is a test response"
            assert data["confidence"] == 0.85
            assert len(data["sources"]) == 2

    @pytest.mark.asyncio
    async def test_query_chatbot_with_selected_text(self, client):
        """Test chatbot query with selected text context."""
        with patch('src.api.chatbot.rag_service') as mock_rag_service:
            mock_response = ChatbotQueryResponse(
                id="test_response_id",
                query="Test query about selection",
                response="Response based on selected text",
                sources=["selected_text_source"],
                confidence=0.9,
                timestamp=datetime.utcnow()
            )

            mock_rag_service.process_query_with_enhanced_reasoning.return_value = mock_response

            response = client.post(
                "/api/chatbot/query",
                json={
                    "query": "What does this selected text mean?",
                    "context_type": "selected_text",
                    "selected_text": "This is the selected text for context."
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "selected text" in data["response"]
            assert data["confidence"] == 0.9

    def test_query_chatbot_invalid_query(self, client):
        """Test chatbot query with invalid parameters."""
        response = client.post(
            "/api/chatbot/query",
            json={
                "query": "",  # Empty query
                "context_type": "full_book"
            }
        )

        # Pydantic validation returns 422 for empty query (min_length validation)
        assert response.status_code == 422
        # Check that the response contains validation error info
        response_data = response.json()
        # The error handler middleware changes the format
        assert "message" in response_data  # Error handler returns 'message' field

    def test_query_chatbot_invalid_context_type(self, client):
        """Test chatbot query with invalid context type."""
        response = client.post(
            "/api/chatbot/query",
            json={
                "query": "Test query",
                "context_type": "invalid_context"  # Invalid context type
            }
        )

        # Custom validation in the endpoint returns 400 for invalid context type
        assert response.status_code == 400
        # Check that the response contains validation error info
        response_data = response.json()
        # Error handler returns 'message' field
        assert "message" in response_data

    def test_query_chatbot_long_query(self, client):
        """Test chatbot query with a query that's too long."""
        long_query = "A" * 2001  # More than 2000 characters

        response = client.post(
            "/api/chatbot/query",
            json={
                "query": long_query,
                "context_type": "full_book"
            }
        )

        # Pydantic validation returns 422 for long query (max_length validation)
        assert response.status_code == 422
        # Check that the response contains validation error info
        response_data = response.json()
        # The error handler middleware changes the format
        assert "message" in response_data  # Error handler returns 'message' field

    def test_chatbot_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/chatbot/health")

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "dependencies" in data
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_query_chatbot_error_handling(self, client):
        """Test error handling in chatbot query."""
        with patch('src.api.chatbot.rag_service') as mock_rag_service:
            # Make the service return None to simulate an error
            mock_rag_service.process_query_with_enhanced_reasoning.return_value = None

            response = client.post(
                "/api/chatbot/query",
                json={
                    "query": "Test error query",
                    "context_type": "full_book"
                }
            )

            # Should return 500 for internal server errors
            assert response.status_code == 500
            response_data = response.json()
            # Error handler returns 'message' field for 500 errors
            assert "message" in response_data

    def test_query_history_endpoint(self, client):
        """Test the query history endpoint."""
        # Add a test user and query
        user_id = "test_user_123"

        response = client.get(f"/api/chatbot/history/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == user_id
        assert "queries" in data

    @pytest.mark.asyncio
    async def test_query_chatbot_with_user_id(self, client):
        """Test chatbot query with user ID for authenticated users."""
        with patch('src.api.chatbot.rag_service') as mock_rag_service:
            mock_response = ChatbotQueryResponse(
                id="test_response_id",
                query="Personalized query",
                response="Response for authenticated user",
                sources=["user_specific_source"],
                confidence=0.88,
                timestamp=datetime.utcnow()
            )

            mock_rag_service.process_query_with_enhanced_reasoning.return_value = mock_response

            response = client.post(
                "/api/chatbot/query",
                json={
                    "query": "What should I study next?",
                    "context_type": "full_book",
                    "user_id": "test_user_123"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "authenticated user" in data["response"]

    def test_invalid_json_request(self, client):
        """Test handling of invalid JSON requests."""
        response = client.post(
            "/api/chatbot/query",
            content="invalid json {",
            headers={"Content-Type": "application/json"}
        )

        # Should return 422 for validation error
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_edge_case_empty_sources(self, client):
        """Test response when no sources are found."""
        with patch('src.api.chatbot.rag_service') as mock_rag_service:
            mock_response = ChatbotQueryResponse(
                id="test_response_id",
                query="Query with no sources",
                response="Response with no sources found",
                sources=[],  # Empty sources
                confidence=0.1,  # Low confidence
                timestamp=datetime.utcnow()
            )

            mock_rag_service.process_query_with_enhanced_reasoning.return_value = mock_response

            response = client.post(
                "/api/chatbot/query",
                json={
                    "query": "Question with no answer in textbook",
                    "context_type": "full_book"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["sources"]) == 0
            assert data["confidence"] <= 0.2  # Should have low confidence


if __name__ == "__main__":
    pytest.main([__file__])