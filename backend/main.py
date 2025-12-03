import os
from fastapi import FastAPI
from qdrant_client import QdrantClient, models
from openai import OpenAI

app = FastAPI()

# --- Qdrant Configuration ---
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY") # Required for Qdrant Cloud
COLLECTION_NAME = "physical_ai_robotics_textbook"
VECTOR_SIZE = 1536  # For OpenAI text-embedding-ada-002

qdrant_client = QdrantClient(host=QDRANT_HOST, api_key=QDRANT_API_KEY)

# --- OpenAI Configuration ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") # Required for OpenAI Embeddings
openai_client = OpenAI(api_key=OPENAI_API_KEY)
EMBEDDING_MODEL = "text-embedding-ada-002"

async def get_text_embedding(text: str) -> list[float]:
    try:
        response = openai_client.embeddings.create(
            input=[text],
            model=EMBEDDING_MODEL
        )
        return response.data[0].embedding
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