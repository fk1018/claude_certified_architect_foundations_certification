# Claude Certified Architect – Foundations Study Workspace

This repository is a self-contained study workspace for the Claude Certified
Architect – Foundations certification. It combines Markdown study material with
an interactive terminal application for notes, flashcards, quizzes, and timed
practice exams.

The Markdown files remain the source of truth, so you can study directly from the
repository or use the CLI for a guided experience.

## Quick start

Run commands from the repository root.

### Docker

Docker is the lowest-friction option because it provides the required Python
environment. With Docker and Docker Compose installed, launch the interactive
menu with:

```bash
docker compose run --rm ccafc
```

You can also append any CLI command directly:

```bash
docker compose run --rm ccafc exam short start
```

The repository is mounted into the container, so generated data and study
progress persist between runs.

### Local installation

Local use requires [uv](https://docs.astral.sh/uv/) and Python 3.14 or newer.
`uv` creates the project environment and installs the dependencies when the
command runs:

```bash
uv run --project cli ccafc
```

Run `uv run --project cli ccafc --help` to see the available commands.

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

Each short exam is derived from one of the four 15-question scenario sections in
its associated full exam. It therefore inherits the generation and review
provenance of that full exam.

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

All questions in the current full exams, derived short exams, and study-pack
quizzes are single-select multiple-choice items: exactly one answer can be chosen.
There are no select-multiple or multiple-response items. This matches the real
certification exam: according to the
[exam guide](exam_guide_pdf_v0.2.txt), every question has one correct response and
three incorrect options. On short exams, correct answers receive a brief
confirmation without revealing the explanation; missed answers receive the full
feedback described above.

Answers are saved after every question. Press `Ctrl+C` to leave an attempt and use
the corresponding `resume` command later. Full and short exams keep independent
active attempts and histories, so one attempt of each type can be active at the
same time.

The `review` commands retry only the questions missed on a completed attempt.
After each retry, the CLI shows the original answer, correct answer, choices, and
explanation. Review answers are not scored or saved.

## CLI command reference

The table below shows the portion of each command that follows `ccafc`. Prefix it
with either `uv run --project cli ccafc` for local use or
`docker compose run --rm ccafc` for Docker.

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

The workspace currently includes eight study packs. Each pack contains detailed
notes, flashcards, and untimed practice questions. Of these, only the
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

Additional material includes:

- [12 full-length practice exams](practice_exams/) with 720 questions in total.
  The CLI derives 48 short exams from their scenario sections.
- [Extracted certification exam guide](exam_guide_pdf_v0.2.txt).
- [Study-pack template](study_packs/_template/) for adding future material.

## Repository layout

```text
.
├── cli/                    # Python terminal app, tests, and generated data
├── practice_exams/         # Full-length Markdown practice exams
├── study_packs/            # Notes, flashcards, and practice questions
├── compose.yaml            # Docker Compose entry point
└── exam_guide_pdf_v0.2.txt # Extracted certification exam guide
```

## Data and progress

The CLI reads generated JSON from `cli/data/generated/`. It creates that data when
it is missing or uses an updated schema, but after editing the Markdown source you
should regenerate it explicitly:

```bash
uv run --project cli ccafc import
```

With Docker, use:

```bash
docker compose run --rm ccafc import
```

Local study progress is saved to `cli/.state/progress.json`. The `.state`
directory is ignored by Git.

## Development

Run the test suite from the repository root:

```bash
uv run --project cli pytest cli/tests
```

Build the CLI package with:

```bash
uv build cli
```
