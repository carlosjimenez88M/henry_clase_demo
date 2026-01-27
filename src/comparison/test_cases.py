"""
Test cases for model comparison.

This module defines standard test queries for comparing different models.
"""

from typing import Any

# Standard test queries for model comparison
TEST_QUERIES: list[dict[str, Any]] = [
    {
        "id": 1,
        "query": "Find melancholic Pink Floyd songs",
        "category": "database_simple",
        "expected_tool": "pink_floyd_database",
        "expected_keywords": ["Time", "Comfortably Numb", "Wish You Were Here"],
    },
    {
        "id": 2,
        "query": "Show me songs from The Dark Side of the Moon album",
        "category": "database_simple",
        "expected_tool": "pink_floyd_database",
        "expected_keywords": ["Time", "Money", "Us and Them"],
    },
    {
        "id": 3,
        "query": "What's the current USD to EUR exchange rate?",
        "category": "currency_simple",
        "expected_tool": "currency_price_checker",
        "expected_keywords": ["USD", "EUR", "exchange rate"],
    },
    {
        "id": 4,
        "query": "How much is 100 dollars in British pounds?",
        "category": "currency_simple",
        "expected_tool": "currency_price_checker",
        "expected_keywords": ["GBP", "100"],
    },
    {
        "id": 5,
        "query": "Find psychedelic songs from the 1960s",
        "category": "database_complex",
        "expected_tool": "pink_floyd_database",
        "expected_keywords": ["Astronomy Domine", "Interstellar Overdrive"],
    },
    {
        "id": 6,
        "query": "I want to listen to energetic Pink Floyd music while checking the euro price",
        "category": "multi_tool",
        "expected_tools": ["pink_floyd_database", "currency_price_checker"],
        "expected_keywords": ["energetic", "EUR"],
    },
    {
        "id": 7,
        "query": "What songs from The Wall album are melancholic?",
        "category": "database_complex",
        "expected_tool": "pink_floyd_database",
        "expected_keywords": ["Comfortably Numb", "Hey You", "Mother"],
    },
    {
        "id": 8,
        "query": "Compare USD to JPY exchange rate",
        "category": "currency_simple",
        "expected_tool": "currency_price_checker",
        "expected_keywords": ["JPY", "yen"],
    },
]


def get_all_test_cases() -> list[dict[str, Any]]:
    """Get all test cases."""
    return TEST_QUERIES


def get_test_cases_by_category(category: str) -> list[dict[str, Any]]:
    """Get test cases filtered by category."""
    return [tc for tc in TEST_QUERIES if tc["category"] == category]


def get_simple_test_cases() -> list[dict[str, Any]]:
    """Get simple test cases (single tool, straightforward)."""
    return [
        tc
        for tc in TEST_QUERIES
        if tc["category"] in ["database_simple", "currency_simple"]
    ]


def get_complex_test_cases() -> list[dict[str, Any]]:
    """Get complex test cases (multi-step reasoning, multiple tools)."""
    return [
        tc
        for tc in TEST_QUERIES
        if tc["category"] in ["database_complex", "multi_tool"]
    ]
