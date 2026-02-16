from __future__ import annotations

import streamlit as st

st.title("Who is using the simulator today?")
st.write("Choose the role that matches how you plan to use the app.")
if st.button("⬅ Back"):
    try:
        st.switch_page("app.py")
    except Exception:
        pass


def _go_to(page_path: str) -> None:
    try:
        st.switch_page(page_path)
    except Exception:
        st.info("Use the sidebar to open the selected page.")


col1, col2 = st.columns(2)
with col1:
    if st.button("I am a Teacher", use_container_width=True):
        st.session_state["role"] = "teacher"
        _go_to("pages/2_Teacher.py")

with col2:
    if st.button("I am a Student", use_container_width=True):
        st.session_state["role"] = "student"
        _go_to("pages/3_Student.py")
