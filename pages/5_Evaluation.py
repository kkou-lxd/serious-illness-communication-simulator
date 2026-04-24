from __future__ import annotations

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
    --blue-light:   #EFF6FF;
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
    max-width: 900px !important;
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
    line-height: 1.15 !important;
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

/* ── Score banner ── */
.cc-score-banner {
    display: flex;
    align-items: center;
    gap: 24px;
    background: var(--surface);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-card);
    padding: 28px 32px;
    margin-bottom: 24px;
}

.cc-score-ring-wrap {
    flex-shrink: 0;
}

.cc-score-banner-right {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* ── Level pill ── */
.cc-level-pill {
    display: inline-block;
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding: 4px 16px;
    border-radius: var(--radius-pill);
    width: fit-content;
    background: transparent;
    color: var(--accent);
    border: 1.5px solid var(--accent-light);
}

.cc-level-pill.developing {
    background: transparent;
    color: var(--accent);
    border-color: var(--accent-light);
}

.cc-level-pill.advanced {
    background: var(--accent-light);
    color: var(--accent-hover);
    border-color: var(--accent);
}

.cc-overall-comment {
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.7;
    margin: 0;
}

/* ── Score dimension mini-cards ── */
/* (nested .cc-card inside grid — inherits base card styles) */

/* ── Strengths / improvements list ── */
.cc-list-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.65;
    margin-bottom: 10px;
}

.cc-list-dot {
    flex-shrink: 0;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 6px;
}

.cc-list-dot.blue   { background-color: #16537E; }
.cc-list-dot.amber  { background-color: #E9A84C; }

/* ── Criterion feedback blocks ── */
.cc-criterion-block {
    padding: 18px 0;
    border-bottom: 1px solid var(--border);
}

.cc-criterion-block:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.cc-criterion-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
    flex-wrap: wrap;
}

.cc-criterion-name {
    font-family: var(--font-title);
    font-size: 17px;
    font-weight: 400;
    color: var(--text-primary);
    flex: 1;
}

.cc-criterion-pips {
    display: flex;
    gap: 5px;
}

.cc-pip {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: var(--border);
    transition: background-color 0.2s ease;
}

.cc-pip.on {
    background-color: var(--accent);
}

.cc-criterion-score-pill {
    font-family: var(--font-body);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--accent);
    background: var(--accent-light);
    border: 1px solid var(--border);
    border-radius: var(--radius-pill);
    padding: 3px 12px;
}

.cc-criterion-explanation {
    font-family: var(--font-body);
    font-size: 14px;
    font-weight: 300;
    color: var(--text-muted);
    line-height: 1.7;
    margin: 0 0 8px 0;
}

.cc-criterion-suggestion {
    font-family: var(--font-body);
    font-size: 13px;
    font-weight: 400;
    color: var(--text-primary);
    background: var(--bg);
    border-left: 3px solid var(--accent);
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    line-height: 1.65;
}

/* ── Tip box ── */
.cc-tip-box {
    background: var(--accent-light);
    border: 1.5px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: var(--radius-card);
    padding: 22px 28px;
    margin-bottom: 24px;
}

.cc-tip-label {
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 8px 0;
}

.cc-tip-text {
    font-family: var(--font-body);
    font-size: 15px;
    font-weight: 300;
    color: var(--text-primary);
    line-height: 1.75;
    margin: 0;
}

/* ── Chat bubbles (transcript replay) ── */
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px 16px 16px 4px !important;
    padding: 14px 18px !important;
    margin-bottom: 12px !important;
}

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

[data-testid="chatAvatarIcon-assistant"],
[data-testid="chatAvatarIcon-user"] {
    display: none !important;
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

/* ── Markdown headers (#### Compare two attempts) ── */
.stMarkdown h4 {
    font-family: var(--font-title) !important;
    font-size: 18px !important;
    font-weight: 400 !important;
    color: var(--text-primary) !important;
    margin: 24px 0 12px 0 !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
}

/* ── Buttons — ghost outline ── */
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
}

/* Primary — filled terracotta */
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

/* Download button — matches ghost style */
[data-testid="stDownloadButton"] > button {
    font-family: var(--font-body) !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    color: var(--accent) !important;
    background-color: var(--accent-light) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-pill) !important;
    padding: 10px 28px !important;
    transition: all 0.22s ease !important;
}

[data-testid="stDownloadButton"] > button:hover {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #FFFFFF !important;
}

