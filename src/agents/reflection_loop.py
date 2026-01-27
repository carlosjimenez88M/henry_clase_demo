"""
Reflection Loop for self-correction in CoT agents.

This module implements a reflection mechanism that allows agents
to self-assess and improve their reasoning before providing final answers.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ReflectionType(Enum):
    """Types of reflection."""

    TOOL_RESULT_VALIDATION = "tool_result_validation"
    REASONING_QUALITY = "reasoning_quality"
    ANSWER_COMPLETENESS = "answer_completeness"
    CONSISTENCY_CHECK = "consistency_check"


@dataclass
class ReflectionResult:
    """Result of a reflection step."""

    should_continue: bool
    issue_detected: str | None
    correction_needed: str | None
    confidence_adjustment: str | None  # "increase" or "decrease"
    next_action: str | None


class ReflectionLoop:
    """
    Implements self-reflection and correction logic for CoT agents.

    The reflection loop enables agents to:
    1. Validate tool results against expectations
    2. Assess reasoning quality
    3. Check answer completeness
    4. Identify inconsistencies
    5. Self-correct when issues detected
    """

    def __init__(self, max_corrections: int = 2):
        """
        Initialize reflection loop.

        Args:
            max_corrections: Maximum number of correction attempts
        """
        self.max_corrections = max_corrections
        self.correction_count = 0

    def reflect_on_tool_result(
        self,
        tool_name: str,
        tool_input: dict,
        tool_output: str,
        expected_output: str | None = None,
    ) -> ReflectionResult:
        """
        Reflect on a tool result to validate if it's as expected.

        Args:
            tool_name: Name of tool executed
            tool_input: Input provided to tool
            tool_output: Output received from tool
            expected_output: Optional expected output description

        Returns:
            ReflectionResult indicating if continuation needed
        """
        # Check for errors in tool output
        if "error" in tool_output.lower() or "failed" in tool_output.lower():
            return ReflectionResult(
                should_continue=True,
                issue_detected=f"Tool '{tool_name}' returned an error",
                correction_needed="Consider alternative tool or approach",
                confidence_adjustment="decrease",
                next_action="try_alternative_tool",
            )

        # Check if output is empty or too short
        if len(tool_output.strip()) < 10:
            return ReflectionResult(
                should_continue=True,
                issue_detected=f"Tool '{tool_name}' returned insufficient data",
                correction_needed="May need to refine tool input or use additional tools",
                confidence_adjustment="decrease",
                next_action="gather_more_information",
            )

        # Check if output matches expectations (if provided)
        if expected_output:
            # Simple keyword matching (can be enhanced)
            expected_keywords = expected_output.lower().split()
            output_lower = tool_output.lower()

            matches = sum(1 for keyword in expected_keywords if keyword in output_lower)
            match_ratio = matches / len(expected_keywords) if expected_keywords else 0

            if match_ratio < 0.3:
                return ReflectionResult(
                    should_continue=True,
                    issue_detected="Tool result doesn't match expectations",
                    correction_needed="Result may not be relevant - consider different approach",
                    confidence_adjustment="decrease",
                    next_action="reconsider_approach",
                )

        # Tool result looks good
        return ReflectionResult(
            should_continue=False,
            issue_detected=None,
            correction_needed=None,
            confidence_adjustment=None,
            next_action="proceed",
        )

    def reflect_on_reasoning(self, reasoning: str, query: str) -> ReflectionResult:
        """
        Reflect on reasoning quality.

        Args:
            reasoning: The reasoning text to evaluate
            query: Original query

        Returns:
            ReflectionResult indicating if reasoning needs improvement
        """
        # Check reasoning length
        if len(reasoning) < 50:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Reasoning is too brief",
                correction_needed="Provide more detailed explanation of your thinking",
                confidence_adjustment="decrease",
                next_action="elaborate_reasoning",
            )

        # Check if reasoning addresses the query
        query_keywords = query.lower().split()
        reasoning_lower = reasoning.lower()

        query_relevance = sum(
            1
            for keyword in query_keywords
            if len(keyword) > 3 and keyword in reasoning_lower
        )

        if query_relevance == 0:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Reasoning doesn't seem to address the query",
                correction_needed="Ensure reasoning directly addresses the user's question",
                confidence_adjustment="decrease",
                next_action="refocus_on_query",
            )

        # Check for explicit thinking indicators
        thinking_indicators = [
            "because",
            "since",
            "therefore",
            "reasoning",
            "consider",
            "need to",
            "should",
        ]

        has_thinking = any(
            indicator in reasoning_lower for indicator in thinking_indicators
        )

        if not has_thinking:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Reasoning lacks explicit thinking process",
                correction_needed="Show your thinking: WHY this approach, WHAT alternatives considered",
                confidence_adjustment="decrease",
                next_action="make_reasoning_explicit",
            )

        # Reasoning looks good
        return ReflectionResult(
            should_continue=False,
            issue_detected=None,
            correction_needed=None,
            confidence_adjustment=None,
            next_action="proceed",
        )

    def reflect_on_answer_completeness(
        self, query: str, answer: str, tool_results: list[str]
    ) -> ReflectionResult:
        """
        Reflect on whether answer is complete.

        Args:
            query: Original user query
            answer: Proposed final answer
            tool_results: Results from tools used

        Returns:
            ReflectionResult indicating if answer is complete
        """
        # Check answer length
        if len(answer) < 30:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Answer is too brief",
                correction_needed="Provide a more comprehensive answer",
                confidence_adjustment="decrease",
                next_action="elaborate_answer",
            )

        # Check if answer references tool results
        has_references = False
        for tool_result in tool_results:
            # Check if key info from tool is mentioned in answer
            tool_words = set(tool_result.lower().split())
            answer_words = set(answer.lower().split())
            overlap = len(tool_words & answer_words)

            if overlap > 5:  # Some overlap with tool results
                has_references = True
                break

        if not has_references and tool_results:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Answer doesn't reference tool results",
                correction_needed="Ensure answer incorporates information from tools used",
                confidence_adjustment="decrease",
                next_action="integrate_tool_results",
            )

        # Check if answer addresses key query terms
        query_keywords = [
            word
            for word in query.lower().split()
            if len(word) > 4  # Focus on meaningful words
        ]

        answer_lower = answer.lower()
        addressed_keywords = sum(
            1 for keyword in query_keywords if keyword in answer_lower
        )

        if query_keywords and addressed_keywords / len(query_keywords) < 0.3:
            return ReflectionResult(
                should_continue=True,
                issue_detected="Answer may not fully address the query",
                correction_needed="Ensure all aspects of the query are addressed",
                confidence_adjustment="decrease",
                next_action="address_all_query_aspects",
            )

        # Answer looks complete
        return ReflectionResult(
            should_continue=False,
            issue_detected=None,
            correction_needed=None,
            confidence_adjustment=None,
            next_action="finalize",
        )

    def check_consistency(
        self, reasoning_trace: list[dict[str, Any]]
    ) -> ReflectionResult:
        """
        Check for consistency across reasoning trace.

        Args:
            reasoning_trace: List of reasoning steps

        Returns:
            ReflectionResult indicating if inconsistencies found
        """
        # Extract confidence levels mentioned
        confidence_levels = []
        for step in reasoning_trace:
            if "confidence" in step:
                confidence_levels.append(step["confidence"])

        # Check for confidence inconsistency
        if confidence_levels:
            high_count = confidence_levels.count("HIGH")
            low_count = confidence_levels.count("LOW")

            # Inconsistent if both high and low confidence
            if high_count > 0 and low_count > 0:
                return ReflectionResult(
                    should_continue=True,
                    issue_detected="Inconsistent confidence levels across reasoning",
                    correction_needed="Resolve confidence inconsistency - reassess overall confidence",
                    confidence_adjustment="decrease",
                    next_action="reassess_confidence",
                )

        # Check for repeated tool use (might indicate inefficiency)
        tool_uses = {}
        for step in reasoning_trace:
            if step.get("type") == "action":
                tool_name = step.get("tool")
                tool_uses[tool_name] = tool_uses.get(tool_name, 0) + 1

        for tool_name, count in tool_uses.items():
            if count > 2:
                return ReflectionResult(
                    should_continue=True,
                    issue_detected=f"Tool '{tool_name}' used {count} times - may be inefficient",
                    correction_needed="Consider if tool is being used optimally",
                    confidence_adjustment=None,
                    next_action="optimize_tool_usage",
                )

        # No consistency issues
        return ReflectionResult(
            should_continue=False,
            issue_detected=None,
            correction_needed=None,
            confidence_adjustment=None,
            next_action="proceed",
        )

    def should_attempt_correction(self) -> bool:
        """Check if another correction attempt should be made."""
        return self.correction_count < self.max_corrections

    def record_correction(self):
        """Record that a correction was attempted."""
        self.correction_count += 1

    def reset(self):
        """Reset correction counter."""
        self.correction_count = 0


class ReflectionPromptGenerator:
    """Generates prompts for reflection-based corrections."""

    @staticmethod
    def generate_correction_prompt(reflection: ReflectionResult) -> str:
        """
        Generate a prompt for the agent to self-correct.

        Args:
            reflection: ReflectionResult with issue details

        Returns:
            Correction prompt string
        """
        if not reflection.issue_detected:
            return ""

        prompt_parts = [
            "SELF-REFLECTION: An issue was detected in your reasoning.",
            f"\nIssue: {reflection.issue_detected}",
            f"\nCorrection needed: {reflection.correction_needed}",
        ]

        if reflection.confidence_adjustment:
            prompt_parts.append(
                f"\nNote: Your confidence should be adjusted {reflection.confidence_adjustment}."
            )

        prompt_parts.append(
            "\nPlease address this issue and continue with improved reasoning."
        )

        return "\n".join(prompt_parts)

    @staticmethod
    def generate_validation_prompt(tool_result: str, expected: str) -> str:
        """
        Generate a prompt asking the agent to validate a tool result.

        Args:
            tool_result: The actual tool result
            expected: What was expected

        Returns:
            Validation prompt
        """
        return f"""
VALIDATION REQUEST:

You expected: {expected}

You received: {tool_result}

Does this result match your expectations? If not, explain the discrepancy and how you should adjust your approach.
        """.strip()
