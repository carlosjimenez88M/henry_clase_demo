"""
Live Agent Page - Interactive Agent Demo.

This page allows users to interact with the AI agent in real-time via REST API.
"""

import os
import httpx
import streamlit as st

# Page config
st.set_page_config(page_title="Live Agent", page_icon="", layout="wide")

# Title
st.title(" Live Agent Interaction")
st.markdown("Try the AI agent yourself! Ask questions about Pink Floyd songs or currency exchange rates.")

# Sidebar for configuration
with st.sidebar:
    st.markdown("##  Configuration")

    # Model selection
    model_name = st.selectbox(
        "Select Model",
        options=["gpt-4o-mini", "gpt-4o", "gpt-5-nano"],
        index=0,
        help="Choose which OpenAI model to use"
    )

    st.markdown("---")

    # Example queries
    st.markdown("###  Example Queries")
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
    st.session_state.history = []

# API URL from environment or default
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Update current model
if st.session_state.current_model != model_name:
    st.session_state.current_model = model_name
    st.success(f" {model_name} selected!")

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
    run_button = st.button(" Run Query", type="primary", use_container_width=True)

with col2:
    clear_button = st.button(" Clear History", use_container_width=True)

with col3:
    if st.session_state.history:
        if st.button(f" History ({len(st.session_state.history)})", use_container_width=True):
            st.session_state.show_history = not st.session_state.get("show_history", False)

# Clear history
if clear_button:
    st.session_state.history = []
    st.rerun()

# Run query
if run_button and query.strip():
    with st.spinner(" Agent is thinking..."):
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
                st.session_state.history.append(result)
            else:
                st.error(f" API Error: {response.status_code}")
                st.json(response.json())
                st.stop()

            # Display result
            st.markdown("---")
            st.markdown("##  Answer")
            st.markdown(result["answer"])

            # Metrics
            st.markdown("---")
            st.markdown("##  Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "⏱ Response Time",
                    f"{result['metrics']['execution_time_seconds']}s"
                )

            with col2:
                st.metric(
                    " Tokens Used",
                    f"{result['metrics']['estimated_tokens']['total']}"
                )

            with col3:
                st.metric(
                    " Est. Cost",
                    f"${result['metrics']['estimated_cost_usd']:.6f}"
                )

            with col4:
                st.metric(
                    " Reasoning Steps",
                    f"{result['metrics']['num_steps']}"
                )

            # Reasoning trace
            st.markdown("---")
            st.markdown("##  Reasoning Trace")

            with st.expander("View detailed reasoning process", expanded=False):
                for step in result["reasoning_trace"]:
                    if step["type"] == "query":
                        st.markdown(f"** User Query:** {step['content']}")

                    elif step["type"] == "action":
                        st.markdown(f"** Action {step['step']}:** Using tool `{step['tool']}`")
                        st.code(str(step['input']), language="json")

                    elif step["type"] == "observation":
                        st.markdown(f"** Observation {step['step']}:**")
                        # Truncate long observations
                        content = step['content']
                        if len(content) > 500:
                            content = content[:500] + "..."
                        st.info(content)

                    elif step["type"] == "thought":
                        st.markdown(f"** Final Thought {step['step']}:**")
                        st.success(step['content'])

        except Exception as e:
            st.error(f" Error executing query: {e}")
            st.exception(e)

elif run_button:
    st.warning(" Please enter a query first!")

# Show history
if st.session_state.get("show_history", False) and st.session_state.history:
    st.markdown("---")
    st.markdown("##  Query History")

    for i, hist in enumerate(reversed(st.session_state.history), 1):
        with st.expander(f"Query {len(st.session_state.history) - i + 1}: {hist['query'][:50]}..."):
            st.markdown(f"**Answer:** {hist['answer'][:200]}...")
            st.markdown(f"**Time:** {hist['metrics']['execution_time_seconds']}s | "
                       f"**Tokens:** {hist['metrics']['estimated_tokens']['total']} | "
                       f"**Cost:** ${hist['metrics']['estimated_cost_usd']:.6f}")

# Tips
st.markdown("---")
st.markdown("###  Tips")
st.info("""
- **Be specific**: Instead of "Pink Floyd", try "melancholic Pink Floyd songs"
- **Combine tools**: Try asking for both music recommendations and currency info
- **Watch the reasoning**: Expand the reasoning trace to see how the agent thinks
- **Try different models**: Compare how gpt-4o-mini vs gpt-4o performs
""")
