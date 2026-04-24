"""
ClinComm HTML Snippets
======================
Paste these st.markdown() calls into the corresponding Streamlit page files.
Each snippet replaces or supplements the existing st.title() / st.write() calls
at the top of each page. No backend logic is touched.

HOW TO USE
----------
1. Copy assets/styles.css → replace your existing assets/styles.css
   (app.py already loads it via _inject_styles(), nothing else needed there)

2. In each page file, REPLACE the existing st.title() and st.write() lines
   with the snippet for that page (marked clearly below).

3. Keep ALL other code (session state, API calls, logic) exactly as-is.
"""

# =============================================================
# pages/1_Home.py
# REPLACE:
#   st.title("Who is using the simulator today?")
#   st.write("Choose the role that matches how you plan to use the app.")
# WITH:
# =============================================================

HOME_HEADER = """
<div class="cc-page-header">
  <p class="cc-page-title">Serious Illness Communication Simulator</p>
  <p class="cc-page-sub">An AI-powered role-play environment for medical trainees.</p>
</div>

<div class="cc-role-cards">
  <div class="cc-role-card">
    <div class="cc-role-icon teacher">🎓</div>
    <p class="cc-role-title">I am a teacher</p>
    <p class="cc-role-desc">Set up courses, configure cases, and review student session records.</p>
    <p class="cc-role-cta">Go to teacher panel →</p>
  </div>
  <div class="cc-role-card">
    <div class="cc-role-icon student">💬</div>
    <p class="cc-role-title">I am a student</p>
    <p class="cc-role-desc">Enter your course, select a case, and start a live simulation.</p>
    <p class="cc-role-cta student">Start a simulation →</p>
  </div>
</div>

<div class="cc-feature-row">
  <span class="cc-feature-chip">AI-generated patient responses</span>
  <span class="cc-feature-chip">Structured rubric evaluation</span>
  <span class="cc-feature-chip">PDF report export</span>
</div>
"""

# Usage in pages/1_Home.py:
#
#   st.markdown(HOME_HEADER, unsafe_allow_html=True)
#
#   # Keep the existing button logic below:
#   col1, col2 = st.columns(2)
#   with col1:
#       if st.button("I am a Teacher", use_container_width=True):
#           ...
#   with col2:
#       if st.button("I am a Student", use_container_width=True):
#           ...
#
# NOTE: The role cards above are decorative. The actual navigation still
# happens via Streamlit buttons below — keep those exactly as they are.


# =============================================================
# pages/2_Teacher.py
# REPLACE:
#   st.title("Teacher Panel")
#   st.write("Create or update a course with randomized scenarios.")
# WITH:
# =============================================================

TEACHER_HEADER = """
<div class="cc-page-header">
  <p class="cc-page-title">Teacher panel</p>
  <p class="cc-page-sub">Create and configure courses for your students.</p>
</div>
"""

# Usage in pages/2_Teacher.py:
#
#   st.markdown(TEACHER_HEADER, unsafe_allow_html=True)
#
# Then wrap the course name input in a card:

TEACHER_COURSE_SETUP_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Course setup</p>
"""

TEACHER_COURSE_SETUP_CLOSE = """
</div>
"""

# Usage pattern for Teacher cards:
#
#   st.markdown(TEACHER_COURSE_SETUP_OPEN, unsafe_allow_html=True)
#   course_name = st.text_input("Course name", ...)
#   st.markdown(TEACHER_COURSE_SETUP_CLOSE, unsafe_allow_html=True)
#
#   # Then the two-column section (case library + references):
#   st.markdown(TEACHER_CASE_REF_OPEN, unsafe_allow_html=True)
#   case_col, ref_col = st.columns(2)
#   ...
#   st.markdown(TEACHER_CASE_REF_CLOSE, unsafe_allow_html=True)

TEACHER_CASE_REF_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Case library &amp; reference materials</p>
"""

TEACHER_CASE_REF_CLOSE = """
</div>
"""

