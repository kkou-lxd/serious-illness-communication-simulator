"""Utility helpers for JSON storage."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
CASES_PATH = DATA_DIR / "cases.json"
STUDENT_RECORDS_PATH = DATA_DIR / "student_records.json"
SERVER_CONFIG_PATH = DATA_DIR / "server_config.json"


def _ensure_data_files() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CASES_PATH.exists():
        CASES_PATH.write_text("{}", encoding="utf-8")
    if not STUDENT_RECORDS_PATH.exists():
        STUDENT_RECORDS_PATH.write_text("[]", encoding="utf-8")
    if not SERVER_CONFIG_PATH.exists():
        SERVER_CONFIG_PATH.write_text("{}", encoding="utf-8")


def _load_json(path: Path, default: Any) -> Any:
    _ensure_data_files()
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default


def _save_json(path: Path, data: Any) -> None:
    _ensure_data_files()
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_cases() -> dict[str, Any]:
    """Return all stored course cases grouped by course_code."""

    return _load_json(CASES_PATH, {})


def save_cases(cases: dict[str, Any]) -> None:
    """Persist the full cases dictionary."""

    _save_json(CASES_PATH, cases)


def load_student_records() -> list[dict[str, Any]]:
    """Return stored student attempt records."""

    return _load_json(STUDENT_RECORDS_PATH, [])


def save_student_records(records: list[dict[str, Any]]) -> None:
    """Persist all student records."""

    for record in records:
        record.setdefault("student_id", "Unknown")
        record.setdefault("timestamp", "")
        record.setdefault("course_code", "")
    _save_json(STUDENT_RECORDS_PATH, records)


def load_server_config() -> dict[str, Any]:
    """Load server-side configuration such as admin password and Azure settings."""

    return _load_json(SERVER_CONFIG_PATH, {})


def save_server_config(data: dict[str, Any]) -> None:
    """Persist server-side configuration."""

    _save_json(SERVER_CONFIG_PATH, data)


def get_student_progress() -> pd.DataFrame:
    """Return a DataFrame of unique students with at least one attempt."""

    records = load_student_records()
    if not records:
        return pd.DataFrame(columns=["student_id", "course_code", "timestamp"])
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=["student_id", "course_code", "timestamp"])
    df = df.drop_duplicates(subset=["student_id", "course_code"])
    return df[["student_id", "course_code", "timestamp"]]


__all__ = [
    "load_cases",
    "save_cases",
    "load_student_records",
    "save_student_records",
    "load_server_config",
    "save_server_config",
    "get_student_progress",
]
