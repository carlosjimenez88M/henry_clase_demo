"""
Custom exception classes for the API.

All exceptions inherit from APIError for consistent error handling.
"""

from typing import Any, Optional


class APIError(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class DatabaseError(APIError):
    """Database operation failed."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class ModelError(APIError):
    """AI model operation failed."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class ToolError(APIError):
    """Tool execution failed."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=500, details=details)


class ValidationError(APIError):
    """Request validation failed."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(APIError):
    """Resource not found."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=404, details=details)


class AuthenticationError(APIError):
    """Authentication failed."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=401, details=details)


class RateLimitError(APIError):
    """Rate limit exceeded."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(message, status_code=429, details=details)
