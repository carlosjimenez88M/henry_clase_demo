"""
Rate Limiting Middleware.

Implements token bucket algorithm to limit requests to 60/minute per IP.
"""

import time
from typing import Dict, Tuple
from collections import defaultdict
from fastapi import Request, HTTPException, status
from api.core.logger import logger


class TokenBucket:
    """
    Token bucket for rate limiting.

    Each IP address gets a bucket with tokens that refill over time.
    """

    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize token bucket.

        Args:
            capacity: Maximum tokens (max burst)
            refill_rate: Tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def consume(self, tokens: int = 1) -> bool:
        """
        Try to consume tokens.

        Args:
            tokens: Number of tokens to consume

        Returns:
            True if tokens consumed, False if insufficient
        """
        # Refill tokens based on time passed
        now = time.time()
        time_passed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + time_passed * self.refill_rate
        )
        self.last_refill = now

        # Try to consume
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False

    def get_wait_time(self) -> float:
        """Get seconds to wait until next token available."""
        if self.tokens >= 1:
            return 0
        return (1 - self.tokens) / self.refill_rate


class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    Default: 60 requests per minute per IP.
    """

    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.

        Args:
            requests_per_minute: Maximum requests per minute
        """
        self.requests_per_minute = requests_per_minute
        self.capacity = requests_per_minute
        self.refill_rate = requests_per_minute / 60.0  # Per second
        self.buckets: Dict[str, TokenBucket] = defaultdict(
            lambda: TokenBucket(self.capacity, self.refill_rate)
        )
        logger.info(f"RateLimiter initialized: {requests_per_minute} req/min")

    def check_rate_limit(self, client_ip: str) -> Tuple[bool, float]:
        """
        Check if request is allowed for this IP.

        Args:
            client_ip: Client IP address

        Returns:
            Tuple of (allowed, wait_time_if_denied)
        """
        bucket = self.buckets[client_ip]
        allowed = bucket.consume()

        if not allowed:
            wait_time = bucket.get_wait_time()
            logger.warning(f"Rate limit exceeded for {client_ip}, wait {wait_time:.1f}s")
            return False, wait_time

        return True, 0.0

    def cleanup_old_buckets(self, max_age_minutes: int = 60):
        """
        Clean up buckets for IPs that haven't made requests recently.

        Args:
            max_age_minutes: Remove buckets older than this
        """
        # Simple cleanup - just reset if too many buckets
        if len(self.buckets) > 10000:
            logger.warning(f"Too many rate limit buckets ({len(self.buckets)}), clearing old ones")
            self.buckets.clear()


# Global rate limiter instance
_rate_limiter = RateLimiter(requests_per_minute=60)


def get_client_ip(request: Request) -> str:
    """
    Extract client IP from request.

    Args:
        request: FastAPI request

    Returns:
        Client IP address
    """
    # Check for forwarded IP (if behind proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()

    # Get direct IP
    return request.client.host if request.client else "unknown"


async def rate_limit_middleware(request: Request, call_next):
    """
    Rate limiting middleware.

    Args:
        request: FastAPI request
        call_next: Next middleware/handler

    Returns:
        Response

    Raises:
        HTTPException: If rate limit exceeded
    """
    # Skip rate limiting for health check
    if request.url.path == "/health":
        return await call_next(request)

    # Get client IP
    client_ip = get_client_ip(request)

    # Check rate limit
    allowed, wait_time = _rate_limiter.check_rate_limit(client_ip)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Please wait {wait_time:.1f} seconds.",
                "retry_after": int(wait_time) + 1
            },
            headers={"Retry-After": str(int(wait_time) + 1)}
        )

    # Process request
    response = await call_next(request)

    # Add rate limit headers
    response.headers["X-RateLimit-Limit"] = str(_rate_limiter.requests_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(int(_rate_limiter.buckets[client_ip].tokens))

    return response
