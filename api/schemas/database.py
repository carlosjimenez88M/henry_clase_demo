"""Pydantic schemas for Database API endpoints."""


from pydantic import BaseModel, Field


class SongResponse(BaseModel):
    """Response schema for a single song."""

    id: int = Field(..., description="Song ID")
    title: str = Field(..., description="Song title")
    album: str = Field(..., description="Album name")
    year: int = Field(..., description="Release year")
    mood: str = Field(..., description="Song mood/feeling")
    lyrics: str | None = Field(None, description="Song lyrics (if available)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "Time",
                "album": "The Dark Side of the Moon",
                "year": 1973,
                "mood": "melancholic",
                "lyrics": "Ticking away the moments...",
            }
        }
    }


class SongSearchRequest(BaseModel):
    """Request schema for searching songs."""

    query: str | None = Field(None, description="Search query (lyrics, title)")
    mood: str | None = Field(None, description="Filter by mood")
    album: str | None = Field(None, description="Filter by album")
    year: int | None = Field(None, description="Filter by year")
    year_min: int | None = Field(None, description="Minimum year")
    year_max: int | None = Field(None, description="Maximum year")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")

    model_config = {
        "json_schema_extra": {
            "example": {
                "query": "time",
                "mood": "melancholic",
                "year_min": 1970,
                "year_max": 1979,
                "limit": 10,
                "offset": 0,
            }
        }
    }


class SongListResponse(BaseModel):
    """Response schema for a list of songs."""

    total: int = Field(..., description="Total number of songs matching criteria")
    songs: list[SongResponse] = Field(..., description="List of songs")
    limit: int = Field(..., description="Results limit")
    offset: int = Field(..., description="Pagination offset")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 28,
                "songs": [
                    {
                        "id": 1,
                        "title": "Time",
                        "album": "The Dark Side of the Moon",
                        "year": 1973,
                        "mood": "melancholic",
                    }
                ],
                "limit": 10,
                "offset": 0,
            }
        }
    }


class DatabaseStats(BaseModel):
    """Statistics about the Pink Floyd database."""

    total_songs: int = Field(..., description="Total number of songs")
    total_albums: int = Field(..., description="Total number of albums")
    year_range: dict[str, int] = Field(..., description="Year range (min/max)")
    moods: dict[str, int] = Field(..., description="Mood distribution")
    albums: dict[str, int] = Field(..., description="Songs per album")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_songs": 28,
                "total_albums": 5,
                "year_range": {"min": 1967, "max": 1979},
                "moods": {"melancholic": 10, "energetic": 8, "psychedelic": 10},
                "albums": {"The Dark Side of the Moon": 10, "The Wall": 8},
            }
        }
    }


class MoodListResponse(BaseModel):
    """Response schema for available moods."""

    moods: list[str] = Field(..., description="List of available moods")
    total: int = Field(..., description="Total number of moods")

    model_config = {
        "json_schema_extra": {
            "example": {
                "moods": ["melancholic", "energetic", "psychedelic"],
                "total": 3,
            }
        }
    }


class AlbumListResponse(BaseModel):
    """Response schema for available albums."""

    albums: list[str] = Field(..., description="List of available albums")
    total: int = Field(..., description="Total number of albums")

    model_config = {
        "json_schema_extra": {
            "example": {
                "albums": [
                    "The Dark Side of the Moon",
                    "The Wall",
                    "Wish You Were Here",
                ],
                "total": 3,
            }
        }
    }
