from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from typing import Any

import questionary
from rich.markdown import Markdown
from rich.table import Table

from ccafc_cli.storage import (
    load_practice_exams,
    load_progress,
    load_short_practice_exams,
    load_study_packs,
    now_iso,
    save_progress,
)
from ccafc_cli.ui import confirm, console, pause, select_one


class ShortExamFeedbackMode(StrEnum):
    IMMEDIATE = "immediate"
    DEFERRED = "deferred"


def find_by_id(items: list[dict[str, Any]], item_id: str) -> dict[str, Any] | None:
    return next((item for item in items if item["id"] == item_id), None)


def normalize_answer(answer: Any) -> list[str]:
    if isinstance(answer, str):
        values = answer.replace("+", ",").split(",")
    elif isinstance(answer, list):
        values = answer
    else:
        values = []
    selected = {
        str(value).strip().upper()
        for value in values
        if str(value).strip().upper() in {"A", "B", "C", "D"}
    }
    return [letter for letter in ("A", "B", "C", "D") if letter in selected]


def correct_choices_for(question: dict[str, Any]) -> list[str]:
    if "correct_choices" in question:
        return normalize_answer(question["correct_choices"])
    return normalize_answer(question.get("correct_choice", ""))


def answer_is_correct(question: dict[str, Any], answer: Any) -> bool:
    return normalize_answer(answer) == correct_choices_for(question)


def answer_differences(question: dict[str, Any], answer: Any) -> tuple[list[str], list[str]]:
    selected = set(normalize_answer(answer))
    correct = set(correct_choices_for(question))
    return (
        [letter for letter in ("A", "B", "C", "D") if letter in correct - selected],
        [letter for letter in ("A", "B", "C", "D") if letter in selected - correct],
    )


def format_answer(answer: Any) -> str:
    choices = normalize_answer(answer)
    return ", ".join(choices) if choices else "unanswered"


def validate_selection_count(selected: list[str], required: int) -> bool | str:
    if len(selected) == required:
        return True
    return f"Select exactly {required} responses."


def choose_study_pack(packs: list[dict[str, Any]], message: str = "Choose a study pack") -> dict[str, Any]:
    choices = [{"name": f"{pack['title']} ({pack['id']})", "value": pack["id"]} for pack in packs]
    pack_id = select_one(message, choices)
    pack = find_by_id(packs, pack_id)
    if pack is None:
        raise RuntimeError(f"Unknown study pack: {pack_id}")
    return pack


def choose_exam(exams: list[dict[str, Any]], message: str = "Choose a practice exam") -> dict[str, Any]:
    choices = [
        {
            "name": f"{exam['title']} - {len(exam['questions'])} questions, {exam['time_limit_minutes']} minutes",
            "value": exam["id"],
        }
        for exam in exams
    ]
    exam_id = select_one(message, choices)
    exam = find_by_id(exams, exam_id)
    if exam is None:
        raise RuntimeError(f"Unknown practice exam: {exam_id}")
    return exam


def choose_short_exam(
    exams: list[dict[str, Any]],
    message: str = "Choose a short practice exam",
) -> dict[str, Any]:
    choices = [
        {
            "name": (
                f"{exam['title']} - "
                f"{exam.get('source_exam_title') or exam.get('source_exam_id', 'unknown')}, "
                f"{exam['questions'][0].get('scenario', 'scenario')} - "
                f"{len(exam['questions'])} questions, {exam['time_limit_minutes']} minutes"
            ),
            "value": exam["id"],
        }
        for exam in exams
    ]
    exam_id = select_one(message, choices)
    exam = find_by_id(exams, exam_id)
    if exam is None:
        raise RuntimeError(f"Unknown short practice exam: {exam_id}")
    return exam


def choose_short_exam_feedback_mode() -> ShortExamFeedbackMode:
    value = select_one(
        "When should feedback be shown?",
        [
            {
                "name": (
                    "After each question - confirm correct answers and explain misses; "
                    "pause the timer until you continue"
                ),
                "value": ShortExamFeedbackMode.IMMEDIATE.value,
            },
            {
                "name": "At the end - hide correctness and explanations until submission",
                "value": ShortExamFeedbackMode.DEFERRED.value,
            },
        ],
    )
    return ShortExamFeedbackMode(value)


