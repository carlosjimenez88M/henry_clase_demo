"""
Professional Design System for Pink Floyd AI Agent Dashboard.

Provides centralized styling, theme configuration, and reusable
UI components. NO EMOJIS - Professional appearance only.
"""

import streamlit as st
from typing import Optional


class DesignSystem:
    """
    Professional design system - NO EMOJIS.

    Colors, typography, spacing, and components designed for
    a clean, professional appearance.
    """

    # Color palette
    COLORS = {
        "primary": "#FF1493",        # Pink Floyd pink
        "primary_dark": "#C71585",   # Darker pink
        "success": "#10B981",        # Green
        "error": "#EF4444",          # Red
        "warning": "#F59E0B",        # Orange
        "info": "#3B82F6",           # Blue
        "background": "#0E1117",     # Dark background
        "surface": "#262730",        # Card background
        "text_primary": "#FAFAFA",   # Primary text
        "text_secondary": "#9CA3AF", # Secondary text
        "border": "#374151",         # Borders
    }

    # Typography
    FONT_SIZES = {
        "h1": "2.5rem",
        "h2": "2rem",
        "h3": "1.5rem",
        "h4": "1.25rem",
        "body": "1rem",
        "small": "0.875rem",
    }

    # Spacing
    SPACING = {
        "xs": "0.25rem",
        "sm": "0.5rem",
        "md": "1rem",
        "lg": "1.5rem",
        "xl": "2rem",
        "xxl": "3rem",
    }

    @classmethod
    def inject_css(cls):
        """Inject professional CSS styling."""
        css = f"""
        <style>
        /* Import professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Global styles */
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }}

        /* Remove default Streamlit padding */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Professional metric card */
        .metric-card {{
            background: {cls.COLORS['surface']};
            border-radius: 0.5rem;
            padding: 1.5rem;
            border-left: 4px solid {cls.COLORS['primary']};
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .metric-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.4);
        }}

        .metric-card-label {{
            color: {cls.COLORS['text_secondary']};
            font-size: {cls.FONT_SIZES['small']};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .metric-card-value {{
            color: {cls.COLORS['text_primary']};
            font-size: {cls.FONT_SIZES['h2']};
            font-weight: 700;
            margin: 0.5rem 0;
        }}

        .metric-card-delta {{
            color: {cls.COLORS['text_secondary']};
            font-size: {cls.FONT_SIZES['small']};
        }}

        /* Professional buttons */
        .stButton>button {{
            background: linear-gradient(90deg, {cls.COLORS['primary']} 0%, {cls.COLORS['primary_dark']} 100%);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(255, 20, 147, 0.3);
        }}

        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255, 20, 147, 0.4);
        }}

        /* Professional info boxes */
        .info-box {{
            background: {cls.COLORS['surface']};
            border-left: 4px solid {cls.COLORS['info']};
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}

        .success-box {{
            background: {cls.COLORS['surface']};
            border-left: 4px solid {cls.COLORS['success']};
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}

        .warning-box {{
            background: {cls.COLORS['surface']};
            border-left: 4px solid {cls.COLORS['warning']};
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}

        .error-box {{
            background: {cls.COLORS['surface']};
            border-left: 4px solid {cls.COLORS['error']};
            border-radius: 0.5rem;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        }}

        /* Professional code blocks */
        .stCodeBlock {{
            background: {cls.COLORS['surface']};
            border-radius: 0.5rem;
            border: 1px solid {cls.COLORS['border']};
        }}

        /* Professional data tables */
        .dataframe {{
            background: {cls.COLORS['surface']};
            border-radius: 0.5rem;
        }}

        /* Professional sidebar */
        [data-testid="stSidebar"] {{
            background: {cls.COLORS['surface']};
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Professional headers */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            letter-spacing: -0.02em;
        }}

        h1 {{
            background: linear-gradient(90deg, {cls.COLORS['primary']} 0%, {cls.COLORS['primary_dark']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        /* Professional expander */
        .streamlit-expanderHeader {{
            background: {cls.COLORS['surface']};
            border-radius: 0.5rem;
            font-weight: 600;
        }}

        /* Professional selectbox and inputs */
        .stSelectbox, .stTextInput, .stTextArea {{
            border-radius: 0.5rem;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    @classmethod
    def metric_card(cls, label: str, value: str, delta: Optional[str] = None):
        """
        Display a professional metric card.

        Args:
            label: Metric label (e.g., "Total Queries")
            value: Metric value (e.g., "1,234")
            delta: Optional delta/change indicator
        """
        delta_html = f'<div class="metric-card-delta">{delta}</div>' if delta else ""

        html = f"""
        <div class="metric-card">
            <div class="metric-card-label">{label}</div>
            <div class="metric-card-value">{value}</div>
            {delta_html}
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    @classmethod
    def info_box(cls, message: str, box_type: str = "info"):
        """
        Display a professional info/success/warning/error box.

        Args:
            message: Message to display
            box_type: Type of box - "info", "success", "warning", "error"
        """
        html = f'<div class="{box_type}-box">{message}</div>'
        st.markdown(html, unsafe_allow_html=True)

    @classmethod
    def section_header(cls, title: str, subtitle: Optional[str] = None):
        """
        Display a professional section header.

        Args:
            title: Section title
            subtitle: Optional subtitle
        """
        st.markdown(f"## {title}")
        if subtitle:
            st.markdown(f"*{subtitle}*")
        st.markdown("---")

    @classmethod
    def stat_row(cls, stats: list[tuple[str, str, Optional[str]]]):
        """
        Display a row of statistics.

        Args:
            stats: List of (label, value, delta) tuples
        """
        cols = st.columns(len(stats))
        for col, (label, value, delta) in zip(cols, stats):
            with col:
                cls.metric_card(label, value, delta)

    @classmethod
    def divider(cls):
        """Display a professional divider."""
        st.markdown(
            f'<hr style="border: 1px solid {cls.COLORS["border"]}; margin: 2rem 0;">',
            unsafe_allow_html=True
        )


# Convenience function for initialization
def init_design_system():
    """Initialize the design system (call at the top of each page)."""
    DesignSystem.inject_css()
