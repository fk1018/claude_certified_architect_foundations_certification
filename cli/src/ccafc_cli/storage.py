from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ccafc_cli.parsers import build_short_practice_exams, parse_all_full_exams, parse_all_study_packs
from ccafc_cli.paths import GENERATED_DIR, PRACTICE_EXAMS_JSON, PROGRESS_PATH, STATE_DIR, STUDY_PACKS_JSON


GENERATED_SCHEMA_VERSION = 3
PROGRESS_SCHEMA_VERSION = 3


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def generate_data() -> dict[str, int]:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    study_packs = [pack.to_dict() for pack in parse_all_study_packs()]
    parsed_practice_exams = parse_all_full_exams()
    practice_exams = [exam.to_dict() for exam in parsed_practice_exams]
    short_practice_exams = [
        exam.to_dict() for exam in build_short_practice_exams(parsed_practice_exams)
    ]

    write_json(
        STUDY_PACKS_JSON,
        {
            "schema_version": GENERATED_SCHEMA_VERSION,
            "generated_at": now_iso(),
            "study_packs": study_packs,
        },
    )
    write_json(
        PRACTICE_EXAMS_JSON,
        {
            "schema_version": GENERATED_SCHEMA_VERSION,
            "generated_at": now_iso(),
            "practice_exams": practice_exams,
            "short_practice_exams": short_practice_exams,
        },
    )

    return {
        "study_packs": len(study_packs),
        "practice_exams": len(practice_exams),
        "short_practice_exams": len(short_practice_exams),
        "flashcards": sum(len(pack["flashcards"]) for pack in study_packs),
        "study_pack_questions": sum(len(pack["practice_questions"]) for pack in study_packs),
        "full_exam_questions": sum(len(exam["questions"]) for exam in practice_exams),
        "short_exam_questions": sum(len(exam["questions"]) for exam in short_practice_exams),
    }


def ensure_generated_data() -> None:
    if not STUDY_PACKS_JSON.exists() or not PRACTICE_EXAMS_JSON.exists():
        generate_data()
        return
    study_data = read_json(STUDY_PACKS_JSON, {})
    exam_data = read_json(PRACTICE_EXAMS_JSON, {})
    if (
        study_data.get("schema_version") != GENERATED_SCHEMA_VERSION
        or exam_data.get("schema_version") != GENERATED_SCHEMA_VERSION
    ):
        generate_data()


def load_study_packs() -> list[dict[str, Any]]:
    ensure_generated_data()
    return read_json(STUDY_PACKS_JSON, {"study_packs": []})["study_packs"]


def load_practice_exams() -> list[dict[str, Any]]:
    ensure_generated_data()
    return read_json(PRACTICE_EXAMS_JSON, {"practice_exams": []})["practice_exams"]


def load_short_practice_exams() -> list[dict[str, Any]]:
    ensure_generated_data()
    return read_json(PRACTICE_EXAMS_JSON, {"short_practice_exams": []})[
        "short_practice_exams"
    ]


def default_progress() -> dict[str, Any]:
    return {
        "schema_version": PROGRESS_SCHEMA_VERSION,
        "active_exam": None,
        "active_short_exam": None,
        "exam_attempts": [],
        "short_exam_attempts": [],
        "flashcards": {},
        "notes": {"last_opened": {}},
    }


def load_progress() -> dict[str, Any]:
    progress = default_progress()
    saved = read_json(PROGRESS_PATH, {})
    progress.update(saved)
    _migrate_progress_answers(progress)
    progress["schema_version"] = PROGRESS_SCHEMA_VERSION
    progress.setdefault("notes", {}).setdefault("last_opened", {})
    progress.setdefault("flashcards", {})
    progress.setdefault("exam_attempts", [])
    progress.setdefault("active_short_exam", None)
    progress.setdefault("short_exam_attempts", [])
    return progress


def save_progress(progress: dict[str, Any]) -> None:
    progress["schema_version"] = PROGRESS_SCHEMA_VERSION
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    write_json(PROGRESS_PATH, progress)


def _migrate_progress_answers(progress: dict[str, Any]) -> None:
    for active_key in ("active_exam", "active_short_exam"):
        active = progress.get(active_key)
        if isinstance(active, dict):
            active["answers"] = _normalize_answer_map(active.get("answers", {}))
    for attempts_key in ("exam_attempts", "short_exam_attempts"):
        for attempt in progress.get(attempts_key) or []:
            if isinstance(attempt, dict):
                attempt["answers"] = _normalize_answer_map(attempt.get("answers", {}))


def _normalize_answer_map(answers: Any) -> dict[str, list[str]]:
    if not isinstance(answers, dict):
        return {}
    return {str(number): _normalize_saved_answer(answer) for number, answer in answers.items()}


def _normalize_saved_answer(answer: Any) -> list[str]:
    if isinstance(answer, str):
        values = answer.replace("+", ",").split(",")
    elif isinstance(answer, list):
        values = answer
    else:
        values = []
    letters = {
        str(value).strip().upper()
        for value in values
        if str(value).strip().upper() in {"A", "B", "C", "D"}
    }
    return [letter for letter in ("A", "B", "C", "D") if letter in letters]
