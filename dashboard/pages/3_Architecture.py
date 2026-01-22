"""
Architecture Page - System Overview.

This page explains how the AI agent system works.
"""

import streamlit as st

st.set_page_config(page_title="Architecture", page_icon="", layout="wide")

st.title(" System Architecture")
st.markdown("Learn how the AI agent system is built and how it works")

# Tabs for different sections
tab1, tab2, tab3 = st.tabs([" ReAct Framework", " Tools", " LangChain Integration"])

with tab1:
    st.markdown("##  ReAct Framework")

    st.markdown("""
    The **ReAct** (Reasoning + Acting) framework is a paradigm for building AI agents that can:
    - **Reason** about complex tasks
    - **Act** by using tools
    - **Learn** from observations

    ### How it Works

    The agent follows a cyclical process:
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        #### 1.  Thought
        The agent analyzes the user's query and decides what to do.

        **Example:**
        > "The user wants melancholic Pink Floyd songs. I need to query the database."

        #### 2.  Action
        The agent selects and invokes the appropriate tool.

        **Example:**
        > Action: `pink_floyd_database`
        > Input: `{"query": "melancholic songs"}`

        #### 3.  Observation
        The agent receives the tool's output.

        **Example:**
        > "Found 7 songs: Time, Comfortably Numb, Wish You Were Here..."

        #### 4.  Repeat or Finish
        The agent either:
        - Continues with more actions, or
        - Provides the final answer
        """)

    with col2:
        st.code("""
Example ReAct Trace:

User: "Find melancholic Pink Floyd songs"

→ Thought 1:
  "I need to search the database
   for melancholic mood songs"

→ Action 1:
  Tool: pink_floyd_database
  Input: "melancholic songs"

→ Observation 1:
  "Found 7 songs:
   1. Time
   2. Comfortably Numb
   3. Wish You Were Here..."

→ Thought 2:
  "I have all the information
   needed to answer"

→ Final Answer:
  "Here are melancholic Pink
   Floyd songs: [detailed list]"
        """, language="text")

    st.markdown("---")
    st.markdown("###  Benefits of ReAct")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ** Transparency**
        - See exactly how the agent thinks
        - Debug reasoning process
        - Understand decision-making
        """)

    with col2:
        st.markdown("""
        ** Accuracy**
        - Tools provide factual information
        - Reduces hallucinations
        - Grounded in real data
        """)

    with col3:
        st.markdown("""
        ** Flexibility**
        - Easy to add new tools
        - Adapt to different tasks
        - Extensible architecture
        """)

with tab2:
    st.markdown("##  Custom Tools")

    st.markdown("""
    Our agent has access to two custom tools that extend its capabilities:
    """)

    # Tool 1: Database
    st.markdown("###  Pink Floyd Database Tool")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        **Purpose:** Query a curated database of 28 Pink Floyd songs

        **Capabilities:**
        - Search by mood (melancholic, energetic, psychedelic, progressive, dark)
        - Search by album name
        - Search by lyrics keywords
        - Filter by year or decade

        **Data Schema:**
        - Title, Album, Year
        - Mood classification
        - Lyrics snippets
        - Duration, Track number
        """)

    with col2:
        st.code("""
class PinkFloydDatabaseTool(BaseTool):
    name = "pink_floyd_database"

    description = '''
    Query Pink Floyd songs by:
    - Mood (melancholic, energetic...)
    - Album name
    - Lyrics keywords
    - Year or decade
    '''

    def _run(self, query: str) -> str:
        # Parse query intent
        # Execute database query
        # Format results
        return formatted_results
        """, language="python")

    st.markdown("---")

    # Tool 2: Currency
    st.markdown("###  Currency Price Checker Tool")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        **Purpose:** Fetch real-time currency exchange rates

        **Capabilities:**
        - Support for 10+ major currencies
        - Real-time API integration
        - 5-minute caching for performance
        - Fallback to mock data for reliability

        **API:** exchangerate-api.io (free tier)

        **Currencies:** USD, EUR, GBP, JPY, CHF, CAD, AUD, MXN, BRL, CNY
        """)

    with col2:
        st.code("""
class CurrencyPriceTool(BaseTool):
    name = "currency_price_checker"

    description = '''
    Get real-time exchange rates.
    Supports: USD, EUR, GBP, JPY...
    '''

    def _run(self, query: str) -> str:
        # Parse currency pair
        # Check cache
        # Fetch from API
        # Format result
        return exchange_rate_info
        """, language="python")

    st.markdown("---")
    st.markdown("###  Tool Design Principles")

    st.info("""
    **1. Clear Descriptions:** The agent needs to understand what each tool does

    **2. Structured Inputs/Outputs:** Consistent format for easy parsing

    **3. Error Handling:** Graceful fallbacks when things go wrong

    **4. Performance:** Caching and optimization for speed
    """)

with tab3:
    st.markdown("##  LangChain & OpenAI Integration")

    st.markdown("""
    ### Technology Stack

    Our agent is built on top of modern AI/ML libraries:
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### LangChain
        - Framework for building LLM applications
        - Provides tool calling interface
        - Handles message formatting
        - Manages agent state

        #### OpenAI API
        - Access to GPT models
        - Function calling capability
        - High-quality language understanding
        """)

    with col2:
        st.code("""
# Agent Creation
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1
)

# Bind tools to LLM
llm_with_tools = llm.bind_tools([
    database_tool,
    currency_tool
])

# Execute query
response = llm_with_tools.invoke(
    messages
)
        """, language="python")

    st.markdown("---")
    st.markdown("###  Execution Flow")

    st.markdown("""
    1. **User Query** → Enters system
    2. **LLM Processing** → Model decides on action
    3. **Tool Execution** → If tool needed, execute it
    4. **Result Processing** → LLM receives tool output
    5. **Final Answer** → LLM generates response
    6. **Metrics Tracking** → Time, tokens, cost recorded
    """)

    st.markdown("---")
    st.markdown("###  Project Structure")

    st.code("""
henry_clase_demo/
 src/
    config.py              # Configuration
    database/              # SQLite database
    tools/                 # Custom tools
    agents/                # ReAct agent
    comparison/            # Model comparison
 dashboard/                 # Streamlit app
 notebooks/                 # Jupyter notebooks
 scripts/                   # Utility scripts
 tests/                     # Unit tests
    """, language="text")

# Footer
st.markdown("---")
st.markdown("""
###  References

- **ReAct Paper:** [Yao et al., 2022](https://arxiv.org/abs/2210.03629)
- **LangChain Docs:** [python.langchain.com](https://python.langchain.com)
- **OpenAI API:** [platform.openai.com](https://platform.openai.com)
""")
