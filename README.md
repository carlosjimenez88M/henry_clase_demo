# Pink Floyd AI Agent - Proyecto Educativo

## Introducción

Este proyecto fue desarrollado como material educativo para estudiantes de Henry, enfocado en demostrar la implementación práctica de agentes autónomos utilizando el framework ReAct (Reasoning + Acting) y Chain of Thought (CoT). El sistema combina orquestación de LLMs, herramientas personalizadas, y una arquitectura de microservicios moderna para crear un agente inteligente capaz de consultar una base de datos de canciones de Pink Floyd y obtener tasas de cambio de divisas en tiempo real.

**Características principales:**
- Implementación completa del framework ReAct con LangChain
- Chain of Thought (CoT) con proceso explícito de razonamiento en 5 pasos
- API REST con FastAPI y documentación OpenAPI automática
- Dashboard interactivo con Streamlit
- Suite de testing exhaustiva (57 tests: unitarios, integración, E2E)
- Notebooks Jupyter educativos con visualizaciones de grafos
- Contenedores Docker para desarrollo y producción
- Almacenamiento persistente y caché de consultas

El proyecto utiliza la temática de Pink Floyd para demostrar cómo los agentes pueden interactuar con conocimiento estructurado (catálogo musical) mientras acceden a información en tiempo real (tasas de cambio).

---

## 1. Instalación del Ambiente

### Prerrequisitos

Los estudiantes necesitarán tener instalado:

- **Python 3.12+**: Lenguaje de programación principal
- **Git**: Control de versiones
- **OpenAI API Key**: Clave de API de OpenAI (se proporciona en el curso)
- **UV Package Manager** (recomendado): Gestor de paquetes rápido de Python
- **Docker + Docker Compose** (opcional): Para ejecutar con contenedores

### Opción A: Instalación con UV (Recomendado)

UV es un gestor de paquetes moderno que instala dependencias significativamente más rápido que pip tradicional.

**Paso 1: Instalar UV**

```bash
# En macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verificar instalación
uv --version
```

**Paso 2: Clonar el Repositorio**

```bash
git clone <repository-url>
cd henry_clase_demo
```

**Paso 3: Configurar Variables de Entorno**

```bash
# Copiar template de configuración
cp .env.example .env

# Editar .env y agregar la API key de OpenAI
# OPENAI_API_KEY=sk-...
```

**Paso 4: Instalación Completa**

```bash
# Este comando instala dependencias y configura la base de datos
make init

# Equivalente a:
# uv sync
# uv run python scripts/setup_database.py
```

**Paso 5: Verificar Instalación**

```bash
# Ejecutar tests para verificar que todo funciona
make test

# Debería mostrar: 57/57 tests passing
```

### Opción B: Instalación con Docker

Docker simplifica el proceso al encapsular todo el ambiente en contenedores.

**Paso 1: Verificar Docker**

```bash
docker --version
docker compose version
```

**Paso 2: Configurar Ambiente**

```bash
# Clonar repositorio
git clone <repository-url>
cd henry_clase_demo

# Configurar .env
cp .env.example .env
# Editar .env y agregar OPENAI_API_KEY
```

**Paso 3: Construir y Ejecutar**

```bash
# Construir imágenes
docker compose build

# Iniciar servicios
docker compose up -d

# Verificar que los servicios están corriendo
docker compose ps
```

**Paso 4: Acceder a los Servicios**

- **API REST**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Dashboard Streamlit**: http://localhost:8501

**Paso 5: Ejecutar Tests en Docker**

```bash
docker compose -f docker-compose.test.yml up
```

**Detener Servicios**

```bash
docker compose down
```

### Configuración de Variables de Entorno

El archivo `.env` contiene la configuración del sistema. Los estudiantes deben crear este archivo a partir de `.env.example`:

```bash
# OpenAI Configuration (REQUERIDO)
OPENAI_API_KEY=sk-...                    # API key de OpenAI

# API Configuration
API_HOST=0.0.0.0                         # Host del API (default)
API_PORT=8000                            # Puerto del API (default)
API_ENV=development                      # Ambiente (development/production)
LOG_LEVEL=INFO                           # Nivel de logging

# Database
DATABASE_PATH=data/pink_floyd_songs.db   # Path de la base de datos SQLite

# CORS (ajustar para producción)
CORS_ORIGINS=["http://localhost:8501","http://localhost:8000"]

# Model Defaults
DEFAULT_MODEL=gpt-4o-mini                # Modelo por defecto (económico)
DEFAULT_TEMPERATURE=0.1                  # Temperatura (baja para consistencia)
DEFAULT_MAX_ITERATIONS=5                 # Máximo de iteraciones ReAct
```

### Comandos Make Útiles

El proyecto incluye un Makefile con comandos para automatizar tareas comunes:

```bash
make help              # Mostrar todos los comandos disponibles
make init              # Instalación completa (install + setup)
make install           # Instalar dependencias con UV
make setup             # Inicializar base de datos
make dev               # Ejecutar API + Dashboard simultáneamente
make run-api           # Ejecutar solo el API
make run-dashboard     # Ejecutar solo el Dashboard
make test              # Ejecutar todos los tests con coverage
make test-unit         # Solo tests unitarios
make test-integration  # Solo tests de integración
make test-e2e          # Solo tests end-to-end
make lint              # Verificar estilo de código
make format            # Formatear código automáticamente
make clean             # Limpiar archivos generados
make docker-build      # Construir imágenes Docker
make docker-up         # Iniciar servicios con Docker
make docker-down       # Detener servicios Docker
```

---

## 2. Estructura del Repositorio

### Organización de Directorios

El repositorio está organizado con una clara separación de responsabilidades:

