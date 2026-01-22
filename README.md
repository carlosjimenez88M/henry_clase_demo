# Pink Floyd AI Agent Demo

**Orchestration and Autonomous Agents with ReAct Framework**

A production-ready AI agent system built with FastAPI, LangChain, and the ReAct (Reasoning + Acting) framework. Features Chain of Thought reasoning, REST API endpoints, comprehensive testing, and a Streamlit dashboard for interacting with Pink Floyd songs database and currency exchange tools.

---

## Quick Start

### Prerequisites

- Python 3.12+
- Docker + Docker Compose
- OpenAI API key
- UV package manager (recommended)

### Option 1: Docker (Recommended)

```bash
# Clone and setup
git clone <repository-url>
cd henry_clase_demo

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY=sk-...

# Build and start services
docker compose build
docker compose up

# Access services:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Dashboard: http://localhost:8501

# Run tests
docker compose -f docker-compose.test.yml up

# Stop services
docker compose down
```

### Option 2: Local Development

```bash
# Install dependencies
make install

# Setup database
make setup

# Run API server (Terminal 1)
make run-api

# Run dashboard (Terminal 2)
make run-dashboard

# Run tests
make test
```

### Quick Commands

```bash
make help              # Show all available commands
make init              # Full setup (install + database)
make dev               # Run API + Dashboard concurrently
make test              # Run all tests with coverage
make docker-build      # Build Docker images
make docker-up         # Start all services
make clean             # Clean generated files
```

---

## System Architecture

### Modern Stack

- **FastAPI REST API**: High-performance async API with OpenAPI documentation
- **Chain of Thought (CoT)**: Explicit reasoning with UNDERSTAND → PLAN → EXECUTE → REFLECT → SYNTHESIZE steps
- **Docker Microservices**: Containerized API, Dashboard, and Test services
- **Comprehensive Testing**: Unit, integration, and E2E tests with >80% coverage
- **Production Features**: Rate limiting, security headers, persistent storage, query caching
- **Streamlit Dashboard**: Interactive UI consuming REST API
- **LangChain Framework**: Agent orchestration with custom tools

### Services

1. **API Service** (Port 8000)
   - FastAPI application with 5 routers
   - Chain of Thought agents by default
   - Persistent execution history (SQLite)
   - Query cache (LRU + TTL)
   - Rate limiting (60 req/min)
   - Security headers and CORS

2. **Dashboard Service** (Port 8501)
   - Streamlit web interface
   - Real-time agent interaction via API
   - Model comparison dashboard
   - Analytics and metrics visualization

3. **Test Service**
   - 40+ automated tests
   - Unit, integration, and E2E coverage
   - Pytest with fixtures and mocking

### API Endpoints

**Health & Info:**
- `GET /health` - System health check
- `GET /health/detailed` - Detailed health status

**Agent Operations:**
- `POST /api/v1/agent/query` - Execute agent query
- `GET /api/v1/agent/history` - Query execution history
- `GET /api/v1/agent/models` - List available models

**Database:**
- `GET /api/v1/database/songs` - Search Pink Floyd songs
- `GET /api/v1/database/songs/{id}` - Get specific song

**Comparison:**
- `POST /api/v1/comparison/run` - Run model comparison
- `GET /api/v1/comparison/results` - Get comparison results

**Metrics:**
- `GET /api/v1/metrics/summary` - Execution metrics summary
- `GET /api/v1/metrics/cache` - Cache statistics
- `GET /api/v1/metrics/storage` - Storage statistics

---

## ReAct Framework Explained

The **ReAct** framework combines **Reasoning** and **Acting** to create transparent, autonomous agents:

### ReAct Loop

```
1. THOUGHT: Agent reasons about what to do
   "User wants melancholic Pink Floyd songs.
    I should query the database with mood='melancholic'"

2. ACTION: Agent selects and uses a tool
   Tool: pink_floyd_database
   Input: {"query": "melancholic songs"}

3. OBSERVATION: Agent receives tool output
   Found 7 songs: Time, Comfortably Numb, Wish You Were Here...

4. REPEAT or ANSWER: Continue reasoning or provide final response
```

