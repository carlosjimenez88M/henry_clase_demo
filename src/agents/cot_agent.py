"""
Chain of Thought (CoT) ReAct Agent Implementation.

This module implements an enhanced ReAct agent with explicit Chain of Thought
reasoning, confidence assessment, and self-reflection capabilities.
"""

from typing import Any

from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from src.agents.prompts import get_adaptive_cot_prompt, get_cot_prompt
from src.agents.prompts.templates import ReasoningStructure
from src.config import config


class CoTReActAgent:
    """
    ReAct agent with explicit Chain of Thought reasoning.

    This agent enhances the standard ReAct pattern with:
    - Explicit reasoning steps (UNDERSTAND, PLAN, EXECUTE, REFLECT, SYNTHESIZE)
    - Confidence assessment (HIGH/MEDIUM/LOW)
    - Alternative consideration
    - Self-reflection and validation
    - Structured reasoning traces
    """

    def __init__(
        self,
        model_name: str,
        tools: list[BaseTool],
        temperature: float = 0.1,
        use_adaptive_prompt: bool = True,
    ):
        """
        Initialize CoT ReAct agent.

        Args:
            model_name: OpenAI model name
            tools: List of available tools
            temperature: Model temperature
            use_adaptive_prompt: Whether to use adaptive prompts based on query complexity
        """
        self.model_name = model_name
        self.tools = tools
        self.temperature = temperature
        self.use_adaptive_prompt = use_adaptive_prompt

        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=SecretStr(config.openai_api_key),
        )

        # Bind tools
        self.llm_with_tools = self.llm.bind_tools(tools)

        # Tool map for quick lookup
        self.tool_map = {tool.name: tool for tool in tools}

        # Prepare tool descriptions for prompt
        self.tool_descriptions = self._prepare_tool_descriptions()

    def _prepare_tool_descriptions(self) -> list[dict]:
        """Prepare tool descriptions for the CoT prompt."""
        descriptions = []
        for tool in self.tools:
            # Get schema safely
            schema_str = "No schema"
            if hasattr(tool, "args_schema") and tool.args_schema is not None:
                try:
                    schema_str = str(tool.args_schema.model_json_schema())
                except:
                    schema_str = "Schema unavailable"

            descriptions.append(
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": schema_str,
                }
            )
        return descriptions

    def _get_system_prompt(self, query: str) -> str:
        """
        Get appropriate system prompt based on configuration.

        Args:
            query: User query

        Returns:
            Formatted system prompt
        """
        if self.use_adaptive_prompt:
            return get_adaptive_cot_prompt(query, self.tool_descriptions)
        else:
            return get_cot_prompt("standard", self.tool_descriptions)

    async def run(
        self, query: str, max_iterations: int = 5, enable_reflection: bool = True
    ) -> dict[str, Any]:
        """
        Run agent with CoT reasoning.

        Args:
            query: User query string
            max_iterations: Maximum reasoning iterations
            enable_reflection: Whether to enable reflection loop

        Returns:
            Result dictionary with answer, reasoning trace, and metadata
        """
        # Initialize reasoning trace
        reasoning_trace = []
        iteration_count = 0

        # Add query step
        reasoning_trace.append(
            {
                "step": len(reasoning_trace) + 1,
                "type": "query",
                "content": query,
                "timestamp": self._get_timestamp(),
            }
        )

        # Get system prompt
        system_prompt = self._get_system_prompt(query)

        # Initialize messages
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ]

        # Main reasoning loop
        while iteration_count < max_iterations:
            iteration_count += 1

            # Generate reasoning
            response = self.llm_with_tools.invoke(messages)

            # Parse structured reasoning
            reasoning_parts = ReasoningStructure.parse_reasoning(response.content)

            # Record thinking step
            if reasoning_parts.get("understanding") or reasoning_parts.get("plan"):
                reasoning_trace.append(
                    {
                        "step": len(reasoning_trace) + 1,
                        "type": "thinking",
                        "content": response.content,
                        "understanding": reasoning_parts.get("understanding"),
                        "plan": reasoning_parts.get("plan"),
                        "confidence": reasoning_parts.get("confidence", "MEDIUM"),
                        "alternatives": reasoning_parts.get("alternatives", []),
                        "timestamp": self._get_timestamp(),
                    }
                )

            # Check for tool calls
            if hasattr(response, "tool_calls") and response.tool_calls:
                # Add assistant message
                messages.append(response)

                # Process tool calls
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_input = tool_call["args"]

                    # Record action
                    reasoning_trace.append(
                        {
                            "step": len(reasoning_trace) + 1,
                            "type": "action",
                            "tool": tool_name,
                            "input": tool_input,
                            "timestamp": self._get_timestamp(),
                        }
                    )

                    # Execute tool
                    tool_result = await self._execute_tool(tool_name, tool_input)

                    # Record observation
                    reasoning_trace.append(
                        {
                            "step": len(reasoning_trace) + 1,
                            "type": "observation",
                            "content": str(tool_result),
                            "timestamp": self._get_timestamp(),
                        }
                    )

                    # Add tool result to messages
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call["id"],
                            "name": tool_name,
                            "content": str(tool_result),
                        }
                    )

                    # Optional: Request reflection on tool result
                    if enable_reflection:
                        reflection_step = await self._reflect_on_tool_result(
                            tool_result, query, messages
                        )
                        if reflection_step:
                            reasoning_trace.append(reflection_step)

                # Continue to next iteration
                continue

            else:
                # No tool calls - agent has final answer
                final_answer = response.content

                # Parse final answer components
                reasoning_trace.append(
                    {
                        "step": len(reasoning_trace) + 1,
                        "type": "synthesis",
                        "content": final_answer,
                        "confidence": reasoning_parts.get("confidence", "MEDIUM"),
                        "assumptions": reasoning_parts.get("assumptions", []),
                        "limitations": reasoning_parts.get("limitations", []),
                        "timestamp": self._get_timestamp(),
                    }
                )

                return {
                    "answer": final_answer,
                    "reasoning_trace": reasoning_trace,
                    "metadata": {
                        "model": self.model_name,
                        "temperature": self.temperature,
                        "iterations": iteration_count,
                        "total_steps": len(reasoning_trace),
                        "confidence": reasoning_parts.get("confidence", "MEDIUM"),
                        "use_adaptive_prompt": self.use_adaptive_prompt,
                    },
                    "raw_response": response,
                }

        # Max iterations reached
        return {
            "answer": "Maximum iterations reached without final answer. Please refine your query.",
            "reasoning_trace": reasoning_trace,
            "metadata": {
                "model": self.model_name,
                "temperature": self.temperature,
                "iterations": iteration_count,
                "total_steps": len(reasoning_trace),
                "confidence": "LOW",
                "max_iterations_reached": True,
            },
            "raw_response": None,
        }

    async def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        """
        Execute a tool and return result.

        Args:
            tool_name: Name of tool to execute
            tool_input: Tool input arguments

        Returns:
            Tool execution result as string
        """
        tool = self.tool_map.get(tool_name)

        if not tool:
            return f"Error: Tool '{tool_name}' not found"

        try:
            result = tool.invoke(tool_input)
            return str(result)
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"

    async def _reflect_on_tool_result(
        self, tool_result: str, original_query: str, messages: list[dict]
    ) -> dict | None:
        """
        Optional reflection step on tool results.

        Args:
            tool_result: Result from tool execution
            original_query: Original user query
            messages: Current message history

        Returns:
            Reflection step dict or None
        """
        # For now, just record basic reflection
        # Can be enhanced with LLM-based reflection
        return {
            "step": -1,  # Will be adjusted by caller
            "type": "reflection",
            "content": f"Tool result received. Assessing if this addresses the query: '{original_query[:50]}...'",
            "timestamp": self._get_timestamp(),
        }

    def _get_timestamp(self) -> str:
        """Get current timestamp for trace steps."""
        from datetime import datetime

        return datetime.utcnow().isoformat() + "Z"


def create_cot_agent(
    model_name: str,
    tools: list[BaseTool],
    temperature: float = 0.1,
    use_adaptive_prompt: bool = True,
) -> CoTReActAgent:
    """
    Factory function to create a CoT ReAct agent.

    Args:
        model_name: OpenAI model name
        tools: List of available tools
        temperature: Model temperature
        use_adaptive_prompt: Whether to use adaptive prompts

    Returns:
        Configured CoTReActAgent instance
    """
    return CoTReActAgent(
        model_name=model_name,
        tools=tools,
        temperature=temperature,
        use_adaptive_prompt=use_adaptive_prompt,
    )


async def run_cot_agent(
    agent: CoTReActAgent, query: str, max_iterations: int = 5
) -> dict[str, Any]:
    """
    Run a CoT agent with a query.

    Args:
        agent: CoTReActAgent instance
        query: User query string
        max_iterations: Maximum iterations

    Returns:
        Execution result with reasoning trace
    """
    return await agent.run(query, max_iterations=max_iterations)
