"""Unit tests for DatabaseService."""

import pytest
from unittest.mock import Mock, patch
from api.services.database_service import DatabaseService
from api.core.errors import DatabaseError


class TestDatabaseService:
    """Test suite for DatabaseService class."""

    @patch('api.services.database_service.DatabaseManager')
    @patch('api.services.database_service.get_settings')
    def test_service_initialization(self, mock_settings, mock_db_manager):
        """Test that service initializes correctly."""
        mock_settings.return_value.database_path = "test.db"

        service = DatabaseService()

        assert service is not None
        mock_db_manager.assert_called_once()

    @patch('api.services.database_service.DatabaseManager')
    @patch('api.services.database_service.get_settings')
    def test_get_moods(self, mock_settings, mock_db_manager):
        """Test getting moods list."""
        mock_settings.return_value.database_path = "test.db"

        # Mock mood statistics
        mock_instance = Mock()
        mock_instance.get_mood_statistics.return_value = {
            "melancholic": 10,
            "energetic": 8
        }
        mock_db_manager.return_value = mock_instance

        service = DatabaseService()
        result = service.get_moods()

        assert "moods" in result
        assert "total" in result
        assert len(result["moods"]) == 2
        assert "melancholic" in result["moods"]

    @patch('api.services.database_service.DatabaseManager')
    @patch('api.services.database_service.get_settings')
    def test_song_to_dict(self, mock_settings, mock_db_manager):
        """Test song to dictionary conversion."""
        mock_settings.return_value.database_path = "test.db"
        service = DatabaseService()

        # Create mock song
        mock_song = Mock()
        mock_song.id = 1
        mock_song.title = "Time"
        mock_song.album = "The Dark Side of the Moon"
        mock_song.year = 1973
        mock_song.mood = "melancholic"
        mock_song.lyrics = "Ticking away..."

        result = service._song_to_dict(mock_song)

        assert result["id"] == 1
        assert result["title"] == "Time"
        assert result["album"] == "The Dark Side of the Moon"
        assert result["year"] == 1973
