from __future__ import annotations

import streamlit as st

from utils.auth import render_nav, set_role_from_query
from utils.evaluator import compare_two_attempts, evaluate_conversation
from utils.pdf_export import generate_pdf_report
from utils.storage import load_cases, load_student_records, save_student_records

st.title("Evaluation & Reflection")
if st.button("⬅ Back"):
    try:
        st.switch_page("pages/3_Student.py")
    except Exception:
        st.info("Open Student page from sidebar.")

set_role_from_query()
render_nav("student")

attempt_id = st.session_state.get("active_attempt_id")
student_id = st.session_state.get("active_student_id")
course_code = st.session_state.get("active_course_code")

if not attempt_id or not student_id or not course_code:
    st.warning("No attempt selected. Finish a simulation first.")
    st.stop()

records = load_student_records()
attempts_for_student = [
    r for r in records if r.get("student_id") == student_id and r.get("course_code") == course_code
]
current_record = next((r for r in attempts_for_student if r.get("attempt_id") == attempt_id), None)
if not current_record:
    st.error("Could not find the attempt record.")
    st.stop()

cases = load_cases()
course_data = cases.get(course_code, {})
case = next(
    (c for c in course_data.get("cases", []) if c.get("case_id") == current_record.get("case_id")),
    {},
)

if not current_record.get("evaluation"):
    with st.spinner("Evaluating conversation..."):
        evaluation = evaluate_conversation(
            case,
            current_record.get("role_play_transcript", []),
            azure_config=st.session_state.get("azure_config"),
            reference_context=st.session_state.get("reference_context", ""),
        )
        current_record["evaluation"] = evaluation
        save_student_records(records)
else:
    evaluation = current_record["evaluation"]

st.subheader("Scores")
scores = evaluation.get("scores", {})
cols = st.columns(len(scores) or 1)
for col, (metric, value) in zip(cols, scores.items()):
    with col:
        st.metric(metric.title(), value)

st.subheader("Strengths")
for strength in evaluation.get("strengths", []):
    st.write(f"- {strength}")

st.subheader("Areas for Improvement")
for gap in evaluation.get("areas_for_improvement", []):
    st.write(f"- {gap}")

st.subheader("Detailed Feedback by Criterion")
criterion_feedback = evaluation.get("criterion_feedback", {}) or {}
for criterion, detail in criterion_feedback.items():
    score_display = detail.get("score", scores.get(criterion, ""))
    st.markdown(f"**{criterion.replace('_', ' ').title()}** — Score: {score_display}/5")
    explanation = detail.get("explanation", "")
    suggestions = detail.get("suggestions", "")
    if explanation:
        st.markdown(f"*Why:* {explanation}")
    if suggestions:
        st.markdown(f"*How to improve:* {suggestions}")

st.subheader("Overall Comment")
st.write(evaluation.get("overall_comment", ""))

st.markdown("**Suggested next practice prompt**")
st.info(evaluation.get("suggested_next_practice_prompt", ""))

if st.button("Return to Simulation"):
    try:
        st.switch_page("pages/4_Simulation.py")
    except Exception:
        st.info("Open the Simulation page from the sidebar.")

pdf_bytes = generate_pdf_report(
    student_name=student_id,
    student_id=student_id,
    course_code=course_code,
    case=case,
    evaluation=evaluation,
    transcript=current_record.get("role_play_transcript", []),
    attempt_id=attempt_id,
    timestamp=current_record.get("timestamp", ""),
)
st.download_button(
    "Download PDF Report",
    data=pdf_bytes,
    file_name=f"{attempt_id}_evaluation.pdf",
    mime="application/pdf",
)

st.markdown("---")
st.subheader("Past attempts")

if attempts_for_student:
    attempts_for_student_sorted = sorted(
        attempts_for_student,
        key=lambda r: r.get("timestamp", ""),
        reverse=True,
    )
    for record in attempts_for_student_sorted[:3]:
        st.write(f"{record['attempt_id']} – {record.get('timestamp')}")

    chronological_attempts = sorted(
        attempts_for_student_sorted,
        key=lambda r: r.get("timestamp", ""),
    )
    if len(chronological_attempts) >= 2:
        st.markdown("#### Compare two attempts")
        attempt_labels = [record["attempt_id"] for record in chronological_attempts]
        col_a, col_b = st.columns(2)
        with col_a:
            attempt_a = st.selectbox("Attempt A (earlier)", attempt_labels, key="compare_a")
        with col_b:
            attempt_b = st.selectbox("Attempt B (later)", attempt_labels, key="compare_b")
        if attempt_labels.index(attempt_a) >= attempt_labels.index(attempt_b):
            st.caption("Tip: choose an earlier attempt for A and later for B.")

        if st.button("Compare Attempts"):
            record_a = next((r for r in chronological_attempts if r["attempt_id"] == attempt_a), None)
            record_b = next((r for r in chronological_attempts if r["attempt_id"] == attempt_b), None)
            if not record_a or not record_b:
                st.error("Attempts not found.")
            else:
                comparison = compare_two_attempts(
                    case,
                    record_a.get("role_play_transcript", []),
                    record_b.get("role_play_transcript", []),
                    azure_config=st.session_state.get("azure_config"),
                )
                st.write("Summary of changes:")
                st.write(comparison.get("summary_of_changes", ""))
                st.write("Improvements:")
                for imp in comparison.get("improvements", []):
                    st.write(f"- {imp}")
                st.write("Remaining gaps:")
                for gap in comparison.get("remaining_gaps", []):
                    st.write(f"- {gap}")
                st.write("Coach message:")
                st.info(comparison.get("coach_message_to_trainee", ""))
else:
    st.info("No previous attempts logged yet.")

st.subheader("Conversation Transcript")
for turn in current_record.get("role_play_transcript", []):
    st.write(f"{turn.get('role', 'unknown').title()}: {turn.get('content', '')}")
