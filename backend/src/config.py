import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")

    # API Keys
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")
    BETTER_AUTH_URL: str = os.getenv("BETTER_AUTH_URL", "") # Base URL of your app
    # Application settings
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    app_name: str = "Physical AI & Humanoid Robotics Textbook Backend"
    version: str = "0.1.0"

    # Qdrant settings
    qdrant_collection_name: str = "physical_ai_robotics_textbook"
    qdrant_vector_size: int = 1024  # For Cohere embeddings

    # Cohere settings
    cohere_embedding_model: str = "embed-english-v3.0"

    # Gemini settings
    gemini_model_name: str = "gemini-pro"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra environment variables

# Create a global settings instance
settings = Settings()