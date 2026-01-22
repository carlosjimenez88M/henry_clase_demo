"""
Professional metric display components.
"""

import streamlit as st
from typing import Optional, List, Tuple


class MetricCard:
    """Professional metric card component."""

    @staticmethod
    def display(label: str, value: str, delta: Optional[str] = None, help_text: Optional[str] = None):
        """
        Display a single metric card.

        Args:
            label: Metric label
            value: Metric value
            delta: Optional delta text
            help_text: Optional help text
        """
        st.metric(
            label=label,
            value=value,
            delta=delta,
            help=help_text
        )


class StatsRow:
    """Row of statistics display."""

    @staticmethod
    def display(stats: List[Tuple[str, str, Optional[str]]]):
        """
        Display multiple metrics in a row.

        Args:
            stats: List of (label, value, delta) tuples
        """
        cols = st.columns(len(stats))
        for col, (label, value, delta) in zip(cols, stats):
            with col:
                MetricCard.display(label, value, delta)
