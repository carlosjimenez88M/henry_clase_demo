"""
Security Headers Middleware.

Adds security headers to all responses and implements request timeout.
"""

import asyncio
from fastapi import Request
from fastapi.responses import JSONResponse
from api.core.logger import logger


async def security_headers_middleware(request: Request, call_next):
    """
    Add security headers to all responses.

    Args:
        request: FastAPI request
        call_next: Next middleware/handler

    Returns:
        Response with security headers
    """
    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    return response


async def timeout_middleware(request: Request, call_next):
    """
    Implement request timeout (60 seconds).

    Args:
        request: FastAPI request
        call_next: Next middleware/handler

    Returns:
        Response or timeout error
    """
    try:
        # 60 second timeout for all requests
        response = await asyncio.wait_for(call_next(request), timeout=60.0)
        return response
    except asyncio.TimeoutError:
        logger.error(f"Request timeout: {request.url.path}")
        return JSONResponse(
            status_code=504,
            content={
                "error": "Gateway Timeout",
                "detail": "Request took too long to process (>60s)",
                "status_code": 504
            }
        )
    except Exception as e:
        logger.error(f"Timeout middleware error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(e),
                "status_code": 500
            }
        )
