"""
Main Streamlit Dashboard for Pink Floyd AI Agent Demo.

This is the home page and navigation for the demo dashboard.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Pink Floyd AI Agent Demo",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #FF1493;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #888;
        padding-bottom: 2rem;
    }
    .feature-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header"> Pink Floyd AI Agent Demo</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Orchestration and Autonomous Agents with ReAct Framework</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
## Welcome to the Demo!

This interactive dashboard demonstrates an AI agent built with the **ReAct (Reasoning + Acting)** framework.
The agent can autonomously use tools to answer complex queries.

###  Available Tools

The agent has access to two custom tools:

1. **Pink Floyd Database** 
   - Query 28 iconic Pink Floyd songs
   - Search by mood (melancholic, energetic, psychedelic, progressive, dark)
   - Search by album, lyrics, or year

2. **Currency Price Checker** 
   - Real-time exchange rates
   - Supports USD, EUR, GBP, JPY, CHF, CAD, AUD, and more
   - Live API integration with fallback data
""")

# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("###  Live Agent")
    st.markdown("""
    **Try the agent yourself!**
    - Interactive query interface
    - Real-time reasoning traces
    - Performance metrics

    **[Go to Live Agent →](pages/1_Live_Agent.py)**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("###  Model Comparison")
    st.markdown("""
    **Compare different models:**
    - gpt-4o-mini
    - gpt-4o
    - gpt-5-nano

    **[Go to Comparison →](pages/2_Model_Comparison.py)**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.markdown("###  Architecture")
    st.markdown("""
    **Learn how it works:**
    - ReAct framework explained
    - Tool design patterns
    - LangGraph integration

    **[Go to Architecture →](pages/3_Architecture.py)**
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ReAct Framework Overview
st.markdown("---")
st.markdown("##  ReAct Framework Overview")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
    The **ReAct** framework combines **Reasoning** and **Acting** to create autonomous agents:

    1. **Thought** : Agent reasons about what to do
    2. **Action** : Agent selects and uses a tool
    3. **Observation** : Agent receives tool output
    4. **Repeat or Answer** : Continue or provide final answer

    This creates a transparent, step-by-step reasoning process that's easy to understand and debug.
    """)

with col2:
    st.code("""
Example ReAct Trace:

Query: "Find melancholic Pink Floyd songs"

Thought: User wants melancholic songs,
         I should use the database tool

Action: pink_floyd_database
Input: "melancholic songs"

Observation: Found 7 songs:
            Time, Comfortably Numb...

Thought: I have the information

Final Answer: Here are melancholic
             Pink Floyd songs: [list]
    """, language="text")

# Technology Stack
st.markdown("---")
st.markdown("##  Technology Stack")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **AI/ML**
    - OpenAI API
    - LangChain
    - LangGraph
    """)

with col2:
    st.markdown("""
    **Backend**
    - Python 3.12
    - SQLAlchemy
    - Pydantic
    """)

with col3:
    st.markdown("""
    **Frontend**
    - Streamlit
    - Plotly
    - Pandas
    """)

with col4:
    st.markdown("""
    **Tools**
    - UV (package manager)
    - Pytest
    - Jupyter
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 2rem 0;">
    <p>Built for Henry Class Demo | 20-Minute Presentation on AI Agents</p>
    <p> Pink Floyd Edition | Powered by OpenAI</p>
</div>
""", unsafe_allow_html=True)
