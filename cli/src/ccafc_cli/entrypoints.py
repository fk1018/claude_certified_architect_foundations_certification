"""Console-script entry points for the non-default certification tracks.

Each function sets CCAFC_TRACK *before* importing ccafc_cli.app, because
ccafc_cli.paths reads the environment variable once at import time. These
thin wrappers are what let `ccdvf` and `ccarp` reuse the exact same Typer
app, flows, parsers, and tests as `ccafc`, just pointed at a different
track's folders and generated-data/progress paths.
"""

from __future__ import annotations

import os


def main_developer_foundations() -> None:
    os.environ["CCAFC_TRACK"] = "developer-foundations"
    from ccafc_cli.app import main

    main()


def main_architect_professional() -> None:
    os.environ["CCAFC_TRACK"] = "architect-professional"
    from ccafc_cli.app import main

    main()
