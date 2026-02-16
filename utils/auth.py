"""Simple role and passcode handling for Teacher vs Student."""

from __future__ import annotations

import os
from typing import Literal

import streamlit as st

from utils.storage import load_server_config

Role = Literal["teacher", "student"]


def set_role_from_query() -> None:
    """Set role from query parameter if present."""
    params = st.query_params
    role_param = (params.get("role") or "").lower()
    if role_param in {"teacher", "student"}:
        st.session_state["role"] = role_param
        if role_param != "teacher":
            st.session_state["teacher_authed"] = False


def hide_default_sidebar_nav() -> None:
    """Hide Streamlit's default multipage sidebar navigation."""
    st.markdown(
        "<style>[data-testid='stSidebarNav'] {display: none !important;}</style>",
        unsafe_allow_html=True,
    )


def render_nav(role: Role) -> None:
    """Render minimal role-specific navigation."""
    hide_default_sidebar_nav()
    with st.sidebar:
        if role == "teacher":
            st.page_link("pages/2_Teacher.py", label="Teacher")
        else:
            st.page_link("pages/3_Student.py", label="Home")
            st.page_link("pages/4_Simulation.py", label="Simulation")
            st.page_link("pages/5_Evaluation.py", label="Evaluation")


def _get_passcode() -> str:
    try:
        server_config = load_server_config()
        if server_config.get("admin_password"):
            return server_config["admin_password"]
    except Exception:
        pass
    return "change-me"


def require_teacher() -> None:
    """Gate Teacher pages with role + passcode."""
    set_role_from_query()
    st.session_state.setdefault("teacher_authed", False)

    passcode = _get_passcode()
    if passcode == "change-me":
        st.warning("TEACHER_PASSCODE is not set. Change it in .env or Streamlit secrets.")

    if not st.session_state.get("teacher_authed"):
        with st.form("teacher_passcode_form"):
            entered = st.text_input("Enter teacher passcode", type="password")
            submitted = st.form_submit_button("Enter")
            if submitted:
                if entered == passcode:
                    st.session_state["teacher_authed"] = True
                    st.session_state["role"] = "teacher"
                    st.success("Authenticated as teacher.")
                    try:
                        st.rerun()
                    except AttributeError:  # Streamlit < 1.27 fallback
                        st.experimental_rerun()
                else:
                    st.error("Incorrect passcode.")
        st.stop()
