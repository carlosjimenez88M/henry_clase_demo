# Pink Floyd AI Agent API Documentation

## Overview

RESTful API for the Pink Floyd AI Agent, providing endpoints for:
- Agent query execution with ReAct framework
- Pink Floyd database search and statistics
- Model performance comparison
- Health checks and monitoring

**Base URL**: `http://localhost:8000`
**Documentation**: `http://localhost:8000/docs` (Swagger UI)

---

## Authentication

Currently, no authentication is required. The API uses the configured OpenAI API key for LLM calls.

---

## Endpoints

### Health Checks

#### GET /health
Basic health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-22T10:30:45Z"
}
```

#### GET /health/ready
Readiness probe with component checks.

**Response**:
```json
{
  "status": "ready",
  "version": "1.0.0",
  "timestamp": "2026-01-22T10:30:45Z",
  "checks": {
    "database": "ok",
    "openai_key": "configured"
  }
}
```

---

### Agent Endpoints

#### POST /api/v1/agent/query
Execute a query with the AI agent.

**Request**:
```json
{
  "query": "Find melancholic Pink Floyd songs from the 1970s",
  "model": "gpt-4o-mini",
  "temperature": 0.1,
  "max_iterations": 5
}
```

**Response**:
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "query": "Find melancholic Pink Floyd songs from the 1970s",
  "answer": "Based on the Pink Floyd database...",
  "reasoning_trace": [
    {
      "step": 1,
      "type": "action",
      "content": "Search database",
      "tool": "pink_floyd_database",
      "input": {"mood": "melancholic"}
    }
  ],
  "metrics": {
    "model": "gpt-4o-mini",
    "execution_time_seconds": 2.34,
    "estimated_tokens": {"total": 700},
    "estimated_cost_usd": 0.0014,
    "num_steps": 3,
    "tools_used": ["pink_floyd_database"]
  },
  "timestamp": "2026-01-22T10:30:45Z"
}
```

#### GET /api/v1/agent/models
Get list of available AI models.

**Response**:
```json
[
  {
    "name": "gpt-4o-mini",
    "display_name": "GPT-4o Mini",
    "description": "Fast and cost-effective model",
    "max_tokens": 128000,
    "cost_per_1k_tokens": {
      "prompt": 0.00015,
      "completion": 0.0006
    }
  }
]
```

#### GET /api/v1/agent/history
Get execution history.

**Query Parameters**:
- `limit` (optional): Maximum results (default: 50)

**Response**:
```json
{
  "total": 42,
  "executions": [
    {
      "execution_id": "550e8400-e29b-41d4-a716-446655440000",
      "query": "Find melancholic songs",
      "timestamp": "2026-01-22T10:30:45Z",
      "model": "gpt-4o-mini",
      "execution_time": 2.34
    }
  ]
}
```

---

### Database Endpoints

#### GET /api/v1/database/songs
Get songs with pagination and filtering.

**Query Parameters**:
- `limit` (optional): Max results (1-100, default: 10)
- `offset` (optional): Pagination offset (default: 0)
- `mood` (optional): Filter by mood
- `album` (optional): Filter by album
- `year` (optional): Filter by year

**Example**: `/api/v1/database/songs?mood=melancholic&limit=5`

**Response**:
```json
{
  "total": 28,
  "songs": [
    {
      "id": 1,
      "title": "Time",
      "album": "The Dark Side of the Moon",
      "year": 1973,
      "mood": "melancholic",
      "lyrics": "Ticking away..."
    }
  ],
  "limit": 10,
  "offset": 0
}
```

#### POST /api/v1/database/search
Advanced search with multiple criteria.

**Request**:
```json
{
  "query": "time",
  "mood": "melancholic",
  "year_min": 1970,
  "year_max": 1979,
  "limit": 10,
  "offset": 0
}
```

#### GET /api/v1/database/stats
Get database statistics.

**Response**:
```json
{
  "total_songs": 28,
  "total_albums": 5,
  "year_range": {"min": 1967, "max": 1979},
  "moods": {
    "melancholic": 10,
    "energetic": 8
  },
  "albums": {
    "The Dark Side of the Moon": 10
  }
}
```

---

### Comparison Endpoints

#### POST /api/v1/comparison/run
Run performance comparison between models.

**Request**:
```json
{
  "models": ["gpt-4o-mini", "gpt-4o"],
  "verbose": true
}
```

**Response**:
```json
{
  "comparison_id": "550e8400-e29b-41d4-a716-446655440000",
  "models": ["gpt-4o-mini", "gpt-4o"],
  "summary": {
    "gpt-4o-mini": {
      "model": "gpt-4o-mini",
      "total_queries": 10,
      "success_rate": 0.9,
      "avg_execution_time": 2.34,
      "total_cost_usd": 0.014,
      "avg_steps": 3.2,
      "tool_usage": {"pink_floyd_database": 8}
    }
  },
  "timestamp": "2026-01-22T10:30:45Z",
  "total_duration": 45.6
}
```

---

## Error Handling

All errors follow a consistent format:

```json
{
  "error": "Error Type",
  "detail": "Detailed error message",
  "status_code": 400
}
```

**Common Status Codes**:
- `200`: Success
- `400`: Bad Request (validation error)
- `404`: Not Found
- `422`: Unprocessable Entity (Pydantic validation)
- `500`: Internal Server Error

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production deployments.

---

## Examples

### cURL Examples

```bash
# Health check
curl http://localhost:8000/health

# Execute agent query
curl -X POST http://localhost:8000/api/v1/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find melancholic Pink Floyd songs",
    "model": "gpt-4o-mini"
  }'

# Search database
curl -X POST http://localhost:8000/api/v1/database/search \
  -H "Content-Type: application/json" \
  -d '{
    "mood": "melancholic",
    "limit": 5
  }'
```

### Python Examples

```python
import httpx

# Execute agent query
response = httpx.post(
    "http://localhost:8000/api/v1/agent/query",
    json={
        "query": "Find melancholic Pink Floyd songs",
        "model": "gpt-4o-mini"
    },
    timeout=60.0
)

if response.status_code == 200:
    result = response.json()
    print(result["answer"])
```
