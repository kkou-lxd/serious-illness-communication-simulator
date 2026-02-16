from __future__ import annotations

import json
import uuid
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st

from utils.auth import render_nav, set_role_from_query
from utils.case_generator import generate_random_cases_from_base
from utils.file_extraction import (
    extract_text_from_uploaded_file,
    extract_general_description_from_uploaded_file,
)
from utils.reference_loader import load_builtin_guides, merge_references
from utils.storage import load_cases, save_cases, get_student_progress

st.title("Teacher Panel")
st.write("Create or update a course with randomized scenarios.")
if st.button("⬅ Back to Home"):
    try:
        st.switch_page("pages/1_Home.py")
    except Exception:
        st.info("Open Home from the sidebar.")


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
    st.stop()

course_name = st.text_input("Course name", st.session_state.get("course_name", ""))
if course_name:
    st.session_state["course_name"] = course_name

case_col, ref_col = st.columns(2)
with case_col:
    st.subheader("Case Library / Base Case")
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
            cols = st.columns([6, 2, 2])
            cols[0].write(f"{c['title']} (uploaded {c.get('uploaded_at','')})")
            if cols[1].button("Delete", key=f"del_case_{c['id']}"):
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
    st.subheader("Reference Materials")
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
    st.subheader("Generated cases")
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

else:
    st.info("Generate scenarios to see them here.")

if st.session_state.get("course_code"):
    st.subheader("Active Course Code")
    st.code(st.session_state["course_code"])

st.subheader("Student Progress")
st.dataframe(get_student_progress(), hide_index=True)

with st.expander("View raw JSON for generated cases"):
    st.code(json.dumps(cases, indent=2, ensure_ascii=False))
