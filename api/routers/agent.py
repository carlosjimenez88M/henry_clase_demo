"""Agent endpoints for query execution."""

from fastapi import APIRouter, Depends, HTTPException

from api.core.logger import logger
from api.schemas.agent import (
    AgentQueryRequest,
    AgentQueryResponse,
    ExecutionHistoryResponse,
    ModelInfo,
)
from api.services.agent_service import AgentService

router = APIRouter()


def get_agent_service():
    """Dependency to get agent service instance."""
    return AgentService()


@router.post("/agent/query", response_model=AgentQueryResponse, tags=["Agent"])
async def execute_agent_query(
    request: AgentQueryRequest, service: AgentService = Depends(get_agent_service)
):
    """
    Execute a query with the AI agent.

    The agent uses the ReAct framework to reason through the query,
    selecting and using tools (Pink Floyd database, currency converter)
    as needed to provide an accurate answer.

    **Example queries:**
    - "Find melancholic Pink Floyd songs from the 1970s"
    - "What albums were released in 1973?"
    - "Convert 100 USD to EUR"
    """
    try:
        result = await service.execute_query(
            query=request.query,
            model=request.model,
            temperature=request.temperature,
            max_iterations=request.max_iterations,
        )

        return AgentQueryResponse(**result)

    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")


@router.get("/agent/models", response_model=list[ModelInfo], tags=["Agent"])
async def get_available_models(service: AgentService = Depends(get_agent_service)):
    """
    Get list of available AI models.

    Returns information about each model including:
    - Name and display name
    - Maximum context tokens
    - Pricing per 1K tokens
    - Description and capabilities
    """
    try:
        model_names = service.get_available_models()
        models = [service.get_model_info(name) for name in model_names]

        return [ModelInfo(**model) for model in models if model]

    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve models: {str(e)}"
        )


@router.get("/agent/history", response_model=ExecutionHistoryResponse, tags=["Agent"])
async def get_execution_history(
    limit: int = 50, service: AgentService = Depends(get_agent_service)
):
    """
    Get execution history.

    Returns a list of recent query executions with summary information.
    Use the execution ID to retrieve full details via /agent/history/{id}.
    """
    try:
        executions = service.get_execution_history(limit=limit)

        return ExecutionHistoryResponse(total=len(executions), executions=executions)

    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve history: {str(e)}"
        )


@router.get(
    "/agent/history/{execution_id}", response_model=AgentQueryResponse, tags=["Agent"]
)
async def get_execution_detail(
    execution_id: str, service: AgentService = Depends(get_agent_service)
):
    """
    Get detailed execution result by ID.

    Returns the complete execution details including:
    - Full reasoning trace
    - Tool usage
    - Performance metrics
    - Cost estimates
    """
    try:
        result = service.get_execution_detail(execution_id)

        if not result:
            raise HTTPException(
                status_code=404, detail=f"Execution {execution_id} not found"
            )

        return AgentQueryResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get execution detail: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve execution: {str(e)}"
        )
