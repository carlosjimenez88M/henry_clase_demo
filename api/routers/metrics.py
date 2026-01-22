"""System metrics endpoints."""

from fastapi import APIRouter
from typing import Any

router = APIRouter()


@router.get("/metrics/system", tags=["Metrics"])
async def get_system_metrics() -> dict[str, Any]:
    """
    Get system metrics.

    Returns basic system information and metrics.
    This endpoint can be extended to include:
    - Request count
    - Average response time
    - Error rate
    - Resource usage
    """
    # Placeholder for future metrics implementation
    return {
        "status": "ok",
        "message": "System metrics endpoint - to be implemented with prometheus/monitoring"
    }
