import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from qdrant_client import QdrantClient, models
import cohere
import google.generativeai as genai
from src.api.chatbot import router as chatbot_router
from src.api.auth import router as auth_router
from src.api.personalization import router as personalization_router
from src.api.translation import router as translation_router
from src.api.content_pipeline import router as content_pipeline_router
from src.api.rag_monitor import router as rag_monitor_router
from src.api.skills_agents import router as skills_agents_router
from src.middleware.error_handler import add_exception_handlers
from src.middleware.rate_limit import rate_limit_middleware
from src.middleware.validation import input_validation_middleware
from src.utils.logging import setup_logging

app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook Backend",
    description="""
    This is the backend API for the Physical AI & Humanoid Robotics Textbook project.

    ## Features
    - RAG (Retrieval-Augmented Generation) chatbot for textbook content
    - User authentication and personalization
    - Urdu translation capabilities
    - Vector search for content retrieval

    ## Technologies Used
    - FastAPI: Modern, fast web framework for building APIs with Python
    - Qdrant: Vector database for similarity search
    - Cohere: Embedding models for content vectorization
    - Google Gemini: Language model for response generation
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup logging
setup_logging(log_level=os.getenv("LOG_LEVEL", "INFO"))

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]").split(",")
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(input_validation_middleware)

# Add exception handlers
add_exception_handlers(app)

# Include API routers
app.include_router(chatbot_router)
app.include_router(auth_router)
app.include_router(personalization_router)
app.include_router(translation_router)
app.include_router(content_pipeline_router)
app.include_router(rag_monitor_router)
app.include_router(skills_agents_router)

from src.config import settings, validate_settings
from src.utils.logging import setup_logging

# Validate settings on startup
startup_errors = validate_settings()
if startup_errors:
    print("Configuration errors found:")
    for error in startup_errors:
        print(f"  - {error}")
    print("Please set the required environment variables before starting the server.")
    exit(1)

# --- Qdrant Configuration ---
qdrant_client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key)

# --- Cohere Configuration ---
co = cohere.Client(settings.cohere_api_key)
EMBEDDING_MODEL = settings.cohere_embedding_model

# --- Google Gemini Configuration ---
genai.configure(api_key=settings.gemini_api_key)
gemini_model = genai.GenerativeModel(settings.gemini_model_name)

async def get_text_embedding(text: str) -> list[float]:
    try:
        response = co.embed(
            texts=[text],
            model=EMBEDDING_MODEL,
            input_type="search_document"
        )
        return response.embeddings[0]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        # Use fallback method if primary embedding service fails
        from src.services.embedding_service import embedding_service
        return embedding_service._get_fallback_embedding(text) or []

# Ensure Qdrant collection exists on startup
@app.on_event("startup")
async def startup_event():
    try:
        qdrant_client.recreate_collection(
            collection_name=settings.qdrant_collection_name,
            vectors_config=models.VectorParams(size=settings.qdrant_vector_size, distance=models.Distance.COSINE),
        )
        print(f"Qdrant collection '{settings.qdrant_collection_name}' created (or re-created) successfully.")
    except Exception as e:
        print(f"Error creating Qdrant collection: {e}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Textbook RAG Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "textbook-backend"}