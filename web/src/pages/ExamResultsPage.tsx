import { useMemo } from 'react'
import { Link, useOutletContext, useParams } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'
import { loadProgress } from '../lib/progress'
import { isCorrect } from '../lib/scoring'
import type { PracticeExam, TrackId } from '../types/domain'

export function ExamResultsPage() {
  const { trackId, kind, examId } = useParams<{
    trackId: TrackId
    kind: 'full' | 'short'
    examId: string
  }>()
  const { trackData } = useOutletContext<TrackOutletContext>()

  const exam = useMemo<PracticeExam | undefined>(() => {
    const pool = kind === 'short' ? trackData.shortExams : trackData.fullExams
    return pool.find((e) => e.id === examId)
  }, [trackData, kind, examId])

  const attempt = useMemo(() => {
    if (!trackId) return undefined
    const progress = loadProgress(trackId)
    return progress.attempts.find((a) => a.examId === examId)
  }, [trackId, examId])

  if (!exam || !attempt || !trackId || !kind) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-10">
        <p className="text-bone-dim">No completed attempt found for this exam yet.</p>
        <Link to={`/${trackId ?? ''}`} className="mt-4 inline-block text-brass hover:underline">
          Back to exams
        </Link>
      </main>
    )
  }

  const passed = attempt.correctCount >= attempt.passingScore
  const pct = Math.round((attempt.correctCount / attempt.totalQuestions) * 100)

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <div className="ticket stamp-in flex flex-col items-center gap-4 px-8 py-10 text-center">
        <div
          className={`seal flex h-28 w-28 flex-col items-center justify-center rounded-full ${
            passed ? '' : 'opacity-90'
          }`}
        >
          <span className="font-display text-3xl font-bold text-bone">
            {attempt.correctCount}/{attempt.totalQuestions}
          </span>
          <span className={`font-mono text-[10px] uppercase tracking-widest ${passed ? 'text-sage' : 'text-ember'}`}>
            {passed ? 'pass' : 'retry'}
          </span>
        </div>
        <div>
          <p className="font-display text-xl text-bone">{attempt.examTitle}</p>
          <p className="mt-1 font-mono text-xs uppercase tracking-widest text-bone-dim">
            {pct}% · needed ≥ {attempt.passingScore}/{attempt.totalQuestions} to pass
          </p>
        </div>
        <Link
          to={`/${trackId}/exam/${kind}/${exam.id}`}
          className="rounded border border-brass/40 px-4 py-2 font-mono text-xs uppercase tracking-widest text-brass hover:bg-brass/10"
        >
          retake exam
        </Link>
      </div>

      <h2 className="mt-10 font-display text-xl font-semibold text-bone">Answer review</h2>
      <div className="mt-4 space-y-4">
        {exam.questions.map((question) => {
          const given = attempt.answers[String(question.number)] ?? []
          const correct = isCorrect(question, given)
          return (
            <article key={question.id} className="ticket px-5 py-4">
              <div className="flex items-center justify-between font-mono text-[11px] uppercase tracking-widest">
                <span className="text-bone-dim">Question {question.number}</span>
                <span className={correct ? 'text-sage' : 'text-ember'}>
                  {correct ? 'correct' : 'missed'}
                </span>
              </div>
              <p className="mt-2 text-sm text-bone">{question.prompt}</p>
              <div className="mt-3 grid gap-1.5 font-mono text-xs">
                {question.choices.map((choice) => {
                  const wasGiven = given.includes(choice.letter)
                  const isKey = question.correct_choices.includes(choice.letter)
                  return (
                    <div
                      key={choice.letter}
                      className={`flex gap-2 rounded px-2 py-1 ${
                        isKey
                          ? 'bg-sage/10 text-sage'
                          : wasGiven
                            ? 'bg-ember/10 text-ember'
                            : 'text-bone-dim'
                      }`}
                    >
                      <span className="font-semibold">{choice.letter}</span>
                      <span className="normal-case text-[13px]">{choice.text}</span>
                    </div>
                  )
                })}
              </div>
              {question.explanation && (
                <p className="mt-3 text-sm leading-relaxed text-bone-dim">
                  {question.explanation}
                </p>
              )}
            </article>
          )
        })}
      </div>

      <Link to={`/${trackId}`} className="mt-8 inline-block text-brass hover:underline">
        ← back to exams
      </Link>
    </main>
  )
}
