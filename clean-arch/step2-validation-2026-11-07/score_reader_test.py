"""Tally the blind reader test (no model calls) under the frozen scoring rules (reader-test/scoring-rules.md, FROZEN.sha256).

Usage: score_reader_test.py <reader-test folder> [<results folder with grade files and views-key.json>]"""
import collections, hashlib, json, sys
from pathlib import Path

POINTS = {'correct': 1, 'partial': 0.5, 'wrong': 0, 'not_found': 0}


def main():
    folder = Path(sys.argv[1])
    results = Path(sys.argv[2]) if len(sys.argv) > 2 else folder
    views_key = results / 'views-key.json' if len(sys.argv) > 2 else folder.parent / 'views-key.json'
    for line in (folder / 'FROZEN.sha256').read_text().split('\n'):
        if line.strip():
            digest, name = line.split()
            if hashlib.sha256((folder / name).read_bytes()).hexdigest() != digest:
                raise SystemExit(f'{name} changed after it was frozen')
    questions = json.loads((folder / 'questions.json').read_text())
    category = {q['id']: q['category'] for d in ('financing', 'competition', 'roadmap') for q in questions[d]}
    mapping = json.loads((results / 'grade-mapping.json').read_text())
    sizes = {v['dossier'] + '/' + v['view']: v['characters'] for v in json.loads(views_key.read_text()).values()}
    score = collections.defaultdict(float); count = collections.Counter(); unsupported = collections.Counter(); doubles = collections.Counter()
    per_question = collections.defaultdict(dict)
    judged = 0
    for d in ('financing', 'competition', 'roadmap'):
        grades = json.loads((results / f'grade-answer-{d}.json').read_text())
        for set_id, rows in grades.items():
            m = mapping[f'{d}/{set_id}']
            if len(rows) != len(questions[d]):
                raise SystemExit(f'{d}/{set_id}: {len(rows)} grades for {len(questions[d])} questions')
            for row in rows:
                judged += 1
                key = (d, m['view'], category[row['id']])
                score[key] += POINTS[row['grade']]; count[key] += 1
                unsupported[(d, m['view'])] += len(row['unsupported'])
                doubles[(d, m['view'])] += bool(row.get('double_counting'))
                per_question[(d, row['id'])][f"{m['view']}-{m['reader']}"] = row['grade']
    print(f'grades judged: {judged}')
    cats = ['detail', 'control', 'comparison', 'independence', 'attribution', 'revision']
    print(f"{'dossier/view':22s} " + ' '.join(f'{c[:11]:>12s}' for c in cats) + '  unsupported  double  characters')
    for d in ('financing', 'competition', 'roadmap'):
        for view in ('none', 'source', 'group'):
            cells = []
            for c in cats:
                n = count[(d, view, c)]
                cells.append(f'{score[(d, view, c)]:>5.1f}/{n:<5d}' if n else f"{'':>12s}")
            print(f'{d + "/" + view:22s} ' + ' '.join(f'{x:>12s}' for x in cells) + f'  {unsupported[(d, view)]:>11d}  {doubles[(d, view)]:>6d}  {sizes[d + "/" + view]:>10d}')
    print('\nper question (view-reader: grade):')
    for (d, qid), row in per_question.items():
        print(f'  {qid:4s} {category[qid][:10]:10s} ' + '  '.join(f'{k}:{row[k]}' for k in sorted(row)))


if __name__ == '__main__':
    main()
