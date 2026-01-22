"""
Agent Executor with metrics tracking.

This module provides an executor for running agents with performance metrics,
token counting, and cost estimation. Supports both standard ReAct and CoT agents.
"""

import time
import asyncio
from typing import Dict, Optional, Union, Any

from src.agents.react_agent import run_agent
from src.agents.cot_agent import CoTReActAgent, run_cot_agent


class AgentExecutor:
    """Executor for running agents with metrics tracking."""

    # Approximate pricing (per 1M tokens)
    MODEL_PRICING = {
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-5-nano": {"input": 0.10, "output": 0.40},  # Estimated
    }

    def __init__(self, agent: Union[Any, CoTReActAgent], model_name: str):
        """
        Initialize agent executor.

        Args:
            agent: Agent instance (standard ReAct or CoT agent)
            model_name: Name of the model being used
        """
        self.agent = agent
        self.model_name = model_name
        self.execution_history = []
        self.is_cot_agent = isinstance(agent, CoTReActAgent)

    def execute(self, query: str) -> Dict:
        """
        Execute a query through the agent and track metrics.

        Args:
            query: User query string

        Returns:
            Dictionary with answer, metrics, and reasoning trace
        """
        # Start timing
        start_time = time.time()

        # Run appropriate agent type
        if self.is_cot_agent:
            # CoT agents are async, so we need to run in event loop
            result = asyncio.run(run_cot_agent(self.agent, query))
        else:
            # Standard ReAct agent (sync)
            result = run_agent(self.agent, query)

        # Calculate execution time
        execution_time = time.time() - start_time

        # Estimate tokens (rough approximation)
        tokens = self._estimate_tokens(query, result["answer"], result["reasoning_trace"])

        # Calculate cost
        cost = self._calculate_cost(tokens)

        # Build result with metrics
        execution_result = {
            "query": query,
            "answer": result["answer"],
            "reasoning_trace": result["reasoning_trace"],
            "metrics": {
                "model": self.model_name,
                "execution_time_seconds": round(execution_time, 2),
                "estimated_tokens": tokens,
                "estimated_cost_usd": cost,
                "num_steps": len(result["reasoning_trace"]),
                "agent_type": "cot" if self.is_cot_agent else "react"
            },
            "raw_messages": result.get("raw_messages", [])
        }

        # Add CoT-specific metadata if available
        if "metadata" in result:
            execution_result["metadata"] = result["metadata"]

        # Store in history
        self.execution_history.append(execution_result)

        return execution_result

    def _estimate_tokens(self, query: str, answer: str, trace: list) -> Dict[str, int]:
        """
        Estimate token usage (rough approximation).

        Uses simple heuristic: ~4 characters per token on average.
        This is not exact but good enough for demos.

        Args:
            query: Input query
            answer: Output answer
            trace: Reasoning trace

        Returns:
            Dictionary with input/output/total tokens
        """
        # Count characters in query and trace
        input_chars = len(query)
        for step in trace:
            if step["type"] in ["query", "action", "observation"]:
                input_chars += len(str(step.get("content", "")))

        # Count characters in answer
        output_chars = len(answer)

        # Rough conversion: 4 chars �� 1 token
        input_tokens = input_chars // 4
        output_tokens = output_chars // 4
        total_tokens = input_tokens + output_tokens

        return {
            "input": input_tokens,
            "output": output_tokens,
            "total": total_tokens
        }

    def _calculate_cost(self, tokens: Dict[str, int]) -> float:
        """
        Calculate estimated cost based on token usage.

        Args:
            tokens: Dictionary with input/output/total tokens

        Returns:
            Estimated cost in USD
        """
        pricing = self.MODEL_PRICING.get(self.model_name)

        if not pricing:
            return 0.0

        # Cost per million tokens
        input_cost = (tokens["input"] / 1_000_000) * pricing["input"]
        output_cost = (tokens["output"] / 1_000_000) * pricing["output"]

        return round(input_cost + output_cost, 6)

    def get_history(self) -> list:
        """Get execution history."""
        return self.execution_history

    def get_last_result(self) -> Optional[Dict]:
        """Get last execution result."""
        if self.execution_history:
            return self.execution_history[-1]
        return None

    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history = []

    def get_metrics_summary(self) -> Dict:
        """Get summary of metrics across all executions."""
        if not self.execution_history:
            return {}

        total_time = sum(r["metrics"]["execution_time_seconds"] for r in self.execution_history)
        total_tokens = sum(r["metrics"]["estimated_tokens"]["total"] for r in self.execution_history)
        total_cost = sum(r["metrics"]["estimated_cost_usd"] for r in self.execution_history)

        return {
            "num_executions": len(self.execution_history),
            "total_time_seconds": round(total_time, 2),
            "avg_time_seconds": round(total_time / len(self.execution_history), 2),
            "total_tokens": total_tokens,
            "avg_tokens": total_tokens // len(self.execution_history),
            "total_cost_usd": round(total_cost, 6),
            "avg_cost_usd": round(total_cost / len(self.execution_history), 6),
        }
