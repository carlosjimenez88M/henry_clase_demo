"""Pydantic schemas for Model Comparison API endpoints."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    """Test case for model comparison."""

    query: str = Field(..., description="Test query")
    expected_tool: Optional[str] = Field(None, description="Expected tool to use")
    category: Optional[str] = Field(None, description="Test category")

    model_config = {"json_schema_extra": {"example": {
        "query": "Find melancholic Pink Floyd songs",
        "expected_tool": "pink_floyd_database",
        "category": "database_search"
    }}}


class ComparisonRequest(BaseModel):
    """Request schema for running model comparison."""

    models: list[str] = Field(
        ...,
        min_length=2,
        max_length=5,
        description="Models to compare"
    )
    test_cases: Optional[list[TestCase]] = Field(
        None,
        description="Custom test cases (uses defaults if not provided)"
    )
    verbose: bool = Field(default=False, description="Include detailed execution traces")

    model_config = {"json_schema_extra": {"example": {
        "models": ["gpt-4o-mini", "gpt-4o"],
        "test_cases": [
            {
                "query": "Find melancholic songs",
                "expected_tool": "pink_floyd_database"
            }
        ],
        "verbose": False
    }}}


class ModelMetricsSummary(BaseModel):
    """Summary metrics for a single model in comparison."""

    model: str = Field(..., description="Model name")
    total_queries: int = Field(..., description="Total queries executed")
    success_rate: float = Field(..., description="Success rate (0-1)")
    avg_execution_time: float = Field(..., description="Average execution time (seconds)")
    total_cost_usd: float = Field(..., description="Total estimated cost")
    avg_steps: float = Field(..., description="Average reasoning steps")
    tool_usage: dict[str, int] = Field(..., description="Tool usage counts")

    model_config = {"json_schema_extra": {"example": {
        "model": "gpt-4o-mini",
        "total_queries": 10,
        "success_rate": 0.9,
        "avg_execution_time": 2.34,
        "total_cost_usd": 0.014,
        "avg_steps": 3.2,
        "tool_usage": {
            "pink_floyd_database": 8,
            "currency_converter": 2
        }
    }}}


class ComparisonResult(BaseModel):
    """Detailed comparison result for a single test case."""

    test_case: str = Field(..., description="Test query")
    results: dict[str, Any] = Field(..., description="Results per model")
    winner: Optional[str] = Field(None, description="Best performing model")

    model_config = {"json_schema_extra": {"example": {
        "test_case": "Find melancholic songs",
        "results": {
            "gpt-4o-mini": {
                "success": True,
                "execution_time": 2.1,
                "cost": 0.0012
            },
            "gpt-4o": {
                "success": True,
                "execution_time": 3.5,
                "cost": 0.0089
            }
        },
        "winner": "gpt-4o-mini"
    }}}


class ComparisonResponse(BaseModel):
    """Response schema for model comparison results."""

    comparison_id: str = Field(..., description="Unique comparison ID")
    models: list[str] = Field(..., description="Models compared")
    summary: dict[str, ModelMetricsSummary] = Field(..., description="Summary per model")
    detailed_results: Optional[list[ComparisonResult]] = Field(
        None,
        description="Detailed results (if verbose=True)"
    )
    timestamp: str = Field(..., description="Comparison timestamp")
    total_duration: float = Field(..., description="Total comparison duration (seconds)")

    model_config = {"json_schema_extra": {"example": {
        "comparison_id": "550e8400-e29b-41d4-a716-446655440000",
        "models": ["gpt-4o-mini", "gpt-4o"],
        "summary": {
            "gpt-4o-mini": {
                "model": "gpt-4o-mini",
                "total_queries": 10,
                "success_rate": 0.9,
                "avg_execution_time": 2.34,
                "total_cost_usd": 0.014,
                "avg_steps": 3.2,
                "tool_usage": {"pink_floyd_database": 8}
            }
        },
        "timestamp": "2026-01-22T10:30:45Z",
        "total_duration": 45.6
    }}}


class ComparisonListResponse(BaseModel):
    """Response schema for listing past comparisons."""

    total: int = Field(..., description="Total number of comparisons")
    comparisons: list[dict[str, Any]] = Field(..., description="Comparison summaries")

    model_config = {"json_schema_extra": {"example": {
        "total": 5,
        "comparisons": [
            {
                "comparison_id": "550e8400-e29b-41d4-a716-446655440000",
                "models": ["gpt-4o-mini", "gpt-4o"],
                "timestamp": "2026-01-22T10:30:45Z"
            }
        ]
    }}}