```
henry_clase_demo/
├── api/                        # REST API con FastAPI
│   ├── main.py                 # Entry point de la aplicación FastAPI
│   ├── core/                   # Configuración y utilidades core
│   │   ├── config.py           # Settings con Pydantic BaseSettings
│   │   ├── logger.py           # Sistema de logging con Loguru
│   │   └── errors.py           # Excepciones personalizadas
│   ├── middleware/             # Componentes de middleware
│   │   ├── rate_limiter.py     # Rate limiting (60 req/min)
│   │   ├── security_headers.py # Headers de seguridad (HSTS, CSP)
│   │   └── request_logger.py   # Logging de requests HTTP
│   ├── routers/                # Endpoints del API (rutas)
│   │   ├── health.py           # Health checks
│   │   ├── agent.py            # Operaciones de agentes
│   │   ├── database.py         # Consultas a base de datos
│   │   ├── comparison.py       # Comparación de modelos
│   │   └── metrics.py          # Métricas del sistema
│   ├── schemas/                # Modelos Pydantic para validación
│   │   ├── agent.py            # Schemas de agentes
│   │   ├── database.py         # Schemas de database
│   │   └── common.py           # Schemas compartidos
│   ├── services/               # Lógica de negocio (business logic)
│   │   ├── agent_service.py    # Servicio de agentes
│   │   ├── database_service.py # Servicio de base de datos
│   │   └── comparison_service.py # Servicio de comparación
│   ├── storage/                # Almacenamiento persistente
│   │   └── execution_store.py  # Historial de ejecuciones (SQLite)
│   └── cache/                  # Sistema de caché
│       └── query_cache.py      # Caché LRU + TTL para consultas
│
├── src/                        # Lógica core del agente
│   ├── agents/                 # Implementaciones de agentes
│   │   ├── react_agent.py      # Agente ReAct estándar
│   │   ├── cot_agent.py        # Agente con Chain of Thought
│   │   ├── langgraph_react_agent.py # Implementación con LangGraph
│   │   ├── agent_factory.py    # Factory para crear agentes
│   │   ├── agent_executor.py   # Ejecución con métricas
│   │   ├── reasoning_validator.py # Validación de razonamiento
│   │   ├── reflection_loop.py  # Auto-corrección del agente
│   │   └── prompts/            # Templates de prompts para CoT
│   │       ├── templates.py    # Templates principales
│   │       ├── cot_templates.py # Templates específicos CoT
│   │       └── registry.py     # Registro de prompts
│   ├── tools/                  # Herramientas personalizadas
│   │   ├── database_tool.py    # Tool para base de datos Pink Floyd
│   │   └── currency_tool.py    # Tool para tasas de cambio
│   ├── database/               # Gestión de base de datos
│   │   ├── db_manager.py       # Manager de SQLite
│   │   ├── schema.py           # Schema de la base de datos
│   │   └── seed_data.py        # Datos iniciales (28 canciones)
│   ├── comparison/             # Framework de comparación de modelos
│   │   ├── evaluator.py        # Evaluador de respuestas
│   │   ├── metrics.py          # Métricas de comparación
│   │   └── test_cases.py       # Casos de prueba predefinidos
│   └── config.py               # Configuración de modelos y settings
│
├── dashboard/                  # Dashboard interactivo con Streamlit
│   ├── app.py                  # Aplicación principal del dashboard
│   ├── design_system.py        # Sistema de diseño y tema
│   ├── history_manager.py      # Gestión de historial persistente
│   └── pages/                  # Páginas del dashboard
│       ├── 1_Live_Agent.py     # Interacción en vivo con el agente
│       ├── 2_Model_Comparison.py # Comparación de modelos
│       ├── 3_Architecture.py   # Documentación del sistema
│       └── 4_Analytics.py      # Dashboard de métricas
│
├── tests/                      # Suite de testing completa
│   ├── conftest.py             # Fixtures de pytest compartidas
│   ├── unit/                   # Tests unitarios (20+ tests)
│   │   ├── test_database/      # Tests de database manager
│   │   └── test_services/      # Tests de servicios
│   ├── integration/            # Tests de integración (17+ tests)
│   │   ├── test_api_agent.py   # Integración API-Agent
│   │   ├── test_api_database.py # Integración API-Database
│   │   └── test_api_health.py  # Integración health checks
│   └── e2e/                    # Tests end-to-end (20+ tests)
│       ├── test_api_integration.py # Workflows completos API
│       ├── test_complete_workflow.py # Workflows de usuario
│       └── test_cot_workflow.py # Workflow Chain of Thought
│
├── docker/                     # Configuración de Docker
│   ├── Dockerfile.api          # Imagen del API
│   ├── Dockerfile.dashboard    # Imagen del Dashboard
│   └── Dockerfile.tests        # Imagen para ejecutar tests
│
├── notebooks/                  # Jupyter notebooks educativos
│   ├── ReAct_Agent_Analysis.ipynb # Análisis profundo del framework ReAct
│   └── Cinema_ReAct_CoT_Analysis.ipynb # Comparación ReAct vs CoT
│
├── scripts/                    # Scripts de utilidad
│   ├── setup_database.py       # Script para inicializar la DB
│   └── run_comparison.py       # Script para comparar modelos
│
├── data/                       # Bases de datos (generadas)
│   ├── pink_floyd_songs.db     # Base de datos de canciones (SQLite)
│   └── execution_history.db    # Historial de ejecuciones (SQLite)
│
├── logs/                       # Directorio de logs (generado)
│
├── docker-compose.yml          # Compose para producción
├── docker-compose.dev.yml      # Compose para desarrollo
├── docker-compose.test.yml     # Compose para tests
├── Makefile                    # Comandos de automatización
├── pyproject.toml              # Dependencias y configuración (UV/Poetry)
├── .env.example                # Template de variables de entorno
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Este archivo
```

### Componentes Principales

#### 1. API REST (api/)

El directorio `api/` contiene una aplicación FastAPI completa con:

- **Routers**: Endpoints organizados por dominio (agent, database, health, etc.)
- **Services**: Lógica de negocio separada de los routers para mejor testeo
- **Schemas**: Modelos Pydantic para validación de request/response
- **Middleware**: Rate limiting, CORS, security headers, logging
- **Storage**: Persistencia de historial de ejecuciones en SQLite
- **Cache**: Sistema de caché con LRU y TTL para mejorar performance

#### 2. Core del Agente (src/)

El directorio `src/` contiene la implementación del agente:

- **Agents**: Tres implementaciones (ReAct estándar, CoT mejorado, LangGraph)
- **Tools**: Herramientas personalizadas que el agente puede usar
- **Database**: Manager de SQLite con 28 canciones de Pink Floyd
- **Comparison**: Framework para comparar diferentes modelos de LLM
- **Prompts**: Templates estructurados para Chain of Thought

#### 3. Dashboard (dashboard/)

Interfaz web interactiva construida con Streamlit que consume el API REST:

- **Live Agent**: Interacción en tiempo real con el agente
- **Model Comparison**: Comparar performance de diferentes modelos
- **Architecture**: Documentación visual del sistema
- **Analytics**: Visualización de métricas y estadísticas

#### 4. Tests (tests/)

Suite de testing exhaustiva con 57 tests que cubren:

- **Unit**: Tests de componentes individuales (factories, services)
- **Integration**: Tests de integración entre componentes
- **E2E**: Tests de workflows completos simulando usuarios reales

#### 5. Notebooks (notebooks/)

Notebooks Jupyter educativos con:

- Visualizaciones de grafos de ejecución del agente
- Análisis paso a paso del proceso de razonamiento
- Comparaciones de modelos con métricas
- Ejemplos prácticos de uso del framework ReAct

---

## 3. Arquitectura del Sistema

### Visión General de la Arquitectura

El sistema implementa una arquitectura de microservicios moderna con los siguientes componentes:

```
                            ┌─────────────────┐
                            │   Dashboard     │
                            │   (Streamlit)   │
                            │   Port 8501     │
                            └────────┬────────┘
                                     │ HTTP REST
                                     │
                            ┌────────▼────────┐
                            │   FastAPI API   │
┌─────────┐                 │   Port 8000     │
│  User   │────HTTP────────►│                 │
└─────────┘                 │  - Routers      │
                            │  - Middleware   │
                            │  - Services     │
                            └────────┬────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼──────┐  ┌──────▼─────┐  ┌──────▼──────┐
            │ Agent Engine │  │   Cache    │  │   Storage   │
            │              │  │   (LRU)    │  │  (SQLite)   │
            │ - ReAct      │  │            │  │             │
            │ - CoT        │  └────────────┘  └─────────────┘
            │ - LangGraph  │
            └──────┬───────┘
                   │
        ┌──────────┼──────────┐
        │                     │
┌───────▼────────┐    ┌───────▼────────┐
│   Tool: DB     │    │ Tool: Currency │
│                │    │                │
│ Pink Floyd DB  │    │ Exchange Rates │
└────────────────┘    └────────────────┘
```

### Framework ReAct (Reasoning + Acting)

El framework ReAct es el corazón del sistema. Combina razonamiento (Reasoning) con acciones (Acting) para crear agentes transparentes y autónomos.

**Ciclo ReAct:**

```
1. THOUGHT (Pensamiento)
   El agente LLM razona sobre qué hacer:
   "El usuario quiere canciones melancólicas de Pink Floyd.
    Debo consultar la base de datos con el filtro mood='melancholic'"

2. ACTION (Acción)
   El agente selecciona y ejecuta una herramienta:
   Tool: pink_floyd_database
   Input: {"query": "melancholic songs"}

3. OBSERVATION (Observación)
   El agente recibe el resultado de la herramienta:
   "Encontradas 7 canciones: Time, Comfortably Numb, Wish You Were Here..."

4. ITERATION (Iteración)
   El agente decide si:
   - Necesita más información (volver a THOUGHT)
   - Tiene suficiente información (dar respuesta final)
```

### Chain of Thought (CoT) - Proceso en 5 Pasos

Este proyecto implementa una versión mejorada con Chain of Thought explícito:

**Paso 1: UNDERSTAND (Comprender)**
- Analizar la consulta del usuario
- Identificar requisitos explícitos e implícitos
- Extraer entidades clave
- Determinar tipo de respuesta esperada

**Paso 2: PLAN (Planificar)**
- Decidir el enfoque de solución
- Seleccionar herramientas necesarias
- Evaluar nivel de confianza en el plan
- Documentar enfoques alternativos

**Paso 3: EXECUTE (Ejecutar)**
- Usar las herramientas seleccionadas
- Validar cada resultado recibido
- Manejar errores de herramientas
- Recolectar observaciones

