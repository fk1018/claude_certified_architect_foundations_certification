from __future__ import annotations

import io
import json
from datetime import datetime, timedelta, timezone

import pytest
from rich.console import Console

from ccafc_cli import flows
from ccafc_cli.flows import (
    _print_review_feedback,
    _prompt_for_answer,
    answer_differences,
    answer_is_correct,
    correct_choices_for,
    format_answer,
    missed_questions_for,
    normalize_answer,
    review_exam_attempt,
    start_quiz,
    validate_selection_count,
)


MULTIPLE_RESPONSE_QUESTION = {
    "number": 1,
    "prompt": "Choose the first and third responses.",
    "correct_choices": ["A", "C"],
    "selection_count": 2,
    "choices": [
        {"letter": "A", "text": "First"},
        {"letter": "B", "text": "Second"},
        {"letter": "C", "text": "Third"},
        {"letter": "D", "text": "Fourth"},
    ],
    "explanation": "The first and third responses are required.",
}


def test_normalize_answer_is_ordered_and_deduplicated() -> None:
    assert normalize_answer(["C", "A", "C"]) == ["A", "C"]
    assert normalize_answer("C+A") == ["A", "C"]


def test_multiple_response_scoring_requires_exact_set() -> None:
    assert answer_is_correct(MULTIPLE_RESPONSE_QUESTION, ["C", "A"])
    assert not answer_is_correct(MULTIPLE_RESPONSE_QUESTION, ["A"])
    assert not answer_is_correct(MULTIPLE_RESPONSE_QUESTION, ["A", "B", "C"])


def test_multiple_response_feedback_identifies_missing_and_extra() -> None:
    missing, extra = answer_differences(MULTIPLE_RESPONSE_QUESTION, ["A", "B"])

    assert missing == ["C"]
    assert extra == ["B"]
    assert format_answer(["C", "A"]) == "A, C"


def test_multiple_response_selection_count_is_enforced() -> None:
    assert validate_selection_count(["A", "C"], 2) is True
    assert validate_selection_count(["A"], 2) == "Select exactly 2 responses."
    assert validate_selection_count(["A", "B", "C"], 2) == "Select exactly 2 responses."


def test_multiple_response_prompt_restores_prior_selections(monkeypatch) -> None:
    class Prompt:
        def ask(self):
            return ["C", "A"]

    def fake_checkbox(message, choices, instruction, validate):
        assert message == "Your answers"
        assert instruction
        assert [choice["value"] for choice in choices if choice["checked"]] == ["A", "C"]
        assert validate(["A"]) == "Select exactly 2 responses."
        assert validate(["A", "C"]) is True
        return Prompt()

    monkeypatch.setattr(flows.questionary, "checkbox", fake_checkbox)

    assert _prompt_for_answer(MULTIPLE_RESPONSE_QUESTION, ["C", "A"]) == ["A", "C"]


def test_exam_attempt_clears_between_questions_and_before_results(monkeypatch) -> None:
    questions = [_question(1, ["A"]), _question(2, ["B"])]
    exam = {
        "id": "practice-exam-1",
        "title": "Practice Exam 1",
        "questions": questions,
        "time_limit_minutes": 90,
    }
    progress = {
        "active_exam": {
            "exam_id": exam["id"],
            "deadline": (datetime.now(timezone.utc) + timedelta(minutes=90)).isoformat(),
            "answers": {},
            "question_index": 0,
        }
    }
    events = []

    def ask_question(question, position, total, deadline, previous_answer=None):
        assert total == 2
        assert previous_answer is None
        events.append(f"question-{position}")
        return correct_choices_for(question)

    monkeypatch.setattr(flows, "_ask_question", ask_question)
    monkeypatch.setattr(flows, "save_progress", lambda _: events.append("save"))
    monkeypatch.setattr(flows.console, "clear", lambda: events.append("clear"))
    monkeypatch.setattr(flows, "_submit_exam", lambda exam, progress: events.append("results"))

    flows._run_exam_attempt(exam, progress)

    assert events == [
        "question-1",
        "save",
        "clear",
        "question-2",
        "save",
        "clear",
        "results",
    ]


