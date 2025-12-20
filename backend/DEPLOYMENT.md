# Deployment Guide: Physical AI & Humanoid Robotics Textbook Backend

This document provides instructions for deploying the Physical AI & Humanoid Robotics Textbook backend service.

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Git
- Access to the following services:
  - Qdrant Cloud (vector database)
  - Cohere API (embedding service)
  - Google Gemini API (language model)
  - Neon Serverless Postgres (user data storage)

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AIBook/backend
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Create and configure the `.env` file with your API keys and settings:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

## Required Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `COHERE_API_KEY` | Cohere API key for embeddings | Yes |
| `GEMINI_API_KEY` | Google Gemini API key for responses | Yes |
| `QDRANT_URL` | Qdrant Cloud URL | Yes |
| `QDRANT_API_KEY` | Qdrant Cloud API key | Yes |
| `NEON_DATABASE_URL` | Neon Postgres database URL | Yes |
| `BETTER_AUTH_SECRET` | BetterAuth.com secret | Yes |
| `SECRET_KEY` | JWT secret key | Yes |

## Running the Application

### Development Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API documentation will be available at `http://localhost:8000/docs`

## Deployment Scripts

The repository includes a deployment script that automates the setup process:

```bash
chmod +x deploy.sh
./deploy.sh
```

## API Endpoints

- `/` - Root endpoint
- `/health` - Health check
- `/docs` - Interactive API documentation (Swagger UI)
- `/redoc` - Alternative API documentation (ReDoc)
- `/api/chatbot/*` - RAG chatbot endpoints
- `/api/auth/*` - Authentication endpoints
- `/api/personalization/*` - Personalization endpoints
- `/api/translation/*` - Translation endpoints

## Configuration Options

### Performance & Limits
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)
- `MAX_QUERY_LENGTH`: Maximum length of chatbot queries (default: 2000)
- `MAX_TEXT_LENGTH`: Maximum length of text for translation (default: 10000)
- `MAX_CHAPTER_LENGTH`: Maximum length of chapter content (default: 50000)

### Rate Limiting
- `RATE_LIMIT_REQUESTS`: Number of requests allowed per window (default: 100)
- `RATE_LIMIT_WINDOW`: Time window in seconds (default: 3600)

### Fallback Services
- `ENABLE_FALLBACK_SERVICES`: Enable fallback mechanisms (default: true)
- `FALLBACK_EMBEDDING_SERVICE`: Backup embedding service (optional)
- `FALLBACK_GENERATION_SERVICE`: Backup generation service (optional)

## Monitoring and Logging

The application logs to stdout by default. For production deployments, consider:

1. Setting up log aggregation
2. Monitoring API response times
3. Tracking error rates
4. Monitoring external service availability

## Security Considerations

1. Never commit API keys or secrets to version control
2. Use environment variables for configuration
3. Implement rate limiting to prevent abuse
4. Validate and sanitize all user inputs
5. Use HTTPS in production
6. Regularly rotate API keys

## Troubleshooting

### Common Issues

1. **API Key Errors**: Verify all required API keys are set in the `.env` file
2. **Database Connection**: Check that the Neon database URL is correct
3. **Qdrant Connection**: Verify Qdrant URL and API key are valid
4. **Rate Limiting**: Check if you've exceeded service limits

### Health Checks

Use the `/health` endpoint to verify the application status. Individual service health endpoints are available at:
- `/api/chatbot/health`
- `/api/translation/health`

## Scaling Recommendations

1. Use multiple workers in production
2. Implement proper load balancing
3. Set up a CDN for static assets
4. Monitor resource usage and scale accordingly
5. Consider using a managed service for vector database

## Rollback Procedure

1. Stop the current application
2. Revert to the previous version
3. Deploy the previous version
4. Verify the rollback was successful