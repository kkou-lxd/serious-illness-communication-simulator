"""Main entry point for the Serious Illness Communication Simulator."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="Serious Illness Communication Simulator",
    page_icon="💬",
    layout="wide",
)


def _inject_styles() -> None:
    css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


_inject_styles()

st.title("Serious Illness Communication Simulator")
st.write(
    """
This proof-of-concept demonstrates a teacher and student workflow for
serious illness communication training. Use the sidebar to navigate
between the Home, Teacher, Student, Simulation, and Evaluation views.
"""
)

st.page_link("pages/1_Home.py", label="Go to Home", icon="🏠")
