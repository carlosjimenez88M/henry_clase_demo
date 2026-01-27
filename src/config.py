"""
Configuration module for AI Agent Demo.

This module handles loading environment variables, validating API keys,
and managing model configurations.
"""

from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig(BaseSettings):
    """Configuration for a single model."""

    name: str
    temperature: float = 0.01
    max_tokens: int = 1000


class Config(BaseSettings):
    """Main configuration class for the application."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="allow"
    )

    # OpenAI API
    openai_api_key: str = Field(..., description="OpenAI API key")

    # Model configurations
    default_model: str = Field(
        default="gpt-4o-mini", description="Default model to use"
    )
    temperature: float = Field(
        default=0.1, description="Temperature for model responses"
    )
    max_tokens: int = Field(
        default=1000, description="Maximum tokens for model responses"
    )

    # Database
    database_path: Path = Field(
        default=Path(__file__).parent.parent / "data" / "pink_floyd_songs.db",
        description="Path to SQLite database",
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Path = Field(
        default=Path(__file__).parent.parent / "logs" / "app.log",
        description="Path to log file",
    )

    @field_validator("openai_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate that API key is not empty and starts with expected prefix."""
        if not v:
            raise ValueError("OPENAI_API_KEY must be set in .env file")
        if not v.startswith("sk-"):
            raise ValueError("OPENAI_API_KEY must start with 'sk-'")
        return v

    @field_validator("database_path", "log_file")
    @classmethod
    def ensure_parent_dir_exists(cls, v: Path) -> Path:
        """Ensure parent directory exists for paths."""
        v.parent.mkdir(parents=True, exist_ok=True)
        return v

    @property
    def models(self) -> dict[str, ModelConfig]:
        """Get configurations for all supported models."""
        return {
            "gpt-4o-mini": ModelConfig(
                name="gpt-4o-mini",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            ),
            "gpt-4o": ModelConfig(
                name="gpt-4o", temperature=self.temperature, max_tokens=self.max_tokens
            ),
            "gpt-5-nano": ModelConfig(
                name="gpt-5-nano",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            ),
        }

    def get_model_config(self, model_name: str) -> ModelConfig:
        """Get configuration for a specific model."""
        if model_name not in self.models:
            raise ValueError(
                f"Model '{model_name}' not supported. "
                f"Available models: {list(self.models.keys())}"
            )
        return self.models[model_name]


# Global configuration instance
config = Config()