def show_exam_list() -> None:
    exams = load_practice_exams()
    table = Table(title="Practice Exams")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Questions", justify="right")
    table.add_column("Item mix", justify="right")
    table.add_column("Timer", justify="right")
    table.add_column("Pass Proxy", justify="right")
    for exam in exams:
        multiple_count = sum(1 for question in exam["questions"] if int(question.get("selection_count", 1)) > 1)
        single_count = len(exam["questions"]) - multiple_count
        table.add_row(
            exam["id"],
            exam["title"],
            str(len(exam["questions"])),
            f"{single_count} single / {multiple_count} multi",
            f"{exam['time_limit_minutes']}m",
            f"{exam['passing_score']} / {exam['total_questions']}",
        )
    console.print(table)


def show_short_exam_list() -> None:
    exams = load_short_practice_exams()
    table = Table(title="Short Practice Exams")
    table.add_column("ID", no_wrap=True)
    table.add_column("Source", no_wrap=True)
    table.add_column("Scenario")
    table.add_column("Q", justify="right", no_wrap=True)
    table.add_column("Mix", justify="right", no_wrap=True)
    table.add_column("Time", justify="right", no_wrap=True)
    table.add_column("Pass", justify="right", no_wrap=True)
    for exam in exams:
        multiple_count = sum(
            1
            for question in exam["questions"]
            if int(question.get("selection_count", 1)) > 1
        )
        single_count = len(exam["questions"]) - multiple_count
        table.add_row(
            exam["id"],
            exam.get("source_exam_id", "unknown").replace("practice-exam-", "Exam "),
            exam["questions"][0].get("scenario", ""),
            str(len(exam["questions"])),
            f"{single_count}S/{multiple_count}M",
            f"{exam['time_limit_minutes']}m",
            f"{exam['passing_score']}/{exam['total_questions']}",
        )
    console.print(table)


def start_exam(exam_id: str | None = None, force: bool = False) -> None:
    exams = load_practice_exams()
    progress = load_progress()
    active = progress.get("active_exam")

    if active and not force:
        should_resume = confirm(
            f"An active attempt for {active['exam_id']} exists. Resume it instead?",
            default=True,
        )
        if should_resume:
            resume_exam()
            return
        if not confirm("Discard the active attempt and start a new one?", default=False):
            return

    exam = find_by_id(exams, exam_id) if exam_id else choose_exam(exams)
    if exam is None:
        console.print(f"[red]Unknown exam:[/] {exam_id}")
        raise SystemExit(1)

    started_at = datetime.now(timezone.utc)
    deadline = started_at + timedelta(minutes=int(exam["time_limit_minutes"]))
    progress["active_exam"] = {
        "exam_id": exam["id"],
        "started_at": started_at.isoformat(),
        "deadline": deadline.isoformat(),
        "answers": {},
        "question_index": 0,
    }
    save_progress(progress)
    _run_exam_attempt(exam, progress)


def resume_exam() -> None:
    exams = load_practice_exams()
    progress = load_progress()
    active = progress.get("active_exam")
    if not active:
        console.print("[yellow]No active exam attempt.[/]")
        return

    exam = find_by_id(exams, active["exam_id"])
    if exam is None:
        console.print(f"[red]Active exam is missing from generated data:[/] {active['exam_id']}")
        return

    _run_exam_attempt(exam, progress)


def start_short_exam(
    exam_id: str | None = None,
    force: bool = False,
    feedback_mode: ShortExamFeedbackMode | str | None = None,
) -> None:
    exams = load_short_practice_exams()
    progress = load_progress()
    active = progress.get("active_short_exam")

    if active and not force:
        should_resume = confirm(
            f"An active short attempt for {active['exam_id']} exists. Resume it instead?",
            default=True,
        )
        if should_resume:
            resume_short_exam()
            return
        if not confirm("Discard the active short attempt and start a new one?", default=False):
            return

    exam = find_by_id(exams, exam_id) if exam_id else choose_short_exam(exams)
    if exam is None:
        console.print(f"[red]Unknown short exam:[/] {exam_id}")
        raise SystemExit(1)

    mode = (
        ShortExamFeedbackMode(feedback_mode)
        if feedback_mode is not None
        else choose_short_exam_feedback_mode()
    )

    started_at = datetime.now(timezone.utc)
    deadline = started_at + timedelta(minutes=int(exam["time_limit_minutes"]))
    progress["active_short_exam"] = {
        "exam_id": exam["id"],
        "started_at": started_at.isoformat(),
        "deadline": deadline.isoformat(),
        "answers": {},
        "question_index": 0,
        "feedback_mode": mode.value,
        "pending_feedback": None,
    }
    save_progress(progress)
    _run_short_exam_attempt(exam, progress)


