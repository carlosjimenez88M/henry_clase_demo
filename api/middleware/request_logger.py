"""Request logging middleware with colored output."""

import time

from fastapi import Request

from api.core.logger import log_error, log_success, logger


async def log_requests(request: Request, call_next):
    """
    Middleware to log all HTTP requests with colored output.

    Logs:
    - Incoming requests (method, path, client IP)
    - Response status and duration
    - Green for successful responses (2xx, 3xx)
    - Red for error responses (4xx, 5xx)
    """
    start_time = time.time()

    # Log incoming request
    logger.info(f"{request.method} {request.url.path} from {request.client.host}")

    try:
        # Process request
        response = await call_next(request)

        # Calculate duration
        duration = (time.time() - start_time) * 1000  # in milliseconds

        # Log response with color based on status
        if response.status_code < 400:
            log_success(
                f"{request.method} {request.url.path} "
                f"{response.status_code} ({duration:.2f}ms)"
            )
        else:
            log_error(
                f"{request.method} {request.url.path} "
                f"{response.status_code} ({duration:.2f}ms)"
            )

        return response

    except Exception as e:
        # Log exception
        duration = (time.time() - start_time) * 1000
        log_error(
            f"{request.method} {request.url.path} "
            f"ERROR: {str(e)} ({duration:.2f}ms)"
        )
        raise
