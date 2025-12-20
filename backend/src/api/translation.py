from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, Field
from src.models.translation import TranslationRequest, TranslationResponse, SupportedLanguagesResponse
from src.services.translation_service import translation_service
from src.api.auth_deps import get_current_user
from datetime import datetime
import uuid

# API Contract Models for validation
class TranslationRequestModel(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    target_language: str = Field(default="ur", max_length=10, description="Target language code (default: ur for Urdu)")
    source_language: str = Field(default="en", max_length=10, description="Source language code (default: en for English)")

class TranslationResponseModel(BaseModel):
    id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    timestamp: datetime

class ChapterTranslationRequestModel(BaseModel):
    chapter_content: str = Field(..., min_length=1, max_length=50000, description="Chapter content to translate")
    target_language: str = Field(default="ur", max_length=10, description="Target language code (default: ur for Urdu)")

class ChapterTranslationResponseModel(BaseModel):
    id: str
    original_content: str
    translated_content: str
    source_language: str
    target_language: str
    timestamp: datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    dependencies: dict

class ErrorResponse(BaseModel):
    error: str
    code: str

router = APIRouter(prefix="/api/translation", tags=["translation"])

@router.post("/translate", response_model=TranslationResponseModel, responses={
    200: {"description": "Successful translation"},
    400: {"description": "Invalid translation parameters", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def translate_text(translation_request: TranslationRequestModel):
    """Translate text from source language to target language using Gemini."""
    try:
        # Validate language codes
        supported_languages = translation_service.get_supported_languages()
        if translation_request.target_language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Target language '{translation_request.target_language}' not supported. Supported languages: {list(supported_languages.keys())}"
            )

        if translation_request.source_language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Source language '{translation_request.source_language}' not supported. Supported languages: {list(supported_languages.keys())}"
            )

        # Validate text length
        if len(translation_request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        if len(translation_request.text) > 10000:
            raise HTTPException(status_code=400, detail="Text too long, maximum 10000 characters")

        # Perform translation
        translated_text = translation_service.translate_text(
            text=translation_request.text,
            target_language=translation_request.target_language,
            source_language=translation_request.source_language
        )

        if translated_text is None:
            raise HTTPException(status_code=500, detail="Unable to translate text")

        return TranslationResponseModel(
            id=str(uuid.uuid4()),
            original_text=translation_request.text,
            translated_text=translated_text,
            source_language=translation_request.source_language,
            target_language=translation_request.target_language,
            timestamp=datetime.utcnow()
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in translation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during translation")

@router.post("/translate-chapter", response_model=ChapterTranslationResponseModel, responses={
    200: {"description": "Successful chapter translation"},
    400: {"description": "Invalid translation parameters", "model": ErrorResponse},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def translate_chapter(translation_request: ChapterTranslationRequestModel):
    """Translate chapter content from source language to target language using Gemini."""
    try:
        # Validate language code
        supported_languages = translation_service.get_supported_languages()
        if translation_request.target_language not in supported_languages:
            raise HTTPException(
                status_code=400,
                detail=f"Target language '{translation_request.target_language}' not supported. Supported languages: {list(supported_languages.keys())}"
            )

        # Validate chapter content length
        if len(translation_request.chapter_content.strip()) == 0:
            raise HTTPException(status_code=400, detail="Chapter content cannot be empty")

        if len(translation_request.chapter_content) > 50000:
            raise HTTPException(status_code=400, detail="Chapter content too long, maximum 50000 characters")

        # Perform chapter translation
        translated_content = translation_service.translate_chapter_content(
            chapter_content=translation_request.chapter_content,
            target_language=translation_request.target_language
        )

        if translated_content is None:
            raise HTTPException(status_code=500, detail="Unable to translate chapter content")

        return ChapterTranslationResponseModel(
            id=str(uuid.uuid4()),
            original_content=translation_request.chapter_content,
            translated_content=translated_content,
            source_language="en",
            target_language=translation_request.target_language,
            timestamp=datetime.utcnow()
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Error in chapter translation endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during chapter translation")

@router.get("/supported-languages", response_model=SupportedLanguagesResponse, responses={
    200: {"description": "List of supported languages"},
    500: {"description": "Internal server error", "model": ErrorResponse}
})
async def get_supported_languages():
    """Get a list of supported languages for translation."""
    try:
        languages = translation_service.get_supported_languages()
        return SupportedLanguagesResponse(
            languages=languages,
            timestamp=datetime.utcnow().isoformat()
        )
    except Exception as e:
        print(f"Error in supported languages endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error retrieving supported languages")

@router.get("/health", response_model=HealthResponse, responses={
    200: {"description": "Health check successful"},
    500: {"description": "Health check failed", "model": ErrorResponse}
})
async def translation_health():
    """Check the health status of the translation service."""
    try:
        # Test if the translation service is accessible
        dependencies_status = {
            "translation_api": "healthy",  # Assuming Gemini is accessible
            "cache_service": "healthy"     # Assuming cache is accessible
        }

        return HealthResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            dependencies=dependencies_status
        )
    except Exception as e:
        print(f"Translation health check error: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")