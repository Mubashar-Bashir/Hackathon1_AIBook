import time
import asyncio
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, requests: int = 100, window: int = 3600):
        """
        Initialize rate limiter.

        Args:
            requests: Number of requests allowed per window
            window: Time window in seconds
        """
        self.requests = requests
        self.window = window
        self.requests_registry: Dict[str, Deque[float]] = defaultdict(deque)

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed for the given identifier.

        Args:
            identifier: Unique identifier for the requester (IP, user ID, etc.)

        Returns:
            True if request is allowed, False otherwise
        """
        now = time.time()
        request_times = self.requests_registry[identifier]

        # Remove requests that are outside the current window
        while request_times and request_times[0] <= now - self.window:
            request_times.popleft()

        # Check if we're under the limit
        if len(request_times) < self.requests:
            request_times.append(now)
            return True

        return False

    def get_reset_time(self, identifier: str) -> float:
        """
        Get the time when the rate limit will reset for the identifier.

        Args:
            identifier: Unique identifier for the requester

        Returns:
            Unix timestamp when the rate limit will reset
        """
        request_times = self.requests_registry[identifier]
        if not request_times:
            return time.time()

        # The reset time is when the oldest request expires
        return request_times[0] + self.window

# Global rate limiter instance
rate_limiter = RateLimiter(requests=100, window=3600)  # 100 requests per hour

async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware to prevent abuse of the API.
    """
    # Get client IP for rate limiting
    client_ip = request.client.host if request.client else "unknown"

    # Add user ID if available (from JWT token or session)
    auth_header = request.headers.get("authorization")
    user_id = "unknown"

    if auth_header and auth_header.startswith("Bearer "):
        # In a real implementation, you would decode the JWT to get user ID
        # For now, we'll just use the IP for rate limiting
        pass

    identifier = f"ip:{client_ip}"

    # Check if request is allowed
    if not rate_limiter.is_allowed(identifier):
        reset_time = rate_limiter.get_reset_time(identifier)
        retry_after = int(reset_time - time.time())

        logger.warning(f"Rate limit exceeded for {identifier}")

        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "code": "RATE_LIMIT_EXCEEDED",
                "message": f"Too many requests. Please try again in {retry_after} seconds.",
                "retry_after": retry_after
            },
            headers={"Retry-After": str(retry_after)}
        )

    response = await call_next(request)
    return response

def get_rate_limiter():
    """
    Get the rate limiter instance.

    Returns:
        RateLimiter instance
    """
    return rate_limiter