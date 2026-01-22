"""
Storage layer for persistent data.

Provides SQLite-backed storage for execution history
to prevent memory leaks from unbounded in-memory dictionaries.
"""

from api.storage.execution_store import ExecutionStore

__all__ = ["ExecutionStore"]
