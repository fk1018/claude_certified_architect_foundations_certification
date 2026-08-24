#!/usr/bin/env python3
"""
Find answer-key errors in a generated exam bank, without using a model.

Two checks, both cheap and both of which have already found real errors in this
repo:

  1. DUPLICATE DISAGREEMENT. The generator reuses questions across exams. Where
     the same stem appears with the same four options but a different answer
     keyed, at least one of them is wrong. Majority rules, minority gets flagged.

  2. ABSOLUTES KEYED CORRECT. Options containing "always", "never", "all",
     "every" are the answer only 12% of the time they appear in this bank --
     they're overwhelmingly distractor language. When one IS keyed correct it is
     usually fine, but it's a short, high-yield review queue: it catches keys
     like "Managed agents are always less secure than self-hosted ones."

Neither check proves a question is right. They find contradictions and smells,
which is where human review time is best spent.

    python find_key_errors.py practice_exams/
    python find_key_errors.py practice_exams_developer_foundations/ --absolutes
"""
from __future__ import annotations
import argparse, collections, re, sys
from pathlib import Path

ABSOLUTE = re.compile(r"\b(always|never|all |every |only ever|impossible|cannot ever)\b", re.I)


def load(directory: Path):
    """Yield (filename, number, stem, {letter: text}, correct_letter)."""
    for path in sorted(directory.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        key_line = re.search(r"\*\*Quick key:\*\*(.*)", text)
        if not key_line:
            continue
        key = {int(n): L for n, L in re.findall(r"(\d+)\s*-\s*([A-D])", key_line.group(1))}
        chunks = re.split(r"\*\*Question (\d+)\.\*\*", text.split("# Answer Key")[0])
        for i in range(1, len(chunks), 2):
            n = int(chunks[i])
            stem = chunks[i + 1].split("\n- A)")[0].strip()
            options = dict(re.findall(r"^- ([A-D])\)\s*(.+)$", chunks[i + 1], re.M))
            if len(options) == 4 and n in key:
                yield path.name, n, stem, options, key[n]


def duplicate_disagreements(questions):
    """Same stem, same option set, different answer text -> one of them is wrong."""
    groups = collections.defaultdict(list)
    for filename, n, stem, options, correct in questions:
        groups[stem.strip().lower()].append((filename, n, options, correct))

    findings = []
    for stem, group in groups.items():
        if len(group) < 2:
            continue
        if len({frozenset(o.values()) for _f, _n, o, _c in group}) != 1:
            continue                      # different options: a variant, not a contradiction
        answers = collections.Counter(o[c].strip().lower() for _f, _n, o, c in group)
        if len(answers) == 1:
            continue                      # same answer, possibly a different letter: just shuffled

        ranked = answers.most_common()
        # With only two copies -- or an even split -- there is no majority to trust.
        # Flag every copy rather than arbitrarily blaming one of them.
        tied = len(ranked) > 1 and ranked[0][1] == ranked[1][1]
        majority_text = None if tied else ranked[0][0]

        for filename, n, options, correct in group:
            keyed = options[correct].strip().lower()
            if tied:
                findings.append({
                    "file": filename, "question": n, "stem": stem,
                    "keyed": options[correct],
                    "majority": " | ".join(
                        o[c] for _f, _n, o, c in group if o[c].strip().lower() != keyed),
                    "agreement": f"no majority — {len(group)} copies disagree, review all",
                })
            elif keyed != majority_text:
                findings.append({
                    "file": filename, "question": n, "stem": stem,
                    "keyed": options[correct],
                    "majority": next(o[c] for _f, _n, o, c in group
                                     if o[c].strip().lower() == majority_text),
                    "agreement": f"{ranked[0][1]} of {len(group)} copies disagree with this one",
                })
    return findings


def absolutes_keyed_correct(questions):
    return [{"file": f, "question": n, "stem": stem, "keyed": options[correct]}
            for f, n, stem, options, correct in questions
            if ABSOLUTE.search(options[correct])]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("directory", type=Path)
    ap.add_argument("--absolutes", action="store_true",
                    help="also print the absolutes review queue (long)")
    args = ap.parse_args()

    questions = list(load(args.directory))
    if not questions:
        raise SystemExit(f"No parseable questions in {args.directory}")
    print(f"{len(questions)} questions\n")

    contradictions = duplicate_disagreements(questions)
    print(f"CONTRADICTIONS — same question, same options, different answer: {len(contradictions)}")
    for f in contradictions:
        print(f"\n  {f['file']} Q{f['question']}   ({f['agreement']})")
        print(f"    stem:     {f['stem'][:120]}...")
        print(f"    keyed:    {f['keyed'][:110]}")
        print(f"    elsewhere:{f['majority'][:110]}")

    absolutes = absolutes_keyed_correct(questions)
    print(f"\nREVIEW QUEUE — an absolute is keyed correct: {len(absolutes)} of {len(questions)}")
    print("  (absolutes are the answer only ~12% of the time they appear, so these are worth a skim)")
    if args.absolutes:
        for f in absolutes:
            print(f"\n  {f['file']} Q{f['question']}: {f['keyed'][:110]}")
    else:
        print("  re-run with --absolutes to list them")

    return 1 if contradictions else 0


if __name__ == "__main__":
    sys.exit(main())
