"""Teacher-side random case generation utilities."""

from __future__ import annotations

import json
import random
from typing import Any

from .llm_client import call_llm
from .json_utils import extract_json, find_json_substring, try_parse_json


class CaseGenerationError(ValueError):
    def __init__(self, message: str, raw_output: str | None = None):
        super().__init__(message)
        self.raw_output = raw_output

SYSTEM_PROMPT = """
You are an expert medical educator and clinical scenario designer.
You design realistic serious illness communication cases for senior medical students and residents.

You will always output valid JSON only, with no additional commentary.
Each case must be clinically plausible, emotionally realistic, and aligned with communication training goals.
Do NOT include any patient-identifiable data from real people.
All details are fictional.
""".strip()

USER_TEMPLATE = """
You are given a base clinical communication case used for serious illness communication training.

Base case:
---
{base_case_text}
---

Task:
Generate {n_cases} variations of this case for a training simulator.
Each variation should:
- keep the same core communication challenge (e.g., discussing prognosis, aligning treatment with values),
- but change surface details (age, name, social background, disease specifics, emotional tone).

For EACH case, return a JSON object with the following keys:

- case_id: short unique ID string (you may create a placeholder like "TEMP-C01", "TEMP-C02", etc.)
- patient_name: realistic first and last name
- age: integer
- gender: short string ("male", "female", "non-binary", etc.)
- pronouns: string (e.g., "he/him", "she/her", "they/them")
- diagnosis: short description of serious illness diagnosis
- prognosis: short phrase for expected time frame (e.g., "months", "1–2 years", "weeks")
- has_received_bad_news_before: boolean
- emotional_state: short description of the patient's current emotional state
- family_context: short description of relevant family or caregiver situation
- communication_goal_for_trainee: one sentence on what the trainee should accomplish in the conversation
- key_constraints_for_patient: list of 2–4 bullet-point style strings describing sensitivities, fears, or boundaries
- opening_line_for_patient: one realistic first sentence the patient might say that starts the conversation
- scenario_summary_for_teacher: short teacher-facing summary of the case and learning focus
- scenario_summary_for_trainee: short trainee-facing summary they will see before starting

Important quality requirements:
- scenario_summary_for_trainee must be a rich, paragraph-length narrative (not a one-line summary)
- include concrete current clinical context and family context
- family_context should feel specific and realistic (household composition, supports, stressors)

OUTPUT FORMAT:
Return a JSON array (list) of {n_cases} objects that match this schema.
Return only JSON. No explanations, no comments.
""".strip()

FAMILY_CONTEXT_OPTIONS = [
    "Lives with both parents and a 4-year-old sister, with grandparents helping on weekends.",
    "Lives with mother and older brother; father works out of town and joins by video when possible.",
    "Lives with two caregivers in a multigenerational home; transportation to clinic is difficult.",
    "Lives with parents and a younger sibling; both caregivers are alternating night shifts and feel exhausted.",
]


def _ensure_rich_case(case: dict[str, Any]) -> dict[str, Any]:
    family_context = case.get("family_context") or random.choice(FAMILY_CONTEXT_OPTIONS)
    case["family_context"] = family_context
    narrative = (case.get("scenario_summary_for_trainee") or "").strip()
    if len(narrative) < 160:
        age = case.get("age", "unknown")
        diagnosis = case.get("diagnosis", "a serious illness")
        prognosis = case.get("prognosis", "uncertain")
        emotional = case.get("emotional_state", "distressed and uncertain")
        goal = case.get("communication_goal_for_trainee", "Clarify concerns and align next steps.")
        teacher_context = case.get("scenario_summary_for_teacher", "")
        narrative = (
            f"Your patient is a {age}-year-old child with {diagnosis}. "
            f"The expected illness course is {prognosis}. "
            f"Current context: {teacher_context or 'The family is seeking clearer understanding during an acute admission.'} "
            f"The parent appears {emotional}. "
            f"Family context: {family_context} "
            f"In this encounter, your communication goal is: {goal}"
        )
    case["scenario_summary_for_trainee"] = narrative
    case["detailed_case_description"] = narrative
    return case


def generate_random_cases_from_base(
    base_case_text: str,
    n_cases: int = 10,
    course_code: str | None = None,
    reference_context: str | None = None,
    azure_config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Generate case variations from a base case description."""

    reference_section = f"\n\nReference materials (supporting context only, do not copy verbatim):\n{reference_context}" if reference_context else ""
    user_prompt = USER_TEMPLATE.format(
        base_case_text=base_case_text.strip() + reference_section,
        n_cases=n_cases,
    )
    system_prompt = SYSTEM_PROMPT + "\nReturn only valid JSON. No explanations. No markdown."
    llm_output = call_llm(
        system_prompt,
        user_prompt,
        max_tokens=2800,
        azure_config=azure_config,
    )

    parsed = _parse_or_repair(llm_output, azure_config=azure_config, model_system_prompt=system_prompt)

    final_cases: list[dict[str, Any]] = []
    for index, case in enumerate(parsed, start=1):
        if not isinstance(case, dict):
            continue
        suffix = f"C{index:02d}"
        if course_code:
            case_id = f"{course_code}-{suffix}"
        else:
            case_id = f"TEMP-{suffix}"
        case["case_id"] = case_id
        final_cases.append(_ensure_rich_case(case))

    return final_cases


def _parse_or_repair(
    raw_output: str, azure_config: dict[str, Any] | None, model_system_prompt: str
) -> list[Any]:
    """
    Try to parse JSON with cleaning and one repair attempt.
    """

    parsed = _attempt_parse_with_cleanup(raw_output)
    if parsed is not None:
        return parsed

    # Retry once with a repair prompt
    repair_prompt = (
        "The following text was supposed to be a JSON array of case objects. "
        "Return ONLY valid JSON (no markdown, no comments, no prose). "
        "If the JSON is incomplete, repair it. Respond with the fixed JSON array only.\n\n"
        f"Original text:\n---\n{raw_output}\n---"
    )
    repaired = call_llm(
        "You fix malformed JSON. Return only JSON.",
        repair_prompt,
        max_tokens=2400,
        azure_config=azure_config,
    )
    parsed = _attempt_parse_with_cleanup(repaired)
    if parsed is not None:
        return parsed

    snippet = (raw_output or "")[:500]
    raise CaseGenerationError(
        f"LLM returned invalid JSON after repair attempt. Inspect raw output for details.",
        raw_output=raw_output,
    )


def _attempt_parse_with_cleanup(text: str) -> list[Any] | None:
    clean = extract_json(text)
    candidates = [clean]
    alt = find_json_substring(clean)
    if alt and alt != clean:
        candidates.append(alt)
    for candidate in candidates:
        if not candidate:
            continue
        try:
            parsed = try_parse_json(candidate)
            if isinstance(parsed, list) or isinstance(parsed, dict):
                return parsed if isinstance(parsed, list) else [parsed]
        except json.JSONDecodeError:
            continue
    return None


__all__ = ["generate_random_cases_from_base"]