def resume_short_exam() -> None:
    exams = load_short_practice_exams()
    progress = load_progress()
    active = progress.get("active_short_exam")
    if not active:
        console.print("[yellow]No active short exam attempt.[/]")
        return

    exam = find_by_id(exams, active["exam_id"])
    if exam is None:
        console.print(
            f"[red]Active short exam is missing from generated data:[/] {active['exam_id']}"
        )
        return

    _run_short_exam_attempt(exam, progress)


def show_exam_results() -> None:
    progress = load_progress()
    _show_attempt_results(
        attempts=progress.get("exam_attempts", []),
        title="Exam Attempts",
        empty_message="No completed exam attempts yet.",
    )


def show_short_exam_results() -> None:
    progress = load_progress()
    _show_attempt_results(
        attempts=progress.get("short_exam_attempts", []),
        title="Short Exam Attempts",
        empty_message="No completed short exam attempts yet.",
    )


def _show_attempt_results(
    attempts: list[dict[str, Any]],
    title: str,
    empty_message: str,
) -> None:
    if not attempts:
        console.print(f"[yellow]{empty_message}[/]")
        return

    table = Table(title=title)
    table.add_column("#", justify="right")
    table.add_column("When")
    table.add_column("Exam")
    table.add_column("Score", justify="right")
    table.add_column("Missed", justify="right")
    table.add_column("Result")
    for attempt_number, attempt in reversed(list(enumerate(attempts, start=1))):
        result = "PASS" if attempt["passed"] else "REVIEW"
        style = "green" if attempt["passed"] else "yellow"
        score = int(attempt["score"])
        total = int(attempt["total"])
        table.add_row(
            str(attempt_number),
            _format_attempt_time(attempt.get("submitted_at")),
            attempt["exam_id"],
            f"{score} / {total}",
            str(total - score),
            f"[{style}]{result}[/]",
        )
    console.print(table)


def review_exam_attempt(attempt_number: int | None = None) -> None:
    _review_attempt(
        attempt_number=attempt_number,
        attempts_key="exam_attempts",
        exam_loader=load_practice_exams,
        empty_message="No completed exam attempts yet.",
        choice_message="Choose an exam attempt to review",
        results_command="ccafc exam results",
        rule_title="Review Attempt",
    )


def review_short_exam_attempt(attempt_number: int | None = None) -> None:
    _review_attempt(
        attempt_number=attempt_number,
        attempts_key="short_exam_attempts",
        exam_loader=load_short_practice_exams,
        empty_message="No completed short exam attempts yet.",
        choice_message="Choose a short exam attempt to review",
        results_command="ccafc exam short results",
        rule_title="Review Short Attempt",
    )


def _review_attempt(
    attempt_number: int | None,
    attempts_key: str,
    exam_loader: Any,
    empty_message: str,
    choice_message: str,
    results_command: str,
    rule_title: str,
) -> None:
    progress = load_progress()
    attempts = progress.get(attempts_key, [])
    if not attempts:
        console.print(f"[yellow]{empty_message}[/]")
        return

    exams = exam_loader()
    exams_by_id = {exam["id"]: exam for exam in exams}
    selected_number = attempt_number

    if selected_number is None:
        choices = [
            {
                "name": _format_attempt_choice(number, attempt, exams_by_id),
                "value": number,
            }
            for number, attempt in reversed(list(enumerate(attempts, start=1)))
        ]
        try:
            selected_number = int(select_one(choice_message, choices))
        except KeyboardInterrupt:
            console.print("\n[yellow]Review cancelled.[/]")
            return

    if selected_number < 1 or selected_number > len(attempts):
        console.print(
            f"[red]Unknown attempt number:[/] {selected_number}. "
            f"Use `{results_command}` to list completed attempts."
        )
        raise SystemExit(1)

    attempt = attempts[selected_number - 1]
    exam = exams_by_id.get(attempt.get("exam_id"))
    if exam is None:
        console.print(
            f"[red]Cannot review attempt #{selected_number}:[/] "
            f"{attempt.get('exam_id', 'unknown exam')} is missing from generated data. "
            "Run `ccafc import` to regenerate it."
        )
        return

    answers = attempt.get("answers", {})
    missed = missed_questions_for(exam["questions"], answers)
    if not missed:
        console.print(f"[green]Attempt #{selected_number} has no missed questions.[/]")
        return

    console.rule(f"{rule_title} #{selected_number}")
    console.print(
        f"[bold]{exam['title']}[/] - "
        f"{attempt.get('score', len(exam['questions']) - len(missed))} / "
        f"{attempt.get('total', len(exam['questions']))}; "
        f"{len(missed)} missed"
    )
    console.print(
        "Retry each question before the original and correct answers are revealed. "
        "Review answers are not scored or saved."
    )

    current_scenario = None
    try:
        for position, question in enumerate(missed, start=1):
            console.rule(
                f"Missed question {position} / {len(missed)} "
                f"(exam question {question['number']})"
            )
            scenario = question.get("scenario", "")
            if scenario and scenario != current_scenario:
                console.print(Markdown(f"**{scenario}**"))
                scenario_context = question.get("scenario_context", "")
                if scenario_context:
                    console.print(Markdown(scenario_context))
                current_scenario = scenario

            console.print(Markdown(question["prompt"]))
            retry_answer = _prompt_for_answer(question)
            original_answer = answers.get(str(question["number"]), [])
            _print_review_feedback(question, original_answer, retry_answer)

            if position < len(missed):
                pause("Continue")
    except KeyboardInterrupt:
        console.print("\n[yellow]Review stopped. No review answers were saved.[/]")
        return

    console.print(f"[green]Review complete:[/] revisited {len(missed)} missed questions.")


