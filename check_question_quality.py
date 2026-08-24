#!/usr/bin/env python3
"""
Measure how much a generated multiple-choice bank gives away.

Two failure modes are checked, both of which let a candidate score well without
knowing the material -- and both of which are invisible if you only eyeball a
few questions:

  1. LENGTH TELL. Generated correct answers tend to be longer than distractors,
     because the generator writes the right answer as a small explanation and the
     wrong ones as one-liners. Fix by length-matching every option.

  2. VOCABULARY TELL. Certain words appear almost exclusively in correct answers
     ("structured", "validate", "deterministic", "hook") or almost exclusively in
     distractors ("temperature", "increase"). Fix by using the same register in
     every option, so the words describe the approach rather than mark the answer.

Run before and after any regeneration. Exit status is nonzero if a threshold
fails, so it works as a CI gate.

    python check_question_quality.py practice_exams/
    python check_question_quality.py practice_exams/ --json
"""
from __future__ import annotations
import argparse, json, re, statistics, sys
from pathlib import Path

# Terms whose presence in an option correlates with it being right or wrong.
# Extend this list as new leaks turn up; the point is the method, not the words.
WATCHLIST = ["hook", "determinist", "structured", "schema", "validat", "normaliz",
             "system prompt", "few-shot", "temperature", "increase"]

# A correct answer longer than this multiple of the mean distractor is a giveaway.
BALANCED_RATIO = 1.15
# Thresholds for a passing bank. Chance is 25% for a 4-option question.
MAX_LONGEST_RATE = 0.35      # how often the longest option is correct
MAX_NAIVE_SCORE = 0.35       # score for "always pick the longest, never read the question"
MAX_LIFT = 2.0               # correct-vs-distractor frequency ratio for any watchlist term


def parse_exam(path: Path):
    """Yield (question_number, {letter: text}, correct_letter) for one exam file."""
    text = path.read_text(encoding="utf-8")
    key_line = re.search(r"\*\*Quick key:\*\*(.*)", text)
    if not key_line:
        return
    key = {int(n): L for n, L in re.findall(r"(\d+)\s*-\s*([A-D])", key_line.group(1))}
    body = text.split("# Answer Key")[0]
    chunks = re.split(r"\*\*Question (\d+)\.\*\*", body)
    for i in range(1, len(chunks), 2):
        n = int(chunks[i])
        options = dict(re.findall(r"^- ([A-D])\)\s*(.+)$", chunks[i + 1], re.M))
        if len(options) == 4 and n in key:
            yield n, options, key[n]


def analyse(directory: Path):
    questions = []
    for path in sorted(directory.glob("*.md")):
        for n, options, correct in parse_exam(path):
            questions.append((path.name, n, options, correct))
    if not questions:
        raise SystemExit(f"No parseable questions found in {directory}")

    correct_texts, wrong_texts, ratios = [], [], []
    longest_hits = 0
    per_exam: dict[str, list[bool]] = {}

    for filename, _n, options, correct in questions:
        correct_texts.append(options[correct].lower())
        wrong_texts += [v.lower() for k, v in options.items() if k != correct]
        others = [len(v) for k, v in options.items() if k != correct]
        ratios.append(len(options[correct]) / statistics.mean(others))
        hit = max(options, key=lambda k: len(options[k])) == correct
        longest_hits += hit
        per_exam.setdefault(filename, []).append(hit)

    def frequency(corpus, term):
        return sum(1 for t in corpus if term in t) / len(corpus)

    lifts = {}
    for term in WATCHLIST:
        c, w = frequency(correct_texts, term), frequency(wrong_texts, term)
        if max(c, w) < 0.01:          # too rare to matter
            continue
        lifts[term] = {"correct": round(100 * c, 1), "wrong": round(100 * w, 1),
                       "lift": round(c / w, 2) if w else None}

    return {
        "questions": len(questions),
        "exams": len(per_exam),
        "longest_is_correct": round(longest_hits / len(questions), 3),
        "naive_score": round(longest_hits / len(questions), 3),
        "median_length_ratio": round(statistics.median(ratios), 2),
        "balanced_questions": sum(1 for r in ratios if r <= BALANCED_RATIO),
        "mean_correct_chars": round(statistics.mean(len(t) for t in correct_texts)),
        "mean_wrong_chars": round(statistics.mean(len(t) for t in wrong_texts)),
        "per_exam_naive_score": {k: round(sum(v) / len(v), 2) for k, v in sorted(per_exam.items())},
        "vocabulary": lifts,
    }


def report(r: dict) -> bool:
    ok = True
    print(f"{r['questions']} questions across {r['exams']} exams\n")

    print("LENGTH")
    print(f"  correct answer is the longest option   {100*r['longest_is_correct']:.0f}%   (chance 25%)")
    print(f"  median correct / mean distractor       {r['median_length_ratio']}x   (target <= {BALANCED_RATIO}x)")
    print(f"  mean length correct vs distractor      {r['mean_correct_chars']} vs {r['mean_wrong_chars']} chars")
    print(f"  length-balanced questions              {r['balanced_questions']} of {r['questions']}")
    print(f"\n  \"never read the question, pick the longest option\" scores {100*r['naive_score']:.0f}%")
    if r["naive_score"] > MAX_NAIVE_SCORE:
        print(f"  FAIL: above the {100*MAX_NAIVE_SCORE:.0f}% threshold")
        ok = False

    worst = sorted(r["per_exam_naive_score"].items(), key=lambda kv: -kv[1])[:3]
    print("  worst exams: " + ", ".join(f"{k} {100*v:.0f}%" for k, v in worst))

    print("\nVOCABULARY  (share of options containing the term)")
    print(f"  {'term':<16}{'correct':>9}{'wrong':>8}{'lift':>7}")
    for term, v in sorted(r["vocabulary"].items(), key=lambda kv: -(kv[1]["lift"] or 99)):
        lift = v["lift"]
        flag = ""
        if lift is None or lift > MAX_LIFT or lift < 1 / MAX_LIFT:
            flag = "   <-- leaks"
            ok = False
        shown = "inf" if lift is None else f"{lift:.2f}"
        print(f"  {term:<16}{v['correct']:>8}%{v['wrong']:>7}%{shown:>7}{flag}")

    print("\n" + ("PASS" if ok else "FAIL — a candidate can score well without reading the questions"))
    return ok


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory", type=Path, help="folder of practice exam .md files")
    ap.add_argument("--json", action="store_true", help="emit raw numbers instead of a report")
    args = ap.parse_args()

    result = analyse(args.directory)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0
    return 0 if report(result) else 1


if __name__ == "__main__":
    sys.exit(main())
