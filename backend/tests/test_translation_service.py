import pytest
from unittest.mock import Mock, patch, MagicMock
from src.services.translation_service import TranslationService
from src.services.cache_service import cache_service


class TestTranslationService:
    @pytest.fixture
    def translation_service(self):
        """Create a translation service instance for testing."""
        service = TranslationService()
        # Mock the Gemini model to avoid external API calls
        service.model = Mock()
        return service

    def test_translate_text_success(self, translation_service):
        """Test successful text translation."""
        # Clear cache first to avoid conflicts with other tests
        from src.services.cache_service import cache_service
        cache_service.clear_all()

        # Mock the Gemini response
        mock_response = Mock()
        mock_response.text = "میں ایک ٹیسٹ ہوں"
        translation_service.model.generate_content.return_value = mock_response

        # Test the translation with unique text
        result = translation_service.translate_text("I am a successful test", "ur")

        assert result == "میں ایک ٹیسٹ ہوں"
        translation_service.model.generate_content.assert_called_once()

    def test_translate_text_empty_response(self, translation_service):
        """Test handling of empty translation response."""
        # Clear cache to ensure we don't get cached results from other tests
        from src.services.cache_service import cache_service
        cache_service.clear_all()

        # Mock the Gemini response with empty text
        mock_response = Mock()
        mock_response.text = ""
        translation_service.model.generate_content.return_value = mock_response

        # Test the translation - should return fallback
        result = translation_service.translate_text("I am an empty test", "ur")

        assert result is not None
        assert "Translation unavailable" in result

    def test_translate_text_exception_handling(self, translation_service):
        """Test exception handling in translation."""
        # Clear cache to ensure we don't get cached results from other tests
        from src.services.cache_service import cache_service
        cache_service.clear_all()

        # Mock the Gemini to raise an exception
        translation_service.model.generate_content.side_effect = Exception("API Error")

        # Test the translation - should return fallback
        result = translation_service.translate_text("I am an exception test", "ur")

        assert result is not None
        assert "Translation unavailable" in result

    def test_translate_chapter_content_success(self, translation_service):
        """Test successful chapter content translation."""
        # Clear cache to ensure we don't get cached results from other tests
        from src.services.cache_service import cache_service
        cache_service.clear_all()

        # Mock the Gemini response
        mock_response = Mock()
        mock_response.text = "یہ ایک ٹیسٹ چیپٹر ہے"
        translation_service.model.generate_content.return_value = mock_response

        # Test the chapter translation
        chapter_content = "This is a test chapter content for translation."
        result = translation_service.translate_chapter_content(chapter_content, "ur")

        assert result == "یہ ایک ٹیسٹ چیپٹر ہے"
        translation_service.model.generate_content.assert_called_once()

    def test_get_supported_languages(self, translation_service):
        """Test getting supported languages."""
        languages = translation_service.get_supported_languages()

        assert "ur" in languages
        assert "en" in languages
        assert languages["ur"] == "Urdu"
        assert languages["en"] == "English"

    def test_get_language_name(self, translation_service):
        """Test getting full language name from code."""
        assert translation_service._get_language_name("ur") == "Urdu"
        assert translation_service._get_language_name("en") == "English"
        assert translation_service._get_language_name("es") == "Spanish"
        assert translation_service._get_language_name("unknown") == "unknown"


class TestCacheService:
    def test_cache_set_and_get(self):
        """Test basic cache functionality."""
        # Clear cache first
        cache_service.clear_all()

        # Test setting a value
        result = cache_service.set("test_key", "test_value", sources=["source1"], confidence=0.9)
        assert result is True

        # Test getting the value
        cached = cache_service.get("test_key")
        assert cached is not None
        assert cached["response"] == "test_value"
        assert cached["sources"] == ["source1"]
        assert cached["confidence"] == 0.9

    def test_cache_expiration(self):
        """Test cache expiration functionality."""
        # Clear cache first
        cache_service.clear_all()

        # Set a value with short TTL
        result = cache_service.set("expiring_key", "expiring_value", ttl=1)  # 1 second TTL
        assert result is True

        # Manually expire the entry by setting past time
        from datetime import datetime, timedelta
        key_hash = cache_service._generate_hash("expiring_key")
        if key_hash in cache_service._cache:
            cache_service._cache[key_hash].expires_at = datetime.utcnow() - timedelta(seconds=1)

        # Try to get the expired value
        cached = cache_service.get("expiring_key")
        assert cached is None

    def test_translation_cache_set_and_get(self):
        """Test translation-specific cache functionality."""
        # Clear cache first
        cache_service.clear_all()

        # Test setting a translation value
        result = cache_service.set_translation("translation_key", "translated_text")
        assert result is True

        # Test getting the translation value
        cached = cache_service.get_translation("translation_key")
        assert cached == "translated_text"

    def test_cache_invalidate(self):
        """Test cache invalidation."""
        # Clear cache first
        cache_service.clear_all()

        # Set a value
        cache_service.set("test_key", "test_value")
        assert cache_service.get("test_key") is not None

        # Invalidate the key
        result = cache_service.invalidate("test_key")
        assert result is True

        # Verify it's no longer in cache
        assert cache_service.get("test_key") is None