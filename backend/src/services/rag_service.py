import google.generativeai as genai
from typing import List, Dict, Any, Optional
from ..config import settings
from ..services.embedding_service import embedding_service
from ..services.cache_service import cache_service
from ..models.chatbot import ChatbotQueryResponse
import uuid
from datetime import datetime

class RAGService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model_name)

    def query_knowledge_base(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None, limit: int = 5) -> Optional[ChatbotQueryResponse]:
        """Process a query against the knowledge base using RAG."""
        try:
            # Check cache first
            cache_key = f"{query}:{context_type}:{selected_text or ''}"
            cached_result = cache_service.get(cache_key)

            if cached_result:
                return ChatbotQueryResponse(
                    id=cached_result["query_hash"][:12] if hasattr(cached_result, 'query_hash') else str(uuid.uuid4())[:12],
                    query=cached_result["query"],
                    response=cached_result["response"],
                    sources=cached_result["sources"],
                    confidence=cached_result["confidence"],
                    timestamp=cached_result["timestamp"]
                )

            # Get relevant context from vector store
            if context_type == "selected_text" and selected_text:
                # Use only the selected text as context
                context_text = selected_text
                sources = ["selected_text"]
            else:
                # Search for relevant content in the knowledge base
                search_results = embedding_service.search_similar_content(query, limit)

                if not search_results:
                    # If no relevant content found, return a response indicating this
                    response = self._generate_response(query, "", "no_context")

                    # Cache the response
                    cache_service.set(
                        query=cache_key,
                        response=response,
                        sources=[],
                        confidence=0.0
                    )

                    return ChatbotQueryResponse(
                        id=str(uuid.uuid4()),
                        query=query,
                        response=response,
                        sources=[],
                        confidence=0.0,
                        timestamp=datetime.utcnow()
                    )

                # Combine the relevant content for context
                context_text = "\n\n".join([result["content_text"] for result in search_results])
                sources = [result["content_id"] for result in search_results]

            # Generate response using the context
            response = self._generate_response(query, context_text, context_type)

            # Calculate a basic confidence score based on the quality of the response
            confidence = self._calculate_confidence(response, query)

            # Cache the response
            cache_service.set(
                query=cache_key,
                response=response,
                sources=sources,
                confidence=confidence
            )

            return ChatbotQueryResponse(
                id=str(uuid.uuid4()),
                query=query,
                response=response,
                sources=sources,
                confidence=confidence,
                timestamp=datetime.utcnow()
            )
        except Exception as e:
            print(f"Error in RAG query: {e}")
            return None

    def _generate_response(self, query: str, context: str, context_type: str) -> str:
        """Generate a response using the LLM with the provided context."""
        try:
            if context_type == "no_context":
                # If no context was found, generate a response acknowledging this
                prompt = f"""
                The user asked: "{query}"

                I couldn't find any relevant information in the textbook to answer this question.
                Please try rephrasing your question or check if the topic is covered in the textbook.
                """
            else:
                # Create a prompt with the context and query
                prompt = f"""
                You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
                Use the following context to answer the user's question accurately and helpfully.

                Context from textbook:
                {context}

                User's question: {query}

                Please provide a comprehensive answer based on the context provided.
                If the context doesn't contain the information needed to answer the question,
                acknowledge this and suggest the user check other parts of the textbook.
                """

            response = self.model.generate_content(prompt)
            return response.text if response.text else "I couldn't generate a response to your query."
        except Exception as e:
            print(f"Error generating response with Gemini: {e}")
            return "Sorry, I encountered an error while processing your query."

    def _calculate_confidence(self, response: str, query: str) -> float:
        """Calculate a basic confidence score for the response."""
        # This is a simple confidence calculation - in a real system, you'd have more sophisticated methods
        if "I couldn't find any relevant information" in response or "I encountered an error" in response:
            return 0.1  # Low confidence

        # Calculate based on response length and keyword presence
        response_length = len(response)
        query_words = query.lower().split()
        response_words = response.lower().split()

        # Count how many query words appear in the response
        matching_words = sum(1 for word in query_words if word in response_words)
        match_ratio = matching_words / len(query_words) if query_words else 0

        # Combine factors for a basic confidence score
        length_factor = min(response_length / 100, 0.5)  # Up to 0.5 for length
        match_factor = match_ratio * 0.5  # Up to 0.5 for matching

        confidence = min(length_factor + match_factor, 1.0)
        return confidence

    def process_query_with_fallback(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None) -> Optional[ChatbotQueryResponse]:
        """Process a query with fallback mechanisms if primary approach fails."""
        # Try the primary RAG approach
        result = self.query_knowledge_base(query, context_type, selected_text)

        if result is None or result.response == "Sorry, I encountered an error while processing your query.":
            # Fallback: try again with a broader context
            result = self.query_knowledge_base(query, "full_book", None, limit=10)

        return result

# Global instance
rag_service = RAGService()