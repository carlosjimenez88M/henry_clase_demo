"""
LangGraph-based ReAct Agent Implementation.

This module provides a proper LangGraph StateGraph implementation of the ReAct pattern,
enabling visualization of agent architecture using LangGraph's built-in graph utilities.
"""

from collections.abc import Sequence
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from pydantic import SecretStr

from src.config import config


class AgentState(TypedDict):
    """State schema for the ReAct agent graph."""

    messages: Annotated[Sequence[BaseMessage], "The messages in the conversation"]


def create_langgraph_react_agent(
    model_name: str, tools: list[BaseTool], temperature: float = 0.1
):
    """
    Create a LangGraph-based ReAct agent with proper StateGraph architecture.

    This implementation uses LangGraph's StateGraph to create a proper graph-based agent
    that can be visualized using get_graph().draw_mermaid_png().

    Args:
        model_name: OpenAI model name (e.g., 'gpt-4o-mini')
        tools: List of LangChain tools
        temperature: Model temperature

    Returns:
        Compiled LangGraph StateGraph with agent workflow
    """
    # Initialize LLM with tools
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=SecretStr(config.openai_api_key),
    )
    llm_with_tools = llm.bind_tools(tools)

    # System prompt for ReAct
    system_prompt = """You are a helpful AI assistant with access to tools.
Follow the ReAct framework:

1. Think about what you need to do
2. Use tools if needed to gather information
3. Provide a clear, helpful answer

Available tools:
- pink_floyd_database: Query Pink Floyd songs by mood, album, lyrics, or year
- currency_price_checker: Get real-time currency exchange rates

Be concise and explain your reasoning."""

    # Define the agent node (reasoning)
    def agent_node(state: AgentState) -> dict:
        """Agent node that calls the LLM to decide next action."""
        messages = state["messages"]

        # Add system prompt if first message (use SystemMessage object, not dict)
        if len(messages) == 1 or not any(isinstance(m, AIMessage) for m in messages):
            messages = [SystemMessage(content=system_prompt)] + list(messages)

        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    # Define the routing function
    def should_continue(state: AgentState) -> Literal["tools", "end"]:
        """Determine whether to continue with tools or end."""
        messages = state["messages"]
        last_message = messages[-1]

        # If the LLM makes a tool call, route to tools
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return "tools"
        # Otherwise, end
        return "end"

    # Create the tool node
    tool_node = ToolNode(tools)

    # Build the StateGraph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)

    # Add edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent", should_continue, {"tools": "tools", "end": END}
    )
    workflow.add_edge("tools", "agent")

    # Compile the graph
    graph = workflow.compile()

    return graph


def run_langgraph_agent(graph, query: str) -> dict:
    """
    Execute the LangGraph ReAct agent with a query.

    Args:
        graph: Compiled LangGraph StateGraph
        query: User query string

    Returns:
        Dictionary with the final state including all messages
    """
    initial_state = {"messages": [HumanMessage(content=query)]}

    result = graph.invoke(initial_state)

    # Extract the final answer from the last AI message
    final_answer = None
    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and not message.tool_calls:
            final_answer = message.content
            break

    return {
        "answer": final_answer or "No response generated",
        "messages": result["messages"],
        "full_state": result,
    }
