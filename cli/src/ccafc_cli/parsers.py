from __future__ import annotations

import re
from dataclasses import replace
from itertools import groupby
from pathlib import Path

from ccafc_cli.models import Flashcard, NoteSection, PracticeExam, Question, StudyPack
from ccafc_cli.paths import PRACTICE_EXAMS_DIR, STUDY_PACKS_DIR, TRACK_LABEL


HEADING_RE = re.compile(r"(?m)^##\s+(.+?)\s*$")
FULL_EXAM_QUESTION_RE = re.compile(
    r"(?ims)^\*\*Question\s+(\d+)\.(?:\s+\(Select\s+(ONE|TWO|THREE|FOUR)\s+responses?\.\))?\*\*\s*"
    r"(.*?)(?=^\*\*Question\s+\d+\.(?:\s+\(Select\s+(?:ONE|TWO|THREE|FOUR)\s+responses?\.\))?\*\*|"
    r"^# Answer Key|\Z)"
)
ANSWER_KEY_ENTRY_RE = re.compile(
    r"(?m)^\*\*(\d+)\.\s+([A-D](?:\s*[+,]\s*[A-D])*)\*\*\s+[—-]\s+"
)
SELECTION_WORD_COUNTS = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4}
SHORT_EXAM_QUESTION_COUNT = 15
SHORT_EXAM_SECTION_COUNT = 4
SHORT_EXAM_TIME_LIMIT_MINUTES = 30
SHORT_EXAM_PASSING_SCORE = 12


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "item"


