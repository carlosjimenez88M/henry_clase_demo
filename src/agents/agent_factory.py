"""
Agent Factory for creating ReAct agents with different models.

This module provides a factory pattern for creating agents with different
OpenAI models and configurations.
"""

from typing import List, Optional

from langchain.tools import BaseTool

from src.agents.react_agent import create_react_agent
from src.config import config
from src.tools.currency_tool import CurrencyPriceTool
from src.tools.database_tool import PinkFloydDatabaseTool


class AgentFactory:
    """Factory for creating ReAct agents with different configurations."""

    # Available models
    SUPPORTED_MODELS = ["gpt-4o-mini", "gpt-4o", "gpt-5-nano"]

    def __init__(self):
        """Initialize agent factory."""
        self.tools = self._initialize_tools()

    def _initialize_tools(self) -> List[BaseTool]:
        """Initialize the tools available to agents."""
        return [
            PinkFloydDatabaseTool(),
            CurrencyPriceTool()
        ]

    def create_agent(
        self,
        model_name: str,
        temperature: Optional[float] = None,
        custom_tools: Optional[List[BaseTool]] = None
    ):
        """
        Create a ReAct agent with specified model.

        Args:
            model_name: Model name (e.g., 'gpt-4o-mini')
            temperature: Optional temperature override
            custom_tools: Optional custom tools (defaults to standard tools)

        Returns:
            Compiled LangGraph agent

        Raises:
            ValueError: If model_name is not supported
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(
                f"Model '{model_name}' not supported. "
                f"Available models: {self.SUPPORTED_MODELS}"
            )

        # Get model configuration
        model_config = config.get_model_config(model_name)

        # Use provided temperature or default from config
        temp = temperature if temperature is not None else model_config.temperature

        # Use provided tools or default tools
        tools = custom_tools if custom_tools is not None else self.tools

        # Create agent
        agent = create_react_agent(
            model_name=model_name,
            tools=tools,
            temperature=temp
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

    def get_tools(self) -> List[BaseTool]:
        """Get list of available tools."""
        return self.tools

    def get_supported_models(self) -> List[str]:
        """Get list of supported models."""
        return self.SUPPORTED_MODELS
