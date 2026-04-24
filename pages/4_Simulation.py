from __future__ import annotations

from datetime import datetime, timezone

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
    max-width: 860px !important;
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

/* ── Streamlit Native Containers -> CC Cards ── */
[data-testid="stVerticalBlockBorderWrapper"]:has(.cc-section-title) {
    background-color: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-card) !important;
    padding: 28px 32px !important;
    margin-bottom: 24px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stVerticalBlockBorderWrapper"]:not(:has(.cc-section-title)) {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
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

/* ── Case overview: tag pill ── */
.cc-tag {
    display: inline-block;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--accent-blue) !important;
    background: var(--accent-lightblue) !important;
    border: 1px solid var(--accent-blue) !important;
    border-radius: var(--radius-pill);
    padding: 4px 14px;
    margin-bottom: 10px;
}

/* ── Case name ── */
.cc-case-name {
    font-family: var(--font-title);
    font-size: 22px;
    font-weight: 400;
    color: var(--text-primary);
    margin: 6px 0 12px 0;
}

/* ── Case narrative / meta text ── */
.cc-case-meta {
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.75;
    margin: 0 0 4px 0;
}

.cc-case-meta strong {
    font-weight: 700;
    color: var(--text-primary);
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    border: none !important;
    padding: 8px 0 !important;
}

[data-testid="stChatMessage"] p {
    font-family: var(--font-body) !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}

/* Trainee / user bubble */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: var(--accent-light) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px 16px 4px 16px !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"] p {
    font-family: var(--font-body) !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}

/* Hide default avatar icons — keeps it clean */
[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    display: none !important;
}

/* ── Text area (user input) ── */
[data-testid="stTextArea"] div[data-baseweb="textarea"] {
    background-color: transparent !important;
    border: none !important;
}
[data-testid="stTextArea"] div[data-baseweb="textarea"]:focus-within {
    box-shadow: none !important;
    border: none !important;
    outline: none !important;
    background-color: transparent !important;
}
[data-testid="stTextArea"] textarea {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--accent-blue) !important; 
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 15px !important;
    line-height: 1.65 !important;
    padding: 14px 16px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(45, 38, 96, 0.12) !important; 
    outline: none !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background-color: var(--accent) !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--accent) !important;
    font-family: var(--font-body) !important;
    font-weight: 700 !important;
}

[data-testid="stSlider"] label {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-muted) !important;
}

/* ── Radio ── */
[data-testid="stRadio"] label {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 20px 0 !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
}

/* ── Buttons — ghost outline (Back, Restart, Cancel, No stay) ── */
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

/* Primary — filled terracotta (Send Reply, Finish & Reflect, Confirm Finish) */
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
            
/* ── Specific Button Overrides (Blue Primary & Blue Ghost) ── */
div[data-testid="stElementContainer"]:has(.blue-primary-anchor) + div[data-testid="stElementContainer"] .stButton > button {
    background-color: var(--accent-blue) !important;
    border-color: var(--accent-blue) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 18px rgba(45, 38, 96, 0.22) !important;
}
            
div[data-testid="stElementContainer"]:has(.blue-primary-anchor) + div[data-testid="stElementContainer"] .stButton > button:hover {
    background-color: #1F1A45 !important; 
    border-color: #1F1A45 !important;
    box-shadow: 0 8px 28px rgba(45, 38, 96, 0.30) !important;
    transform: translateY(-2px) !important;
}

div[data-testid="stElementContainer"]:has(.blue-ghost-anchor) + div[data-testid="stElementContainer"] .stButton > button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    background-color: var(--accent-lightblue) !important;
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
from utils.simulation_engine import generate_patient_reply
from utils.storage import load_student_records, save_student_records

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
  <p class="cc-page-title">Live simulation</p>
  <p class="cc-page-sub">Respond as the treating clinician. The AI plays the patient's family.</p>