### Chain of Thought (CoT) Enhancement

This implementation includes explicit Chain of Thought reasoning:

**5-Step CoT Process:**
1. **UNDERSTAND**: Comprehend the query, identify requirements
2. **PLAN**: Decide approach, select tools, assess confidence
3. **EXECUTE**: Use tools, validate each result
4. **REFLECT**: Check completeness, identify gaps
5. **SYNTHESIZE**: Formulate final answer with confidence level

**Key Features:**
- Confidence levels: HIGH / MEDIUM / LOW
- Alternative approaches documented
- Assumptions explicitly stated
- Reasoning validation and quality scoring
- Self-correction loop for poor reasoning

---

## Custom Tools Design

### 1. Pink Floyd Database Tool

Query 28 iconic Pink Floyd songs with natural language:

```python
class PinkFloydDatabaseTool(BaseTool):
    name = "pink_floyd_database"
    description = """
    Query Pink Floyd songs by:
    - Mood: melancholic, energetic, psychedelic, progressive, dark
    - Album: The Dark Side of the Moon, The Wall, Wish You Were Here, etc.
    - Lyrics: keyword search in song lyrics
    - Year: specific year or decade (1960s, 1970s, 1980s)

    Returns formatted list of matching songs with details.
    """
```

**Database Features:**
- 28 curated Pink Floyd songs
- SQLite with indexed search
- Fields: title, album, year, lyrics, mood, duration
- Natural language query parsing

**Example Queries:**
- "Find melancholic songs from the 1970s"
- "Show me songs from The Dark Side of the Moon"
- "What psychedelic songs mention space?"

### 2. Currency Price Tool

Real-time currency exchange rates with caching:

```python
class CurrencyPriceTool(BaseTool):
    name = "currency_price_checker"
    description = """
    Get real-time currency exchange rates.
    Supports: USD, EUR, GBP, JPY, CHF, CAD, AUD, MXN, BRL, CNY

    Returns current exchange rate with timestamp and conversion examples.
    """
```

**Features:**
- Real-time API integration (exchangerate-api.com)
- 5-minute caching for performance
- Fallback to mock data for reliability
- Supports 10+ major currencies
- Natural language parsing ("100 dollars in euros")

**Example Queries:**
- "What's the USD to EUR exchange rate?"
- "How much is 100 dollars in British pounds?"
- "Convert 50 euros to Japanese yen"

---

## Model Comparison

Compare performance across three OpenAI models:

| Model | Speed | Cost (per 1M tokens) | Use Case |
|-------|-------|---------------------|----------|
| **gpt-4o-mini** | Fast | $0.15 input / $0.60 output | Development, testing |
| **gpt-4o** | Moderate | $2.50 input / $10.00 output | Production, complex queries |
| **gpt-5-nano** | Very Fast | $0.10 input / $0.40 output | High-volume, simple tasks |

### Running Comparisons

```bash
# Run full comparison (8 test queries)
python scripts/run_comparison.py

# Compare specific models
python scripts/run_comparison.py --models gpt-4o-mini,gpt-4o

# Save results
python scripts/run_comparison.py --output results/comparison.json
```

### Metrics Tracked

- Response time (seconds)
- Token usage (input + output)
- Cost estimation (USD)
- Success rate
- Reasoning steps count
- Tool usage patterns

---

## Project Structure

