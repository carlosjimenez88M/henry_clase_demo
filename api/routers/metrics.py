"""System metrics endpoints."""

from typing import Any

from fastapi import APIRouter, Depends

from api.services.agent_service import AgentService

router = APIRouter()

# Singleton service instance
_agent_service = AgentService()


def get_agent_service() -> AgentService:
    """Get agent service instance."""
    return _agent_service


@router.get("/metrics/summary", tags=["Metrics"])
async def get_metrics_summary(
    service: AgentService = Depends(get_agent_service),
) -> dict[str, Any]:
    """
    Get summary metrics.

    Returns:
        Summary of agent usage, costs, and performance
    """
    storage_stats = service.get_storage_statistics()
    cache_stats = service.get_cache_statistics()

    return {"storage": storage_stats, "cache": cache_stats, "status": "ok"}


@router.get("/metrics/storage", tags=["Metrics"])
async def get_storage_metrics(
    service: AgentService = Depends(get_agent_service),
) -> dict[str, Any]:
    """
    Get storage statistics.

    Returns:
        Storage statistics including total executions, costs, tokens
    """
    return service.get_storage_statistics()


@router.get("/metrics/cache", tags=["Metrics"])
async def get_cache_metrics(
    service: AgentService = Depends(get_agent_service),
) -> dict[str, Any]:
    """
    Get cache statistics.

    Returns:
        Cache statistics including hit rate, size
    """
    return service.get_cache_statistics()


@router.get("/metrics/system", tags=["Metrics"])
async def get_system_metrics() -> dict[str, Any]:
    """
    Get system metrics.

    Returns basic system information and metrics.
    """
    return {"status": "ok", "message": "System metrics endpoint - available"}
