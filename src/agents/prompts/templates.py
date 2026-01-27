"""
Base Chain of Thought prompt template system.

This module defines the core CoT prompt structure that enforces
explicit reasoning, confidence levels, and self-reflection.
"""

from dataclasses import dataclass


@dataclass
class CoTPromptTemplate:
    """
    Chain of Thought prompt template with explicit reasoning steps.

    This template enforces a structured reasoning process:
    1. UNDERSTAND - Comprehend the query
    2. PLAN - Decide on approach and tools
    3. EXECUTE - Use tools and gather information
    4. REFLECT - Validate results and assess quality
    5. SYNTHESIZE - Formulate final answer with confidence
    """

    SYSTEM_TEMPLATE = """You are a reasoning AI agent with access to tools for querying information.

CRITICAL: You MUST follow this Chain of Thought (CoT) reasoning process for EVERY query:

## STEP 1: UNDERSTAND
Before taking any action, clearly articulate:
- What information is being requested?
- What are the key requirements?
- What format should the answer take?
- Are there any ambiguities that need clarification?

## STEP 2: PLAN
Develop your approach:
- Which tools will you use and WHY?
- What is your reasoning strategy?
- What alternatives did you consider?
- Why is this approach better than alternatives?
- Confidence level in this approach: HIGH / MEDIUM / LOW
- What could go wrong?

## STEP 3: EXECUTE
Use tools to gather information:
- Execute your planned tool calls
- After EACH tool result, validate: "Is this what I expected?"
- If unexpected: Explain why and adjust plan
- Document any surprises or issues

## STEP 4: REFLECT
After gathering information:
- Does the information fully answer the query?
- Are there gaps, inconsistencies, or contradictions?
- Should I gather more information?
- Do I need to use additional tools?
- What assumptions am I making?

## STEP 5: SYNTHESIZE
Formulate your final answer:
- Provide a clear, comprehensive answer
- State your confidence: HIGH / MEDIUM / LOW
- Mention any assumptions or limitations
- Identify edge cases or caveats

## RESPONSE FORMAT

Your reasoning should be structured and explicit. When thinking through the problem:

**UNDERSTANDING:**
[Explain what you understand about the query]

**PLAN:**
[Describe your approach, tools to use, and reasoning]
- Confidence: [HIGH/MEDIUM/LOW]
- Alternatives considered: [List alternatives]
- Potential issues: [What could go wrong]

**EXECUTION:**
[Use tools and validate results]

**REFLECTION:**
[Assess quality and completeness of information]

**FINAL ANSWER:**
[Clear, comprehensive answer]
- Confidence: [HIGH/MEDIUM/LOW]
- Assumptions: [List any assumptions]
- Limitations: [Note any limitations]

## AVAILABLE TOOLS

You have access to the following tools:

{tool_descriptions}

## CRITICAL RULES

1. ALWAYS show your reasoning explicitly - never skip steps
2. ALWAYS assess confidence levels (HIGH/MEDIUM/LOW)
3. ALWAYS consider alternatives before choosing an approach
4. ALWAYS validate tool results against expectations
5. ALWAYS identify assumptions and limitations
6. If you encounter unexpected results, explain why and adjust
7. If information is incomplete, acknowledge gaps explicitly

Remember: The goal is transparent, reliable reasoning. Make your thinking visible!
"""

    TOOL_DESCRIPTION_TEMPLATE = """
- **{tool_name}**: {tool_description}
  Input schema: {input_schema}
"""

    VALIDATION_PROMPT = """
You previously provided reasoning for this query. However, your reasoning has some issues:

{issues}

Please improve your reasoning by addressing these concerns. Be more explicit about:
1. Your understanding of the problem
2. Why you chose this approach
3. What alternatives you considered
4. Your confidence level and reasoning
"""

    REFLECTION_PROMPT = """
Based on the tool result:
{tool_result}

Reflect on this result:
1. Is this what you expected? Why or why not?
2. Does this fully address the query or do you need more information?
3. Are there any unexpected patterns or issues?
4. Should you adjust your approach?

Provide your reflection:
"""

    @classmethod
    def format_system_prompt(cls, tools: list[dict]) -> str:
        """
        Format the system prompt with tool descriptions.

        Args:
            tools: List of tool dictionaries with name, description, and schema

        Returns:
            Formatted system prompt with tool information
        """
        tool_descriptions = ""
        for tool in tools:
            tool_descriptions += cls.TOOL_DESCRIPTION_TEMPLATE.format(
                tool_name=tool.get("name", "Unknown"),
                tool_description=tool.get("description", "No description"),
                input_schema=tool.get("input_schema", "No schema"),
            )

        return cls.SYSTEM_TEMPLATE.format(tool_descriptions=tool_descriptions)

    @classmethod
    def format_validation_prompt(cls, issues: list[str]) -> str:
        """
        Format a prompt to request improved reasoning.

        Args:
            issues: List of issues with the reasoning

        Returns:
            Formatted validation prompt
        """
        issues_text = "\n".join(f"- {issue}" for issue in issues)
        return cls.VALIDATION_PROMPT.format(issues=issues_text)

    @classmethod
    def format_reflection_prompt(cls, tool_result: str) -> str:
        """
        Format a prompt for reflection on tool results.

        Args:
            tool_result: The result from tool execution

        Returns:
            Formatted reflection prompt
        """
        return cls.REFLECTION_PROMPT.format(tool_result=tool_result)


class ReasoningStructure:
    """Helper class to parse structured reasoning from LLM responses."""

    @staticmethod
    def parse_reasoning(response: str) -> dict[str, str | None]:
        """
        Parse structured reasoning from LLM response.

        Extracts:
        - understanding
        - plan
        - confidence
        - alternatives
        - reflection
        - final_answer

        Args:
            response: Raw LLM response text

        Returns:
            Dictionary with extracted reasoning components
        """
        result = {
            "understanding": None,
            "plan": None,
            "confidence": "MEDIUM",  # Default
            "alternatives": [],
            "potential_issues": [],
            "reflection": None,
            "final_answer": None,
            "assumptions": [],
            "limitations": [],
        }

        # Simple extraction (can be enhanced with regex or LLM parsing)
        response_lower = response.lower()

        # Extract confidence
        if "confidence: high" in response_lower:
            result["confidence"] = "HIGH"
        elif "confidence: low" in response_lower:
            result["confidence"] = "LOW"

        # Extract sections
        sections = {
            "understanding": ["understanding:", "step 1"],
            "plan": ["plan:", "step 2"],
            "reflection": ["reflection:", "step 4"],
            "final_answer": ["final answer:", "step 5"],
        }

        for key, markers in sections.items():
            for marker in markers:
                if marker in response_lower:
                    # Find the section start
                    start_idx = response_lower.find(marker)
                    # Find next section or end
                    end_idx = len(response)
                    for other_key, other_markers in sections.items():
                        if other_key != key:
                            for other_marker in other_markers:
                                marker_idx = response_lower.find(
                                    other_marker, start_idx + len(marker)
                                )
                                if marker_idx != -1 and marker_idx < end_idx:
                                    end_idx = marker_idx

                    result[key] = response[start_idx:end_idx].strip()
                    break

        return result

    @staticmethod
    def extract_confidence(text: str) -> str:
        """Extract confidence level from text."""
        text_lower = text.lower()
        if "high" in text_lower:
            return "HIGH"
        elif "low" in text_lower:
            return "LOW"
        return "MEDIUM"
