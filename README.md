# Physical AI & Humanoid Robotics Textbook

A comprehensive textbook for Physical AI & Humanoid Robotics with integrated RAG chatbot, user authentication, personalization, and Urdu translation capabilities.

## Features

- **Interactive Textbook**: Docusaurus-based textbook for Physical AI & Humanoid Robotics
- **RAG Chatbot**: Ask questions about textbook content with Retrieval-Augmented Generation
- **User Authentication**: Secure login with BetterAuth.com integration
- **Personalized Content**: Content adapts based on user background (beginner/intermediate/expert)
- **Urdu Translation**: Translate content to Urdu for better comprehension
- **GitHub Pages Deployment**: Static content deployed to GitHub Pages

## Tech Stack

- **Frontend**: Docusaurus 3.x
- **Backend**: FastAPI
- **Database**: Neon Serverless Postgres
- **Vector Store**: Qdrant Cloud
- **Embeddings**: Cohere API
- **AI Responses**: Google Gemini API
- **Authentication**: BetterAuth.com

## Setup

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your API keys and service configurations

6. Run the backend server:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the book directory:
   ```bash
   cd book
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create environment file:
   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your configuration

5. Run the development server:
   ```bash
   npm start
   ```

The textbook will be available at `http://localhost:3000`.

## Project Structure

```
AIBook/
├── book/                 # Docusaurus frontend
│   ├── docs/             # Textbook content in markdown
│   ├── src/              # Custom Docusaurus components
│   ├── package.json      # Frontend dependencies
│   └── docusaurus.config.js # Docusaurus configuration
├── backend/              # FastAPI backend services
│   ├── src/
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── api/          # API endpoints
│   ├── main.py           # FastAPI application entry point
│   └── requirements.txt  # Backend dependencies
└── specs/                # Feature specifications and plans
```