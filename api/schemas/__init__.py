"""Pydantic schemas for API request/response models."""

from api.schemas.common import ErrorResponse, SuccessResponse
from api.schemas.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
    ReasoningStep,
    MetricsData,
    ModelInfo,
)
from api.schemas.database import (
    SongResponse,
    SongSearchRequest,
    SongListResponse,
    DatabaseStats,
)
from api.schemas.comparison import (
    ComparisonRequest,
    ComparisonResponse,
    ModelMetricsSummary,
    ComparisonResult,
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
