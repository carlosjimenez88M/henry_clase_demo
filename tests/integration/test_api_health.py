"""Integration tests for health endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_health_check(api_client: TestClient):
    """Test basic health check endpoint."""
    response = api_client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_readiness_check(api_client: TestClient):
    """Test readiness probe endpoint."""
    response = api_client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "checks" in data


def test_liveness_check(api_client: TestClient):
    """Test liveness probe endpoint."""
    response = api_client.get("/health/live")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data


def test_root_endpoint(api_client: TestClient):
    """Test root endpoint."""
    response = api_client.get("/")

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