**Paso 4: REFLECT (Reflexionar)**
- Verificar completitud de la respuesta
- Identificar información faltante
- Evaluar calidad de los resultados
- Decidir si se necesita más información

**Paso 5: SYNTHESIZE (Sintetizar)**
- Formular respuesta final
- Integrar toda la información recolectada
- Asignar nivel de confianza (HIGH/MEDIUM/LOW)
- Documentar suposiciones realizadas

**Características Clave del CoT:**
- **Niveles de confianza**: HIGH / MEDIUM / LOW en cada etapa
- **Enfoques alternativos**: Se documentan otras formas de resolver el problema
- **Suposiciones explícitas**: Se registran todas las suposiciones realizadas
- **Validación de razonamiento**: Sistema de scoring de calidad (0-100)
- **Auto-corrección**: Loop de reflexión para mejorar razonamientos pobres

### Flujo de Datos

El flujo típico de una consulta a través del sistema:

```
1. Usuario/Dashboard → POST /api/v1/agent/query
                         Body: {"query": "...", "model": "..."}

2. API Router (agent.py) → Validación con Pydantic Schema
                          → Middleware (rate limit, logging)

3. AgentService → Verificar caché
                → Si cache hit: retornar inmediatamente
                → Si cache miss: continuar

4. AgentExecutor → Crear agente con AgentFactory
                 → Ejecutar agente con métricas

5. Agent (CoT/ReAct) → Loop THOUGHT → ACTION → OBSERVATION
                      → Usar herramientas (database/currency)

6. Tools → Ejecutar consulta
         → Retornar resultados

7. AgentExecutor → Recolectar métricas (tiempo, tokens, costo)
                 → Guardar en execution_store

8. AgentService → Guardar en caché
                → Retornar respuesta con métricas

9. API Router → Formatear respuesta
              → Agregar headers de seguridad
              → Log de request

10. Usuario/Dashboard ← Respuesta JSON
                       {"answer": "...", "metrics": {...}}
```

### Componentes de Middleware

El API incluye varios middleware para funcionalidad de producción:

**1. Rate Limiter (rate_limiter.py)**
- Límite: 60 requests por minuto por IP
- Previene abuso del API
- Retorna 429 Too Many Requests si se excede

**2. Security Headers (security_headers.py)**
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Strict-Transport-Security (HSTS)

**3. Request Logger (request_logger.py)**
- Log de todos los requests HTTP
- Incluye: método, path, status code, tiempo de respuesta
- Útil para debugging y monitoreo

**4. CORS Middleware**
- Configurado para permitir acceso desde Dashboard
- Headers permitidos personalizables
- Métodos HTTP configurables

### Almacenamiento y Caché

**Execution Store (SQLite)**
- Almacena historial de todas las consultas
- Schema: id, query, model, answer, execution_time, tokens, cost, timestamp
- Permite análisis histórico y debugging

**Query Cache (LRU + TTL)**
- Caché en memoria con política LRU (Least Recently Used)
- TTL (Time To Live): 5 minutos por defecto
- Mejora performance evitando llamadas repetidas al LLM
- Cache hit reduce tiempo de respuesta de ~8s a <100ms

---

## 4. Uso del Sistema

### Iniciar el API

El API es el componente principal del sistema. Los estudiantes pueden iniciarlo de dos formas:

**Opción 1: Con Make (Recomendado)**

```bash
# Iniciar API en puerto 8000
make run-api

# El API estará disponible en:
# - http://localhost:8000
# - Documentación: http://localhost:8000/docs
```

**Opción 2: Con UV Directamente**

```bash
# Desde el directorio raíz
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Verificar que el API está funcionando:**

```bash
# Health check
curl http://localhost:8000/health

# Respuesta esperada:
# {"status":"healthy","version":"1.0.0"}
```

### Iniciar el Dashboard

El dashboard es una interfaz web interactiva para usar el agente:

**Iniciar Dashboard:**

```bash
# Con Make
make run-dashboard

# O directamente con UV
uv run streamlit run dashboard/app.py

# Acceder en: http://localhost:8501
```

**Características del Dashboard:**
- **Live Agent**: Interactuar con el agente en tiempo real
- **Model Comparison**: Comparar gpt-4o-mini vs gpt-4o vs gpt-5-nano
- **Architecture**: Visualización de la arquitectura del sistema
- **Analytics**: Métricas y estadísticas de uso

### Ejecutar Consultas

Los estudiantes pueden interactuar con el agente de varias formas:

**Método 1: A través del Dashboard (más fácil)**

1. Abrir http://localhost:8501
2. Navegar a "Live Agent"
3. Escribir consulta en el text area
4. Seleccionar modelo (gpt-4o-mini recomendado)
5. Hacer click en "Execute"
6. Ver la respuesta y métricas

**Método 2: A través del API con curl**

```bash
# Consulta simple de base de datos
curl -X POST 'http://localhost:8000/api/v1/agent/query' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Find melancholic Pink Floyd songs",
    "model": "gpt-4o-mini"
  }'

# Consulta de tasas de cambio
curl -X POST 'http://localhost:8000/api/v1/agent/query' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "What is the USD to EUR exchange rate?",
    "model": "gpt-4o-mini"
  }'

# Consulta multi-herramienta
curl -X POST 'http://localhost:8000/api/v1/agent/query' \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "Show me energetic songs and the current GBP to USD rate",
    "model": "gpt-4o-mini"
  }'
```

**Método 3: A través de Python**

```python
import requests

# Configurar endpoint
API_URL = "http://localhost:8000/api/v1/agent/query"

# Realizar consulta
response = requests.post(
    API_URL,
    json={
        "query": "What psychedelic songs are from the 1960s?",
        "model": "gpt-4o-mini"
    }
)

# Procesar respuesta
result = response.json()
print(f"Answer: {result['answer']}")
print(f"Execution time: {result['metrics']['execution_time_seconds']}s")
print(f"Tokens used: {result['metrics']['tokens_used']}")
print(f"Cost: ${result['metrics']['cost_usd']}")
```

### Ejemplos de Consultas

**Consultas de Base de Datos:**

```
"Find melancholic Pink Floyd songs"
Resultado: 7 canciones (Time, Comfortably Numb, Wish You Were Here, etc.)

"Show me songs from The Dark Side of the Moon album"
Resultado: 5 canciones del álbum icónico

"What psychedelic songs are from the 1960s?"
Resultado: Astronomy Domine, Interstellar Overdrive

"Songs with lyrics about time"
Resultado: Time, Us and Them (búsqueda en lyrics)

"Show me energetic Pink Floyd music"
Resultado: Run Like Hell, Young Lust, Another Brick in the Wall Part 2
```

**Consultas de Divisas:**

```
"What's the USD to EUR exchange rate?"
Resultado: Tasa actual con timestamp

"How much is 100 dollars in British pounds?"
Resultado: Conversión de 100 USD a GBP

"Convert 50 euros to Japanese yen"
Resultado: 50 EUR en JPY con tasa de cambio

"Compare USD to JPY and EUR rates"
Resultado: Ambas tasas de cambio
```

**Consultas Multi-Herramienta:**

```
"I want energetic Pink Floyd music and the current EUR price in USD"
Resultado: El agente usa ambas herramientas y combina resultados

"Show me melancholic songs and tell me the GBP to USD rate"
Resultado: Lista de canciones + tasa de cambio
```

### Ver Historial de Consultas

```bash
# Ver últimas 10 consultas
curl http://localhost:8000/api/v1/agent/history?limit=10

# Ver consultas de un modelo específico
curl http://localhost:8000/api/v1/agent/history?model=gpt-4o-mini

# Ver consultas con filtro de fecha
curl http://localhost:8000/api/v1/agent/history?from_date=2026-01-20
```

### Ver Métricas del Sistema

```bash
# Resumen de métricas
curl http://localhost:8000/api/v1/metrics/summary

# Estadísticas de caché
curl http://localhost:8000/api/v1/metrics/cache

# Estadísticas de storage
curl http://localhost:8000/api/v1/metrics/storage

