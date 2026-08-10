# Cert Prep Desk (web)

A static React + TypeScript + Tailwind front end for the same practice exams, study
notes, and flashcards the CLI (`../cli`) serves in the terminal. There is no backend:
`npm run build`/`npm run dev` copy the CLI's already-generated JSON
(`cli/data/generated/**`) into `public/data/`, and the app fetches it directly. Progress
(in-progress attempts, completed scores, flashcard "known" state) lives in the
browser's `localStorage`, one record per track.

## Develop

```bash
cd cli && CCAFC_TRACK=developer-foundations python -c "from ccafc_cli.storage import generate_data; generate_data()"
cd cli && CCAFC_TRACK=architect-professional python -c "from ccafc_cli.storage import generate_data; generate_data()"
cd cli && python -c "from ccafc_cli.storage import generate_data; generate_data()"  # default track
cd web
npm install
npm run dev
```

`npm run dev`/`npm run build` both run `npm run sync-data` first, which copies the
three tracks' JSON into `public/data/` (gitignored — regenerated on every run, the
CLI's generated JSON is the single source of truth).

## What's here

- One track per certification (`architect-foundations`, `developer-foundations`,
  `architect-professional`), each with its full practice-exam bank, short drills,
  study notes, and flashcards.
- Exam runner with a real countdown timer, single/multi-select questions, and
  auto-submit at time's up.
- Answer review with per-question explanations after submitting.
- Flashcard flow with a "known" / "still learning" split.

## What's intentionally not here

No backend, no account system, no cross-device sync, and no server-side enforcement
of the timer or question order — everything is client-side and trivially bypassable.
That trade-off is the point: it's a free, static study tool, not a proctored exam.
