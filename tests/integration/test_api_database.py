"""Integration tests for database endpoints."""

import pytest
from fastapi.testclient import TestClient


def test_get_songs(api_client: TestClient):
    """Test getting songs with pagination."""
    response = api_client.get("/api/v1/database/songs?limit=10&offset=0")

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "songs" in data
    assert "limit" in data
    assert "offset" in data
    assert data["limit"] == 10
    assert data["offset"] == 0


def test_get_songs_with_mood_filter(api_client: TestClient):
    """Test filtering songs by mood."""
    response = api_client.get("/api/v1/database/songs?mood=melancholic&limit=5")

    assert response.status_code == 200
    data = response.json()
    assert "songs" in data


def test_get_songs_with_album_filter(api_client: TestClient):
    """Test filtering songs by album."""
    response = api_client.get("/api/v1/database/songs?album=Dark Side")

    assert response.status_code == 200
    data = response.json()
    assert "songs" in data


def test_search_songs(api_client: TestClient):
    """Test searching songs."""
    request_data = {
        "query": "time",
        "mood": "melancholic",
        "limit": 10,
        "offset": 0
    }

    response = api_client.post("/api/v1/database/search", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "songs" in data


def test_get_database_stats(api_client: TestClient):
    """Test getting database statistics."""
    response = api_client.get("/api/v1/database/stats")

    assert response.status_code == 200
    data = response.json()
    assert "total_songs" in data
    assert "total_albums" in data
    assert "moods" in data
    assert "albums" in data


def test_get_moods(api_client: TestClient):
    """Test getting available moods."""
    response = api_client.get("/api/v1/database/moods")

    assert response.status_code == 200
    data = response.json()
    assert "moods" in data
    assert "total" in data
    assert isinstance(data["moods"], list)


def test_get_albums(api_client: TestClient):
    """Test getting available albums."""
    response = api_client.get("/api/v1/database/albums")

    assert response.status_code == 200
    data = response.json()
    assert "albums" in data
    assert "total" in data
    assert isinstance(data["albums"], list)


def test_search_with_year_range(api_client: TestClient):
    """Test searching with year range."""
    request_data = {
        "year_min": 1970,
        "year_max": 1979,
        "limit": 10
    }

    response = api_client.post("/api/v1/database/search", json=request_data)

    assert response.status_code == 200
    data = response.json()
    assert "songs" in data
