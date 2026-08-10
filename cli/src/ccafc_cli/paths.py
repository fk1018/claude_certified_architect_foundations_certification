from __future__ import annotations

import os
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[0]
CLI_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = CLI_ROOT.parent

# Multi-track support -------------------------------------------------------
# The CLI was originally built for a single certification (Architect —
# Foundations). CCAFC_TRACK lets the same CLI/test suite drive study
# material for additional certification tracks that live in sibling
# top-level folders, without disturbing the original track's paths, saved
# progress, or generated-data schema. Read once per process at import time —
# each `ccafc`/`ccdvf`/`ccarp` invocation is a fresh process, so this is not
# a runtime-mutable setting.
DEFAULT_TRACK = "architect-foundations"
CCAFC_TRACK = os.environ.get("CCAFC_TRACK", DEFAULT_TRACK).strip() or DEFAULT_TRACK

TRACK_INFO = {
    "architect-foundations": {
        "label": "CCAFC",
        "name": "Claude Certified Architect Foundations",
        "study_packs_dirname": "study_packs",
        "practice_exams_dirname": "practice_exams",
    },
    "developer-foundations": {
        "label": "CCDVF",
        "name": "Claude Certified Developer Foundations",
        "study_packs_dirname": "study_packs_developer_foundations",
        "practice_exams_dirname": "practice_exams_developer_foundations",
    },
    "architect-professional": {
        "label": "CCARP",
        "name": "Claude Certified Architect Professional",
        "study_packs_dirname": "study_packs_architect_professional",
        "practice_exams_dirname": "practice_exams_architect_professional",
    },
}

if CCAFC_TRACK not in TRACK_INFO:
    raise ValueError(
        f"Unknown CCAFC_TRACK '{CCAFC_TRACK}'. Expected one of: {', '.join(sorted(TRACK_INFO))}"
    )

_TRACK = TRACK_INFO[CCAFC_TRACK]
TRACK_LABEL = _TRACK["label"]
TRACK_NAME = _TRACK["name"]

STUDY_PACKS_DIR = REPO_ROOT / _TRACK["study_packs_dirname"]
PRACTICE_EXAMS_DIR = REPO_ROOT / _TRACK["practice_exams_dirname"]

# The default track keeps its original, unnamespaced generated-data and
# progress paths so existing users see zero disruption. Other tracks get
# their own subfolder so three tracks can be studied independently (and
# concurrently) without one track's progress or cached data clobbering
# another's.
if CCAFC_TRACK == DEFAULT_TRACK:
    GENERATED_DIR = CLI_ROOT / "data" / "generated"
    STATE_DIR = CLI_ROOT / ".state"
else:
    GENERATED_DIR = CLI_ROOT / "data" / "generated" / CCAFC_TRACK
    STATE_DIR = CLI_ROOT / ".state" / CCAFC_TRACK

PROGRESS_PATH = STATE_DIR / "progress.json"

STUDY_PACKS_JSON = GENERATED_DIR / "study_packs.json"
PRACTICE_EXAMS_JSON = GENERATED_DIR / "practice_exams.json"
