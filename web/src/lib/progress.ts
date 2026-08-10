import type { TrackId } from '../types/domain'

// Mirrors the shape of cli/src/ccafc_cli/storage.py's progress.json, adapted for
// browser storage: one record per track, kept in localStorage instead of a state
// directory, since this app has no backend to persist attempts against.

export type AnswerMap = Record<string, string[]>

export interface ActiveAttempt {
  examId: string
  examTitle: string
  kind: 'full' | 'short'
  startedAt: string
  timeLimitMinutes: number
  currentQuestion: number
  answers: AnswerMap
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
  schemaVersion: 1
  active: ActiveAttempt | null
  attempts: ExamAttempt[]
  flashcards: Record<string, FlashcardState>
}

function defaultProgress(): TrackProgress {
  return { schemaVersion: 1, active: null, attempts: [], flashcards: {} }
}

const storageKey = (trackId: TrackId) => `ccafc-web:progress:${trackId}`

export function loadProgress(trackId: TrackId): TrackProgress {
  try {
    const raw = localStorage.getItem(storageKey(trackId))
    if (!raw) return defaultProgress()
    const parsed = JSON.parse(raw) as Partial<TrackProgress>
    return {
      schemaVersion: 1,
      active: parsed.active ?? null,
      attempts: parsed.attempts ?? [],
      flashcards: parsed.flashcards ?? {},
    }
  } catch {
    return defaultProgress()
  }
}

export function saveProgress(trackId: TrackId, progress: TrackProgress): void {
  localStorage.setItem(storageKey(trackId), JSON.stringify(progress))
}

export function startAttempt(
  trackId: TrackId,
  active: ActiveAttempt,
): TrackProgress {
  const progress = loadProgress(trackId)
  progress.active = active
  saveProgress(trackId, progress)
  return progress
}

export function updateActiveAnswers(
  trackId: TrackId,
  questionNumber: number,
  letters: string[],
): TrackProgress {
  const progress = loadProgress(trackId)
  if (!progress.active) return progress
  progress.active.answers[String(questionNumber)] = letters
  saveProgress(trackId, progress)
  return progress
}

export function updateActiveQuestion(trackId: TrackId, currentQuestion: number): TrackProgress {
  const progress = loadProgress(trackId)
  if (!progress.active) return progress
  progress.active.currentQuestion = currentQuestion
  saveProgress(trackId, progress)
  return progress
}

export function completeAttempt(
  trackId: TrackId,
  attempt: ExamAttempt,
): TrackProgress {
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
