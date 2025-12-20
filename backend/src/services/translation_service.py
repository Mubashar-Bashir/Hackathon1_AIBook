import google.generativeai as genai
from typing import Optional
from ..config import settings
from ..services.cache_service import cache_service
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model_name)

    def translate_text(self, text: str, target_language: str = "ur", source_language: str = "en") -> Optional[str]:
        """
        Translate text from source language to target language using Gemini.

        Args:
            text: The text to translate
            target_language: Target language code (default: "ur" for Urdu)
            source_language: Source language code (default: "en" for English)

        Returns:
            Translated text or None if translation fails
        """
        try:
            # Check cache first to avoid unnecessary API calls
            cache_key = f"translation:{source_language}:{target_language}:{hash(text)}"
            cached_result = cache_service.get_translation(cache_key)

            if cached_result:
                logger.info(f"Returning cached translation for key: {cache_key[:32]}...")
                return cached_result

            # Create a prompt for translation
            prompt = f"""
            You are a professional translator. Translate the following text from {self._get_language_name(source_language)} to {self._get_language_name(target_language)}.

            Requirements:
            1. Preserve the original meaning and context
            2. Use appropriate formal tone suitable for educational content
            3. Maintain technical terminology accuracy
            4. Keep the translation as close to the original as possible while ensuring readability
            5. Do not add any explanations or additional text

            Text to translate:
            {text}

            Translation:
            """

            response = self.model.generate_content(prompt)

            if response.text:
                # Cache the translation result
                cache_service.set_translation(cache_key, response.text)
                logger.info(f"Translation cached with key: {cache_key[:32]}...")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty translation response")
                return self._get_fallback_translation(text, target_language)

        except Exception as e:
            logger.error(f"Error in translation service: {e}")
            return self._get_fallback_translation(text, target_language)

    def translate_chapter_content(self, chapter_content: str, target_language: str = "ur") -> Optional[str]:
        """
        Translate chapter content with special handling for educational material.

        Args:
            chapter_content: The chapter text to translate
            target_language: Target language code (default: "ur" for Urdu)

        Returns:
            Translated chapter content or None if translation fails
        """
        try:
            # Check cache first
            cache_key = f"chapter_translation:{target_language}:{hash(chapter_content)}"
            cached_result = cache_service.get_translation(cache_key)

            if cached_result:
                logger.info(f"Returning cached chapter translation for key: {cache_key[:32]}...")
                return cached_result

            # Create a prompt specifically for educational content translation
            prompt = f"""
            You are a professional translator specializing in educational content.
            Translate the following textbook chapter from English to {self._get_language_name(target_language)}.

            Guidelines for educational content translation:
            1. Preserve all technical terminology and concepts accurately
            2. Maintain the educational tone and structure
            3. Keep code snippets, formulas, and examples in their original form
            4. Ensure the translation is suitable for students learning the subject
            5. Maintain paragraph structure and readability
            6. Do not add any explanations or modify the content beyond translation
            7. Preserve headings, subheadings, and formatting cues

            Chapter content to translate:
            {chapter_content}

            Translated chapter content:
            """

            response = self.model.generate_content(prompt)

            if response.text:
                # Cache the translation result
                cache_service.set_translation(cache_key, response.text)
                logger.info(f"Chapter translation cached with key: {cache_key[:32]}...")
                return response.text.strip()
            else:
                logger.warning("Gemini returned empty chapter translation response")
                return self._get_fallback_translation(chapter_content, target_language)

        except Exception as e:
            logger.error(f"Error in chapter translation service: {e}")
            return self._get_fallback_translation(chapter_content, target_language)

    def _get_fallback_translation(self, text: str, target_language: str) -> Optional[str]:
        """
        Provide a fallback translation when the primary translation service fails.

        Args:
            text: The text to translate
            target_language: Target language code

        Returns:
            Fallback translation or None if no fallback is available
        """
        # For now, return the original text with a note that translation failed
        # In a more sophisticated system, you might use a different translation service
        # or return a placeholder message
        if target_language == "ur":
            # Return the original text with a note in Urdu that translation is unavailable
            fallback_note = f"Translation unavailable. Original text: {text}"
            return fallback_note
        else:
            # For other languages, return the original text with a note
            fallback_note = f"Translation unavailable. Original text: {text}"
            return fallback_note

    def _get_language_name(self, language_code: str) -> str:
        """
        Convert language code to full language name.

        Args:
            language_code: Language code (e.g., "ur", "en")

        Returns:
            Full language name
        """
        language_map = {
            "ur": "Urdu",
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "zh": "Chinese",
            "ja": "Japanese",
            "ar": "Arabic",
            "hi": "Hindi"
        }
        return language_map.get(language_code, language_code)

    def get_supported_languages(self) -> dict:
        """
        Get supported languages for translation.

        Returns:
            Dictionary of supported language codes and names
        """
        return {
            "ur": "Urdu",
            "en": "English"
        }

# Global instance
translation_service = TranslationService()