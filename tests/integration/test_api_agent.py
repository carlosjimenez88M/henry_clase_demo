"""Integration tests for agent endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_get_available_models(api_client: TestClient):
    """Test getting list of available models."""
    response = api_client.get("/api/v1/agent/models")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Check model structure
    model = data[0]
    assert "name" in model
    assert "display_name" in model
    assert "max_tokens" in model


def test_get_execution_history_empty(api_client: TestClient):
    """Test getting execution history when empty."""
    response = api_client.get("/api/v1/agent/history")

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "executions" in data
    assert isinstance(data["executions"], list)


def test_get_execution_detail_not_found(api_client: TestClient):
    """Test getting detail for non-existent execution."""
    response = api_client.get("/api/v1/agent/history/non-existent-id")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_agent_query_validation_empty_query(api_client: TestClient):
    """Test agent query with empty query (should fail validation)."""
    request_data = {
        "query": "",
        "model": "gpt-4o-mini"
    }

    response = api_client.post("/api/v1/agent/query", json=request_data)

    # Should fail validation (422 for Pydantic validation)
    assert response.status_code == 422


def test_agent_query_validation_temperature(api_client: TestClient):
    """Test agent query with invalid temperature."""
    request_data = {
        "query": "test",
        "model": "gpt-4o-mini",
        "temperature": 2.0  # Should be 0.0-1.0
    }

    response = api_client.post("/api/v1/agent/query", json=request_data)

    # Should fail validation
    assert response.status_code == 422