def test_exam_timeout_shows_notice_after_clearing_question_view(monkeypatch) -> None:
    exam = {
        "id": "practice-exam-1",
        "title": "Practice Exam 1",
        "questions": [_question(1, ["A"])],
        "time_limit_minutes": 90,
    }
    progress = {
        "active_exam": {
            "exam_id": exam["id"],
            "deadline": datetime.now(timezone.utc).isoformat(),
            "answers": {},
            "question_index": 0,
        }
    }
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False, color_system=None, width=160)
    clears = []
    submissions = []

    def submit_exam(exam, progress):
        assert "Time expired. Submitting your attempt." in output.getvalue()
        submissions.append(exam["id"])

    monkeypatch.setattr(flows, "console", test_console)
    monkeypatch.setattr(test_console, "clear", lambda: clears.append(True))
    monkeypatch.setattr(flows, "_seconds_remaining", lambda deadline: 0)
    monkeypatch.setattr(
        flows,
        "_ask_question",
        lambda *args, **kwargs: pytest.fail("An expired exam must not show a question"),
    )
    monkeypatch.setattr(flows, "_submit_exam", submit_exam)

    flows._run_exam_attempt(exam, progress)

    assert clears == [True]
    assert submissions == [exam["id"]]


def test_study_pack_quiz_clears_between_questions_and_before_results(monkeypatch) -> None:
    questions = [_question(1, ["A"]), _question(2, ["B"])]
    pack = {
        "id": "sample-pack",
        "title": "Sample Pack",
        "practice_questions": questions,
    }
    events = []

    def ask_question(question, position, total):
        assert total == 2
        events.append(f"question-{position}")
        return correct_choices_for(question)

    monkeypatch.setattr(flows, "load_study_packs", lambda: [pack])
    monkeypatch.setattr(flows, "_ask_quiz_question", ask_question)
    monkeypatch.setattr(flows.console, "clear", lambda: events.append("clear"))
    monkeypatch.setattr(
        flows,
        "_print_missed_questions",
        lambda questions, answers: events.append("results"),
    )

    start_quiz(pack_id=pack["id"])

    assert events == [
        "question-1",
        "clear",
        "question-2",
        "clear",
        "results",
    ]


def test_legacy_single_answer_question_remains_supported() -> None:
    assert answer_is_correct({"correct_choice": "B"}, "B")
    assert not answer_is_correct({"correct_choice": "B"}, "A")


def test_missed_questions_for_uses_exact_match_scoring() -> None:
    questions = [
        _question(1, ["A"]),
        _question(2, ["B"]),
        _question(3, ["A", "C"]),
    ]
    answers = {"1": ["B"], "2": ["B"], "3": ["A", "B"]}

    assert [question["number"] for question in missed_questions_for(questions, answers)] == [1, 3]


