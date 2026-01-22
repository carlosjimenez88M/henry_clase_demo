"""Model comparison endpoints."""

from fastapi import APIRouter, HTTPException, Depends

from api.schemas.comparison import (
    ComparisonRequest,
    ComparisonResponse,
    ComparisonListResponse
)
from api.services.comparison_service import ComparisonService
from api.core.logger import logger

router = APIRouter()


def get_comparison_service():
    """Dependency to get comparison service instance."""
    return ComparisonService()


@router.post("/comparison/run", response_model=ComparisonResponse, tags=["Comparison"])
async def run_comparison(
    request: ComparisonRequest,
    service: ComparisonService = Depends(get_comparison_service)
):
    """
    Run performance comparison between multiple AI models.

    Executes the same test queries across different models and compares:
    - **Success rate**: Percentage of queries answered correctly
    - **Execution time**: Average time per query
    - **Cost**: Total and average cost per query
    - **Tool usage**: Which tools each model uses

    **Example request:**
    ```json
    {
      "models": ["gpt-4o-mini", "gpt-4o"],
      "verbose": true
    }
    ```

    Set `verbose: true` to include detailed results for each test case.
    """
    try:
        result = await service.run_comparison(
            models=request.models,
            test_cases=[tc.model_dump() for tc in request.test_cases] if request.test_cases else None,
            verbose=request.verbose
        )

        return ComparisonResponse(**result)

    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}"
        )


@router.get("/comparison/{comparison_id}", response_model=ComparisonResponse, tags=["Comparison"])
async def get_comparison_result(
    comparison_id: str,
    service: ComparisonService = Depends(get_comparison_service)
):
    """
    Get comparison result by ID.

    Retrieves the complete results of a previous comparison including:
    - Summary metrics for each model
    - Detailed results (if comparison was run with verbose=true)
    - Winner analysis
    """
    try:
        result = service.get_comparison(comparison_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Comparison {comparison_id} not found"
            )

        return ComparisonResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get comparison: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve comparison: {str(e)}"
        )


@router.get("/comparison/list", response_model=ComparisonListResponse, tags=["Comparison"])
async def list_comparisons(
    limit: int = 50,
    service: ComparisonService = Depends(get_comparison_service)
):
    """
    List recent comparisons.

    Returns a summary of recent model comparisons.
    Use the comparison ID to retrieve full details.
    """
    try:
        result = service.list_comparisons(limit=limit)
        return ComparisonListResponse(**result)

    except Exception as e:
        logger.error(f"Failed to list comparisons: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve comparison list: {str(e)}"
        )
