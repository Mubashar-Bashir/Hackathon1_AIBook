# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git
- Access to Cohere API (for embeddings)
- Access to Google Gemini API (for responses)
- Access to Qdrant Cloud (for vector storage)
- Access to Neon Serverless Postgres (for user data)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd AIBook
```

### 2. Set up the Frontend (Docusaurus)

```bash
# Navigate to the book directory
cd book

# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Update .env with your configuration
# (API endpoints for backend services)
```

### 3. Set up the Backend (FastAPI)

```bash
# Navigate to the backend directory
cd ../backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your API keys and service configurations:
# - COHERE_API_KEY
# - GEMINI_API_KEY
# - QDRANT_URL and QDRANT_API_KEY
# - NEON_DATABASE_URL
# - BETTER_AUTH_SECRET
```

### 4. Environment Variables

Create `.env` files in both directories with the following variables:

**Backend (.env):**
```env
COHERE_API_KEY=your_cohere_api_key
GEMINI_API_KEY=your_gemini_api_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_auth_secret
DEBUG=true
```

**Frontend (.env):**
```env
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_BETTER_AUTH_URL=http://localhost:8000/auth
```

### 5. Initialize the Vector Database

```bash
cd backend
source venv/bin/activate
python -m src.services.vector_store.initialize
```

This will:
- Connect to Qdrant
- Create the necessary collections
- Index the textbook content

### 6. Run the Backend Server

```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --port 8000
```

### 7. Run the Frontend Development Server

In a new terminal:

```bash
cd book
npm start
```

The textbook will be available at `http://localhost:3000`.

## Key Components

### Textbook Content
- Located in `book/docs/`
- Written in Markdown format
- Organized by chapters and modules
- Supports Docusaurus features (tabs, admonitions, code blocks)

### RAG Chatbot
- Backend: FastAPI service at `/api/chatbot`
- Frontend: React component integrated into Docusaurus pages
- Uses Cohere embeddings and Gemini for responses
- Supports both full-book and selected-text queries

### User Authentication
- Integration with BetterAuth.com
- Stores user background information (beginner/intermediate/expert)
- Required for personalization and translation features

### Personalization Service
- Backend: FastAPI service at `/api/personalization`
- Adjusts content complexity based on user background
- Caching for performance

### Translation Service
- Backend: FastAPI service at `/api/translation`
- Supports Urdu translation
- Caching for performance

## Deployment

### Frontend to GitHub Pages
```bash
cd book
npm run build
# The build output is in the build/ directory
# Configure GitHub Pages to serve from the build/ directory
```

### Backend to Cloud Platform
Deploy the FastAPI application to your preferred cloud platform (AWS, GCP, Azure, Vercel, etc.)

## Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend Tests
```bash
cd book
npm test
```

### End-to-End Tests
```bash
# Using Playwright
cd backend
source venv/bin/activate
# Run backend server first, then:
npx playwright test
```

## Troubleshooting

### Common Issues

1. **API Keys Not Working**
   - Verify all API keys are correctly set in environment variables
   - Check that the services (Cohere, Gemini) are properly configured

2. **Database Connection Issues**
   - Ensure Neon Serverless Postgres URL is correct
   - Verify database credentials and permissions

3. **Vector Search Not Returning Results**
   - Confirm Qdrant collection was properly initialized
   - Check that textbook content was indexed

4. **Frontend Cannot Connect to Backend**
   - Verify backend server is running
   - Check that REACT_APP_BACKEND_URL is set correctly

## Next Steps

1. Add textbook content to the `book/docs/` directory
2. Customize the Docusaurus theme and styling
3. Implement additional personalization features
4. Add more language translations
5. Set up monitoring and logging