def test_review_attempt_selects_newest_first_and_never_saves(monkeypatch) -> None:
    questions = [
        _question(1, ["A"], scenario="Scenario A", context="Shared scenario context."),
        _question(2, ["B"], scenario="Scenario A", context="Shared scenario context."),
        _question(3, ["A", "C"], scenario="Scenario B", context="Another scenario."),
    ]
    progress = {
        "exam_attempts": [
            {
                "exam_id": "practice-exam-1",
                "submitted_at": "2026-07-01T12:00:00+00:00",
                "score": 1,
                "total": 3,
                "passed": False,
                "answers": {"1": ["B"], "2": ["B"], "3": ["A", "B"]},
            },
            {
                "exam_id": "practice-exam-1",
                "submitted_at": "2026-07-02T12:00:00+00:00",
                "score": 3,
                "total": 3,
                "passed": True,
                "answers": {"1": ["A"], "2": ["B"], "3": ["A", "C"]},
            },
        ]
    }
    original_progress = json.dumps(progress, sort_keys=True)
    exam = {"id": "practice-exam-1", "title": "Practice Exam 1", "questions": questions}
    prompted_questions = []
    feedback = []
    pauses = []
    retry_answers = iter([["A"], ["A", "C"]])
    output = io.StringIO()

    def choose_attempt(message, choices):
        assert message == "Choose an exam attempt to review"
        assert [choice["value"] for choice in choices] == [2, 1]
        assert choices[0]["name"].startswith("#2 - Practice Exam 1")
        return 1

    def prompt_for_answer(question, previous_answer=None):
        assert previous_answer is None
        prompted_questions.append(question["number"])
        return next(retry_answers)

    def record_feedback(question, original_answer, retry_answer):
        feedback.append((question["number"], original_answer, retry_answer))

    monkeypatch.setattr(flows, "load_progress", lambda: progress)
    monkeypatch.setattr(flows, "load_practice_exams", lambda: [exam])
    monkeypatch.setattr(flows, "select_one", choose_attempt)
    monkeypatch.setattr(flows, "_prompt_for_answer", prompt_for_answer)
    monkeypatch.setattr(flows, "_print_review_feedback", record_feedback)
    monkeypatch.setattr(flows, "pause", lambda message: pauses.append(message))
    monkeypatch.setattr(
        flows,
        "save_progress",
        lambda _: pytest.fail("Review must not save progress"),
    )
    monkeypatch.setattr(
        flows,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=160),
    )

    review_exam_attempt()

    assert prompted_questions == [1, 3]
    assert feedback == [
        (1, ["B"], ["A"]),
        (3, ["A", "B"], ["A", "C"]),
    ]
    assert pauses == ["Continue"]
    assert output.getvalue().count("Shared scenario context.") == 1
    assert output.getvalue().count("Another scenario.") == 1
    assert "Review complete: revisited 2 missed questions." in output.getvalue()
    assert json.dumps(progress, sort_keys=True) == original_progress


def test_review_feedback_reveals_answers_choices_and_multi_response_gaps(monkeypatch) -> None:
    output = io.StringIO()
    monkeypatch.setattr(
        flows,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=160),
    )

    _print_review_feedback(MULTIPLE_RESPONSE_QUESTION, ["A", "B"], ["A", "D"])

    rendered = output.getvalue()
    assert "Not quite." in rendered
    assert "Original answer: A, B" in rendered
    assert "Retry answer: A, D" in rendered
    assert "Correct answer: A, C" in rendered
    assert "Retry missing: C" in rendered
    assert "Retry extra: D" in rendered
    assert "original, retry, correct" in rendered
    assert "The first and third responses are required." in rendered


def test_review_attempt_handles_empty_perfect_invalid_and_missing_exam(monkeypatch) -> None:
    output = io.StringIO()
    monkeypatch.setattr(
        flows,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=160),
    )

    monkeypatch.setattr(flows, "load_progress", lambda: {"exam_attempts": []})
    review_exam_attempt()
    assert "No completed exam attempts yet." in output.getvalue()

    output.seek(0)
    output.truncate(0)
    perfect = {
        "exam_id": "practice-exam-1",
        "score": 1,
        "total": 1,
        "passed": True,
        "answers": {"1": ["A"]},
    }
    monkeypatch.setattr(flows, "load_progress", lambda: {"exam_attempts": [perfect]})
    monkeypatch.setattr(
        flows,
        "load_practice_exams",
        lambda: [{"id": "practice-exam-1", "title": "Exam", "questions": [_question(1, ["A"])]}],
    )
    review_exam_attempt(attempt_number=1)
    assert "Attempt #1 has no missed questions." in output.getvalue()

    output.seek(0)
    output.truncate(0)
    with pytest.raises(SystemExit) as exc_info:
        review_exam_attempt(attempt_number=2)
    assert exc_info.value.code == 1
    assert "Unknown attempt number: 2" in output.getvalue()

    output.seek(0)
    output.truncate(0)
    monkeypatch.setattr(flows, "load_practice_exams", lambda: [])
    review_exam_attempt(attempt_number=1)
    assert "Cannot review attempt #1" in output.getvalue()