def compact_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_h1(text: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return match.group(1).strip() if match else fallback


def parse_source_url(text: str) -> str:
    match = re.search(r"(?m)^-\s+Source URL:\s+(.+?)\s*$", text)
    if not match:
        return ""
    return match.group(1).strip().strip("`")


def parse_note_sections(path: Path) -> tuple[str, str, list[NoteSection]]:
    text = read_text(path)
    title = first_h1(text, path.parent.name)
    source_url = parse_source_url(text)
    matches = list(HEADING_RE.finditer(text))
    sections: list[NoteSection] = []

    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section_title = match.group(1).strip()
        body = text[match.end() : next_start].strip()
        sections.append(
            NoteSection(
                id=slugify(section_title),
                title=section_title,
                body=body,
            )
        )

    return title, source_url, sections


def parse_flashcards(path: Path, pack_id: str) -> list[Flashcard]:
    if not path.exists():
        return []

    text = read_text(path)
    matches = list(HEADING_RE.finditer(text))
    cards: list[Flashcard] = []

    for section_index, match in enumerate(matches):
        next_start = matches[section_index + 1].start() if section_index + 1 < len(matches) else len(text)
        topic = match.group(1).strip()
        body = text[match.end() : next_start].strip()
        qa_pairs = re.finditer(r"(?ms)^Q:\s*(.*?)\n\s*A:\s*(.*?)(?=^Q:|\Z)", body)

        for card_index, qa in enumerate(qa_pairs, start=1):
            question = qa.group(1).strip()
            answer = qa.group(2).strip()
            if not question or not answer:
                continue
            card_number = len(cards) + 1
            cards.append(
                Flashcard(
                    id=f"{pack_id}:card:{card_number}",
                    pack_id=pack_id,
                    topic=topic,
                    question=question,
                    answer=answer,
                )
            )

    return cards


def parse_study_pack_questions(path: Path, pack_id: str) -> list[Question]:
    if not path.exists():
        return []

    text = read_text(path)
    blocks = re.split(r"(?m)^## Question\s+(\d+)\s*$", text)
    questions: list[Question] = []

    for index in range(1, len(blocks), 2):
        number = int(blocks[index])
        block = blocks[index + 1].strip()
        scenario = _extract_label_block(block, "Scenario", "Question")
        prompt = _extract_label_block(block, "Question", "A\\.")
        choices = _parse_letter_choices(block, r"^([A-D])\.\s+(.+?)\s*$")
        correct_choices = _parse_study_pack_correct_choices(block)
        selection_count = len(correct_choices)
        explanation = _extract_explanation(block)
        distractors = _parse_distractors(block)
        stated_selection_count = _selection_count_from_text(prompt)
        if selection_count > 1 and stated_selection_count is None:
            raise ValueError(
                f"{path} question {number} has multiple correct answers but does not state how many responses to select"
            )
        if stated_selection_count is not None and stated_selection_count != selection_count:
            raise ValueError(
                f"{path} question {number} states {stated_selection_count} selections but keys {selection_count}"
            )
        _validate_question(path, number, choices, correct_choices, selection_count)

        questions.append(
            Question(
                id=f"{pack_id}:question:{number}",
                number=number,
                scenario=compact_whitespace(scenario),
                prompt=compact_whitespace(prompt),
                choices=choices,
                correct_choices=correct_choices,
                selection_count=selection_count,
                explanation=compact_whitespace(explanation),
                distractors=distractors,
            )
        )

    return questions


def parse_study_pack(pack_dir: Path) -> StudyPack:
    pack_id = pack_dir.name
    title, source_url, notes_sections = parse_note_sections(pack_dir / "notes.md")
    flashcards = parse_flashcards(pack_dir / "flashcards.md", pack_id)
    practice_questions = parse_study_pack_questions(pack_dir / "practice_questions.md", pack_id)

    return StudyPack(
        id=pack_id,
        title=title,
        source_url=source_url,
        notes_sections=notes_sections,
        flashcards=flashcards,
        practice_questions=practice_questions,
    )


def parse_all_study_packs(base_dir: Path = STUDY_PACKS_DIR) -> list[StudyPack]:
    packs: list[StudyPack] = []
    for pack_dir in sorted(base_dir.iterdir()):
        if not pack_dir.is_dir() or pack_dir.name.startswith("_"):
            continue
        if not (pack_dir / "notes.md").exists():
            continue
        packs.append(parse_study_pack(pack_dir))
    return packs


def parse_full_exam(path: Path) -> PracticeExam:
    text = read_text(path)
    answer_key_start = re.search(r"(?m)^# Answer Key", text)
    if not answer_key_start:
        raise ValueError(f"{path} does not contain an answer key")

    body = text[: answer_key_start.start()]
    answer_key = text[answer_key_start.start() :]
    exam_id = path.stem
    title = first_h1(text, path.stem)
    time_limit_minutes = int(_single_match(text, r"\| Time limit \|\s*(\d+)\s+minutes\s*\|", "120"))
    total_questions = int(_single_match(text, r"\| Questions \|\s*(\d+)\s*\|", "0"))
    passing_score = int(_single_match(text, r"≥\s*(\d+)\s*/\s*\d+", "0"))
    domain_distribution = _parse_domain_distribution(body)
    quick_key = _parse_quick_key(answer_key)
    detailed_key = _parse_detailed_key(answer_key)
    explanations = _parse_answer_explanations(answer_key)
    scenario_info = _parse_scenario_info(body)
    questions: list[Question] = []

    for question_match in FULL_EXAM_QUESTION_RE.finditer(body):
        number = int(question_match.group(1))
        selection_word = question_match.group(2)
        block = question_match.group(3).strip()
        scenario_title, scenario_context = _scenario_for_position(scenario_info, question_match.start())
        prompt = _extract_full_exam_prompt(block)
        choices = _parse_letter_choices(block, r"^-\s+([A-D])\)\s+(.+?)\s*$")
        correct_choices = quick_key.get(number, [])
        selection_count = SELECTION_WORD_COUNTS.get((selection_word or "ONE").upper(), 1)
        if len(correct_choices) > 1 and selection_word is None:
            raise ValueError(
                f"{path} question {number} has multiple correct answers but no selection-count instruction"
            )
        if detailed_key.get(number) and detailed_key[number] != correct_choices:
            raise ValueError(f"{path} question {number} quick key and detailed key disagree")
        _validate_question(path, number, choices, correct_choices, selection_count)
        explanation = explanations.get(number, "")
        questions.append(
            Question(
                id=f"{exam_id}:question:{number}",
                number=number,
                scenario=scenario_title,
                scenario_context=scenario_context,
                prompt=compact_whitespace(prompt),
                choices=choices,
                correct_choices=correct_choices,
                selection_count=selection_count,
                explanation=compact_whitespace(explanation),
            )
        )

    parsed_numbers = {question.number for question in questions}
    if total_questions and total_questions != len(questions):
        raise ValueError(
            f"{path} declares {total_questions} questions but contains {len(questions)}"
        )
    if set(quick_key) != parsed_numbers:
        raise ValueError(f"{path} quick key does not match the parsed question numbers")
    if set(detailed_key) != parsed_numbers:
        raise ValueError(f"{path} detailed answer key does not match the parsed question numbers")
    if not total_questions:
        total_questions = len(questions)
    if not passing_score and total_questions:
        passing_score = round(total_questions * 0.75)

    return PracticeExam(
        id=exam_id,
        title=title,
        time_limit_minutes=time_limit_minutes,
        passing_score=passing_score,
        total_questions=total_questions,
        domain_distribution=domain_distribution,
        questions=questions,
    )


def parse_all_full_exams(base_dir: Path = PRACTICE_EXAMS_DIR) -> list[PracticeExam]:
    paths = sorted(base_dir.glob("*.md"), key=_practice_exam_sort_key)
    return [parse_full_exam(path) for path in paths]


def build_short_practice_exams(full_exams: list[PracticeExam]) -> list[PracticeExam]:
    short_exams: list[PracticeExam] = []

    for full_exam in full_exams:
        sections = [
            list(section_questions)
            for _, section_questions in groupby(full_exam.questions, key=lambda question: question.scenario)
        ]
        if len(sections) != SHORT_EXAM_SECTION_COUNT:
            raise ValueError(
                f"{full_exam.id} must contain exactly {SHORT_EXAM_SECTION_COUNT} scenario sections "
                "to generate short practice exams"
            )

        for section_index, source_questions in enumerate(sections, start=1):
            if len(source_questions) != SHORT_EXAM_QUESTION_COUNT:
                raise ValueError(
                    f"{full_exam.id} section {section_index} must contain exactly "
                    f"{SHORT_EXAM_QUESTION_COUNT} questions to generate a short practice exam"
                )

            short_number = len(short_exams) + 1
            short_id = f"short-practice-exam-{short_number}"
            source_scenario = source_questions[0].scenario
            scenario = _short_scenario_title(source_scenario)
            questions = [
                replace(
                    question,
                    id=f"{short_id}:question:{local_number}",
                    number=local_number,
                    scenario=scenario,
                    source_question_id=question.id,
                    source_question_number=question.number,
                )
                for local_number, question in enumerate(source_questions, start=1)
            ]
            short_exams.append(
                PracticeExam(
                    id=short_id,
                    title=f"{TRACK_LABEL} Short Practice Exam {short_number}",
                    time_limit_minutes=SHORT_EXAM_TIME_LIMIT_MINUTES,
                    passing_score=SHORT_EXAM_PASSING_SCORE,
                    total_questions=SHORT_EXAM_QUESTION_COUNT,
                    domain_distribution=[],
                    questions=questions,
                    source_exam_id=full_exam.id,
                    source_exam_title=full_exam.title,
                    source_section_index=section_index,
                    source_scenario=source_scenario,
                )
            )

    return short_exams


def _practice_exam_sort_key(path: Path) -> tuple[int, int | str]:
    match = re.search(r"(\d+)$", path.stem)
    if match:
        return (0, int(match.group(1)))
    return (1, path.stem)


def _short_scenario_title(value: str) -> str:
    return re.sub(r"\s*\(Questions\s+\d+\s*[–-]\s*\d+\)\s*$", "", value).strip()


def _extract_label_block(text: str, label: str, next_label_pattern: str) -> str:
    pattern = rf"(?ms)^{label}:\s*(.*?)(?=\n\n{next_label_pattern})"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else ""


def _parse_letter_choices(text: str, pattern: str) -> list[dict[str, str]]:
    choices = []
    for match in re.finditer(pattern, text, flags=re.MULTILINE):
        choices.append({"letter": match.group(1), "text": match.group(2).strip()})
    return choices


def _single_match(text: str, pattern: str, default: str = "") -> str:
    match = re.search(pattern, text)
    return match.group(1).strip() if match else default


def _parse_choice_letters(value: str) -> list[str]:
    return [letter for letter in re.findall(r"[A-D]", value.upper())]


def _parse_study_pack_correct_choices(block: str) -> list[str]:
    match = re.search(
        r"(?m)^Correct answers?:\s*([A-D](?:\s*[+,]\s*[A-D])*)\s*$",
        block,
    )
    return _parse_choice_letters(match.group(1)) if match else []


def _selection_count_from_text(text: str) -> int | None:
    match = re.search(
        r"\bselect\s+(ONE|TWO|THREE|FOUR)(?:\s+responses?)?\b",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return SELECTION_WORD_COUNTS[match.group(1).upper()]


def _validate_question(
    path: Path,
    number: int,
    choices: list[dict[str, str]],
    correct_choices: list[str],
    selection_count: int,
) -> None:
    choice_letters = [choice["letter"] for choice in choices]
    if len(choices) != 4 or choice_letters != ["A", "B", "C", "D"]:
        raise ValueError(f"{path} question {number} must contain choices A through D exactly once")
    if not correct_choices:
        raise ValueError(f"{path} question {number} has no keyed answer")
    if len(correct_choices) != len(set(correct_choices)):
        raise ValueError(f"{path} question {number} contains duplicate keyed answers")
    if any(letter not in choice_letters for letter in correct_choices):
        raise ValueError(f"{path} question {number} keys an unknown choice")
    if selection_count != len(correct_choices):
        raise ValueError(
            f"{path} question {number} requires {selection_count} selections but keys {len(correct_choices)}"
        )


def _extract_explanation(block: str) -> str:
    match = re.search(r"(?ms)^Explanation:\s*(.*?)(?=\n\nDistractors:|\Z)", block)
    return match.group(1).strip() if match else ""


def _parse_distractors(block: str) -> dict[str, str]:
    match = re.search(r"(?ms)^Distractors:\s*(.*)\Z", block)
    if not match:
        return {}
    distractors: dict[str, str] = {}
    for line_match in re.finditer(r"(?m)^-\s+([A-D]):\s+(.+?)\s*$", match.group(1)):
        distractors[line_match.group(1)] = line_match.group(2).strip()
    return distractors


def _parse_domain_distribution(text: str) -> list[dict[str, str]]:
    marker = "| Domain | Questions |"
    marker_index = text.find(marker)
    if marker_index == -1:
        return []
    table_text = text[marker_index:].split("\n\n", 1)[0]
    rows: list[dict[str, str]] = []
    for line in table_text.splitlines()[2:]:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 2 and cells[0] and cells[1]:
            rows.append({"domain": cells[0], "questions": cells[1]})
    return rows


def _parse_quick_key(answer_key: str) -> dict[int, list[str]]:
    match = re.search(r"(?m)^\*\*Quick key:\*\*\s*(.+?)\s*$", answer_key)
    if not match:
        return {}
    key_text = match.group(1)
    answers: dict[int, list[str]] = {}
    for answer_match in re.finditer(r"(\d+)-([A-D](?:\s*\+\s*[A-D])*)", key_text):
        answers[int(answer_match.group(1))] = _parse_choice_letters(answer_match.group(2))
    return answers


def _parse_detailed_key(answer_key: str) -> dict[int, list[str]]:
    return {
        int(match.group(1)): _parse_choice_letters(match.group(2))
        for match in ANSWER_KEY_ENTRY_RE.finditer(answer_key)
    }


def _parse_answer_explanations(answer_key: str) -> dict[int, str]:
    matches = list(ANSWER_KEY_ENTRY_RE.finditer(answer_key))
    explanations: dict[int, str] = {}

    for index, match in enumerate(matches):
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(answer_key)
        number = int(match.group(1))
        explanation = answer_key[match.end() : next_start].strip()
        explanations[number] = explanation

    return explanations


def _parse_scenario_info(body: str) -> list[dict[str, object]]:
    scenario_matches = list(re.finditer(r"(?m)^##\s+Scenario\s+(.+?)\s*$", body))
    scenarios: list[dict[str, object]] = []

    for index, match in enumerate(scenario_matches):
        next_scenario = scenario_matches[index + 1].start() if index + 1 < len(scenario_matches) else len(body)
        segment = body[match.end() : next_scenario]
        first_question = re.search(r"(?m)^\*\*Question\s+\d+\.", segment)
        context = segment[: first_question.start()].strip() if first_question else segment.strip()
        scenarios.append(
            {
                "start": match.start(),
                "title": f"Scenario {match.group(1).strip()}",
                "context": _strip_rules(context),
            }
        )

    return scenarios


def _scenario_for_position(scenarios: list[dict[str, object]], position: int) -> tuple[str, str]:
    selected: dict[str, object] | None = None
    for scenario in scenarios:
        if int(scenario["start"]) <= position:
            selected = scenario
        else:
            break
    if not selected:
        return "", ""
    return str(selected["title"]), str(selected["context"])


def _strip_rules(text: str) -> str:
    lines = [line for line in text.splitlines() if line.strip() != "---"]
    return compact_whitespace("\n".join(lines))


def _extract_full_exam_prompt(block: str) -> str:
    choice_match = re.search(r"(?m)^-\s+[A-D]\)\s+", block)
    if not choice_match:
        return block.strip()
    return block[: choice_match.start()].strip()
