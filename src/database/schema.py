"""
Database schema for Pink Floyd songs.

This module defines the SQLAlchemy models for storing and querying Pink Floyd songs.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Index, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


class Song(Base):
    """Model for Pink Floyd songs."""

    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    album: Mapped[str] = mapped_column(String(200), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    lyrics: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    track_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )

    # Indexes for faster queries
    __table_args__ = (
        Index("idx_mood", "mood"),
        Index("idx_album", "album"),
        Index("idx_year", "year"),
    )

    def __repr__(self) -> str:
        """String representation of Song."""
        return (
            f"Song(id={self.id}, title='{self.title}', "
            f"album='{self.album}', year={self.year}, mood='{self.mood}')"
        )

    def to_dict(self) -> dict:
        """Convert song to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "album": self.album,
            "year": self.year,
            "lyrics": self.lyrics,
            "mood": self.mood,
            "duration_seconds": self.duration_seconds,
            "track_number": self.track_number,
        }


def create_tables(engine):
    """Create all tables in the database."""
    Base.metadata.create_all(engine)


def get_session_factory(database_url: str):
    """Create a sessionmaker for the given database URL."""
    engine = create_engine(database_url, echo=False)
    return sessionmaker(bind=engine), engine
