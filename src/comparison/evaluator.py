"""
Model comparison evaluator.

This module runs test queries across multiple models and compares their performance.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

from src.agents.agent_factory import AgentFactory
from src.agents.agent_executor import AgentExecutor
from src.comparison.metrics import MetricsCalculator
from src.comparison.test_cases import get_all_test_cases


class ModelEvaluator:
    """Evaluator for comparing multiple models."""

    def __init__(self, models: List[str]):
        """
        Initialize evaluator with models to test.

        Args:
            models: List of model names to evaluate
        """
        self.models = models
        self.factory = AgentFactory()
        self.results = {}

    def run_evaluation(
        self,
        test_cases: List[Dict[str, Any]] = None,
        verbose: bool = True
    ) -> Dict[str, List[Dict]]:
        """
        Run evaluation across all models.

        Args:
            test_cases: Optional custom test cases (uses default if None)
            verbose: Whether to print progress

        Returns:
            Dictionary mapping model names to their results
        """
        if test_cases is None:
            test_cases = get_all_test_cases()

        if verbose:
            print(f" Starting evaluation with {len(test_cases)} test cases")
            print(f" Models: {', '.join(self.models)}\n")

        for model_name in self.models:
            if verbose:
                print(f"Testing model: {model_name}")
                print("-" * 60)

            # Create agent and executor
            try:
                agent = self.factory.create_agent(model_name)
                executor = AgentExecutor(agent, model_name)

                model_results = []

                for i, test_case in enumerate(test_cases, 1):
                    query = test_case["query"]

                    if verbose:
                        print(f"  [{i}/{len(test_cases)}] {query[:50]}...", end=" ")

                    try:
                        result = executor.execute(query)
                        result["test_case"] = test_case
                        model_results.append(result)

                        if verbose:
                            time_taken = result["metrics"]["execution_time_seconds"]
                            print(f" ({time_taken}s)")

                    except Exception as e:
                        if verbose:
                            print(f" Error: {e}")
                        model_results.append({
                            "query": query,
                            "answer": f"Error: {e}",
                            "test_case": test_case,
                            "metrics": {
                                "model": model_name,
                                "execution_time_seconds": 0,
                                "estimated_tokens": {"total": 0},
                                "estimated_cost_usd": 0,
                                "num_steps": 0,
                            }
                        })

                self.results[model_name] = model_results

                if verbose:
                    print()

            except Exception as e:
                if verbose:
                    print(f" Failed to create agent for {model_name}: {e}\n")
                self.results[model_name] = []

        return self.results

    def calculate_comparison(self) -> Dict[str, Any]:
        """
        Calculate comparison metrics across all models.

        Returns:
            Comparison summary
        """
        return MetricsCalculator.compare_models(self.results)

    def save_results(self, output_path: Path) -> None:
        """
        Save results to JSON file.

        Args:
            output_path: Path to save results
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Prepare data for JSON serialization
        data = {
            "timestamp": datetime.now().isoformat(),
            "models": self.models,
            "results": {},
            "comparison": self.calculate_comparison()
        }

        # Convert results to serializable format
        for model_name, results in self.results.items():
            serializable_results = []
            for result in results:
                serializable_result = {
                    "query": result["query"],
                    "answer": result["answer"],
                    "metrics": result["metrics"],
                    "test_case": result.get("test_case", {}),
                    "reasoning_trace": result.get("reasoning_trace", [])
                }
                serializable_results.append(serializable_result)

            data["results"][model_name] = serializable_results

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n Results saved to: {output_path}")

    def print_summary(self) -> None:
        """Print comparison summary."""
        comparison = self.calculate_comparison()

        print("\n" + "="*70)
        print("COMPARISON SUMMARY")
        print("="*70)

        for model_name in self.models:
            if model_name not in comparison:
                continue

            model_data = comparison[model_name]
            metrics = model_data["metrics"]

            print(f"\n{model_name}")
            print("-" * 70)
            print(f"  Queries: {model_data['num_queries']}")
            print(f"  Success Rate: {model_data['success_rate']}%")
            print(f"  Avg Time: {metrics['execution_time']['mean']}s")
            print(f"  Total Tokens: {metrics['tokens']['total']}")
            print(f"  Total Cost: ${metrics['cost']['total']}")

        if "best" in comparison:
            print("\n" + "="*70)
            print("WINNERS")
            print("="*70)
            print(f"   Fastest: {comparison['best']['fastest']}")
            print(f"   Cheapest: {comparison['best']['cheapest']}")
            print(f"   Most Successful: {comparison['best']['most_successful']}")

        print("\n" + "="*70)
