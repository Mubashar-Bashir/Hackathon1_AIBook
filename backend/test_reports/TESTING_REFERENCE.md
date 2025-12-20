# Testing Reference Guide

## Quick Test Commands

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories
```bash
# API tests
python -m pytest tests/test_chatbot_api.py -v

# Integration tests
python -m pytest tests/integration/ -v

# Performance tests
python -m pytest tests/test_performance_benchmarks.py -v

# Specific feature tests
python -m pytest tests/ -k "streaming" -v
```

### Run Tests with Coverage
```bash
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term
```

## Test Environment Setup

### Required Environment Variables
```bash
# Copy from .env.example
cp .env.example .env

# Update with your values
export GEMINI_API_KEY="your_key_here"
export COHERE_API_KEY="your_key_here"
export QDRANT_API_KEY="your_key_here"
export DATABASE_URL="your_db_url"
export BETTER_AUTH_SECRET="your_secret"
```

### Test Database Setup
```bash
# For testing, use SQLite
export DATABASE_URL="sqlite:///./test.db"
export TEST_MODE="true"
```

## Common Test Scenarios

### 1. RAG Streaming Test
```python
# Test streaming endpoint
test_data = {
    "query": "Your question here",
    "context_type": "full_book",  # or "selected_text"
    "selected_text": None,        # if context_type is "selected_text"
    "user_id": "optional_user_id"
}

response = client.post("/api/chatbot/stream-query", json=test_data)
# Expected: 200 OK with SSE formatted response
```

### 2. Standard Query Test
```python
# Test standard endpoint
response = client.post("/api/chatbot/query", json=test_data)
# Expected: 200 OK with JSON response
```

### 3. Authentication Test
```python
# Test auth endpoints
response = client.post("/api/auth/login", json={
    "email": "test@example.com",
    "password": "test_password"
})
# Expected: 200 OK with token
```

## Debugging Commands

### Check API Endpoints
```bash
# Check all available endpoints
curl http://localhost:8000/docs

# Test health endpoint
curl http://localhost:8000/health

# Test chatbot endpoint
curl -X POST http://localhost:8000/api/chatbot/query \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "context_type": "full_book"}'
```

### Test Streaming Manually
```bash
# Test streaming endpoint
curl -N -X POST http://localhost:8000/api/chatbot/stream-query \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "context_type": "full_book"}'
```

## Common Issues & Solutions

### 1. API Key Issues
**Problem**: `404 models/gemini-pro is not found`
**Solution**: Update your GEMINI_API_KEY and check model availability

### 2. Database Connection Issues
**Problem**: Database connection errors
**Solution**: Verify DATABASE_URL and connection parameters

### 3. Vector Store Issues
**Problem**: Qdrant connection failures
**Solution**: Check QDRANT_API_KEY and collection configuration

### 4. Streaming Format Issues
**Problem**: Incorrect SSE format
**Solution**: Verify response format matches: `data: {...}\n\n`

## Test Data Patterns

### Valid Test Data
```python
valid_query = {
    "query": "What is Physical AI?",
    "context_type": "full_book",  # Options: "full_book", "current_page", "selected_text"
    "selected_text": "Optional selected text",
    "user_id": "optional_user_id"
}
```

### Invalid Test Data
```python
# Empty query
{"query": "", "context_type": "full_book"}

# Invalid context type
{"query": "test", "context_type": "invalid_type"}

# Missing required field
{"context_type": "full_book"}  # Missing query
```

## Response Validation

### Standard Response Format
```json
{
  "id": "uuid",
  "query": "original query",
  "response": "AI response",
  "sources": ["list", "of", "sources"],
  "confidence": 0.85,
  "timestamp": "datetime"
}
```

### Streaming Response Format
```
data: {"type": "sources", "sources": ["source1", "source2"]}
data: {"type": "response", "content": "Response chunk", "done": false}
data: {"type": "response", "content": "", "sources": ["sources"], "confidence": 0.8, "done": true}
```

## Performance Benchmarks

### Expected Response Times
- Health check: < 100ms
- Simple query: < 2s
- Complex query: < 5s
- Streaming first chunk: < 2s

### Memory Usage
- Startup: < 100MB
- Under load: < 300MB
- Peak usage: < 500MB

## Test Coverage Targets

### Minimum Coverage
- API endpoints: 90%
- Service methods: 85%
- Error handling: 80%
- Integration tests: 95%

### Coverage Commands
```bash
# Generate coverage report
coverage run -m pytest tests/
coverage report
coverage html  # Creates HTML report in htmlcov/
```

## Troubleshooting Checklist

### Before Running Tests
- [ ] Environment variables set
- [ ] Database connection available
- [ ] External services accessible
- [ ] Dependencies installed

### If Tests Fail
- [ ] Check environment variables
- [ ] Verify API keys are valid
- [ ] Confirm database connectivity
- [ ] Review recent code changes
- [ ] Check logs for error details

### Performance Issues
- [ ] Monitor response times
- [ ] Check memory usage
- [ ] Verify database connections
- [ ] Test external service latency

## Quick Debug Script
```python
# debug_test.py - Quick functionality check
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test health
resp = client.get("/health")
print(f"Health: {resp.status_code}")

# Test chatbot
resp = client.post("/api/chatbot/query",
                  json={"query": "test", "context_type": "full_book"})
print(f"Query: {resp.status_code}")

# Test streaming
resp = client.post("/api/chatbot/stream-query",
                  json={"query": "test", "context_type": "full_book"})
print(f"Streaming: {resp.status_code}, Length: {len(resp.content)}")
```

---
*Reference Guide Version: 1.0*
*Last Updated: December 15, 2025*