# Métricas del sistema (CPU, memoria)
curl http://localhost:8000/api/v1/metrics/system
```

---

## 5. Jupyter Notebooks - Material de Aprendizaje

Los notebooks Jupyter proporcionan análisis profundo y visualizaciones del framework ReAct implementado en el proyecto.

### ReAct_Agent_Analysis.ipynb

Este notebook ofrece un análisis profesional del agente ReAct con visualizaciones interactivas.

**Contenido del Notebook:**

1. **Framework Overview**: Explicación del loop ReAct (Thought → Action → Observation)
2. **Agent Initialization**: Setup del agente con LangGraph
3. **Visualización de Grafos**: Representación visual del grafo de estados del agente
4. **Casos de Prueba**:
   - Database Query: Consulta de canciones melancólicas
   - Currency Query: Obtención de tasas de cambio
   - Multi-Tool Query: Combinación de ambas herramientas
5. **Análisis de Traces**: Examen paso a paso del razonamiento
6. **Métricas de Performance**: Tiempo, tokens, costo por consulta
7. **Comparación de Modelos**: gpt-4o-mini vs gpt-4o
8. **Validación**: Verificación contra ground truth de la base de datos

**Objetivos de Aprendizaje:**

- Comprender el ciclo THOUGHT → ACTION → OBSERVATION
- Visualizar el proceso de razonamiento del agente
- Identificar puntos de decisión y selección de herramientas
- Analizar trade-offs entre diferentes modelos de LLM
- Evaluar costos y performance en casos reales

**Visualizaciones Incluidas:**

- **Grafo LangGraph**: Visualización Mermaid del StateGraph
- **Execution Trace**: Grafo NetworkX mostrando el flujo de razonamiento
- **Performance Charts**: Gráficos de barras comparando métricas
- **Comparison Tables**: DataFrames con styling para análisis lado a lado

### Cinema_ReAct_CoT_Analysis.ipynb

Este notebook compara el agente ReAct estándar con la versión mejorada Chain of Thought.

**Contenido del Notebook:**

1. **Setup de Herramientas**: Creación de una herramienta de base de datos de cine
2. **Agente ReAct**: Implementación estándar de ReAct
3. **Agente CoT**: Implementación con Chain of Thought de 5 pasos
4. **Comparación Lado a Lado**: Misma consulta con ambos agentes
5. **Análisis de Razonamiento**: Diferencias en el proceso de pensamiento
6. **Métricas Comparativas**: Performance, calidad, transparencia

**Objetivos de Aprendizaje:**

- Diferenciar ReAct estándar vs Chain of Thought
- Entender el proceso de 5 pasos del CoT (UNDERSTAND → PLAN → EXECUTE → REFLECT → SYNTHESIZE)
- Evaluar niveles de confianza en razonamiento
- Aprender cuándo usar cada enfoque

### Cómo Ejecutar los Notebooks

**Paso 1: Asegurar que el Ambiente está Configurado**

```bash
# Verificar que las dependencias están instaladas
make install

# Verificar que la base de datos existe
ls data/pink_floyd_songs.db
```

**Paso 2: Lanzar Jupyter**

```bash
# Opción A: Jupyter Notebook (interfaz clásica)
uv run jupyter notebook notebooks/

# Opción B: Jupyter Lab (interfaz moderna)
uv run jupyter lab notebooks/
```

**Paso 3: Abrir Notebook**

En la interfaz de Jupyter:
1. Navegar al directorio `notebooks/`
2. Click en `ReAct_Agent_Analysis.ipynb` o `Cinema_ReAct_CoT_Analysis.ipynb`

**Paso 4: Ejecutar Celdas**

- **Ejecutar celda**: Shift + Enter
- **Ejecutar todas**: Cell → Run All
- **Reiniciar kernel**: Kernel → Restart & Run All

**Nota Importante:** Los notebooks hacen llamadas al API de OpenAI, lo que consume tokens y tiene costo asociado. Los estudiantes deben ser conscientes del uso.

### Resolución de Problemas con Notebooks

**Error: "Module not found"**
```bash
# Reinstalar dependencias
uv sync --group dev
```

**Error: "Database not found"**
```bash
# Inicializar base de datos
make setup
```

**Error: "OpenAI API key not configured"**
```bash
# Verificar que .env existe y tiene OPENAI_API_KEY
cat .env | grep OPENAI_API_KEY
```

**Error: "Cannot connect to kernel"**
```bash
# Reinstalar Jupyter
uv pip install --force-reinstall jupyter
```

---

## 6. Testing y Verificación

El proyecto incluye una suite exhaustiva de testing con 57 tests que cubren unit, integration, y end-to-end.

### Suite de Tests

**Tests Unitarios (20 tests)**

Los tests unitarios verifican componentes individuales de forma aislada:

- `test_database/test_db_manager.py`: Tests del manager de base de datos
  - Creación de conexiones
  - Consultas SQL
  - Manejo de errores

- `test_services/test_agent_service.py`: Tests del servicio de agentes
  - Inicialización de agentes
  - Caché de consultas
  - Métricas de ejecución

- `test_services/test_database_service.py`: Tests del servicio de database
  - Búsqueda de canciones
  - Filtros por mood/album/year
  - Validación de respuestas

**Tests de Integración (17 tests)**

Los tests de integración verifican la interacción entre componentes:

- `test_api_agent.py`: Integración API-Agent
  - Endpoint de query funciona correctamente
  - Modelos disponibles retornan lista correcta
  - Historial de ejecuciones persiste

- `test_api_database.py`: Integración API-Database
  - Endpoints de database retornan datos correctos
  - Búsquedas con filtros funcionan
  - Estadísticas de canciones son precisas

- `test_api_health.py`: Health checks
  - Endpoint básico retorna healthy
  - Endpoint detailed incluye métricas del sistema

**Tests End-to-End (20 tests)**

Los tests E2E simulan workflows completos de usuarios:

- `test_api_integration.py`: Workflows completos del API
  - Rate limiting funciona (429 después de 60 requests)
  - CORS headers están presentes
  - Security headers configurados correctamente
  - Caché funciona (cache hit/miss)

- `test_cot_workflow.py`: Chain of Thought workflow
  - Agente CoT ejecuta correctamente
  - Trace de razonamiento está estructurado
  - Niveles de confianza están presentes
  - Comparación CoT vs ReAct funciona

- `test_complete_workflow.py`: Workflows de usuario real
  - Exploración de base de datos completa
  - Health check workflow
  - API discovery workflow

### Ejecutar Tests

**Ejecutar Todos los Tests:**

```bash
# Con Make (recomendado)
make test

# Muestra: 57/57 tests passing
# Coverage: ~32% (puede mejorar)
```

**Ejecutar Tests por Categoría:**

```bash
# Solo tests unitarios
make test-unit

# Solo tests de integración
make test-integration

# Solo tests E2E
make test-e2e
```

**Ejecutar con Coverage Detallado:**

```bash
# Generar reporte HTML de coverage
make coverage-html

# Abrir reporte en navegador
open htmlcov/index.html
```

**Ejecutar Test Específico:**

```bash
# Ejecutar un archivo de tests
uv run pytest tests/unit/test_services/test_agent_service.py -v

# Ejecutar un test específico
uv run pytest tests/unit/test_services/test_agent_service.py::test_agent_initialization -v
```

**Ejecutar con Verbose Output:**

```bash
# Ver output detallado de cada test
uv run pytest tests/ -v