```
henry_clase_demo/
├── api/                        # FastAPI REST API
│   ├── main.py                 # FastAPI app entry point
│   ├── core/                   # Configuration and utilities
│   │   ├── config.py           # Settings with Pydantic
│   │   └── logger.py           # Colored logging
│   ├── middleware/             # Middleware components
│   │   ├── rate_limiter.py     # Rate limiting (60 req/min)
│   │   ├── security_headers.py # Security headers
│   │   └── request_logger.py   # Request logging
│   ├── routers/                # API endpoints
│   │   ├── health.py           # Health checks
│   │   ├── agent.py            # Agent operations
│   │   ├── database.py         # Database queries
│   │   ├── comparison.py       # Model comparison
│   │   └── metrics.py          # Metrics endpoints
│   ├── schemas/                # Pydantic models
│   ├── services/               # Business logic
│   ├── storage/                # Persistent storage
│   └── cache/                  # Query caching
│
├── src/                        # Core agent logic
│   ├── agents/                 # Agent implementations
│   │   ├── react_agent.py      # Standard ReAct agent
│   │   ├── cot_agent.py        # CoT-enhanced agent
│   │   ├── agent_factory.py    # Agent creation
│   │   ├── agent_executor.py   # Execution with metrics
│   │   ├── reasoning_validator.py # Quality validation
│   │   ├── reflection_loop.py  # Self-correction
│   │   └── prompts/            # CoT prompt templates
│   ├── tools/                  # Custom tools
│   │   ├── database_tool.py    # Pink Floyd DB
│   │   └── currency_tool.py    # Currency exchange
│   ├── database/               # Database management
│   └── comparison/             # Comparison framework
│
├── dashboard/                  # Streamlit UI
│   ├── app.py                  # Main dashboard
│   ├── design_system.py        # Professional theme
│   ├── history_manager.py      # Persistent history
│   └── pages/                  # Dashboard pages
│       ├── 1_Live_Agent.py     # Interactive agent
│       ├── 2_Model_Comparison.py # Comparison UI
│       ├── 3_Architecture.py   # System documentation
│       └── 4_Analytics.py      # Metrics dashboard
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests (21+ tests)
│   ├── integration/            # Integration tests (18+ tests)
│   └── e2e/                    # E2E tests (3+ tests)
│
├── docker/                     # Docker configuration
│   ├── Dockerfile.api          # API image
│   ├── Dockerfile.dashboard    # Dashboard image
│   └── Dockerfile.tests        # Test runner image
│
├── notebooks/                  # Jupyter notebooks
│   └── react_deep_dive.ipynb   # Educational notebook
│
├── scripts/                    # Utility scripts
│   ├── setup_database.py       # Initialize database
│   └── run_comparison.py       # Run model comparison
│
├── docker-compose.yml          # Production compose
├── docker-compose.dev.yml      # Development mode
├── docker-compose.test.yml     # Test environment
├── Makefile                    # Automation commands
├── pyproject.toml              # Dependencies (uv)
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## Development

### Environment Setup

```bash
# Install UV package manager (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
make install

# Setup database
make setup

# Full initialization
make init
```

### Running Services

```bash
# Run API only
make run-api

# Run Dashboard only
make run-dashboard

# Run both concurrently
make dev

# With Docker
make docker-dev
```

### Testing

```bash
# Run all tests
make test

# Run specific test suites
make test-unit
make test-integration
make test-e2e

# Generate coverage report
make coverage-html

# Run tests in Docker
make docker-test
```

### Code Quality

```bash
# Linting
make lint

# Format code
make format

# Type checking
make type-check
```

---

## Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...           # Required: Your OpenAI API key

# API Configuration
API_HOST=0.0.0.0                # API host (default: 0.0.0.0)
API_PORT=8000                   # API port (default: 8000)
API_ENV=development             # Environment (development/production)
LOG_LEVEL=INFO                  # Logging level

# Database
DATABASE_PATH=data/pink_floyd_songs.db  # SQLite database path

# CORS (adjust for production)
CORS_ORIGINS=["http://localhost:8501","http://localhost:8000"]

# Model Defaults
DEFAULT_MODEL=gpt-4o-mini       # Default OpenAI model
DEFAULT_TEMPERATURE=0.1         # Temperature for responses
DEFAULT_MAX_ITERATIONS=5        # Max agent iterations
```

### Model Configuration

Models are configured in `src/config.py`:

```python
models = {
    "gpt-4o-mini": {
        "temperature": 0.1,
        "max_tokens": 2000,
        "pricing": {
            "input": 0.15,    # per 1M tokens
            "output": 0.60
        }
    },
    "gpt-4o": {
        "temperature": 0.1,
        "max_tokens": 4000,
        "pricing": {
            "input": 2.50,
            "output": 10.00
        }
    }
}
```

