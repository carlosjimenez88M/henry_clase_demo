"""
Model Comparison Page.

This page shows comparison results between different models.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

st.set_page_config(page_title="Model Comparison", page_icon="", layout="wide")

st.title(" Model Comparison Dashboard")
st.markdown("Compare performance across different OpenAI models")

# Check if comparison results exist
results_path = Path("data/comparison_results.json")

if not results_path.exists():
    st.warning(" No comparison results found. Run the comparison first!")
    st.markdown("""
    To generate comparison results, run:
    ```bash
    uv run python scripts/run_comparison.py
    ```
    """)

    # Option to run comparison
    if st.button(" Run Comparison Now"):
        with st.spinner("Running comparison... This may take a few minutes."):
            import subprocess
            try:
                subprocess.run([
                    "uv", "run", "python", "scripts/run_comparison.py"
                ], check=True)
                st.success(" Comparison complete! Refresh the page.")
                st.rerun()
            except Exception as e:
                st.error(f" Error: {e}")

else:
    # Load results
    with open(results_path, 'r') as f:
        data = json.load(f)

    comparison = data["comparison"]
    models = data["models"]

    # Summary
    st.markdown("##  Summary")

    cols = st.columns(len(models))
    for i, model in enumerate(models):
        if model in comparison:
            with cols[i]:
                st.markdown(f"### {model}")
                model_data = comparison[model]
                metrics = model_data["metrics"]

                st.metric("Success Rate", f"{model_data['success_rate']}%")
                st.metric("Avg Time", f"{metrics['execution_time']['mean']}s")
                st.metric("Total Tokens", f"{metrics['tokens']['total']}")
                st.metric("Total Cost", f"${metrics['cost']['total']:.6f}")

    # Winners
    if "best" in comparison:
        st.markdown("---")
        st.markdown("##  Winners")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.success(f"** Fastest:** {comparison['best']['fastest']}")

        with col2:
            st.success(f"** Cheapest:** {comparison['best']['cheapest']}")

        with col3:
            st.success(f"** Most Successful:** {comparison['best']['most_successful']}")

    # Charts
    st.markdown("---")
    st.markdown("##  Visualizations")

    # Prepare data for charts
    chart_data = []
    for model in models:
        if model in comparison:
            metrics = comparison[model]["metrics"]
            chart_data.append({
                "Model": model,
                "Avg Time (s)": metrics["execution_time"]["mean"],
                "Total Tokens": metrics["tokens"]["total"],
                "Total Cost ($)": metrics["cost"]["total"],
                "Success Rate (%)": comparison[model]["success_rate"]
            })

    df = pd.DataFrame(chart_data)

    # Response time chart
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  Average Response Time")
        fig = px.bar(
            df,
            x="Model",
            y="Avg Time (s)",
            color="Model",
            title="Average Response Time by Model"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("###  Total Token Usage")
        fig = px.bar(
            df,
            x="Model",
            y="Total Tokens",
            color="Model",
            title="Total Tokens Used by Model"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Cost and success rate
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("###  Total Cost")
        fig = px.bar(
            df,
            x="Model",
            y="Total Cost ($)",
            color="Model",
            title="Total Cost by Model"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("###  Success Rate")
        fig = px.bar(
            df,
            x="Model",
            y="Success Rate (%)",
            color="Model",
            title="Success Rate by Model"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Detailed results
    st.markdown("---")
    st.markdown("##  Detailed Results")

    selected_model = st.selectbox("Select model to view details", models)

    if selected_model in data["results"]:
        results = data["results"][selected_model]

        st.markdown(f"### Results for {selected_model}")

        for i, result in enumerate(results, 1):
            with st.expander(f"Query {i}: {result['query'][:50]}..."):
                st.markdown(f"**Query:** {result['query']}")
                st.markdown(f"**Answer:** {result['answer'][:300]}...")

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Time", f"{result['metrics']['execution_time_seconds']}s")
                with col2:
                    st.metric("Tokens", result['metrics']['estimated_tokens']['total'])
                with col3:
                    st.metric("Cost", f"${result['metrics']['estimated_cost_usd']:.6f}")

    # Export option
    st.markdown("---")
    if st.button(" Export Results to CSV"):
        df.to_csv("data/comparison_summary.csv", index=False)
        st.success(" Exported to data/comparison_summary.csv")