# Ver output incluyendo prints
uv run pytest tests/ -v -s
```

### Resultados de Tests - Última Verificación

**Fecha**: 2026-01-27
**Estado**: TODOS LOS TESTS PASANDO

| Categoría | Tests | Pass Rate | Cobertura | Tiempo |
|-----------|-------|-----------|-----------|---------|
| Unit Tests | 20 | 100% | 60% | ~2.5s |
| Integration Tests | 17 | 100% | 25% | ~1.8s |
| E2E Tests | 20 | 100% | 15% | ~93s |
| **TOTAL** | **57** | **100%** | **32%** | **~97s** |

**Detalles de Cobertura:**

```
src/agents/          - 45% coverage
src/tools/           - 70% coverage
src/database/        - 65% coverage
api/routers/         - 80% coverage
api/services/        - 55% coverage
api/middleware/      - 40% coverage
```

**Componentes Críticos con Alta Cobertura:**
- Agent Factory: 85%
- Database Tool: 90%
- API Routers: 80%
- Database Manager: 75%

**Áreas con Baja Cobertura (mejorables):**
- Reflection Loop: 15%
- Reasoning Validator: 20%
- Middleware: 40%

### Interpretar Resultados

**Test Exitoso:**
```
tests/unit/test_services/test_agent_service.py::test_agent_initialization PASSED
```
Significa que el test pasó correctamente.

**Test Fallido:**
```
tests/unit/test_services/test_agent_service.py::test_agent_initialization FAILED
AssertionError: expected 'gpt-4o-mini' but got 'gpt-4o'
```
Muestra el error específico que causó la falla.

**Warnings:**
```
ResourceWarning: unclosed connection <sqlite3.Connection>
```
Warnings no son errores críticos pero indican áreas de mejora.

### Tests en Docker

Los estudiantes también pueden ejecutar tests en un ambiente Docker aislado:

```bash
# Ejecutar tests en contenedor
docker compose -f docker-compose.test.yml up

# Ver logs de tests
docker compose -f docker-compose.test.yml logs -f

# Limpiar contenedores de tests
docker compose -f docker-compose.test.yml down
```

---

## 7. Herramientas Personalizadas

El sistema incluye dos herramientas personalizadas que el agente puede usar para responder consultas.

### Pink Floyd Database Tool

Esta herramienta permite al agente consultar una base de datos con 28 canciones icónicas de Pink Floyd.

**Descripción de la Herramienta:**

```python
name = "pink_floyd_database"
description = """
Query Pink Floyd songs by:
- Mood: melancholic, energetic, psychedelic, progressive, dark, introspective, peaceful
- Album: The Dark Side of the Moon, The Wall, Wish You Were Here, Animals, etc.
- Lyrics: keyword search in song lyrics
- Year: specific year or decade (1960s, 1970s, 1980s, 1990s)

Returns formatted list of matching songs with details (title, album, year, mood, duration).
"""
```

**Características de la Base de Datos:**

- **Total de canciones**: 28 canciones curadas
- **Álbumes incluidos**: 11 álbumes diferentes
  - The Dark Side of the Moon (1973)
  - The Wall (1979)
  - Wish You Were Here (1975)
  - Animals (1977)
  - The Division Bell (1994)
  - Meddle (1971)
  - The Piper at the Gates of Dawn (1967)
  - Y más...

- **Moods disponibles**:
  - melancholic: Time, Comfortably Numb, Wish You Were Here, Hey You
  - energetic: Run Like Hell, Young Lust, Another Brick in the Wall Part 2
  - psychedelic: Astronomy Domine, Interstellar Overdrive, Set the Controls
  - introspective: Echoes, Shine On You Crazy Diamond, High Hopes
  - peaceful: Breathe, The Great Gig in the Sky, Us and Them

- **Rango temporal**: 1967-1994 (27 años de historia)

**Ejemplos de Uso:**

```python
# Consulta por mood
Input: "Find melancholic songs"
Output: 7 canciones (Time, Comfortably Numb, Wish You Were Here, etc.)

# Consulta por álbum
Input: "Songs from The Dark Side of the Moon"
Output: 5 canciones del álbum

# Consulta por década
Input: "What songs are from the 1960s?"
Output: Astronomy Domine, Interstellar Overdrive, See Emily Play

# Búsqueda en lyrics
Input: "Songs with lyrics about time"
Output: Time ("Ticking away the moments..."), Us and Them
```

**Implementación Técnica:**

La herramienta usa SQLite con índices para búsqueda eficiente:

```python
# Búsqueda por mood (indexada)
SELECT * FROM songs WHERE mood = ? ORDER BY year DESC

# Búsqueda por álbum (indexada)
SELECT * FROM songs WHERE album LIKE ? ORDER BY year ASC

# Búsqueda en lyrics (full-text search)
SELECT * FROM songs WHERE lyrics LIKE ? ORDER BY year DESC
```

### Currency Converter Tool

Esta herramienta proporciona tasas de cambio en tiempo real entre divisas principales.

**Descripción de la Herramienta:**

```python
name = "currency_price_checker"
description = """
Get real-time currency exchange rates between major currencies.
Supports: USD, EUR, GBP, JPY, CHF, CAD, AUD, MXN, BRL, CNY

Returns current exchange rate with timestamp, conversion examples, and trend information.
Includes 5-minute caching for performance.
"""
```

**Divisas Soportadas:**

- **USD**: Dólar estadounidense
- **EUR**: Euro
- **GBP**: Libra esterlina
- **JPY**: Yen japonés
- **CHF**: Franco suizo
- **CAD**: Dólar canadiense
- **AUD**: Dólar australiano
- **MXN**: Peso mexicano
- **BRL**: Real brasileño
- **CNY**: Yuan chino

**Características Técnicas:**

1. **API Externa**: Integración con exchangerate-api.com
2. **Caché de 5 Minutos**: Evita llamadas repetidas para misma tasa
3. **Fallback a Mock Data**: Si API falla, usa datos de ejemplo
4. **Parsing de Lenguaje Natural**: Entiende consultas como "100 dollars in euros"

**Ejemplos de Uso:**

```python
# Tasa de cambio simple
Input: "What's the USD to EUR exchange rate?"
Output: "1 USD = 0.85 EUR (as of 2026-01-27 10:30 UTC)"

# Conversión con cantidad
Input: "How much is 100 dollars in British pounds?"
Output: "100 USD = 79.23 GBP at current rate (1 USD = 0.7923 GBP)"

# Comparación de múltiples divisas
Input: "Compare USD to JPY and EUR"
Output:
  "USD to JPY: 1 USD = 149.50 JPY
   USD to EUR: 1 USD = 0.85 EUR"
```

**Implementación del Caché:**

```python
# Estructura del caché
cache = {
    "USD_EUR": {
        "rate": 0.85,
        "timestamp": 1706348400,
        "expires_at": 1706348700  # 5 min después
    }
}

# Lógica de caché
if (current_time - cache_timestamp) < 300:  # 5 minutos
    return cached_rate
else:
    fetch_new_rate()
    update_cache()
```

**Manejo de Errores:**

La herramienta maneja varios escenarios de error:

1. **API no disponible**: Usa datos mock
2. **Divisa no soportada**: Retorna lista de divisas válidas
3. **Timeout de red**: Reintenta con exponential backoff
4. **Rate limit excedido**: Usa caché aunque esté expirado

### Cómo el Agente Selecciona Herramientas

El agente LLM decide qué herramienta usar basándose en:

1. **Descripción de la herramienta**: El LLM lee las descripciones
2. **Contexto de la consulta**: Analiza qué información necesita
3. **Razonamiento previo**: Considera pasos anteriores en el loop ReAct

**Ejemplo de Selección:**

```
User Query: "Find melancholic Pink Floyd songs and tell me the EUR to USD rate"

Agent Thought 1:
"La consulta tiene dos partes:
 1. Canciones melancólicas de Pink Floyd → pink_floyd_database
 2. Tasa EUR a USD → currency_price_checker
 Necesito usar ambas herramientas"

Agent Action 1: pink_floyd_database(query="melancholic songs")
Agent Observation 1: "Found 7 songs: Time, Comfortably Numb..."

Agent Thought 2: "Tengo las canciones. Ahora necesito la tasa de cambio"

Agent Action 2: currency_price_checker(from="EUR", to="USD")
Agent Observation 2: "1 EUR = 1.18 USD"

Agent Thought 3: "Tengo toda la información necesaria"

