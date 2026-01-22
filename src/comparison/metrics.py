"""
Metrics calculation for model comparison.

This module provides utilities for calculating and analyzing performance metrics
across different models.
"""

from typing import Dict, List, Any
import statistics


class MetricsCalculator:
    """Calculator for model performance metrics."""

    @staticmethod
    def calculate_execution_metrics(results: List[Dict]) -> Dict[str, Any]:
        """
        Calculate aggregate metrics from execution results.

        Args:
            results: List of execution results

        Returns:
            Dictionary with aggregate metrics
        """
        if not results:
            return {}

        # Extract metrics
        execution_times = [r["metrics"]["execution_time_seconds"] for r in results]
        token_counts = [r["metrics"]["estimated_tokens"]["total"] for r in results]
        costs = [r["metrics"]["estimated_cost_usd"] for r in results]
        num_steps = [r["metrics"]["num_steps"] for r in results]

        # Calculate statistics
        metrics = {
            "num_queries": len(results),
            "execution_time": {
                "total": round(sum(execution_times), 2),
                "mean": round(statistics.mean(execution_times), 2),
                "median": round(statistics.median(execution_times), 2),
                "min": round(min(execution_times), 2),
                "max": round(max(execution_times), 2),
                "stdev": round(statistics.stdev(execution_times), 2) if len(execution_times) > 1 else 0,
            },
            "tokens": {
                "total": sum(token_counts),
                "mean": int(statistics.mean(token_counts)),
                "median": int(statistics.median(token_counts)),
                "min": min(token_counts),
                "max": max(token_counts),
            },
            "cost": {
                "total": round(sum(costs), 6),
                "mean": round(statistics.mean(costs), 6),
                "median": round(statistics.median(costs), 6),
                "min": round(min(costs), 6),
                "max": round(max(costs), 6),
            },
            "steps": {
                "mean": round(statistics.mean(num_steps), 1),
                "median": statistics.median(num_steps),
                "min": min(num_steps),
                "max": max(num_steps),
            }
        }

        return metrics

    @staticmethod
    def calculate_success_rate(results: List[Dict]) -> float:
        """
        Calculate success rate (queries that got an answer).

        Args:
            results: List of execution results

        Returns:
            Success rate as percentage (0-100)
        """
        if not results:
            return 0.0

        successful = sum(
            1 for r in results
            if r["answer"] and "error" not in r["answer"].lower()
        )

        return round((successful / len(results)) * 100, 1)

    @staticmethod
    def compare_models(model_results: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Compare metrics across multiple models.

        Args:
            model_results: Dictionary mapping model names to their results

        Returns:
            Comparison summary
        """
        comparison = {}

        for model_name, results in model_results.items():
            metrics = MetricsCalculator.calculate_execution_metrics(results)
            success_rate = MetricsCalculator.calculate_success_rate(results)

            comparison[model_name] = {
                "metrics": metrics,
                "success_rate": success_rate,
                "num_queries": len(results),
            }

        # Find best model for each metric
        if comparison:
            comparison["best"] = {
                "fastest": min(
                    comparison.items(),
                    key=lambda x: x[1]["metrics"]["execution_time"]["mean"]
                )[0],
                "cheapest": min(
                    comparison.items(),
                    key=lambda x: x[1]["metrics"]["cost"]["total"]
                )[0],
                "most_successful": max(
                    comparison.items(),
                    key=lambda x: x[1]["success_rate"]
                )[0],
            }

        return comparison

    @staticmethod
    def export_to_dict(metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Export metrics to a serializable dictionary."""
        return metrics
