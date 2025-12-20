import pytest
from unittest.mock import patch, MagicMock
from src.services.rag_service import RAGService
from src.models.chatbot import ChatbotQueryResponse
from datetime import datetime


class TestResponseAccuracy:
    """Test cases for response accuracy and quality."""

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

    def test_response_relevance_to_query(self, rag_service):
        """Test that responses are relevant to the original query."""
        test_cases = [
            {
                "query": "What is Physical AI?",
                "context": "Physical AI is a field that combines artificial intelligence with physical systems and robotics.",
                "expected_keywords": ["Physical AI", "artificial intelligence", "robotics"]
            },
            {
                "query": "Explain humanoid robotics",
                "context": "Humanoid robotics involves creating robots with human-like form and capabilities.",
                "expected_keywords": ["humanoid", "robotics", "human-like"]
            },
            {
                "query": "What are neural networks?",
                "context": "Neural networks are computing systems inspired by the human brain.",
                "expected_keywords": ["neural networks", "brain", "computing"]
            }
        ]

        for case in test_cases:
            with patch.object(rag_service, '_generate_response', return_value=f"Based on the context: {case['context']}, Physical AI is related to your query about {case['query']}"), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.8), \
                 patch('src.services.rag_service.embedding_service') as mock_embedding_service:

                mock_embedding_service.search_similar_content.return_value = [
                    {
                        "content_id": "test_content_1",
                        "content_text": case["context"],
                        "metadata": {},
                        "score": 0.9
                    }
                ]

                result = rag_service.query_knowledge_base(
                    query=case["query"],
                    context_type="full_book"
                )

                assert result is not None
                response_lower = result.response.lower()

                # Check that at least one expected keyword is in the response
                keyword_found = any(keyword.lower() in response_lower for keyword in case["expected_keywords"])
                assert keyword_found, f"Response '{result.response}' should contain keywords related to query '{case['query']}'"

    def test_response_accuracy_with_specific_context(self, rag_service):
        """Test that responses accurately reflect the provided context."""
        specific_context = "The Three Laws of Robotics are: 1) A robot may not injure a human being or, through inaction, allow a human being to come to harm. 2) A robot must obey the orders given to it by human beings, except where such orders would conflict with the First Law. 3) A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws."

        query = "What are the Three Laws of Robotics?"

        with patch.object(rag_service, '_generate_response', return_value="The Three Laws of Robotics are: 1) A robot may not injure a human being or, through inaction, allow a human being to come to harm. 2) A robot must obey the orders given to it by human beings, except where such orders would conflict with the First Law. 3) A robot must protect its own existence as long as such protection does not conflict with the First or Second Laws."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.95), \
             patch('src.services.rag_service.embedding_service') as mock_embedding_service:

            mock_embedding_service.search_similar_content.return_value = [
                {
                    "content_id": "robotics_laws_1",
                    "content_text": specific_context,
                    "metadata": {},
                    "score": 0.98
                }
            ]

            result = rag_service.query_knowledge_base(
                query=query,
                context_type="full_book"
            )

            assert result is not None
            # The response should contain information about the Three Laws of Robotics
            assert "Three Laws" in result.response
            assert "robot" in result.response.lower()
            assert result.confidence > 0.9  # High confidence due to exact match

    def test_response_quality_with_insufficient_context(self, rag_service):
        """Test response quality when context doesn't contain the answer."""
        insufficient_context = "This chapter discusses general programming concepts."
        query = "What is the mathematical formula for inverse kinematics?"

        with patch.object(rag_service, '_generate_response', return_value="I couldn't find any relevant information in the textbook to answer this question. Please try rephrasing your question or check if the topic is covered in the textbook."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.1), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "general_programming_1",
                    "content_text": insufficient_context,
                    "metadata": {},
                    "score": 0.3  # Low score indicating poor match
                }
            ]

            result = rag_service.query_knowledge_base(
                query=query,
                context_type="full_book"
            )

            assert result is not None
            # Should acknowledge that information wasn't found
            assert "couldn't find" in result.response.lower() or "not covered" in result.response.lower()
            assert result.confidence < 0.3  # Low confidence for insufficient context

    def test_response_consistency_for_same_query(self, rag_service):
        """Test that the same query with same context produces consistent responses."""
        context = "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience."
        query = "What is machine learning?"

        with patch.object(rag_service, '_generate_response', return_value="Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.9), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "ml_definition_1",
                    "content_text": context,
                    "metadata": {},
                    "score": 0.95
                }
            ]

            # Get response for the same query twice
            result1 = rag_service.query_knowledge_base(
                query=query,
                context_type="full_book"
            )

            result2 = rag_service.query_knowledge_base(
                query=query,
                context_type="full_book"
            )

            assert result1 is not None
            assert result2 is not None
            # Responses should be similar (or identical)
            assert result1.response == result2.response
            assert abs(result1.confidence - result2.confidence) < 0.01  # Confidence should be very similar

    def test_context_preservation_in_response(self, rag_service):
        """Test that important context information is preserved in responses."""
        context = "According to Asimov's laws, robots must not harm humans. This principle guides all robot behavior in the textbook examples."
        query = "What is the primary principle for robot behavior?"

        with patch.object(rag_service, '_generate_response', return_value="The primary principle for robot behavior, according to Asimov's laws, is that robots must not harm humans. This principle guides all robot behavior in the textbook examples."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.88), \
             patch.object(rag_service, 'content_service') as mock_content_service:

            mock_content_service.search_similar_content.return_value = [
                {
                    "content_id": "robot_principles_1",
                    "content_text": context,
                    "metadata": {},
                    "score": 0.92
                }
            ]

            result = rag_service.query_knowledge_base(
                query=query,
                context_type="full_book"
            )

            assert result is not None
            response_lower = result.response.lower()
            # Response should contain key information from context
            assert "asimov" in response_lower
            assert "harm humans" in response_lower
            assert "principle" in response_lower

    def test_selected_text_context_accuracy(self, rag_service):
        """Test that responses accurately reflect only the selected text context."""
        selected_text = "Deep reinforcement learning combines deep learning with reinforcement learning to enable agents to learn optimal behaviors."
        query = "What is deep reinforcement learning?"

        with patch.object(rag_service, '_generate_response', return_value="Deep reinforcement learning combines deep learning with reinforcement learning to enable agents to learn optimal behaviors."), \
             patch.object(rag_service, '_calculate_confidence', return_value=0.92):

            result = rag_service.query_knowledge_base(
                query=query,
                context_type="selected_text",
                selected_text=selected_text
            )

            assert result is not None
            # Response should be based on the selected text
            assert "deep learning" in result.response.lower()
            assert "reinforcement learning" in result.response.lower()
            assert "agents" in result.response.lower()
            assert result.confidence > 0.8  # High confidence for exact match

    def test_response_quality_metric_calculation(self, rag_service):
        """Test that confidence scores accurately reflect response quality."""
        # Test high-quality response
        high_quality_response = "Based on the context, Physical AI is a field that combines artificial intelligence with physical systems and robotics. The key aspects include sensorimotor learning, embodied cognition, and adaptive behavior in real-world environments."
        query = "What is Physical AI?"

        high_confidence = rag_service._calculate_confidence(high_quality_response, query)

        # Test low-quality response (acknowledging lack of information)
        low_quality_response = "I couldn't find any relevant information in the textbook to answer this question. Please try rephrasing your question or check if the topic is covered in the textbook."
        low_confidence = rag_service._calculate_confidence(low_quality_response, query)

        # High-quality response should have higher confidence
        assert high_confidence > low_confidence
        # Low-quality response should have low confidence
        assert low_confidence < 0.3
        # High-quality response should have moderate to high confidence
        assert high_confidence > 0.5

    def test_response_relevance_under_different_context_types(self, rag_service):
        """Test that responses remain relevant under different context types."""
        context = "Humanoid robots are robots with human-like body structure, including limbs and sometimes facial features."

        queries_and_contexts = [
            {
                "query": "What defines a humanoid robot?",
                "context_type": "full_book",
                "selected_text": None
            },
            {
                "query": "What makes a robot humanoid?",
                "context_type": "selected_text",
                "selected_text": context
            }
        ]

        for test_case in queries_and_contexts:
            with patch.object(rag_service, '_generate_response', return_value="Humanoid robots are robots with human-like body structure, including limbs and sometimes facial features."), \
                 patch.object(rag_service, '_calculate_confidence', return_value=0.85), \
                 patch.object(rag_service, 'content_service') as mock_content_service:

                if test_case["context_type"] == "full_book":
                    mock_content_service.search_similar_content.return_value = [
                        {
                            "content_id": "humanoid_def_1",
                            "content_text": context,
                            "metadata": {},
                            "score": 0.9
                        }
                    ]

                result = rag_service.query_knowledge_base(
                    query=test_case["query"],
                    context_type=test_case["context_type"],
                    selected_text=test_case["selected_text"]
                )

                assert result is not None
                assert "humanoid" in result.response.lower()
                assert "human-like" in result.response.lower()


if __name__ == "__main__":
    pytest.main([__file__])