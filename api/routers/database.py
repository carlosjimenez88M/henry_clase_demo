"""Database endpoints for Pink Floyd songs."""

from fastapi import APIRouter, Depends, HTTPException, Query

from api.core.logger import logger
from api.schemas.database import (
    AlbumListResponse,
    DatabaseStats,
    MoodListResponse,
    SongListResponse,
    SongSearchRequest,
)
from api.services.database_service import DatabaseService

router = APIRouter()


def get_database_service():
    """Dependency to get database service instance."""
    return DatabaseService()


@router.get("/database/songs", response_model=SongListResponse, tags=["Database"])
async def get_songs(
    limit: int = Query(default=10, ge=1, le=100, description="Maximum results"),
    offset: int = Query(default=0, ge=0, description="Pagination offset"),
    mood: str | None = Query(default=None, description="Filter by mood"),
    album: str | None = Query(default=None, description="Filter by album"),
    year: int | None = Query(default=None, description="Filter by year"),
    service: DatabaseService = Depends(get_database_service),
):
    """
    Get Pink Floyd songs with pagination and filtering.

    Returns a list of songs with optional filtering by:
    - **mood**: melancholic, energetic, psychedelic, etc.
    - **album**: Album name (partial match)
    - **year**: Specific release year

    **Example:**
    - `/database/songs?mood=melancholic&limit=5`
    - `/database/songs?album=Dark Side&year=1973`
    """
    try:
        result = service.get_songs(
            limit=limit, offset=offset, mood=mood, album=album, year=year
        )

        return SongListResponse(**result)

    except Exception as e:
        logger.error(f"Failed to get songs: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve songs: {str(e)}"
        )


@router.post("/database/search", response_model=SongListResponse, tags=["Database"])
async def search_songs(
    request: SongSearchRequest, service: DatabaseService = Depends(get_database_service)
):
    """
    Search songs with multiple criteria.

    Supports searching by:
    - **query**: Search in title, album, and lyrics
    - **mood**: Filter by mood
    - **album**: Filter by album name
    - **year**: Filter by specific year
    - **year_min/year_max**: Filter by year range

    **Example request:**
    ```json
    {
      "query": "time",
      "mood": "melancholic",
      "year_min": 1970,
      "year_max": 1979,
      "limit": 10
    }
    ```
    """
    try:
        result = service.search_songs(
            query=request.query,
            mood=request.mood,
            album=request.album,
            year=request.year,
            year_min=request.year_min,
            year_max=request.year_max,
            limit=request.limit,
            offset=request.offset,
        )

        return SongListResponse(**result)

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/database/stats", response_model=DatabaseStats, tags=["Database"])
async def get_database_stats(service: DatabaseService = Depends(get_database_service)):
    """
    Get database statistics.

    Returns comprehensive statistics about the Pink Floyd database:
    - Total number of songs and albums
    - Year range of songs
    - Distribution of songs by mood
    - Distribution of songs by album
    """
    try:
        stats = service.get_statistics()
        return DatabaseStats(**stats)

    except Exception as e:
        logger.error(f"Failed to get stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve statistics: {str(e)}"
        )


@router.get("/database/moods", response_model=MoodListResponse, tags=["Database"])
async def get_moods(service: DatabaseService = Depends(get_database_service)):
    """
    Get list of available moods.

    Returns all unique moods present in the database.
    Use these values to filter songs by mood.
    """
    try:
        result = service.get_moods()
        return MoodListResponse(**result)

    except Exception as e:
        logger.error(f"Failed to get moods: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve moods: {str(e)}"
        )


@router.get("/database/albums", response_model=AlbumListResponse, tags=["Database"])
async def get_albums(service: DatabaseService = Depends(get_database_service)):
    """
    Get list of available albums.

    Returns all unique albums present in the database.
    Use these values to filter songs by album.
    """
    try:
        result = service.get_albums()
        return AlbumListResponse(**result)

    except Exception as e:
        logger.error(f"Failed to get albums: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve albums: {str(e)}"
        )
