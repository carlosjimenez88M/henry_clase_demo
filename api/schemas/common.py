"""Common Pydantic schemas used across the API."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response format."""

    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: Optional[str] = Field(None, description="Error timestamp")

    model_config = {"json_schema_extra": {"example": {
        "error": "Validation Error",
        "detail": "Query cannot be empty",
        "status_code": 400,
        "timestamp": "2026-01-22T10:30:45Z"
    }}}


class SuccessResponse(BaseModel):
    """Standard success response format."""

    message: str = Field(..., description="Success message")
    data: Optional[dict[str, Any]] = Field(None, description="Response data")
    timestamp: Optional[str] = Field(None, description="Response timestamp")

    model_config = {"json_schema_extra": {"example": {
        "message": "Operation completed successfully",
        "data": {"id": "123"},
        "timestamp": "2026-01-22T10:30:45Z"
    }}}


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")
    checks: Optional[dict[str, Any]] = Field(None, description="Component health checks")

    model_config = {"json_schema_extra": {"example": {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": "2026-01-22T10:30:45Z",
        "checks": {
            "database": "ok",
            "openai": "ok"
        }
    }}}
