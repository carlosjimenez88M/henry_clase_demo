"""Agent service for handling agent query execution."""

import uuid
from datetime import datetime
from typing import Any

from api.cache.query_cache import get_query_cache
from api.core.errors import ModelError
from api.core.logger import logger
from api.storage.execution_store import ExecutionStore
from src.agents.agent_executor import AgentExecutor
from src.agents.agent_factory import AgentFactory


class AgentService:
    """Service for managing agent query execution."""

    def __init__(self):
        """Initialize agent service."""
        self.factory = AgentFactory(
            default_agent_type="cot"
        )  # Use CoT agents by default
        self.execution_store = (
            ExecutionStore()
        )  # FIXED: Use persistent storage instead of dict
        self.query_cache = get_query_cache()  # Query cache for performance
        logger.info(
            "AgentService initialized with CoT agents, persistent storage, and caching"
        )

    async def execute_query(
        self, query: str, model: str, temperature: float, max_iterations: int
    ) -> dict[str, Any]:
        """
        Execute a query with the AI agent (with caching).

        Args:
            query: User query string
            model: Model name to use
            temperature: Model temperature
            max_iterations: Maximum reasoning iterations

        Returns:
            Execution result with answer, reasoning trace, and metrics

        Raises:
            ModelError: If model execution fails
        """
        # Check cache first
        cached_result = self.query_cache.get(query, model, temperature)
        if cached_result:
            logger.info(f"Cache HIT for query: {query[:50]}...")
            # Add new execution_id and timestamp for this cache hit
            cached_result["execution_id"] = str(uuid.uuid4())
            cached_result["timestamp"] = datetime.utcnow().isoformat() + "Z"
            cached_result["from_cache"] = True
            return cached_result

        execution_id = str(uuid.uuid4())

        try:
            logger.info(
                f"Cache MISS - Executing query with model={model}: {query[:50]}..."
            )

            # Create agent
            agent = self.factory.create_agent(model, temperature=temperature)

            # Create executor
            executor = AgentExecutor(agent, model)

            # Execute query
            result = await executor.execute(query)

            # Extract tools used from reasoning trace
            tools_used = []
            for step in result.get("reasoning_trace", []):
                if step.get("type") == "action" and step.get("tool"):
                    tool_name = step["tool"]
                    if tool_name not in tools_used:
                        tools_used.append(tool_name)

            # Add tools_used to metrics
            if "metrics" in result:
                result["metrics"]["tools_used"] = tools_used

            # Add execution metadata
            result["execution_id"] = execution_id
            result["timestamp"] = datetime.utcnow().isoformat() + "Z"
            result["from_cache"] = False

            # Cache the result for future queries
            self.query_cache.set(query, model, temperature, result.copy())

            # Store in persistent storage (FIXED: No more memory leak!)
            self.execution_store.save_execution(result)

            # Periodically cleanup old executions (every 100 queries)
            if int(execution_id.split("-")[0], 16) % 100 == 0:
                self.execution_store.cleanup_old_executions()

            logger.success(
                f"Query executed successfully: {execution_id} "
                f"({result['metrics']['execution_time_seconds']}s, "
                f"agent_type={result.get('metrics', {}).get('agent_type', 'unknown')})"
            )

            return result

        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            raise ModelError(
                f"Failed to execute query: {str(e)}",
                details={"model": model, "query": query[:100]},
            )

    def get_available_models(self) -> list[str]:
        """Get list of available models."""
        return self.factory.get_supported_models()

    def get_model_info(self, model_name: str) -> dict[str, Any]:
        """
        Get detailed information about a model.

        Args:
            model_name: Name of the model

        Returns:
            Model information dictionary
        """
        # Model metadata
        model_info_map = {
            "gpt-4o-mini": {
                "name": "gpt-4o-mini",
                "display_name": "GPT-4o Mini",
                "description": "Fast and cost-effective model for most tasks",
                "max_tokens": 128000,
                "cost_per_1k_tokens": {"prompt": 0.00015, "completion": 0.0006},
            },
            "gpt-4o": {
                "name": "gpt-4o",
                "display_name": "GPT-4o",
                "description": "Most capable model for complex reasoning",
                "max_tokens": 128000,
                "cost_per_1k_tokens": {"prompt": 0.0025, "completion": 0.01},
            },
            "gpt-5-nano": {
                "name": "gpt-5-nano",
                "display_name": "GPT-5 Nano",
                "description": "Experimental next-generation model",
                "max_tokens": 128000,
                "cost_per_1k_tokens": {"prompt": 0.0001, "completion": 0.0004},
            },
        }

        return model_info_map.get(model_name, {})

    def get_execution_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """
        Get execution history from persistent storage.

        Args:
            limit: Maximum number of executions to return

        Returns:
            List of execution summaries
        """
        return self.execution_store.get_recent_executions(limit)

    def get_execution_detail(self, execution_id: str) -> dict[str, Any] | None:
        """
        Get detailed execution result by ID from persistent storage.

        Args:
            execution_id: Execution ID

        Returns:
            Full execution result or None if not found
        """
        return self.execution_store.get_execution(execution_id)

    def clear_history(self) -> None:
        """Clear execution history from persistent storage."""
        self.execution_store.clear_all()
        logger.info("Execution history cleared from persistent storage")

    def get_storage_statistics(self) -> dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Storage statistics dictionary
        """
        return self.execution_store.get_statistics()

    def get_cache_statistics(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Cache statistics dictionary
        """
        return self.query_cache.get_statistics()
