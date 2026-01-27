"""
Agent Factory for creating ReAct agents with different models.

This module provides a factory pattern for creating agents with different
OpenAI models and configurations. Supports both standard ReAct and CoT-enhanced agents.
"""

from typing import Literal

from langchain.tools import BaseTool

from src.agents.cot_agent import CoTReActAgent, create_cot_agent
from src.agents.langgraph_react_agent import create_langgraph_react_agent
from src.agents.react_agent import create_react_agent
from src.config import config
from src.tools.currency_tool import CurrencyPriceTool
from src.tools.database_tool import PinkFloydDatabaseTool

AgentType = Literal["react", "cot", "langgraph_react"]


class AgentFactory:
    """Factory for creating ReAct agents with different configurations."""

    # Available models
    SUPPORTED_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-5-nano"]

    # Default agent type
    DEFAULT_AGENT_TYPE: AgentType = "cot"  # Use CoT by default for better reasoning

    def __init__(self, default_agent_type: AgentType = "cot"):
        """
        Initialize agent factory.

        Args:
            default_agent_type: Default agent type to create ("react" or "cot")
        """
        self.tools = self._initialize_tools()
        self.default_agent_type = default_agent_type

    def _initialize_tools(self) -> list[BaseTool]:
        """Initialize the tools available to agents."""
        return [PinkFloydDatabaseTool(), CurrencyPriceTool()]

    def create_agent(
        self,
        model_name: str,
        temperature: float | None = None,
        custom_tools: list[BaseTool] | None = None,
        agent_type: AgentType | None = None,
        use_adaptive_prompt: bool = True,
    ):
        """
        Create an agent with specified configuration.

        Args:
            model_name: Model name (e.g., 'gpt-4o-mini')
            temperature: Optional temperature override
            custom_tools: Optional custom tools (defaults to standard tools)
            agent_type: Type of agent ("react" or "cot"). Defaults to factory's default.
            use_adaptive_prompt: For CoT agents, whether to use adaptive prompts

        Returns:
            Configured agent (either standard ReAct or CoT)

        Raises:
            ValueError: If model_name is not supported or agent_type is invalid
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model '{model_name}' not supported. "
                f"Available models: {self.SUPPORTED_MODELS}"
            )

        # Get model configuration
        model_config = config.get_model_config(model_name)
        temp = temperature if temperature is not None else model_config.temperature

        # Use provided tools or default tools
        tools = custom_tools if custom_tools is not None else self.tools

        # Determine agent type
        agent_type_to_use = (
            agent_type if agent_type is not None else self.default_agent_type
        )

        # Create appropriate agent type
        if agent_type_to_use == "cot":
            agent = create_cot_agent(
                model_name=model_name,
                tools=tools,
                temperature=temp,
                use_adaptive_prompt=use_adaptive_prompt,
            )
        elif agent_type_to_use == "react":
            agent = create_react_agent(
                model_name=model_name, tools=tools, temperature=temp
            )
        elif agent_type_to_use == "langgraph_react":
            agent = create_langgraph_react_agent(
                model_name=model_name, tools=tools, temperature=temp
            )
        else:
            raise ValueError(
                f"Invalid agent_type '{agent_type_to_use}'. "
                f"Supported types: 'react', 'cot', 'langgraph_react'"
            )

        return agent

    def create_all_agents(self) -> dict:
        """
        Create agents for all supported models.

        Returns:
            Dictionary mapping model names to agents
        """
        agents = {}
        for model_name in self.SUPPORTED_MODELS:
            try:
                agents[model_name] = self.create_agent(model_name)
            except Exception as e:
                print(f"Warning: Failed to create agent for {model_name}: {e}")

        return agents

    def get_tools(self) -> list[BaseTool]:
        """Get list of available tools."""
        return self.tools

    def get_supported_models(self) -> list[str]:
        """Get list of supported models."""
        return self.SUPPORTED_MODELS

    def create_cot_agent(
        self,
        model_name: str,
        temperature: float | None = None,
        use_adaptive_prompt: bool = True,
    ) -> CoTReActAgent:
        """
        Convenience method to create a CoT agent.

        Args:
            model_name: Model name
            temperature: Optional temperature override
            use_adaptive_prompt: Whether to use adaptive prompts

        Returns:
            CoTReActAgent instance
        """
        return self.create_agent(
            model_name=model_name,
            temperature=temperature,
            agent_type="cot",
            use_adaptive_prompt=use_adaptive_prompt,
        )

    def create_react_agent(self, model_name: str, temperature: float | None = None):
        """
        Convenience method to create a standard ReAct agent.

        Args:
            model_name: Model name
            temperature: Optional temperature override

        Returns:
            Standard ReAct agent
        """
        return self.create_agent(
            model_name=model_name, temperature=temperature, agent_type="react"
        )
