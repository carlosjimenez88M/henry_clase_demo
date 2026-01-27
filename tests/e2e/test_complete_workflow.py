"""End-to-end tests for complete workflows."""

from fastapi.testclient import TestClient


def test_database_exploration_workflow(api_client: TestClient):
    """
    Test complete database exploration workflow.

    Steps:
    1. Get database stats
    2. Get available moods
    3. Search songs by mood
    4. Get specific songs with filters
    """
    # Step 1: Get database stats
    stats_response = api_client.get("/api/v1/database/stats")
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats["total_songs"] > 0

    # Step 2: Get available moods
    moods_response = api_client.get("/api/v1/database/moods")
    assert moods_response.status_code == 200
    moods_data = moods_response.json()
    assert len(moods_data["moods"]) > 0

    # Step 3: Search songs by mood (if moods exist)
    if moods_data["moods"]:
        mood = moods_data["moods"][0]
        search_response = api_client.post(
            "/api/v1/database/search", json={"mood": mood, "limit": 5}
        )
        assert search_response.status_code == 200
        search_data = search_response.json()
        assert "songs" in search_data

    # Step 4: Get songs with pagination
    songs_response = api_client.get("/api/v1/database/songs?limit=10&offset=0")
    assert songs_response.status_code == 200
    songs_data = songs_response.json()
    assert "songs" in songs_data


def test_health_check_workflow(api_client: TestClient):
    """
    Test health check workflow.

    Steps:
    1. Check basic health
    2. Check readiness
    3. Check liveness
    """
    # Step 1: Basic health
    health = api_client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    # Step 2: Readiness
    ready = api_client.get("/health/ready")
    assert ready.status_code == 200

    # Step 3: Liveness
    live = api_client.get("/health/live")
    assert live.status_code == 200
    assert live.json()["status"] == "alive"


def test_api_discovery_workflow(api_client: TestClient):
    """
    Test API discovery workflow.

    Steps:
    1. Get root endpoint (API info)
    2. Get available models
    3. Get database moods
    4. Get database albums
    """
    # Step 1: Root endpoint
    root = api_client.get("/")
    assert root.status_code == 200
    root_data = root.json()
    assert "docs" in root_data
    assert "endpoints" in root_data

    # Step 2: Available models
    models = api_client.get("/api/v1/agent/models")
    assert models.status_code == 200
    models_data = models.json()
    assert len(models_data) > 0

    # Step 3: Database moods
    moods = api_client.get("/api/v1/database/moods")
    assert moods.status_code == 200

    # Step 4: Database albums
    albums = api_client.get("/api/v1/database/albums")
    assert albums.status_code == 200
