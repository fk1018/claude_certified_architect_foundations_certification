from __future__ import annotations

from typing import Any, Iterable

import questionary
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table


console = Console()


def select_one(message: str, choices: list[dict[str, Any] | str]) -> Any:
    answer = questionary.select(message, choices=choices).ask()
    if answer is None:
        raise KeyboardInterrupt
    return answer


def confirm(message: str, default: bool = False) -> bool:
    answer = questionary.confirm(message, default=default).ask()
    if answer is None:
        raise KeyboardInterrupt
    return bool(answer)


def pause(message: str = "Press Enter to continue") -> None:
    answer = questionary.text(message).ask()
    if answer is None:
        raise KeyboardInterrupt


def render_markdown(text: str) -> None:
    console.print(Markdown(text))


def print_panel(title: str, body: str, style: str = "cyan") -> None:
    console.print(Panel(body, title=title, border_style=style))


def make_table(title: str, columns: Iterable[str]) -> Table:
    table = Table(title=title)
    for column in columns:
        table.add_column(column)
    return table
