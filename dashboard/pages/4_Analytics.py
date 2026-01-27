"""
Analytics Dashboard Page.

Provides insights into agent usage, performance, and costs.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import os
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import httpx
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Analytics", page_icon="Analytics", layout="wide")

# Import design system
from dashboard.design_system import init_design_system

# Initialize design system
init_design_system()

# Title
st.title("Analytics Dashboard")
st.markdown("Insights into agent performance, usage patterns, and costs")

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Fetch data from API
@st.cache_data(ttl=60)
def fetch_metrics():
    """Fetch metrics from API."""
    try:
        response = httpx.get(f"{API_URL}/api/v1/metrics/summary", timeout=10.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching metrics: {e}")
        return None

# Fetch storage stats
@st.cache_data(ttl=60)
def fetch_storage_stats():
    """Fetch storage statistics."""
    try:
        response = httpx.get(f"{API_URL}/api/v1/metrics/storage", timeout=10.0)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# Fetch recent executions
@st.cache_data(ttl=30)
def fetch_recent_executions(limit=100):
    """Fetch recent execution history."""
    try:
        response = httpx.get(
            f"{API_URL}/api/v1/agent/history",
            params={"limit": limit},
            timeout=10.0
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("executions", [])
        return []
    except Exception as e:
        return []

# Main content
with st.spinner("Cargando analytics..."):
    metrics = fetch_metrics()
    storage_stats = fetch_storage_stats()
    executions = fetch_recent_executions(100)

if not metrics and not storage_stats:
    st.warning("No se pueden cargar las métricas. Asegúrate de que la API esté corriendo.")
    st.stop()

# Overview metrics
st.markdown("## Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_queries = storage_stats.get("total_executions", 0) if storage_stats else 0
    st.metric("Total Queries", f"{total_queries:,}")

with col2:
    total_cost = storage_stats.get("total_cost_usd", 0) if storage_stats else 0
    st.metric("Total Cost", f"${total_cost:.4f}")

with col3:
    total_tokens = storage_stats.get("total_tokens", 0) if storage_stats else 0
    st.metric("Total Tokens", f"{total_tokens:,}")

with col4:
    if storage_stats:
        db_size_mb = storage_stats.get("database_size_mb", 0)
        st.metric("DB Size", f"{db_size_mb:.2f} MB")

st.markdown("---")

# Agent type distribution
st.markdown("## Agent Type Usage")

if storage_stats and "by_agent_type" in storage_stats:
    agent_types = storage_stats["by_agent_type"]

    fig = go.Figure(data=[
        go.Pie(
            labels=list(agent_types.keys()),
            values=list(agent_types.values()),
            hole=0.4,
            marker=dict(colors=['#FF1493', '#10B981'])
        )
    ])

    fig.update_layout(
        title="Distribución por Tipo de Agente",
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No hay datos de tipo de agente disponibles.")

st.markdown("---")

# Model usage distribution
st.markdown("## Model Usage")

if storage_stats and "by_model" in storage_stats:
    models = storage_stats["by_model"]

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(data=[
            go.Bar(
                x=list(models.keys()),
                y=list(models.values()),
                marker=dict(color='#FF1493')
            )
        ])

        fig.update_layout(
            title="Queries por Modelo",
            xaxis_title="Modelo",
            yaxis_title="Cantidad",
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Show as table
        df = pd.DataFrame({
            "Modelo": list(models.keys()),
            "Queries": list(models.values())
        })
        df["Porcentaje"] = (df["Queries"] / df["Queries"].sum() * 100).round(2)
        st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")

# Recent activity timeline
st.markdown("## Recent Activity")

if executions:
    df_exec = pd.DataFrame(executions)

    # Execution time over time
    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(df_exec))),
            y=df_exec["execution_time"],
            mode='lines+markers',
            name='Tiempo de Ejecución',
            line=dict(color='#FF1493', width=2),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title="Tiempo de Ejecución (últimas queries)",
            xaxis_title="Query #",
            yaxis_title="Tiempo (segundos)",
            template="plotly_dark",
            height=350
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Average by model
        if "model" in df_exec.columns:
            avg_by_model = df_exec.groupby("model")["execution_time"].mean().reset_index()

            fig = go.Figure(data=[
                go.Bar(
                    x=avg_by_model["model"],
                    y=avg_by_model["execution_time"],
                    marker=dict(color='#10B981')
                )
            ])

            fig.update_layout(
                title="Tiempo Promedio por Modelo",
                xaxis_title="Modelo",
                yaxis_title="Tiempo Promedio (s)",
                template="plotly_dark",
                height=350
            )

            st.plotly_chart(fig, use_container_width=True)

    # Cost analysis
    st.markdown("---")
    st.markdown("## Cost Analysis")

    if "estimated_cost" in df_exec.columns:
        col1, col2 = st.columns(2)

        with col1:
            # Cost over time
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=list(range(len(df_exec))),
                y=df_exec["estimated_cost"],
                marker=dict(color='#F59E0B')
            ))

            fig.update_layout(
                title="Costo por Query",
                xaxis_title="Query #",
                yaxis_title="Costo (USD)",
                template="plotly_dark",
                height=350
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Stats
            st.markdown("### Estadísticas de Costo")
            st.metric("Costo Promedio", f"${df_exec['estimated_cost'].mean():.6f}")
            st.metric("Costo M�ximo", f"${df_exec['estimated_cost'].max():.6f}")
            st.metric("Costo Minimo", f"${df_exec['estimated_cost'].min():.6f}")
            st.metric("Costo Total (muestra)", f"${df_exec['estimated_cost'].sum():.6f}")

    # Recent queries table
    st.markdown("---")
    st.markdown("## Recent Queries")

    display_df = df_exec.copy()
    if "query" in display_df.columns:
        display_df["query"] = display_df["query"].str[:50] + "..."

    columns_to_show = []
    if "query" in display_df.columns:
        columns_to_show.append("query")
    if "model" in display_df.columns:
        columns_to_show.append("model")
    if "agent_type" in display_df.columns:
        columns_to_show.append("agent_type")
    if "execution_time" in display_df.columns:
        columns_to_show.append("execution_time")
    if "estimated_cost" in display_df.columns:
        columns_to_show.append("estimated_cost")

    if columns_to_show:
        st.dataframe(
            display_df[columns_to_show].head(20),
            use_container_width=True,
            hide_index=True
        )

else:
    st.info("No hay ejecuciones recientes para mostrar.")

# Cache statistics
st.markdown("---")
st.markdown("## Cache Performance")

try:
    response = httpx.get(f"{API_URL}/api/v1/metrics/cache", timeout=5.0)
    if response.status_code == 200:
        cache_stats = response.json()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Cache Size", f"{cache_stats.get('size', 0)}/{cache_stats.get('max_size', 100)}")

        with col2:
            st.metric("Hit Rate", f"{cache_stats.get('hit_rate_percent', 0):.1f}%")

        with col3:
            st.metric("Cache Hits", cache_stats.get('hits', 0))

        with col4:
            st.metric("Cache Misses", cache_stats.get('misses', 0))
except Exception as e:
    st.info("Estadísticas de cache no disponibles.")

# Refresh button
st.markdown("---")
if st.button("Refrescar Datos", type="primary"):
    st.cache_data.clear()
    st.rerun()
