import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Outlet, Route, Routes } from 'react-router-dom'
import { loadProgress } from '../lib/progress'
import type { PracticeExam, TrackData, TrackId } from '../types/domain'
import { ExamRunnerPage } from './ExamRunnerPage'

const trackId: TrackId = 'architect-foundations'
const firstQuestion = {
  id: 'short-practice-exam-1:question:1',
  number: 1,
  scenario: 'Scenario one',
  scenario_context: 'Shared context.',
  prompt: 'Question one?',
  choices: [
    { letter: 'A', text: 'First answer' },
    { letter: 'B', text: 'Second answer' },
    { letter: 'C', text: 'Third answer' },
    { letter: 'D', text: 'Fourth answer' },
  ],
  correct_choices: ['A'],
  selection_count: 1,
  explanation: 'The first answer is correct.',
  distractors: {},
}
const secondQuestion = {
  ...firstQuestion,
  id: 'short-practice-exam-1:question:2',
  number: 2,
  prompt: 'Question two?',
  correct_choices: ['C'],
  explanation: 'The third answer is correct.',
}
const shortExam: PracticeExam = {
  id: 'short-practice-exam-1',
  title: 'Short Practice Exam 1',
  time_limit_minutes: 30,
  passing_score: 2,
  total_questions: 2,
  domain_distribution: [],
  questions: [firstQuestion, secondQuestion],
  source_exam_id: 'practice-exam-1',
  source_exam_title: 'Practice Exam 1',
  source_section_index: 1,
}
const fullExam: PracticeExam = {
  ...shortExam,
  id: 'practice-exam-1',
  title: 'Full Practice Exam 1',
  time_limit_minutes: 120,
}
const trackData: TrackData = {
  info: {
    id: trackId,
    label: 'Architect – Foundations',
    name: 'Claude Certified Architect – Foundations',
  },
  studyPacks: [],
  fullExams: [fullExam],
  shortExams: [shortExam],
}

function TestLayout() {
  return <Outlet context={{ trackData }} />
}

function renderRunner(kind: 'full' | 'short', examId: string) {
  return render(
    <MemoryRouter initialEntries={[`/${trackId}/exam/${kind}/${examId}`]}>
      <Routes>
        <Route path="/:trackId" element={<TestLayout />}>
          <Route path="exam/:kind/:examId" element={<ExamRunnerPage />} />
          <Route path="exam/:kind/:examId/results" element={<p>Results reached</p>} />
          <Route index element={<p>Track home</p>} />
        </Route>
      </Routes>
    </MemoryRouter>,
  )
}

function choiceButton(label: string): HTMLButtonElement {
  const text = screen.getByText(label)
  const button = text.closest('button')
  if (!(button instanceof HTMLButtonElement)) throw new Error(`No button found for ${label}`)
  return button
}