def missed_questions_for(
    questions: list[dict[str, Any]],
    answers: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        question
        for question in questions
        if not answer_is_correct(question, answers.get(str(question["number"]), []))
    ]


def _format_attempt_choice(
    attempt_number: int,
    attempt: dict[str, Any],
    exams_by_id: dict[str, dict[str, Any]],
) -> str:
    exam_id = str(attempt.get("exam_id", "unknown exam"))
    exam = exams_by_id.get(exam_id)
    exam_name = exam["title"] if exam else exam_id
    score = attempt.get("score", "?")
    total = attempt.get("total", "?")
    if isinstance(score, int) and isinstance(total, int):
        missed = str(max(0, total - score))
    else:
        missed = "?"
    return (
        f"#{attempt_number} - {exam_name} - "
        f"{_format_attempt_time(attempt.get('submitted_at'))} - "
        f"{score}/{total} - {missed} missed"
    )


def _format_attempt_time(value: Any) -> str:
    if not isinstance(value, str) or not value:
        return "unknown time"
    try:
        submitted_at = datetime.fromisoformat(value)
    except ValueError:
        return value
    if submitted_at.tzinfo is None:
        submitted_at = submitted_at.replace(tzinfo=timezone.utc)
    return submitted_at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def _print_review_feedback(
    question: dict[str, Any],
    original_answer: Any,
    retry_answer: Any,
) -> None:
    correct = correct_choices_for(question)
    retry_correct = answer_is_correct(question, retry_answer)
    result = "[green]Correct.[/]" if retry_correct else "[yellow]Not quite.[/]"
    console.print(result)
    console.print(f"[bold]Original answer:[/] {format_answer(original_answer)}")
    console.print(f"[bold]Retry answer:[/] {format_answer(retry_answer)}")
    console.print(f"[bold]Correct answer:[/] {format_answer(correct)}")

    if int(question.get("selection_count", 1)) > 1 and not retry_correct:
        missing, extra = answer_differences(question, retry_answer)
        if missing:
            console.print(f"[yellow]Retry missing:[/] {format_answer(missing)}")
        if extra:
            console.print(f"[yellow]Retry extra:[/] {format_answer(extra)}")

    original = set(normalize_answer(original_answer))
    retry = set(normalize_answer(retry_answer))
    correct_set = set(correct)
    table = Table(show_header=True, header_style="bold")
    table.add_column("Choice", justify="center")
    table.add_column("Response")
    table.add_column("Markers")
    for choice in question["choices"]:
        letter = choice["letter"]
        markers = []
        if letter in original:
            markers.append("original")
        if letter in retry:
            markers.append("retry")
        if letter in correct_set:
            markers.append("correct")
        table.add_row(letter, Markdown(choice["text"]), ", ".join(markers))
    console.print(table)

    explanation = question.get("explanation", "")
    if explanation:
        console.print(Markdown(f"**Explanation:** {explanation}"))
    else:
        console.print("[yellow]No explanation is available for this question.[/]")


