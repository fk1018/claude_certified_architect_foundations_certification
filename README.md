# Claude Certification Study Workspace

This repository is a self-contained study workspace for three Claude certification
tracks — **Architect – Foundations**, **Developer – Foundations**, and
**Architect – Professional**. It combines Markdown study material with an
interactive terminal application (and, optionally, a web app) for notes,
flashcards, quizzes, and timed practice exams.

The Markdown files remain the source of truth, so you can study directly from the
repository, use the CLI for a guided terminal experience, or use the web app for a
guided browser experience.

## Certification tracks

| Track | CLI command | Full exams | Questions | Study packs |
|---|---|---:|---:|---|
| Architect – Foundations (CCAFC) | `ccafc` | 12 | 720 | 8 packs, incl. the recommended Exam Guide Gap Pack |
| Developer – Foundations (CCDVF) | `ccdvf` | 12 | 720 | Exam Guide Gap Pack |
| Architect – Professional (CCARP) | `ccarp` | 12 | 720 | Exam Guide Gap Pack |

Each track has its own generated data, study progress, and terminal command, so
you can work through more than one certification without either one clobbering
the other's saved state. The commands below all apply equally to `ccafc`,
`ccdvf`, and `ccarp` — swap in whichever track you're studying.

## Quick start

Run commands from the repository root.

### Docker

Docker is the lowest-friction option because it provides the required Python
environment. With Docker and Docker Compose installed, launch the interactive
menu for a track with:

```bash
docker compose run --rm ccafc   # Architect – Foundations
docker compose run --rm ccdvf   # Developer – Foundations
docker compose run --rm ccarp   # Architect – Professional
```

You can also append any CLI command directly:

```bash
docker compose run --rm ccafc exam short start
docker compose run --rm ccdvf exam list
```

The repository is mounted into the container, so generated data and study
progress persist between runs.

### Local installation

