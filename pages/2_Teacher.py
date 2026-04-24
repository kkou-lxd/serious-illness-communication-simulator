from __future__ import annotations

import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path

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

/* ── Streamlit Native Containers -> CC Cards ── */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-card) !important;
    padding: 28px 32px !important;
    margin-bottom: 8px !important;
    transition: all 0.3s ease !important;
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

/* ── Course code box (Pure HTML) ── */
.cc-code-box {
    display: flex;
    align-items: center;
    background: var(--accent-light);
    border: 1.5px solid var(--border);
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 8px;
}

.cc-code-label {
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin: 0 0 6px 0;
}

.cc-code-value {
    font-family: var(--font-title);
    font-size: 28px;
    font-weight: 400;
    color: var(--text-primary);
    letter-spacing: 0.04em;
    margin: 0;
}

/* ── Streamlit inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stNumberInput"] input:focus {
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

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background-color: var(--surface) !important;
    border: 1.5px dashed var(--border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}
[data-testid="stFileUploader"] section,
[data-testid="stFileUploadDropzone"] {
    background-color: transparent !important;
}
[data-testid="stFileUploadDropzone"] svg {
    stroke: var(--text-muted) !important; 
}
[data-testid="stFileUploadDropzone"] p,
[data-testid="stFileUploader"] label {
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    padding: 14px 18px !important;
}

/* ── Alerts: success / info / warning / error  ── */
[data-testid="stAlert"] {
    background-color: transparent !important;
    border: none !important;
}
[data-testid="stAlert"] > div {
    background-color: var(--surface) !important; 
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--text-muted) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
[data-testid="stAlert"] p {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important; 
}
[data-testid="stAlert"] svg {
    fill: var(--text-muted) !important; 
}

/* ── Number Input ── */
[data-testid="stNumberInputStepUp"],
[data-testid="stNumberInputStepDown"] {
    background-color: transparent !important;
    color: var(--text-muted) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    padding: 14px 18px !important;
}

/* ── Alerts: success / info / warning / error 大改造 ── */
[data-testid="stAlert"] {
    background-color: var(--surface) !important;
    border: none !important;
    border-left: 4px solid var(--text-muted) !important;
    border-radius: 8px !important;
}
[data-testid="stAlert"][data-baseweb="notification"] {
    background-color: var(--surface) !important;
}
[data-testid="stAlert"] p {
    font-family: var(--font-body) !important;
    font-size: 14px !important;
    color: var(--text-primary) !important; 
}
[data-testid="stAlert"] svg {
    fill: var(--text-muted) !important; 
}

/* ── Buttons ── */
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
.stButton > button[kind="primary"],
.stButton > button[data-testid*="primary"] {
    background-color: var(--accent) !important;
    border-color: var(--accent) !important;
    color: #FFFFFF !important;
}
.stButton > button p {
    white-space: nowrap !important;
    word-break: keep-all !important;
}
div[data-testid="stElementContainer"]:has(.back-btn-anchor) + div[data-testid="stElementContainer"] .stButton > button:hover {
    border-color: var(--accent-blue) !important;
    color: var(--accent-blue) !important;
    background-color: var(--accent-lightblue) !important;
}

/* ── Link Button (返回键专用) ── */
[data-testid="stLinkButton"] a {
    color: var(--text-muted) !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    text-decoration: none !important;
}
[data-testid="stLinkButton"] a:hover {
    color: var(--accent) !important;
}

[data-testid="stAlert"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}
/* 穿透到内层：统一给一个干净的白底和微弱阴影，让它从素色背景里浮出来 */
[data-testid="stAlert"] > div {
    background-color: #FFFFFF !important; 
    border: 1px solid var(--border) !important;
    border-left: 4px solid var(--accent-blue) !important; /* 默认提示用深蓝，显得很专业 */
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.03) !important; /* 增加轻微呼吸感 */
}
/* 如果是系统警告（比如上传重复文件），就保持你的赤陶色 */
[data-testid="stAlert"][data-baseweb="notification"] > div {
    border-left-color: var(--accent) !important; 
    background-color: var(--accent-light) !important;
}
            
/* ── Dataframe 表头强化 ── */
[data-testid="stDataFrame"] th {
    background-color: var(--accent-blue) !important; /* 深蓝表头 */
    color: #FFFFFF !important; /* 纯白文字 */
    font-family: var(--font-body) !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    border-bottom: none !important;
}
[data-testid="stDataFrame"] {
    border: 1.5px solid var(--accent-blue) !important; 
    border-radius: 12px !important;
    overflow: hidden !important;
}
            
