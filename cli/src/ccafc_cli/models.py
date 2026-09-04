from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


Choice = dict[str, str]


@dataclass
class NoteSection:
    id: str
    title: str
    body: str

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "title": self.title, "body": self.body}


@dataclass
class Flashcard:
    id: str
    pack_id: str
    topic: str
    question: str
    answer: str
    example: str | None = None
    domain: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "pack_id": self.pack_id,
            "topic": self.topic,
            "question": self.question,
            "answer": self.answer,
            "example": self.example,
            "domain": self.domain,
        }


@dataclass
class Question:
    id: str
    number: int
    prompt: str
    choices: list[Choice]
    correct_choices: list[str]
    selection_count: int
    explanation: str
    scenario: str = ""
    scenario_context: str = ""
    distractors: dict[str, str] = field(default_factory=dict)
    source_question_id: str = ""
    source_question_number: int | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "number": self.number,
            "scenario": self.scenario,
            "scenario_context": self.scenario_context,
            "prompt": self.prompt,
            "choices": self.choices,
            "correct_choices": self.correct_choices,
            "selection_count": self.selection_count,
            "explanation": self.explanation,
            "distractors": self.distractors,
        }
        if self.source_question_id:
            payload["source_question_id"] = self.source_question_id
        if self.source_question_number is not None:
            payload["source_question_number"] = self.source_question_number
        return payload


@dataclass
class StudyPack:
    id: str
    title: str
    source_url: str
    notes_sections: list[NoteSection]
    flashcards: list[Flashcard]
    practice_questions: list[Question]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "source_url": self.source_url,
            "notes_sections": [section.to_dict() for section in self.notes_sections],
            "flashcards": [card.to_dict() for card in self.flashcards],
            "practice_questions": [question.to_dict() for question in self.practice_questions],
        }


@dataclass
class PracticeExam:
    id: str
    title: str
    time_limit_minutes: int
    passing_score: int
    total_questions: int
    domain_distribution: list[dict[str, str]]
    questions: list[Question]
    source_exam_id: str = ""
    source_exam_title: str = ""
    source_section_index: int | None = None
    source_scenario: str = ""

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "id": self.id,
            "title": self.title,
            "time_limit_minutes": self.time_limit_minutes,
            "passing_score": self.passing_score,
            "total_questions": self.total_questions,
            "domain_distribution": self.domain_distribution,
            "questions": [question.to_dict() for question in self.questions],
        }
        if self.source_exam_id:
            payload["source_exam_id"] = self.source_exam_id
        if self.source_exam_title:
            payload["source_exam_title"] = self.source_exam_title
        if self.source_section_index is not None:
            payload["source_section_index"] = self.source_section_index
        if self.source_scenario:
            payload["source_scenario"] = self.source_scenario
        return payload
