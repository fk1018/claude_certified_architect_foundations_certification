import { useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useOutletContext, useParams } from 'react-router-dom'
import type { TrackOutletContext } from '../components/TrackLayout'
import {
  completeAttempt,
  discardActiveAttempt,
  loadProgress,
  replaceActiveAttempt,
  secondsRemainingForAttempt,
  startAttempt,
  type ActiveAttempt,
  type FullActiveAttempt,
  type ShortActiveAttempt,
  type ShortExamFeedbackMode,
} from '../lib/progress'
import { isCorrect, scoreExam, toggleChoice } from '../lib/scoring'
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
    return pool.find((item) => item.id === examId)
  }, [trackData, kind, examId])

  const [active, setActive] = useState<ActiveAttempt | null>(null)
  const [ready, setReady] = useState(false)
  const [now, setNow] = useState(() => Date.now())
  const submittedRef = useRef(false)

  useEffect(() => {
    if (!exam || !trackId || !kind) return

    setReady(false)
    const progress = loadProgress(trackId)
    let nextActive: ActiveAttempt | null = null

    if (progress.active?.examId === exam.id && progress.active.kind === kind) {
      nextActive = progress.active
    } else if (kind === 'full') {
      const startedAt = new Date().toISOString()
      const fullAttempt: FullActiveAttempt = {
        examId: exam.id,
        examTitle: exam.title,
        kind: 'full',
        startedAt,
        timeLimitMinutes: exam.time_limit_minutes,
        currentQuestion: 0,
        answers: {},
      }
      startAttempt(trackId, fullAttempt)
      nextActive = fullAttempt
    }

    setActive(nextActive)
    setNow(Date.now())
    setReady(true)
    submittedRef.current = false
  }, [exam, trackId, kind])

  useEffect(() => {
    const interval = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(interval)
  }, [])

  const secondsRemaining = useMemo(
    () => (active ? secondsRemainingForAttempt(active, now) : (exam?.time_limit_minutes ?? 0) * 60),
    [active, exam?.time_limit_minutes, now],
  )

  function submit(attemptState: ActiveAttempt | null = active) {
    if (!exam || !trackId || !kind || !attemptState || submittedRef.current) return
    submittedRef.current = true
    const correctCount = scoreExam(exam, attemptState.answers)
    completeAttempt(trackId, {
      examId: exam.id,
      examTitle: exam.title,
      kind,
      startedAt: attemptState.startedAt,
      submittedAt: new Date().toISOString(),
      answers: attemptState.answers,
      correctCount,
      totalQuestions: exam.questions.length,
      passingScore: exam.passing_score,
    })
    navigate(`/${trackId}/exam/${kind}/${exam.id}/results`, { replace: true })
  }

  const feedbackPending = active?.kind === 'short' && active.pendingFeedback !== null

  useEffect(() => {
    if (secondsRemaining <= 0 && active && !feedbackPending) submit()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [secondsRemaining <= 0, feedbackPending])

  if (!exam || !trackId || !kind) {
    return (
      <main className="mx-auto max-w-4xl px-6 py-10">
        <p className="text-bone-dim">That exam could not be found.</p>
      </main>
    )
  }

  if (!ready) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-10">
        <p className="font-mono text-xs uppercase tracking-widest text-bone-dim">Loading exam…</p>
      </main>
    )
  }

  const activeTrackId: TrackId = trackId
  const activeExam: PracticeExam = exam

  function beginShortAttempt(feedbackMode: ShortExamFeedbackMode) {
    const startedAt = new Date().toISOString()
    const shortAttempt: ShortActiveAttempt = {
      examId: activeExam.id,
      examTitle: activeExam.title,
      kind: 'short',
      startedAt,
      timeLimitMinutes: activeExam.time_limit_minutes,
      currentQuestion: 0,
      answers: {},
      feedbackMode,
      pausedMilliseconds: 0,
      pendingFeedback: null,
    }
    startAttempt(activeTrackId, shortAttempt)
    setActive(shortAttempt)
    setNow(Date.now())
  }

  if (kind === 'short' && !active) {
    return (
      <main className="mx-auto max-w-3xl px-6 py-10">
        <p className="font-mono text-xs uppercase tracking-[0.25em] text-brass">Short practice exam</p>
        <h1 className="mt-2 font-display text-3xl font-semibold text-bone">{exam.title}</h1>
        <p className="mt-2 text-sm text-bone-dim">
          {exam.questions.length} questions · {exam.time_limit_minutes} minutes · the timer starts
          after you choose
        </p>

        <section className="ticket mt-8 px-6 py-6">
          <h2 className="font-display text-xl font-semibold text-bone">When should feedback appear?</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2">
            <button
              type="button"
              onClick={() => beginShortAttempt('immediate')}
              className="rounded-md border border-brass/45 bg-brass/5 px-5 py-5 text-left transition-colors hover:bg-brass/10"
            >
              <span className="font-display text-lg text-bone">After each question</span>
              <span className="mt-2 block text-sm leading-relaxed text-bone-dim">
                Confirm correct responses and explain misses. Answers lock and the timer pauses until
                you continue.
              </span>
            </button>
            <button
              type="button"
              onClick={() => beginShortAttempt('deferred')}
              className="rounded-md border border-bone/15 px-5 py-5 text-left transition-colors hover:border-bone/30"
            >
              <span className="font-display text-lg text-bone">At the end</span>
              <span className="mt-2 block text-sm leading-relaxed text-bone-dim">
                Move freely through the exam, then see your score, correct answers, and explanations
                after submission.
              </span>
            </button>
          </div>
        </section>

        <button
          type="button"
          onClick={() => navigate(`/${trackId}`)}
          className="mt-6 font-mono text-sm text-bone-dim hover:text-bone"
        >
          ← back to exams
        </button>
      </main>
    )
  }

  if (!active) return null

  // Re-bind after the guard so nested handlers retain the non-null narrowing.
  const activeAttempt: ActiveAttempt = active
  const current = Math.max(
    0,
    Math.min(activeExam.questions.length - 1, activeAttempt.currentQuestion),
  )
  const question = activeExam.questions[current]
  const given = activeAttempt.answers[String(question.number)] ?? []
  const immediateFeedback =
    activeAttempt.kind === 'short' && activeAttempt.feedbackMode === 'immediate'
  const showingFeedback =
    immediateFeedback && activeAttempt.pendingFeedback?.questionNumber === question.number
  const responseIsCorrect = showingFeedback && isCorrect(question, given)
  const missingChoices = question.correct_choices.filter((letter) => !given.includes(letter))
  const extraChoices = given.filter((letter) => !question.correct_choices.includes(letter))

  function saveActive(nextActive: ActiveAttempt) {
    replaceActiveAttempt(activeTrackId, nextActive)
    setActive(nextActive)
  }

  function select(letter: string) {
    if (showingFeedback) return
    const next = toggleChoice(given, letter, question.selection_count)
    saveActive({
      ...activeAttempt,
      answers: { ...activeAttempt.answers, [String(question.number)]: next },
    })
  }

  function goTo(nextIndex: number) {
    if (immediateFeedback) return
    const clamped = Math.max(0, Math.min(activeExam.questions.length - 1, nextIndex))
    saveActive({ ...activeAttempt, currentQuestion: clamped })
  }

  function checkAnswer() {
    if (
      activeAttempt.kind !== 'short' ||
      activeAttempt.feedbackMode !== 'immediate' ||
      activeAttempt.pendingFeedback ||
      given.length !== question.selection_count
    ) {
      return
    }

    const nextActive: ShortActiveAttempt = {
      ...activeAttempt,
      pendingFeedback: {
        questionNumber: question.number,
        startedAt: new Date().toISOString(),
      },
    }
    saveActive(nextActive)
  }

  function continueAfterFeedback() {
    if (activeAttempt.kind !== 'short' || !activeAttempt.pendingFeedback) return

    const finishedAt = Date.now()
    const feedbackStartedAt = new Date(activeAttempt.pendingFeedback.startedAt).getTime()
    const pausedFor = Number.isFinite(feedbackStartedAt)
      ? Math.max(finishedAt - feedbackStartedAt, 0)
      : 0
    const nextActive: ShortActiveAttempt = {
      ...activeAttempt,
      currentQuestion:
        current === activeExam.questions.length - 1 ? current : Math.min(current + 1, activeExam.questions.length - 1),
      pausedMilliseconds: activeAttempt.pausedMilliseconds + pausedFor,
      pendingFeedback: null,
    }

    if (current === activeExam.questions.length - 1) {
      submit(nextActive)
      return
    }

    saveActive(nextActive)
    setNow(finishedAt)
  }

  const answeredCount = exam.questions.filter(
    (item) => (activeAttempt.answers[String(item.number)] ?? []).length > 0,
  ).length
  const lowOnTime = secondsRemaining <= 300

  return (
    <main className="mx-auto max-w-3xl px-6 py-8">
      <div className="flex items-center justify-between font-mono text-xs uppercase tracking-widest text-bone-dim">
        <span className="text-brass">{question.scenario || exam.title}</span>
        <span className={lowOnTime ? 'text-ember' : 'text-bone'}>
          ⏱ {formatClock(secondsRemaining)}
          {showingFeedback && <span className="ml-2 text-sage">paused</span>}
        </span>
      </div>

      <div className="mt-3 flex gap-1">
        {exam.questions.map((item, index) => {
          const answered = (activeAttempt.answers[String(item.number)] ?? []).length > 0
          const classes = `h-1.5 flex-1 rounded-full transition-colors ${
            index === current ? 'bg-brass' : answered ? 'bg-sage/60' : 'bg-bone/15'
          }`
          return immediateFeedback ? (
            <span key={item.id} className={classes} />
          ) : (
            <button
              key={item.id}
              type="button"
              aria-label={`Question ${item.number}`}
              onClick={() => goTo(index)}
              className={classes}
            />
          )
        })}
      </div>
      <div className="mt-2 flex items-center justify-between font-mono text-[11px] text-bone-dim">
        <span>
          {answeredCount}/{exam.questions.length} answered
        </span>
        {activeAttempt.kind === 'short' && (
          <span>{immediateFeedback ? 'feedback after each question' : 'feedback at the end'}</span>
        )}
      </div>

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
            const isKey = question.correct_choices.includes(choice.letter)
            let choiceClasses = selected
              ? 'border-brass bg-brass/10'
              : 'border-bone/12 hover:border-bone/30'
            let letterClasses = selected ? 'text-brass' : 'text-bone-dim'

            if (showingFeedback) {
              if (responseIsCorrect && selected) {
                choiceClasses = 'border-sage/50 bg-sage/10'
                letterClasses = 'text-sage'
              } else if (!responseIsCorrect && isKey) {
                choiceClasses = 'border-sage/50 bg-sage/10'
                letterClasses = 'text-sage'
              } else if (!responseIsCorrect && selected) {
                choiceClasses = 'border-ember/50 bg-ember/10'
                letterClasses = 'text-ember'
              } else {
                choiceClasses = 'border-bone/10 opacity-60'
                letterClasses = 'text-bone-dim'
              }
            }

            return (
              <button
                key={choice.letter}
                type="button"
                onClick={() => select(choice.letter)}
                disabled={showingFeedback}
                className={`flex items-start gap-3 rounded-md border px-4 py-3 text-left transition-colors ${choiceClasses}`}
              >
                <span className={`font-mono text-xs font-semibold ${letterClasses}`}>
                  {choice.letter}
                </span>
                <span className="text-sm text-bone">{choice.text}</span>
              </button>
            )
          })}
        </div>

        {showingFeedback && (
          <div
            role="status"
            className={`mt-5 rounded-md border px-4 py-4 ${
              responseIsCorrect
                ? 'border-sage/35 bg-sage/5'
                : 'border-ember/35 bg-ember/5'
            }`}
          >
            <p className={`font-display text-lg ${responseIsCorrect ? 'text-sage' : 'text-ember'}`}>
              {responseIsCorrect ? 'Correct.' : 'Incorrect.'}
            </p>
            {!responseIsCorrect && (
              <>
                <p className="mt-2 font-mono text-xs text-bone-dim">
                  Your answer: {given.join(', ') || 'unanswered'} · Correct answer:{' '}
                  {question.correct_choices.join(', ')}
                </p>
                {question.selection_count > 1 && (missingChoices.length > 0 || extraChoices.length > 0) && (
                  <p className="mt-1 font-mono text-xs text-bone-dim">
                    {missingChoices.length > 0 && `Missing: ${missingChoices.join(', ')}`}
                    {missingChoices.length > 0 && extraChoices.length > 0 && ' · '}
                    {extraChoices.length > 0 && `Extra: ${extraChoices.join(', ')}`}
                  </p>
                )}
                {question.explanation && (
                  <p className="mt-3 text-sm leading-relaxed text-bone-dim">
                    {question.explanation}
                  </p>
                )}
              </>
            )}
          </div>
        )}
      </div>

      <div className="mt-6 flex items-center justify-between gap-4">
        {immediateFeedback ? (
          <>
            <span className="font-mono text-xs uppercase tracking-widest text-bone-dim/60">
              answers lock on check
            </span>
            {showingFeedback ? (
              <button
                type="button"
                onClick={continueAfterFeedback}
                className="rounded border border-brass bg-brass/10 px-5 py-2 font-mono text-xs uppercase tracking-widest text-brass hover:bg-brass/20"
              >
                {current === exam.questions.length - 1 ? 'Continue to results' : 'Continue'}
              </button>
            ) : (
              <button
                type="button"
                onClick={checkAnswer}
                disabled={given.length !== question.selection_count}
                className="rounded border border-brass bg-brass/10 px-5 py-2 font-mono text-xs uppercase tracking-widest text-brass hover:bg-brass/20 disabled:cursor-not-allowed disabled:opacity-35"
              >
                Check answer
              </button>
            )}
          </>
        ) : (
          <>
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
                onClick={() => submit()}
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
          </>
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
