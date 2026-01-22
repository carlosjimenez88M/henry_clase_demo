"""
Professional error handling components.
"""

import streamlit as st
import traceback
from typing import Optional


class ErrorBoundary:
    """
    Error boundary for graceful error handling in Streamlit.

    Usage:
        with ErrorBoundary():
            # Your code here
    """

    def __init__(self, show_traceback: bool = False):
        """
        Initialize error boundary.

        Args:
            show_traceback: Whether to show full traceback
        """
        self.show_traceback = show_traceback

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            display_error(exc_val, show_traceback=self.show_traceback)
            return True  # Suppress exception
        return False


def display_error(error: Exception, show_traceback: bool = False, title: str = "Error Occurred"):
    """
    Display a professional error message.

    Args:
        error: Exception that occurred
        show_traceback: Whether to show full traceback
        title: Error title
    """
    st.error(f"**{title}**")

    # Error message
    st.markdown(f"```\n{str(error)}\n```")

    if show_traceback:
        with st.expander("Show Traceback"):
            st.code(traceback.format_exc(), language="python")


def display_warning(message: str, title: str = "Warning"):
    """
    Display a professional warning message.

    Args:
        message: Warning message
        title: Warning title
    """
    st.warning(f"**{title}**\n\n{message}")


def display_success(message: str, title: str = "Success"):
    """
    Display a professional success message.

    Args:
        message: Success message
        title: Success title
    """
    st.success(f"**{title}**\n\n{message}")


def display_info(message: str, title: str = "Information"):
    """
    Display a professional info message.

    Args:
        message: Info message
        title: Info title
    """
    st.info(f"**{title}**\n\n{message}")