describe('short exam feedback modes', () => {
  beforeEach(() => localStorage.clear())
  afterEach(cleanup)

  it('waits for a mode choice before starting a short attempt', async () => {
    const user = userEvent.setup()
    renderRunner('short', shortExam.id)

    await screen.findByRole('heading', { name: 'When should feedback appear?' })
    expect(loadProgress(trackId).active).toBeNull()

    await user.click(screen.getByRole('button', { name: /After each question/ }))

    await screen.findByRole('button', { name: 'Check answer' })
    const active = loadProgress(trackId).active
    expect(active?.kind).toBe('short')
    if (active?.kind !== 'short') throw new Error('Expected a short attempt')
    expect(active.feedbackMode).toBe('immediate')
  })

  it('locks an immediate answer, explains a miss, and pauses until continue', async () => {
    const user = userEvent.setup()
    renderRunner('short', shortExam.id)
    await user.click(await screen.findByRole('button', { name: /After each question/ }))
    await user.click(choiceButton('Second answer'))
    await user.click(screen.getByRole('button', { name: 'Check answer' }))

    expect(await screen.findByText('Incorrect.')).not.toBeNull()
    expect(screen.getByText('The first answer is correct.')).not.toBeNull()
    expect(screen.getByText('paused')).not.toBeNull()
    expect(choiceButton('Second answer').disabled).toBe(true)
    expect(screen.queryByRole('button', { name: /next/i })).toBeNull()

    const pending = loadProgress(trackId).active
    expect(pending?.kind).toBe('short')
    if (pending?.kind !== 'short') throw new Error('Expected a short attempt')
    expect(pending.pendingFeedback?.questionNumber).toBe(1)

    await user.click(screen.getByRole('button', { name: 'Continue' }))

    expect(await screen.findByText('Question 2')).not.toBeNull()
    const continued = loadProgress(trackId).active
    expect(continued?.currentQuestion).toBe(1)
    if (continued?.kind !== 'short') throw new Error('Expected a short attempt')
    expect(continued.pendingFeedback).toBeNull()

    await user.click(choiceButton('Third answer'))
    await user.click(screen.getByRole('button', { name: 'Check answer' }))
    expect(await screen.findByText('Correct.')).not.toBeNull()
    await user.click(screen.getByRole('button', { name: 'Continue to results' }))

    expect(await screen.findByText('Results reached')).not.toBeNull()
    const completed = loadProgress(trackId)
    expect(completed.active).toBeNull()
    expect(completed.attempts[0].correctCount).toBe(1)
  })

  it('shows only a confirmation for a correct immediate answer', async () => {
    const user = userEvent.setup()
    renderRunner('short', shortExam.id)
    await user.click(await screen.findByRole('button', { name: /After each question/ }))
    await user.click(choiceButton('First answer'))
    await user.click(screen.getByRole('button', { name: 'Check answer' }))

    expect(await screen.findByText('Correct.')).not.toBeNull()
    expect(screen.queryByText('The first answer is correct.')).toBeNull()
    expect(screen.getByRole('button', { name: 'Continue' })).not.toBeNull()
  })

  it('keeps deferred mode freely navigable and silent until submission', async () => {
    const user = userEvent.setup()
    renderRunner('short', shortExam.id)
    await user.click(await screen.findByRole('button', { name: /At the end/ }))

    await user.click(choiceButton('Second answer'))
    expect(screen.queryByText('Incorrect.')).toBeNull()
    await user.click(screen.getByRole('button', { name: /next/i }))
    await user.click(choiceButton('Third answer'))
    await user.click(screen.getByRole('button', { name: 'Submit exam' }))

    expect(await screen.findByText('Results reached')).not.toBeNull()
    const progress = loadProgress(trackId)
    expect(progress.active).toBeNull()
    expect(progress.attempts[0].correctCount).toBe(1)
  })

  it('resumes persisted feedback with the timer still paused', async () => {
    const now = Date.now()
    localStorage.setItem(
      `ccafc-web:progress:${trackId}`,
      JSON.stringify({
        schemaVersion: 2,
        active: {
          examId: shortExam.id,
          examTitle: shortExam.title,
          kind: 'short',
          startedAt: new Date(now - 60_000).toISOString(),
          timeLimitMinutes: 30,
          currentQuestion: 0,
          answers: { '1': ['B'] },
          feedbackMode: 'immediate',
          pausedMilliseconds: 0,
          pendingFeedback: {
            questionNumber: 1,
            startedAt: new Date(now - 30_000).toISOString(),
          },
        },
        attempts: [],
        flashcards: {},
      }),
    )

    renderRunner('short', shortExam.id)

    expect(await screen.findByText('Incorrect.')).not.toBeNull()
    expect(screen.getByText('paused')).not.toBeNull()
    expect(screen.queryByRole('heading', { name: 'When should feedback appear?' })).toBeNull()
  })

  it('starts full exams directly without a feedback picker', async () => {
    renderRunner('full', fullExam.id)

    expect(await screen.findByText('Question 1')).not.toBeNull()
    expect(screen.queryByRole('heading', { name: 'When should feedback appear?' })).toBeNull()
    expect(loadProgress(trackId).active?.kind).toBe('full')
  })
})
