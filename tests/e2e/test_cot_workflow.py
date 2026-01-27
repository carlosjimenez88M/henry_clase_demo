"""
E2E Tests for Chain of Thought Workflow.

Tests the complete CoT reasoning flow from query to answer.
"""


import pytest

from src.agents.agent_executor import AgentExecutor
from src.agents.agent_factory import AgentFactory


class TestCoTWorkflow:
    """Test CoT agent end-to-end workflow."""

    @pytest.fixture
    def agent_factory(self):
        """Create agent factory."""
        return AgentFactory(default_agent_type="cot")

    @pytest.fixture
    def test_query(self):
        """Test query."""
        return "Find melancholic Pink Floyd songs"

    def test_cot_agent_creation(self, agent_factory):
        """Test that CoT agent can be created."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        assert agent is not None
        assert hasattr(agent, "run")

    @pytest.mark.asyncio
    async def test_cot_agent_execution(self, agent_factory, test_query):
        """Test that CoT agent executes successfully."""
        # Create agent
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")

        # Create executor
        executor = AgentExecutor(agent, "gpt-4o-mini")

        # Execute query
        result = await executor.execute(test_query)

        # Verify result structure
        assert "answer" in result
        assert "reasoning_trace" in result
        assert "metrics" in result
        assert result["answer"] is not None
        assert len(result["answer"]) > 0

    @pytest.mark.asyncio
    async def test_cot_reasoning_trace_structure(self, agent_factory, test_query):
        """Test that CoT reasoning trace has proper structure."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        executor = AgentExecutor(agent, "gpt-4o-mini")
        result = await executor.execute(test_query)

        trace = result["reasoning_trace"]
        assert len(trace) > 0

        # Check for CoT-specific step types
        step_types = [step.get("type") for step in trace]
        assert "query" in step_types  # Should have query step

        # Check that steps have required fields
        for step in trace:
            assert "step" in step
            assert "type" in step
            assert "timestamp" in step

    @pytest.mark.asyncio
    async def test_cot_confidence_levels(self, agent_factory, test_query):
        """Test that CoT agent provides confidence levels."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        executor = AgentExecutor(agent, "gpt-4o-mini")
        result = await executor.execute(test_query)

        # Check for confidence in metadata
        if "metadata" in result:
            assert "confidence" in result["metadata"]
            assert result["metadata"]["confidence"] in ["HIGH", "MEDIUM", "LOW"]

    @pytest.mark.asyncio
    async def test_cot_vs_react_comparison(self, agent_factory, test_query):
        """Test that CoT agent produces different output than ReAct."""
        # Create CoT agent
        cot_agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        cot_executor = AgentExecutor(cot_agent, "gpt-4o-mini")
        cot_result = await cot_executor.execute(test_query)

        # Create ReAct agent
        react_agent = agent_factory.create_agent("gpt-4o-mini", agent_type="react")
        react_executor = AgentExecutor(react_agent, "gpt-4o-mini")
        react_result = await react_executor.execute(test_query)

        # Both should have answers
        assert cot_result["answer"] is not None
        assert react_result["answer"] is not None

        # CoT should have metadata
        assert "metadata" in cot_result
        assert cot_result["metrics"]["agent_type"] == "cot"

        # ReAct should not have CoT metadata
        assert react_result["metrics"]["agent_type"] == "react"

    @pytest.mark.asyncio
    async def test_multiple_queries_same_agent(self, agent_factory):
        """Test that same agent can handle multiple queries."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        executor = AgentExecutor(agent, "gpt-4o-mini")

        queries = [
            "Find energetic Pink Floyd songs",
            "What's the USD to EUR exchange rate?",
            "Show songs from The Wall album",
        ]

        for query in queries:
            result = await executor.execute(query)
            assert result["answer"] is not None
            assert len(result["reasoning_trace"]) > 0

    @pytest.mark.asyncio
    async def test_error_handling(self, agent_factory):
        """Test that agent handles errors gracefully."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        executor = AgentExecutor(agent, "gpt-4o-mini")

        # Empty query
        result = await executor.execute("")
        assert result is not None

    @pytest.mark.asyncio
    async def test_performance_metrics(self, agent_factory, test_query):
        """Test that performance metrics are captured."""
        agent = agent_factory.create_agent("gpt-4o-mini", agent_type="cot")
        executor = AgentExecutor(agent, "gpt-4o-mini")
        result = await executor.execute(test_query)

        metrics = result["metrics"]
        assert "execution_time_seconds" in metrics
        assert "estimated_tokens" in metrics
        assert "estimated_cost_usd" in metrics
        assert "num_steps" in metrics
        assert "agent_type" in metrics

        # Values should be reasonable
        assert metrics["execution_time_seconds"] > 0
        assert metrics["estimated_tokens"]["total"] > 0
        assert metrics["estimated_cost_usd"] >= 0
        assert metrics["num_steps"] > 0