def _run_exam_attempt(exam: dict[str, Any], progress: dict[str, Any]) -> None:
    active = progress["active_exam"]
    questions = exam["questions"]
    answers: dict[str, list[str]] = active.setdefault("answers", {})
    index = int(active.get("question_index", 0))
    questions_shown = 0
    timed_out = False

    console.print(f"[bold]{exam['title']}[/] ({len(questions)} questions, {exam['time_limit_minutes']} minutes)")
    multiple_count = sum(1 for question in questions if int(question.get("selection_count", 1)) > 1)
    if multiple_count:
        console.print(
            f"{multiple_count} multiple-response items use exact-match scoring and state the required selection count."
        )
    console.print("Answers are saved after every question. Ctrl+C exits; use `ccafc exam resume` to continue.")

    try:
        while index < len(questions):
            if _seconds_remaining(active["deadline"]) <= 0:
                timed_out = True
                break

            if questions_shown:
                console.clear()

            question = questions[index]
            answer = _ask_question(question, index + 1, len(questions), active["deadline"], answers.get(str(question["number"])))
            answers[str(question["number"])] = answer
            index += 1
            questions_shown += 1
            active["question_index"] = index
            save_progress(progress)
    except KeyboardInterrupt:
        console.print("\n[yellow]Attempt saved.[/]")
        return

    console.clear()
    if timed_out:
        console.print("[red]Time expired. Submitting your attempt.[/]")
    _submit_exam(exam, progress)


def _run_short_exam_attempt(exam: dict[str, Any], progress: dict[str, Any]) -> None:
    active = progress["active_short_exam"]
    feedback_mode = ShortExamFeedbackMode(
        active.get("feedback_mode", ShortExamFeedbackMode.IMMEDIATE.value)
    )
    immediate_feedback = feedback_mode is ShortExamFeedbackMode.IMMEDIATE
    questions = exam["questions"]
    answers: dict[str, list[str]] = active.setdefault("answers", {})
    index = int(active.get("question_index", 0))
    questions_shown = 0
    timed_out = False

    console.print(
        f"[bold]{exam['title']}[/] "
        f"({len(questions)} questions, {exam['time_limit_minutes']} minutes)"
    )
    console.print(
        f"Source: {exam.get('source_exam_title', exam.get('source_exam_id', 'unknown'))} - "
        f"{questions[0].get('scenario', 'scenario')}"
    )
    multiple_count = sum(
        1 for question in questions if int(question.get("selection_count", 1)) > 1
    )
    if multiple_count:
        console.print(
            f"{multiple_count} multiple-response items use exact-match scoring and state "
            "the required selection count."
        )
    if immediate_feedback:
        console.print(
            "Feedback follows every answer; missed answers include an explanation. "
            "The timer pauses until you continue."
        )
    else:
        console.print("Correctness and explanations stay hidden until you submit.")
    console.print(
        "Answers are saved after every question. Ctrl+C exits; "
        "use `ccafc exam short resume` to continue."
    )

    try:
        if immediate_feedback and active.get("pending_feedback"):
            _show_pending_short_feedback(exam, progress)
            console.clear()

        while index < len(questions):
            if _seconds_remaining(active["deadline"]) <= 0:
                timed_out = True
                break

            if questions_shown:
                console.clear()

            question = questions[index]
            answer = _ask_question(
                question,
                index + 1,
                len(questions),
                active["deadline"],
                answers.get(str(question["number"])),
            )
            answers[str(question["number"])] = answer
            index += 1
            questions_shown += 1
            active["question_index"] = index

            if immediate_feedback:
                active["pending_feedback"] = {
                    "question_number": question["number"],
                    "started_at": now_iso(),
                }
            save_progress(progress)

            if immediate_feedback and active.get("pending_feedback"):
                console.clear()
                _show_pending_short_feedback(exam, progress)
    except KeyboardInterrupt:
        console.print("\n[yellow]Short attempt saved.[/]")
        return

    console.clear()
    if timed_out:
        console.print("[red]Time expired. Submitting your short attempt.[/]")
    _submit_short_exam(exam, progress)


def _show_pending_short_feedback(
    exam: dict[str, Any],
    progress: dict[str, Any],
) -> None:
    active = progress["active_short_exam"]
    pending = active.get("pending_feedback")
    if not isinstance(pending, dict):
        return

    question_number = int(pending.get("question_number", 0))
    question = next(
        (item for item in exam["questions"] if int(item["number"]) == question_number),
        None,
    )
    if question is None:
        active["pending_feedback"] = None
        save_progress(progress)
        return

    answer = active.get("answers", {}).get(str(question_number), [])
    _print_short_answer_feedback(question, answer)
    pause("Continue")
    _finish_pending_short_feedback(active, progress)


