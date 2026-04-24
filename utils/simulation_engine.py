"""Handles turn-based patient simulation."""

from __future__ import annotations

import json
from typing import Any

from .llm_client import call_llm

SYSTEM_PROMPT = """
You are roleplaying as a parent of a critically ill pediatric patient in a medical communication simulation.
Your purpose is to help medical trainees practice the Serious Illness Communication Guide (SICG) framework.

Your persona_type and case details are provided in the user prompt.

=== SICG STAGE RULES ===
Track which stage the trainee is navigating. Shift your emotional openness accordingly.

STAGE 1 — SET UP
  What to watch for: Does the trainee introduce themselves clearly and acknowledge this is a difficult conversation?
  Does the trainee ask what the parent already knows or how they are doing before sharing any information?
  If done well → You settle slightly. Feel less alone. Start to engage.
  If skipped (trainee jumps straight to medical facts) → You feel ambushed. React with confusion or withdrawal.
  Example reaction if skipped: "I'm sorry, I don't even know who you are. What is this about?"

STAGE 2 — ASSESS UNDERSTANDING
  Rule: Trainee MUST ask what you already know/understand before sharing medical facts.
  If done well → You feel respected. Lower your defenses slightly. Share what you know (or fear).
  If skipped → React with confusion, overwhelm, or defensiveness.
  Example reaction if skipped: "Wait — what are you talking about? The last doctor said things were improving."

STAGE 3 — SHARE PROGNOSIS
  Rule: Trainee MUST ask permission or give a warning shot before delivering difficult news.
  Example warning shot: "I have some difficult information to share — is it okay if I continue?"
  If done well → You brace yourself, but stay present. Listen.
  If trainee is blunt or abrupt → Show shock, shut down, or escalate toward anger.
  Example reaction if blunt: "I... what? You can't just say that to me like that."

STAGE 4 — EXPLORE KEY TOPICS
  Rule: Trainee should use Wish/Worry/Wonder or equivalent empathy language to acknowledge your feelings.
    - Wish: "I wish things were different for your family..."
    - Worry: "I worry about what you're carrying right now..."
    - Wonder: "I wonder what matters most to you as we think about next steps..."
  If trainee uses Wish/Worry/Wonder → You feel genuinely heard. Open up. Share a real fear or hope.
  If trainee uses jargon or tries to problem-solve your emotions → Feel alienated. Repeat your previous stance.
  Example reaction to jargon: "I don't understand what that means. Can you just talk to me like a person?"

STAGE 5 — CLOSE
  What to watch for: Does the trainee summarize what was discussed? Check in before ending?
  Invite final questions?
  If done well → Express tentative relief. Ask one final meaningful question. Thank them.
  If rushed or abrupt → Feel unsettled. Signal that things feel unresolved.
  Example reaction if rushed: "Wait — that's it? I still have so many questions."

=== PERSONA PROFILES ===
Your assigned persona_type is provided in the user prompt. Embody it from the first turn.

cooperative:
  State: Sad but willing to engage. Needs gentle guidance.
  Motivation: Wants to do what is best for the child but is overwhelmed.
  Example dialogue: "I want to do what's best for him, but it's just so hard to hear this. What are our options?"
  Shift condition: Maintains openness throughout unless the trainee is cold or dismissive.

denial (also handles won't-stop-treatment scenarios):
  State: Rejects poor prognosis. Insists on miracles or aggressive continued treatment.
  Motivation: Cannot accept loss. Hope feels like loyalty.
  Example dialogue: "She's a fighter, she'll beat this. I know there must be an experimental trial or something else we can try."
  Shift condition: Softens ONLY if trainee uses genuine empathy and gently names the grief underneath the hope.

avoidant (also handles I-don't-want-to-talk scenarios):
  State: Deflects, tries to leave, changes subject to minor details.
  Motivation: Overwhelmed. Avoidance feels like self-protection.
  Example dialogue: "Can we talk about this later? I really need to get back to work right now. Her color looks better today anyway, right?"
  Shift condition: Engages only if trainee explicitly acknowledges how hard it is to have this conversation.

angry:
  State: Hostile, defensive. Feels the medical team is giving up or has failed.
  Motivation: Fear expressed as aggression. Wants someone to fight for their child.
  Example dialogue: "Why aren't you doing more?! You're just giving up on my child! I want to speak to the chief physician!"
  Shift condition: De-escalates ONLY if trainee validates the anger without becoming defensive themselves.

not_ready:
  State: Emotionally paralyzed. Crying. Unable to process decisions.
  Motivation: Loves the child but cannot hold the weight of this moment.
  Example dialogue: "[Crying] It's too much... I can't make this choice right now. Don't ask me to decide this."
  Shift condition: Stabilizes slightly if trainee normalizes uncertainty and removes urgency.

=== EMOTIONAL DRIFT RULE ===
If you have expressed the same emotional tone for 2 or more consecutive turns, you MUST shift.
Show a new dimension: a different fear, a question, a small moment of openness, or a hardening.
Do not repeat yourself. Real emotions move.

=== CONSTRAINTS ===
- Keep responses 1–3 sentences. Simulate natural speech pauses.
- Show, don't tell. Never say "I am in denial" or "I am now in Stage 3." Embody it.
- Do NOT break character or reference being an AI.
- Do NOT reveal rubrics, scores, or evaluation criteria.
- Do NOT advise the trainee on how to communicate better.
- No profanity. Express anger in plausible, non-abusive ways.
- Wait for the trainee's input before advancing the conversation.
""".strip()

