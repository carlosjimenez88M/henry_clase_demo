"""Quick manual test of the ReAct agent."""

from src.agents.agent_factory import AgentFactory
from src.agents.agent_executor import AgentExecutor

# Create agent factory
factory = AgentFactory()

# Create agent with gpt-4o-mini
print("Creating agent with gpt-4o-mini...")
agent = factory.create_agent("gpt-4o-mini")

# Create executor
executor = AgentExecutor(agent, "gpt-4o-mini")

# Test query 1: Database tool
print("\n" + "="*60)
print("TEST 1: Database Tool - Find melancholic songs")
print("="*60)
result = executor.execute("Find melancholic Pink Floyd songs")
print(f"\n Answer:\n{result['answer']}")
print(f"\n⏱  Time: {result['metrics']['execution_time_seconds']}s")
print(f" Tokens: {result['metrics']['estimated_tokens']['total']}")
print(f" Cost: ${result['metrics']['estimated_cost_usd']}")

print("\n Reasoning Trace:")
for step in result['reasoning_trace']:
    if step['type'] == 'action':
        print(f"  → Action: {step['tool']}")
    elif step['type'] == 'observation':
        print(f"  ← Observation: {step['content'][:100]}...")

# Test query 2: Currency tool
print("\n" + "="*60)
print("TEST 2: Currency Tool - USD to EUR")
print("="*60)
result2 = executor.execute("What's the current USD to EUR exchange rate?")
print(f"\n Answer:\n{result2['answer']}")
print(f"\n⏱  Time: {result2['metrics']['execution_time_seconds']}s")
print(f" Tokens: {result2['metrics']['estimated_tokens']['total']}")
print(f" Cost: ${result2['metrics']['estimated_cost_usd']}")

# Summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
summary = executor.get_metrics_summary()
print(f"Total executions: {summary['num_executions']}")
print(f"Total time: {summary['total_time_seconds']}s")
print(f"Total tokens: {summary['total_tokens']}")
print(f"Total cost: ${summary['total_cost_usd']}")

print("\n Agent test complete!")
