import { useMemo, useState } from 'react'
import { Link, useOutletContext, useParams } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'
import { loadProgress } from '../lib/progress'
import type { PracticeExam, TrackId } from '../types/domain'

function ExamRow({
  trackId,
  kind,
  exam,
}: {
  trackId: TrackId
  kind: 'full' | 'short'
  exam: PracticeExam
}) {
  const progress = loadProgress(trackId)
  const isActive = progress.active?.examId === exam.id
  const lastAttempt = progress.attempts.find((a) => a.examId === exam.id)

  return (
    <Link
      to={`/${trackId}/exam/${kind}/${exam.id}`}
      className="ticket ticket-stub group flex items-center justify-between gap-4 px-5 py-3.5 pl-7 transition-transform hover:-translate-y-0.5"
    >
      <div className="min-w-0">
        <p className="truncate font-display text-base font-medium text-bone group-hover:text-brass-bright">
          {exam.title}
        </p>
        <p className="mt-1 font-mono text-[11px] uppercase tracking-widest text-bone-dim">
          {exam.total_questions} q · {exam.time_limit_minutes} min · pass ≥ {exam.passing_score}
        </p>
      </div>
      <div className="shrink-0 font-mono text-xs uppercase tracking-widest">
        {isActive && <span className="text-sage">resume</span>}
        {!isActive && lastAttempt && (
          <span
            className={lastAttempt.correctCount >= lastAttempt.passingScore ? 'text-sage' : 'text-ember'}
          >
            {lastAttempt.correctCount}/{lastAttempt.totalQuestions}
          </span>
        )}
        {!isActive && !lastAttempt && <span className="text-bone-dim/60">start →</span>}
      </div>
    </Link>
  )
}

export function TrackHomePage() {
  const { trackId } = useParams<{ trackId: TrackId }>()
  const { trackData } = useOutletContext<TrackOutletContext>()
  const [shortExamsOpen, setShortExamsOpen] = useState(false)

  const shortExamGroups = useMemo(() => {
    const groups = new Map<string, PracticeExam[]>()
    for (const exam of trackData.shortExams) {
      const key = exam.source_exam_title ?? 'Other'
      const list = groups.get(key) ?? []
      list.push(exam)
      groups.set(key, list)
    }
    return Array.from(groups.entries())
  }, [trackData.shortExams])

  const studyPack = trackData.studyPacks[0]

  return (
    <main className="mx-auto max-w-4xl px-6 py-10">
      <p className="font-mono text-xs uppercase tracking-[0.3em] text-brass">{trackData.info.label}</p>
      <h1 className="mt-2 font-display text-3xl font-semibold text-bone sm:text-4xl">
        {trackData.info.name}
      </h1>

      {studyPack && (
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          <Link
            to={`/${trackId}/notes`}
            className="ticket px-5 py-4 transition-transform hover:-translate-y-0.5"
          >
            <p className="font-mono text-xs uppercase tracking-widest text-brass">study pack</p>
            <p className="mt-1 font-display text-lg text-bone">Notes</p>
            <p className="mt-1 text-sm text-bone-dim">{studyPack.notes_sections.length} sections</p>
          </Link>
          <Link
            to={`/${trackId}/flashcards`}
            className="ticket px-5 py-4 transition-transform hover:-translate-y-0.5"
          >
            <p className="font-mono text-xs uppercase tracking-widest text-brass">study pack</p>
            <p className="mt-1 font-display text-lg text-bone">Flashcards</p>
            <p className="mt-1 text-sm text-bone-dim">{studyPack.flashcards.length} cards</p>
          </Link>
        </div>
      )}

      <section className="mt-10">
        <h2 className="font-display text-xl font-semibold text-bone">Full practice exams</h2>
        <p className="mt-1 text-sm text-bone-dim">
          60 questions across four scenarios, timed at the real exam's length.
        </p>
        <div className="mt-4 grid gap-3">
          {trackData.fullExams.map((exam) => (
            <ExamRow key={exam.id} trackId={trackId as TrackId} kind="full" exam={exam} />
          ))}
        </div>
      </section>

      <section className="mt-10">
        <button
          type="button"
          onClick={() => setShortExamsOpen((open) => !open)}
          className="flex w-full items-center justify-between font-display text-xl font-semibold text-bone"
        >
          <span>Short practice exams</span>
          <span className="font-mono text-sm text-bone-dim">
            {shortExamsOpen ? 'hide' : `show ${trackData.shortExams.length}`}
          </span>
        </button>
        <p className="mt-1 text-sm text-bone-dim">
          15-question drills, one per scenario from each full exam — good for a quick session.
        </p>
        {shortExamsOpen && (
          <div className="mt-4 space-y-6">
            {shortExamGroups.map(([title, exams]) => (
              <div key={title}>
                <p className="font-mono text-xs uppercase tracking-widest text-bone-dim">{title}</p>
                <div className="mt-2 grid gap-3">
                  {exams.map((exam) => (
                    <ExamRow key={exam.id} trackId={trackId as TrackId} kind="short" exam={exam} />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  )
}
