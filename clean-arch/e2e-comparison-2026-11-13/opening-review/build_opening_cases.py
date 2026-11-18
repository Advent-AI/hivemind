"""D457's opening review, the listing step ($0): for each graded ruler question lost or unresolved in a full-run draw, the ruler's question
and due day; for a view opened but not eligible or unresolved, the view's own question, outcome and period with both families' eligibility
reading; for a question not opened, every opened question either matching family tied to it with a relation other than "same" (with the
relation and the reader's reason), or a note that no reader tied any. The classification into the four outcomes is Claude's, by hand.

  python3 build_opening_cases.py > cases-full.txt
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'clean-arch/e2e-comparison-2026-11-13'
DATA = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
GRADED = ['q04', 'q05', 'q08', 'q09', 'q13', 'q18', 'q23']
DRAWS = ['c1', 'c2', 'c3', 'p1', 'p2', 'p3']


def read_jsonl(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main():
    ruler = {q['id']: q for q in json.loads((E / 'full-matching/ruler-questions.json').read_text())}
    key = json.loads((DATA / 'matching-key.json').read_text())
    opened = {}
    for number in range(1, 7):
        for entry in json.loads((E / f'full-matching/opened-r{number}.json').read_text()):
            opened[f"{entry['run']}/{entry['id']}"] = entry
    answers = {}
    for number in range(1, 7):
        for family, name in (('claude', f'match-r{number}-claude.jsonl'), ('codex', f'match-r{number}-codex.txt')):
            for row in read_jsonl(E / 'full-matching-answers' / name):
                answers.setdefault(f"{row['run']}/{row['id']}", {})[family] = row
    outcomes = json.loads((E / 'full-eligibility-answers/census-outcomes.json').read_text())
    mapping = json.loads((E / 'full-matching-answers/mapping-full.json').read_text())
    unresolved = mapping['unresolved (the third readers split)']
    by_draw = {}
    for name, entry in key.items():
        by_draw.setdefault(entry['draw'], []).append(name)
    count = 0
    for draw in DRAWS:
        rows = outcomes.get(draw, {})
        for question in GRADED:
            status = rows[question][1] if question in rows else None
            matching_split = [v for v, q in unresolved.get(draw, {}).items() if q == question]
            if status == 'agrees':
                continue
            count += 1
            print(f"\n## {draw} {question}: {ruler[question]['question']} (due {ruler[question]['due_day']})")
            if status:
                view = rows[question][0]
                name = next(n for n in by_draw[draw] if key[n]['id'] == view or key[n]['id'] == f'clean-{view[1:]}' and draw.startswith('c'))
                entry = opened[name]
                print(f'   OPENED {view} -> {status} | {entry["description"][:200]}')
                print(f'      outcome: {entry["outcome"][:200]}')
                print(f'      period: {entry["period"][:200]}')
            elif matching_split:
                print(f'   MATCHING SPLIT on {matching_split}')
            near = []
            for name in by_draw[draw]:
                for family, row in answers.get(name, {}).items():
                    if row['match'] == question and row['relation'] != 'same':
                        near.append((name, family, row))
            for name, family, row in near:
                entry = opened[name]
                print(f'   NEAR {name} ({family}: {row["relation"]}) | {entry["description"][:170]}')
                print(f'      period: {entry["period"][:150]} | why: {row["reason"][:220]}')
            if not status and not near and not matching_split:
                print('   nothing opened that any reader tied to this question')
    print(f'\n{count} cases (graded questions not agreeing, six full-run draws)')


if __name__ == '__main__':
    main()