---

## Production Deployment

### Docker Production Deployment

```bash
# Build production images
docker compose build

# Start services
docker compose up -d

# Check logs
docker compose logs -f

# Stop services
docker compose down
```

### Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed status
curl http://localhost:8000/health/detailed

# Check metrics
curl http://localhost:8000/api/v1/metrics/summary
```

### Monitoring

The API includes built-in monitoring:

- Request logging with colored output
- Execution history tracking
- Cache performance metrics
- Storage statistics
- Rate limiting status

Access metrics at: `http://localhost:8000/api/v1/metrics/*`

---

## Example Queries

### Database Queries

```python
# Simple mood query
"Find melancholic Pink Floyd songs"
# Returns: Time, Comfortably Numb, Wish You Were Here...

# Album-specific query
"Show me songs from The Dark Side of the Moon"
# Returns: Time, Money, Us and Them, Brain Damage, Eclipse

# Complex query with multiple criteria
"What psychedelic songs are from the 1960s?"
# Returns: Astronomy Domine, Interstellar Overdrive

# Lyrics search
"Songs with lyrics about time"
# Returns: Time, Us and Them
```

### Currency Queries

```python
# Simple exchange rate
"What's the USD to EUR exchange rate?"
# Returns: 1 USD = 0.85 EUR (with timestamp)

# Conversion with amount
"How much is 100 dollars in British pounds?"
# Returns: 100 USD = 79.23 GBP

# Multiple currencies
"Compare USD to JPY and EUR"
# Returns rates for both pairs
```

### Combined Queries (Multi-Tool)

```python
# Query requiring both tools
"I want energetic Pink Floyd music and the current EUR price in USD"
# Agent uses:
# 1. pink_floyd_database for music
# 2. currency_price_checker for exchange rate
```

---

## Testing

### Test Coverage

- **Unit Tests**: 21+ tests (60% coverage)
  - Agent factory and executor
  - Tools (database, currency)
  - Configuration and utilities

- **Integration Tests**: 18+ tests (25% coverage)
  - API endpoints
  - Database operations
  - Service layer

- **E2E Tests**: 3+ tests (15% coverage)
  - Complete agent workflows
  - API integration
  - CoT reasoning traces

### Running Tests

```bash
# All tests with coverage
pytest tests/ --cov=src --cov=api --cov-report=html

# Specific test file
pytest tests/unit/test_agent_factory.py -v

# E2E tests only
pytest tests/e2e/ -v

# With Docker
docker compose -f docker-compose.test.yml up
```

---

## Key Technologies

- **Python 3.12**: Modern Python with type hints
- **FastAPI**: High-performance async web framework
- **LangChain**: LLM application framework
- **OpenAI API**: GPT models (gpt-4o-mini, gpt-4o, gpt-5-nano)
- **Streamlit**: Interactive web dashboard
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation and settings
- **Docker**: Containerization
- **Pytest**: Testing framework
- **UV**: Fast Python package manager
- **Loguru**: Beautiful logging

---

## Contributing

### Code Style

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions/classes
- Keep functions small and focused
- Test all new features

### Pull Request Process

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit pull request with clear description

---

## References

- **ReAct Paper**: [Yao et al., 2022 - ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
- **Chain of Thought**: [Wei et al., 2022 - Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903)
- **LangChain Documentation**: [python.langchain.com](https://python.langchain.com)
- **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Streamlit**: [streamlit.io](https://streamlit.io)

---

## License

This project is created for educational purposes as part of the Henry bootcamp coursework.

---

## About

**Pink Floyd Edition** - A tribute to one of the greatest progressive rock bands, demonstrating how AI agents can interact with structured knowledge (music catalog) while accessing real-time information (currency exchange rates).

Built for the **Henry Class Demo** on Orchestration and Autonomous Agents with the ReAct framework and Chain of Thought reasoning.