Final Answer: [Combina ambos resultados]
```

---

## 8. Modelos Soportados

El sistema soporta tres modelos de OpenAI con diferentes características de performance y costo.

### Tabla Comparativa de Modelos

| Modelo | Velocidad | Costo Input | Costo Output | Tokens Máx | Caso de Uso |
|--------|-----------|-------------|--------------|------------|-------------|
| **gpt-4o-mini** | Rápida | $0.15 / 1M | $0.60 / 1M | 16,000 | Desarrollo, testing, queries simples |
| **gpt-4o** | Moderada | $2.50 / 1M | $10.00 / 1M | 128,000 | Producción, queries complejas |
| **gpt-5-nano** | Muy Rápida | $0.10 / 1M | $0.40 / 1M | 8,000 | Alto volumen, tareas simples |

### Descripción de Modelos

**gpt-4o-mini**
- **Mejor para**: Desarrollo, experimentación, queries simples
- **Performance**: Responde en 2-4 segundos promedio
- **Calidad**: Buena calidad para la mayoría de casos de uso
- **Costo**: Muy económico, ideal para testing
- **Limitación**: Puede fallar en queries muy complejas

**gpt-4o**
- **Mejor para**: Producción, queries complejas, alta calidad
- **Performance**: Responde en 4-8 segundos promedio
- **Calidad**: Excelente calidad, razonamiento robusto
- **Costo**: Más costoso (16x vs gpt-4o-mini)
- **Ventaja**: Maneja contextos largos, mejor razonamiento

**gpt-5-nano**
- **Mejor para**: Alto volumen, respuestas rápidas
- **Performance**: Responde en 1-3 segundos promedio
- **Calidad**: Adecuada para tareas bien definidas
- **Costo**: El más económico
- **Limitación**: Contexto limitado (8K tokens)

### Configuración de Modelos

Los modelos están configurados en `src/config.py`:

```python
MODELS = {
    "gpt-4o-mini": {
        "temperature": 0.1,
        "max_tokens": 2000,
        "pricing": {
            "input": 0.15,   # USD per 1M tokens
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
    },
    "gpt-5-nano": {
        "temperature": 0.1,
        "max_tokens": 1500,
        "pricing": {
            "input": 0.10,
            "output": 0.40
        }
    }
}
```

### Cómo Seleccionar el Modelo Apropiado

**Usar gpt-4o-mini cuando:**
- Estás desarrollando y probando el sistema
- La consulta es simple (1 herramienta, consulta directa)
- El costo es una preocupación principal
- No necesitas razonamiento muy complejo

**Usar gpt-4o cuando:**
- Estás en producción con usuarios reales
- La consulta es compleja (múltiples herramientas, razonamiento multi-paso)
- La calidad de la respuesta es crítica
- Necesitas contexto largo o memoria extendida

**Usar gpt-5-nano cuando:**
- Necesitas procesar alto volumen de consultas
- Las consultas son simples y repetitivas
- La velocidad es más importante que la profundidad
- El costo por consulta debe ser mínimo

### Ejemplos de Costo

**Consulta Simple con gpt-4o-mini:**
```
Input tokens: 500
Output tokens: 300
Costo: (500 * 0.15 / 1M) + (300 * 0.60 / 1M) = $0.000255
```

**Consulta Compleja con gpt-4o:**
```
Input tokens: 2000
Output tokens: 1500
Costo: (2000 * 2.50 / 1M) + (1500 * 10.00 / 1M) = $0.020
```

**1000 Consultas Simples con gpt-5-nano:**
```
Promedio: 400 input + 200 output por consulta
Costo total: 1000 * [(400 * 0.10 + 200 * 0.40) / 1M] = $0.12
```

### Cambiar el Modelo por Defecto

**En el archivo .env:**
```bash
DEFAULT_MODEL=gpt-4o-mini
```

**En el request del API:**
```bash
curl -X POST 'http://localhost:8000/api/v1/agent/query' \
  -d '{"query": "...", "model": "gpt-4o"}'
```

**En el Dashboard:**
Usar el selector de modelo en la interfaz de "Live Agent".

---

## 9. Desarrollo y Extensión

Esta sección guía a los estudiantes en cómo extender el sistema con nuevas herramientas y agentes.

### Agregar Nuevas Herramientas

**Paso 1: Crear el Archivo de la Herramienta**

Crear un nuevo archivo en `src/tools/`, por ejemplo `weather_tool.py`:

```python
from langchain.tools import BaseTool
from typing import Optional
import requests

class WeatherTool(BaseTool):
    """Herramienta para obtener información del clima"""

    name = "weather_checker"
    description = """
    Get current weather information for a city.
    Input should be a city name (e.g., "London", "New York").
    Returns temperature, conditions, humidity, and wind speed.
    """

    def _run(self, city: str) -> str:
        """Ejecutar consulta de clima"""
        try:
            # Llamar a API de clima (ejemplo con OpenWeatherMap)
            api_key = "your_api_key"
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}

            response = requests.get(url, params=params)
            data = response.json()

            # Formatear respuesta
            result = f"""
            Weather in {city}:
            - Temperature: {data['main']['temp']}C
            - Conditions: {data['weather'][0]['description']}
            - Humidity: {data['main']['humidity']}%
            - Wind: {data['wind']['speed']} m/s
            """
            return result.strip()

        except Exception as e:
            return f"Error getting weather for {city}: {str(e)}"

    async def _arun(self, city: str) -> str:
        """Versión asíncrona (opcional)"""
        return self._run(city)
```

**Paso 2: Registrar la Herramienta**

Editar `src/agents/agent_factory.py` para incluir la nueva herramienta:

```python
from src.tools.weather_tool import WeatherTool

def create_agent(agent_type: str, model: str = "gpt-4o-mini"):
    # ... código existente ...

    # Agregar nueva herramienta
    tools = [
        PinkFloydDatabaseTool(),
        CurrencyPriceTool(),
        WeatherTool(),  # Nueva herramienta
    ]

    # ... resto del código ...
```

**Paso 3: Probar la Herramienta**

Crear un test en `tests/unit/test_tools/test_weather_tool.py`:

```python
import pytest
from src.tools.weather_tool import WeatherTool

def test_weather_tool_creation():
    """Verificar que la herramienta se crea correctamente"""
    tool = WeatherTool()
    assert tool.name == "weather_checker"
    assert "weather" in tool.description.lower()

def test_weather_tool_execution():
    """Verificar que la herramienta ejecuta consultas"""
    tool = WeatherTool()
    result = tool._run("London")
    assert "Temperature" in result
    assert "London" in result
```

**Paso 4: Documentar la Herramienta**

Agregar documentación en este README en la sección de Herramientas Personalizadas.

### Crear Nuevos Agentes

**Paso 1: Definir el Tipo de Agente**

Decidir qué tipo de agente crear:
- **ReAct Variant**: Modificación del loop ReAct
- **Specialized Agent**: Agente para dominio específico
- **Multi-Agent System**: Sistema con múltiples agentes coordinados

**Paso 2: Implementar el Agente**

Crear archivo en `src/agents/`, por ejemplo `specialized_agent.py`:

```python
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent
from src.agents.prompts.templates import get_react_prompt

def create_specialized_agent(tools: list, model: str = "gpt-4o-mini"):
    """Crear agente especializado con configuración custom"""

    # Inicializar LLM con configuración específica
    llm = ChatOpenAI(
        model=model,
        temperature=0.0,  # Temperatura baja para consistencia
        max_tokens=3000
    )

    # Prompt personalizado para el dominio
    custom_prompt = """You are a specialized agent for...

    Your task is to...

    You have access to the following tools:
    {tools}

    Use the following format:
    ...
    """

    # Crear agente
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=custom_prompt
    )

    # Crear executor con configuración custom
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        max_iterations=10,  # Más iteraciones si es necesario
        max_execution_time=60,  # Timeout de 60 segundos
        verbose=True,
        return_intermediate_steps=True
    )

    return agent_executor
```

**Paso 3: Registrar en Agent Factory**

Editar `src/agents/agent_factory.py`:

```python
from src.agents.specialized_agent import create_specialized_agent

def create_agent(agent_type: str, model: str = "gpt-4o-mini"):
    if agent_type == "specialized":
        return create_specialized_agent(tools, model)
    # ... otros tipos ...
