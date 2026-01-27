"""Unit tests for DatabaseManager."""

from src.database.db_manager import DatabaseManager
from src.database.schema import Song


class TestDatabaseManager:
    """Test suite for DatabaseManager class."""

    def test_initialize_database(self, temp_db_path):
        """Test database initialization."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        assert temp_db_path.exists()

        # Check that songs were seeded
        songs = db_manager.get_all_songs()
        assert len(songs) > 0

    def test_get_all_songs(self, temp_db_path):
        """Test getting all songs."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        songs = db_manager.get_all_songs()
        assert isinstance(songs, list)
        assert len(songs) > 0
        assert isinstance(songs[0], Song)

    def test_get_all_songs_with_limit(self, temp_db_path):
        """Test getting songs with limit."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        songs = db_manager.get_all_songs(limit=5)
        assert len(songs) <= 5

    def test_get_songs_by_mood(self, temp_db_path):
        """Test filtering songs by mood."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        melancholic_songs = db_manager.get_songs_by_mood("melancholic")
        assert isinstance(melancholic_songs, list)
        assert all(song.mood == "melancholic" for song in melancholic_songs)

    def test_get_songs_by_album(self, temp_db_path):
        """Test filtering songs by album."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        dark_side_songs = db_manager.get_songs_by_album("Dark Side")
        assert isinstance(dark_side_songs, list)
        assert all("Dark Side" in song.album for song in dark_side_songs)

    def test_get_songs_by_year(self, temp_db_path):
        """Test filtering songs by year."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        songs_1973 = db_manager.get_songs_by_year(1973)
        assert isinstance(songs_1973, list)
        assert all(song.year == 1973 for song in songs_1973)

    def test_get_songs_by_decade(self, temp_db_path):
        """Test filtering songs by decade."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        songs_1970s = db_manager.get_songs_by_decade(1970)
        assert isinstance(songs_1970s, list)
        assert all(1970 <= song.year <= 1979 for song in songs_1970s)

    def test_search_lyrics(self, temp_db_path):
        """Test searching lyrics."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        results = db_manager.search_lyrics("time")
        assert isinstance(results, list)

    def test_get_mood_statistics(self, temp_db_path):
        """Test mood statistics calculation."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        stats = db_manager.get_mood_statistics()
        assert isinstance(stats, dict)
        assert len(stats) > 0
        assert all(isinstance(count, int) for count in stats.values())

    def test_search_songs_general(self, temp_db_path):
        """Test general search functionality."""
        db_manager = DatabaseManager(temp_db_path)
        db_manager.initialize_database()

        results = db_manager.search_songs("time")
        assert isinstance(results, list)