</div>
""", unsafe_allow_html=True)

set_role_from_query()
render_nav("student")

case = st.session_state.get("simulation_case")
transcript = st.session_state.get("simulation_transcript", [])
student_id = st.session_state.get("active_student_id")
course_code = st.session_state.get("active_course_code")
conversation_start_mode = st.session_state.get("conversation_start_mode", "Parent-first")
tone_intensity = st.session_state.get("tone_intensity", 3)
last_tone_intensity = st.session_state.get("last_tone_intensity", tone_intensity)
reference_context = st.session_state.get("reference_context", "")
azure_config = st.session_state.get("azure_config")
st.session_state.setdefault("input_version", 0)

if transcript is None:
    transcript = []

if not case or not student_id or not course_code:
    st.warning("Start from the Student page to launch a simulation.")
    st.stop()

st.session_state.setdefault("pending_nav_action", None)
nav_col1, nav_col_spacer, nav_col2 = st.columns([1.5, 4, 1.5])
with nav_col1:
    if st.button("Back"):
        st.session_state["pending_nav_action"] = "back"
with nav_col2:
    if st.button("🔄 Restart", use_container_width=True):
        st.session_state["pending_nav_action"] = "restart"

pending_action = st.session_state.get("pending_nav_action")
if pending_action:
    st.warning("Going back or restarting will reset this simulation session. Are you sure?")
    confirm_col1, confirm_col2 = st.columns(2)
    with confirm_col1:
        st.markdown('<div class="blue-ghost-anchor"></div>', unsafe_allow_html=True)
        if st.button("Yes, continue", key="confirm_pending_action"):
            if pending_action == "back":
                for key in ["simulation_transcript", "simulation_input", "input_version", "last_tone_intensity", "pending_nav_action"]:
                    st.session_state.pop(key, None)
                try:
                    st.switch_page("pages/3_Student.py")
                except Exception:
                    st.info("Open Student page from sidebar.")
            else:
                opening_line = case.get("opening_line_for_patient") or (case.get("script_text", "").splitlines() or [""])[0]
                if st.session_state.get("conversation_start_mode", "Parent-first") == "Parent-first":
                    st.session_state["simulation_transcript"] = [{"role": "patient", "content": opening_line}]
                else:
                    st.session_state["simulation_transcript"] = []
                st.session_state["input_version"] = 0
                st.session_state.pop("pending_nav_action", None)
                st.rerun()
    with confirm_col2:
        st.markdown('<div class="blue-ghost-anchor"></div>', unsafe_allow_html=True)
        if st.button("No, stay", key="cancel_pending_action"):
            st.session_state.pop("pending_nav_action", None)
            st.rerun()
    st.stop()

# Case overview card
case_name = f"{case.get('patient_name', 'Patient')}, {case.get('age', '?')} yrs"
diagnosis = case.get("diagnosis", "")
tag = f"{case.get('age', '?')} yrs · {diagnosis[:40]}" if diagnosis else "Case"
current_description = st.session_state.get("current_case_description")
jacob_reference = (
    "Your patient is a 1-year-old diagnosed with Menkes Disease, a neurodegenerative disease with no cure. "
    "Most children don't live past age 2. Jacob has been hospitalized with RSV for the past 3 days requiring "
    "supplemental oxygen. He has a G-Tube for nutrition, hydration, and medication. He is fully dependent on "
    "his parents for care and has significant developmental delays. The parents are exhausted and scared, and "
    "they are unsure what to hope for. They want to know what this hospitalization means and what to expect next."
)
narrative = current_description or case.get("scenario_summary_for_trainee") or jacob_reference
goal = case.get("communication_goal_for_trainee", "Guide the family through this difficult conversation.")

st.markdown(f"""
<div class="cc-card">
  <p class="cc-section-title">Case overview</p>
  <span class="cc-tag">{tag}</span>
  <p class="cc-case-name">{case_name}</p>
  <div class="cc-case-meta">{narrative}</div>
  <hr style="border:none; border-top:0.5px solid #EEEBFB; margin:12px 0;">
  <p class="cc-case-meta"><strong>Your goal:</strong> {goal}</p>
