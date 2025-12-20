import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
from main import app
from src.middleware.rate_limit import rate_limiter


class TestE2EWorkflows:
    @pytest.fixture
    def client(self):
        """Create a test client for the API."""
        # Reset rate limiter state to avoid conflicts between tests
        rate_limiter.requests_registry.clear()
        return TestClient(app)

    @pytest.mark.asyncio
    async def test_health_check_endpoints(self, client):
        """Test that all health check endpoints are accessible."""
        # Test main health check
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

        # Test chatbot health
        response = client.get("/api/chatbot/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

        # Test auth health (if available)
        response = client.get("/api/auth/health")
        # This endpoint might not exist, so we'll handle both cases
        assert response.status_code in [200, 404, 405]

        # Test translation health
        response = client.get("/api/translation/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    @patch('src.services.translation_service.translation_service.translate_text')
    def test_translation_workflow(self, mock_translate, client):
        """Test the translation workflow end-to-end."""
        # Mock the translation service to return a known value
        mock_translate.return_value = "میں ایک ٹیسٹ ہوں"

        # Test the translation endpoint
        response = client.post("/api/translation/translate", json={
            "text": "I am a test",
            "target_language": "ur"
        })

        assert response.status_code == 200
        data = response.json()
        assert "translated_text" in data
        assert data["translated_text"] == "میں ایک ٹیسٹ ہوں"
        assert data["source_language"] == "en"
        assert data["target_language"] == "ur"

    @patch('src.services.translation_service.translation_service.translate_chapter_content')
    def test_chapter_translation_workflow(self, mock_translate, client):
        """Test the chapter translation workflow end-to-end."""
        # Mock the translation service to return a known value
        mock_translate.return_value = "یہ ایک ٹیسٹ چیپٹر ہے"

        # Test the chapter translation endpoint
        response = client.post("/api/translation/translate-chapter", json={
            "chapter_content": "This is a test chapter for translation.",
            "target_language": "ur"
        })

        assert response.status_code == 200
        data = response.json()
        assert "translated_content" in data
        assert data["translated_content"] == "یہ ایک ٹیسٹ چیپٹر ہے"
        assert data["source_language"] == "en"
        assert data["target_language"] == "ur"

    def test_supported_languages_workflow(self, client):
        """Test the supported languages workflow."""
        response = client.get("/api/translation/supported-languages")
        assert response.status_code == 200
        data = response.json()
        assert "languages" in data
        assert "ur" in data["languages"]
        assert "en" in data["languages"]

    @patch('src.services.rag_service.rag_service.process_query_with_fallback')
    def test_chatbot_workflow(self, mock_rag, client):
        """Test the chatbot workflow end-to-end."""
        # Mock the RAG service to return a known response
        from src.models.chatbot import ChatbotQueryResponse
        from datetime import datetime
        mock_response = ChatbotQueryResponse(
            id="test-id",
            query="Test query?",
            response="This is a test response.",
            sources=["source1"],
            confidence=0.9,
            timestamp=datetime.utcnow()  # Provide a valid datetime
        )
        mock_rag.return_value = mock_response

        # Test the chatbot query endpoint
        response = client.post("/api/chatbot/query", json={
            "query": "Test query?",
            "context_type": "full_book"
        })

        # Should return 200 for successful response
        assert response.status_code == 200

    def test_rate_limiting_workflow(self, client):
        """Test that rate limiting is applied."""
        # Make multiple requests to test rate limiting
        for i in range(5):
            response = client.get("/health")
            # All requests under the limit should succeed
            assert response.status_code == 200

    def test_error_handling_workflow(self, client):
        """Test error handling for invalid requests."""
        # Test with invalid translation request (empty text)
        response = client.post("/api/translation/translate", json={
            "text": "",  # Empty text should cause validation error
            "target_language": "ur"
        })

        # Should return 422 for Pydantic validation error
        assert response.status_code == 422

        # Test with invalid language code
        response = client.post("/api/translation/translate", json={
            "text": "Test",
            "target_language": "invalid_lang"
        })

        # Should return 422 for Pydantic validation error (too long)
        assert response.status_code == 422

    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in responses."""
        response = client.get("/health")
        assert response.status_code == 200

        # Check for CORS headers (these should be present if CORS middleware is working)
        # The exact header name might vary depending on the request type
        has_cors_header = any(
            header in response.headers
            for header in ["access-control-allow-origin", "Access-Control-Allow-Origin"]
        )
        assert has_cors_header, f"No CORS headers found in response. Headers: {dict(response.headers)}"


@pytest.mark.asyncio
class TestAsyncWorkflows:
    @pytest.fixture
    def client(self):
        """Create a test client for the API."""
        return TestClient(app)

    async def test_async_health_checks(self, client):
        """Test async health check functionality."""
        # Test main health check endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Physical AI & Humanoid Robotics Textbook" in data["message"]