def _finish_pending_short_feedback(
    active: dict[str, Any],
    progress: dict[str, Any],
    finished_at: datetime | None = None,
) -> None:
    pending = active.get("pending_feedback")
    if not isinstance(pending, dict):
        return

    started_at = datetime.fromisoformat(str(pending["started_at"]))
    deadline = datetime.fromisoformat(str(active["deadline"]))
    if started_at.tzinfo is None:
        started_at = started_at.replace(tzinfo=timezone.utc)
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    feedback_finished_at = finished_at or datetime.now(timezone.utc)
    if feedback_finished_at.tzinfo is None:
        feedback_finished_at = feedback_finished_at.replace(tzinfo=timezone.utc)
    paused_for = max(feedback_finished_at - started_at, timedelta(0))

    active["deadline"] = (deadline + paused_for).isoformat()
    active["pending_feedback"] = None
    save_progress(progress)


def _print_short_answer_feedback(question: dict[str, Any], answer: Any) -> None:
    console.rule(f"Question {question['number']} Feedback")
    if answer_is_correct(question, answer):
        console.print("[green]Correct.[/]")
        return

    selected = set(normalize_answer(answer))
    correct = correct_choices_for(question)
    correct_set = set(correct)

    console.print("[red]Incorrect.[/]")
    console.print(Markdown(question["prompt"]))
    console.print(f"[bold]Your answer:[/] {format_answer(answer)}")
    console.print(f"[bold]Correct answer:[/] {format_answer(correct)}")

    if int(question.get("selection_count", 1)) > 1:
        missing, extra = answer_differences(question, answer)
        if missing:
            console.print(f"[yellow]Missing:[/] {format_answer(missing)}")
        if extra:
            console.print(f"[yellow]Extra:[/] {format_answer(extra)}")

    table = Table(show_header=True, header_style="bold")
    table.add_column("Choice", justify="center")
    table.add_column("Response")
    table.add_column("Markers")
    for choice in question["choices"]:
        letter = choice["letter"]
        markers = []
        if letter in selected:
            markers.append("your answer")
        if letter in correct_set:
            markers.append("correct")
        table.add_row(letter, Markdown(choice["text"]), ", ".join(markers))
    console.print(table)

    explanation = question.get("explanation", "")
    if explanation:
        console.print(Markdown(f"**Explanation:** {explanation}"))
    else:
        console.print("[yellow]No explanation is available for this question.[/]")


def _ask_question(
    question: dict[str, Any],
    position: int,
    total: int,
    deadline: str,
    previous_answer: list[str] | str | None = None,
) -> list[str]:
    remaining = _format_remaining(_seconds_remaining(deadline))
    console.rule(f"Question {position} / {total} - {remaining} remaining")
    if question.get("scenario"):
        console.print(f"[bold]{question['scenario']}[/]")
    console.print(Markdown(question["prompt"]))
    return _prompt_for_answer(question, previous_answer)


def _prompt_for_answer(
    question: dict[str, Any],
    previous_answer: list[str] | str | None = None,
) -> list[str]:
    normalized_previous = normalize_answer(previous_answer)
    choices = [
        {
            "name": f"{choice['letter']}. {choice['text']}",
            "value": choice["letter"],
            "checked": choice["letter"] in normalized_previous,
        }
        for choice in question["choices"]
    ]
    if normalized_previous:
        console.print(f"[dim]Previous answer: {format_answer(normalized_previous)}[/]")
    selection_count = int(question.get("selection_count", len(correct_choices_for(question)) or 1))
    if selection_count == 1:
        answer = questionary.select(
            "Your answer",
            choices=choices,
            default=normalized_previous[0] if normalized_previous else None,
        ).ask()
    else:
        console.print(f"[bold]Select exactly {selection_count} responses.[/]")
        answer = questionary.checkbox(
            "Your answers",
            choices=choices,
            instruction="Use Space to toggle; Enter to submit.",
            validate=lambda selected: validate_selection_count(selected, selection_count),
        ).ask()
    if answer is None:
        raise KeyboardInterrupt
    return normalize_answer(answer)


def _submit_exam(exam: dict[str, Any], progress: dict[str, Any]) -> None:
    _submit_timed_attempt(
        exam=exam,
        progress=progress,
        active_key="active_exam",
        attempts_key="exam_attempts",
        results_title="Exam Results",
    )


def _submit_short_exam(exam: dict[str, Any], progress: dict[str, Any]) -> None:
    _submit_timed_attempt(
        exam=exam,
        progress=progress,
        active_key="active_short_exam",
        attempts_key="short_exam_attempts",
        results_title="Short Exam Results",
    )


