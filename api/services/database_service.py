"""Database service for handling Pink Floyd database operations."""

from pathlib import Path
from typing import Any

from api.core.config import get_settings
from api.core.errors import DatabaseError
from api.core.logger import logger
from src.database.db_manager import DatabaseManager
from src.database.schema import Song


class DatabaseService:
    """Service for managing Pink Floyd database operations."""

    def __init__(self):
        """Initialize database service."""
        settings = get_settings()
        db_path = Path(settings.database_path)

        try:
            self.db_manager = DatabaseManager(db_path)
            logger.info(f"DatabaseService initialized with path: {db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")

    def get_songs(
        self,
        limit: int = 10,
        offset: int = 0,
        mood: str | None = None,
        album: str | None = None,
        year: int | None = None,
    ) -> dict[str, Any]:
        """
        Get songs with pagination and filtering.

        Args:
            limit: Maximum number of songs to return
            offset: Number of songs to skip
            mood: Filter by mood
            album: Filter by album
            year: Filter by year

        Returns:
            Dictionary with songs and metadata

        Raises:
            DatabaseError: If query fails
        """
        try:
            # Get all songs first
            if mood:
                songs = self.db_manager.get_songs_by_mood(mood)
            elif album:
                songs = self.db_manager.get_songs_by_album(album)
            elif year:
                songs = self.db_manager.get_songs_by_year(year)
            else:
                songs = self.db_manager.get_all_songs(limit=None)

            # Apply pagination
            total = len(songs)
            paginated_songs = songs[offset : offset + limit]

            # Convert to dictionaries
            song_dicts = [self._song_to_dict(song) for song in paginated_songs]

            return {
                "total": total,
                "songs": song_dicts,
                "limit": limit,
                "offset": offset,
            }

        except Exception as e:
            logger.error(f"Failed to get songs: {e}")
            raise DatabaseError(f"Failed to retrieve songs: {str(e)}")

    def search_songs(
        self,
        query: str | None = None,
        mood: str | None = None,
        album: str | None = None,
        year: int | None = None,
        year_min: int | None = None,
        year_max: int | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict[str, Any]:
        """
        Search songs with multiple criteria.

        Args:
            query: Search query for title/lyrics
            mood: Filter by mood
            album: Filter by album
            year: Filter by specific year
            year_min: Minimum year
            year_max: Maximum year
            limit: Maximum results
            offset: Pagination offset

        Returns:
            Dictionary with songs and metadata

        Raises:
            DatabaseError: If search fails
        """
        try:
            # Use search_songs method if query provided
            if query:
                songs = self.db_manager.search_songs(query, mood=mood, album=album)
            elif mood:
                songs = self.db_manager.get_songs_by_mood(mood)
            elif album:
                songs = self.db_manager.get_songs_by_album(album)
            elif year:
                songs = self.db_manager.get_songs_by_year(year)
            else:
                songs = self.db_manager.get_all_songs(limit=None)

            # Filter by year range if specified
            if year_min or year_max:
                filtered_songs = []
                for song in songs:
                    if year_min and song.year < year_min:
                        continue
                    if year_max and song.year > year_max:
                        continue
                    filtered_songs.append(song)
                songs = filtered_songs

            # Apply pagination
            total = len(songs)
            paginated_songs = songs[offset : offset + limit]

            # Convert to dictionaries
            song_dicts = [self._song_to_dict(song) for song in paginated_songs]

            logger.info(f"Search returned {total} songs (showing {len(song_dicts)})")

            return {
                "total": total,
                "songs": song_dicts,
                "limit": limit,
                "offset": offset,
            }

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise DatabaseError(f"Search operation failed: {str(e)}")

    def get_statistics(self) -> dict[str, Any]:
        """
        Get database statistics.

        Returns:
            Statistics dictionary

        Raises:
            DatabaseError: If stats calculation fails
        """
        try:
            all_songs = self.db_manager.get_all_songs(limit=None)
            mood_stats = self.db_manager.get_mood_statistics()

            # Calculate album distribution
            albums: dict[str, int] = {}
            years = []
            for song in all_songs:
                albums[song.album] = albums.get(song.album, 0) + 1
                years.append(song.year)

            return {
                "total_songs": len(all_songs),
                "total_albums": len(albums),
                "year_range": {
                    "min": min(years) if years else 0,
                    "max": max(years) if years else 0,
                },
                "moods": mood_stats,
                "albums": albums,
            }

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            raise DatabaseError(f"Statistics calculation failed: {str(e)}")

    def get_moods(self) -> dict[str, Any]:
        """
        Get list of available moods.

        Returns:
            Dictionary with moods list

        Raises:
            DatabaseError: If query fails
        """
        try:
            mood_stats = self.db_manager.get_mood_statistics()
            moods = list(mood_stats.keys())

            return {"moods": sorted(moods), "total": len(moods)}

        except Exception as e:
            logger.error(f"Failed to get moods: {e}")
            raise DatabaseError(f"Failed to retrieve moods: {str(e)}")

    def get_albums(self) -> dict[str, Any]:
        """
        Get list of available albums.

        Returns:
            Dictionary with albums list

        Raises:
            DatabaseError: If query fails
        """
        try:
            all_songs = self.db_manager.get_all_songs(limit=None)
            albums = sorted(set(song.album for song in all_songs))

            return {"albums": albums, "total": len(albums)}

        except Exception as e:
            logger.error(f"Failed to get albums: {e}")
            raise DatabaseError(f"Failed to retrieve albums: {str(e)}")

    @staticmethod
    def _song_to_dict(song: Song) -> dict[str, Any]:
        """Convert Song object to dictionary."""
        return {
            "id": song.id,
            "title": song.title,
            "album": song.album,
            "year": song.year,
            "mood": song.mood,
            "lyrics": song.lyrics,
        }
