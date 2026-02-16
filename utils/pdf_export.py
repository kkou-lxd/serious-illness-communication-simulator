"""
Pretty modern PDF export (Unicode + nice layout)
Uses fpdf2 + DejaVuSans
"""

from __future__ import annotations
import json
import re
from typing import Any
from fpdf import FPDF
from fpdf.errors import FPDFException


FONT_PATH = "utils/DejaVuSans.ttf"
MIN_TURNS_FOR_DETAILED_FEEDBACK = 2


def _chunk_long_tokens(text: str, chunk_size: int = 32) -> str:
    def repl(match: re.Match[str]) -> str:
        token = match.group(0)
        return " ".join(token[i : i + chunk_size] for i in range(0, len(token), chunk_size))

    return re.sub(r"\S{64,}", repl, text)


def _sanitize_pdf_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return _chunk_long_tokens(text)


def _extract_overall_comment(evaluation: dict[str, Any]) -> str:
    overall = _sanitize_pdf_text(evaluation.get("overall_comment", "")).strip()
    if not overall:
        return ""
    if overall[:1] not in {"{", "["}:
        return overall

    try:
        parsed = json.loads(overall)
    except json.JSONDecodeError:
        return ""
    if isinstance(parsed, dict):
        parsed_comment = parsed.get("overall_comment")
        if isinstance(parsed_comment, str):
            return _sanitize_pdf_text(parsed_comment).strip()
    return ""


def _count_meaningful_turns(transcript: list[dict[str, Any]] | None) -> int:
    if not transcript:
        return 0
    return sum(
        1
        for turn in transcript
        if str(turn.get("content", "")).strip() and str(turn.get("role", "")).lower() != "system"
    )


class PrettyPDF(FPDF):
    def header(self):
        self.set_font("DejaVu", size=18)
        self.cell(0, 12, "Serious Illness Communication Evaluation Report", ln=True)
        self.ln(6)


def generate_pdf_report(
    student_name: str,
    course_code: str,
    case: dict[str, Any],
    evaluation: dict[str, Any],
    transcript: list[dict[str, Any]] | None = None,
    attempt_id: str | None = None,
    timestamp: str | None = None,
    student_id: str | None = None,
) -> bytes:

    pdf = PrettyPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_font("DejaVu", "", FONT_PATH)
    pdf.set_font("DejaVu", size=11)

    pdf.add_page()
    insufficient_data = _count_meaningful_turns(transcript) < MIN_TURNS_FOR_DETAILED_FEEDBACK

    # ---------- helpers ----------
    def section(title: str):
        pdf.ln(8)
        pdf.set_font("DejaVu", size=14)
        pdf.cell(0, 8, title, ln=True)
        pdf.set_font("DejaVu", size=11)
        pdf.ln(2)

    def line(text):
        content = _sanitize_pdf_text(text)
        pdf.set_x(pdf.l_margin)
        width = pdf.w - pdf.l_margin - pdf.r_margin
        if width <= 5:
            pdf.add_page()
            pdf.set_x(pdf.l_margin)
            width = pdf.w - pdf.l_margin - pdf.r_margin
        try:
            # Avoid empty-string layout edge cases in some fpdf versions.
            pdf.multi_cell(width, 6, content or " ")
        except FPDFException:
            pdf.multi_cell(width, 6, _chunk_long_tokens(content, chunk_size=24) or " ")
    

    # ---------- Student Info ----------
    section("Student Information")

    line(f"Student: {student_name}")
    if student_id:
        line(f"Student ID: {student_id}")

    line(f"Course: {course_code}")
    line(f"Case: {case.get('patient_name', 'Unknown')} ({case.get('case_id')})")

    if attempt_id:
        line(f"Attempt: {attempt_id}")
    if timestamp:
        line(f"Time: {timestamp}")

    # ---------- Scores ----------
    section("Scores")

    if insufficient_data:
        line(
            "N/A: The simulation was ended before sufficient data could be collected for a detailed evaluation."
        )
        for k in evaluation.get("scores", {}).keys():
            line(f"{k.title()}: N/A")
    else:
        for k, v in evaluation.get("scores", {}).items():
            line(f"{k.title()}: {v}")

    # ---------- Overall ----------
    section("Overall Comment")
    if insufficient_data:
        line(
            "The simulation was ended before sufficient data could be collected for a detailed evaluation. "
            "Please complete a longer session for a full report."
        )
    else:
        overall_comment = _extract_overall_comment(evaluation)
        if overall_comment:
            line(overall_comment)
        else:
            line("Evaluation summary unavailable in this attempt.")

    # ---------- Strengths ----------
    section("Strengths")
    if insufficient_data:
        line("Not enough conversation data to identify reliable strengths.")
    else:
        for s in evaluation.get("strengths", []):
            line(f"• {s}")

    # ---------- Improvements ----------
    section("Areas for Improvement")
    if insufficient_data:
        line("Please run a longer simulation to receive personalized improvement feedback.")
    else:
        for s in evaluation.get("areas_for_improvement", []):
            line(f"• {s}")

    # ---------- Detailed Feedback ----------
    section("Detailed Feedback")

    if insufficient_data:
        line("Detailed criterion feedback is unavailable because the transcript is too short.")
    else:
        for crit, detail in (evaluation.get("criterion_feedback") or {}).items():
            pdf.ln(3)
            pdf.set_font("DejaVu", size=12)
            line(f"{crit.title()}  (Score: {detail.get('score','')})")

            pdf.set_font("DejaVu", size=11)
            line(f"Why: {detail.get('explanation','')}")
            line(f"How to improve: {detail.get('suggestions','')}")

    # ---------- Transcript ----------
    if transcript:
        pdf.ln(4)
        section("Conversation Transcript")
        for turn in transcript:
            role = str(turn.get("role", "unknown")).title()
            line(f"{role}: {turn.get('content')}")

    return bytes(pdf.output(dest="S"))
