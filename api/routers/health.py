"""Health check endpoints."""

from datetime import datetime, timezone
from fastapi import APIRouter
from pathlib import Path

from api.schemas.common import HealthResponse
from api.core.config import get_settings
from api.core.logger import logger

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Basic health check endpoint.

    Returns service status and version information.
    """
    settings = get_settings()

    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get("/health/ready", response_model=HealthResponse, tags=["Health"])
async def readiness_check():
    """
    Readiness probe endpoint.

    Checks if the service is ready to accept requests by verifying
    database connectivity and external API availability.
    """
    settings = get_settings()
    checks = {}

    # Check database
    try:
        db_path = Path(settings.database_path)
        if db_path.exists():
            checks["database"] = "ok"
        else:
            checks["database"] = "not_found"
    except Exception as e:
        logger.error(f"Database check failed: {e}")
        checks["database"] = "error"

    # Check OpenAI API key
    if settings.openai_api_key:
        checks["openai_key"] = "configured"
    else:
        checks["openai_key"] = "missing"

    # Determine overall status
    status = "ready" if all(v in ["ok", "configured"] for v in checks.values()) else "not_ready"

    return HealthResponse(
        status=status,
        version=settings.api_version,
        timestamp=datetime.now(timezone.utc).isoformat(),
        checks=checks
    )


@router.get("/health/live", response_model=HealthResponse, tags=["Health"])
async def liveness_check():
    """
    Liveness probe endpoint.

    Simple endpoint to verify the service is alive and responding.
    """
    settings = get_settings()

    return HealthResponse(
        status="alive",
        version=settings.api_version,
        timestamp=datetime.now(timezone.utc).isoformat()
    )