def test_review_attempt_stops_cleanly_on_interrupt(monkeypatch) -> None:
    attempt = {
        "exam_id": "practice-exam-1",
        "score": 0,
        "total": 1,
        "passed": False,
        "answers": {"1": ["B"]},
    }
    exam = {
        "id": "practice-exam-1",
        "title": "Exam",
        "questions": [_question(1, ["A"])],
    }
    output = io.StringIO()

    monkeypatch.setattr(flows, "load_progress", lambda: {"exam_attempts": [attempt]})
    monkeypatch.setattr(flows, "load_practice_exams", lambda: [exam])
    monkeypatch.setattr(
        flows,
        "_prompt_for_answer",
        lambda question: (_ for _ in ()).throw(KeyboardInterrupt),
    )
    monkeypatch.setattr(
        flows,
        "save_progress",
        lambda _: pytest.fail("Review must not save progress"),
    )
    monkeypatch.setattr(
        flows,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=160),
    )

    review_exam_attempt(attempt_number=1)

    assert "Review stopped. No review answers were saved." in output.getvalue()


def test_short_attempt_confirms_correct_and_explains_wrong_answers(monkeypatch) -> None:
    questions = [_question(1, ["A"]), _question(2, ["A", "C"])]
    exam = _short_exam(questions)
    progress = {
        "active_short_exam": {
            "exam_id": exam["id"],
            "started_at": datetime.now(timezone.utc).isoformat(),
            "deadline": (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat(),
            "answers": {},
            "question_index": 0,
            "pending_feedback": None,
        }
    }
    answers = iter([["A"], ["A", "B"]])
    pauses = []
    saved_states = []
    submissions = []
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False, color_system=None, width=160)

    monkeypatch.setattr(flows, "console", test_console)
    monkeypatch.setattr(test_console, "clear", lambda: None)
    monkeypatch.setattr(flows, "_ask_question", lambda *args, **kwargs: next(answers))
    monkeypatch.setattr(flows, "pause", lambda message: pauses.append(message))
    monkeypatch.setattr(
        flows,
        "save_progress",
        lambda value: saved_states.append(json.loads(json.dumps(value))),
    )
    monkeypatch.setattr(
        flows,
        "_submit_short_exam",
        lambda selected_exam, value: submissions.append(selected_exam["id"]),
    )

    flows._run_short_exam_attempt(exam, progress)

    rendered = output.getvalue()
    assert "Correct." in rendered
    assert "Incorrect." in rendered
    assert "Your answer: A, B" in rendered
    assert "Correct answer: A, C" in rendered
    assert "Missing: C" in rendered
    assert "Extra: B" in rendered
    assert "Explanation 1." not in rendered
    assert "Explanation 2." in rendered
    assert pauses == ["Continue", "Continue"]
    assert submissions == [exam["id"]]
    assert progress["active_short_exam"]["question_index"] == 2
    assert progress["active_short_exam"]["pending_feedback"] is None
    assert any(
        state["active_short_exam"].get("pending_feedback")
        for state in saved_states
    )


def test_deferred_short_attempt_hides_feedback_until_submission(monkeypatch) -> None:
    questions = [_question(1, ["A"]), _question(2, ["A", "C"])]
    exam = _short_exam(questions)
    progress = {
        "active_short_exam": {
            "exam_id": exam["id"],
            "started_at": datetime.now(timezone.utc).isoformat(),
            "deadline": (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat(),
            "answers": {},
            "question_index": 0,
            "feedback_mode": "deferred",
            "pending_feedback": None,
        }
    }
    answers = iter([["A"], ["A", "B"]])
    submissions = []
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False, color_system=None, width=160)

    monkeypatch.setattr(flows, "console", test_console)
    monkeypatch.setattr(test_console, "clear", lambda: None)
    monkeypatch.setattr(flows, "_ask_question", lambda *args, **kwargs: next(answers))
    monkeypatch.setattr(
        flows,
        "pause",
        lambda *args, **kwargs: pytest.fail("Deferred feedback must not pause the exam"),
    )
    monkeypatch.setattr(flows, "save_progress", lambda value: None)
    monkeypatch.setattr(
        flows,
        "_submit_short_exam",
        lambda selected_exam, value: submissions.append(selected_exam["id"]),
    )

    flows._run_short_exam_attempt(exam, progress)

    rendered = output.getvalue()
    assert "Correct." not in rendered
    assert "Incorrect." not in rendered
    assert "Explanation 2." not in rendered
    assert "Correctness and explanations stay hidden until you submit." in rendered
    assert progress["active_short_exam"]["pending_feedback"] is None
    assert submissions == [exam["id"]]


