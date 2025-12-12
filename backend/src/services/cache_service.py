import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pydantic import BaseModel

class CacheEntry(BaseModel):
    query_hash: str
    query_text: str
    response: str
    sources: list
    confidence: float
    timestamp: datetime
    expires_at: datetime

class CacheService:
    def __init__(self, default_ttl: int = 3600):  # 1 hour default TTL
        self.default_ttl = default_ttl
        self._cache: Dict[str, CacheEntry] = {}

    def _generate_hash(self, query: str) -> str:
        """Generate a hash for the query to use as cache key."""
        return hashlib.sha256(query.encode()).hexdigest()

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        """Get cached response for a query if it exists and hasn't expired."""
        query_hash = self._generate_hash(query)

        if query_hash in self._cache:
            entry = self._cache[query_hash]

            # Check if entry has expired
            if datetime.utcnow() > entry.expires_at:
                del self._cache[query_hash]
                return None

            # Return cached response data
            return {
                "query": entry.query_text,
                "response": entry.response,
                "sources": entry.sources,
                "confidence": entry.confidence,
                "timestamp": entry.timestamp
            }

        return None

    def set(self, query: str, response: str, sources: list = None, confidence: float = 0.0, ttl: int = None) -> bool:
        """Cache a response for a query."""
        if sources is None:
            sources = []

        if ttl is None:
            ttl = self.default_ttl

        query_hash = self._generate_hash(query)
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)

        entry = CacheEntry(
            query_hash=query_hash,
            query_text=query,
            response=response,
            sources=sources,
            confidence=confidence,
            timestamp=datetime.utcnow(),
            expires_at=expires_at
        )

        self._cache[query_hash] = entry
        return True

    def invalidate(self, query: str) -> bool:
        """Remove a specific query from cache."""
        query_hash = self._generate_hash(query)

        if query_hash in self._cache:
            del self._cache[query_hash]
            return True

        return False

    def clear_expired(self):
        """Remove all expired entries from cache."""
        current_time = datetime.utcnow()
        expired_keys = []

        for key, entry in self._cache.items():
            if current_time > entry.expires_at:
                expired_keys.append(key)

        for key in expired_keys:
            del self._cache[key]

    def clear_all(self):
        """Clear all entries from cache."""
        self._cache.clear()

# Global instance
cache_service = CacheService()