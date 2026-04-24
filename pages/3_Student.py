from __future__ import annotations

import random

import streamlit as st

# ── Inject design system CSS ──────────────────────────────────

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
:root {
    --bg:           #FBF7F0;
    --surface:      #F2EEE8;
    --text-primary: #3A3530;
    --text-muted:   #7A746D;
    --accent:       #C17F5A;
    --accent-hover: #A86845;
    --accent-light: #F0E0D2;
    --accent-blue:  #2D2660; 
    --accent-lightblue: #F2F0FB; 
    --border:       #E2DAD1;
    --radius-pill:  50px;
    --radius-card:  16px;
    --font-title:   'DM Serif Display', Georgia, serif;
    --font-body:    'Lato', system-ui, sans-serif;
}

/* ── Global ── */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
.main, .stApp {
    background-color: var(--bg) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ── Hide chrome ── */
[data-testid="stSidebar"],
[data-testid="collapsedControl"],
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton {
    display: none !important;
    height: 0 !important;
    visibility: hidden !important;
}

.block-container {
    padding: 52px 40px !important;
    max-width: 960px !important;
    margin: 0 auto !important;
}

/* ── Page header ── */
.cc-page-header {
    text-align: center;
    margin-bottom: 48px;
}

.cc-page-title {
    font-family: var(--font-title) !important;
    font-size: clamp(36px, 5vw, 54px) !important;
    font-weight: 400 !important;
    color: var(--text-primary) !important;
    line-height: 1.2 !important;
    margin: 0 0 12px 0 !important;
}

.cc-page-sub {
    font-family: var(--font-body);
    font-size: 16px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.7;
    margin: 0;
}

/* ── Cards ── */
.cc-card {
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-card);
    padding: 28px 32px;
    margin-bottom: 24px;
}

.cc-section-title {
    font-family: var(--font-title);
    font-size: 20px;
    font-weight: 400;
    color: var(--text-primary);
    margin: 0 0 16px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

/* ── Success chip (course loaded confirmation) ── */
.cc-chip {
    display: inline-block;
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 6px 16px;
    border-radius: var(--radius-pill);
}

.cc-chip.success {
    background-color: var(--accent-light);
    color: var(--accent);
    border: 1.5px solid var(--border);
}

/* ── Inputs ── */
[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(193, 127, 90, 0.12) !important;
    outline: none !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
}

[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(193, 127, 90, 0.12) !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
}

[data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
    font-size: 14px !important;
    color: var(--text-muted) !important;
}

/* Radio selected accent */
[data-testid="stRadio"] input:checked + div {
    color: var(--accent) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
}

/* ── Buttons — ghost outline (Back, Load Course) ── */
.stButton > button {
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    color: var(--text-muted) !important;
    background-color: transparent !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-pill) !important;
    padding: 10px 28px !important;
    transition: all 0.22s ease !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background-color: var(--accent-light) !important;
    box-shadow: none !important;
}
            
/* ── Back to Home Button  ── */
div[data-testid="stElementContainer"]:has(.back-btn-anchor) + div[data-testid="stElementContainer"] .stButton > button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    background-color: var(--accent-lightblue) !important;
}

/* Primary — filled terracotta (Start Simulation) */
.stButton > button[kind="primary"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    box-shadow: 0 4px 18px rgba(193, 127, 90, 0.22) !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--accent-hover) !important;
    border-color: var(--accent-hover) !important;
    box-shadow: 0 8px 28px rgba(168, 104, 69, 0.30) !important;
    transform: translateY(-2px) !important;
}

/* ── Fade-in ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

.cc-page-header { animation: fadeUp 0.6s ease both 0.08s; }
.cc-card        { animation: fadeUp 0.6s ease both 0.18s; }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────

from utils.auth import render_nav, set_role_from_query
from utils.storage import load_cases

st.set_page_config(
    page_title="...",
    initial_sidebar_state="collapsed"  
)

st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="cc-page-header">
  <p class="cc-page-title">Student setup</p>
  <p class="cc-page-sub">Join your course and choose a case to practise.</p>
</div>
""", unsafe_allow_html=True)

def _init_state() -> None:
    st.session_state.setdefault("student_course_data", {})
    st.session_state.setdefault("selected_case_id", "")


set_role_from_query()
_init_state()
render_nav("student")
st.query_params["role"] = "student"

st.markdown('<div class="cc-card"><p class="cc-section-title">Your details</p>', unsafe_allow_html=True)

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
        loaded_name = course_data.get("course_name", "Course")
        st.markdown(
            f'<div style="margin-top:8px;"><span class="cc-chip success">✓ &nbsp;{loaded_name} loaded</span></div>',
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

course_data = st.session_state.get("student_course_data")
if course_data:
    st.markdown('<div class="cc-card"><p class="cc-section-title">Select a case</p>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Load a course to view cases.")

st.markdown('<div class="back-btn-anchor"></div>', unsafe_allow_html=True)

if st.button("Back to Home"):
    try:
        st.switch_page("pages/1_Home.py")
    except Exception:
        pass