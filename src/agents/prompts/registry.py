"""
Prompt registry for managing and retrieving prompt templates.

Provides centralized access to all prompt templates with
caching and dynamic selection capabilities.
"""

from typing import Dict, Type, Optional
from src.agents.prompts.templates import CoTPromptTemplate
from src.agents.prompts.cot_templates import (
    StandardCoTTemplate,
    VerboseCoTTemplate,
    ConciseCoTTemplate,
    AdaptiveCoTTemplate
)


class PromptRegistry:
    """
    Central registry for managing prompt templates.

    Features:
    - Template registration and retrieval
    - Template caching
    - Dynamic template selection
    - Template versioning support
    """

    _templates: Dict[str, Type[CoTPromptTemplate]] = {
        "standard": StandardCoTTemplate,
        "verbose": VerboseCoTTemplate,
        "concise": ConciseCoTTemplate,
        "default": StandardCoTTemplate
    }

    _template_cache: Dict[str, str] = {}

    @classmethod
    def register_template(cls, name: str, template_class: Type[CoTPromptTemplate]) -> None:
        """
        Register a new template.

        Args:
            name: Template identifier
            template_class: Template class
        """
        cls._templates[name] = template_class
        cls._clear_cache(name)

    @classmethod
    def get_template(cls, name: str = "default") -> Type[CoTPromptTemplate]:
        """
        Get template by name.

        Args:
            name: Template identifier

        Returns:
            Template class

        Raises:
            KeyError: If template not found
        """
        if name not in cls._templates:
            raise KeyError(f"Template '{name}' not found. Available: {list(cls._templates.keys())}")

        return cls._templates[name]

    @classmethod
    def get_adaptive_template(cls, query: str) -> Type[CoTPromptTemplate]:
        """
        Get template dynamically based on query complexity.

        Args:
            query: User query string

        Returns:
            Appropriate template class
        """
        complexity = AdaptiveCoTTemplate.assess_complexity(query)
        return AdaptiveCoTTemplate.select_template(query, complexity)

    @classmethod
    def format_prompt(
        cls,
        template_name: str,
        tools: list,
        use_cache: bool = True
    ) -> str:
        """
        Format system prompt with tool descriptions.

        Args:
            template_name: Name of template to use
            tools: List of available tools
            use_cache: Whether to use cached prompts

        Returns:
            Formatted system prompt
        """
        cache_key = f"{template_name}_{len(tools)}"

        if use_cache and cache_key in cls._template_cache:
            return cls._template_cache[cache_key]

        template_class = cls.get_template(template_name)
        formatted = template_class.format_system_prompt(tools)

        if use_cache:
            cls._template_cache[cache_key] = formatted

        return formatted

    @classmethod
    def list_templates(cls) -> list[str]:
        """Get list of available template names."""
        return list(cls._templates.keys())

    @classmethod
    def _clear_cache(cls, template_name: Optional[str] = None) -> None:
        """Clear template cache."""
        if template_name:
            # Clear specific template cache
            keys_to_remove = [k for k in cls._template_cache if k.startswith(template_name)]
            for key in keys_to_remove:
                del cls._template_cache[key]
        else:
            # Clear all cache
            cls._template_cache.clear()

    @classmethod
    def get_template_info(cls, name: str) -> dict:
        """
        Get metadata about a template.

        Args:
            name: Template identifier

        Returns:
            Template metadata dictionary
        """
        template_class = cls.get_template(name)

        return {
            "name": name,
            "class": template_class.__name__,
            "description": template_class.__doc__.strip() if template_class.__doc__ else "No description",
            "system_template_length": len(template_class.SYSTEM_TEMPLATE)
        }


# Convenience functions
def get_cot_prompt(template_name: str = "default", tools: list = None) -> str:
    """
    Convenience function to get formatted CoT prompt.

    Args:
        template_name: Name of template (default, standard, verbose, concise)
        tools: List of available tools

    Returns:
        Formatted system prompt
    """
    tools = tools or []
    return PromptRegistry.format_prompt(template_name, tools)


def get_adaptive_cot_prompt(query: str, tools: list = None) -> str:
    """
    Get adaptive CoT prompt based on query complexity.

    Args:
        query: User query
        tools: List of available tools

    Returns:
        Formatted system prompt with appropriate template
    """
    tools = tools or []
    template_class = PromptRegistry.get_adaptive_template(query)
    return template_class.format_system_prompt(tools)
