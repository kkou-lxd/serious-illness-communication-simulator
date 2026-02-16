"""Lightweight helpers for cleaning and extracting JSON from LLM text outputs."""

from __future__ import annotations

import json
import re
from typing import Any


CODE_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$", re.IGNORECASE | re.MULTILINE)
JSON_OBJECT_OR_ARRAY_RE = re.compile(r"(\{.*\}|\[.*\])", re.DOTALL)


def extract_json(text: str) -> str:
    """
    Remove common markdown code fences and trim whitespace.
    """
    cleaned = re.sub(CODE_FENCE_RE, "", text or "")
    return cleaned.strip()


def find_json_substring(text: str) -> str:
    """
    Locate the first plausible JSON object/array substring.
    Returns an empty string if none found.
    """
    match = JSON_OBJECT_OR_ARRAY_RE.search(text or "")
    return match.group(1).strip() if match else ""


def try_parse_json(text: str) -> Any:
    """
    Attempt to parse JSON, returning the parsed object or raising json.JSONDecodeError.
    """
    return json.loads(text)


__all__ = ["extract_json", "find_json_substring", "try_parse_json"]
