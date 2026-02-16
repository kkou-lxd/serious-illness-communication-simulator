from __future__ import annotations

import random

import streamlit as st

from utils.auth import render_nav, set_role_from_query
from utils.storage import load_cases, load_server_config

st.title("Student Home")
st.write("Join your course, pick a scenario, and start the simulation.")
if st.button("⬅ Back to Home"):
    try:
        st.switch_page("pages/1_Home.py")
    except Exception:
        st.info("Open Home from the sidebar.")


def _init_state() -> None:
    st.session_state.setdefault("student_course_data", {})
    st.session_state.setdefault("selected_case_id", "")


set_role_from_query()
_init_state()
render_nav("student")
st.query_params["role"] = "student"

student_id = st.text_input("Student name or ID", st.session_state.get("student_id", ""))
if student_id:
    st.session_state["student_id"] = student_id
course_code = st.text_input("Course code", st.session_state.get("student_course_code", ""))
if course_code:
    st.session_state["student_course_code"] = course_code

if st.button("Load Course"):
    all_courses = load_cases()
    course_data = all_courses.get(course_code)
    if not course_data:
        st.error("Course code not found.")
    else:
        st.session_state["student_course_data"] = course_data
        server_config = load_server_config()
        st.session_state["azure_config"] = {
            "azure_api_key": server_config.get("azure_api_key"),
            "azure_endpoint": server_config.get("azure_endpoint"),
            "azure_deployment": server_config.get("azure_deployment"),
            "azure_api_version": server_config.get("azure_api_version"),
        }
        st.success(f"Loaded {course_data.get('course_name', 'Course')}")

course_data = st.session_state.get("student_course_data")
if course_data:
    st.subheader("Select a case")
    cases = course_data.get("cases", []) + course_data.get("base_cases", [])
    selection_mode = st.radio("Case selection mode", ["Use a specific case", "Random scenario"])
    chosen_case = None
    if selection_mode == "Use a specific case":
        labels = [f"{c['case_id']}: {c['patient_name']}" for c in cases]
        if labels:
            selected_label = st.selectbox("Choose case", labels)
            idx = labels.index(selected_label)
            chosen_case = cases[idx]
    else:
        if cases:
            chosen_case = random.choice(cases)
            st.info(f"Random case selected: {chosen_case['patient_name']} ({chosen_case['case_id']})")

    if st.button("Start Simulation", type="primary"):
        if not student_id or not course_code:
            st.error("Enter student ID and course code first.")
        elif not chosen_case:
            st.error("No case available.")
        else:
            script_text = chosen_case.get("script_text", "")
            opening_line = chosen_case.get("opening_line_for_patient", "")
            if not opening_line and script_text:
                opening_line = script_text.strip().splitlines()[0]
            st.session_state["simulation_case"] = chosen_case
            st.session_state["simulation_transcript"] = [
                {"role": "patient", "content": opening_line}
            ]
            st.session_state["current_case_description"] = (
                chosen_case.get("detailed_case_description")
                or chosen_case.get("scenario_summary_for_trainee")
                or chosen_case.get("script_text")
                or ""
            )
            st.session_state["active_course_code"] = course_code
            st.session_state["active_student_id"] = student_id
            st.session_state["active_case_id"] = chosen_case.get("case_id")
            st.session_state["active_attempt_id"] = None
            st.session_state["conversation_start_mode"] = "Parent-first"
            st.session_state["tone_intensity"] = 3
            st.session_state["reference_context"] = st.session_state.get("student_course_data", {}).get("reference_context", "")
            try:
                st.switch_page("pages/4_Simulation.py")
            except Exception:
                st.info("Open the Simulation page from the sidebar.")
else:
    st.info("Load a course to view cases.")
