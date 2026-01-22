"""
API-specific configuration using Pydantic Settings.

Extends the base configuration from src.config with API-specific settings.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class APISettings(BaseSettings):
    """API-specific settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=4, description="Number of workers")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )

    # Environment
    environment: Literal["development", "production", "test"] = Field(
        default="development", description="Environment"
    )

    # CORS - FIXED: No wildcards for security
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:8501",  # Streamlit dashboard
            "http://localhost:8000",  # API itself
            "http://127.0.0.1:8501",
            "http://127.0.0.1:8000",
        ],
        description="Allowed CORS origins (no wildcards for security)"
    )

    # OpenAI API Key (from base config)
    openai_api_key: str = Field(default="", description="OpenAI API key")

    # Database
    database_path: str = Field(
        default="data/pink_floyd_songs.db", description="Path to SQLite database"
    )

    # API Metadata
    api_title: str = Field(
        default="Pink Floyd AI Agent API", description="API title"
    )
    api_description: str = Field(
        default="ReAct agent API with Pink Floyd database and currency tools",
        description="API description",
    )
    api_version: str = Field(default="1.0.0", description="API version")


@lru_cache
def get_settings() -> APISettings:
    """Get cached API settings instance."""
    return APISettings()
