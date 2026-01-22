"""
History Manager for Dashboard.

Manages persistent query history using the API's ExecutionStore.
"""

import os
import httpx
from typing import List, Dict, Any, Optional


class HistoryManager:
    """
    Manages query history by communicating with the API.

    Features:
    - Fetches history from API's persistent storage
    - Caches locally in session for performance
    - Export capabilities
    """

    def __init__(self, api_url: Optional[str] = None):
        """
        Initialize history manager.

        Args:
            api_url: API base URL (defaults to environment variable or localhost)
        """
        self.api_url = api_url or os.getenv("API_URL", "http://localhost:8000")

    def get_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent execution history from API.

        Args:
            limit: Maximum number of executions to retrieve

        Returns:
            List of execution summary dictionaries
        """
        try:
            response = httpx.get(
                f"{self.api_url}/api/v1/agent/history",
                params={"limit": limit},
                timeout=10.0
            )

            if response.status_code == 200:
                data = response.json()
                return data.get("executions", [])
            else:
                return []

        except Exception as e:
            print(f"Error fetching history: {e}")
            return []

    def get_execution_detail(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed execution result by ID.

        Args:
            execution_id: Execution ID

        Returns:
            Full execution result or None
        """
        try:
            response = httpx.get(
                f"{self.api_url}/api/v1/agent/history/{execution_id}",
                timeout=10.0
            )

            if response.status_code == 200:
                return response.json()
            else:
                return None

        except Exception as e:
            print(f"Error fetching execution detail: {e}")
            return None

    def search_history(
        self,
        query_text: Optional[str] = None,
        model: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Search history with filters.

        Args:
            query_text: Filter by query text
            model: Filter by model name
            limit: Maximum results

        Returns:
            Filtered execution list
        """
        history = self.get_history(limit)

        # Apply filters
        if query_text:
            history = [
                h for h in history
                if query_text.lower() in h.get("query", "").lower()
            ]

        if model:
            history = [
                h for h in history
                if h.get("model") == model
            ]

        return history

    def export_to_csv(self, history: List[Dict[str, Any]], filename: str = "history_export.csv"):
        """
        Export history to CSV file.

        Args:
            history: List of execution summaries
            filename: Output filename
        """
        import csv

        if not history:
            return

        # Define columns
        columns = ["execution_id", "query", "model", "agent_type", "execution_time", "estimated_cost", "timestamp"]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()

            for item in history:
                row = {col: item.get(col, "") for col in columns}
                writer.writerow(row)

    def get_statistics(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate statistics from history.

        Args:
            history: List of execution summaries

        Returns:
            Statistics dictionary
        """
        if not history:
            return {
                "total_queries": 0,
                "avg_execution_time": 0,
                "total_cost": 0,
                "models_used": []
            }

        total_time = sum(h.get("execution_time", 0) for h in history)
        total_cost = sum(h.get("estimated_cost", 0) for h in history)
        models = list(set(h.get("model", "unknown") for h in history))

        return {
            "total_queries": len(history),
            "avg_execution_time": round(total_time / len(history), 2) if history else 0,
            "total_cost": round(total_cost, 6),
            "models_used": models
        }