def _submit_timed_attempt(
    exam: dict[str, Any],
    progress: dict[str, Any],
    active_key: str,
    attempts_key: str,
    results_title: str,
) -> None:
    active = progress[active_key]
    answers: dict[str, list[str]] = active.get("answers", {})
    questions = exam["questions"]
    score = sum(
        1
        for question in questions
        if answer_is_correct(question, answers.get(str(question["number"]), []))
    )
    total = len(questions)
    passed = score >= int(exam["passing_score"])
    submitted_at = now_iso()

    progress.setdefault(attempts_key, []).append(
        {
            "exam_id": exam["id"],
            "started_at": active["started_at"],
            "submitted_at": submitted_at,
            "score": score,
            "total": total,
            "passing_score": exam["passing_score"],
            "passed": passed,
            "answers": answers,
        }
    )
    progress[active_key] = None
    save_progress(progress)

    style = "green" if passed else "yellow"
    console.rule(results_title)
    console.print(f"[bold {style}]Score: {score} / {total}[/] (passing proxy: {exam['passing_score']} / {exam['total_questions']})")
    _print_missed_questions(questions, answers)


def _print_missed_questions(questions: list[dict[str, Any]], answers: dict[str, Any]) -> None:
    missed = missed_questions_for(questions, answers)
    if not missed:
        console.print("[green]No missed questions.[/]")
        return

    console.print(f"[bold]Missed questions:[/] {len(missed)}")
    for question in missed:
        given = answers.get(str(question["number"]), [])
        correct = correct_choices_for(question)
        console.print(
            f"\n[bold]Question {question['number']}[/] - "
            f"your answer: {format_answer(given)}; correct: {format_answer(correct)}"
        )
        if int(question.get("selection_count", 1)) > 1:
            missing, extra = answer_differences(question, given)
            if missing:
                console.print(f"[yellow]Missing:[/] {format_answer(missing)}")
            if extra:
                console.print(f"[yellow]Extra:[/] {format_answer(extra)}")
        console.print(Markdown(question["prompt"]))
        if question.get("explanation"):
            console.print(Markdown(f"**Explanation:** {question['explanation']}"))


def _seconds_remaining(deadline: str) -> int:
    deadline_dt = datetime.fromisoformat(deadline)
    return max(0, int((deadline_dt - datetime.now(timezone.utc)).total_seconds()))


def _format_remaining(seconds: int) -> str:
    minutes, remainder = divmod(seconds, 60)
    return f"{minutes:02d}:{remainder:02d}"


def show_notes_list() -> None:
    packs = load_study_packs()
    table = Table(title="Study Pack Notes")
    table.add_column("ID")
    table.add_column("Title")
    table.add_column("Sections", justify="right")
    for pack in packs:
        table.add_row(pack["id"], pack["title"], str(len(pack["notes_sections"])))
    console.print(table)


def open_notes(pack_id: str | None = None, section: str | None = None) -> None:
    packs = load_study_packs()
    progress = load_progress()
    pack = find_by_id(packs, pack_id) if pack_id else choose_study_pack(packs, "Choose notes to study")
    if pack is None:
        console.print(f"[red]Unknown study pack:[/] {pack_id}")
        raise SystemExit(1)

    sections = pack["notes_sections"]
    selected = None
    if section:
        selected = next(
            (
                item
                for item in sections
                if item["id"] == section or item["title"].lower() == section.lower()
            ),
            None,
        )
    if selected is None:
        last_section = progress.get("notes", {}).get("last_opened", {}).get(pack["id"])
        choices = [
            {
                "name": f"{item['title']}{' (last)' if item['id'] == last_section else ''}",
                "value": item["id"],
            }
            for item in sections
        ]
        section_id = select_one("Choose a section", choices)
        selected = next(item for item in sections if item["id"] == section_id)

    progress.setdefault("notes", {}).setdefault("last_opened", {})[pack["id"]] = selected["id"]
    save_progress(progress)
    console.rule(f"{pack['title']} - {selected['title']}")
    console.print(Markdown(selected["body"] or "_No content in this section._"))


def show_card_list() -> None:
    packs = load_study_packs()
    table = Table(title="Flashcards")
    table.add_column("Pack")
    table.add_column("Title")
    table.add_column("Cards", justify="right")
    for pack in packs:
        table.add_row(pack["id"], pack["title"], str(len(pack["flashcards"])))
    console.print(table)


