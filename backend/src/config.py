import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # Database settings
    neon_database_url: str = os.getenv("NEON_DATABASE_URL", "")
    database_url: str = os.getenv("DATABASE_URL", "")

    # API Keys
    cohere_api_key: str = os.getenv("COHERE_API_KEY", "")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    qdrant_url: str = os.getenv("QDRANT_URL", "")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "")
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "")

    # BetterAuth settings
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

    # Next.js/Stack settings (for compatibility)
    next_public_stack_project_id: str = os.getenv("NEXT_PUBLIC_STACK_PROJECT_ID", "")
    next_public_stack_publishable_client_key: str = os.getenv("NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY", "")
    stack_secret_server_key: str = os.getenv("STACK_SECRET_SERVER_KEY", "")

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

    # Performance & Limits
    default_cache_ttl: int = int(os.getenv("CACHE_TTL", "3600"))  # 1 hour
    max_query_length: int = int(os.getenv("MAX_QUERY_LENGTH", "2000"))
    max_text_length: int = int(os.getenv("MAX_TEXT_LENGTH", "10000"))
    max_chapter_length: int = int(os.getenv("MAX_CHAPTER_LENGTH", "50000"))

    # Rate Limiting
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_window: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hour

    # Fallback & Resilience
    enable_fallback_services: bool = os.getenv("ENABLE_FALLBACK_SERVICES", "true").lower() == "true"
    fallback_embedding_service: Optional[str] = os.getenv("FALLBACK_EMBEDDING_SERVICE")
    fallback_generation_service: Optional[str] = os.getenv("FALLBACK_GENERATION_SERVICE")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Performance settings
    max_concurrent_requests: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "10"))
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

    class Config:
        env_file = ".env"

# Create a global settings instance
settings = Settings()


def validate_settings():
    """
    Validate that required settings are present.

    Returns:
        List of validation errors
    """
    errors = []

    if not settings.cohere_api_key:
        errors.append("COHERE_API_KEY is required")

    if not settings.gemini_api_key:
        errors.append("GEMINI_API_KEY is required")

    if not settings.qdrant_url:
        errors.append("QDRANT_URL is required")

    if not settings.qdrant_api_key:
        errors.append("QDRANT_API_KEY is required")

    # OpenAI API key is optional since we have fallback to basic RAG
    # But if function calling is enabled, it becomes required
    # For now, we'll make it optional to maintain fallback capability

    return errors


def get_service_status():
    """
    Get the status of external services.

    Returns:
        Dictionary with service status information
    """
    status = {
        "cohere": bool(settings.cohere_api_key),
        "gemini": bool(settings.gemini_api_key),
        "openai": bool(settings.openai_api_key),
        "qdrant": bool(settings.qdrant_url and settings.qdrant_api_key),
        "database": bool(settings.neon_database_url),
        "fallback_enabled": settings.enable_fallback_services
    }

    return status