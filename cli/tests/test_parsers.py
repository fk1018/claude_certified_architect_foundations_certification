from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import pytest

from ccafc_cli.parsers import (
    build_short_practice_exams,
    parse_all_full_exams,
    parse_all_study_packs,
    parse_full_exam,
    parse_study_pack_questions,
)
from ccafc_cli.paths import PRACTICE_EXAMS_DIR


def test_full_exams_parse_all_questions() -> None:
    exams = parse_all_full_exams()

    assert len(exams) == 12
    assert [exam.id for exam in exams] == [
        *(f"practice-exam-{number}" for number in range(1, 11)),
        "practice-exam-13",
        "practice-exam-14",
    ]
    for exam in exams:
        assert exam.time_limit_minutes == 120
        assert exam.total_questions == 60
        assert exam.passing_score == 45
        assert len(exam.questions) == 60
        assert all(question.correct_choices for question in exam.questions)
        assert all(
            set(question.correct_choices) <= {"A", "B", "C", "D"}
            for question in exam.questions
        )
        assert all(question.selection_count == len(question.correct_choices) for question in exam.questions)
        assert all(len(question.choices) == 4 for question in exam.questions)


def test_full_exam_answer_explanations_attach() -> None:
    exam = parse_full_exam(PRACTICE_EXAMS_DIR / "practice-exam-1.md")
    first = exam.questions[0]

    assert first.correct_choices == ["B"]
    assert first.selection_count == 1
    assert "stop_reason" in first.explanation


def test_short_exams_are_derived_from_ordered_scenario_sections() -> None:
    full_exams = parse_all_full_exams()
    short_exams = build_short_practice_exams(full_exams)

    assert len(short_exams) == 48
    assert [exam.id for exam in short_exams] == [
        f"short-practice-exam-{number}" for number in range(1, 49)
    ]
    assert [exam.source_exam_id for exam in short_exams[:8]] == [
        *(["practice-exam-1"] * 4),
        *(["practice-exam-2"] * 4),
    ]
    assert [exam.source_exam_id for exam in short_exams[40:44]] == ["practice-exam-13"] * 4
    assert [exam.source_exam_id for exam in short_exams[44:48]] == ["practice-exam-14"] * 4

    full_by_id = {exam.id: exam for exam in full_exams}
    for short_exam in short_exams:
        assert short_exam.time_limit_minutes == 30
        assert short_exam.passing_score == 12
        assert short_exam.total_questions == 15
        assert short_exam.domain_distribution == []
        assert [question.number for question in short_exam.questions] == list(range(1, 16))
        assert all("(Questions" not in question.scenario for question in short_exam.questions)

        source_exam = full_by_id[short_exam.source_exam_id]
        start = (int(short_exam.source_section_index) - 1) * 15
        source_questions = source_exam.questions[start : start + 15]
        for local_number, (question, source_question) in enumerate(
            zip(short_exam.questions, source_questions, strict=True),
            start=1,
        ):
            assert question.id == f"{short_exam.id}:question:{local_number}"
            assert question.source_question_id == source_question.id
            assert question.source_question_number == source_question.number
            assert question.prompt == source_question.prompt
            assert question.choices == source_question.choices
            assert question.correct_choices == source_question.correct_choices
            assert question.explanation == source_question.explanation
            assert question.scenario_context == source_question.scenario_context


def test_short_exam_generation_rejects_incomplete_scenario_sections() -> None:
    full_exam = parse_full_exam(PRACTICE_EXAMS_DIR / "practice-exam-1.md")
    full_exam.questions = full_exam.questions[:-1]

    with pytest.raises(ValueError, match="section 4 must contain exactly 15 questions"):
        build_short_practice_exams([full_exam])


@pytest.mark.parametrize(
    ("exam_number", "expected_focus_counts"),
    [
        (
            13,
            {
                "CFG": 8,
                "MCP": 6,
                "DEC": 8,
                "EXT": 8,
                "REF": 6,
                "EXP": 6,
                "DESC": 5,
                "RES": 4,
                "REV": 4,
                "ERR": 5,
            },
        ),
        (
            14,
            {
                "CFG": 6,
                "MCP": 6,
                "DEC": 8,
                "EXT": 11,
                "REF": 6,
                "EXP": 3,
                "DESC": 5,
                "RES": 4,
                "REV": 6,
                "ERR": 5,
            },
        ),
    ],
)
def test_targeted_exams_are_single_answer_and_balanced(
    exam_number: int,
    expected_focus_counts: dict[str, int],
) -> None:
    path = PRACTICE_EXAMS_DIR / f"practice-exam-{exam_number}.md"
    exam = parse_full_exam(path)

    assert all(question.selection_count == 1 for question in exam.questions)
    assert Counter(question.correct_choices[0] for question in exam.questions) == {
        "A": 15,
        "B": 15,
        "C": 15,
        "D": 15,
    }
    assert set(Counter(question.scenario for question in exam.questions).values()) == {15}
    assert len({question.scenario for question in exam.questions}) == 4

    for question in exam.questions:
        lengths = {
            choice["letter"]: len(re.findall(r"\b\w+\b", choice["text"]))
            for choice in question.choices
        }
        correct = question.correct_choices[0]
        assert max(length for letter, length in lengths.items() if letter != correct) >= lengths[correct]

    focus_key = re.search(r"(?m)^\*\*Focus key:\*\*\s*(.+)$", path.read_text(encoding="utf-8"))
    assert focus_key is not None
    focus_entries = re.findall(r"(\d+)-(CFG|MCP|DEC|EXT|REF|EXP|DESC|RES|REV|ERR)", focus_key.group(1))
    assert {int(number) for number, _ in focus_entries} == set(range(1, 61))
    assert Counter(code for _, code in focus_entries) == expected_focus_counts


def test_full_exam_requires_selection_instruction_for_multiple_answers(tmp_path: Path) -> None:
    path = tmp_path / "invalid-mixed-exam.md"
    path.write_text(
        """# Invalid Mixed Exam

| Questions | 1 |
| Time limit | 120 minutes |
| Passing proxy | aim for **≥ 1 / 1** |

## Scenario A: Test

**Question 1.** Which two?

- A) One
- B) Two
- C) Three
- D) Four

# Answer Key

**Quick key:** 1-A+B

**1. A+B** — Explanation.
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="no selection-count instruction"):
        parse_full_exam(path)


def test_study_pack_multiple_response_format(tmp_path: Path) -> None:
    path = tmp_path / "practice_questions.md"
    path.write_text(
        """# Test Questions

## Question 1

Scenario: A production system needs two safeguards.

Question: Which safeguards are required? Select TWO responses.

A. First safeguard

B. Weak alternative

C. Second safeguard

D. Weak alternative

Correct answers: A, C

Explanation: Both safeguards are required.

Distractors:

- B: It is weaker.
- D: It is weaker.
""",
        encoding="utf-8",
    )

    question = parse_study_pack_questions(path, "test-pack")[0]
    assert question.correct_choices == ["A", "C"]
    assert question.selection_count == 2


def test_study_packs_parse_current_markdown() -> None:
    packs = parse_all_study_packs()

    assert len(packs) >= 8
    pack_ids = {pack.id for pack in packs}
    assert "claude-101" in pack_ids

    claude_101 = next(pack for pack in packs if pack.id == "claude-101")
    assert claude_101.title == "Claude 101"
    assert len(claude_101.notes_sections) >= 8
    assert len(claude_101.flashcards) >= 30
    assert len(claude_101.practice_questions) == 10
    assert claude_101.practice_questions[0].correct_choices == ["B"]
