from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
import uuid

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to translate")
    target_language: str = Field(default="ur", max_length=10, description="Target language code")
    source_language: str = Field(default="en", max_length=10, description="Source language code")

class TranslationResponse(BaseModel):
    id: str
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    timestamp: datetime

class ChapterTranslationRequest(BaseModel):
    chapter_content: str = Field(..., min_length=1, max_length=50000, description="Chapter content to translate")
    target_language: str = Field(default="ur", max_length=10, description="Target language code")

class ChapterTranslationResponse(BaseModel):
    id: str
    original_content: str
    translated_content: str
    source_language: str
    target_language: str
    timestamp: datetime

class SupportedLanguagesResponse(BaseModel):
    languages: Dict[str, str]  # language_code: language_name
    timestamp: str