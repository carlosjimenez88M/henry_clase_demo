"""
Reasoning Validator for assessing Chain of Thought quality.

This module provides validation logic to ensure reasoning steps
are explicit, thorough, and meet quality standards.
"""

from dataclasses import dataclass
from enum import Enum


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""

    CRITICAL = "critical"  # Must be fixed
    WARNING = "warning"  # Should be improved
    INFO = "info"  # Minor suggestion


@dataclass
class ValidationIssue:
    """Represents a single validation issue."""

    severity: ValidationSeverity
    category: str
    message: str
    suggestion: str


@dataclass
class ValidationResult:
    """Result of reasoning validation."""

    is_valid: bool
    score: float  # 0.0 to 1.0
    issues: list[ValidationIssue]
    strengths: list[str]

    @property
    def has_critical_issues(self) -> bool:
        """Check if there are any critical issues."""
        return any(
            issue.severity == ValidationSeverity.CRITICAL for issue in self.issues
        )

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(
            issue.severity == ValidationSeverity.WARNING for issue in self.issues
        )

    def get_issues_by_severity(
        self, severity: ValidationSeverity
    ) -> list[ValidationIssue]:
        """Get issues filtered by severity."""
        return [issue for issue in self.issues if issue.severity == severity]


class ReasoningValidator:
    """
    Validates quality of Chain of Thought reasoning.

    Quality criteria:
    1. Explicit thinking - Not just "I'll use tool X"
    2. Considers alternatives - Shows multiple approaches were evaluated
    3. Has confidence assessment - Includes HIGH/MEDIUM/LOW confidence
    4. Identifies assumptions - Acknowledges what's being assumed
    5. Validates tool results - Checks if results are as expected
    6. Handles uncertainty - Explicitly states when uncertain
    """

    # Quality thresholds
    MIN_LENGTH = 50  # Minimum characters for reasoning
    MIN_SCORE_VALID = 0.6  # Minimum score to be considered valid

    # Keywords for different quality dimensions
    EXPLICIT_THINKING_KEYWORDS = [
        "because",
        "since",
        "therefore",
        "thus",
        "reasoning",
        "understand",
        "need to",
        "should",
        "considering",
    ]

    ALTERNATIVE_KEYWORDS = [
        "alternative",
        "instead",
        "could also",
        "another option",
        "considered",
        "compared to",
        "versus",
        "or",
    ]

    CONFIDENCE_KEYWORDS = [
        "confidence",
        "high",
        "medium",
        "low",
        "certain",
        "uncertain",
    ]

    ASSUMPTION_KEYWORDS = ["assume", "assuming", "assumption", "if", "given that"]

    VALIDATION_KEYWORDS = ["expected", "unexpected", "validates", "confirms", "check"]

    def validate(self, reasoning: str) -> ValidationResult:
        """
        Validate reasoning quality.

        Args:
            reasoning: The reasoning text to validate

        Returns:
            ValidationResult with score, issues, and strengths
        """
        issues = []
        strengths = []
        score_components = {}

        # 1. Check explicit thinking
        explicit_score = self._check_explicit_thinking(reasoning, issues, strengths)
        score_components["explicit"] = explicit_score

        # 2. Check alternatives consideration
        alternatives_score = self._check_alternatives(reasoning, issues, strengths)
        score_components["alternatives"] = alternatives_score

        # 3. Check confidence assessment
        confidence_score = self._check_confidence(reasoning, issues, strengths)
        score_components["confidence"] = confidence_score

        # 4. Check assumptions identification
        assumptions_score = self._check_assumptions(reasoning, issues, strengths)
        score_components["assumptions"] = assumptions_score

        # 5. Check length and detail
        detail_score = self._check_detail_level(reasoning, issues, strengths)
        score_components["detail"] = detail_score

        # Calculate overall score (weighted average)
        overall_score = (
            explicit_score * 0.30
            + alternatives_score * 0.20
            + confidence_score * 0.20
            + assumptions_score * 0.15
            + detail_score * 0.15
        )

        # Determine if valid
        is_valid = overall_score >= self.MIN_SCORE_VALID and not any(
            issue.severity == ValidationSeverity.CRITICAL for issue in issues
        )

        return ValidationResult(
            is_valid=is_valid,
            score=round(overall_score, 2),
            issues=issues,
            strengths=strengths,
        )

    def _check_explicit_thinking(
        self, reasoning: str, issues: list[ValidationIssue], strengths: list[str]
    ) -> float:
        """Check if reasoning is explicit and detailed."""
        reasoning_lower = reasoning.lower()

        # Count explicit thinking keywords
        keyword_count = sum(
            1
            for keyword in self.EXPLICIT_THINKING_KEYWORDS
            if keyword in reasoning_lower
        )

        # Check for mere tool announcement (bad)
        tool_announcement_patterns = ["i'll use", "i will use", "using the", "call the"]

        has_tool_announcement = any(
            pattern in reasoning_lower for pattern in tool_announcement_patterns
        )

        # Check for explicit reasoning (good)
        has_reasoning = keyword_count >= 2

        score = 0.0

        if has_reasoning:
            score = min(1.0, keyword_count / 5.0)
            strengths.append("Reasoning shows explicit thinking process")
        else:
            score = 0.3
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="explicit_thinking",
                    message="Reasoning lacks explicit thinking - appears to just announce tool usage",
                    suggestion="Explain WHY you're taking this approach and HOW it addresses the query",
                )
            )

        if has_tool_announcement and keyword_count < 2:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="explicit_thinking",
                    message="Reasoning focuses on tool usage rather than problem-solving approach",
                    suggestion="Focus on the reasoning process, not just which tools to use",
                )
            )

        return score

    def _check_alternatives(
        self, reasoning: str, issues: list[ValidationIssue], strengths: list[str]
    ) -> float:
        """Check if alternatives were considered."""
        reasoning_lower = reasoning.lower()

        # Count alternative consideration keywords
        keyword_count = sum(
            1 for keyword in self.ALTERNATIVE_KEYWORDS if keyword in reasoning_lower
        )

        if keyword_count >= 1:
            strengths.append("Reasoning considers alternative approaches")
            return min(1.0, keyword_count / 2.0)
        else:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="alternatives",
                    message="No alternative approaches mentioned",
                    suggestion="Consider and mention at least one alternative approach before choosing your method",
                )
            )
            return 0.4

    def _check_confidence(
        self, reasoning: str, issues: list[ValidationIssue], strengths: list[str]
    ) -> float:
        """Check if confidence is assessed."""
        reasoning_lower = reasoning.lower()

        # Check for confidence keywords
        has_confidence = any(
            keyword in reasoning_lower for keyword in self.CONFIDENCE_KEYWORDS
        )

        # Check for explicit confidence levels
        has_explicit_level = any(
            level in reasoning_lower for level in ["high", "medium", "low"]
        )

        if has_explicit_level:
            strengths.append("Reasoning includes explicit confidence assessment")
            return 1.0
        elif has_confidence:
            strengths.append("Reasoning mentions confidence")
            return 0.7
        else:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    category="confidence",
                    message="No confidence assessment provided",
                    suggestion="Include confidence level (HIGH/MEDIUM/LOW) with reasoning for your approach",
                )
            )
            return 0.3

    def _check_assumptions(
        self, reasoning: str, issues: list[ValidationIssue], strengths: list[str]
    ) -> float:
        """Check if assumptions are identified."""
        reasoning_lower = reasoning.lower()

        # Count assumption keywords
        keyword_count = sum(
            1 for keyword in self.ASSUMPTION_KEYWORDS if keyword in reasoning_lower
        )

        if keyword_count >= 1:
            strengths.append("Reasoning identifies assumptions")
            return min(1.0, keyword_count / 2.0)
        else:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.INFO,
                    category="assumptions",
                    message="No assumptions explicitly identified",
                    suggestion="State any assumptions you're making about the query or approach",
                )
            )
            return 0.5

    def _check_detail_level(
        self, reasoning: str, issues: list[ValidationIssue], strengths: list[str]
    ) -> float:
        """Check if reasoning has sufficient detail."""
        length = len(reasoning)

        if length < self.MIN_LENGTH:
            issues.append(
                ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="detail",
                    message=f"Reasoning too brief ({length} chars, minimum {self.MIN_LENGTH})",
                    suggestion="Provide more detailed reasoning about your approach and thinking",
                )
            )
            return 0.2

        # Score based on length
        if length > 300:
            strengths.append("Reasoning is detailed and thorough")
            return 1.0
        elif length > 150:
            return 0.8
        else:
            return 0.6