TEACHER_GENERATED_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Generated cases</p>
"""

TEACHER_GENERATED_CLOSE = """
</div>
"""

# After saving, replace st.info(course_code) with:
def teacher_course_code_html(course_code: str) -> str:
    return f"""
<div class="cc-card">
  <p class="cc-section-title">Active course code</p>
  <div class="cc-code-box">
    <div>
      <p class="cc-code-label">Share with students</p>
      <p class="cc-code-value">{course_code}</p>
    </div>
  </div>
</div>
"""

TEACHER_PROGRESS_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Student progress</p>
"""

TEACHER_PROGRESS_CLOSE = """
</div>
"""


# =============================================================
# pages/3_Student.py
# REPLACE:
#   st.title("Student Home")
#   st.write("Join your course, pick a scenario, and start the simulation.")
# WITH:
# =============================================================

STUDENT_HEADER = """
<div class="cc-page-header">
  <p class="cc-page-title">Student setup</p>
  <p class="cc-page-sub">Join your course and choose a case to practise.</p>
</div>
"""

STUDENT_DETAILS_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Your details</p>
"""

STUDENT_DETAILS_CLOSE = """
</div>
"""

STUDENT_CASE_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Select a case</p>
"""

STUDENT_CASE_CLOSE = """
</div>
"""

# Success chip after loading course — replace st.success(...) with:
def student_course_loaded_html(course_name: str) -> str:
    return f"""
<div style="margin-top: 8px;">
  <span class="cc-chip success">✓ &nbsp;{course_name} loaded</span>
</div>
"""

# Usage in pages/3_Student.py:
#
#   st.markdown(STUDENT_HEADER, unsafe_allow_html=True)
#
#   st.markdown(STUDENT_DETAILS_OPEN, unsafe_allow_html=True)
#   student_id = st.text_input("Student name or ID", ...)
#   course_code = st.text_input("Course code", ...)
#   if st.button("Load Course"):
#       ...
#       st.markdown(student_course_loaded_html(course_data["course_name"]),
#                   unsafe_allow_html=True)
#   st.markdown(STUDENT_DETAILS_CLOSE, unsafe_allow_html=True)
#
#   if course_data:
#       st.markdown(STUDENT_CASE_OPEN, unsafe_allow_html=True)
#       # existing case selection radio + selectbox + Start button
#       st.markdown(STUDENT_CASE_CLOSE, unsafe_allow_html=True)


# =============================================================
# pages/4_Simulation.py
# REPLACE:
#   st.title("Live Simulation")
# WITH:
# =============================================================

SIMULATION_HEADER = """
<div class="cc-page-header">
  <p class="cc-page-title">Live simulation</p>
  <p class="cc-page-sub">Respond as the treating clinician. The AI plays the patient's family.</p>
</div>
"""

# Case overview card — replace the existing st.subheader("Case overview") block
# and the narrative/background section with:
def simulation_case_card_html(
    tag: str,
    case_name: str,
    diagnosis: str,
    situation: str,
    goal: str,
) -> str:
    return f"""
<div class="cc-card">
  <p class="cc-section-title">Case overview</p>
  <span class="cc-tag">{tag}</span>
  <p class="cc-case-name">{case_name}</p>
  <div class="cc-case-meta">
    <strong>Diagnosis:</strong> {diagnosis}<br>
    <strong>Situation:</strong> {situation}<br>
    <strong>Your goal:</strong> {goal}
  </div>
</div>
"""

# Settings card wrapper — wrap st.markdown("### Conversation Settings") + columns:
SIMULATION_SETTINGS_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Conversation settings</p>
"""

SIMULATION_SETTINGS_CLOSE = """
</div>
"""

# Conversation card wrapper — wrap the chat container + input + buttons:
SIMULATION_CHAT_OPEN = """
<div class="cc-card">
  <p class="cc-section-title">Conversation</p>
