#  Demo Guide - 20 Minutes

## Preparación Pre-Demo (5 minutos antes)

### 1. Verificar que todo funciona
```bash
# Asegurar que la base de datos está inicializada
uv run python scripts/setup_database.py

# Ejecutar test rápido del sistema
uv run python test_complete_system.py

# Iniciar Streamlit dashboard
uv run streamlit run dashboard/app.py
```

### 2. Tener Abierto
-  **Terminal 1**: Dashboard de Streamlit corriendo
-  **Terminal 2**: Disponible para ejecutar comandos
-  **Browser**: Dashboard en http://localhost:8501
-  **Editor**: Código fuente abierto (VS Code/Cursor)

---

## Script del Demo (20 minutos)

###  Minutos 0-2: Introducción

**Qué Hacer:**
1. Abrir el dashboard de Streamlit (página principal)
2. Mostrar la introducción

**Qué Decir:**
> "Hoy vamos a ver cómo construir agentes de IA autónomos usando el framework ReAct.
>
> Este demo usa Pink Floyd como caso de uso - tenemos un agente que puede consultar
> una base de datos de 28 canciones icónicas Y obtener precios de divisas en tiempo real.
>
> El agente puede razonar sobre qué herramienta usar y cuándo usarla."

**Puntos Clave:**
-  **ReAct** = Reasoning + Acting
-  Dos herramientas custom: Database + Currency
-  Agente autónomo que decide qué hacer

---

###  Minutos 2-5: Arquitectura

**Qué Hacer:**
1. Ir a la página "Architecture" (tab 3)
2. Mostrar el diagrama Mermaid del README en el editor

**Qué Decir:**
> "El sistema tiene tres capas principales:
>
> 1. **User Interface**: Streamlit dashboard y notebooks
> 2. **Agent Core**: Aquí está la magia - el loop ReAct que razona y actúa
> 3. **Tools**: Database de Pink Floyd y API de divisas
>
> El agente recibe una query, piensa qué hacer (Thought), ejecuta una acción (Action),
> observa el resultado (Observation), y repite hasta tener la respuesta final."

**Puntos Clave:**
-  Loop iterativo: Thought → Action → Observation
-  LLM toma decisiones sobre qué tool usar
-  Tracking de métricas: tiempo, tokens, costo

---

###  Minutos 5-9: Live Agent Demo

**Qué Hacer:**
1. Ir a la página "Live Agent" (tab 1)
2. Seleccionar modelo: `gpt-4o-mini`
3. Ejecutar 3 queries en vivo

**Query 1: Database Simple**
```
Find melancholic Pink Floyd songs
```

**Qué Mostrar:**
- ⏱ Reasoning trace (expandir)
-  Cómo el agente decide usar `pink_floyd_database`
-  Métricas: tiempo, tokens, costo

**Qué Decir:**
> "Observen cómo el agente:
> 1. Entiende que necesita consultar la base de datos
> 2. Selecciona la herramienta correcta
> 3. Ejecuta la query
> 4. Formatea la respuesta para el usuario
>
> Todo esto de forma autónoma, sin programación específica para esta query."

**Query 2: Currency Simple**
```
What's the current USD to EUR exchange rate?
```

**Qué Mostrar:**
-  Uso de API externa en tiempo real
-  Respuesta con tasa de cambio actual

**Qué Decir:**
> "Ahora usa una herramienta completamente diferente - consulta una API externa
> para obtener precios en tiempo real. El agente eligió la herramienta correcta
> basándose en la query del usuario."

**Query 3: Multi-Tool**
```
I want energetic Pink Floyd music and the current EUR price
```

**Qué Mostrar:**
-  Uso de AMBAS herramientas en una sola query
-  Cómo el agente coordina múltiples acciones

**Qué Decir:**
> "Y aquí está lo poderoso: una query que requiere AMBAS herramientas.
> El agente razona que necesita:
> 1. Buscar canciones energéticas en la base de datos
> 2. Obtener el precio del EUR
>
> Y ejecuta ambas acciones automáticamente."

---

###  Minutos 9-13: Comparación de Modelos

**Qué Hacer:**
1. Ir a la página "Model Comparison" (tab 2)
2. Si no hay resultados, ejecutar: `uv run python scripts/run_comparison.py` (en terminal 2)
3. Mostrar la comparación

**Qué Mostrar:**
-  Tabla de comparación (gpt-4o-mini vs gpt-4o vs gpt-5-nano)
-  Gráficas de tiempo de respuesta
-  Análisis de costos
-  Tasas de éxito

**Qué Decir:**
> "Comparamos tres modelos diferentes ejecutando las mismas queries:
>
> - **gpt-4o-mini**: Más rápido y barato, excelente para producción
> - **gpt-4o**: Mejor calidad, pero 15x más caro
> - **gpt-5-nano**: El más nuevo, balance entre velocidad y costo
>
> En la práctica, gpt-4o-mini es suficiente para la mayoría de casos de uso.
> Solo usas gpt-4o cuando necesitas razonamiento muy complejo."

**Puntos Clave:**
-  Velocidad vs  Costo vs  Calidad
-  Trade-offs en la vida real
-  Elegir el modelo correcto para tu caso de uso

---

###  Minutos 13-17: Code Walkthrough

