#!/bin/bash

# Deployment script for Physical AI & Humanoid Robotics Textbook Backend
# This script handles the deployment of the backend service

set -e  # Exit on any error

echo "🚀 Starting deployment of Physical AI & Humanoid Robotics Textbook Backend..."

# Check if we're in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run this script from the backend directory."
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ Error: pip is not installed or not in PATH"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create or update virtual environment
echo "📦 Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists, activating..."
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check for environment variables
ENV_FILE=".env"
if [ ! -f "$ENV_FILE" ]; then
    echo "⚠️  Warning: $ENV_FILE file not found. Creating a template..."
    cat > .env << EOF
# Physical AI & Humanoid Robotics Textbook Backend Environment Variables

# API Keys
COHERE_API_KEY=your_cohere_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
QDRANT_URL=your_qdrant_url_here
QDRANT_API_KEY=your_qdrant_api_key_here
BETTER_AUTH_SECRET=your_better_auth_secret_here

# Database
NEON_DATABASE_URL=your_neon_database_url_here

# Security
SECRET_KEY=change_this_to_a_secure_random_key

# Performance & Limits
CACHE_TTL=3600
MAX_QUERY_LENGTH=2000
MAX_TEXT_LENGTH=10000
MAX_CHAPTER_LENGTH=50000

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# Fallback & Resilience
ENABLE_FALLBACK_SERVICES=true
FALLBACK_EMBEDDING_SERVICE=
FALLBACK_GENERATION_SERVICE=

# Debug
DEBUG=false
EOF
    echo "📝 Template .env file created. Please update it with your actual values."
    echo "⚠️  IMPORTANT: Update the .env file with your actual API keys and configuration before running the server!"
    exit 1
else
    echo "✅ Environment file found, loading variables..."
    export $(grep -v '^#' .env | xargs)
fi

# Run tests to ensure everything is working
echo "🧪 Running tests..."
python -m pytest tests/ -v

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Please fix the issues before deployment."
    exit 1
fi

echo "✅ All tests passed"

# Create necessary directories if they don't exist
mkdir -p logs

# Run database migrations if needed (if migration directory exists)
if [ -d "migrations" ]; then
    echo "🔄 Running database migrations..."
    # Add migration command here if using Alembic or similar
    # python -m alembic upgrade head
fi

echo "✅ Backend deployment preparation complete!"

echo ""
echo "🎉 Deployment preparation successful!"
echo ""
echo "To start the server, run:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "For production, use:"
echo "  uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4"
echo ""
echo "Make sure your environment variables are properly set in the .env file."

# Check if services are accessible
echo ""
echo "📡 Checking service connectivity..."

# Check if Qdrant is accessible (this is a basic check)
if [ ! -z "$QDRANT_URL" ] && [ ! -z "$QDRANT_API_KEY" ]; then
    echo "✅ Qdrant configuration found"
else
    echo "❌ Qdrant configuration missing in .env file"
fi

# Check if Cohere is accessible
if [ ! -z "$COHERE_API_KEY" ]; then
    echo "✅ Cohere configuration found"
else
    echo "❌ Cohere configuration missing in .env file"
fi

# Check if Gemini is accessible
if [ ! -z "$GEMINI_API_KEY" ]; then
    echo "✅ Gemini configuration found"
else
    echo "❌ Gemini configuration missing in .env file"
fi

echo ""
echo "📋 Deployment checklist:"
echo "  - [ ] Update .env file with real API keys"
echo "  - [ ] Verify Qdrant connection"
echo "  - [ ] Verify Cohere API access"
echo "  - [ ] Verify Gemini API access"
echo "  - [ ] Test API endpoints"
echo "  - [ ] Set up monitoring (optional)"
echo "  - [ ] Set up logging aggregation (optional)"