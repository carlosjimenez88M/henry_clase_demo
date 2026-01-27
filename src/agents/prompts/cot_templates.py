"""
Specialized Chain of Thought template variants.

Provides different CoT templates for various use cases:
- StandardCoTTemplate: Balanced reasoning depth
- VerboseCoTTemplate: Maximum reasoning detail
- ConciseCoTTemplate: Minimal but complete reasoning
"""

from src.agents.prompts.templates import CoTPromptTemplate


class StandardCoTTemplate(CoTPromptTemplate):
    """
    Standard CoT template with balanced reasoning depth.

    Use for most queries where thorough reasoning is needed
    but not excessive verbosity.
    """

    pass  # Uses base template


class VerboseCoTTemplate(CoTPromptTemplate):
    """
    Verbose CoT template for complex queries requiring detailed reasoning.

    Use when:
    - Query is particularly complex
    - High stakes decision
    - Need maximum transparency
    """

    SYSTEM_TEMPLATE = """You are a reasoning AI agent with access to tools for querying information.

CRITICAL: You MUST provide EXTREMELY DETAILED Chain of Thought reasoning for this complex query.

## DETAILED REASONING PROCESS

### STEP 1: DEEP UNDERSTANDING
Thoroughly analyze the query:
- Primary question being asked
- Implicit requirements or expectations
- Context and background assumptions
- Potential ambiguities or edge cases
- Expected output format and detail level
- Any domain-specific considerations

### STEP 2: COMPREHENSIVE PLANNING
Develop a detailed strategy:
- List ALL potentially relevant tools
- For EACH tool, explain:
  * Why it might be useful
  * What information it would provide
  * Pros and cons of using it
- Choose your final approach with detailed justification
- Consider AT LEAST 2-3 alternative approaches
- Explain why your chosen approach is superior
- Identify potential failure modes and mitigation strategies
- Confidence assessment: HIGH / MEDIUM / LOW with reasoning

### STEP 3: METHODICAL EXECUTION
Execute with careful validation:
- Before using each tool: State expected outcome
- After each tool result: Compare actual vs expected
- If unexpected: Provide detailed analysis of why
- Document all observations and patterns
- Track cumulative information gathered

### STEP 4: CRITICAL REFLECTION
Rigorously evaluate results:
- Completeness: Does this answer all aspects of the query?
- Accuracy: Are there any inconsistencies or contradictions?
- Gaps: What information is still missing?
- Quality: How reliable is this information?
- Need for additional tools: Should I gather more data?
- Validation: How can I verify these results?

### STEP 5: COMPREHENSIVE SYNTHESIS
Provide a complete answer:
- Main answer with full detail
- Supporting evidence and reasoning
- Confidence level: HIGH / MEDIUM / LOW with justification
- Detailed list of assumptions
- Known limitations or caveats
- Alternative interpretations if applicable
- Recommendations for further investigation if needed

## AVAILABLE TOOLS

{tool_descriptions}

## CRITICAL RULES

1. Leave NO reasoning step implicit - explain EVERYTHING
2. Consider MULTIPLE alternatives before deciding
3. Validate EVERY tool result against expectations
4. Identify ALL assumptions and limitations
5. Provide detailed confidence assessments with reasoning
6. If uncertain, be VERY explicit about what and why

Your goal is MAXIMUM TRANSPARENCY and RELIABILITY in reasoning.
"""


class ConciseCoTTemplate(CoTPromptTemplate):
    """
    Concise CoT template for simpler queries.

    Use when:
    - Query is straightforward
    - Quick response needed
    - Reasoning path is clear

    Still maintains core CoT principles but with less verbosity.
    """

    SYSTEM_TEMPLATE = """You are a reasoning AI agent with access to tools.

IMPORTANT: Provide clear, concise Chain of Thought reasoning.

## REASONING PROCESS

**UNDERSTAND:**
What is being asked? What's needed?

**PLAN:**
- Approach: [Your strategy]
- Tools: [Which tools and why]
- Confidence: [HIGH/MEDIUM/LOW]

**EXECUTE:**
Use tools and validate results.

**REFLECT:**
Does this answer the query? Any issues?

**ANSWER:**
[Clear, direct answer]
- Confidence: [HIGH/MEDIUM/LOW]
- Assumptions: [If any]

## AVAILABLE TOOLS

{tool_descriptions}

## RULES

1. Show your reasoning clearly but concisely
2. Always assess confidence
3. Validate tool results
4. Note assumptions or limitations

Be clear, accurate, and efficient.
"""


class AdaptiveCoTTemplate:
    """
    Adaptive template selector that chooses the appropriate
    CoT template based on query characteristics.
    """

    @staticmethod
    def select_template(
        query: str, complexity: str = "medium"
    ) -> type[CoTPromptTemplate]:
        """
        Select appropriate CoT template based on query complexity.

        Args:
            query: The user query
            complexity: Complexity level - "low", "medium", "high"

        Returns:
            Appropriate CoT template class
        """
        if complexity == "high":
            return VerboseCoTTemplate
        elif complexity == "low":
            return ConciseCoTTemplate
        else:
            return StandardCoTTemplate

    @staticmethod
    def assess_complexity(query: str) -> str:
        """
        Assess query complexity to select appropriate template.

        Args:
            query: User query string

        Returns:
            Complexity level: "low", "medium", or "high"
        """
        # Simple heuristics (can be enhanced with ML)
        query_lower = query.lower()

        # High complexity indicators
        high_complexity_keywords = [
            "compare",
            "analyze",
            "explain why",
            "what if",
            "evaluate",
            "assess",
            "multiple",
            "complex",
        ]

        # Low complexity indicators
        low_complexity_keywords = ["find", "list", "what is", "show", "get"]

        word_count = len(query.split())

        # Check for high complexity
        if word_count > 20 or any(kw in query_lower for kw in high_complexity_keywords):
            return "high"

        # Check for low complexity
        if word_count < 10 and any(kw in query_lower for kw in low_complexity_keywords):
            return "low"

        # Default to medium
        return "medium"
