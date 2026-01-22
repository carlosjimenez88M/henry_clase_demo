"""Unit tests for AgentService."""

import pytest
from api.services.agent_service import AgentService


class TestAgentService:
    """Test suite for AgentService class."""

    def test_service_initialization(self):
        """Test that service initializes correctly."""
        service = AgentService()
        assert service is not None
        assert service.factory is not None
        assert len(service.execution_history) == 0

    def test_get_available_models(self):
        """Test getting available models."""
        service = AgentService()
        models = service.get_available_models()

        assert isinstance(models, list)
        assert len(models) > 0
        assert "gpt-4o-mini" in models

    def test_get_model_info(self):
        """Test getting model information."""
        service = AgentService()
        info = service.get_model_info("gpt-4o-mini")

        assert isinstance(info, dict)
        assert info["name"] == "gpt-4o-mini"
        assert "display_name" in info
        assert "cost_per_1k_tokens" in info

    def test_get_model_info_invalid(self):
        """Test getting info for invalid model."""
        service = AgentService()
        info = service.get_model_info("invalid-model")

        assert info == {}

    def test_get_execution_history_empty(self):
        """Test getting history when empty."""
        service = AgentService()
        history = service.get_execution_history()

        assert isinstance(history, list)
        assert len(history) == 0

    def test_get_execution_detail_not_found(self):
        """Test getting detail for non-existent execution."""
        service = AgentService()
        detail = service.get_execution_detail("non-existent-id")

        assert detail is None

    def test_clear_history(self):
        """Test clearing execution history."""
        service = AgentService()
        service.execution_history["test"] = {"data": "test"}

        assert len(service.execution_history) == 1

        service.clear_history()

        assert len(service.execution_history) == 0
