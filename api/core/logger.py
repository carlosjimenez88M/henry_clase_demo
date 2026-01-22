"""
Logger configuration with colored output using loguru.

Features:
- Colored console output (green for success, red for errors)
- File logging with rotation
- Structured logging with context
"""

import sys
from pathlib import Path
from loguru import logger

# Remove default handler
logger.remove()

# Create logs directory
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Console handler with colors
logger.add(
    sys.stdout,
    colorize=True,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}:{function}:{line}</cyan> - "
        "<level>{message}</level>"
    ),
    level="DEBUG",
)

# File handler without colors (with rotation and retention)
logger.add(
    log_dir / "api.log",
    rotation="10 MB",
    retention="30 days",
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} - "
        "{message}"
    ),
    level="INFO",
)


def log_success(message: str, **kwargs):
    """Log a success message in green."""
    logger.opt(colors=True).success(f"<green>✓ {message}</green>", **kwargs)


def log_error(message: str, **kwargs):
    """Log an error message in red."""
    logger.opt(colors=True).error(f"<red>✗ {message}</red>", **kwargs)


def log_warning(message: str, **kwargs):
    """Log a warning message in yellow."""
    logger.opt(colors=True).warning(f"<yellow>⚠ {message}</yellow>", **kwargs)


def log_info(message: str, **kwargs):
    """Log an info message in blue."""
    logger.opt(colors=True).info(f"<blue>ℹ {message}</blue>", **kwargs)


def log_debug(message: str, **kwargs):
    """Log a debug message in magenta."""
    logger.opt(colors=True).debug(f"<magenta>🔍 {message}</magenta>", **kwargs)


# Export logger and convenience functions
__all__ = ["logger", "log_success", "log_error", "log_warning", "log_info", "log_debug"]