Local use requires [uv](https://docs.astral.sh/uv/) and Python 3.14 or newer.
`uv` creates the project environment and installs the dependencies when the
command runs:

```bash
uv run --project cli ccafc   # Architect – Foundations
uv run --project cli ccdvf   # Developer – Foundations
uv run --project cli ccarp   # Architect – Professional
```

Run `uv run --project cli ccafc --help` to see the available commands (the same
options apply to `ccdvf` and `ccarp`).

### Web app

Prefer a browser? `web/` has a static React/TypeScript/Tailwind app covering the
same practice exams, notes, and flashcards for all three tracks — no backend, no
account, progress kept in your browser's local storage. See
[`web/README.md`](web/README.md) for setup; the short version:

```bash
cd web
npm install
npm run dev
```

## Recommended study approach

Use the **short timed practice exams for regular study**. Each short exam focuses
on one 15-question scenario, gives you 30 minutes, and immediately explains a
missed answer while pausing the timer. That tight feedback loop makes it easier
to identify and correct weak areas.

Use the **full-length practice exams to simulate the real exam**. Each full exam
contains 60 questions with a 120-minute limit, and feedback stays hidden until
submission so you can practice pacing, focus, and decision-making under realistic
exam conditions.

A practical study loop is:

1. Review the Exam Guide Gap Pack.
2. Take short exams and review every missed question.
3. Use a full-length exam periodically to measure readiness under exam-like
   conditions.

> **Study-pack recommendation:** I recommend the
> [Exam Guide Gap Pack](study_packs/exam-guide-gap-pack/notes.md). I do not
> recommend the other study packs for primary exam preparation; they remain in
> the repository as supplemental reference material.

Whether you complete every exam or only a subset, include at least a few full and
short exams from **both generation groups** listed below. This prevents your
practice from reflecting only one model's question-writing style.

## Exam generation provenance

The provenance table below covers the **Architect – Foundations** track only.
Each short exam is derived from one of the four 15-question scenario sections in
its associated full exam, so it inherits the generation and review provenance of
that full exam.

The **Developer – Foundations** and **Architect – Professional** tracks were
generated in a later pass: exam 1 in each track predates this workspace's
current tooling, and exams 2–12 were generated together, in one pass, by the
model listed in this repository's git history for that change — without the
multi-model cross-audit the Architect – Foundations exams below went through.
Treat them accordingly, and, as with any practice material, don't take a single
missed or oddly-worded question as authoritative on its own.

### Claude Fable xhigh, audited and edited by GPT-5.6-Sol max

| Full exam | Associated short exams |
|---|---|
| [Practice Exam 1](practice_exams/practice-exam-1.md) | `short-practice-exam-1` through `short-practice-exam-4` |
| [Practice Exam 2](practice_exams/practice-exam-2.md) | `short-practice-exam-5` through `short-practice-exam-8` |
| [Practice Exam 3](practice_exams/practice-exam-3.md) | `short-practice-exam-9` through `short-practice-exam-12` |
| [Practice Exam 4](practice_exams/practice-exam-4.md) | `short-practice-exam-13` through `short-practice-exam-16` |
| [Practice Exam 5](practice_exams/practice-exam-5.md) | `short-practice-exam-17` through `short-practice-exam-20` |

### GPT-5.6-Sol max

| Full exam | Associated short exams |
|---|---|
| [Practice Exam 6](practice_exams/practice-exam-6.md) | `short-practice-exam-21` through `short-practice-exam-24` |
| [Practice Exam 7](practice_exams/practice-exam-7.md) | `short-practice-exam-25` through `short-practice-exam-28` |
| [Practice Exam 8](practice_exams/practice-exam-8.md) | `short-practice-exam-29` through `short-practice-exam-32` |
| [Practice Exam 9](practice_exams/practice-exam-9.md) | `short-practice-exam-33` through `short-practice-exam-36` |
| [Practice Exam 10](practice_exams/practice-exam-10.md) | `short-practice-exam-37` through `short-practice-exam-40` |
| [Practice Exam 13](practice_exams/practice-exam-13.md) | `short-practice-exam-41` through `short-practice-exam-44` |
| [Practice Exam 14](practice_exams/practice-exam-14.md) | `short-practice-exam-45` through `short-practice-exam-48` |

## Practice exam modes

| | Short practice exam | Full practice exam |
|---|---:|---:|
| Questions | 15 from one scenario | 60 across four scenarios |
| Time limit | 30 minutes | 120 minutes |
| Passing proxy | 12/15 | 45/60 |
| Feedback | Immediate after a missed answer; timer pauses during review | After submission |
| Best use | Focused study and fast feedback | Full exam simulation |

All questions in the **Architect – Foundations** full exams, derived short exams,
and study-pack quizzes are single-select multiple-choice items: exactly one
answer can be chosen, with no select-multiple or multiple-response items. This
matches that certification's real exam format: according to its
[exam guide](exam_guide_pdf_v0.2.txt), every question has one correct response
and three incorrect options.

The **Developer – Foundations** and **Architect – Professional** exams are
almost entirely single-select as well, but their official exam guides
([developer](exam_guide_developer_foundations.txt),
[architect professional](exam_guide_architect_professional.txt)) allow
multiple-response items that state how many answers to select, and a small
number of practice questions in those tracks use that format — read each
question's instructions before answering. On short exams, correct answers
receive a brief confirmation without revealing the explanation; missed answers
receive the full feedback described above.

Answers are saved after every question. Press `Ctrl+C` to leave an attempt and use
the corresponding `resume` command later. Full and short exams keep independent
active attempts and histories, so one attempt of each type can be active at the
same time.

The `review` commands retry only the questions missed on a completed attempt.
After each retry, the CLI shows the original answer, correct answer, choices, and
explanation. Review answers are not scored or saved.

## CLI command reference

The table below shows the portion of each command that follows `ccafc`. Prefix it
with `uv run --project cli ccafc` (or `ccdvf`/`ccarp`) for local use, or
`docker compose run --rm ccafc` (or `ccdvf`/`ccarp`) for Docker — the commands
are identical across tracks, only the data they operate on differs.

| Command | Purpose |
|---|---|
| `exam list` | List the full practice exams. |
| `exam start [EXAM_ID] [--force]` | Start a full timed exam. |
| `exam resume` | Resume the active full exam. |
| `exam results` | Show completed full-exam attempts. |
| `exam review [ATTEMPT_NUMBER]` | Retry missed questions from a completed full exam. |
| `exam short list` | List the generated 15-question exams. |
| `exam short start [EXAM_ID] [--force]` | Start a short timed exam. |
| `exam short resume` | Resume the active short exam. |
| `exam short results` | Show completed short-exam attempts. |
| `exam short review [ATTEMPT_NUMBER]` | Retry missed questions from a completed short exam. |
| `notes list` | List available study-pack notes. |
| `notes open [PACK_ID] [--section SECTION]` | Open a study pack or one of its sections. |
| `cards list` | Show flashcard counts by study pack. |
| `cards review [--pack PACK_ID] [--topic TOPIC] [--limit N]` | Review a filtered flashcard set. |
| `quiz start [--pack PACK_ID]` | Run an untimed study-pack quiz. |
| `stats` | Show saved local study progress. |
| `import` | Regenerate CLI data from the Markdown source files. |
| `--version` | Show the CLI version. |

Running `ccafc` without a subcommand opens an interactive menu containing the same
workflows. When starting an exam, `--force` discards an existing active attempt of
the same type instead of offering to resume it.

## Study materials

### Architect – Foundations

This track has the workspace's original eight study packs. Each pack contains
detailed notes, flashcards, and untimed practice questions. Of these, only the
**Exam Guide Gap Pack is recommended for exam preparation**; the other packs are
included as supplemental references.

| Study pack | Notes |
|---|---|
| AI Fluency: Framework & Foundations | [Open notes](study_packs/ai-fluency-framework-foundations/notes.md) |
| Claude 101 | [Open notes](study_packs/claude-101/notes.md) |
| Claude Code in Action | [Open notes](study_packs/claude-code-in-action/notes.md) |
| Claude with Amazon Bedrock | [Open notes](study_packs/claude-in-amazon-bedrock/notes.md) |
| Claude with Google Cloud's Vertex AI | [Open notes](study_packs/claude-with-google-vertex/notes.md) |
| Building with the Claude API | [Open notes](study_packs/claude-with-the-anthropic-api/notes.md) |
| Exam Guide Gap Pack | [Open notes](study_packs/exam-guide-gap-pack/notes.md) |
| Introduction to Model Context Protocol | [Open notes](study_packs/introduction-to-model-context-protocol/notes.md) |

- [12 full-length practice exams](practice_exams/) with 720 questions in total.
  The CLI derives 48 short exams from their scenario sections.
- [Extracted certification exam guide](exam_guide_pdf_v0.2.txt).
- [Study-pack template](study_packs/_template/) for adding future material.

### Developer – Foundations and Architect – Professional

Each of these tracks currently ships one study pack — an Exam Guide Gap Pack
built from that certification's own [exam
guide](exam_guide_developer_foundations.txt) — plus its own
[12 full-length practice exams](practice_exams_developer_foundations/) (720
questions, 48 derived short exams), matching the Architect – Foundations
track's scale. See
[`practice_exams_architect_professional/`](practice_exams_architect_professional/)
and
[`study_packs_architect_professional/`](study_packs_architect_professional/) for
the Architect – Professional equivalents.

