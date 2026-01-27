"""
Prompt templates for Chain of Thought reasoning.

This module provides structured prompts that enforce explicit reasoning,
confidence assessment, and self-reflection in AI agents.
"""

from src.agents.prompts.cot_templates import (
    AdaptiveCoTTemplate,
    ConciseCoTTemplate,
    StandardCoTTemplate,
    VerboseCoTTemplate,
)
from src.agents.prompts.registry import (
    PromptRegistry,
    get_adaptive_cot_prompt,
    get_cot_prompt,
)
from src.agents.prompts.templates import CoTPromptTemplate, ReasoningStructure

__all__ = [
    "CoTPromptTemplate",
    "ReasoningStructure",
    "StandardCoTTemplate",
    "VerboseCoTTemplate",
    "ConciseCoTTemplate",
    "AdaptiveCoTTemplate",
    "PromptRegistry",
    "get_cot_prompt",
    "get_adaptive_cot_prompt",
]