"""

SIMULATION_CHAT_CLOSE = """
</div>
"""

# Usage in pages/4_Simulation.py:
#
#   st.markdown(SIMULATION_HEADER, unsafe_allow_html=True)
#
#   # Build tag / case fields from session state:
#   case = st.session_state.get("simulation_case", {})
#   tag = f"{case.get('age', '?')} yrs · {case.get('diagnosis', '')[:30]}"
#   st.markdown(simulation_case_card_html(
#       tag=tag,
#       case_name=f"{case.get('patient_name', 'Patient')}, {case.get('age', '?')} yrs",
#       diagnosis=case.get('diagnosis', ''),
#       situation=case.get('scenario_summary_for_trainee', '')[:160] + '…',
#       goal=case.get('communication_goal_for_trainee', ''),
#   ), unsafe_allow_html=True)
#
#   st.markdown(SIMULATION_SETTINGS_OPEN, unsafe_allow_html=True)
#   col_start, col_tone = st.columns(2)
#   ... existing widgets ...
#   st.markdown(SIMULATION_SETTINGS_CLOSE, unsafe_allow_html=True)
#
#   st.markdown(SIMULATION_CHAT_OPEN, unsafe_allow_html=True)
#   ... existing chat container, input, buttons ...
#   st.markdown(SIMULATION_CHAT_CLOSE, unsafe_allow_html=True)


# =============================================================
# pages/5_Evaluation.py
# REPLACE:
#   st.title("Evaluation & Reflection")
# WITH:
# =============================================================

EVALUATION_HEADER = """
<div class="cc-page-header">
  <p class="cc-page-title">Evaluation &amp; reflection</p>
  <p class="cc-page-sub">Review your performance and feedback for this attempt.</p>
</div>
"""

# Overall score banner — replace st.subheader("Scores") + st.columns metrics:
def evaluation_score_banner_html(
    overall: float,
    level: str,
    overall_comment: str,
) -> str:
    # ring: circumference of r=28 circle = 175.93
    # fill proportion = overall/5
    filled = round(175.93 * (overall / 5))
    offset = round(175.93 - filled)
    level_class = {
        "Beginning": "developing",
        "Developing": "developing",
        "Proficient": "",
        "Advanced": "advanced",
    }.get(level, "")
    return f"""
<div class="cc-score-banner">
  <div class="cc-score-ring-wrap">
    <svg width="72" height="72" viewBox="0 0 72 72">
      <circle cx="36" cy="36" r="28" fill="none" stroke="#EDE9FB" stroke-width="6"/>
      <circle cx="36" cy="36" r="28" fill="none" stroke="#5B50D8" stroke-width="6"
        stroke-dasharray="175.93" stroke-dashoffset="{offset}"
        stroke-linecap="round" transform="rotate(-90 36 36)"/>
      <text x="36" y="33" text-anchor="middle"
        font-family="DM Serif Display, serif" font-size="18" fill="#2D2660">{overall}</text>
      <text x="36" y="45" text-anchor="middle"
        font-family="DM Sans, sans-serif" font-size="9" fill="#A09BC4">/ 5</text>
    </svg>
  </div>
  <div class="cc-score-banner-right">
    <span class="cc-level-pill {level_class}">{level}</span>
    <p class="cc-overall-comment">{overall_comment}</p>
  </div>
</div>
"""

# Scores grid — replace st.subheader("Scores") + metric columns with:
def evaluation_scores_grid_html(scores: dict) -> str:
    cells = ""
    for name, value in scores.items():
        pct = int((value / 5) * 100)
        label = name.replace("_", " ").title()
        cells += f"""
    <div class="cc-card" style="margin-bottom:0; padding: 12px 14px;">
      <p class="cc-section-title" style="margin-bottom:6px;">{label}</p>
      <div style="display:flex; align-items:baseline; gap:3px;">
        <span style="font-family:'DM Serif Display',serif; font-size:22px;
          color:#2D2660; line-height:1;">{value}</span>
        <span style="font-size:12px; color:#B0ABDA;">/ 5</span>
      </div>
      <div style="height:4px; background:#E0DCF0; border-radius:2px;
        margin-top:8px; overflow:hidden;">
        <div style="height:100%; width:{pct}%; background:#7B6FE8;
          border-radius:2px;"></div>
      </div>
    </div>"""
    return f"""
