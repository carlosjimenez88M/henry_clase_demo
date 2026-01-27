"""
Global pytest fixtures for all tests.

Provides:
- Database fixtures (in-memory SQLite)
- API client fixtures (FastAPI TestClient)
- Mock fixtures for external APIs
- Sample data fixtures
"""


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.main import app
from src.database.schema import Base, Song


@pytest.fixture(scope="session")
def test_db_engine():
    """
    Create an in-memory SQLite database engine for testing.

    Scope: session (created once per test session)
    """
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """
    Create a database session with test data.

    Scope: function (fresh data for each test)
    """
    SessionLocal = sessionmaker(bind=test_db_engine)
    session = SessionLocal()

    # Seed with minimal test data (2 songs)
    test_songs = [
        Song(
            title="Time",
            album="The Dark Side of the Moon",
            year=1973,
            mood="melancholic",
            lyrics="Ticking away the moments that make up a dull day",
        ),
        Song(
            title="Money",
            album="The Dark Side of the Moon",
            year=1973,
            mood="energetic",
            lyrics="Money, get away. Get a good job with more pay",
        ),
        Song(
            title="Wish You Were Here",
            album="Wish You Were Here",
            year=1975,
            mood="melancholic",
            lyrics="So, so you think you can tell heaven from hell",
        ),
    ]

    session.add_all(test_songs)
    session.commit()

    yield session

    session.close()


@pytest.fixture
def api_client():
    """
    Create FastAPI test client.

    Scope: function (fresh client for each test)
    """
    return TestClient(app)


@pytest.fixture
def mock_openai_response():
    """
    Mock response from OpenAI API.

    Returns a sample agent response for testing without making real API calls.
    """
    return {
        "answer": "Based on the Pink Floyd database, I found several melancholic songs.",
        "reasoning_trace": [
            {
                "step": 1,
                "type": "action",
                "content": "Search for melancholic songs",
                "tool": "pink_floyd_database",
                "input": {"mood": "melancholic"},
            },
            {
                "step": 2,
                "type": "observation",
                "content": "Found 2 songs: Time, Wish You Were Here",
            },
        ],
    }


@pytest.fixture
def sample_test_cases():
    """
    Sample test cases for model comparison.

    Returns a list of test queries with expected tools.
    """
    return [
        {
            "query": "Find melancholic Pink Floyd songs",
            "expected_tool": "pink_floyd_database",
            "category": "database_search",
        },
        {
            "query": "What songs are from The Dark Side of the Moon?",
            "expected_tool": "pink_floyd_database",
            "category": "database_search",
        },
        {
            "query": "Convert 100 USD to EUR",
            "expected_tool": "currency_converter",
            "category": "currency_conversion",
        },
    ]


@pytest.fixture
def temp_db_path(tmp_path):
    """
    Create a temporary database path for testing.

    Scope: function (fresh path for each test)
    """
    db_file = tmp_path / "test_songs.db"
    return db_file
