# ŸŽ“ ReAct Agent Analysis Notebooks

## Overview

This directory contains professional Jupyter notebooks for deep analysis of the ReAct (Reasoning + Acting) framework implementation.

---

## Notebooks

### 1. ReAct_Agent_Analysis.ipynb

**Professional analysis notebook with:**

- **Graph Visualizations**: Visual representation of agent execution flow
  - Color-coded nodes (Query †’ Thought â†’ Action â†’ Observation â†’ Answer)
  - NetworkX-based directed graphs showing reasoning paths
  - Interactive matplotlib visualizations

- **Three Test Cases**:
  1. **Database Query**: Single-tool usage (Pink Floyd database)
  2. **Currency Query**: Single-tool usage (Currency API)
  3. **Multi-Tool Query**: Complex query requiring both tools

- **Critical Analysis**:
  - Step-by-step trace examination
  - Performance metrics comparison
  - Model comparison (gpt-4o-mini vs gpt-4o)
  - Failure mode analysis
  - Production considerations

- **Validation**:
  - Ground truth verification against database
  - Answer accuracy checking
  - Coherence evaluation

---

## Quick Start

### 1. Launch Jupyter

```bash
# From project root
uv run jupyter notebook notebooks/

# Or use Jupyter Lab
uv run jupyter lab notebooks/
```

### 2. Open Notebook

Open `ReAct_Agent_Analysis.ipynb` in the Jupyter interface

### 3. Run Cells

Execute cells sequentially (Shift+Enter) to:
- Initialize agent and tools
- Run test queries
- Generate graph visualizations
- Compare performance metrics

---

## What You'll Learn

### ReAct Framework Fundamentals

1. **How ReAct Works**:
   - Thought: LLM reasons about what to do
   - Action: LLM selects and calls a tool
   - Observation: Tool returns results
   - Iteration: Repeat until answer is complete

2. **Visual Understanding**:
   - See the reasoning path as a graph
   - Identify decision points
   - Understand tool selection logic
   - Track information flow

3. **Performance Characteristics**:
   - Execution time per query type
   - Token usage patterns
   - Cost estimation
   - Complexity scaling

### Critical Engineering Insights

**Strengths**:
- Transparent decision-making
- Autonomous tool selection
- Handles complex multi-step queries
- Easy to debug via trace

**Weaknesses**:
- Multiple LLM calls increase latency
- Token costs scale with complexity
- Potential for infinite loops
- Context window limitations

**Production Considerations**:
- Max iteration limits needed
- Error handling is critical
- Monitoring tool usage patterns
- Caching for performance

---

## Notebook Structure

### Section 1: Framework Overview
- ReAct loop explanation
- Conceptual diagrams
- Key terminology

### Section 2-3: Agent Initialization & Database Query
- Setup and configuration
- Single-tool query execution
- Graph visualization
- Detailed trace analysis

### Section 4-5: Currency & Multi-Tool Queries
- Different query types
- Tool coordination
- Comparative analysis

### Section 6: Performance Comparison
- Side-by-side metrics
- Visualization charts
- Cost/time analysis

### Section 7: Critical Analysis
- Strengths and weaknesses
- Failure modes
- Production recommendations

### Section 8: Validation
- Ground truth checking
- Answer accuracy verification

### Section 9: Model Comparison (Optional)
- gpt-4o-mini vs gpt-4o
- Cost/performance trade-offs

### Section 10: Conclusion
- Key takeaways
- When to use ReAct
- Next steps

---

## Visualizations

The notebook generates several types of visualizations:

### 1. Execution Graphs (NetworkX)
- **Pink nodes**: Query (starting point)
- **Blue nodes**: Thoughts (reasoning)
- **Green nodes**: Actions (tool calls)
- **Orange nodes**: Observations (results)
- **Purple nodes**: Answer (final output)

### 2. Performance Charts (Matplotlib)
- Execution time comparison
- Token usage comparison
- Cost comparison
- Complexity metrics (steps + tools)

### 3. Comparison Tables (Pandas)
- Styled DataFrames with gradient backgrounds
- Side-by-side metrics
- Statistical summaries

---

## Requirements

All dependencies are installed automatically with:
```bash
uv sync --group dev
```

**Key libraries**:
- `jupyter`: Notebook environment
- `matplotlib`: Plotting and visualization
- `seaborn`: Statistical visualizations
- `networkx`: Graph creation and analysis
- `pandas`: Data manipulation
- `IPython`: Rich display support

---

## Tips for Best Results

### 1. Environment Setup
```bash
# Ensure database is initialized
uv run python scripts/setup_database.py

# Ensure OpenAI API key is set
echo $OPENAI_API_KEY
```

### 2. Running Queries
- **Start with simple queries** to understand the flow
- **Observe the graphs** to see reasoning patterns
- **Compare metrics** across different query types
- **Experiment** with your own queries

### 3. Critical Analysis
- Question every tool call: Was it necessary?
- Check answer accuracy against ground truth
- Consider alternative reasoning paths
- Think about failure scenarios

### 4. Model Comparison
- Run same query on different models
- Compare cost vs quality trade-offs
- Consider production constraints

---

## Expected Results

### Database Query
- 1 tool call (pink_floyd_database)
- ~2-4 seconds execution
- ~500-1000 tokens
- ~$0.001-0.002 cost

### Currency Query
- 1 tool call (currency_price_checker)
- ~2-3 seconds execution
- ~400-800 tokens
- ~$0.001-0.002 cost

### Multi-Tool Query
- 2 tool calls (both tools)
- ~4-6 seconds execution
- ~800-1500 tokens
- ~$0.002-0.004 cost

*Note: Actual values may vary based on query complexity and model selection*

---

## Troubleshooting

### "Module not found" errors
```bash
# Reinstall dependencies
uv sync --group dev
```

### "Database not found" errors
```bash
# Initialize database
uv run python scripts/setup_database.py
```

### "OpenAI API key not configured"
```bash
# Set API key in .env file
echo "OPENAI_API_KEY=your_key_here" > .env
```

### Graphs not displaying
```bash
# Ensure matplotlib backend is set
%matplotlib inline  # Add this to notebook cell
```

---

## Further Reading

- **ReAct Paper**: https://arxiv.org/abs/2210.03629
- **LangChain Agents**: https://python.langchain.com/docs/modules/agents/
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **NetworkX Documentation**: https://networkx.org/documentation/stable/

---

## Contributing

To add new notebooks:

1. Create notebook in this directory
2. Add documentation to this README
3. Ensure notebook runs from start to finish
4. Include clear explanations and visualizations
5. Add to git: `git add notebooks/your_notebook.ipynb`

---

## License

Part of the henry_clase_demo project. See main README for details.
