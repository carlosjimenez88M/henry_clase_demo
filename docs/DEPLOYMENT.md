# Deployment Guide

## Quick Start

### Prerequisites

- Python 3.12+
- UV package manager
- Docker and Docker Compose (for containerized deployment)
- OpenAI API key

### Environment Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd henry_clase_demo
```

2. **Copy environment file**:
```bash
cp .env.example .env
```

3. **Configure environment variables**:
```bash
# Edit .env file
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_PATH=data/pink_floyd_songs.db
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Local Development

### Option 1: Using Makefile (Recommended)

```bash
# Install dependencies and setup database
make init

# Run API server
make run-api

# Run Streamlit dashboard (in another terminal)
make run-dashboard

# Run both in parallel
make dev
```

### Option 2: Manual Setup

```bash
# Install dependencies
uv sync --group dev

# Setup database
uv run python scripts/setup_database.py

# Run API
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Run dashboard (in another terminal)
uv run streamlit run dashboard/app.py
```

**Access**:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Dashboard: http://localhost:8501

---

## Docker Deployment

### Build and Run

```bash
# Build all images
make docker-build

# Start services
make docker-up

# View logs
make docker-logs

# Stop services
make docker-down
```

### Development Mode

```bash
# Start with hot-reload
make docker-dev
```

### Manual Docker Commands

```bash
# Build specific service
docker-compose build api

# Run services
docker-compose up -d

# View logs for specific service
docker-compose logs -f api

# Stop all services
docker-compose down
```

**Access (Docker)**:
- API: http://localhost:8000
- Dashboard: http://localhost:8501

---

## Testing

### Run All Tests

```bash
# Local
make test

# Docker
make docker-test
```

### Test Categories

```bash
# Unit tests only
make test-unit

# Integration tests only
make test-integration

# E2E tests only
make test-e2e

# Generate HTML coverage report
make coverage-html
```

### Coverage Requirements

Tests must maintain >80% coverage to pass. Coverage reports are generated in:
- `htmlcov/index.html` (HTML report)
- `coverage/coverage.xml` (XML report for CI/CD)

---

## Production Deployment

### Docker Production Setup

1. **Update docker-compose.yml** for production:
```yaml
services:
  api:
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
    restart: always
```

2. **Use production build**:
```bash
docker-compose -f docker-compose.yml up -d
```

3. **Health checks**:
```bash
curl http://localhost:8000/health/ready
```

### Environment Variables

**Required**:
- `OPENAI_API_KEY`: OpenAI API key

**Optional**:
- `DATABASE_PATH`: SQLite database path (default: `data/pink_floyd_songs.db`)
- `API_HOST`: API host (default: `0.0.0.0`)
- `API_PORT`: API port (default: `8000`)
- `API_WORKERS`: Number of workers (default: `4`)
- `LOG_LEVEL`: Logging level (default: `INFO`)
- `ENVIRONMENT`: Environment name (default: `development`)
- `API_URL`: API URL for dashboard (default: `http://localhost:8000`)

---

## Reverse Proxy (Nginx)

Example Nginx configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Dashboard
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

---

## Monitoring and Logging

### Logs

**Local**:
- API logs: `logs/api.log`
- Console output with colors

**Docker**:
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f api

# Follow last 100 lines
docker-compose logs --tail=100 -f
```

### Health Checks

```bash
# Basic health
curl http://localhost:8000/health

# Readiness (checks database, OpenAI key)
curl http://localhost:8000/health/ready

# Liveness
curl http://localhost:8000/health/live
```

---

## Database Management

### Initialize/Reset Database

```bash
# Local
make reset-db

# Manual
rm -f data/pink_floyd_songs.db
uv run python scripts/setup_database.py
```

### Backup Database

```bash
# Create backup
cp data/pink_floyd_songs.db data/backup_$(date +%Y%m%d).db

# Restore backup
cp data/backup_20260122.db data/pink_floyd_songs.db
```

---

## Troubleshooting

### API Not Starting

1. Check OpenAI API key:
```bash
echo $OPENAI_API_KEY
```

2. Check database exists:
```bash
ls -la data/pink_floyd_songs.db
```

3. Check logs:
```bash
tail -f logs/api.log
```

### Dashboard Can't Connect to API

1. Check API is running:
```bash
curl http://localhost:8000/health
```

2. Check API_URL environment variable:
```bash
echo $API_URL
```

3. In Docker, ensure services are on same network:
```bash
docker network inspect pinkfloyd-network
```

### Tests Failing

1. Check coverage threshold:
```bash
pytest tests/ --cov=src --cov=api --cov-report=term-missing
```

2. Run specific test:
```bash
pytest tests/integration/test_api_health.py -v
```

---

## Performance Tuning

### API Workers

Adjust workers based on CPU cores:
```yaml
# docker-compose.yml
environment:
  - API_WORKERS=8  # 2x CPU cores
```

### Database Optimization

SQLite is suitable for demos. For production at scale, consider:
- PostgreSQL for better concurrency
- Redis for caching
- Separate read replicas

---

## Security Considerations

1. **API Key Protection**:
   - Never commit `.env` file
   - Use secrets management in production
   - Rotate keys regularly

2. **CORS**:
   - Update `cors_origins` in production
   - Restrict to specific domains

3. **Rate Limiting**:
   - Add rate limiting middleware for production
   - Consider using FastAPI Rate Limiter

4. **HTTPS**:
   - Use reverse proxy with SSL/TLS
   - Let's Encrypt for certificates
