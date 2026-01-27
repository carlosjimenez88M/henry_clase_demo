"""
ReAct Agent implementation using OpenAI function calling.

This module implements a simple ReAct agent using OpenAI's function calling API.
"""


from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.config import config


def create_react_agent(
    model_name: str, tools: list[BaseTool], temperature: float = 0.1
):
    """
    Create a ReAct agent with the specified model and tools.

    Args:
        model_name: OpenAI model name (e.g., 'gpt-4o-mini')
        tools: List of LangChain tools
        temperature: Model temperature

    Returns:
        Tuple of (configured LLM with tools, tools list)
    """
    # Initialize LLM
    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        api_key=SecretStr(config.openai_api_key),
    )

    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(tools)

    return llm_with_tools, tools


def run_agent(agent_tuple, query: str, max_iterations: int = 5) -> dict:
    """
    Run the agent with a query using the ReAct pattern.

    Args:
        agent_tuple: Tuple of (LLM with tools bound, tools list)
        query: User query string
        max_iterations: Maximum number of tool calling iterations

    Returns:
        Dictionary with answer and reasoning trace
    """
    llm_with_tools, tools = agent_tuple
    reasoning_steps = []
    step_num = 1

    # Initial query
    reasoning_steps.append({"step": step_num, "type": "query", "content": query})
    step_num += 1

    # System message for ReAct
    system_prompt = """You are a helpful AI assistant with access to tools.
Follow the ReAct framework:

1. Think about what you need to do
2. Use tools if needed to gather information
3. Provide a clear, helpful answer

Available tools:
- pink_floyd_database: Query Pink Floyd songs by mood, album, lyrics, or year
- currency_price_checker: Get real-time currency exchange rates

Be concise and explain your reasoning."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    for iteration in range(max_iterations):
        # Call LLM
        response = llm_with_tools.invoke(messages)

        # Check if tool calls are present
        if hasattr(response, "tool_calls") and response.tool_calls:
            # Add assistant message with tool calls
            messages.append(response)

            # Process each tool call
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_input = tool_call["args"]

                # Record action
                reasoning_steps.append(
                    {
                        "step": step_num,
                        "type": "action",
                        "tool": tool_name,
                        "input": tool_input,
                    }
                )
                step_num += 1

                # Execute tool
                # Find the tool by name
                tool_to_call = next((t for t in tools if t.name == tool_name), None)

                if tool_to_call:
                    try:
                        tool_result = tool_to_call.invoke(tool_input)
                    except Exception as e:
                        tool_result = f"Error executing tool: {e}"
                else:
                    tool_result = f"Tool {tool_name} not found"

                # Record observation
                reasoning_steps.append(
                    {
                        "step": step_num,
                        "type": "observation",
                        "content": str(tool_result),
                    }
                )
                step_num += 1

                # Add tool result to messages
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "name": tool_name,
                        "content": str(tool_result),
                    }
                )

            # Continue to next iteration to get final answer
            continue

        else:
            # No tool calls, agent has final answer
            final_answer = response.content
            reasoning_steps.append(
                {"step": step_num, "type": "thought", "content": final_answer}
            )

            return {
                "answer": final_answer,
                "reasoning_trace": reasoning_steps,
                "raw_response": response,
            }

    # Max iterations reached
    return {
        "answer": "Max iterations reached without final answer",
        "reasoning_trace": reasoning_steps,
        "raw_response": None,
    }
