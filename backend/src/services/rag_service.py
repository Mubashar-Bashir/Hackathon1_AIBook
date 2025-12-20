import google.generativeai as genai
from typing import List, Dict, Any, Optional
from ..config import settings
from ..services.embedding_service import embedding_service
from ..services.cache_service import cache_service
from ..models.chatbot import ChatbotQueryResponse
from ..services.content_service import ContentService
from ..utils.logging import log_function_calling_event, log_rag_query_event, log_error
import uuid
import asyncio
from datetime import datetime

class RAGService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model_name)

        # Initialize content service for content retrieval functions
        from .embedding_service import embedding_service
        from ..utils.vector_store import vector_store
        self.content_service = ContentService(embedding_service, vector_store)

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
            # Provide a graceful fallback response
            return self._get_fallback_response(query)

    def _get_fallback_response(self, query: str) -> str:
        """
        Provide a fallback response when the primary LLM service is unavailable.

        Args:
            query: The original query from the user

        Returns:
            Fallback response string
        """
        # In a more sophisticated system, you might:
        # 1. Use a local model
        # 2. Return cached responses
        # 3. Provide helpful links to relevant textbook sections
        # 4. Suggest the user try again later
        fallback_message = (
            f"Currently unable to process your query: '{query[:50]}...'\n\n"
            "The AI service may be temporarily unavailable. Please try again later.\n\n"
            "In the meantime, you might want to browse the textbook content directly "
            "to find the information you're looking for."
        )
        return fallback_message

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

    def query_with_function_calling(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None) -> Optional[ChatbotQueryResponse]:
        """
        Process a query using enhanced reasoning with Google Gemini's capabilities.
        Falls back to basic RAG if advanced features are unavailable.
        """
        try:
            # Log the function calling event
            log_function_calling_event(
                function_name="query_with_function_calling",
                args={"query_length": len(query), "context_type": context_type, "has_selected_text": selected_text is not None},
                **{"query_preview": query[:100] + "..." if len(query) > 100 else query}
            )

            # Define available functions/tools
            functions = [
                {
                    "name": "search_knowledge_base",
                    "description": "Search the knowledge base for information related to the query",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of results to return"
                            }
                        },
                        "required": ["query", "limit"]
                    }
                },
                {
                    "name": "get_content_by_url",
                    "description": "Get specific content by its URL",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL of the content to retrieve"
                            }
                        },
                        "required": ["url"]
                    }
                },
                {
                    "name": "summarize_content",
                    "description": "Summarize a piece of content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content to summarize"
                            }
                        },
                        "required": ["content"]
                    }
                }
            ]

            # Prepare the initial message
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant for a Physical AI & Humanoid Robotics textbook. Use the provided tools to search for information and answer the user's question accurately and helpfully."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]

            # Use Gemini's capabilities to understand the query and determine the best approach
            analysis_prompt = f"""
            You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
            Analyze the user's query and determine the best approach to answer it.

            Query: {query}

            Consider these approaches:
            1. Search the knowledge base for relevant information
            2. Summarize specific content (if URL or specific content is mentioned)
            3. Provide a direct answer based on general knowledge

            Respond in JSON format with the following structure:
            {{
                "approach": "search_knowledge_base|summarize_content|direct_answer",
                "search_query": "query to search if approach is search_knowledge_base",
                "content_to_summarize": "content to summarize if approach is summarize_content",
                "direct_response": "direct response if approach is direct_answer"
            }}
            """

            analysis_response = self.model.generate_content(analysis_prompt)

            # Parse the response to determine the approach
            import json
            import re

            # Extract JSON from the response
            response_text = analysis_response.text if analysis_response.text else ""
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)

            if json_match:
                try:
                    approach_data = json.loads(json_match.group())
                except json.JSONDecodeError:
                    # If JSON parsing fails, use basic RAG
                    result = self.query_knowledge_base(query, context_type, selected_text)
                    if result:
                        log_rag_query_event(
                            query=query,
                            response=result.response,
                            sources=result.sources,
                            confidence=result.confidence,
                            **{"fallback_reason": "json_parsing_failed"}
                        )
                    return result
            else:
                # If no JSON found, use basic RAG
                result = self.query_knowledge_base(query, context_type, selected_text)
                if result:
                    log_rag_query_event(
                        query=query,
                        response=result.response,
                        sources=result.sources,
                        confidence=result.confidence,
                        **{"fallback_reason": "no_json_response"}
                    )
                return result

            approach = approach_data.get("approach", "search_knowledge_base")

            if approach == "search_knowledge_base":
                search_query = approach_data.get("search_query", query)

                # Use the existing search functionality
                search_results = embedding_service.search_similar_content(search_query, 5)

                if search_results:
                    context_text = "\n\n".join([result["content_text"] for result in search_results])
                    sources = [result["content_id"] for result in search_results]

                    # Generate final response with the retrieved context
                    final_prompt = f"""
                    You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
                    Use the following context to answer the user's question accurately and helpfully.

                    Context from textbook:
                    {context_text}

                    User's question: {query}

                    Please provide a comprehensive answer based on the context provided.
                    """

                    final_response = self.model.generate_content(final_prompt)
                    response_text = final_response.text if final_response.text else "I couldn't generate a response to your query."

                    confidence = self._calculate_confidence(response_text, query)

                    result = ChatbotQueryResponse(
                        id=str(uuid.uuid4()),
                        query=query,
                        response=response_text,
                        sources=sources,
                        confidence=confidence,
                        timestamp=datetime.utcnow()
                    )

                    # Log the successful RAG query
                    log_rag_query_event(
                        query=query,
                        response=response_text,
                        sources=sources,
                        confidence=confidence
                    )

                    return result
                else:
                    # No results found, return appropriate response
                    result = ChatbotQueryResponse(
                        id=str(uuid.uuid4()),
                        query=query,
                        response="I couldn't find any relevant information in the textbook to answer this question. Please try rephrasing your question or check if the topic is covered in the textbook.",
                        sources=[],
                        confidence=0.1,
                        timestamp=datetime.utcnow()
                    )

                    log_rag_query_event(
                        query=query,
                        response=result.response,
                        sources=[],
                        confidence=0.1
                    )

                    return result
            elif approach == "summarize_content":
                content_to_summarize = approach_data.get("content_to_summarize", "")
                if content_to_summarize:
                    summary_prompt = f"""
                    Please summarize the following content concisely:

                    {content_to_summarize}
                    """

                    summary_response = self.model.generate_content(summary_prompt)
                    response_text = summary_response.text if summary_response.text else "I couldn't generate a summary."

                    result = ChatbotQueryResponse(
                        id=str(uuid.uuid4()),
                        query=query,
                        response=response_text,
                        sources=[],
                        confidence=0.7,
                        timestamp=datetime.utcnow()
                    )

                    log_rag_query_event(
                        query=query,
                        response=result.response,
                        sources=[],
                        confidence=0.7
                    )

                    return result
            elif approach == "direct_answer":
                direct_response = approach_data.get("direct_response", "")
                if direct_response:
                    result = ChatbotQueryResponse(
                        id=str(uuid.uuid4()),
                        query=query,
                        response=direct_response,
                        sources=[],
                        confidence=0.5,
                        timestamp=datetime.utcnow()
                    )

                    log_rag_query_event(
                        query=query,
                        response=result.response,
                        sources=[],
                        confidence=0.5
                    )

                    return result

            # If no specific approach worked, fallback to basic RAG
            result = self.query_knowledge_base(query, context_type, selected_text)

            if result:
                log_rag_query_event(
                    query=query,
                    response=result.response,
                    sources=result.sources,
                    confidence=result.confidence
                )

            return result

        except Exception as e:
            print(f"Error in Gemini enhanced reasoning: {e}")
            log_error(e, "gemini_enhanced_reasoning")
            log_function_calling_event(
                function_name="query_with_function_calling",
                args={"query": query},
                error=str(e)
            )
            # Fallback to basic RAG if enhanced reasoning fails
            result = self.query_knowledge_base(query, context_type, selected_text)

            if result:
                log_rag_query_event(
                    query=query,
                    response=result.response,
                    sources=result.sources,
                    confidence=result.confidence,
                    **{"fallback_reason": "enhanced_reasoning_error"}
                )

            return result

    def process_query_with_enhanced_reasoning(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None) -> Optional[ChatbotQueryResponse]:
        """
        Process a query with enhanced reasoning using Google Gemini capabilities.
        Falls back to basic RAG if advanced features are unavailable.
        """
        # First try the enhanced function calling approach
        result = self.query_with_function_calling(query, context_type, selected_text)

        if result and result.response and "couldn't find any relevant information" not in result.response.lower():
            return result
        else:
            # If function calling didn't work well, fallback to basic RAG
            return self.query_knowledge_base(query, context_type, selected_text)

    def stream_query_response(self, query: str, context_type: str = "full_book", selected_text: Optional[str] = None):
        """
        Stream a query response using the LLM with the provided context.
        Yields response chunks as they are generated.
        """
        try:
            if context_type == "selected_text" and selected_text:
                # Use only the selected text as context
                context_text = selected_text
            else:
                # Search for relevant content in the knowledge base
                search_results = embedding_service.search_similar_content(query, 5)

                if not search_results:
                    # If no relevant content found, return a response indicating this
                    yield {
                        "type": "response",
                        "content": "I couldn't find any relevant information in the textbook to answer this question. Please try rephrasing your question or check if the topic is covered in the textbook.",
                        "sources": [],
                        "confidence": 0.0,
                        "done": True
                    }
                    return

                # Combine the relevant content for context
                context_text = "\n\n".join([result["content_text"] for result in search_results])
                sources = [result["content_id"] for result in search_results]

            # Create a prompt with the context and query
            prompt = f"""
            You are an AI assistant for a Physical AI & Humanoid Robotics textbook.
            Use the following context to answer the user's question accurately and helpfully.

            Context from textbook:
            {context_text}

            User's question: {query}

            Please provide a comprehensive answer based on the context provided.
            If the context doesn't contain the information needed to answer the question,
            acknowledge this and suggest the user check other parts of the textbook.
            """

            # Use streaming generation
            response = self.model.generate_content(prompt, stream=True)

            # Yield the sources first
            yield {
                "type": "sources",
                "sources": sources
            }

            # Stream the response chunks
            full_response = ""
            for chunk in response:
                chunk_text = chunk.text if chunk.text else ""
                full_response += chunk_text
                if chunk_text.strip():  # Only yield non-empty chunks
                    yield {
                        "type": "response",
                        "content": chunk_text,
                        "done": False
                    }

            # Calculate confidence based on the full response
            confidence = self._calculate_confidence(full_response, query)

            # Cache the full response
            cache_key = f"{query}:{context_type}:{selected_text or ''}"
            cache_service.set(
                query=cache_key,
                response=full_response,
                sources=sources,
                confidence=confidence
            )

            # Signal completion
            yield {
                "type": "response",
                "content": "",
                "sources": sources,
                "confidence": confidence,
                "done": True
            }

        except Exception as e:
            print(f"Error in streaming RAG query: {e}")
            yield {
                "type": "error",
                "content": "Sorry, I encountered an error while processing your query.",
                "done": True
            }


# Global instance
rag_service = RAGService()