"""
FastAPI main application for Pink Floyd AI Agent.

This module creates and configures the FastAPI app with:
- All routers (health, agent, database, comparison, metrics)
- CORS middleware
- Request logging middleware
- Startup/shutdown events
- OpenAPI documentation
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import health, agent, database, comparison, metrics
from api.middleware import log_requests
from api.core.logger import logger, log_success, log_error
from api.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Startup:
    - Log API startup
    - Check database connectivity
    - Verify OpenAI API key

    Shutdown:
    - Log API shutdown
    - Clean up resources
    """
    settings = get_settings()

    # Startup
    logger.info("="*70)
    log_success(f"Starting {settings.api_title} v{settings.api_version}")
    logger.info("="*70)

    # Check database
    db_path = Path(settings.database_path)
    if db_path.exists():
        log_success(f"Database found: {db_path}")
    else:
        log_error(f"Database not found: {db_path}")

    # Check OpenAI API key
    if settings.openai_api_key:
        log_success("OpenAI API key configured")
    else:
        log_error("OpenAI API key not configured")

    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Log level: {settings.log_level}")
    logger.info(f"CORS origins: {settings.cors_origins}")
    logger.info("="*70)

    yield

    # Shutdown
    logger.info("="*70)
    log_success(f"Shutting down {settings.api_title}")
    logger.info("="*70)


# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add request logging middleware
app.middleware("http")(log_requests)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(agent.router, prefix="/api/v1", tags=["Agent"])
app.include_router(database.router, prefix="/api/v1", tags=["Database"])
app.include_router(comparison.router, prefix="/api/v1", tags=["Comparison"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Returns links to documentation and basic API metadata.
    """
    return {
        "message": "Pink Floyd AI Agent API",
        "version": settings.api_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/health",
        "endpoints": {
            "agent": "/api/v1/agent/query",
            "database": "/api/v1/database/songs",
            "comparison": "/api/v1/comparison/run"
        }
    }


# Error handlers
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "detail": f"The requested resource was not found: {request.url.path}",
            "status_code": 404
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    log_error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later.",
            "status_code": 500
        }
    )