## Repository layout

```text
.
├── cli/                                    # Python terminal app, tests, and generated data
├── web/                                    # Static React/TS/Tailwind web app (all tracks)
├── practice_exams/                         # Architect – Foundations: full-length exams
├── study_packs/                            # Architect – Foundations: notes, flashcards, quizzes
├── practice_exams_developer_foundations/   # Developer – Foundations: full-length exams
├── study_packs_developer_foundations/      # Developer – Foundations: study pack
├── practice_exams_architect_professional/  # Architect – Professional: full-length exams
├── study_packs_architect_professional/     # Architect – Professional: study pack
├── compose.yaml                            # Docker Compose entry point (ccafc/ccdvf/ccarp)
├── exam_guide_pdf_v0.2.txt                 # Architect – Foundations exam guide
├── exam_guide_developer_foundations.txt    # Developer – Foundations exam guide
└── exam_guide_architect_professional.txt   # Architect – Professional exam guide
```

## Data and progress

The CLI reads generated JSON from `cli/data/generated/` (each of `ccdvf`/`ccarp`
uses its own subfolder there, e.g. `cli/data/generated/developer-foundations/`).
It creates that data when it is missing or uses an updated schema, but after
editing the Markdown source you should regenerate it explicitly:

```bash
uv run --project cli ccafc import
uv run --project cli ccdvf import
uv run --project cli ccarp import
```

With Docker, use:

```bash
docker compose run --rm ccafc import
```

Local study progress is saved to `cli/.state/progress.json` for Architect –
Foundations, and to a per-track subfolder of `cli/.state/` for the other two
tracks. The `.state` directory is ignored by Git. The web app doesn't read any
of this — it keeps its own progress in browser local storage (see
[`web/README.md`](web/README.md)).

## Development

Run the test suite from the repository root:

```bash
uv run --project cli pytest cli/tests
```

Build the CLI package with:

```bash
uv build cli
```
