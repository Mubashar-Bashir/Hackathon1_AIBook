# RAG Chatbot API Documentation

## Overview
This document describes the RAG (Retrieval-Augmented Generation) chatbot API endpoints for the Physical AI & Humanoid Robotics Textbook platform. The RAG system provides intelligent question-answering capabilities based on textbook content with support for context-specific queries.

## Base URL
All RAG chatbot endpoints are prefixed with `/api/chatbot`

## Authentication
- Most endpoints do not require authentication for basic functionality
- For personalized features, include a session token in the Authorization header
- Format: `Authorization: Bearer <session_token>` (optional)

## Endpoints

### POST /api/chatbot/query
Submit a query to the RAG chatbot and receive a response based on textbook content.

#### Request
```json
{
  "query": "What is Physical AI?",
  "context_type": "full_book",
  "selected_text": null,
  "user_id": null
}
```

#### Request Parameters
- `query` (string, required): The question to ask the chatbot (1-2000 characters)
- `context_type` (string, optional): Type of context to use (default: "full_book")
  - "full_book": Search entire textbook for relevant information
  - "current_page": Search only current page/chapter (not implemented yet)
  - "selected_text": Use only the provided selected text as context
- `selected_text` (string, optional): Text selected by user when context_type is "selected_text" (max 5000 characters)
- `user_id` (string, optional): User ID for authenticated users to enable personalization

#### Response (200 OK)
```json
{
  "id": "uuid-string",
  "query": "What is Physical AI?",
  "response": "Physical AI is a field that combines artificial intelligence with physical systems and robotics...",
  "sources": ["content-id-1", "content-id-2"],
  "confidence": 0.85,
  "timestamp": "2023-12-13T10:30:00Z"
}
```

#### Response Fields
- `id`: Unique identifier for the query response
- `query`: The original query submitted
- `response`: The AI-generated response to the query
- `sources`: Array of content IDs that contributed to the response
- `confidence`: Confidence score between 0 and 1 indicating response reliability
- `timestamp`: ISO 8601 formatted timestamp of the response

#### Error Responses
- `400 Bad Request`: Invalid query parameters
- `500 Internal Server Error`: Server error processing query

---

### GET /api/chatbot/health
Check the health status of the chatbot service.

#### Response (200 OK)
```json
{
  "status": "healthy",
  "timestamp": "2023-12-13T10:30:00Z",
  "dependencies": {
    "vector_db": "healthy",
    "embedding_api": "healthy",
    "generation_api": "healthy"
  }
}
```

#### Response Fields
- `status`: Overall health status ("healthy" or "error")
- `timestamp`: ISO 8601 formatted timestamp of the check
- `dependencies`: Status of external services used by the chatbot

#### Error Responses
- `500 Internal Server Error`: Health check failed

---

### GET /api/chatbot/history/{user_id}
Get the query history for a specific user (for authenticated users).

#### Path Parameters
- `user_id` (string, required): The ID of the user whose history to retrieve

#### Response (200 OK)
```json
{
  "user_id": "user-uuid-string",
  "queries": [
    {
      "id": "query-uuid",
      "query": "What is machine learning?",
      "response": "Machine learning is a subset of AI...",
      "timestamp": "2023-12-13T10:30:00Z"
    }
  ]
}
```

#### Error Responses
- `401 Unauthorized`: Missing or invalid authorization header
- `500 Internal Server Error`: Server error retrieving history

## Context Types

### Full Book Context (`context_type: "full_book"`)
- Searches the entire textbook for relevant information
- Most comprehensive but potentially slower
- Best for general questions about the subject matter

### Selected Text Context (`context_type: "selected_text"`)
- Uses only the provided text as context
- Faster response time
- Best for questions about specific passages or concepts

## Response Confidence Scoring

The API returns a confidence score between 0 and 1:
- `0.8 - 1.0`: High confidence - response is likely accurate
- `0.5 - 0.79`: Medium confidence - response is probably accurate
- `0.2 - 0.49`: Low confidence - response may contain inaccuracies
- `0.0 - 0.19`: Very low confidence - information was not found or response is unreliable

## Error Handling

The API follows standard HTTP status codes:
- `200`: Success
- `400`: Client error (bad request, validation error)
- `401`: Unauthorized (invalid/missing credentials for protected endpoints)
- `500`: Server error

All error responses include a descriptive message in the response body.

## Rate Limiting

The API implements rate limiting:
- Anonymous users: 100 requests per hour
- Authenticated users: 500 requests per hour
- Requests exceeding limits will receive a `429 Too Many Requests` response

## Performance Guidelines

- Query response times typically under 3 seconds
- 95% of queries should respond within 3 seconds
- Complex queries may take up to 5 seconds
- Caching is used to improve response times for repeated queries

## Security Considerations

1. **Input Validation**:
   - Query length limited to 2000 characters
   - Context type restricted to predefined values
   - Selected text length limited to 5000 characters

2. **Rate Limiting**:
   - Protection against abuse and excessive API usage
   - Configurable limits based on authentication status

3. **Data Sanitization**:
   - All user inputs are sanitized before processing
   - Protection against prompt injection attacks

4. **Privacy**:
   - User query history is only accessible to the authenticated user
   - Personalization data is stored securely

## Example Usage

### Basic Query
```bash
curl -X POST http://localhost:8000/api/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the Three Laws of Robotics?",
    "context_type": "full_book"
  }'
```

### Context-Specific Query
```bash
curl -X POST http://localhost:8000/api/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What does this text explain?",
    "context_type": "selected_text",
    "selected_text": "The Three Laws of Robotics are: 1) A robot may not injure a human being..."
  }'
```

### Authenticated Query with Personalization
```bash
curl -X POST http://localhost:8000/api/chatbot/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-session-token" \
  -d '{
    "query": "How does this relate to my background?",
    "context_type": "full_book",
    "user_id": "user-uuid-string"
  }'
```