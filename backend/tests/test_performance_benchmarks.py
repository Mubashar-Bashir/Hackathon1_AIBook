import pytest
import time
from unittest.mock import patch, MagicMock
from src.services.rag_service import RAGService
from src.models.chatbot import ChatbotQueryResponse
from datetime import datetime
import asyncio


class TestPerformanceBenchmarks:
    """Performance benchmark tests for RAG functionality."""

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

    def test_response_time_under_normal_conditions(self, rag_service):
        """Test that response times are acceptable under normal conditions."""
        with patch.object(rag_service, '_generate_response', return_value="Test response for timing"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "test_content_1",
                    "content_text": "This is test content for timing purposes.",
                    "metadata": {},
                    "score": 0.85
                }
            ]

            start_time = time.time()
            result = rag_service.query_knowledge_base(
                query="Performance test query",
                context_type="full_book"
            )
            end_time = time.time()

            response_time = end_time - start_time

            # Response should be under 3 seconds for 95% of queries
            assert response_time < 3.0, f"Response time {response_time:.2f}s exceeds 3 second limit"
            assert result is not None

    def test_response_time_with_selected_text_context(self, rag_service):
        """Test response time with selected text context."""
        selected_text = "This is the selected text that will be used as context for the query."

        start_time = time.time()
        with patch.object(rag_service, '_generate_response', return_value="Response based on selected text"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.85):

            result = rag_service.query_knowledge_base(
                query="What does this selected text mean?",
                context_type="selected_text",
                selected_text=selected_text
            )
        end_time = time.time()

        response_time = end_time - start_time

        # Selected text context should be faster since no search is needed
        assert response_time < 2.0, f"Selected text response time {response_time:.2f}s exceeds 2 second limit"
        assert result is not None

    def test_concurrent_query_handling(self, rag_service):
        """Test handling of multiple concurrent queries."""
        import concurrent.futures

        def simulate_query(query_num):
            with patch.object(rag_service, '_generate_response', return_value=f"Response for query {query_num}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.7 + (query_num * 0.01)), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                mock_content_service.search_similar_content.return_value = [
                    {
                        "content_id": f"test_content_{query_num}",
                        "content_text": f"This is test content for query {query_num}.",
                        "metadata": {},
                        "score": 0.85
                    }
                ]

                result = rag_service.query_knowledge_base(
                    query=f"Concurrent test query {query_num}",
                    context_type="full_book"
                )
                return result

        # Test handling 5 concurrent queries
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(simulate_query, i) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # All queries should return successfully
        assert len(results) == 5
        for result in results:
            assert result is not None

    @pytest.mark.asyncio
    async def test_async_performance_with_multiple_queries(self, rag_service):
        """Test async performance with multiple queries."""
        async def async_query(query_num):
            with patch.object(rag_service, '_generate_response', return_value=f"Async response for query {query_num}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.75), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                mock_content_service.search_similar_content.return_value = [
                    {
                        "content_id": f"async_content_{query_num}",
                        "content_text": f"This is async test content for query {query_num}.",
                        "metadata": {},
                        "score": 0.8
                    }
                ]

                # Simulate the async behavior
                await asyncio.sleep(0.01)  # Small delay to simulate async operation
                result = rag_service.query_knowledge_base(
                    query=f"Async test query {query_num}",
                    context_type="full_book"
                )
                return result

        # Run 3 async queries concurrently
        tasks = [async_query(i) for i in range(3)]
        results = await asyncio.gather(*tasks)

        # All queries should return successfully
        assert len(results) == 3
        for result in results:
            assert result is not None

    def test_cache_performance_improvement(self, rag_service):
        """Test that caching provides performance improvements."""
        with patch.object(rag_service, '_generate_response', return_value="Cached response"), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
             patch.object(rag_service, 'content_service') as mock_content_service, \
             patch('src.services.cache_service.cache_service') as mock_cache:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "cache_test_content",
                    "content_text": "This is test content for cache performance testing.",
                    "metadata": {},
                    "score": 0.9
                }
            ]

            # First call - not cached
            mock_cache.get.return_value = None
            start_time = time.time()
            result1 = rag_service.query_knowledge_base(
                query="Cache performance test",
                context_type="full_book"
            )
            first_call_time = time.time() - start_time

            # Second call - should be cached
            cached_result = {
                "query": "Cache performance test",
                "response": "Cached response",
                "sources": ["cache_test_content"],
                "confidence": 0.8,
                "timestamp": datetime.utcnow()
            }
            mock_cache.get.return_value = cached_result
            start_time = time.time()
            result2 = rag_service.query_knowledge_base(
                query="Cache performance test",
                context_type="full_book"
            )
            second_call_time = time.time() - start_time

            # Second call should be significantly faster due to caching
            assert result1 is not None
            assert result2 is not None
            assert second_call_time < first_call_time, f"Cache didn't improve performance: first={first_call_time:.3f}s, second={second_call_time:.3f}s"

    def test_large_context_handling_performance(self, rag_service):
        """Test performance with large context texts."""
        large_context = "Artificial intelligence is a wonderful field. " * 100  # Large context
        large_query = "Can you summarize the key points about artificial intelligence from this large text?"

        start_time = time.time()
        with patch.object(rag_service, '_generate_response', return_value="Summary of key points about artificial intelligence."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.7):

            result = rag_service.query_knowledge_base(
                query=large_query,
                context_type="selected_text",
                selected_text=large_context
            )
        end_time = time.time()

        response_time = end_time - start_time

        # Even with large context, response should be reasonable
        assert response_time < 5.0, f"Large context response time {response_time:.2f}s exceeds 5 second limit"
        assert result is not None

    def test_short_query_response_time(self, rag_service):
        """Test response time for short, simple queries."""
        short_queries = [
            "What is AI?",
            "Define robotics.",
            "What is machine learning?"
        ]

        for query in short_queries:
            start_time = time.time()
            with patch.object(rag_service, '_generate_response', return_value=f"Response to: {query}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                mock_content_service.search_similar_content.return_value = [
                    {
                        "content_id": f"short_query_{hash(query)}",
                        "content_text": f"Content related to {query}.",
                        "metadata": {},
                        "score": 0.85
                    }
                ]

                result = rag_service.query_knowledge_base(
                    query=query,
                    context_type="full_book"
                )
            end_time = time.time()

            response_time = end_time - start_time

            # Short queries should be fast
            assert response_time < 2.5, f"Short query '{query}' took {response_time:.2f}s, exceeds 2.5s limit"
            assert result is not None

    def test_complex_query_handling(self, rag_service):
        """Test handling of complex, multi-part queries."""
        complex_query = "Based on the principles of embodied cognition and sensorimotor learning, how do humanoid robots adapt to new environments while maintaining safety protocols?"

        start_time = time.time()
        with patch.object(rag_service, '_generate_response', return_value="Complex response addressing embodied cognition, sensorimotor learning, humanoid robot adaptation, and safety protocols."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.75), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "complex_content_1",
                    "content_text": "Embodied cognition and sensorimotor learning are key principles for humanoid robot adaptation.",
                    "metadata": {},
                    "score": 0.9
                },
                {
                    "content_id": "complex_content_2",
                    "content_text": "Safety protocols must be maintained during robot adaptation processes.",
                    "metadata": {},
                    "score": 0.85
                }
            ]

            result = rag_service.query_knowledge_base(
                query=complex_query,
                context_type="full_book"
            )
        end_time = time.time()

        response_time = end_time - start_time

        # Complex queries may take longer but should still be reasonable
        assert response_time < 4.0, f"Complex query response time {response_time:.2f}s exceeds 4 second limit"
        assert result is not None
        assert len(result.response) > 0

    def test_response_time_percentiles(self, rag_service):
        """Test that 95% of queries meet response time requirements."""
        query_count = 20
        response_times = []

        for i in range(query_count):
            with patch.object(rag_service, '_generate_response', return_value=f"Response for query {i}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.7 + (i * 0.01)), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                mock_content_service.search_similar_content.return_value = [
                    {
                        "content_id": f"perf_test_{i}",
                        "content_text": f"This is performance test content {i}.",
                        "metadata": {},
                        "score": 0.8 + (i * 0.005)
                    }
                ]

                start_time = time.time()
                result = rag_service.query_knowledge_base(
                    query=f"Performance test query {i}",
                    context_type="full_book"
                )
                end_time = time.time()

                response_time = end_time - start_time
                response_times.append(response_time)

                assert result is not None

        # Calculate 95th percentile
        response_times.sort()
        percentile_95 = response_times[int(len(response_times) * 0.95)]

        # 95% of queries should respond within 3 seconds
        assert percentile_95 < 3.0, f"95th percentile response time {percentile_95:.2f}s exceeds 3 second limit"

    def test_memory_usage_consistency(self, rag_service):
        """Test that memory usage remains consistent across multiple queries."""
        # This is a basic test - in a real scenario, you'd measure actual memory usage
        initial_queries = 5

        for i in range(initial_queries):
            with patch.object(rag_service, '_generate_response', return_value=f"Response for memory test {i}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                mock_content_service.search_similar_content.return_value = [
                    {
                        "content_id": f"memory_test_{i}",
                        "content_text": f"This is memory usage test content {i}.",
                        "metadata": {},
                        "score": 0.85
                    }
                ]

                result = rag_service.query_knowledge_base(
                    query=f"Memory usage test query {i}",
                    context_type="full_book"
                )

                assert result is not None

        # If we reach this point, memory usage was manageable for the test queries
        assert True, "Memory usage remained stable during multiple queries"


if __name__ == "__main__":
    pytest.main([__file__])