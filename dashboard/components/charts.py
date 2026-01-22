"""
Professional chart components using Plotly.
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any


def create_execution_time_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create execution time chart.

    Args:
        data: List of execution dictionaries with timestamp and execution_time

    Returns:
        Plotly figure
    """
    if not data:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig

    timestamps = [d.get("timestamp", "") for d in data]
    times = [d.get("execution_time", 0) for d in data]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=times,
        mode='lines+markers',
        name='Execution Time',
        line=dict(color='#FF1493', width=2),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title="Execution Time Over Time",
        xaxis_title="Timestamp",
        yaxis_title="Execution Time (seconds)",
        template="plotly_dark",
        hovermode='x unified'
    )

    return fig


def create_cost_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """
    Create cost analysis chart.

    Args:
        data: List of execution dictionaries with timestamp and cost

    Returns:
        Plotly figure
    """
    if not data:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False
        )
        return fig

    timestamps = [d.get("timestamp", "") for d in data]
    costs = [d.get("estimated_cost", 0) for d in data]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=timestamps,
        y=costs,
        name='Cost',
        marker=dict(color='#10B981')
    ))

    fig.update_layout(
        title="Cost Per Query",
        xaxis_title="Timestamp",
        yaxis_title="Cost (USD)",
        template="plotly_dark",
        hovermode='x unified'
    )

    return fig


def create_model_comparison_chart(comparison_data: Dict[str, Any]) -> go.Figure:
    """
    Create model comparison chart.

    Args:
        comparison_data: Dictionary with model comparison data

    Returns:
        Plotly figure
    """
    models = list(comparison_data.keys())
    times = [comparison_data[m].get("execution_time_seconds", 0) for m in models]
    costs = [comparison_data[m].get("estimated_cost_usd", 0) for m in models]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Execution Time (s)',
        x=models,
        y=times,
        marker=dict(color='#FF1493')
    ))

    fig.add_trace(go.Bar(
        name='Cost (USD)',
        x=models,
        y=costs,
        marker=dict(color='#10B981'),
        yaxis='y2'
    ))

    fig.update_layout(
        title="Model Performance Comparison",
        xaxis_title="Model",
        yaxis_title="Execution Time (seconds)",
        yaxis2=dict(
            title="Cost (USD)",
            overlaying='y',
            side='right'
        ),
        template="plotly_dark",
        barmode='group'
    )

    return fig