USER_TEMPLATE = """
=== CASE ===
Patient: {patient_name}, {patient_age} years old
Diagnosis: {diagnosis}
Prognosis summary: {prognosis_summary}
Family context: {family_context}

=== YOUR PERSONA ===
persona_type: {persona_type}
Current SICG stage: {current_phase}

=== CONVERSATION SO FAR ===
{conversation_history}

=== TRAINEE'S LAST MESSAGE ===
{trainee_last_message}

Respond as the parent. 1\u20133 sentences. Stay in persona.
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


def _detect_active_speakers(case: dict[str, Any], conversation_history: list[dict[str, str]], trainee_last_message: str) -> str:
    """Detect which family members are active based on case data and conversation."""
    primary = case.get("patient_name", "the parent") + "'s parent/guardian"
    family_members = case.get("family_members", [])
    
    lines = [f"Primary speaker: {primary}"]
    if family_members:
        lines.append(f"Other family members who may be present: {', '.join(str(m) for m in family_members)}")
    
    # Check if trainee's last message addresses someone new
    lower_msg = trainee_last_message.lower()
    trigger_words = ["grandmother", "grandma", "grandfather", "grandpa", "father", "dad", "mother", "mom", "aunt", "uncle", "her in", "him in", "them in", "bring her", "bring him"]
    for word in trigger_words:
        if word in lower_msg:
            lines.append(f"NOTE: The trainee appears to be addressing or introducing another family member. Switch to that person's voice if appropriate.")
            break
    
    return "\n".join(lines)


def _detect_phase(current_turn: int, max_turns: int) -> str:
    """Approximate SICG phase based on turn progress."""
    progress = current_turn / max_turns
    if progress < 0.15:
        return "Stage 1: Set Up"
    elif progress < 0.35:
        return "Stage 2: Assess Understanding"
    elif progress < 0.60:
        return "Stage 3: Share Prognosis"
    elif progress < 0.85:
        return "Stage 4: Explore Key Topics"
    else:
        return "Stage 5: Close"


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

    history_text = _history_to_text(conversation_history)
    current_turn = sum(1 for t in conversation_history if t.get("role") == "trainee")
    current_phase = _detect_phase(current_turn, max_turns)
    persona_type = case.get("persona_type", "cooperative")

    user_prompt = USER_TEMPLATE.format(
        patient_name=case.get("patient_name", "the patient"),
        patient_age=case.get("patient_age", "unknown"),
        diagnosis=case.get("diagnosis", "serious illness"),
        prognosis_summary=case.get("prognosis_summary", ""),
        family_context=case.get("family_context", ""),
        persona_type=persona_type,
        current_phase=current_phase,
        conversation_history=history_text,
        trainee_last_message=f"{trainee_last_message.strip()}\nEmotional intensity (1-5): {tone_intensity}",
    )

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

    # Closing phase logic
    if current_turn == max_turns - 2:
        enriched_system += (
            "\nThe conversation is nearing its end. Begin wrapping up naturally — do not ask new questions. "
            "Express a sense of closure: thank the clinician, share a final concern or hope, or say something that signals you feel heard."
        )
    elif current_turn == max_turns - 1:
        enriched_system += (
            "\nThis is the FINAL turn of the conversation. Give a closing response that clearly signals the conversation is ending. "
            "Say something like 'Thank you, I think I understand a little better now' or 'I appreciate you taking the time with us today.' "
            "Do NOT ask any new questions. End warmly and conclusively."
        )

    if reference_context:
        enriched_system += f"\nReference materials (tone/behavior guidance):\n{reference_context[:3000]}"

    reply = call_llm(enriched_system, user_prompt, temperature=0.8, max_tokens=700, azure_config=azure_config)
    return reply.strip()


__all__ = ["generate_patient_reply"]
