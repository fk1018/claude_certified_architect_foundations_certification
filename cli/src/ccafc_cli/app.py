from __future__ import annotations

from typing import Optional

import typer

from ccafc_cli import __version__
from ccafc_cli.flows import (
    ShortExamFeedbackMode,
    open_notes,
    resume_exam,
    resume_short_exam,
    review_cards,
    review_exam_attempt,
    review_short_exam_attempt,
    show_card_list,
    show_exam_list,
    show_exam_results,
    show_notes_list,
    show_short_exam_list,
    show_short_exam_results,
    show_stats,
    start_exam,
    start_quiz,
    start_short_exam,
)
from ccafc_cli.paths import TRACK_NAME
from ccafc_cli.storage import generate_data
from ccafc_cli.ui import console, select_one


app = typer.Typer(
    help=f"Study tools for the {TRACK_NAME} certification.",
    invoke_without_command=True,
)
exam_app = typer.Typer(help="Timed practice exam workflows.")
short_exam_app = typer.Typer(help="Timed 15-question short practice exam workflows.")
notes_app = typer.Typer(help="Study-pack notes workflows.")
cards_app = typer.Typer(help="Flashcard workflows.")
quiz_app = typer.Typer(help="Untimed study-pack practice questions.")

app.add_typer(exam_app, name="exam")
exam_app.add_typer(short_exam_app, name="short")
app.add_typer(notes_app, name="notes")
app.add_typer(cards_app, name="cards")
app.add_typer(quiz_app, name="quiz")


@app.callback()
def root(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", help="Show version and exit."),
) -> None:
    if version:
        console.print(__version__)
        raise typer.Exit()
    if ctx.invoked_subcommand is None:
        interactive_menu()


def interactive_menu() -> None:
    while True:
        choice = select_one(
            "What would you like to do?",
            [
                {"name": "Take a full timed practice exam", "value": "exam"},
                {"name": "Take a short timed practice exam", "value": "short_exam"},
                {"name": "Review missed full-exam questions", "value": "exam_review"},
                {
                    "name": "Review missed short-exam questions",
                    "value": "short_exam_review",
                },
                {"name": "Study notes", "value": "notes"},
                {"name": "Review flashcards", "value": "cards"},
                {"name": "Take a study-pack quiz", "value": "quiz"},
                {"name": "Import/regenerate data", "value": "import"},
                {"name": "View stats", "value": "stats"},
                {"name": "Exit", "value": "exit"},
            ],
        )
        if choice == "exam":
            start_exam()
        elif choice == "short_exam":
            start_short_exam()
        elif choice == "exam_review":
            review_exam_attempt()
        elif choice == "short_exam_review":
            review_short_exam_attempt()
        elif choice == "notes":
            open_notes()
        elif choice == "cards":
            review_cards()
        elif choice == "quiz":
            start_quiz()
        elif choice == "import":
            import_data()
        elif choice == "stats":
            show_stats()
        else:
            return


@app.command("import")
def import_data() -> None:
    """Parse Markdown study material into generated JSON."""
    summary = generate_data()
    console.print("[green]Generated study data.[/]")
    console.print(
        f"{summary['study_packs']} study packs, "
        f"{summary['practice_exams']} full exams, "
        f"{summary['short_practice_exams']} short exams, "
        f"{summary['flashcards']} flashcards, "
        f"{summary['study_pack_questions']} study-pack questions, "
        f"{summary['full_exam_questions']} full-exam questions, "
        f"{summary['short_exam_questions']} short-exam question references."
    )


@app.command()
def stats() -> None:
    """Show saved local study progress."""
    show_stats()


@exam_app.command("list")
def exam_list() -> None:
    """List full practice exams."""
    show_exam_list()


@exam_app.command("start")
def exam_start(
    exam_id: Optional[str] = typer.Argument(None, help="Practice exam ID, e.g. practice-exam-1."),
    force: bool = typer.Option(False, "--force", help="Discard any active attempt."),
) -> None:
    """Start a strict timed practice exam."""
    start_exam(exam_id=exam_id, force=force)


@exam_app.command("resume")
def exam_resume() -> None:
    """Resume the active timed practice exam."""
    resume_exam()


@exam_app.command("results")
def exam_results() -> None:
    """Show completed exam attempts."""
    show_exam_results()


@exam_app.command("review")
def exam_review(
    attempt_number: Optional[int] = typer.Argument(
        None,
        min=1,
        help="Completed attempt number from `ccafc exam results`.",
    ),
) -> None:
    """Retry and study questions missed on a completed exam attempt."""
    review_exam_attempt(attempt_number=attempt_number)


@short_exam_app.command("list")
def short_exam_list() -> None:
    """List 15-question short practice exams."""
    show_short_exam_list()


@short_exam_app.command("start")
def short_exam_start(
    exam_id: Optional[str] = typer.Argument(
        None,
        help="Short practice exam ID, e.g. short-practice-exam-1.",
    ),
    force: bool = typer.Option(False, "--force", help="Discard any active short attempt."),
    feedback: Optional[ShortExamFeedbackMode] = typer.Option(
        None,
        "--feedback",
        help="Show feedback after each question (immediate) or only at the end (deferred).",
    ),
) -> None:
    """Start a timed short practice exam and choose when feedback appears."""
    start_short_exam(exam_id=exam_id, force=force, feedback_mode=feedback)


@short_exam_app.command("resume")
def short_exam_resume() -> None:
    """Resume the active short practice exam."""
    resume_short_exam()


@short_exam_app.command("results")
def short_exam_results() -> None:
    """Show completed short exam attempts."""
    show_short_exam_results()


@short_exam_app.command("review")
def short_exam_review(
    attempt_number: Optional[int] = typer.Argument(
        None,
        min=1,
        help="Completed attempt number from `ccafc exam short results`.",
    ),
) -> None:
    """Retry and study questions missed on a completed short attempt."""
    review_short_exam_attempt(attempt_number=attempt_number)


@notes_app.command("list")
def notes_list() -> None:
    """List study-pack notes."""
    show_notes_list()


@notes_app.command("open")
def notes_open(
    pack_id: Optional[str] = typer.Argument(None, help="Study pack ID."),
    section: Optional[str] = typer.Option(None, "--section", "-s", help="Section ID or title."),
) -> None:
    """Open a study-pack note section."""
    open_notes(pack_id=pack_id, section=section)


@cards_app.command("list")
def cards_list() -> None:
    """List flashcard counts by study pack."""
    show_card_list()


@cards_app.command("review")
def cards_review(
    pack_id: Optional[str] = typer.Option(None, "--pack", "-p", help="Study pack ID."),
    topic: Optional[str] = typer.Option(None, "--topic", "-t", help="Exact flashcard topic."),
    limit: Optional[int] = typer.Option(None, "--limit", "-n", min=1, help="Maximum cards to review."),
    domain: Optional[str] = typer.Option(None, "--domain", "-d", help="Exam domain code, e.g. D1."),
) -> None:
    """Review flashcards interactively."""
    review_cards(pack_id=pack_id, topic=topic, limit=limit, domain=domain)


@quiz_app.command("start")
def quiz_start(
    pack_id: Optional[str] = typer.Option(None, "--pack", "-p", help="Study pack ID."),
) -> None:
    """Run untimed study-pack practice questions."""
    start_quiz(pack_id=pack_id)


def main() -> None:
    app()
