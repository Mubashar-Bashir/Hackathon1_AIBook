import pytest
import time
from unittest.mock import Mock, patch
from fastapi import Request
from fastapi.responses import JSONResponse
from src.middleware.rate_limit import RateLimiter, rate_limit_middleware


class TestRateLimiter:
    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        limiter = RateLimiter(requests=10, window=3600)
        assert limiter.requests == 10
        assert limiter.window == 3600

    def test_rate_limiter_allows_requests_under_limit(self):
        """Test that rate limiter allows requests under the limit."""
        limiter = RateLimiter(requests=3, window=3600)

        # First 3 requests should be allowed
        assert limiter.is_allowed("test_id") is True
        assert limiter.is_allowed("test_id") is True
        assert limiter.is_allowed("test_id") is True

        # 4th request should be denied
        assert limiter.is_allowed("test_id") is False

    def test_rate_limiter_resets_after_window(self):
        """Test that rate limiter resets after the time window."""
        limiter = RateLimiter(requests=2, window=1)  # 1 second window

        # Use up the requests
        assert limiter.is_allowed("test_id") is True
        assert limiter.is_allowed("test_id") is True
        assert limiter.is_allowed("test_id") is False

        # Wait for window to pass
        time.sleep(1.1)

        # Now requests should be allowed again
        assert limiter.is_allowed("test_id") is True

    def test_rate_limiter_separate_counts_per_identifier(self):
        """Test that rate limiter tracks separate counts for different identifiers."""
        limiter = RateLimiter(requests=2, window=3600)

        # Both identifiers should be able to make requests independently
        assert limiter.is_allowed("id1") is True
        assert limiter.is_allowed("id1") is True
        assert limiter.is_allowed("id1") is False  # id1 is now limited

        assert limiter.is_allowed("id2") is True  # id2 should still be allowed
        assert limiter.is_allowed("id2") is True
        assert limiter.is_allowed("id2") is False  # id2 is now limited


class TestRateLimitMiddleware:
    @pytest.mark.asyncio
    async def test_rate_limit_middleware_allows_requests_under_limit(self):
        """Test that the middleware allows requests under the rate limit."""
        # Create a mock request
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.headers = {}

        # Create a mock call_next function that returns a successful response
        async def mock_call_next(request):
            return Mock()

        # Test that requests are allowed under the limit
        response = await rate_limit_middleware(mock_request, mock_call_next)
        assert response is not None

    @pytest.mark.asyncio
    async def test_rate_limit_middleware_blocks_excessive_requests(self):
        """Test that the middleware blocks requests that exceed the rate limit."""
        # Create rate limiter with very low limit
        from src.middleware.rate_limit import rate_limiter
        original_requests = rate_limiter.requests
        rate_limiter.requests = 1  # Only allow 1 request

        try:
            # Create a mock request
            mock_request = Mock(spec=Request)
            mock_request.client = Mock()
            mock_request.client.host = "127.0.0.1"
            mock_request.headers = {}

            # Create a mock call_next function
            async def mock_call_next(request):
                return Mock()

            # First request should pass
            response1 = await rate_limit_middleware(mock_request, mock_call_next)
            assert response1 is not None

            # Second request should be blocked
            response2 = await rate_limit_middleware(mock_request, mock_call_next)
            assert isinstance(response2, JSONResponse)
            assert response2.status_code == 429

        finally:
            # Restore original rate limit
            rate_limiter.requests = original_requests