class ReasoningImprover:
    """
    Suggests improvements to reasoning based on validation results.
    """

    @staticmethod
    def generate_improvement_prompt(
        original_reasoning: str, validation_result: ValidationResult
    ) -> str:
        """
        Generate a prompt to improve reasoning.

        Args:
            original_reasoning: Original reasoning text
            validation_result: Validation result with issues

        Returns:
            Improvement prompt for the agent
        """
        if validation_result.is_valid:
            return ""

        prompt_parts = [
            "Your reasoning needs improvement. Please address the following issues:\n"
        ]

        # Add critical issues
        critical = validation_result.get_issues_by_severity(ValidationSeverity.CRITICAL)
        if critical:
            prompt_parts.append("\nCRITICAL ISSUES:")
            for issue in critical:
                prompt_parts.append(f"- {issue.message}")
                prompt_parts.append(f"  Suggestion: {issue.suggestion}")

        # Add warnings
        warnings = validation_result.get_issues_by_severity(ValidationSeverity.WARNING)
        if warnings:
            prompt_parts.append("\nIMPROVEMENTS NEEDED:")
            for issue in warnings:
                prompt_parts.append(f"- {issue.message}")
                prompt_parts.append(f"  Suggestion: {issue.suggestion}")

        prompt_parts.append(
            f"\nYour reasoning score: {validation_result.score:.2f}/1.00"
        )
        prompt_parts.append(
            "\nPlease provide improved reasoning that addresses these issues."
        )

        return "\n".join(prompt_parts)