/* ── Course code box 变身 ── */
.cc-code-box {
    display: flex;
    align-items: center;
    background: var(--blue-light); /* 冰蓝底色 */
    border: 1.5px solid var(--accent-blue); /* 深蓝边框 */
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 8px;
}
.cc-code-label {
    font-family: var(--font-body);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent-blue); /* 标签深蓝色 */
    margin: 0 0 6px 0;
}
.cc-code-value {
    font-family: var(--font-title);
    font-size: 28px;
    font-weight: 400;
    color: var(--accent-blue); /* 号码深蓝色 */
    letter-spacing: 0.04em;
    margin: 0;
}
            
/* ── Fade-in ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
.cc-page-header { animation: fadeUp 0.6s ease both 0.08s; }
[data-testid="stVerticalBlockBorderWrapper"] { animation: fadeUp 0.6s ease both 0.18s; }
</style>
""", unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────

from utils.auth import render_nav, set_role_from_query
from utils.case_generator import generate_random_cases_from_base
from utils.file_extraction import (
    extract_text_from_uploaded_file,
    extract_general_description_from_uploaded_file,
)
from utils.reference_loader import load_builtin_guides, merge_references
from utils.storage import load_cases, save_cases, get_student_progress

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
  <p class="cc-page-title">Teacher panel</p>
  <p class="cc-page-sub">Create and configure courses for your students.</p>
</div>
""", unsafe_allow_html=True)

def _init_state() -> None:
    st.session_state.setdefault("generated_cases", [])
    st.session_state.setdefault("course_code", None)
    st.session_state.setdefault("case_library", [])
    st.session_state.setdefault("reference_library", [])
    st.session_state.setdefault("selected_base_case", None)
    if "builtin_references" not in st.session_state:
        base_dir = Path(__file__).resolve().parents[1]
        st.session_state["builtin_references"] = load_builtin_guides(base_dir)
    st.session_state.setdefault("case_library", [])
    st.session_state.setdefault("selected_base_case", None)


set_role_from_query()
_init_state()
def render_back_button():
    st.markdown('<div class="back-btn-anchor"></div>', unsafe_allow_html=True)
    if st.button("Back"):
        try:
            st.switch_page("pages/1_Home.py")
        except Exception:
            pass
render_nav("teacher")
st.session_state.setdefault("authenticated", False)
if not st.session_state["authenticated"]:
    passcode_input = st.text_input("Enter teacher passcode", type="password")
    if st.button("Access"):
        if passcode_input == st.secrets["TEACHER_PASSCODE"]:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect passcode.")
    render_back_button() 
    st.stop()   

st.markdown('<div class="cc-card"><p class="cc-section-title">Course setup</p>', unsafe_allow_html=True)
course_name = st.text_input("Course name", st.session_state.get("course_name", ""))
if course_name:
    st.session_state["course_name"] = course_name
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="cc-card"><p class="cc-section-title">Case library &amp; reference materials</p>', unsafe_allow_html=True)
case_col, ref_col = st.columns(2)
with case_col:
    st.markdown('<p class="cc-section-title" style="margin-top:4px;">Case library</p>', unsafe_allow_html=True)
    case_files = st.file_uploader("Upload base case file(s)", type=["txt", "pdf", "docx"], accept_multiple_files=True)
    if case_files:
        for f in case_files:
            try:
                text = extract_text_from_uploaded_file(f)
                f.seek(0)
                general_description = extract_general_description_from_uploaded_file(f)
                title = f.name
                content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
                if any(c.get("hash") == content_hash or c.get("title") == title for c in st.session_state["case_library"]):
                    st.warning(f"This file was already uploaded: {title}")
                    continue
                st.session_state["case_library"].append(
                    {
                        "id": str(uuid.uuid4()),
                        "title": title,
                        "text": text,
                        "description": general_description or text,
                        "length": len(text),
                        "hash": content_hash,
                        "uploaded_at": datetime.utcnow().isoformat(),
                    }
                )
                st.success(f"Added case: {title} ({len(text)} chars)")
                with st.expander(f"Case Preview: {title}"):
                    st.write(f"Length: {len(text)} chars")
                    st.code(text[:300] or "[No text extracted]")
                    if len(text.strip()) < 200:
                        st.warning("Extraction seems too short; check file type or parser.")
            except Exception as exc:
                st.error(f"Could not read {f.name}: {exc}")

    if st.session_state["case_library"]:
        st.info(f"Cases in library: {len(st.session_state['case_library'])}")
        st.dataframe(
            [
                {
                    "id": c["id"][:8],
                    "filename": c["title"],
                    "uploaded_at": c.get("uploaded_at", ""),
                    "length": c.get("length", 0),
                }
                for c in st.session_state["case_library"]
            ],
            hide_index=True,
        )
        for idx, c in enumerate(st.session_state["case_library"]):
            cols = st.columns([0.85, 0.15]) 
            with cols[0]:
                st.markdown(f"""
                    <div style="padding: 5px 0;">
                        <span style="font-weight:500;">{c['title']}</span><br>
                        <span style="font-size:11px; color:var(--text-muted);">Uploaded: {c.get('uploaded_at','')[:16]}</span>
                    </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                if st.button(" Delete ", key=f"del_case_{c['id']}", use_container_width=True):
                   st.session_state["case_library"] = [x for x in st.session_state["case_library"] if x["id"] != c["id"]]
                   st.rerun()
        titles = [c["title"] for c in st.session_state["case_library"]]
        default_index = titles.index(st.session_state["selected_base_case"]) if st.session_state["selected_base_case"] in titles else 0
        selected_title = st.selectbox("Select base case", titles, index=default_index)
        st.session_state["selected_base_case"] = selected_title
        selected_case_text = next(
            (c.get("description") or c["text"])
            for c in st.session_state["case_library"]
            if c["title"] == selected_title
        )
        st.session_state["current_case_description"] = selected_case_text
    else:
        selected_case_text = ""
        st.info("Upload a base case file to add it to the library.")

with ref_col:
    st.markdown('<p class="cc-section-title" style="margin-top:4px;">Reference materials</p>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload reference files", type=["txt", "pdf", "docx"], accept_multiple_files=True)
    extracted_texts: list[str] = []
    if uploaded_files:
        for uf in uploaded_files:
            try:
                text = extract_text_from_uploaded_file(uf)
                extracted_texts.append(text)
                st.session_state["reference_library"].append(
                    {"id": str(uuid.uuid4()), "title": uf.name, "text": text, "length": len(text)}
                )
                st.success(f"Loaded reference: {uf.name} ({len(text)} chars)")
                with st.expander(f"Reference Preview: {uf.name}"):
                    st.write(f"Length: {len(text)} chars")
                    st.code(text[:300] or "[No text extracted]")
                    if len(text.strip()) < 200:
                        st.warning("Extraction seems too short; check file type or parser.")
            except Exception as exc:
                st.error(f"Could not read {uf.name}: {exc}")

base_case_text = st.text_area(
    "Or paste base case text here",
    st.session_state.get("base_case_text", ""),
    height=200,
)
st.markdown('</div>', unsafe_allow_html=True)

reference_context = "\n\n".join(extracted_texts) if uploaded_files else ""

if base_case_text:
    st.session_state["base_case_text"] = base_case_text

col_n, _ = st.columns(2)
with col_n:
    n_cases = st.number_input("Number of random scenarios", min_value=1, max_value=15, value=5)

if st.button("Generate Random Scenarios", use_container_width=True):
    st.session_state["course_code"] = f"COURSE-{uuid.uuid4().hex[:6].upper()}"
    base_standard = (selected_case_text or "") + ("\n\n" + base_case_text.strip() if base_case_text.strip() else "")
    combined_references = merge_references(
        st.session_state.get("builtin_references", []),
        st.session_state.get("reference_library", []),
    )
    full_reference_context = "\n\n".join(filter(None, [combined_references, reference_context]))
    if not base_standard.strip():
        st.error("Please provide a base case (upload or paste).")
    else:
        with st.spinner("Generating cases..."):
            try:
                cases = generate_random_cases_from_base(
                    base_standard,
                    n_cases=int(n_cases),
                    course_code=st.session_state["course_code"],
                    reference_context=full_reference_context,
                )
                for c in cases:
                    c.pop("difficulty", None)
                st.session_state["generated_cases"] = cases
                st.success(f"Course code: {st.session_state['course_code']}")
            except Exception as exc:
                from utils.case_generator import CaseGenerationError

                if isinstance(exc, CaseGenerationError):
                    st.error(f"Case generation failed: {exc}")
                    if exc.raw_output:
                        with st.expander("View raw LLM output"):
                            st.code(exc.raw_output)
                else:
                    st.error(f"Case generation failed: {exc}")

cases = st.session_state.get("generated_cases", [])
if cases:
    st.markdown('<div class="cc-card"><p class="cc-section-title">Generated cases</p>', unsafe_allow_html=True)
    st.dataframe(
        [
            {
                "case_id": c.get("case_id"),
                "patient_name": c.get("patient_name"),
                "age": c.get("age"),
                "diagnosis": c.get("diagnosis"),
            }
            for c in cases
        ],
        hide_index=True,
    )

    st.markdown("### Quick edit")
    case_options = {f"{c['case_id']} - {c['patient_name']}": idx for idx, c in enumerate(cases)}
    selected_label = st.selectbox("Select a case to edit", list(case_options.keys()))
    selected_case = cases[case_options[selected_label]]
    edit_col1, edit_col2 = st.columns(2)
    with edit_col1:
        patient_name = st.text_input("Patient name", selected_case.get("patient_name", ""))
        age = st.number_input("Age", min_value=0, max_value=120, value=int(selected_case.get("age", 60)))
    with edit_col2:
        diagnosis = st.text_input("Diagnosis", selected_case.get("diagnosis", ""))
        prognosis = st.text_input("Prognosis", selected_case.get("prognosis", "months"))

    # [ADDED] Persona type selector — maps to simulation_engine.py persona profiles
    PERSONA_OPTIONS = ["cooperative", "denial", "avoidant", "angry", "not_ready"]
    PERSONA_DESCRIPTIONS = {
        "cooperative": "Sad but willing to engage. Needs gentle guidance.",
        "denial": "Rejects poor prognosis. Insists on miracles or continued treatment.",
        "avoidant": "Deflects, tries to leave, changes subject to minor details.",
        "angry": "Hostile, defensive. Feels the medical team is giving up.",
        "not_ready": "Emotionally paralyzed. Unable to process decisions.",
    }
    current_persona = selected_case.get("persona_type", "cooperative")
    if current_persona not in PERSONA_OPTIONS:
        current_persona = "cooperative"
    persona_type = st.selectbox(
        "Parent persona type",
        options=PERSONA_OPTIONS,
        index=PERSONA_OPTIONS.index(current_persona),
        help="Determines the parent's emotional starting point in the simulation.",
    )
    st.caption(f"ℹ️ {PERSONA_DESCRIPTIONS[persona_type]}")
    # [END ADDED]
    narrative = st.text_area(
        "Patient Narrative / General Description",
        selected_case.get("scenario_summary_for_trainee", ""),
        height=120,
    )

    if st.button("Apply edits"):
        selected_case.update(
            {
                "patient_name": patient_name,
                "age": int(age),
                "diagnosis": diagnosis,
                "prognosis": prognosis,
                "scenario_summary_for_trainee": narrative,
                "persona_type": persona_type,  # [ADDED]
            }
        )
        st.success("Case updated in memory.")

    if st.button("Save Case Library", type="primary"):
        existing = load_cases()
        course_code = st.session_state["course_code"]
        base_cases = []
        for idx, c in enumerate(st.session_state.get("case_library", []), start=1):
            base_cases.append(
                {
                    "case_id": f"{course_code}-SCRIPT-{idx}",
                    "patient_name": c["title"],
                    "case_type": "scripted",
                    "script_text": c["text"],
                    "scenario_summary_for_teacher": c["text"][:200],
                    "scenario_summary_for_trainee": c.get("description") or c["text"],
                    "detailed_case_description": c.get("description") or c["text"],
                    "uploaded_at": c.get("uploaded_at"),
                }
            )
        existing[course_code] = {
            "course_name": course_name or "Unnamed Course",
            "base_case_description": base_case_text,
            "reference_context": merge_references(
                st.session_state.get("builtin_references", []),
                st.session_state.get("reference_library", []),
            ),
            "cases": cases,
            "base_cases": base_cases,
        }
        save_cases(existing)
        st.success("Course saved. Share this course code with students:")
        st.info(course_code)

    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Generate scenarios to see them here.")

if st.session_state.get("course_code"):
    cc = st.session_state["course_code"]
    st.markdown(f"""
<div class="cc-card">
  <p class="cc-section-title">Active course code</p>
  <div class="cc-code-box">
    <div>
      <p class="cc-code-label">Share with students</p>
      <p class="cc-code-value">{cc}</p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="cc-card"><p class="cc-section-title">Student progress</p>', unsafe_allow_html=True)
st.dataframe(get_student_progress(), hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("View raw JSON for generated cases"):
    st.code(json.dumps(cases, indent=2, ensure_ascii=False))

render_back_button()