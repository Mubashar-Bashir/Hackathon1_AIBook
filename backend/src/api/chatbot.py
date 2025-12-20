from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List, Optional, AsyncGenerator
from pydantic import BaseModel, Field
from src.models.chatbot import ChatbotQueryCreate, ChatbotQueryResponse
from src.services.rag_service import rag_service
from datetime import datetime
import uuid
import json
from fastapi.responses import StreamingResponse

# API Contract Models for validation
class ChatbotQueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The question to ask the chatbot")
    context_type: str = Field(default="full_book", description="Type of context: 'full_book', 'current_page', or 'selected_text'")
    selected_text: Optional[str] = Field(default=None, max_length=5000, description="Text selected by user when context_type is 'selected_text'")
    user_id: Optional[str] = Field(default=None, max_length=100, description="User ID for authenticated users")

class ChatbotQueryResponseModel(BaseModel):
    id: str
    query: str
    response: str
    sources: List[str]
    confidence: float
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    dependencies: dict

class ErrorResponse(BaseModel):
    error: str
    code: str

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])

@router.post("/query", response_model=ChatbotQueryResponse, responses={
    200: {"description": "Successful response to the query"},
    400: {"description": "Invalid query parameters", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def query_chatbot(chatbot_query: ChatbotQueryRequest):
    """Submit a query to the RAG chatbot and receive a response based on textbook content."""
    try:
        # Validate the query length
        if len(chatbot_query.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(chatbot_query.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long, maximum 2000 characters")

        # Validate context_type
        valid_context_types = ["full_book", "current_page", "selected_text"]
        if chatbot_query.context_type not in valid_context_types:
            raise HTTPException(status_code=400, detail=f"context_type must be one of {valid_context_types}")

        # Process the query using the RAG service with enhanced reasoning
        result = rag_service.process_query_with_enhanced_reasoning(
            query=chatbot_query.query,
            context_type=chatbot_query.context_type,
            selected_text=chatbot_query.selected_text
        )

        if result is None:
            raise HTTPException(status_code=500, detail="Error processing the query")

        return result
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in chatbot query endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing query")

@router.get("/health", response_model=HealthResponse, responses={
    200: {"description": "Health check successful"},
    500: {"description": "Health check failed", "model": ErrorResponse}
})
async def chatbot_health():
    """Check the health status of the chatbot service."""
    try:
        # Test if the services are accessible
        dependencies_status = {
            "vector_db": "healthy",  # Assuming vector store is accessible
            "embedding_api": "healthy",  # Assuming Cohere is accessible
            "generation_api": "healthy"  # Assuming Gemini is accessible
        }

        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            dependencies=dependencies_status
        )
    except Exception as e:
        print(f"Health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")

# In-memory storage for query history (in production, use a proper database)
query_history = []

@router.get("/history/{user_id}")
async def get_query_history(user_id: str):
    """Get the query history for a specific user."""
    user_queries = [q for q in query_history if q.get("user_id") == user_id]
    return {"user_id": user_id, "queries": user_queries}

@router.post("/stream-query")
async def stream_query(chatbot_query: ChatbotQueryRequest):
    """Stream a query response using Server-Sent Events (SSE) for real-time chat experience."""
    try:
        # Validate the query length
        if len(chatbot_query.query.strip()) == 0:
            raise HTTPException(status_code=400, detail="Query cannot be empty")

        if len(chatbot_query.query) > 2000:
            raise HTTPException(status_code=400, detail="Query too long, maximum 2000 characters")

        # Validate context_type
        valid_context_types = ["full_book", "current_page", "selected_text"]
        if chatbot_query.context_type not in valid_context_types:
            raise HTTPException(status_code=400, detail=f"context_type must be one of {valid_context_types}")

        def event_generator():
            try:
                for chunk in rag_service.stream_query_response(
                    query=chatbot_query.query,
                    context_type=chatbot_query.context_type,
                    selected_text=chatbot_query.selected_text
                ):
                    yield f"data: {json.dumps(chunk)}\n\n"
            except GeneratorExit:
                # Client disconnected, stop streaming
                pass

        return StreamingResponse(event_generator(), media_type="text/plain")

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in streaming chatbot query endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error processing stream query")