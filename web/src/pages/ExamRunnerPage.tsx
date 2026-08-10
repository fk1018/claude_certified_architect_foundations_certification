import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useOutletContext, useParams } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'
import {
  completeAttempt,
  discardActiveAttempt,
  loadProgress,
  startAttempt,
  updateActiveAnswers,
  updateActiveQuestion,
  type AnswerMap,
} from '../lib/progress'
import { scoreExam, toggleChoice } from '../lib/scoring'
import type { PracticeExam, TrackId } from '../types/domain'

function formatClock(totalSeconds: number): string {
  const clamped = Math.max(totalSeconds, 0)
  const minutes = Math.floor(clamped / 60)
  const seconds = clamped % 60
  return `${minutes}:${String(seconds).padStart(2, '0')}`
}

export function ExamRunnerPage() {
  const { trackId, kind, examId } = useParams<{
    trackId: TrackId
    kind: 'full' | 'short'
    examId: string
  }>()
  const { trackData } = useOutletContext<TrackOutletContext>()
  const navigate = useNavigate()

  const exam = useMemo<PracticeExam | undefined>(() => {
    const pool = kind === 'short' ? trackData.shortExams : trackData.fullExams
    return pool.find((e) => e.id === examId)
  }, [trackData, kind, examId])

  const [startedAt, setStartedAt] = useState<string | null>(null)
  const [answers, setAnswers] = useState<AnswerMap>({})
  const [current, setCurrent] = useState(0)
  const [now, setNow] = useState(() => Date.now())
  const submittedRef = useRef(false)

  useEffect(() => {
    if (!exam || !trackId || !kind) return
    const progress = loadProgress(trackId)
    if (progress.active?.examId === exam.id) {
      setStartedAt(progress.active.startedAt)
      setAnswers(progress.active.answers)
      setCurrent(progress.active.currentQuestion)
    } else {
      const active = {
        examId: exam.id,
        examTitle: exam.title,
        kind,
        startedAt: new Date().toISOString(),
        timeLimitMinutes: exam.time_limit_minutes,
        currentQuestion: 0,
        answers: {},
      }
      startAttempt(trackId, active)
      setStartedAt(active.startedAt)
      setAnswers({})
      setCurrent(0)
    }
    submittedRef.current = false
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [exam?.id, trackId, kind])

  useEffect(() => {
    const interval = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(interval)
  }, [])

  const secondsRemaining = useMemo(() => {
    if (!exam || !startedAt) return exam ? exam.time_limit_minutes * 60 : 0
    const elapsed = Math.floor((now - new Date(startedAt).getTime()) / 1000)
    return exam.time_limit_minutes * 60 - elapsed
  }, [exam, startedAt, now])

  function submit() {
    if (!exam || !trackId || !kind || !startedAt || submittedRef.current) return
    submittedRef.current = true
    const correctCount = scoreExam(exam, answers)
    completeAttempt(trackId, {
      examId: exam.id,
      examTitle: exam.title,
      kind,
      startedAt,
      submittedAt: new Date().toISOString(),
      answers,
      correctCount,
      totalQuestions: exam.questions.length,
      passingScore: exam.passing_score,
    })
    navigate(`/${trackId}/exam/${kind}/${exam.id}/results`, { replace: true })
  }

  useEffect(() => {
    if (secondsRemaining <= 0 && startedAt) {
      submit()
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [secondsRemaining <= 0])

  if (!exam || !trackId || !kind) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-10">
        <p className="text-bone-dim">That exam could not be found.</p>
      </main>
    )
  }

  // Re-bind as explicitly-typed locals: TS narrows `trackId`/`exam` from the guard
  // above in this scope, but that narrowing doesn't carry into the nested function
  // declarations below, which close over the original (possibly-undefined) types.
  const activeTrackId: TrackId = trackId
  const activeExam: PracticeExam = exam

  const question = activeExam.questions[current]
  const given = answers[String(question.number)] ?? []

  function select(letter: string) {
    const next = toggleChoice(given, letter, question.selection_count)
    const updatedAnswers = { ...answers, [String(question.number)]: next }
    setAnswers(updatedAnswers)
    updateActiveAnswers(activeTrackId, question.number, next)
  }

  function goTo(nextIndex: number) {
    const clamped = Math.max(0, Math.min(activeExam.questions.length - 1, nextIndex))
    setCurrent(clamped)
    updateActiveQuestion(activeTrackId, clamped)
  }

  const answeredCount = exam.questions.filter(
    (q) => (answers[String(q.number)] ?? []).length > 0,
  ).length
  const lowOnTime = secondsRemaining <= 300

  return (
    <main className="mx-auto max-w-3xl px-6 py-8">
      <div className="flex items-center justify-between font-mono text-xs uppercase tracking-widest text-bone-dim">
        <span className="text-brass">{question.scenario || exam.title}</span>
        <span className={lowOnTime ? 'text-ember' : 'text-bone'}>
          ⏱ {formatClock(secondsRemaining)}
        </span>
      </div>

      <div className="mt-3 flex gap-1">
        {exam.questions.map((q, i) => {
          const answered = (answers[String(q.number)] ?? []).length > 0
          return (
            <button
              key={q.id}
              type="button"
              aria-label={`Question ${q.number}`}
              onClick={() => goTo(i)}
              className={`h-1.5 flex-1 rounded-full transition-colors ${
                i === current
                  ? 'bg-brass'
                  : answered
                    ? 'bg-sage/60'
                    : 'bg-bone/15'
              }`}
            />
          )
        })}
      </div>
      <p className="mt-2 font-mono text-[11px] text-bone-dim">
        {answeredCount}/{exam.questions.length} answered
      </p>

      <div className="ticket mt-6 px-6 py-6">
        <p className="font-mono text-xs uppercase tracking-widest text-bone-dim">
          Question {question.number}
          {question.selection_count > 1 && (
            <span className="text-brass"> · select {question.selection_count}</span>
          )}
        </p>
        {question.scenario_context && (
          <p className="mt-3 text-sm text-bone-dim">{question.scenario_context}</p>
        )}
        <p className="mt-4 font-display text-lg leading-relaxed text-bone">{question.prompt}</p>

        <div className="mt-5 grid gap-2.5">
          {question.choices.map((choice) => {
            const selected = given.includes(choice.letter)
            return (
              <button
                key={choice.letter}
                type="button"
                onClick={() => select(choice.letter)}
                className={`flex items-start gap-3 rounded-md border px-4 py-3 text-left transition-colors ${
                  selected
                    ? 'border-brass bg-brass/10'
                    : 'border-bone/12 hover:border-bone/30'
                }`}
              >
                <span
                  className={`font-mono text-xs font-semibold ${selected ? 'text-brass' : 'text-bone-dim'}`}
                >
                  {choice.letter}
                </span>
                <span className="text-sm text-bone">{choice.text}</span>
              </button>
            )
          })}
        </div>
      </div>

      <div className="mt-6 flex items-center justify-between">
        <button
          type="button"
          onClick={() => goTo(current - 1)}
          disabled={current === 0}
          className="font-mono text-sm text-bone-dim hover:text-bone disabled:opacity-30"
        >
          ← prev
        </button>

        {current === exam.questions.length - 1 ? (
          <button
            type="button"
            onClick={submit}
            className="rounded border border-brass bg-brass/10 px-5 py-2 font-mono text-xs uppercase tracking-widest text-brass hover:bg-brass/20"
          >
            Submit exam
          </button>
        ) : (
          <button
            type="button"
            onClick={() => goTo(current + 1)}
            className="font-mono text-sm text-bone-dim hover:text-bone"
          >
            next →
          </button>
        )}

        <button
          type="button"
          onClick={() => {
            discardActiveAttempt(trackId)
            navigate(`/${trackId}`)
          }}
          className="font-mono text-xs uppercase tracking-widest text-bone-dim/60 hover:text-ember"
        >
          exit
        </button>
      </div>
    </main>
  )
}
