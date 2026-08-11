from __future__ import annotations

from typer.testing import CliRunner

from ccafc_cli import app as app_module


runner = CliRunner()


def test_exam_review_command_is_available() -> None:
    result = runner.invoke(app_module.app, ["exam", "review", "--help"])

    assert result.exit_code == 0
    assert "Retry and study questions missed on a completed exam attempt." in result.output
    assert "ATTEMPT_NUMBER" in result.output


def test_short_exam_commands_are_available() -> None:
    result = runner.invoke(app_module.app, ["exam", "short", "--help"])

    assert result.exit_code == 0
    for command in ("list", "start", "resume", "results", "review"):
        assert command in result.output


def test_short_exam_start_exposes_feedback_option() -> None:
    result = runner.invoke(app_module.app, ["exam", "short", "start", "--help"])

    assert result.exit_code == 0
    assert "--feedback" in result.output
    assert "immediate" in result.output
    assert "deferred" in result.output


def test_short_exam_start_passes_explicit_feedback_mode(monkeypatch) -> None:
    calls = []
    monkeypatch.setattr(
        app_module,
        "start_short_exam",
        lambda **kwargs: calls.append(kwargs),
    )

    result = runner.invoke(
        app_module.app,
        ["exam", "short", "start", "short-practice-exam-1", "--feedback", "deferred"],
    )

    assert result.exit_code == 0
    assert calls == [
        {
            "exam_id": "short-practice-exam-1",
            "force": False,
            "feedback_mode": app_module.ShortExamFeedbackMode.DEFERRED,
        }
    ]


def test_interactive_menu_exposes_separate_full_and_short_workflows(monkeypatch) -> None:
    answers = iter(["short_exam", "short_exam_review", "exam_review", "exit"])
    calls = []

    def choose_menu_item(message, choices):
        assert message == "What would you like to do?"
        if not calls:
            assert any(
                choice["name"] == "Review missed full-exam questions"
                and choice["value"] == "exam_review"
                for choice in choices
            )
            assert any(
                choice["name"] == "Take a short timed practice exam"
                and choice["value"] == "short_exam"
                for choice in choices
            )
            assert any(
                choice["name"] == "Review missed short-exam questions"
                and choice["value"] == "short_exam_review"
                for choice in choices
            )
        return next(answers)

    monkeypatch.setattr(app_module, "select_one", choose_menu_item)
    monkeypatch.setattr(app_module, "start_short_exam", lambda: calls.append("short-start"))
    monkeypatch.setattr(
        app_module,
        "review_short_exam_attempt",
        lambda: calls.append("short-review"),
    )
    monkeypatch.setattr(app_module, "review_exam_attempt", lambda: calls.append("full-review"))

    app_module.interactive_menu()

    assert calls == ["short-start", "short-review", "full-review"]
