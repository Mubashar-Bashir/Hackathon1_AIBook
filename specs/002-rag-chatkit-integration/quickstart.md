# Quickstart Guide: RAG Integration with ChatKit UI

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Git
- Access to OpenAI API
- Access to Cohere API
- Access to Qdrant Cloud
- Access to Neon Postgres

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AIBook
   ```

2. **Set up backend environment**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up frontend environment**
   ```bash
   cd ../book
   npm install
   ```

4. **Configure environment variables**
   Create `.env` file in the `backend` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_cloud_url
   QDRANT_API_KEY=your_qdrant_api_key
   NEON_DATABASE_URL=your_neon_database_url
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

2. **Start the frontend development server**
   ```bash
   cd book
   npm start
   ```

## Key Components

### Backend Structure
- `src/api/` - FastAPI endpoints
- `src/services/` - Business logic services
- `src/models/` - Data models
- `src/tools/` - OpenAI Function Calling tools
- `src/utils/` - Utility functions

### Frontend Structure
- `src/components/` - React components including ChatKit integration
- `src/pages/` - Docusaurus pages
- `static/` - Static assets

## Running Tests

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd book
npm test
```

## Content Pipeline

### Fetching Content
To fetch content from Vercel/GitHub:
```bash
cd backend
python -c "from src.services.content_service import fetch_content_pipeline; fetch_content_pipeline()"
```

### Manual Content Pipeline Trigger
Send a POST request to `/api/content/fetch` to trigger the content pipeline.

## API Endpoints

### Chatbot API
- `POST /api/chatbot/query` - Process user queries with RAG
- Request body: `{"query": "your question", "context_type": "full_book|selected_text", "selected_text": "optional text"}`

### Content Pipeline API
- `POST /api/content/fetch` - Trigger content fetching pipeline
- `GET /api/content/status` - Check pipeline status

## Deployment

### Backend Deployment
1. Set up production environment variables
2. Deploy to cloud platform (AWS, GCP, Azure, or VPS)
3. Ensure Qdrant Cloud and Neon Postgres are accessible

### Frontend Deployment
1. Build the static site: `npm run build`
2. Deploy to GitHub Pages or preferred static hosting
3. Configure CORS to allow backend API calls

## Troubleshooting

### Common Issues

1. **API Keys Not Working**
   - Verify all API keys are correctly set in environment variables
   - Check for typos in the key values

2. **Qdrant Connection Issues**
   - Verify Qdrant URL and API key
   - Ensure network connectivity to Qdrant Cloud

3. **Content Fetching Fails**
   - Check if the source URL is accessible
   - Verify the sitemap.xml or content structure

### Logging
- Backend logs are available in the console during development
- For production, configure structured logging to file or monitoring service

## Performance Tips

1. **Caching**: Enable Redis caching for frequent queries
2. **Embedding Batching**: Process multiple chunks simultaneously during pipeline runs
3. **Database Indexing**: Ensure proper indexes are created for frequently queried fields

## Security Considerations

1. **Input Sanitization**: All user inputs are sanitized before processing
2. **Rate Limiting**: API endpoints have built-in rate limiting
3. **Authentication**: Optional authentication for personalized features