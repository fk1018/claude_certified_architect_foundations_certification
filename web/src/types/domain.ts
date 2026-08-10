// Mirrors the JSON shape produced by cli/src/ccafc_cli/models.py's to_dict() methods.
// This is the CLI's data contract — keep in sync by hand if models.py changes.

export type TrackId = 'architect-foundations' | 'developer-foundations' | 'architect-professional'

export interface TrackInfo {
  id: TrackId
  label: string
  name: string
}

export interface Manifest {
  tracks: TrackInfo[]
}

export interface Choice {
  letter: string
  text: string
}

export interface Question {
  id: string
  number: number
  scenario: string
  scenario_context: string
  prompt: string
  choices: Choice[]
  correct_choices: string[]
  selection_count: number
  explanation: string
  distractors: Record<string, string>
  source_question_id?: string
  source_question_number?: number
}

export interface DomainRow {
  domain: string
  questions: string
}

export interface PracticeExam {
  id: string
  title: string
  time_limit_minutes: number
  passing_score: number
  total_questions: number
  domain_distribution: DomainRow[]
  questions: Question[]
  source_exam_id?: string
  source_exam_title?: string
  source_section_index?: number
  source_scenario?: string
}

export interface NoteSection {
  id: string
  title: string
  body: string
}

export interface Flashcard {
  id: string
  pack_id: string
  topic: string
  question: string
  answer: string
}

export interface StudyPack {
  id: string
  title: string
  source_url: string
  notes_sections: NoteSection[]
  flashcards: Flashcard[]
  practice_questions: Question[]
}

export interface PracticeExamsPayload {
  schema_version: number
  generated_at: string
  practice_exams: PracticeExam[]
  short_practice_exams: PracticeExam[]
}

export interface StudyPacksPayload {
  schema_version: number
  generated_at: string
  study_packs: StudyPack[]
}

export interface TrackData {
  info: TrackInfo
  studyPacks: StudyPack[]
  fullExams: PracticeExam[]
  shortExams: PracticeExam[]
}
