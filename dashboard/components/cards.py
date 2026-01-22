"""
Professional card components.
"""

import streamlit as st
from typing import Optional


class InfoCard:
    """Professional information card."""

    @staticmethod
    def display(title: str, content: str, card_type: str = "info"):
        """
        Display an info card.

        Args:
            title: Card title
            content: Card content
            card_type: Type - info, success, warning, error
        """
        with st.container():
            st.markdown(f"**{title}**")
            st.markdown(content)


class CodeCard:
    """Professional code display card."""

    @staticmethod
    def display(code: str, language: str = "python", title: Optional[str] = None):
        """
        Display code in a professional card.

        Args:
            code: Code content
            language: Programming language
            title: Optional title
        """
        if title:
            st.markdown(f"**{title}**")
        st.code(code, language=language)
