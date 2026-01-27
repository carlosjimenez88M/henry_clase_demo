"""Comparison service for model performance evaluation."""

import uuid
from datetime import UTC, datetime
from typing import Any

from api.core.errors import ModelError
from api.core.logger import logger
from src.comparison.evaluator import ModelEvaluator
from src.comparison.test_cases import get_all_test_cases


class ComparisonService:
    """Service for managing model comparisons."""

    def __init__(self):
        """Initialize comparison service."""
        self.comparison_history: dict[str, dict[str, Any]] = {}
        logger.info("ComparisonService initialized")

    async def run_comparison(
        self,
        models: list[str],
        test_cases: list[dict[str, Any]] | None = None,
        verbose: bool = False,
    ) -> dict[str, Any]:
        """
        Run comparison between multiple models.

        Args:
            models: List of model names to compare
            test_cases: Optional custom test cases
            verbose: Whether to include detailed traces

        Returns:
            Comparison results with summary and detailed results

        Raises:
            ModelError: If comparison fails
        """
        comparison_id = str(uuid.uuid4())

        try:
            logger.info(
                f"Starting comparison of {len(models)} models: {', '.join(models)}"
            )

            # Convert test_cases if provided
            formatted_test_cases = None
            if test_cases:
                formatted_test_cases = [
                    {
                        "query": tc.get("query"),
                        "expected_tool": tc.get("expected_tool"),
                        "category": tc.get("category"),
                    }
                    for tc in test_cases
                ]
            else:
                formatted_test_cases = get_all_test_cases()

            # Create evaluator
            evaluator = ModelEvaluator(models)

            # Run evaluation
            start_time = datetime.now(UTC)
            results = evaluator.run_evaluation(
                test_cases=formatted_test_cases, verbose=False  # Use our own logging
            )
            end_time = datetime.now(UTC)

            # Calculate comparison metrics
            comparison_data = evaluator.calculate_comparison()

            # Build summary for each model
            summary = {}
            for model_name in models:
                if model_name in comparison_data:
                    model_data = comparison_data[model_name]
                    metrics = model_data.get("metrics", {})

                    # Extract tool usage from results
                    tool_usage: dict[str, int] = {}
                    if model_name in results:
                        for result in results[model_name]:
                            tools = result.get("metrics", {}).get("tools_used", [])
                            for tool in tools:
                                tool_usage[tool] = tool_usage.get(tool, 0) + 1

                    summary[model_name] = {
                        "model": model_name,
                        "total_queries": model_data.get("num_queries", 0),
                        "success_rate": model_data.get("success_rate", 0) / 100.0,
                        "avg_execution_time": metrics.get("execution_time", {}).get(
                            "mean", 0
                        ),
                        "total_cost_usd": metrics.get("cost", {}).get("total", 0),
                        "avg_steps": metrics.get("steps", {}).get("mean", 0),
                        "tool_usage": tool_usage,
                    }

            # Build detailed results if verbose
            detailed_results = None
            if verbose:
                detailed_results = []
                # Get all test cases
                test_queries = [tc["query"] for tc in formatted_test_cases]

                for i, query in enumerate(test_queries):
                    result_entry: dict[str, Any] = {"test_case": query, "results": {}}

                    # Get results for each model
                    for model_name in models:
                        if model_name in results and i < len(results[model_name]):
                            model_result = results[model_name][i]
                            result_entry["results"][model_name] = {
                                "success": "Error"
                                not in model_result.get("answer", ""),
                                "execution_time": model_result.get("metrics", {}).get(
                                    "execution_time_seconds", 0
                                ),
                                "cost": model_result.get("metrics", {}).get(
                                    "estimated_cost_usd", 0
                                ),
                                "answer": model_result.get("answer", "")[:200],
                            }

                    detailed_results.append(result_entry)

            # Build final response
            total_duration = (end_time - start_time).total_seconds()

            comparison_result = {
                "comparison_id": comparison_id,
                "models": models,
                "summary": summary,
                "detailed_results": detailed_results,
                "timestamp": datetime.now(UTC).isoformat(),
                "total_duration": round(total_duration, 2),
            }

            # Store in history
            self.comparison_history[comparison_id] = comparison_result

            logger.success(
                f"Comparison completed: {comparison_id} "
                f"({total_duration:.2f}s, {len(formatted_test_cases)} tests)"
            )

            return comparison_result

        except Exception as e:
            logger.error(f"Comparison failed: {e}")
            raise ModelError(
                f"Model comparison failed: {str(e)}", details={"models": models}
            )

    def get_comparison(self, comparison_id: str) -> dict[str, Any] | None:
        """
        Get comparison result by ID.

        Args:
            comparison_id: Comparison ID

        Returns:
            Comparison result or None if not found
        """
        return self.comparison_history.get(comparison_id)

    def list_comparisons(self, limit: int = 50) -> dict[str, Any]:
        """
        List recent comparisons.

        Args:
            limit: Maximum number of comparisons to return

        Returns:
            Dictionary with comparison summaries
        """
        comparisons = []
        for comp_id, result in list(self.comparison_history.items())[-limit:]:
            comparisons.append(
                {
                    "comparison_id": comp_id,
                    "models": result.get("models", []),
                    "timestamp": result.get("timestamp", ""),
                    "total_duration": result.get("total_duration", 0),
                }
            )

        return {
            "total": len(self.comparison_history),
            "comparisons": list(reversed(comparisons)),
        }

    def clear_history(self) -> None:
        """Clear comparison history."""
        self.comparison_history.clear()
        logger.info("Comparison history cleared")