</div>
""", unsafe_allow_html=True)

# Conversation settings card
with st.container(border=True):
    st.markdown('<p class="cc-section-title">Conversation settings</p>', unsafe_allow_html=True)
    start_choice = st.radio(
        "Conversation starts with",
        ["Parent-first", "Clinician-first"],
        index=0 if conversation_start_mode == "Parent-first" else 1,
    )
tone_intensity = 3  
if (start_choice != conversation_start_mode) and len(transcript) <= 1:
    if start_choice == "Parent-first":
        opening = generate_patient_reply(
            case,
            [],
            "The clinician is about to begin. Greet them naturally as the parent.",
            tone_intensity=tone_intensity,
            reference_context=reference_context,
            azure_config=azure_config,
        )
        st.session_state["simulation_transcript"] = [{"role": "patient", "content": opening}]
    else:
        st.session_state["simulation_transcript"] = []
    transcript = st.session_state["simulation_transcript"]
    st.session_state["conversation_start_mode"] = start_choice
    st.session_state["input_version"] += 1
else:
    st.session_state["conversation_start_mode"] = start_choice

# 3. Conversation card 
with st.container(border=True):
    st.markdown('<p class="cc-section-title">Conversation</p>', unsafe_allow_html=True)
    chat_container = st.container()
    with chat_container:
        for turn in transcript:
            role = turn.get("role", "trainee")
            content = turn.get("content", "")
            if role == "patient":
                st.chat_message("assistant").write(content)
            elif role == "trainee":
                st.chat_message("user").write(content)
            else:
                st.write(f"**{role.capitalize()}:** {content}")

st.markdown("---")
input_key = f"simulation_input_{st.session_state['input_version']}"
user_input = st.text_area("What would you say to the parent?", key=input_key)

if st.button("Send Reply"):
    if not user_input.strip():
        st.warning("Please write a reply before continuing.")
    else:
        updated_transcript = transcript + [{"role": "trainee", "content": user_input.strip()}]
        try:
            patient_reply = generate_patient_reply(
                case,
                updated_transcript,
                user_input,
                tone_intensity=tone_intensity,
                reference_context=reference_context,
                azure_config=azure_config,
            )
        except Exception as exc:
            st.warning("We had trouble generating the parent response. Please try again.")
        else:
            if (not patient_reply.strip()) or patient_reply.startswith("System not configured"):
                st.warning("System not configured. Please ask the instructor to set up the AI connection.")
            else:
                updated_transcript.append({"role": "patient", "content": patient_reply})
                st.session_state["simulation_transcript"] = updated_transcript
                current_turns = sum(1 for t in updated_transcript if t.get("role") == "trainee")
                max_limit = 12
            if current_turns >= max_limit:
        
                st.session_state["auto_finish_triggered"] = True
            st.session_state["input_version"] += 1
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()


def _persist_attempt() -> str:
    transcript_snapshot = st.session_state.get("simulation_transcript", [])
    records = load_student_records()
    case_id = case.get("case_id")
    existing_attempts = [
        r for r in records if r.get("student_id") == student_id and r.get("case_id") == case_id
    ]
    next_number = len(existing_attempts) + 1
    attempt_id = f"{case_id}-{student_id}-{next_number}"
    record = {
        "student_id": student_id,
        "course_code": course_code,
        "case_id": case_id,
        "attempt_id": attempt_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role_play_transcript": transcript_snapshot,
    }
    records.append(record)
    save_student_records(records)
    return attempt_id

# ==========================================
if st.session_state.get("auto_finish_triggered"):
    st.info("You have reached the limit for this simulation. Are you ready to end the simulation and view feedback?")
    auto_col1, auto_col2 = st.columns(2)
    
    with auto_col1:
        st.markdown('<div class="blue-primary-anchor"></div>', unsafe_allow_html=True)
        if st.button("Yes, view feedback", key="auto_finish_yes", type="primary"):
            attempt_id = _persist_attempt()
            st.session_state["active_attempt_id"] = attempt_id
            st.session_state["auto_finish_triggered"] = False
            st.success("Simulation saved. Proceeding to reflection…")
            try:
                st.switch_page("pages/5_Evaluation.py")
            except Exception:
                st.info("Open the Evaluation page from the sidebar.")
                
    with auto_col2:
        st.markdown('<div class="blue-ghost-anchor"></div>', unsafe_allow_html=True)
        if st.button("No, let me review", key="auto_finish_no"):
            st.session_state["auto_finish_triggered"] = False
            st.rerun()

st.session_state.setdefault("pending_finish_confirmation", False)
if st.button("Finish & Reflect", type="primary"):
    st.session_state["pending_finish_confirmation"] = True

if st.session_state.get("pending_finish_confirmation"):
    st.info("Are you ready to end the simulation and view feedback?")
    finish_col1, finish_col2 = st.columns(2)
    with finish_col1:
        st.markdown('<div class="blue-primary-anchor"></div>', unsafe_allow_html=True)
        if st.button("Confirm Finish", type="primary"):
            attempt_id = _persist_attempt()
            st.session_state["active_attempt_id"] = attempt_id
            st.session_state["pending_finish_confirmation"] = False
            st.success("Simulation saved. Proceeding to reflection…")
            try:
                st.switch_page("pages/5_Evaluation.py")
            except Exception:
                st.info("Open the Evaluation page from the sidebar.")
    with finish_col2:
        st.markdown('<div class="blue-ghost-anchor"></div>', unsafe_allow_html=True)
        if st.button("Cancel"):
            st.session_state["pending_finish_confirmation"] = False