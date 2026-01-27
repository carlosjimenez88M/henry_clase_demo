"""Pydantic schemas for Agent API endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class AgentQueryRequest(BaseModel):
    """Request schema for agent query execution."""

    query: str = Field(..., min_length=1, max_length=2000, description="User query")
    model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    temperature: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Model temperature"
    )
    max_iterations: int = Field(
        default=5, ge=1, le=10, description="Max reasoning iterations"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "Find melancholic Pink Floyd songs from the 1970s",
                "model": "gpt-4o-mini",
                "temperature": 0.1,
                "max_iterations": 5,
            }
        }
    }


class ReasoningStep(BaseModel):
    """Single step in the agent's reasoning trace with CoT support."""

    step: int = Field(..., description="Step number")
    type: str = Field(
        ...,
        description="Step type: query, action, observation, thought, thinking, reflection, synthesis",
    )
    content: str | None = Field(None, description="Step content")
    tool: str | None = Field(None, description="Tool used (if action)")
    input: dict[str, Any] | None = Field(None, description="Tool input (if action)")
    output: str | None = Field(None, description="Tool output (if observation)")

    # CoT-specific fields
    understanding: str | None = Field(
        None, description="Understanding of the problem (CoT)"
    )
    plan: str | None = Field(None, description="Planned approach (CoT)")
    confidence: str | None = Field(
        None, description="Confidence level: HIGH/MEDIUM/LOW (CoT)"
    )
    alternatives: list[str] = Field(
        default_factory=list, description="Alternative approaches considered (CoT)"
    )
    assumptions: list[str] = Field(
        default_factory=list, description="Assumptions made (CoT)"
    )
    limitations: list[str] = Field(
        default_factory=list, description="Known limitations (CoT)"
    )
    timestamp: str | None = Field(None, description="Step timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "step": 1,
                "type": "thinking",
                "content": "I need to search for melancholic songs because...",
                "confidence": "HIGH",
                "alternatives": ["Search by album first", "Search by year"],
            }
        }
    }


class CoTMetadata(BaseModel):
    """Chain of Thought metadata."""

    agent_type: str = Field(default="react", description="Agent type: react or cot")
    temperature: float = Field(..., description="Model temperature used")
    iterations: int | None = Field(
        None, description="Number of iterations performed"
    )
    total_steps: int | None = Field(None, description="Total reasoning steps")
    confidence: str | None = Field(
        None, description="Overall confidence: HIGH/MEDIUM/LOW"
    )
    use_adaptive_prompt: bool | None = Field(
        None, description="Whether adaptive prompts were used"
    )
    max_iterations_reached: bool | None = Field(
        None, description="Whether max iterations was reached"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "agent_type": "cot",
                "temperature": 0.1,
                "iterations": 3,
                "total_steps": 7,
                "confidence": "HIGH",
                "use_adaptive_prompt": True,
            }
        }
    }


class MetricsData(BaseModel):
    """Execution metrics for an agent query."""

    model: str = Field(..., description="Model used")
    execution_time_seconds: float = Field(..., description="Total execution time")
    estimated_tokens: dict[str, int] = Field(..., description="Token usage estimates")
    estimated_cost_usd: float = Field(..., description="Estimated cost in USD")
    num_steps: int = Field(..., description="Number of reasoning steps")
    tools_used: list[str] = Field(default_factory=list, description="Tools used")
    agent_type: str = Field(default="react", description="Agent type used")

    model_config = {
        "json_schema_extra": {
            "example": {
                "model": "gpt-4o-mini",
                "execution_time_seconds": 2.34,
                "estimated_tokens": {"prompt": 500, "completion": 200, "total": 700},
                "estimated_cost_usd": 0.0014,
                "num_steps": 3,
                "tools_used": ["pink_floyd_database"],
                "agent_type": "cot",
            }
        }
    }


class AgentQueryResponse(BaseModel):
    """Response schema for agent query execution."""

    execution_id: str = Field(..., description="Unique execution ID")
    query: str = Field(..., description="Original query")
    answer: str = Field(..., description="Agent's final answer")
    reasoning_trace: list[ReasoningStep] = Field(
        ..., description="Step-by-step reasoning"
    )
    metrics: MetricsData = Field(..., description="Execution metrics")
    timestamp: str = Field(..., description="Execution timestamp")
    from_cache: bool = Field(
        default=False, description="Whether this result was served from cache"
    )
    metadata: CoTMetadata | None = Field(
        None, description="Chain of Thought metadata (if using CoT agent)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "execution_id": "550e8400-e29b-41d4-a716-446655440000",
                "query": "Find melancholic Pink Floyd songs",
                "answer": "Based on the Pink Floyd database, here are some melancholic songs...",
                "reasoning_trace": [
                    {
                        "step": 1,
                        "type": "thinking",
                        "content": "I need to search for melancholic songs",
                        "confidence": "HIGH",
                    }
                ],
                "metrics": {
                    "model": "gpt-4o-mini",
                    "execution_time_seconds": 2.34,
                    "estimated_tokens": {"total": 700},
                    "estimated_cost_usd": 0.0014,
                    "num_steps": 3,
                    "tools_used": ["pink_floyd_database"],
                    "agent_type": "cot",
                },
                "timestamp": "2026-01-22T10:30:45Z",
                "metadata": {
                    "agent_type": "cot",
                    "temperature": 0.1,
                    "confidence": "HIGH",
                },
            }
        }
    }


class ModelInfo(BaseModel):
    """Information about an available model."""

    name: str = Field(..., description="Model name")
    display_name: str = Field(..., description="Human-readable display name")
    description: str | None = Field(None, description="Model description")
    max_tokens: int = Field(..., description="Maximum context tokens")
    cost_per_1k_tokens: dict[str, float] = Field(..., description="Cost per 1K tokens")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "gpt-4o-mini",
                "display_name": "GPT-4o Mini",
                "description": "Fast and cost-effective model",
                "max_tokens": 128000,
                "cost_per_1k_tokens": {"prompt": 0.00015, "completion": 0.0006},
            }
        }
    }


class ExecutionHistoryResponse(BaseModel):
    """Response schema for execution history list."""

    total: int = Field(..., description="Total number of executions")
    executions: list[dict[str, Any]] = Field(..., description="Execution summaries")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 42,
                "executions": [
                    {
                        "execution_id": "550e8400-e29b-41d4-a716-446655440000",
                        "query": "Find melancholic songs",
                        "timestamp": "2026-01-22T10:30:45Z",
                        "model": "gpt-4o-mini",
                    }
                ],
            }
        }
    }