/* ── Fade-in ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

.cc-page-header    { animation: fadeUp 0.6s ease both 0.08s; }
.cc-score-banner   { animation: fadeUp 0.6s ease both 0.14s; }
.cc-card           { animation: fadeUp 0.6s ease both 0.20s; }
.cc-tip-box        { animation: fadeUp 0.6s ease both 0.26s; }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────

from utils.auth import render_nav, set_role_from_query
from utils.evaluator import compare_two_attempts, evaluate_conversation
from utils.pdf_export import generate_pdf_report
from utils.storage import load_cases, load_student_records, save_student_records

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
  <p class="cc-page-title">Evaluation &amp; reflection</p>
  <p class="cc-page-sub">Review your performance and feedback for this attempt.</p>
</div>
""", unsafe_allow_html=True)

if st.button("Back"):
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

# Overall score banner
scores = evaluation.get("scores", {})
overall_avg = round(sum(scores.values()) / len(scores), 1) if scores else 0.0
level = evaluation.get("level", "Developing")
overall_comment = evaluation.get("overall_comment", "")
filled = round(175.93 * (overall_avg / 5))
offset = round(175.93 - filled)
level_class = {
    "Beginning": "developing",
    "Developing": "developing",
    "Proficient": "",
    "Advanced": "advanced",
}.get(level, "")

st.markdown(f"""
<div class="cc-score-banner">
  <div class="cc-score-ring-wrap">
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r="28" fill="none" stroke="var(--border)" stroke-width="6"/>
      <circle cx="36" cy="36" r="28" fill="none" stroke="var(--accent)" stroke-width="6"
        stroke-dasharray="175.93" stroke-dashoffset="{offset}"
        stroke-linecap="round" transform="rotate(-90 36 36)"/>
      <text x="36" y="33" text-anchor="middle"
        font-family="DM Serif Display, serif" font-size="18" fill="var(--accent-blue)">{overall_avg}</text>
      <text x="36" y="45" text-anchor="middle"
        font-family="DM Sans, sans-serif" font-size="9" fill="var(--text-muted)">/ 5</text>
    </svg>
  </div>
  <div class="cc-score-banner-right">
    <span class="cc-level-pill {level_class}">{level}</span>
    <p class="cc-overall-comment">{overall_comment}</p>
  </div>
</div>
""", unsafe_allow_html=True)

# Scores grid
scores_html = '<div class="cc-card"><p class="cc-section-title">Scores by dimension</p><div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20px 16px;">'

for name, value in scores.items():
    pct = int((value / 5) * 100)
    label = name.replace("_", " ").title()
    scores_html += f"""
    <div style="padding: 4px 0;">
      <p style="font-family:var(--font-title); font-size:16px; margin:0 0 6px 0; color:var(--text-primary);">{label}</p>
      <div style="display:flex; align-items:baseline; gap:4px;">
        <span style="font-family:'DM Serif Display',serif; font-size:24px; color:var(--accent); line-height:1;">{value}</span>
        <span style="font-size:13px; color:var(--text-muted);">/ 5</span>
      </div>
      <div style="height:6px; background:var(--accent-lightblue); border-radius:3px; margin-top:8px; overflow:hidden;">
        <div style="height:100%; width:{pct}%; background:var(--accent); border-radius:3px;"></div>
      </div>
    </div>"""

scores_html += '</div></div>'
st.markdown(scores_html, unsafe_allow_html=True)

# Strengths and areas for improvement
s_items = "".join(
    f'<div class="cc-list-item"><div class="cc-list-dot green"></div>{s}</div>'
    for s in evaluation.get("strengths", [])
)
a_items = "".join(
    f'<div class="cc-list-item"><div class="cc-list-dot amber"></div>{a}</div>'
    for a in evaluation.get("areas_for_improvement", [])
)
st.markdown(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:14px; margin-bottom:14px;">
  <div class="cc-card" style="margin-bottom:0;">
    <p class="cc-section-title">Strengths</p>
    {s_items}
  </div>
  <div class="cc-card" style="margin-bottom:0;">
    <p class="cc-section-title">Areas for improvement</p>
    {a_items}
  </div>
</div>
""", unsafe_allow_html=True)

# Detailed criterion feedback
criterion_feedback = evaluation.get("criterion_feedback", {}) or {}
blocks = ""
for criterion, detail in criterion_feedback.items():
    score = detail.get("score", 0)
    explanation = detail.get("explanation", "")
    suggestions = detail.get("suggestions", "")
    label = criterion.replace("_", " ").title()
    pips = "".join(
        f'<span class="cc-pip {"on" if i < score else ""}"></span>'
        for i in range(5)
    )
    blocks += f"""
<div class="cc-criterion-block">
  <div class="cc-criterion-header">
    <span class="cc-criterion-name">{label}</span>
    <div class="cc-criterion-pips">{pips}</div>
    <span class="cc-criterion-score-pill">{score} / 5</span>
  </div>
  <p class="cc-criterion-explanation">{explanation}</p>
  <div class="cc-criterion-suggestion">{suggestions}</div>
</div>"""

st.markdown(f"""
<div class="cc-card">
  <p class="cc-section-title">Detailed feedback by criterion</p>
  {blocks}
</div>
""", unsafe_allow_html=True)

# Suggested next practice prompt
next_prompt = evaluation.get("suggested_next_practice_prompt", "")
st.markdown(f"""
<div class="cc-tip-box">
  <p class="cc-tip-label">Suggested next practice focus</p>
  <p class="cc-tip-text">{next_prompt}</p>
</div>
""", unsafe_allow_html=True)

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


# Past attempts
attempts_for_student_sorted = sorted(
    attempts_for_student,
    key=lambda r: r.get("timestamp", ""),
    reverse=True,
)

if attempts_for_student:
    st.markdown('<div class="cc-card"><p class="cc-section-title">Past attempts</p>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No previous attempts logged yet.")

# Transcript
st.markdown('<div class="cc-card"><p class="cc-section-title">Conversation transcript</p>', unsafe_allow_html=True)
for turn in current_record.get("role_play_transcript", []):
    role = turn.get("role", "unknown")
    content = turn.get("content", "")
    if role == "patient":
        st.chat_message("assistant").write(content)
    elif role == "trainee":
        st.chat_message("user").write(content)
    else:
        st.write(f"**{role.capitalize()}:** {content}")
st.markdown('</div>', unsafe_allow_html=True)
