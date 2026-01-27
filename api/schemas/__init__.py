"""Pydantic schemas for API request/response models."""

from api.schemas.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
    MetricsData,
    ModelInfo,
    ReasoningStep,
)
from api.schemas.common import ErrorResponse, SuccessResponse
from api.schemas.comparison import (
    ComparisonRequest,
    ComparisonResponse,
    ComparisonResult,
    ModelMetricsSummary,
)
from api.schemas.database import (
    DatabaseStats,
    SongListResponse,
    SongResponse,
    SongSearchRequest,
)

__all__ = [
    # Common
    "ErrorResponse",
    "SuccessResponse",
    # Agent
    "AgentQueryRequest",
    "AgentQueryResponse",
    "ReasoningStep",
    "MetricsData",
    "ModelInfo",
    # Database
    "SongResponse",
    "SongSearchRequest",
    "SongListResponse",
    "DatabaseStats",
    # Comparison
    "ComparisonRequest",
    "ComparisonResponse",
    "ModelMetricsSummary",
    "ComparisonResult",
]
