import { beforeEach, describe, expect, it } from 'vitest'
import {
  loadProgress,
  secondsRemainingForAttempt,
  type FullActiveAttempt,
  type ShortActiveAttempt,
} from './progress'
import type { TrackId } from '../types/domain'

const trackId: TrackId = 'architect-foundations'
const storageKey = `ccafc-web:progress:${trackId}`

describe('browser progress', () => {
  beforeEach(() => localStorage.clear())

  it('migrates a legacy short attempt to deferred feedback', () => {
    localStorage.setItem(
      storageKey,
      JSON.stringify({
        schemaVersion: 1,
        active: {
          examId: 'short-practice-exam-1',
          examTitle: 'Short Exam 1',
          kind: 'short',
          startedAt: '2026-08-10T12:00:00.000Z',
          timeLimitMinutes: 30,
          currentQuestion: 3,
          answers: { '1': ['A'] },
        },
        attempts: [],
        flashcards: {},
      }),
    )

    const progress = loadProgress(trackId)

    expect(progress.schemaVersion).toBe(2)
    expect(progress.active?.kind).toBe('short')
    if (progress.active?.kind !== 'short') throw new Error('Expected a short attempt')
    expect(progress.active.feedbackMode).toBe('deferred')
    expect(progress.active.pausedMilliseconds).toBe(0)
    expect(progress.active.pendingFeedback).toBeNull()
  })

  it('freezes an immediate-mode timer at feedback and accounts for prior pauses', () => {
    const active: ShortActiveAttempt = {
      examId: 'short-practice-exam-1',
      examTitle: 'Short Exam 1',
      kind: 'short',
      startedAt: '2026-08-10T12:00:00.000Z',
      timeLimitMinutes: 30,
      currentQuestion: 1,
      answers: { '1': ['B'] },
      feedbackMode: 'immediate',
      pausedMilliseconds: 120_000,
      pendingFeedback: {
        questionNumber: 1,
        startedAt: '2026-08-10T12:10:00.000Z',
      },
    }

    expect(
      secondsRemainingForAttempt(active, new Date('2026-08-10T12:20:00.000Z').getTime()),
    ).toBe(22 * 60)
    expect(
      secondsRemainingForAttempt(
        { ...active, pendingFeedback: null },
        new Date('2026-08-10T12:20:00.000Z').getTime(),
      ),
    ).toBe(12 * 60)
  })

  it('keeps the standard countdown for a full exam', () => {
    const active: FullActiveAttempt = {
      examId: 'practice-exam-1',
      examTitle: 'Full Exam 1',
      kind: 'full',
      startedAt: '2026-08-10T12:00:00.000Z',
      timeLimitMinutes: 120,
      currentQuestion: 0,
      answers: {},
    }

    expect(
      secondsRemainingForAttempt(active, new Date('2026-08-10T12:05:00.000Z').getTime()),
    ).toBe(115 * 60)
  })
})