**Qué Hacer:**
1. Abrir VS Code/Cursor
2. Mostrar 3 archivos clave:

**Archivo 1: `src/tools/database_tool.py`** (2 min)

**Qué Mostrar:**
```python
class PinkFloydDatabaseTool(BaseTool):
    name = "pink_floyd_database"
    description = """
    A database of Pink Floyd songs. Use this tool to search...
    """

    def _run(self, query: str) -> str:
        # Parse query and execute
```

**Qué Decir:**
> "Crear una herramienta es súper simple:
> 1. Hereda de `BaseTool`
> 2. Define un `name` y `description` clara
> 3. Implementa `_run()` con tu lógica
>
> El LLM lee la descripción y decide cuándo usar esta herramienta."

**Archivo 2: `src/agents/react_agent.py`** (2 min)

**Qué Mostrar:**
```python
def create_react_agent(model_name, tools, temperature):
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    llm_with_tools = llm.bind_tools(tools)
    return llm_with_tools
```

**Qué Decir:**
> "El agente es simplemente un LLM con herramientas 'bindeadas'.
> LangChain maneja toda la complejidad del loop ReAct por nosotros."

**Archivo 3: README.md - Diagrama Mermaid** (1 min)

**Qué Mostrar:**
- Diagrama de arquitectura
- Diagrama de secuencia ReAct

**Qué Decir:**
> "La documentación incluye diagramas Mermaid que explican el flujo completo.
> Esto es crucial para que otros desarrolladores entiendan el sistema."

---

###  Minutos 17-19: Chat Completions vs Assistant API

**Qué Hacer:**
1. Volver al dashboard, página "Architecture"
2. Mostrar la sección sobre APIs

**Qué Decir:**
> "OpenAI ofrece dos formas de trabajar con agentes:
>
> **Chat Completions API (lo que usamos):**
> -  Más control sobre el flujo
> -  Más flexible
> -  Funciona con cualquier modelo
> -  Más código manual
>
> **Assistant API:**
> -  Más simple de usar
> -  OpenAI maneja el estado
> -  Menos control
> -  Vendor lock-in
>
> Para este tipo de demos educativas, preferimos Chat Completions porque
> podemos ver exactamente qué está pasando."

---

###  Minutos 19-20: Q&A y Conclusión

**Preguntas Frecuentes a Preparar:**

**Q: ¿Cuándo uso un agente vs un simple prompt?**
> A: Usa agentes cuando necesitas:
> - Acceder a datos externos (APIs, databases)
> - Múltiples pasos de razonamiento
> - Decisiones dinámicas sobre qué hacer
>
> Usa prompts simples cuando:
> - Tarea única y directa
> - No necesitas herramientas externas
> - Latencia es crítica

**Q: ¿Cómo aseguro que el agente use las herramientas correctas?**
> A: La clave está en la descripción de las herramientas. Debe ser:
> - Clara y específica
> - Incluir ejemplos
> - Explicar cuándo usar vs no usar

**Q: ¿Qué pasa si el agente falla?**
> A: Implementamos error handling en múltiples niveles:
> - Fallback a datos mock (currency tool)
> - Try-catch en ejecución de tools
> - Max iterations para evitar loops infinitos

**Conclusión Final:**
> "Puntos clave de hoy:
>
> 1. **ReAct** combina razonamiento y acción para agentes autónomos
> 2. **Tools** son fáciles de crear - solo necesitas una descripción clara
> 3. **LangChain** simplifica mucho la implementación
> 4. **Comparación de modelos** es crucial - diferentes casos de uso necesitan diferentes modelos
>
> El código completo está en GitHub con documentación exhaustiva.
> ¡Gracias! "

---

##  Troubleshooting Durante el Demo

### Si el agente falla:
```bash
# Reiniciar el dashboard
Ctrl+C en terminal
uv run streamlit run dashboard/app.py
```

### Si la API de currency falla:
> "Esto demuestra por qué implementamos fallback a datos mock -
> en producción, siempre ten un plan B."

### Si las queries son muy lentas:
> "Esto es normal con gpt-4o - tarda más pero da mejores resultados.
> Por eso gpt-4o-mini es mejor para demos en vivo."

### Si alguien pregunta sobre gpt-5-nano:
> "Es el modelo más nuevo de OpenAI, optimizado para latencia y costo.
> Perfecto para casos de uso donde velocidad > calidad absoluta."

---

##  Checklist Pre-Demo

- [ ] Base de datos inicializada (28 canciones)
- [ ] .env con OPENAI_API_KEY válida
- [ ] Streamlit dashboard corriendo en http://localhost:8501
- [ ] Test completo ejecutado sin errores
- [ ] Código fuente abierto en editor
- [ ] README abierto para mostrar diagramas Mermaid
- [ ] Terminal disponible para comandos
- [ ] Conexión a internet estable (para currency API)

---

##  Objetivos del Demo

Al final del demo, la audiencia debe entender:

1.  Qué es el framework ReAct y por qué es útil
2.  Cómo crear herramientas custom para agentes
3.  Cómo integrar LangChain con OpenAI
4.  Trade-offs entre diferentes modelos
5.  Cuándo usar agentes vs prompts simples
6.  Cómo estructurar un proyecto de agentes en producción

---

**¡Buena suerte con tu demo! **