<div class="cc-card">
  <p class="cc-section-title">Scores by dimension</p>
  <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:10px;">
    {cells}
  </div>
</div>
"""

# Strengths and areas — replace st.subheader + bullet lists:
def evaluation_strengths_areas_html(strengths: list, areas: list) -> str:
    s_items = "".join(
        f'<div class="cc-list-item"><div class="cc-list-dot green"></div>{s}</div>'
        for s in strengths
    )
    a_items = "".join(
        f'<div class="cc-list-item"><div class="cc-list-dot amber"></div>{a}</div>'
        for a in areas
    )
    return f"""
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
"""

# Criterion feedback block — replace st.subheader + per-criterion markdown:
def evaluation_criterion_block_html(criterion: str, detail: dict) -> str:
    score = detail.get("score", 0)
    explanation = detail.get("explanation", "")
    suggestions = detail.get("suggestions", "")
    label = criterion.replace("_", " ").title()
    pips = "".join(
        f'<span class="cc-pip {"on" if i < score else ""}"></span>'
        for i in range(5)
    )
    return f"""
<div class="cc-criterion-block">
  <div class="cc-criterion-header">
    <span class="cc-criterion-name">{label}</span>
    <div class="cc-criterion-pips">{pips}</div>
    <span class="cc-criterion-score-pill">{score} / 5</span>
  </div>
  <p class="cc-criterion-explanation">{explanation}</p>
  <div class="cc-criterion-suggestion">{suggestions}</div>
</div>
"""

# Suggested next practice prompt — replace st.markdown + st.info:
def evaluation_next_prompt_html(prompt: str) -> str:
    return f"""
<div class="cc-tip-box">
  <p class="cc-tip-label">Suggested next practice focus</p>
  <p class="cc-tip-text">{prompt}</p>
</div>
"""

# Usage in pages/5_Evaluation.py:
#
#   st.markdown(EVALUATION_HEADER, unsafe_allow_html=True)
#
#   # ... existing logic to load/generate evaluation ...
#
#   overall_avg = round(
#       sum(evaluation["scores"].values()) / len(evaluation["scores"]), 1
#   )
#   st.markdown(evaluation_score_banner_html(
#       overall=overall_avg,
#       level=evaluation.get("level", "Developing"),
#       overall_comment=evaluation.get("overall_comment", ""),
#   ), unsafe_allow_html=True)
#
#   st.markdown(evaluation_scores_grid_html(evaluation["scores"]),
#               unsafe_allow_html=True)
#
#   st.markdown(evaluation_strengths_areas_html(
#       evaluation.get("strengths", []),
#       evaluation.get("areas_for_improvement", []),
#   ), unsafe_allow_html=True)
#
#   st.markdown('<div class="cc-card"><p class="cc-section-title">'
#               'Detailed feedback by criterion</p>', unsafe_allow_html=True)
#   for criterion, detail in evaluation.get("criterion_feedback", {}).items():
#       st.markdown(evaluation_criterion_block_html(criterion, detail),
#                   unsafe_allow_html=True)
#   st.markdown('</div>', unsafe_allow_html=True)
#
#   st.markdown(evaluation_next_prompt_html(
#       evaluation.get("suggested_next_practice_prompt", "")
#   ), unsafe_allow_html=True)
#
#   # Keep existing: st.button("Return to Simulation"), st.download_button(...)
#   # Keep existing: past attempts section
#   # Keep existing: transcript section


# =============================================================
# Quick integration checklist
# =============================================================
#
# [ ] Replace assets/styles.css with the new file
# [ ] pages/1_Home.py     — add HOME_HEADER, keep buttons
# [ ] pages/2_Teacher.py  — add TEACHER_HEADER, wrap sections in cc-card
# [ ] pages/3_Student.py  — add STUDENT_HEADER, wrap sections in cc-card
# [ ] pages/4_Simulation.py — add SIMULATION_HEADER, case card, settings/chat wrappers
# [ ] pages/5_Evaluation.py — add EVALUATION_HEADER, replace metrics/lists with helpers
#
# DO NOT touch: utils/, app.py logic, session_state, API calls, storage
