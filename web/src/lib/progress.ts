import type { TrackId } from '../types/domain'

// Mirrors the shape of cli/src/ccafc_cli/storage.py's progress.json, adapted for
// browser storage: one record per track, kept in localStorage instead of a state
// directory, since this app has no backend to persist attempts against.

export type AnswerMap = Record<string, string[]>
export type ShortExamFeedbackMode = 'immediate' | 'deferred'

interface ActiveAttemptBase {
  examId: string
  examTitle: string
  startedAt: string
  timeLimitMinutes: number
  currentQuestion: number
  answers: AnswerMap
}

export interface FullActiveAttempt extends ActiveAttemptBase {
  kind: 'full'
}

export interface PendingFeedback {
  questionNumber: number
  startedAt: string
}

export interface ShortActiveAttempt extends ActiveAttemptBase {
  kind: 'short'
  feedbackMode: ShortExamFeedbackMode
  pausedMilliseconds: number
  pendingFeedback: PendingFeedback | null
}

export type ActiveAttempt = FullActiveAttempt | ShortActiveAttempt

export function secondsRemainingForAttempt(
  active: ActiveAttempt,
  nowMilliseconds: number,
): number {
  const startedAt = new Date(active.startedAt).getTime()
  if (!Number.isFinite(startedAt)) return active.timeLimitMinutes * 60

  let effectiveNow = nowMilliseconds
  let pausedMilliseconds = 0
  if (active.kind === 'short') {
    pausedMilliseconds = active.pausedMilliseconds
    if (active.pendingFeedback) {
      const feedbackStartedAt = new Date(active.pendingFeedback.startedAt).getTime()
      if (Number.isFinite(feedbackStartedAt)) effectiveNow = feedbackStartedAt
    }
  }

  const elapsedSeconds = Math.floor(
    Math.max(effectiveNow - startedAt - pausedMilliseconds, 0) / 1000,
  )
  return active.timeLimitMinutes * 60 - elapsedSeconds
}

export interface ExamAttempt {
  examId: string
  examTitle: string
  kind: 'full' | 'short'
  startedAt: string
  submittedAt: string
  answers: AnswerMap
  correctCount: number
  totalQuestions: number
  passingScore: number
}

export interface FlashcardState {
  known: boolean
}

export interface TrackProgress {
  schemaVersion: 2
  active: ActiveAttempt | null
  attempts: ExamAttempt[]
  flashcards: Record<string, FlashcardState>
}

function defaultProgress(): TrackProgress {
  return { schemaVersion: 2, active: null, attempts: [], flashcards: {} }
}

const storageKey = (trackId: TrackId) => `ccafc-web:progress:${trackId}`

function migrateActiveAttempt(value: unknown): ActiveAttempt | null {
  if (!value || typeof value !== 'object') return null

  const candidate = value as Partial<ActiveAttempt> & Record<string, unknown>
  if (candidate.kind !== 'full' && candidate.kind !== 'short') return null

  const common = {
    examId: String(candidate.examId ?? ''),
    examTitle: String(candidate.examTitle ?? ''),
    startedAt: String(candidate.startedAt ?? ''),
    timeLimitMinutes: Number(candidate.timeLimitMinutes ?? 0),
    currentQuestion: Number(candidate.currentQuestion ?? 0),
    answers:
      candidate.answers && typeof candidate.answers === 'object'
        ? (candidate.answers as AnswerMap)
        : {},
  }

  if (candidate.kind === 'full') return { ...common, kind: 'full' }

  const feedbackMode =
    candidate.feedbackMode === 'immediate' || candidate.feedbackMode === 'deferred'
      ? candidate.feedbackMode
      : 'deferred'
  const pausedMilliseconds = Number(candidate.pausedMilliseconds ?? 0)
  const pending = candidate.pendingFeedback
  const pendingFeedback =
    pending &&
    typeof pending === 'object' &&
    typeof (pending as Record<string, unknown>).questionNumber === 'number' &&
    typeof (pending as Record<string, unknown>).startedAt === 'string'
      ? (pending as PendingFeedback)
      : null

  return {
    ...common,
    kind: 'short',
    feedbackMode,
    pausedMilliseconds:
      Number.isFinite(pausedMilliseconds) && pausedMilliseconds > 0 ? pausedMilliseconds : 0,
    pendingFeedback,
  }
}

export function loadProgress(trackId: TrackId): TrackProgress {
  try {
    const raw = localStorage.getItem(storageKey(trackId))
    if (!raw) return defaultProgress()
    const parsed = JSON.parse(raw) as Partial<TrackProgress>
    return {
      schemaVersion: 2,
      active: migrateActiveAttempt(parsed.active),
      attempts: Array.isArray(parsed.attempts) ? parsed.attempts : [],
      flashcards:
        parsed.flashcards && typeof parsed.flashcards === 'object' ? parsed.flashcards : {},
    }
  } catch {
    return defaultProgress()
  }
}

export function saveProgress(trackId: TrackId, progress: TrackProgress): void {
  localStorage.setItem(storageKey(trackId), JSON.stringify(progress))
}

export function startAttempt(trackId: TrackId, active: ActiveAttempt): TrackProgress {
  const progress = loadProgress(trackId)
  progress.active = active
  saveProgress(trackId, progress)
  return progress
}

export function replaceActiveAttempt(trackId: TrackId, active: ActiveAttempt): TrackProgress {
  const progress = loadProgress(trackId)
  progress.active = active
  saveProgress(trackId, progress)
  return progress
}

export function completeAttempt(trackId: TrackId, attempt: ExamAttempt): TrackProgress {
  const progress = loadProgress(trackId)
  progress.active = null
  progress.attempts = [attempt, ...progress.attempts].slice(0, 50)
  saveProgress(trackId, progress)
  return progress
}

export function discardActiveAttempt(trackId: TrackId): TrackProgress {
  const progress = loadProgress(trackId)
  progress.active = null
  saveProgress(trackId, progress)
  return progress
}

export function setFlashcardKnown(
  trackId: TrackId,
  cardId: string,
  known: boolean,
): TrackProgress {
  const progress = loadProgress(trackId)
  progress.flashcards[cardId] = { known }
  saveProgress(trackId, progress)
  return progress
}
