"""
Execution Store for persistent storage of agent execution history.

Replaces unbounded in-memory dictionary with SQLite-backed storage
to prevent memory leaks and enable persistence across restarts.
"""

import sqlite3
import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from contextlib import contextmanager

from api.core.logger import logger


class ExecutionStore:
    """
    SQLite-backed storage for execution history.

    Features:
    - Persistent storage (survives restarts)
    - Automatic cleanup of old entries
    - Memory efficient (no unbounded growth)
    - Thread-safe with context managers
    """

    def __init__(self, db_path: str = "data/execution_history.db", retention_days: int = 30):
        """
        Initialize execution store.

        Args:
            db_path: Path to SQLite database file
            retention_days: Number of days to retain execution history
        """
        self.db_path = Path(db_path)
        self.retention_days = retention_days

        # Create data directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_db()

        logger.info(f"ExecutionStore initialized at {self.db_path}")

    def _init_db(self):
        """Initialize database schema."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Create executions table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS executions (
                execution_id TEXT PRIMARY KEY,
                query TEXT NOT NULL,
                answer TEXT NOT NULL,
                model TEXT NOT NULL,
                agent_type TEXT DEFAULT 'react',
                execution_time_seconds REAL NOT NULL,
                estimated_cost_usd REAL NOT NULL,
                total_tokens INTEGER NOT NULL,
                num_steps INTEGER NOT NULL,
                timestamp TEXT NOT NULL,
                reasoning_trace TEXT NOT NULL,
                metrics TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Create index on timestamp for faster queries
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp
            ON executions(timestamp)
            """)

            # Create index on model for analytics
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_model
            ON executions(model)
            """)

            conn.commit()
            logger.debug("ExecutionStore database schema initialized")

    @contextmanager
    def _get_connection(self):
        """Get database connection context manager."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def save_execution(self, execution_result: Dict[str, Any]) -> bool:
        """
        Save execution result to database.

        Args:
            execution_result: Full execution result dictionary

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Extract fields
                execution_id = execution_result.get("execution_id")
                query = execution_result.get("query", "")
                answer = execution_result.get("answer", "")
                timestamp = execution_result.get("timestamp", "")

                metrics = execution_result.get("metrics", {})
                model = metrics.get("model", "unknown")
                agent_type = metrics.get("agent_type", "react")
                execution_time = metrics.get("execution_time_seconds", 0.0)
                estimated_cost = metrics.get("estimated_cost_usd", 0.0)
                num_steps = metrics.get("num_steps", 0)

                # Calculate total tokens
                tokens = metrics.get("estimated_tokens", {})
                total_tokens = tokens.get("total", 0)

                # Serialize complex fields
                reasoning_trace = json.dumps(execution_result.get("reasoning_trace", []))
                metrics_json = json.dumps(metrics)
                metadata_json = json.dumps(execution_result.get("metadata")) if "metadata" in execution_result else None

                # Insert or replace
                cursor.execute("""
                INSERT OR REPLACE INTO executions (
                    execution_id, query, answer, model, agent_type,
                    execution_time_seconds, estimated_cost_usd, total_tokens,
                    num_steps, timestamp, reasoning_trace, metrics, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    execution_id, query, answer, model, agent_type,
                    execution_time, estimated_cost, total_tokens,
                    num_steps, timestamp, reasoning_trace, metrics_json, metadata_json
                ))

                conn.commit()
                logger.debug(f"Saved execution {execution_id} to store")
                return True

        except Exception as e:
            logger.error(f"Failed to save execution: {e}")
            return False

    def get_execution(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve execution by ID.

        Args:
            execution_id: Execution ID to retrieve

        Returns:
            Full execution result or None if not found
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                SELECT * FROM executions WHERE execution_id = ?
                """, (execution_id,))

                row = cursor.fetchone()

                if row:
                    return self._row_to_dict(row)

                return None

        except Exception as e:
            logger.error(f"Failed to retrieve execution {execution_id}: {e}")
            return None

    def get_recent_executions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent execution summaries.

        Args:
            limit: Maximum number of executions to return

        Returns:
            List of execution summary dictionaries
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                SELECT
                    execution_id, query, timestamp, model, agent_type,
                    execution_time_seconds, estimated_cost_usd, num_steps
                FROM executions
                ORDER BY timestamp DESC
                LIMIT ?
                """, (limit,))

                rows = cursor.fetchall()

                return [
                    {
                        "execution_id": row["execution_id"],
                        "query": row["query"][:100],  # Truncate long queries
                        "timestamp": row["timestamp"],
                        "model": row["model"],
                        "agent_type": row["agent_type"],
                        "execution_time": row["execution_time_seconds"],
                        "estimated_cost": row["estimated_cost_usd"],
                        "num_steps": row["num_steps"]
                    }
                    for row in rows
                ]

        except Exception as e:
            logger.error(f"Failed to get recent executions: {e}")
            return []

    def cleanup_old_executions(self) -> int:
        """
        Delete executions older than retention period.

        Returns:
            Number of executions deleted
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=self.retention_days)
            cutoff_str = cutoff_date.isoformat() + "Z"

            with self._get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                DELETE FROM executions WHERE timestamp < ?
                """, (cutoff_str,))

                deleted_count = cursor.rowcount
                conn.commit()

                if deleted_count > 0:
                    logger.info(f"Cleaned up {deleted_count} old executions")

                return deleted_count

        except Exception as e:
            logger.error(f"Failed to cleanup old executions: {e}")
            return 0

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get storage statistics.

        Returns:
            Dictionary with storage statistics
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()

                # Total count
                cursor.execute("SELECT COUNT(*) as total FROM executions")
                total = cursor.fetchone()["total"]

                # Total cost
                cursor.execute("SELECT SUM(estimated_cost_usd) as total_cost FROM executions")
                total_cost = cursor.fetchone()["total_cost"] or 0.0

                # Total tokens
                cursor.execute("SELECT SUM(total_tokens) as total_tokens FROM executions")
                total_tokens = cursor.fetchone()["total_tokens"] or 0

                # By model
                cursor.execute("""
                SELECT model, COUNT(*) as count
                FROM executions
                GROUP BY model
                """)
                by_model = {row["model"]: row["count"] for row in cursor.fetchall()}

                # By agent type
                cursor.execute("""
                SELECT agent_type, COUNT(*) as count
                FROM executions
                GROUP BY agent_type
                """)
                by_agent_type = {row["agent_type"]: row["count"] for row in cursor.fetchall()}

                # Database size
                db_size = self.db_path.stat().st_size if self.db_path.exists() else 0

                return {
                    "total_executions": total,
                    "total_cost_usd": round(total_cost, 4),
                    "total_tokens": total_tokens,
                    "by_model": by_model,
                    "by_agent_type": by_agent_type,
                    "database_size_bytes": db_size,
                    "database_size_mb": round(db_size / (1024 * 1024), 2),
                    "retention_days": self.retention_days
                }

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {}

    def clear_all(self) -> bool:
        """
        Clear all executions (use with caution).

        Returns:
            True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM executions")
                conn.commit()

                logger.warning("All executions cleared from store")
                return True

        except Exception as e:
            logger.error(f"Failed to clear executions: {e}")
            return False

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert database row to execution result dictionary."""
        return {
            "execution_id": row["execution_id"],
            "query": row["query"],
            "answer": row["answer"],
            "reasoning_trace": json.loads(row["reasoning_trace"]),
            "metrics": json.loads(row["metrics"]),
            "timestamp": row["timestamp"],
            "metadata": json.loads(row["metadata"]) if row["metadata"] else None
        }

    def vacuum(self):
        """Optimize database by running VACUUM."""
        try:
            with self._get_connection() as conn:
                conn.execute("VACUUM")
                logger.info("Database vacuumed successfully")
        except Exception as e:
            logger.error(f"Failed to vacuum database: {e}")
