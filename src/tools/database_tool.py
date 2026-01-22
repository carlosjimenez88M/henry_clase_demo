"""
Pink Floyd Database Tool for AI Agent.

This tool allows the agent to query the Pink Floyd songs database by mood,
album, lyrics, year, and other criteria.
"""

from typing import List, Optional

from langchain.tools import BaseTool
from pydantic import Field

from src.config import config
from src.database.db_manager import DatabaseManager
from src.database.schema import Song


class PinkFloydDatabaseTool(BaseTool):
    """Tool for querying Pink Floyd songs database."""

    name: str = "pink_floyd_database"
    description: str = """
    A database of Pink Floyd songs. Use this tool to search for songs by:
    - Mood (melancholic, energetic, psychedelic, progressive, dark)
    - Album name (e.g., 'The Dark Side of the Moon', 'The Wall', 'Wish You Were Here')
    - Lyrics keywords (e.g., 'time', 'wall', 'shine', 'shine', 'crazy')
    - Year or decade (e.g., 1973, 1970s)

    Input should be a natural language query like:
    - "Find melancholic songs"
    - "Songs from The Wall album"
    - "Songs with lyrics about time"
    - "Psychedelic songs from the 1970s"

    Output includes song title, album, year, lyrics snippet, and mood.
    """

    db_manager: DatabaseManager = Field(default=None, exclude=True)

    def __init__(self):
        """Initialize the tool with database manager."""
        super().__init__()
        self.db_manager = DatabaseManager(config.database_path)

    def _run(self, query: str) -> str:
        """
        Execute the database query.

        Args:
            query: Natural language query string

        Returns:
            Formatted string with song results
        """
        query_lower = query.lower()

        # Parse query intent
        songs = self._parse_and_query(query_lower)

        # Format and return results
        if not songs:
            return self._format_no_results(query)

        return self._format_results(songs)

    def _parse_and_query(self, query: str) -> List[Song]:
        """Parse query and execute appropriate database operation."""
        # Mood queries
        moods = ["melancholic", "energetic", "psychedelic", "progressive", "dark"]
        for mood in moods:
            if mood in query:
                return self.db_manager.get_songs_by_mood(mood)

        # Album queries
        albums = ["dark side", "the wall", "wish you were here", "animals", "meddle", "piper"]
        for album in albums:
            if album in query:
                return self.db_manager.get_songs_by_album(album)

        # Year/decade queries
        if "1970" in query or "70s" in query or "seventies" in query:
            return self.db_manager.get_songs_by_decade(1970)
        if "1960" in query or "60s" in query or "sixties" in query:
            return self.db_manager.get_songs_by_decade(1960)

        # Specific year
        for year in range(1965, 1985):
            if str(year) in query:
                return self.db_manager.get_songs_by_year(year)

        # Lyrics search
        if "lyrics" in query or "words" in query or "about" in query:
            # Extract potential keywords
            keywords = self._extract_keywords(query)
            if keywords:
                return self.db_manager.search_lyrics(keywords)

        # General search
        return self.db_manager.search_songs(query)

    def _extract_keywords(self, query: str) -> str:
        """Extract keywords from query for lyrics search."""
        # Remove common words
        stop_words = {
            "find", "search", "show", "get", "songs", "with", "lyrics", "about",
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for"
        }
        words = query.split()
        keywords = [w for w in words if w not in stop_words]
        return " ".join(keywords)

    def _format_results(self, songs: List[Song], max_songs: int = 10) -> str:
        """Format songs as a readable string."""
        # Limit number of results
        songs = songs[:max_songs]

        result = f"Found {len(songs)} song(s):\n\n"

        for i, song in enumerate(songs, 1):
            result += f"{i}. '{song.title}' from {song.album} ({song.year})\n"
            result += f"   Mood: {song.mood}\n"

            # Show lyrics snippet (first 120 characters)
            if song.lyrics:
                lyrics_snippet = song.lyrics[:120]
                if len(song.lyrics) > 120:
                    lyrics_snippet += "..."
                result += f"   Lyrics: \"{lyrics_snippet}\"\n"

            result += "\n"

        return result.strip()

    def _format_no_results(self, query: str) -> str:
        """Format message when no results found."""
        return (
            f"No Pink Floyd songs match your query: '{query}'\n\n"
            "Try searching by:\n"
            "- Mood: melancholic, energetic, psychedelic, progressive, dark\n"
            "- Album: The Dark Side of the Moon, The Wall, Wish You Were Here, Animals\n"
            "- Lyrics keywords\n"
            "- Year or decade"
        )

    async def _arun(self, query: str) -> str:
        """Async version (not implemented, falls back to sync)."""
        return self._run(query)
