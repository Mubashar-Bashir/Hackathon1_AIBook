import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from src.services.rag_service import RAGService
from src.models.chatbot import ChatbotQueryResponse
from datetime import datetime


class TestRAGService:
    """Test cases for the RAG service functionality."""

    @pytest.fixture
    def rag_service(self):
        """Create a RAG service instance for testing."""
        with patch('src.services.rag_service.genai.configure'), \
             patch('src.services.rag_service.genai.GenerativeModel') as mock_model:

            # Mock the model instance
            mock_model_instance = MagicMock()
            mock_model_instance.generate_content.return_value = MagicMock(text="Test response")
            mock_model.return_value = mock_model_instance

            service = RAGService()
            service.model = mock_model_instance
            return service

    @pytest.mark.asyncio
    async def test_query_knowledge_base_full_book_context(self, rag_service):
        """Test querying the knowledge base with full book context."""
        with patch.object(rag_service, '_generate_response', return_value="Test response"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
             patch('src.services.rag_service.embedding_service') as mock_embedding_service:

            # Mock the search results - using embedding_service, not content_service
            mock_embedding_service.search_similar_content.return_value = [
                {
                    "content_id": "test_content_1",
                    "content_text": "This is test content for the textbook.",
                    "metadata": {},
                    "score": 0.9
                }
            ]

            result = rag_service.query_knowledge_base(
                query="What is Physical AI?",
                context_type="full_book"
            )

            assert result is not None
            assert "Test response" in result.response
            assert len(result.sources) > 0
            assert result.confidence == 0.8

    @pytest.mark.asyncio
    async def test_query_knowledge_base_selected_text_context(self, rag_service):
        """Test querying the knowledge base with selected text context."""
        with patch.object(rag_service, '_generate_response', return_value="Test response"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.85):

            result = rag_service.query_knowledge_base(
                query="What does this selected text mean?",
                context_type="selected_text",
                selected_text="This is the selected text for context."
            )

            assert result is not None
            assert "Test response" in result.response
            assert result.confidence == 0.85

    @pytest.mark.asyncio
    async def test_query_knowledge_base_no_context(self, rag_service):
        """Test querying when no relevant context is found."""
        with patch.object(rag_service, '_generate_response', return_value="No context response"), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            # Mock empty search results
            mock_content_service.search_similar_content.return_value = []

            result = rag_service.query_knowledge_base(
                query="Unknown question",
                context_type="full_book"
            )

            assert result is not None
            assert "No context response" in result.response

    @pytest.mark.asyncio
    async def test_process_query_with_enhanced_reasoning(self, rag_service):
        """Test processing a query with enhanced reasoning."""
        with patch.object(rag_service, 'query_with_function_calling', return_value=ChatbotQueryResponse(
            id="test_id",
            query="Test query",
            response="Enhanced response",
            sources=["source1"],
            confidence=0.9,
            timestamp=datetime.utcnow()
        )):
            result = rag_service.process_query_with_enhanced_reasoning(
                query="Test enhanced reasoning query"
            )

            assert result is not None
            assert result.response == "Enhanced response"
            assert result.confidence == 0.9

    @pytest.mark.asyncio
    async def test_cache_functionality(self, rag_service):
        """Test that caching works correctly."""
        with patch.object(rag_service, '_generate_response', return_value="Cached response"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.75), \
             patch('src.services.rag_service.embedding_service') as mock_embedding_service, \
             patch('src.services.rag_service.cache_service') as mock_cache:

            # Mock search results - using embedding_service, not content_service
            mock_embedding_service.search_similar_content.return_value = [
                {
                    "content_id": "test_content_1",
                    "content_text": "This is test content for caching.",
                    "metadata": {},
                    "score": 0.85
                }
            ]

            # Mock cache to return None initially (not cached)
            mock_cache.get.return_value = None

            # First call - should not be cached
            result1 = rag_service.query_knowledge_base(
                query="Cache test query",
                context_type="full_book"
            )

            # Second call - should be cached
            cached_result = {"query": "Cache test query", "response": "Cached response", "sources": ["test"], "confidence": 0.75, "timestamp": datetime.utcnow()}
            mock_cache.get.return_value = cached_result

            result2 = rag_service.query_knowledge_base(
                query="Cache test query",
                context_type="full_book"
            )

            # Verify cache was called
            assert mock_cache.get.call_count >= 1
            assert result1 is not None

    @pytest.mark.asyncio
    async def test_fallback_mechanism(self, rag_service):
        """Test that fallback mechanism works when primary approach fails."""
        with patch.object(rag_service, 'query_knowledge_base', side_effect=[None, ChatbotQueryResponse(
            id="fallback_id",
            query="Fallback query",
            response="Fallback response",
            sources=[],
            confidence=0.5,
            timestamp=datetime.utcnow()
        )]):
            result = rag_service.process_query_with_fallback(
                query="Fallback test query"
            )

            assert result is not None
            assert "Fallback response" in result.response

    def test_calculate_confidence(self, rag_service):
        """Test confidence calculation."""
        response = "This is a response that addresses the query appropriately."
        query = "What is this?"

        confidence = rag_service._calculate_confidence(response, query)

        # Confidence should be between 0 and 1
        assert 0.0 <= confidence <= 1.0

    def test_calculate_confidence_low_for_error_responses(self, rag_service):
        """Test that error responses get low confidence."""
        error_response = "I couldn't find any relevant information in the textbook to answer this question."
        query = "What is this?"

        confidence = rag_service._calculate_confidence(error_response, query)

        # Error responses should have low confidence
        assert confidence < 0.2


if __name__ == "__main__":
    pytest.main([__file__])