def review_cards(
    pack_id: str | None = None,
    topic: str | None = None,
    limit: int | None = None,
    domain: str | None = None,
) -> None:
    packs = load_study_packs()
    progress = load_progress()
    pack = find_by_id(packs, pack_id) if pack_id else choose_study_pack(packs, "Choose flashcards")
    if pack is None:
        console.print(f"[red]Unknown study pack:[/] {pack_id}")
        raise SystemExit(1)

    cards = list(pack["flashcards"])
    if domain:
        cards = [card for card in cards if (card.get("domain") or "").lower() == domain.lower()]
    if topic:
        cards = [card for card in cards if card["topic"].lower() == topic.lower()]
    elif cards:
        topics = sorted({card["topic"] for card in cards})
        choice = select_one(
            "Choose a topic",
            [{"name": "All topics", "value": "__all__"}]
            + [{"name": topic_name, "value": topic_name} for topic_name in topics],
        )
        if choice != "__all__":
            cards = [card for card in cards if card["topic"] == choice]

    if not cards:
        console.print("[yellow]No flashcards matched.[/]")
        return

    random.shuffle(cards)
    if limit:
        cards = cards[:limit]

    try:
        for index, card in enumerate(cards, start=1):
            console.rule(f"Card {index} / {len(cards)}")
            heading = f"{card['domain']} · {card['topic']}" if card.get("domain") else card["topic"]
            console.print(f"[bold]{heading}[/]\n")
            console.print(Markdown(card["question"]))
            pause("Reveal answer")
            console.print(Markdown(f"**Answer:** {card['answer']}"))
            if card.get("example"):
                console.print(Markdown(f"**Example:** {card['example']}"))
            rating = select_one(
                "Rate recall",
                [
                    {"name": "Again", "value": "again"},
                    {"name": "Good", "value": "good"},
                    {"name": "Easy", "value": "easy"},
                ],
            )
            stats = progress.setdefault("flashcards", {}).setdefault(
                card["id"],
                {"again": 0, "good": 0, "easy": 0, "last_reviewed_at": None},
            )
            stats[rating] += 1
            stats["last_reviewed_at"] = now_iso()
            save_progress(progress)
    except KeyboardInterrupt:
        console.print("\n[yellow]Card progress saved.[/]")
        return


def start_quiz(pack_id: str | None = None) -> None:
    packs = load_study_packs()
    pack = find_by_id(packs, pack_id) if pack_id else choose_study_pack(packs, "Choose a study-pack quiz")
    if pack is None:
        console.print(f"[red]Unknown study pack:[/] {pack_id}")
        raise SystemExit(1)

    questions = pack["practice_questions"]
    if not questions:
        console.print("[yellow]This study pack has no practice questions.[/]")
        return

    answers: dict[str, list[str]] = {}
    for index, question in enumerate(questions, start=1):
        if index > 1:
            console.clear()
        answer = _ask_quiz_question(question, index, len(questions))
        answers[str(question["number"])] = answer

    score = sum(
        1
        for question in questions
        if answer_is_correct(question, answers.get(str(question["number"]), []))
    )
    console.clear()
    console.rule("Quiz Results")
    console.print(f"[bold]Score: {score} / {len(questions)}[/]")
    _print_missed_questions(questions, answers)


def _ask_quiz_question(question: dict[str, Any], position: int, total: int) -> list[str]:
    console.rule(f"Question {position} / {total}")
    if question.get("scenario"):
        console.print(Markdown(f"**Scenario:** {question['scenario']}"))
    console.print(Markdown(question["prompt"]))
    return _prompt_for_answer(question)


def show_stats() -> None:
    progress = load_progress()
    attempts = progress.get("exam_attempts", [])
    short_attempts = progress.get("short_exam_attempts", [])
    flashcards = progress.get("flashcards", {})
    table = Table(title="Progress")
    table.add_column("Metric")
    table.add_column("Value", justify="right")
    table.add_row("Completed full exam attempts", str(len(attempts)))
    table.add_row("Completed short exam attempts", str(len(short_attempts)))
    table.add_row("Reviewed flashcards", str(len(flashcards)))
    if attempts:
        latest = attempts[-1]
        table.add_row("Latest full exam score", f"{latest['score']} / {latest['total']}")
    if short_attempts:
        latest_short = short_attempts[-1]
        table.add_row(
            "Latest short exam score",
            f"{latest_short['score']} / {latest_short['total']}",
        )
    console.print(table)