def test_short_feedback_pause_extends_deadline_and_clears_pending(monkeypatch) -> None:
    active = {
        "deadline": "2026-08-03T12:30:00+00:00",
        "pending_feedback": {
            "question_number": 1,
            "started_at": "2026-08-03T12:10:00+00:00",
        },
    }
    progress = {"active_short_exam": active}
    saves = []
    monkeypatch.setattr(flows, "save_progress", lambda value: saves.append(value))

    flows._finish_pending_short_feedback(
        active,
        progress,
        finished_at=datetime(2026, 8, 3, 12, 14, 30, tzinfo=timezone.utc),
    )

    assert active["deadline"] == "2026-08-03T12:34:30+00:00"
    assert active["pending_feedback"] is None
    assert saves == [progress]


def test_short_attempt_interrupted_on_feedback_resumes_feedback_state(monkeypatch) -> None:
    question = _question(1, ["A"])
    exam = _short_exam([question])
    progress = {
        "active_short_exam": {
            "exam_id": exam["id"],
            "started_at": datetime.now(timezone.utc).isoformat(),
            "deadline": (datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat(),
            "answers": {"1": ["B"]},
            "question_index": 1,
            "pending_feedback": {
                "question_number": 1,
                "started_at": datetime.now(timezone.utc).isoformat(),
            },
        }
    }
    output = io.StringIO()
    test_console = Console(file=output, force_terminal=False, color_system=None, width=160)

    monkeypatch.setattr(flows, "console", test_console)
    monkeypatch.setattr(test_console, "clear", lambda: None)
    monkeypatch.setattr(
        flows,
        "pause",
        lambda message: (_ for _ in ()).throw(KeyboardInterrupt),
    )
    monkeypatch.setattr(
        flows,
        "_ask_question",
        lambda *args, **kwargs: pytest.fail("Pending feedback must be shown before another question"),
    )
    monkeypatch.setattr(
        flows,
        "_submit_short_exam",
        lambda *args, **kwargs: pytest.fail("Interrupted feedback must not submit the attempt"),
    )

    flows._run_short_exam_attempt(exam, progress)

    assert "Incorrect." in output.getvalue()
    assert "Short attempt saved." in output.getvalue()
    assert progress["active_short_exam"]["pending_feedback"] is not None


@pytest.mark.parametrize(("score", "expected_passed"), [(11, False), (12, True)])
def test_short_submission_uses_twelve_of_fifteen_and_keeps_full_state(
    score: int,
    expected_passed: bool,
    monkeypatch,
) -> None:
    questions = [_question(number, ["A"]) for number in range(1, 16)]
    exam = _short_exam(questions)
    full_active = {"exam_id": "practice-exam-1", "answers": {}}
    progress = {
        "active_exam": full_active,
        "exam_attempts": [],
        "active_short_exam": {
            "exam_id": exam["id"],
            "started_at": "2026-08-03T12:00:00+00:00",
            "answers": {
                str(number): ["A"] if number <= score else ["B"]
                for number in range(1, 16)
            },
        },
        "short_exam_attempts": [],
    }
    monkeypatch.setattr(flows, "save_progress", lambda value: None)
    monkeypatch.setattr(flows, "_print_missed_questions", lambda questions, answers: None)

    flows._submit_short_exam(exam, progress)

    attempt = progress["short_exam_attempts"][0]
    assert attempt["score"] == score
    assert attempt["passing_score"] == 12
    assert attempt["passed"] is expected_passed
    assert progress["active_short_exam"] is None
    assert progress["active_exam"] is full_active
    assert progress["exam_attempts"] == []


def test_start_short_exam_ignores_active_full_exam(monkeypatch) -> None:
    exam = _short_exam([_question(1, ["A"])])
    full_active = {"exam_id": "practice-exam-1", "answers": {}}
    progress = {
        "active_exam": full_active,
        "active_short_exam": None,
        "short_exam_attempts": [],
    }
    runs = []

    monkeypatch.setattr(flows, "load_short_practice_exams", lambda: [exam])
    monkeypatch.setattr(flows, "load_progress", lambda: progress)
    monkeypatch.setattr(flows, "save_progress", lambda value: None)
    monkeypatch.setattr(
        flows,
        "choose_short_exam_feedback_mode",
        lambda: flows.ShortExamFeedbackMode.DEFERRED,
    )
    monkeypatch.setattr(
        flows,
        "confirm",
        lambda *args, **kwargs: pytest.fail("An active full exam must not block a short exam"),
    )
    monkeypatch.setattr(
        flows,
        "_run_short_exam_attempt",
        lambda selected_exam, value: runs.append(selected_exam["id"]),
    )

    flows.start_short_exam(exam_id=exam["id"])

    assert runs == [exam["id"]]
    assert progress["active_exam"] is full_active
    assert progress["active_short_exam"]["exam_id"] == exam["id"]
    assert progress["active_short_exam"]["feedback_mode"] == "deferred"


def test_start_short_exam_explicit_feedback_mode_skips_prompt(monkeypatch) -> None:
    exam = _short_exam([_question(1, ["A"])])
    progress = {"active_short_exam": None, "short_exam_attempts": []}

    monkeypatch.setattr(flows, "load_short_practice_exams", lambda: [exam])
    monkeypatch.setattr(flows, "load_progress", lambda: progress)
    monkeypatch.setattr(flows, "save_progress", lambda value: None)
    monkeypatch.setattr(
        flows,
        "choose_short_exam_feedback_mode",
        lambda: pytest.fail("An explicit feedback mode must bypass the prompt"),
    )
    monkeypatch.setattr(flows, "_run_short_exam_attempt", lambda *args: None)

    flows.start_short_exam(exam_id=exam["id"], feedback_mode="immediate")

    assert progress["active_short_exam"]["feedback_mode"] == "immediate"


def test_short_review_reads_only_short_attempt_history(monkeypatch) -> None:
    output = io.StringIO()
    monkeypatch.setattr(
        flows,
        "console",
        Console(file=output, force_terminal=False, color_system=None, width=160),
    )
    monkeypatch.setattr(
        flows,
        "load_progress",
        lambda: {"exam_attempts": [{"exam_id": "practice-exam-1"}], "short_exam_attempts": []},
    )
    monkeypatch.setattr(
        flows,
        "load_short_practice_exams",
        lambda: pytest.fail("An empty short history must return before loading exams"),
    )

    flows.review_short_exam_attempt()

    assert "No completed short exam attempts yet." in output.getvalue()


def _question(
    number: int,
    correct_choices: list[str],
    scenario: str = "",
    context: str = "",
) -> dict:
    return {
        "number": number,
        "prompt": f"Question {number}?",
        "correct_choices": correct_choices,
        "selection_count": len(correct_choices),
        "choices": [
            {"letter": "A", "text": "First"},
            {"letter": "B", "text": "Second"},
            {"letter": "C", "text": "Third"},
            {"letter": "D", "text": "Fourth"},
        ],
        "explanation": f"Explanation {number}.",
        "scenario": scenario,
        "scenario_context": context,
    }


def _short_exam(questions: list[dict]) -> dict:
    return {
        "id": "short-practice-exam-1",
        "title": "CCAFC Short Practice Exam 1",
        "source_exam_id": "practice-exam-1",
        "source_exam_title": "CCAFC Practice Exam 1",
        "questions": questions,
        "time_limit_minutes": 30,
        "passing_score": 12,
        "total_questions": 15,
    }
