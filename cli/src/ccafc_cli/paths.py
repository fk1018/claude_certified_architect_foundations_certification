from __future__ import annotations

from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[0]
CLI_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = CLI_ROOT.parent

STUDY_PACKS_DIR = REPO_ROOT / "study_packs"
PRACTICE_EXAMS_DIR = REPO_ROOT / "practice_exams"
GENERATED_DIR = CLI_ROOT / "data" / "generated"
STATE_DIR = CLI_ROOT / ".state"
PROGRESS_PATH = STATE_DIR / "progress.json"

STUDY_PACKS_JSON = GENERATED_DIR / "study_packs.json"
PRACTICE_EXAMS_JSON = GENERATED_DIR / "practice_exams.json"
