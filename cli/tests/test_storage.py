from __future__ import annotations

import json
from pathlib import Path

from ccafc_cli.paths import PRACTICE_EXAMS_JSON, STUDY_PACKS_JSON
from ccafc_cli import storage
from ccafc_cli.storage import GENERATED_SCHEMA_VERSION, PROGRESS_SCHEMA_VERSION, generate_data


def test_generate_data_writes_json() -> None:
    summary = generate_data()

    assert summary["practice_exams"] == 12
    assert summary["short_practice_exams"] == 48
    assert summary["full_exam_questions"] == 720
    assert summary["short_exam_questions"] == 720
    assert summary["study_packs"] >= 8
    assert STUDY_PACKS_JSON.exists()
    assert PRACTICE_EXAMS_JSON.exists()

    study_packs = json.loads(STUDY_PACKS_JSON.read_text(encoding="utf-8"))
    practice_exams = json.loads(PRACTICE_EXAMS_JSON.read_text(encoding="utf-8"))
    assert study_packs["schema_version"] == GENERATED_SCHEMA_VERSION
    assert practice_exams["schema_version"] == GENERATED_SCHEMA_VERSION
    assert study_packs["study_packs"]
    assert practice_exams["practice_exams"]
    assert len(practice_exams["short_practice_exams"]) == 48
    first_short = practice_exams["short_practice_exams"][0]
    assert first_short["id"] == "short-practice-exam-1"
    assert first_short["source_exam_id"] == "practice-exam-1"
    assert first_short["source_section_index"] == 1
    assert first_short["questions"][0]["number"] == 1
    assert first_short["questions"][0]["source_question_number"] == 1
    assert [exam["id"] for exam in practice_exams["practice_exams"]] == [
        *(f"practice-exam-{number}" for number in range(1, 11)),
        "practice-exam-13",
        "practice-exam-14",
    ]


def test_load_progress_migrates_legacy_answer_strings(tmp_path: Path, monkeypatch) -> None:
    progress_path = tmp_path / "progress.json"
    progress_path.write_text(
        json.dumps(
            {
                "active_exam": {
                    "exam_id": "practice-exam-1",
                    "answers": {"1": "B", "2": ["A", "C"], "3": "C+A"},
                    "question_index": 2,
                },
                "exam_attempts": [
                    {
                        "exam_id": "practice-exam-2",
                        "answers": {"1": "D"},
                    }
                ],
                "active_short_exam": {
                    "exam_id": "short-practice-exam-1",
                    "answers": {"1": "A+C"},
                    "question_index": 1,
                },
                "short_exam_attempts": [
                    {
                        "exam_id": "short-practice-exam-2",
                        "answers": {"1": "B"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(storage, "PROGRESS_PATH", progress_path)

    progress = storage.load_progress()

    assert progress["schema_version"] == PROGRESS_SCHEMA_VERSION
    assert progress["active_exam"]["answers"] == {
        "1": ["B"],
        "2": ["A", "C"],
        "3": ["A", "C"],
    }
    assert progress["exam_attempts"][0]["answers"] == {"1": ["D"]}
    assert progress["active_short_exam"]["answers"] == {"1": ["A", "C"]}
    assert progress["short_exam_attempts"][0]["answers"] == {"1": ["B"]}


def test_ensure_generated_data_rebuilds_stale_schema(tmp_path: Path, monkeypatch) -> None:
    generated_dir = tmp_path / "generated"
    study_path = generated_dir / "study_packs.json"
    exam_path = generated_dir / "practice_exams.json"
    generated_dir.mkdir()
    study_path.write_text('{"schema_version": 1, "study_packs": []}\n', encoding="utf-8")
    exam_path.write_text('{"schema_version": 1, "practice_exams": []}\n', encoding="utf-8")
    monkeypatch.setattr(storage, "GENERATED_DIR", generated_dir)
    monkeypatch.setattr(storage, "STUDY_PACKS_JSON", study_path)
    monkeypatch.setattr(storage, "PRACTICE_EXAMS_JSON", exam_path)

    storage.ensure_generated_data()

    study_data = json.loads(study_path.read_text(encoding="utf-8"))
    exam_data = json.loads(exam_path.read_text(encoding="utf-8"))
    assert study_data["schema_version"] == GENERATED_SCHEMA_VERSION
    assert exam_data["schema_version"] == GENERATED_SCHEMA_VERSION
    assert len(exam_data["practice_exams"]) == 12
    assert len(exam_data["short_practice_exams"]) == 48
