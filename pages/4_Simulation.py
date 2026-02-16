from __future__ import annotations

from datetime import datetime, timezone

import streamlit as st

from utils.auth import render_nav, set_role_from_query
from utils.simulation_engine import generate_patient_reply
from utils.storage import load_student_records, save_student_records

st.title("Live Simulation")

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
nav_col1, nav_col2 = st.columns(2)
with nav_col1:
    if st.button("⬅ Back"):
        st.session_state["pending_nav_action"] = "back"
with nav_col2:
    if st.button("🔄 Restart"):
        st.session_state["pending_nav_action"] = "restart"

pending_action = st.session_state.get("pending_nav_action")
if pending_action:
    st.warning("Going back or restarting will reset this simulation session. Are you sure?")
    confirm_col1, confirm_col2 = st.columns(2)
    with confirm_col1:
        if st.button("Yes, continue", key="confirm_pending_action"):
            if pending_action == "back":
                for key in [
                    "simulation_transcript",
                    "simulation_input",
                    "input_version",
                    "last_tone_intensity",
                    "pending_nav_action",
                ]:
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
        if st.button("No, stay", key="cancel_pending_action"):
            st.session_state.pop("pending_nav_action", None)
            st.rerun()
    st.stop()

st.subheader("Case overview")

def _build_background(case_dict: dict) -> str:
    parts = []
    parts.append(
        f"Patient: {case_dict.get('patient_name', 'Unknown')} ({case_dict.get('age', '?')} yrs, {case_dict.get('gender', '?')})"
    )
    parts.append(f"Diagnosis & prognosis: {case_dict.get('diagnosis', 'Unknown')} ; prognosis: {case_dict.get('prognosis', 'N/A')}")
    parts.append(f"Parent emotional state & concerns: {case_dict.get('emotional_state', 'N/A')}")
    parts.append(f"Family context: {case_dict.get('family_context', 'N/A')}")
    parts.append(f"Communication goal for clinician: {case_dict.get('communication_goal_for_trainee', 'N/A')}")
    if case_dict.get("key_constraints_for_patient"):
        parts.append(f"Key constraints: {', '.join(case_dict.get('key_constraints_for_patient', []))}")
    if case_dict.get("scenario_summary_for_teacher"):
        parts.append(f"Clinical background: {case_dict.get('scenario_summary_for_teacher')}")
    return "\n".join(parts)

jacob_reference = (
    "Your patient is a 1-year-old diagnosed with Menkes Disease, a neurodegenerative disease with no cure. "
    "Most children don't live past age 2. Jacob has been hospitalized with RSV for the past 3 days requiring "
    "supplemental oxygen. He has a G-Tube for nutrition, hydration, and medication. He is fully dependent on "
    "his parents for care and has significant developmental delays. The parents are exhausted and scared, and "
    "they are unsure what to hope for. They want to know what this hospitalization means and what to expect next."
)
current_description = st.session_state.get("current_case_description")
if ("jacob" in str(case.get("patient_name", "")).lower()) or current_description or case.get("scenario_summary_for_trainee"):
    narrative = current_description or case.get("scenario_summary_for_trainee") or jacob_reference
    st.markdown("**Scenario Background**")
    st.markdown(f"<div class='case-summary'>{narrative}</div>", unsafe_allow_html=True)
else:
    st.markdown("**Scenario Background**")
    st.code(_build_background(case), language="text")

st.markdown("### Conversation Settings")
col_start, col_tone = st.columns(2)
with col_start:
    start_choice = st.radio(
        "Conversation starts with",
        ["Parent-first", "Clinician-first"],
        index=0 if conversation_start_mode == "Parent-first" else 1,
    )
with col_tone:
    tone_intensity = st.slider("Parent emotional intensity", 1, 5, value=int(tone_intensity))
    st.session_state["tone_intensity"] = tone_intensity

# Refresh opening and header when tone or starter changes at start of conversation
if (tone_intensity != last_tone_intensity or start_choice != conversation_start_mode) and len(transcript) <= 1:
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
st.session_state["last_tone_intensity"] = tone_intensity

st.markdown("### Conversation")
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
            st.session_state["input_version"] += 1
            try:
                st.rerun()
            except AttributeError:  # Streamlit < 1.27 fallback
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


st.session_state.setdefault("pending_finish_confirmation", False)
if st.button("Finish & Reflect", type="primary"):
    st.session_state["pending_finish_confirmation"] = True

if st.session_state.get("pending_finish_confirmation"):
    st.info("Are you ready to end the simulation and view feedback?")
    finish_col1, finish_col2 = st.columns(2)
    with finish_col1:
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
        if st.button("Cancel"):
            st.session_state["pending_finish_confirmation"] = False
