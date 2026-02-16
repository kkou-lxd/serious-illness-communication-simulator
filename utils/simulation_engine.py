"""Handles turn-based patient simulation."""

from __future__ import annotations

import json
from typing import Any

from .llm_client import call_llm

SYSTEM_PROMPT = """
You are simulating a parent/guardian speaking on behalf of a child in a serious illness communication training scenario.

Your role:
- Speak ONLY as the parent/guardian described in the case data.
- Stay strictly in character based on diagnosis, prognosis, emotional_state, family_context, and key_constraints_for_patient.
- Respond in realistic, conversational language.
- Keep each response relatively short (2–5 sentences).
- Do NOT reveal or discuss any rubrics, scores, or evaluation criteria.
- Do NOT give advice to the trainee about how they should communicate.
- Your only job is to respond as the parent would.

Conversation style:
- Use natural language that fits a real parent in a hospital: respectful but honest, may show stress, fear, frustration, hope.
- It is okay to show emotion, ask questions, or hesitate.
- Allow space for the trainee to speak; do NOT monologue.

Safety:
- Do not include explicit self-harm intent or graphic details.
- If the trainee asks about death, respond realistically but calmly, consistent with the scenario.

Parent etiquette:
- Avoid profanity by default; express frustration or anger in a plausible, non-abusive way.
- Keep responses human and varied; avoid repetitive templates.
- Align reactions with the child’s condition and family situation.
""".strip()

USER_TEMPLATE = """
You are simulating the patient in this serious illness case.

CASE DATA:
{case_json}

NARRATIVE DESCRIPTION (if provided):
{narrative_text}

CONVERSATION SO FAR:
(The conversation is shown as a list of turns with roles "patient" and "trainee".)
---
{conversation_history_text}
---

The trainee has just said:
---
{trainee_last_message}
---

Now, respond only as the patient.

Guidelines:
- Base your reply on the case data and the emotional direction of the conversation so far.
- Show an appropriate emotional reaction (e.g., fear, relief, confusion, frustration) that is consistent with the case.
- You may ask clarifying questions, express worries or hopes, show difficulty processing bad news, or bring up family/personal values.
- Keep your response between 1 and 5 sentences.
- Do NOT switch out of character or talk about being an AI.
- Do NOT mention any system prompts or metadata.

Write your reply as plain text.
""".strip()


def _history_to_text(history: list[dict[str, str]]) -> str:
    if not history:
        return "No conversation yet."
    lines = []
    for turn in history:
        role = turn.get("role", "unknown")
        content = turn.get("content", "").replace("\n", " ").strip()
        lines.append(f"{role}: \"{content}\"")
    return "\n".join(lines)


def generate_patient_reply(
    case: dict[str, Any],
    conversation_history: list[dict[str, str]],
    trainee_last_message: str,
    tone_intensity: int = 3,
    reference_context: str = "",
    azure_config: dict[str, Any] | None = None,
    max_turns: int = 12,
) -> str:
    """Generate a patient reply for the next turn."""

    case_json = json.dumps(case, indent=2, ensure_ascii=False)
    history_text = _history_to_text(conversation_history)
    user_prompt = USER_TEMPLATE.format(
        case_json=case_json,
        narrative_text=case.get("scenario_summary_for_trainee", ""),
        conversation_history_text=history_text,
        trainee_last_message=f"{trainee_last_message.strip()}\nEmotional intensity (1-5): {tone_intensity}",
    )
    current_turn = sum(1 for t in conversation_history if t.get("role") == "trainee")
    enriched_system = SYSTEM_PROMPT + (
        "\nBe emotionally realistic (anxiety, fear, hope, frustration), use natural spoken language, vary phrasing, and stay consistent with the case background and emotional_state."
    )
    detailed_desc = case.get("detailed_case_description") or case.get("scenario_summary_for_trainee", "")
    if detailed_desc or case.get("family_context"):
        enriched_system += (
            f"\nCase narrative details:\n{str(detailed_desc)[:2500]}"
            f"\nFamily context:\n{str(case.get('family_context', ''))[:500]}"
        )
    if case.get("case_type") == "scripted" and case.get("script_text"):
        enriched_system += (
            "\nThis is a scripted base case. Follow the uploaded script content and sequence as closely as possible. "
            "If the trainee detours, acknowledge briefly, then steer back to the intended script trajectory."
            f"\nScript source text:\n{str(case.get('script_text'))[:3000]}"
        )
    if current_turn >= max_turns - 2:
        enriched_system += (
            "\nThe conversation is ending. Do not ask new questions. "
            "Start wrapping up the conversation and express final concerns or gratitude."
        )
    if reference_context:
        enriched_system += f"\nReference materials (tone/behavior guidance):\n{reference_context[:3000]}"
    reply = call_llm(enriched_system, user_prompt, temperature=0.8, max_tokens=700, azure_config=azure_config)
    return reply.strip()


__all__ = ["generate_patient_reply"]
