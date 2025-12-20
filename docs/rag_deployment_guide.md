# RAG System Deployment Guide

## Overview
This document provides instructions for deploying the RAG (Retrieval-Augmented Generation) system for the Physical AI & Humanoid Robotics Textbook. The RAG system includes vector storage, content processing pipeline, and chatbot API components.

## Architecture Components

### Backend Services
- **FastAPI Application**: Main API server handling chatbot queries
- **Qdrant Vector Database**: Stores text embeddings for similarity search
- **Neon Postgres**: Stores metadata, user data, and content references
- **External APIs**: Cohere (embeddings), Google Gemini (generation)

### Frontend Components
- **Docusaurus Site**: Static textbook content with integrated chatbot
- **Chatbot UI**: React component for interacting with the RAG system

## Prerequisites

### Infrastructure Requirements
- Python 3.11+ (backend server)
- Node.js 18+ (frontend build)
- Access to Qdrant Cloud (vector database)
- Access to Neon Serverless Postgres
- API keys for Cohere and Google Gemini
- Web server for hosting static content (GitHub Pages, Vercel, etc.)

### Environment Variables
Create a `.env` file in the backend directory with the following variables:

```env
# API Keys
COHERE_API_KEY=your_cohere_api_key
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional, for fallback

# Database Configuration
NEON_DATABASE_URL=your_neon_database_url
DATABASE_URL=your_database_url

# Vector Database Configuration
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
QDRANT_COLLECTION_NAME=physical_ai_robotics_textbook
QDRANT_VECTOR_SIZE=1024

# Application Settings
SECRET_KEY=your_secret_key_for_jwt
BETTER_AUTH_SECRET=your_betterauth_secret
BETTER_AUTH_URL=http://localhost:3000

# Performance & Limits
CACHE_TTL=3600
MAX_QUERY_LENGTH=2000
MAX_TEXT_LENGTH=10000
MAX_CHAPTER_LENGTH=50000

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Fallback Services
ENABLE_FALLBACK_SERVICES=true
FALLBACK_EMBEDDING_SERVICE=openai  # Optional fallback
FALLBACK_GENERATION_SERVICE=openai  # Optional fallback

# Security Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Backend Deployment

### 1. Environment Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Database Initialization
```bash
# The application will automatically create required tables on first run
# No manual database initialization required
```

### 3. Vector Database Setup
The Qdrant collection will be automatically created when the application starts if it doesn't exist. The configuration is:
- Collection name: `physical_ai_robotics_textbook`
- Vector size: 1024 (for Cohere embeddings)
- Distance function: Cosine similarity

### 4. Starting the Backend Server
```bash
# Development mode
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API documentation will be available at `http://localhost:8000/docs`

## Frontend Deployment

### 1. Environment Setup
```bash
# Navigate to book directory
cd book

# Install dependencies
npm install
```

### 2. Environment Configuration
Create a `.env` file in the book directory:

```env
# Backend API URL
REACT_APP_API_URL=http://localhost:8000  # Change to your backend URL in production

# Other environment variables as needed
```

### 3. Building the Static Site
```bash
# Build the static site
npm run build

# The built site will be in the build/ directory
```

### 4. Deploying to GitHub Pages
```bash
# Use Docusaurus deployment command
npm run deploy
```

## Content Pipeline Automation

### 1. Initial Content Population
To populate the knowledge base with textbook content:

```bash
# Run the content pipeline
cd backend
source venv/bin/activate
python -c "
from src.services.content_service import ContentService
from src.services.embedding_service import EmbeddingService
import asyncio

async def run_pipeline():
    embedding_service = EmbeddingService()
    content_service = ContentService(embedding_service)
    results = await content_service.update_content_pipeline(
        base_url='https://your-book-url.com'
    )
    print(f'Processed {len(results)} documents')

asyncio.run(run_pipeline())
"
```

### 2. Automated Pipeline Trigger
Send a POST request to trigger the content pipeline:

```bash
curl -X POST http://localhost:8000/api/content/fetch \
  -H "Content-Type: application/json" \
  -d '{
    "base_url": "https://your-book-url.com",
    "sitemap_url": "https://your-book-url.com/sitemap.xml"
  }'
```

### 3. Scheduled Updates
Set up a cron job or scheduled task to periodically update content:

```bash
# Example cron job to run daily at 2 AM
0 2 * * * cd /path/to/backend && source venv/bin/activate && python -c "..."
```

## Monitoring and Health Checks

### API Health Endpoints
- `/api/chatbot/health` - Chatbot service health
- `/api/auth/health` - Authentication service health
- `/health` - Overall application health

### Performance Monitoring
The system tracks:
- Query response times
- API error rates
- External service availability
- Vector database performance

### Logging
- Application logs are written to stdout
- Error logs include detailed information for debugging
- Access logs track API usage patterns

## Security Configuration

### Rate Limiting
- Anonymous users: 100 requests/hour
- Authenticated users: 500 requests/hour
- Configurable via environment variables

### Authentication
- JWT-based session management
- Secure password hashing (PBKDF2)
- Session expiration (configurable)

### Input Validation
- Query length limits
- Content type restrictions
- Sanitization of user inputs

## Scaling Recommendations

### Horizontal Scaling
- Use multiple workers for the FastAPI application
- Implement load balancing for high traffic
- Consider using a managed service for vector database

### Caching Strategy
- Response caching for frequently asked questions
- Embedding caching to reduce API calls
- CDN for static assets

### Database Optimization
- Proper indexing on frequently queried fields
- Connection pooling for database connections
- Read replicas for high-read scenarios

## Troubleshooting

### Common Issues

#### API Key Errors
- **Symptoms**: 500 errors, "Invalid API key" messages
- **Solution**: Verify all API keys are correctly set in environment variables

#### Database Connection Issues
- **Symptoms**: "Connection refused", "Database unavailable"
- **Solution**: Check database URL and credentials in environment variables

#### Vector Database Issues
- **Symptoms**: Slow responses, search failures
- **Solution**: Verify Qdrant URL and API key, check collection exists

#### Content Pipeline Failures
- **Symptoms**: 404 errors when fetching content, incomplete indexing
- **Solution**: Verify source URLs are accessible, check sitemap.xml format

### Health Checks
Regularly monitor:
- `/api/chatbot/health` for chatbot status
- External API availability (Cohere, Gemini)
- Database connectivity
- Vector database connectivity

### Log Analysis
Check application logs for:
- Error patterns
- Performance bottlenecks
- Failed API calls
- Security incidents

## Rollback Procedure

1. Stop the current application
2. Revert to the previous version
3. Deploy the previous version
4. Verify the rollback was successful using health checks
5. Monitor for any issues post-rollback

## Performance Benchmarks

### Response Time Targets
- 95% of queries respond in under 3 seconds
- Simple queries respond in under 1.5 seconds
- Complex queries respond in under 5 seconds

### Throughput Targets
- Support 100 concurrent users
- Handle 500+ daily chatbot queries
- Process content updates within 10 minutes

## Environment-Specific Configurations

### Development
- Enable debug mode
- Use local database instances
- Lower rate limits for testing

### Staging
- Mirror production configuration
- Reduced rate limits
- Separate API keys for testing

### Production
- Disable debug mode
- Use production-grade databases
- Full rate limiting enabled
- Proper monitoring and alerting