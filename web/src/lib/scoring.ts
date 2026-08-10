import type { PracticeExam, Question } from '../types/domain'
import type { AnswerMap } from './progress'

export function isCorrect(question: Question, given: string[] | undefined): boolean {
  if (!given || given.length !== question.correct_choices.length) return false
  const correctSet = new Set(question.correct_choices)
  return given.every((letter) => correctSet.has(letter))
}

export function scoreExam(exam: PracticeExam, answers: AnswerMap): number {
  return exam.questions.reduce(
    (total, question) => total + (isCorrect(question, answers[String(question.number)]) ? 1 : 0),
    0,
  )
}

export function toggleChoice(
  current: string[] | undefined,
  letter: string,
  selectionCount: number,
): string[] {
  const set = new Set(current ?? [])
  if (set.has(letter)) {
    set.delete(letter)
    return Array.from(set)
  }
  if (selectionCount <= 1) return [letter]
  if (set.size >= selectionCount) return Array.from(set)
  set.add(letter)
  return Array.from(set).sort()
}
