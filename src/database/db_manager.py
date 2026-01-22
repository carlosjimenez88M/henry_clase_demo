"""
Database manager for Pink Floyd songs.

This module handles database initialization, seeding, and querying operations.
"""

from pathlib import Path
from typing import List, Optional

from sqlalchemy import create_engine, or_
from sqlalchemy.orm import Session, sessionmaker

from src.database.schema import Base, Song
from src.database.seed_data import PINK_FLOYD_SONGS


class DatabaseManager:
    """Manager for Pink Floyd songs database."""

    def __init__(self, database_path: Path):
        """Initialize database manager."""
        self.database_path = database_path
        self.database_url = f"sqlite:///{database_path}"
        self.engine = create_engine(self.database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def initialize_database(self, force_recreate: bool = False) -> None:
        """
        Initialize database and seed with data.

        Args:
            force_recreate: If True, drop existing tables and recreate
        """
        if force_recreate:
            Base.metadata.drop_all(self.engine)

        # Create tables
        Base.metadata.create_all(self.engine)

        # Seed data if database is empty
        with self.SessionLocal() as session:
            count = session.query(Song).count()
            if count == 0:
                self._seed_data(session)
                print(f" Database initialized with {len(PINK_FLOYD_SONGS)} songs")
            else:
                print(f"✓ Database already contains {count} songs")

    def _seed_data(self, session: Session) -> None:
        """Seed database with Pink Floyd songs."""
        for song_data in PINK_FLOYD_SONGS:
            song = Song(**song_data)
            session.add(song)
        session.commit()

    def get_all_songs(self, limit: Optional[int] = None) -> List[Song]:
        """Get all songs, optionally limited."""
        with self.SessionLocal() as session:
            query = session.query(Song)
            if limit:
                query = query.limit(limit)
            return query.all()

    def get_songs_by_mood(self, mood: str) -> List[Song]:
        """Get songs by mood."""
        with self.SessionLocal() as session:
            return session.query(Song).filter(
                Song.mood.ilike(f"%{mood}%")
            ).all()

    def get_songs_by_album(self, album: str) -> List[Song]:
        """Get songs by album name (partial match)."""
        with self.SessionLocal() as session:
            return session.query(Song).filter(
                Song.album.ilike(f"%{album}%")
            ).all()

    def get_songs_by_year(self, year: int) -> List[Song]:
        """Get songs by year."""
        with self.SessionLocal() as session:
            return session.query(Song).filter(Song.year == year).all()

    def get_songs_by_decade(self, decade: int) -> List[Song]:
        """Get songs by decade (e.g., 1970 for 1970s)."""
        start_year = decade
        end_year = decade + 9
        with self.SessionLocal() as session:
            return session.query(Song).filter(
                Song.year >= start_year,
                Song.year <= end_year
            ).all()

    def search_lyrics(self, keywords: str) -> List[Song]:
        """Search songs by lyrics keywords."""
        with self.SessionLocal() as session:
            # Split keywords and search for any of them
            words = keywords.lower().split()
            conditions = [Song.lyrics.ilike(f"%{word}%") for word in words]
            return session.query(Song).filter(or_(*conditions)).all()

    def search_songs(
        self,
        query: str,
        mood: Optional[str] = None,
        album: Optional[str] = None
    ) -> List[Song]:
        """
        General search across title, album, lyrics.

        Args:
            query: Search query string
            mood: Optional mood filter
            album: Optional album filter
        """
        with self.SessionLocal() as session:
            filters = or_(
                Song.title.ilike(f"%{query}%"),
                Song.album.ilike(f"%{query}%"),
                Song.lyrics.ilike(f"%{query}%")
            )

            db_query = session.query(Song).filter(filters)

            if mood:
                db_query = db_query.filter(Song.mood.ilike(f"%{mood}%"))

            if album:
                db_query = db_query.filter(Song.album.ilike(f"%{album}%"))

            return db_query.all()

    def get_song_by_title(self, title: str) -> Optional[Song]:
        """Get a specific song by title."""
        with self.SessionLocal() as session:
            return session.query(Song).filter(
                Song.title.ilike(f"%{title}%")
            ).first()

    def get_mood_statistics(self) -> dict:
        """Get statistics about songs by mood."""
        with self.SessionLocal() as session:
            songs = session.query(Song).all()
            moods = {}
            for song in songs:
                mood = song.mood
                moods[mood] = moods.get(mood, 0) + 1
            return moods

    def close(self) -> None:
        """Close database connection."""
        self.engine.dispose()