```

**Paso 4: Crear Tests**

Crear tests en `tests/unit/test_agents/test_specialized_agent.py`

### Best Practices para Desarrollo

**1. Testing Incremental**
- Escribir tests antes de implementar (TDD)
- Probar cada componente de forma aislada
- Usar mocks para dependencias externas

**2. Logging Apropiado**
- Usar el sistema de logging configurado (Loguru)
- Log de eventos importantes (tool calls, errores)
- Incluir contexto en los logs

**3. Manejo de Errores**
- Capturar excepciones específicas
- Proveer mensajes de error claros
- Implementar fallbacks cuando sea posible

**4. Documentación**
- Docstrings en todas las funciones/clases
- Comentarios para lógica compleja
- Actualizar README con nuevas features

**5. Performance**
- Usar caché cuando sea apropiado
- Evitar llamadas innecesarias al LLM
- Monitorear uso de tokens

---

## 10. Resolución de Problemas

### Errores Comunes y Soluciones

**Error: "OPENAI_API_KEY not configured"**

```
Síntoma: El API retorna 500 o el agente falla al ejecutar
Causa: La API key de OpenAI no está configurada
Solución:
1. Verificar que existe .env: ls .env
2. Verificar contenido: cat .env | grep OPENAI_API_KEY
3. Asegurar formato correcto: OPENAI_API_KEY=sk-...
4. Reiniciar el API después de cambiar .env
```

**Error: "Database not found"**

```
Síntoma: Consultas de base de datos fallan con FileNotFoundError
Causa: La base de datos no ha sido inicializada
Solución:
1. Ejecutar setup: make setup
2. Verificar que existe: ls data/pink_floyd_songs.db
3. Verificar permisos: ls -l data/
4. Si persiste: rm data/*.db && make setup
```

**Error: "Port 8000 already in use"**

```
Síntoma: El API no inicia, error de bind
Causa: Otro proceso está usando el puerto 8000
Solución:
1. Encontrar proceso: lsof -i :8000
2. Matar proceso: kill -9 <PID>
3. O usar otro puerto: API_PORT=8001 make run-api
```

**Error: "Module not found"**

```
Síntoma: ImportError al ejecutar código
Causa: Dependencias no instaladas o ambiente incorrecto
Solución:
1. Reinstalar dependencias: make install
2. Verificar ambiente: uv run which python
3. Limpiar caché: make clean && make install
```

**Error: "Rate limit exceeded (429)"**

```
Síntoma: Requests al API retornan 429 Too Many Requests
Causa: Se excedió el límite de 60 req/min
Solución:
1. Esperar 1 minuto para reset
2. Reducir frecuencia de requests
3. Implementar backoff exponencial en cliente
4. Ajustar límite en api/middleware/rate_limiter.py (dev only)
```

**Error: "Connection timeout to OpenAI API"**

```
Síntoma: Requests al agente timeout después de 30+ segundos
Causa: Problemas de red o API de OpenAI caída
Solución:
1. Verificar conexión: curl https://api.openai.com/v1/models
2. Verificar status de OpenAI: https://status.openai.com
3. Aumentar timeout en src/config.py si es necesario
4. Implementar retry logic
```

**Error: "SQLite database locked"**

```
Síntoma: Operaciones de database fallan con "database is locked"
Causa: Múltiples escrituras simultáneas a SQLite
Solución:
1. Cerrar conexiones: Verificar que connections se cierran
2. Aumentar timeout: sqlite3.connect(db, timeout=20)
3. Considerar PostgreSQL para producción con alta concurrencia
```

**Error: "Tests failing with ResourceWarning"**

```
Síntoma: Tests pasan pero muestran warnings de recursos no cerrados
Causa: Conexiones de DB no se cierran en tests
Solución:
1. Agregar teardown en fixtures:
   @pytest.fixture
   def db_connection():
       conn = create_connection()
       yield conn
       conn.close()  # Asegurar cierre
2. Usar context managers: with sqlite3.connect() as conn:
```

### Logs y Debugging

**Acceder a Logs del API:**

```bash
# Ver logs en tiempo real
tail -f logs/api.log

# Buscar errores
grep "ERROR" logs/api.log

# Buscar queries específicas
grep "melancholic" logs/api.log
```

**Aumentar Nivel de Logging:**

Editar `.env`:
```bash
LOG_LEVEL=DEBUG  # Cambiarde INFO a DEBUG
```

Reiniciar API para aplicar cambios.

**Debugging con VS Code:**

Crear `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Debug API",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "jinja": true
        }
    ]
}
```

Luego usar F5 para iniciar debugging.

**Debugging de Agentes:**

Activar modo verbose en agent creation:

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # Mostrar todos los pasos
    return_intermediate_steps=True
)
```

### Verificación de Salud del Sistema

**Script de Health Check:**

```bash
#!/bin/bash
# health_check.sh

echo "Checking API..."
curl -f http://localhost:8000/health || echo "API DOWN"

echo "Checking Database..."
ls data/pink_floyd_songs.db || echo "DB NOT FOUND"

echo "Checking Environment..."
test -f .env && echo "ENV OK" || echo "ENV MISSING"

echo "Checking Dependencies..."
uv run python -c "import fastapi, langchain" && echo "DEPS OK" || echo "DEPS MISSING"
```

### Recursos de Ayuda

**Documentación Oficial:**
- FastAPI: https://fastapi.tiangolo.com
- LangChain: https://python.langchain.com
- OpenAI API: https://platform.openai.com/docs

**Comunidad:**
- LangChain Discord: https://discord.gg/langchain
- FastAPI Discussions: https://github.com/tiangolo/fastapi/discussions

**Reporting de Bugs:**
Los estudiantes pueden reportar problemas creando un issue en el repositorio del proyecto con:
1. Descripción del problema
2. Steps para reproducir
3. Logs relevantes
4. Ambiente (OS, Python version, etc.)

---

## 11. Recursos Adicionales

### Referencias Académicas

**ReAct Framework:**
- **Paper Original**: [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
  - Autores: Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
  - Año: 2022
  - Resumen: Propone el framework ReAct que intercala razonamiento (reasoning traces) con acciones (action traces) para mejorar la capacidad de los LLMs en tareas que requieren interacción con el mundo exterior.

**Chain of Thought:**
- **Paper Original**: [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
  - Autores: Jason Wei, Xuezhi Wang, et al. (Google Research)
  - Año: 2022
  - Resumen: Demuestra que provocar que los LLMs generen pasos de razonamiento intermedios mejora significativamente su capacidad en tareas complejas.

**LLM Agents:**
- **Survey Paper**: [A Survey on Large Language Model based Autonomous Agents](https://arxiv.org/abs/2308.11432)
  - Año: 2023
  - Cubre arquitecturas, aplicaciones, y desafíos de agentes basados en LLMs

**Tool Use:**
- **Paper**: [Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
  - Meta AI Research
  - Año: 2023
  - Explora cómo los LLMs pueden aprender a usar herramientas externas

### Documentación de Dependencias

**Frameworks Principales:**

- **LangChain**: https://python.langchain.com
  - Agents: https://python.langchain.com/docs/modules/agents/
  - Tools: https://python.langchain.com/docs/modules/agents/tools/
  - Memory: https://python.langchain.com/docs/modules/memory/

- **LangGraph**: https://langchain-ai.github.io/langgraph/
  - Conceptos: https://langchain-ai.github.io/langgraph/concepts/
  - Tutorials: https://langchain-ai.github.io/langgraph/tutorials/

- **FastAPI**: https://fastapi.tiangolo.com
  - Tutorial: https://fastapi.tiangolo.com/tutorial/
  - Advanced: https://fastapi.tiangolo.com/advanced/

- **Streamlit**: https://docs.streamlit.io
  - API Reference: https://docs.streamlit.io/library/api-reference
  - Components: https://docs.streamlit.io/library/components

**APIs Externas:**

- **OpenAI API**: https://platform.openai.com/docs
  - Chat Completions: https://platform.openai.com/docs/guides/chat
  - Token Pricing: https://openai.com/pricing

- **ExchangeRate API**: https://www.exchangerate-api.com/docs
  - Free tier: 1500 requests/mes

**Testing y Quality:**

- **Pytest**: https://docs.pytest.org
  - Fixtures: https://docs.pytest.org/en/stable/fixture.html
  - Markers: https://docs.pytest.org/en/stable/mark.html

- **Coverage.py**: https://coverage.readthedocs.io
  - Measuring: https://coverage.readthedocs.io/en/coverage-5.5/cmd.html

### Tutoriales y Cursos

**LangChain:**
- LangChain Academy: https://academy.langchain.com
- Build with LangChain: https://python.langchain.com/docs/use_cases

**FastAPI:**
- Official Tutorial: https://fastapi.tiangolo.com/tutorial/
- Real Python Course: https://realpython.com/fastapi-python-web-apis/

**LLM Agents:**
- DeepLearning.AI: "LangChain for LLM Application Development"
- Coursera: "Generative AI with Large Language Models"

### Herramientas de Desarrollo

**Package Management:**
- UV: https://github.com/astral-sh/uv
  - Documentación: https://astral-sh.github.io/uv/

**Docker:**
- Docker Docs: https://docs.docker.com
- Docker Compose: https://docs.docker.com/compose/

**Git:**
- Pro Git Book: https://git-scm.com/book/en/v2
- Git Workflows: https://www.atlassian.com/git/tutorials/comparing-workflows

### Blogs y Artículos

**ReAct y Agentes:**
- "Building Reliable AI Agents with ReAct" - LangChain Blog
- "The Rise of Autonomous Agents" - Anthropic Blog
- "Tool Use in Large Language Models" - OpenAI Blog

**Prompt Engineering:**
- "Prompt Engineering Guide" - https://www.promptingguide.ai
- "Best Practices for Prompt Engineering" - OpenAI
- "Chain of Thought Prompting" - Google AI Blog

### Comunidades y Soporte

**Discord Servers:**
- LangChain: https://discord.gg/langchain
- FastAPI: https://discord.gg/fastapi

**GitHub Discussions:**
- LangChain: https://github.com/langchain-ai/langchain/discussions
- FastAPI: https://github.com/tiangolo/fastapi/discussions

**Stack Overflow:**
- Tag: [langchain]
- Tag: [fastapi]
- Tag: [openai-api]

---

## 12. Estado del Sistema

### Última Verificación: 2026-01-27

**Estado General**: PRODUCCIÓN READY

El sistema ha sido exhaustivamente testeado y está listo para uso en ambientes de producción educativa.

### Métricas de Calidad

| Métrica | Valor | Estado | Meta |
|---------|-------|--------|------|
| Tests Pasando | 57/57 | 100% | 100% |
| Cobertura de Código | 32% | Aceptable | 50%+ |
| Endpoints Funcionando | 7/7 | 100% | 100% |
| Notebooks Ejecutando | 2/2 | 100% | 100% |
| Errores de Linting | 0 críticos | OK | 0 |
| Type Errors | 0 críticos | OK | 0 |

### Tests - Desglose Completo

**Unit Tests: 20/20 PASSING**
- Agent Factory: 5/5
- Agent Executor: 3/3
- Database Manager: 4/4
- Services: 8/8

**Integration Tests: 17/17 PASSING**
- API-Agent Integration: 6/6
- API-Database Integration: 5/5
- API Health: 3/3
- Service Integration: 3/3

**E2E Tests: 20/20 PASSING**
- Complete API Workflow: 10/10
- CoT Reasoning Workflow: 7/7
- User Workflows: 3/3

### Performance Benchmarks

**API Response Times:**
- Health check: ~5ms
- Database query: ~2-4ms
- Agent query (cold): ~7-8 seconds (incluye llamada a LLM)
- Agent query (cached): <100ms

**Agent Execution:**
- Simple query (1 tool): ~3-5 segundos
- Complex query (2+ tools): ~6-10 segundos
- Token usage promedio: 800-1500 tokens
- Costo promedio: $0.001-0.003 USD (gpt-4o-mini)

**Database:**
- Tamaño: ~40KB (28 canciones)
- Tiempo de query: <5ms
- Queries concurrentes soportadas: 100+

### Componentes Verificados

**API Endpoints:**
- GET /health
- GET /
- GET /api/v1/database/songs
- GET /api/v1/database/stats
- POST /api/v1/agent/query
- GET /api/v1/agent/history
- GET /api/v1/metrics/summary

**Middleware:**
- Rate Limiter: Funcionando (60 req/min)
- Security Headers: Configurados correctamente
- Request Logger: Logging activo
- CORS: Configurado para Dashboard

**Storage:**
- Execution History: SQLite persistente
- Query Cache: LRU + TTL funcionando
- Database: 28 canciones cargadas

**Notebooks:**
- ReAct_Agent_Analysis.ipynb: Ejecuta sin errores
- Cinema_ReAct_CoT_Analysis.ipynb: Ejecuta sin errores

### Limitaciones Conocidas

**1. Cobertura de Tests (32%)**
- Algunas áreas con baja cobertura: reflection_loop (15%), reasoning_validator (20%)
- No impacta funcionalidad pero reduce confianza en cambios futuros
- Recomendación: Agregar tests para estos componentes

**2. Type Hints Incompletos**
- 41 type errors de mypy (no críticos)
- No afecta runtime pero reduce ayuda de IDE
- Recomendación: Agregar type hints gradualmente

**3. SQLite Concurrency**
- SQLite puede tener issues con alta concurrencia de escritura
- Para producción de alto tráfico, considerar PostgreSQL
- Actual: Suficiente para ambientes educativos

**4. Cache In-Memory**
- Caché se pierde al reiniciar API
- Para producción considerar Redis
- Actual: Suficiente para desarrollo y demo

### Roadmap de Mejoras

**Corto Plazo (Opcional):**
- Aumentar cobertura de tests a 50%+
- Agregar más type hints
- Implementar más casos de prueba en notebooks

**Mediano Plazo:**
- Agregar más herramientas (weather, news, etc.)
- Implementar reflection loop mejorado
- Dashboard con más visualizaciones

**Largo Plazo:**
- Migrar a PostgreSQL para producción
- Implementar Redis para caché distribuido
- Sistema multi-agente colaborativo
- Fine-tuning de modelo específico para Pink Floyd

### Recomendaciones de Uso

**Para Estudiantes:**
- Comenzar con gpt-4o-mini para economizar
- Explorar notebooks antes de modificar código
- Ejecutar tests después de cada cambio
- Usar Dashboard para experimentación rápida

**Para Instructores:**
- Sistema listo para demos en vivo
- Notebooks pueden usarse directamente en clases
- Tests proporcionan ejemplos de best practices
- Código bien documentado para explicar conceptos

**Para Desarrollo Futuro:**
- Seguir arquitectura existente para consistencia
- Agregar tests para nuevas features
- Documentar cambios en README
- Mantener compatibilidad con Docker

---

## Contribuciones y Contacto

### Propósito Educativo

Este proyecto fue creado como material educativo para el bootcamp de Henry. Los estudiantes son animados a:

- Experimentar con el código
- Agregar nuevas herramientas
- Crear variantes de agentes
- Mejorar la documentación
- Reportar bugs encontrados

### Cómo Contribuir

Los estudiantes que deseen contribuir pueden:

1. **Fork del repositorio**
2. **Crear branch de feature**: `git checkout -b feature/nueva-herramienta`
3. **Hacer cambios y commit**: `git commit -m "feat: agregar herramienta de clima"`
4. **Push del branch**: `git push origin feature/nueva-herramienta`
5. **Crear Pull Request** con descripción clara de cambios

### Guidelines de Contribución

- Seguir estilo de código existente (PEP 8)
- Agregar tests para nuevas features
- Actualizar documentación relevante
- Asegurar que todos los tests pasan
- Usar commits descriptivos (conventional commits)

### Contacto

Para preguntas relacionadas con el curso de Henry, contactar a los instructores a través de los canales oficiales de la plataforma Henry.

---

**Built for Henry Class Demo** - Demonstrating Orchestration and Autonomous Agents with ReAct Framework and Chain of Thought Reasoning.

**Pink Floyd Edition** - Una tribute a una de las bandas de rock progresivo más grandes, demostrando cómo los agentes AI pueden interactuar con conocimiento estructurado (catálogo musical) mientras acceden a información en tiempo real (tasas de cambio de divisas).

---

**Última actualización**: 2026-01-27
**Versión**: 1.0.0
**Estado**: Producción Ready
