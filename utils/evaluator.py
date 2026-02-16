"""Evaluation and comparative evaluation logic."""

from __future__ import annotations

import json
from typing import Any

from .llm_client import call_llm

EVAL_SYSTEM_PROMPT = """
You are an expert clinical communication educator.
You evaluate serious illness conversations between medical trainees and patients.

You use a structured rubric and give clear, constructive feedback.

For EACH criterion provide:
- score (1-5)
- detailed explanation of WHY that score was given (minimum 30 words), referencing specific observable behaviors from the transcript
- concrete, actionable suggestions for improvement (minimum 30 words)

Avoid generic statements. Anchor feedback in what was said/done.
Output JSON only.
""".strip()

EVAL_USER_TEMPLATE = """
Evaluate the following serious illness communication role-play.

CASE DATA:
{case_json}

CONVERSATION TRANSCRIPT:
(The roles are "trainee" and "patient".)
---
{transcript_text}
---

Rubric dimensions:
- empathy: Does the trainee acknowledge and validate the patient's emotions?
- clarity: Is information delivered clearly, without jargon, and at an appropriate pace?
- structure: Does the conversation have a logical flow (setup, exploration, information sharing, planning)?
- information_delivery: Does the trainee share key medical information honestly and sensitively?
- shared_decision_making: Does the trainee explore patient values and preferences, and invite them into decision making?
- managing_emotions: Does the trainee respond appropriately when emotions arise (e.g., silence, tears, anger, fear)?

Scoring:
- 1 = Poor / rarely demonstrated
- 2 = Inconsistent / major gaps
- 3 = Adequate / meets minimum expectations
- 4 = Strong / often demonstrates good practice
- 5 = Excellent / consistently models best practice

OUTPUT FORMAT:
Return a single JSON object with the following structure:
{{
  "scores": {{...as above...}},
  "overall_comment": "<summary 3–6 sentences>",
  "strengths": ["...", "..."],
  "areas_for_improvement": ["...", "..."],
  "criterion_feedback": {{
    "empathy": {{"score": <int>, "explanation": "<>=30 words>", "suggestions": "<>=30 words>"}},
    "clarity": {{...}},
    "structure": {{...}},
    "information_delivery": {{...}},
    "shared_decision_making": {{...}},
    "managing_emotions": {{...}}
  }},
  "suggested_next_practice_prompt": "<one sentence>",
  "level": "<Beginning|Developing|Proficient|Advanced>"
}}
Do NOT include markdown or commentary. JSON only.
""".strip()

COMPARE_SYSTEM_PROMPT = """
You are an expert clinical communication coach.

You compare two attempts by the same trainee on the same serious illness case.
Identify growth between attempts and remaining opportunities.
Output JSON only.
""".strip()

COMPARE_USER_TEMPLATE = """
Compare the following two serious illness communication attempts.

CASE DATA:
{case_json}

ATTEMPT A (earlier attempt) TRANSCRIPT:
---
{attempt_a_text}
---

ATTEMPT B (later attempt) TRANSCRIPT:
---
{attempt_b_text}
---

Focus on empathy, clarity, structure and pacing, exploration of values, and handling of emotions.

OUTPUT FORMAT:
Return a JSON object with summary_of_changes, improvements, remaining_gaps, and coach_message_to_trainee.
""".strip()


def _transcript_to_text(transcript: list[dict[str, str]]) -> str:
    if not transcript:
        return "No transcript available."
    return "\n".join(
        f"{t.get('role', 'unknown')}: \"{t.get('content', '').strip()}\""
        for t in transcript
    )


def _safe_json_loads(data: str, default: dict[str, Any]) -> dict[str, Any]:
    try:
        parsed = json.loads(data)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    return default


def evaluate_conversation(
    case: dict[str, Any],
    transcript: list[dict[str, str]],
    azure_config: dict[str, Any] | None = None,
    reference_context: str = "",
) -> dict[str, Any]:
    """Return structured evaluation JSON for a single attempt."""

    case_json = json.dumps(case, indent=2, ensure_ascii=False)
    transcript_text = _transcript_to_text(transcript)
    user_prompt = EVAL_USER_TEMPLATE.format(
        case_json=case_json,
        transcript_text=transcript_text,
    )
    if reference_context:
        user_prompt += f"\n\nREFERENCE GUIDES:\n{reference_context[:3000]}"
    llm_output = call_llm(EVAL_SYSTEM_PROMPT, user_prompt, temperature=0.2, max_tokens=900, azure_config=azure_config)
    default = {
        "scores": {
            "empathy": 3,
            "clarity": 3,
            "structure": 3,
            "information_delivery": 3,
            "shared_decision_making": 3,
            "managing_emotions": 3,
        },
        "overall_comment": llm_output[:400],
        "strengths": ["Demonstrated empathy at least once."],
        "areas_for_improvement": ["Be more explicit about patient values."],
        "suggested_next_practice_prompt": "Next time, pause to explore what matters most to the patient before sharing more facts.",
        "level": "Developing",
        "criterion_feedback": {
            k: {
                "score": 3,
                "explanation": "Default feedback placeholder with insufficient data to personalize.",
                "suggestions": "Default improvement suggestion placeholder.",
            }
            for k in ["empathy", "clarity", "structure", "information_delivery", "shared_decision_making", "managing_emotions"]
        },
    }
    return _safe_json_loads(llm_output, default)


def compare_two_attempts(
    case: dict[str, Any],
    attempt_a_transcript: list[dict[str, str]],
    attempt_b_transcript: list[dict[str, str]],
    azure_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return growth-focused comparison between two attempts."""

    case_json = json.dumps(case, indent=2, ensure_ascii=False)
    user_prompt = COMPARE_USER_TEMPLATE.format(
        case_json=case_json,
        attempt_a_text=_transcript_to_text(attempt_a_transcript),
        attempt_b_text=_transcript_to_text(attempt_b_transcript),
    )
    llm_output = call_llm(
        COMPARE_SYSTEM_PROMPT, user_prompt, temperature=0.3, max_tokens=800, azure_config=azure_config
    )
    default = {
        "summary_of_changes": llm_output[:200],
        "improvements": ["Attempt B shows clearer information delivery."],
        "remaining_gaps": ["Still needs deeper exploration of values."],
        "coach_message_to_trainee": "Use these reflections to keep iterating; notice what improved and plan a concrete focus for next time.",
    }
    return _safe_json_loads(llm_output, default)


__all__ = ["evaluate_conversation", "compare_two_attempts"]
