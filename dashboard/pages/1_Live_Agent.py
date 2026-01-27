"""
Live Agent Page - Interactive Agent Demo with Persistent History.

This page allows users to interact with the AI agent in real-time via REST API.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import httpx
import streamlit as st
from dashboard.history_manager import HistoryManager

# Page config
st.set_page_config(page_title="Live Agent", page_icon="◆", layout="wide")

# Title
st.title("Live Agent Interaction")
st.markdown("Try the AI agent yourself! Ask questions about Pink Floyd songs or currency exchange rates.")

# API URL from environment or default
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Initialize history manager (persistent)
history_manager = HistoryManager(API_URL)

# Sidebar for configuration
with st.sidebar:
    st.markdown("## Configuration")

    # Model selection
    model_name = st.selectbox(
        "Select Model",
        options=["gpt-4o-mini", "gpt-4o", "gpt-5-nano"],
        index=0,
        help="Choose which OpenAI model to use"
    )

    st.markdown("---")

    # Example queries
    st.markdown("### Example Queries")
    st.markdown("""
    **Database Queries:**
    - Find melancholic Pink Floyd songs
    - Show songs from The Wall album
    - What psychedelic songs are from the 1960s?

    **Currency Queries:**
    - What's the USD to EUR exchange rate?
    - How much is 100 dollars in GBP?

    **Combined:**
    - I want energetic music and EUR price
    """)

# Initialize session state
if "current_model" not in st.session_state:
    st.session_state.current_model = None

# Update current model
if st.session_state.current_model != model_name:
    st.session_state.current_model = model_name
    st.success(f"{model_name} selected!")

# Query input
query = st.text_area(
    "Enter your query:",
    height=100,
    placeholder="Example: Find melancholic Pink Floyd songs",
    help="Ask anything about Pink Floyd songs or currency exchange rates"
)

# Buttons
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    run_button = st.button("Run Query", type="primary", use_container_width=True)

with col2:
    if st.button("Ver Historial", use_container_width=True):
        st.session_state.show_history = not st.session_state.get("show_history", False)

with col3:
    # Refresh history
    if st.button("Refrescar", use_container_width=True):
        st.rerun()

# Run query
if run_button and query.strip():
    with st.spinner("Agent is thinking..."):
        try:
            # Call API instead of direct execution
            response = httpx.post(
                f"{API_URL}/api/v1/agent/query",
                json={
                    "query": query.strip(),
                    "model": model_name,
                    "temperature": 0.1,
                    "max_iterations": 5
                },
                timeout=60.0
            )

            if response.status_code == 200:
                result = response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                st.json(response.json())
                st.stop()

            # Display result
            st.markdown("---")
            st.markdown("## Answer")
            st.markdown(result["answer"])

            # Show if from cache
            if result.get("from_cache"):
                st.info("Esta respuesta vino del cache (instantánea!)")

            # Metrics
            st.markdown("---")
            st.markdown("## Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Response Time",
                    f"{result['metrics']['execution_time_seconds']}s"
                )

            with col2:
                st.metric(
                    "Tokens Used",
                    f"{result['metrics']['estimated_tokens']['total']}"
                )

            with col3:
                st.metric(
                    "Est. Cost",
                    f"${result['metrics']['estimated_cost_usd']:.6f}"
                )

            with col4:
                st.metric(
                    "Reasoning Steps",
                    f"{result['metrics']['num_steps']}"
                )

            # Show agent type
            if "metadata" in result:
                st.info(f"Tipo de Agente: **{result['metadata'].get('agent_type', 'unknown')}** | "
                       f"Confianza: **{result['metadata'].get('confidence', 'N/A')}**")

            # Reasoning trace
            st.markdown("---")
            st.markdown("## Reasoning Trace")

            with st.expander("View detailed reasoning process", expanded=False):
                for step in result["reasoning_trace"]:
                    step_type = step.get("type", "unknown")

                    if step_type == "query":
                        st.markdown(f"**User Query:** {step.get('content', '')}")

                    elif step_type == "thinking":
                        st.markdown(f"**Thinking Step {step.get('step')}:**")
                        st.markdown(step.get('content', ''))
                        if "confidence" in step:
                            st.caption(f"Confidence: {step['confidence']}")

                    elif step_type == "action":
                        st.markdown(f"**Action {step.get('step')}:** Using tool `{step.get('tool', 'unknown')}`")
                        st.code(str(step.get('input', {})), language="json")

                    elif step_type == "observation":
                        st.markdown(f"**Observation {step.get('step')}:**")
                        # Truncate long observations
                        content = step.get('content', '')
                        if len(content) > 500:
                            content = content[:500] + "..."
                        st.info(content)

                    elif step_type == "thought":
                        st.markdown(f"**Final Thought {step.get('step')}:**")
                        st.success(step.get('content', ''))

                    elif step_type == "synthesis":
                        st.markdown(f"**Synthesis {step.get('step')}:**")
                        st.success(step.get('content', ''))
                        if "confidence" in step:
                            st.caption(f"Final Confidence: {step['confidence']}")

        except Exception as e:
            st.error(f"Error executing query: {e}")
            st.exception(e)

elif run_button:
    st.warning("Please enter a query first!")

# Show persistent history
if st.session_state.get("show_history", False):
    st.markdown("---")
    st.markdown("## Query History (Persistente)")

    # Fetch history from API
    history = history_manager.get_history(limit=20)

    if history:
        # Show statistics
        stats = history_manager.get_statistics(history)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Queries", stats["total_queries"])
        with col2:
            st.metric("Tiempo Promedio", f"{stats['avg_execution_time']:.2f}s")
        with col3:
            st.metric("Costo Total", f"${stats['total_cost']:.6f}")

        st.markdown("---")

        for i, hist in enumerate(history, 1):
            query_preview = hist.get('query', '')[:50]
            with st.expander(f"Query {i}: {query_preview}..."):
                st.markdown(f"**Query Completo:** {hist.get('query', '')}")
                st.markdown(f"**Modelo:** {hist.get('model', 'unknown')}")
                st.markdown(f"**Tipo Agente:** {hist.get('agent_type', 'unknown')}")
                st.markdown(f"**Time:** {hist.get('execution_time', 0):.2f}s")
                st.markdown(f"**Cost:** ${hist.get('estimated_cost', 0):.6f}")
                st.markdown(f"**Timestamp:** {hist.get('timestamp', '')}")

        # Export button
        if st.button("Exportar a CSV"):
            history_manager.export_to_csv(history, "history_export.csv")
            st.success("Historial exportado a history_export.csv")
    else:
        st.info("No hay historial disponible.")

# Tips
st.markdown("---")
st.markdown("### Tips")
st.info("""
- **Be specific**: Instead of "Pink Floyd", try "melancholic Pink Floyd songs"
- **Combine tools**: Try asking for both music recommendations and currency info
- **Watch the reasoning**: Expand the reasoning trace to see how the agent thinks
- **Try different models**: Compare how gpt-4o-mini vs gpt-4o performs
- **History is persistent**: Your queries are saved and can be viewed anytime
""")
