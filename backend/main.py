import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import QdrantClient, models
import cohere
import google.generativeai as genai
from src.api.chatbot import router as chatbot_router
from src.api.auth import router as auth_router
from src.api.personalization import router as personalization_router

app = FastAPI(title="Physical AI & Humanoid Robotics Textbook Backend")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(chatbot_router)
app.include_router(auth_router)
app.include_router(personalization_router)

# --- Qdrant Configuration ---
QDRANT_URL = os.getenv("QDRANT_URL")  # Required for Qdrant Cloud
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  # Required for Qdrant Cloud
COLLECTION_NAME = "physical_ai_robotics_textbook"
VECTOR_SIZE = 1024  # For Cohere embeddings

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# --- Cohere Configuration ---
COHERE_API_KEY = os.getenv("COHERE_API_KEY")  # Required for Cohere embeddings
co = cohere.Client(COHERE_API_KEY)
EMBEDDING_MODEL = "embed-english-v3.0"

# --- Google Gemini Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Required for Gemini responses
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

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
        return []

# Ensure Qdrant collection exists on startup
@app.on_event("startup")
async def startup_event():
    try:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
        )
        print(f"Qdrant collection '{COLLECTION_NAME}' created (or re-created) successfully.")
    except Exception as e:
        print(f"Error creating Qdrant collection: {e}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Physical AI & Humanoid Robotics Textbook RAG Backend!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "textbook-backend"}