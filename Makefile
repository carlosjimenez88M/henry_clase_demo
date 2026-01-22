.PHONY: help install setup init run-api run-dashboard dev test test-unit test-integration test-e2e coverage coverage-html docker-build docker-up docker-down docker-dev docker-test docker-logs docker-clean lint format type-check clean reset-db logs

help:
	@echo "🎸 Pink Floyd AI Agent - Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install          - Install dependencies"
	@echo "  make setup            - Setup database"
	@echo "  make init             - Full init (install + setup)"
	@echo ""
	@echo "Development:"
	@echo "  make run-api          - Run FastAPI locally"
	@echo "  make run-dashboard    - Run Streamlit locally"
	@echo "  make dev              - Run both"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - All tests with coverage"
	@echo "  make test-unit        - Unit tests only"
	@echo "  make test-integration - Integration tests only"
	@echo "  make test-e2e         - E2E tests only"
	@echo "  make coverage-html    - HTML coverage report"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build images"
	@echo "  make docker-up        - Start containers"
	@echo "  make docker-dev       - Start in dev mode"
	@echo "  make docker-test      - Run tests in Docker"
	@echo "  make docker-down      - Stop containers"
	@echo "  make docker-logs      - View logs"
	@echo "  make docker-clean     - Clean all"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Linting with ruff"
	@echo "  make format           - Format with black + ruff"
	@echo "  make type-check       - Type checking with mypy"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            - Clean generated files"
	@echo "  make reset-db         - Reset database"
	@echo "  make logs             - View application logs"

install:
	@echo "📦 Installing dependencies..."
	uv sync --group dev

setup:
	@echo "🗄️ Setting up database..."
	uv run python scripts/setup_database.py

init: install setup
	@echo "✅ Initialization complete!"

run-api:
	@echo "🚀 Starting FastAPI..."
	uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard:
	@echo "🎨 Starting Streamlit..."
	uv run streamlit run dashboard/app.py

dev:
	@echo "🚀 Starting both API and Dashboard..."
	@make -j2 run-api run-dashboard

test:
	@echo "🧪 Running tests with coverage..."
	uv run pytest tests/ --cov=src --cov=api --cov-report=term-missing --cov-report=html --cov-fail-under=80 -v

test-unit:
	@echo "🧪 Running unit tests..."
	uv run pytest tests/unit/ -v

test-integration:
	@echo "🧪 Running integration tests..."
	uv run pytest tests/integration/ -v

test-e2e:
	@echo "🧪 Running E2E tests..."
	uv run pytest tests/e2e/ -v

coverage-html:
	@echo "📊 Generating HTML coverage..."
	uv run pytest tests/ --cov=src --cov=api --cov-report=html
	@echo "✅ Report at htmlcov/index.html"

docker-build:
	@echo "🐳 Building Docker images..."
	docker-compose build

docker-up:
	@echo "🐳 Starting containers..."
	docker-compose up -d
	@echo "✅ API: http://localhost:8000"
	@echo "✅ Dashboard: http://localhost:8501"

docker-down:
	@echo "🐳 Stopping containers..."
	docker-compose down

docker-dev:
	@echo "🐳 Starting in development mode..."
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

docker-test:
	@echo "🧪 Running tests in Docker..."
	docker-compose --profile test run --rm tests

docker-logs:
	@echo "📋 Showing logs..."
	docker-compose logs -f

docker-clean:
	@echo "🧹 Cleaning Docker..."
	docker-compose down -v --rmi all --remove-orphans

lint:
	@echo "🔍 Linting..."
	uv run ruff check src/ api/ tests/

format:
	@echo "✨ Formatting..."
	uv run black src/ api/ tests/
	uv run ruff check --fix src/ api/ tests/

type-check:
	@echo "🔍 Type checking..."
	uv run mypy src/ api/

clean:
	@echo "🧹 Cleaning..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

reset-db:
	@echo "🗄️ Resetting database..."
	rm -f data/pink_floyd_songs.db
	uv run python scripts/setup_database.py

logs:
	@echo "📋 Viewing logs..."
	tail -f logs/*.log 2>/dev/null || echo "No logs found"
