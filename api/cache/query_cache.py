"""
Query Cache for Agent Executions.

Caches frequent queries to improve response time and reduce API costs.
Uses LRU cache with 5-minute TTL.
"""

import hashlib
import time
from collections import OrderedDict
from typing import Any

from api.core.logger import logger


class QueryCache:
    """
    LRU cache with TTL for query results.

    Features:
    - LRU eviction when full
    - 5-minute TTL per entry
    - Cache key based on query+model+temperature
    - Thread-safe (for single-process use)
    """

    def __init__(self, max_size: int = 100, ttl_seconds: int = 300):
        """
        Initialize query cache.

        Args:
            max_size: Maximum number of cached entries
            ttl_seconds: Time-to-live in seconds (default: 5 minutes)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.cache: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0
        logger.info(f"QueryCache initialized: max_size={max_size}, ttl={ttl_seconds}s")

    def _generate_cache_key(self, query: str, model: str, temperature: float) -> str:
        """
        Generate cache key from query parameters.

        Args:
            query: User query
            model: Model name
            temperature: Model temperature

        Returns:
            Cache key (hash)
        """
        # Create deterministic string
        cache_str = f"{query}|{model}|{temperature}"

        # Generate SHA256 hash
        return hashlib.sha256(cache_str.encode()).hexdigest()[:16]

    def get(
        self, query: str, model: str, temperature: float
    ) -> dict[str, Any] | None:
        """
        Get cached result if available and not expired.

        Args:
            query: User query
            model: Model name
            temperature: Model temperature

        Returns:
            Cached result or None if not found/expired
        """
        cache_key = self._generate_cache_key(query, model, temperature)

        if cache_key not in self.cache:
            self.misses += 1
            return None

        # Get entry
        entry = self.cache[cache_key]

        # Check TTL
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            # Expired - remove it
            del self.cache[cache_key]
            self.misses += 1
            logger.debug(f"Cache expired: {cache_key}")
            return None

        # Move to end (LRU)
        self.cache.move_to_end(cache_key)

        self.hits += 1
        hit_rate = self.hits / (self.hits + self.misses) * 100
        logger.info(f"Cache HIT: {cache_key} (hit rate: {hit_rate:.1f}%)")

        return entry["result"]

    def set(self, query: str, model: str, temperature: float, result: dict[str, Any]):
        """
        Cache a query result.

        Args:
            query: User query
            model: Model name
            temperature: Model temperature
            result: Execution result to cache
        """
        cache_key = self._generate_cache_key(query, model, temperature)

        # Remove oldest if at capacity
        if len(self.cache) >= self.max_size and cache_key not in self.cache:
            removed_key = next(iter(self.cache))
            del self.cache[removed_key]
            logger.debug(f"Cache evicted (LRU): {removed_key}")

        # Add/update entry
        self.cache[cache_key] = {"result": result, "timestamp": time.time()}

        # Move to end (most recent)
        self.cache.move_to_end(cache_key)

        logger.debug(
            f"Cache SET: {cache_key} (size: {len(self.cache)}/{self.max_size})"
        )

    def clear(self):
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        logger.info("Query cache cleared")

    def get_statistics(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats
        """
        total_requests = self.hits + self.misses
        hit_rate = (self.hits / total_requests * 100) if total_requests > 0 else 0

        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total_requests,
            "hit_rate_percent": round(hit_rate, 2),
            "ttl_seconds": self.ttl_seconds,
        }

    def cleanup_expired(self):
        """Remove expired entries from cache."""
        now = time.time()
        expired_keys = [
            key
            for key, entry in self.cache.items()
            if now - entry["timestamp"] > self.ttl_seconds
        ]

        for key in expired_keys:
            del self.cache[key]

        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global cache instance
_query_cache = QueryCache(max_size=100, ttl_seconds=300)


def get_query_cache() -> QueryCache:
    """
    Get global query cache instance.

    Returns:
        QueryCache instance
    """
    return _query_cache
