"""A sheet for the recount the council asked for (D547): in the July full run's reading of answer choices (40 fresh theses, three
attempts each), every clause that sits only in a thesis's `outcome` field behind a marker of a second side, a comparison, a
consequence or a condition, whether each attempt listed something in `not_judged`, and how the two first readers marked `L`.
A locating aid for reading against D397 and D436: it decides nothing. Reads the stored run only.

  python3 july_line2_recount.py
"""
import json
import re
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
RUN = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
HERE = Path(__file__).parent
MARKERS = re.compile(r'\b(compared with|compared to|versus|vs\.?|relative to|rather than|so that|and whether|as well as whether|against the)\b|\(', re.I)


def main():
    key = json.loads((RUN / 'stage-a-key.json').read_text())
    marks = {'codex': {}, 'claude': {}}
    for family in marks:
        for path in sorted((RUN / 'stage-a/readers-answers').glob(f'reader-{family}-packet-*.jsonl')):
            for line in path.read_text().splitlines():
                if line.strip().startswith('{'):
                    row = json.loads(line)
                    marks[family][tuple(key[str(row['item'])])] = row
    cases = {}
    for draw in ('c1', 'c2', 'c3'):
        for case in json.loads((RUN / draw / 'cases/cases.json').read_text()):
            cases[case['case']] = case
    outcomes = {}
    for send in (1, 2, 3):
        for line in (RUN / f'stage-a/send-{send}/outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            outcomes[(row['case'], row['pass'])] = row
    sheet = []
    for name, case in sorted(cases.items()):
        thesis = case['thesis']
        clauses = [thesis['outcome'][max(0, m.start() - 10): m.start() + 130] for m in MARKERS.finditer(thesis['outcome'])]
        attempts = []
        for attempt in (1, 2, 3):
            outcome = outcomes.get((name, attempt))
            if not outcome or outcome['status'] != 'ladder':
                attempts.append({'attempt': attempt, 'status': outcome['status'] if outcome else 'missing'})
                continue
            listed = [part['part'] for part in outcome['answer']['ladder']['not_judged']]
            attempts.append({'attempt': attempt, 'status': 'ladder', 'not_judged': listed,
                             'L': {family: marks[family].get((name, attempt), {}).get('L') for family in marks},
                             'why': {family: marks[family].get((name, attempt), {}).get('why', '')[:200] for family in marks if marks[family].get((name, attempt), {}).get('L') == 'fails'}})
        sheet.append({'case': name, 'description': thesis['description'], 'outcome': thesis['outcome'], 'marked_clauses_in_the_outcome': clauses, 'attempts': attempts})
    (HERE / 'july-line2-sheet.json').write_text(json.dumps(sheet, indent=1, ensure_ascii=False) + '\n')
    ladders = [a for row in sheet for a in row['attempts'] if a['status'] == 'ladder']
    fails = [(row['case'], a['attempt'], a['L']) for row in sheet for a in row['attempts'] if a['status'] == 'ladder' and 'fails' in a['L'].values()]
    empty_with_clause = [(row['case'], a['attempt']) for row in sheet if row['marked_clauses_in_the_outcome'] for a in row['attempts'] if a['status'] == 'ladder' and not a['not_judged']]
    print(f"theses {len(sheet)}; ladders read {len(ladders)}; attempts where a first reader failed L: {len(fails)} {fails}")
    print(f"theses whose outcome carries a marked clause: {sum(1 for row in sheet if row['marked_clauses_in_the_outcome'])}; their attempts with an empty not_judged list: {len(empty_with_clause)}")
    for row in sheet:
        if not row['marked_clauses_in_the_outcome']:
            continue
        summary = ' | '.join(f"a{a['attempt']}: {('listed ' + str(len(a['not_judged']))) if a['status'] == 'ladder' else a['status']}{'' if a['status'] != 'ladder' else ' L ' + '/'.join(str(v)[:5] for v in a['L'].values())}" for a in row['attempts'])
        print(f"\n{row['case']}: {row['description'][:110]}\n   outcome: {row['outcome'][:330]}\n   {summary}")
        for a in row['attempts']:
            if a['status'] == 'ladder':
                print(f"      a{a['attempt']} lists: {[p[:70] for p in a['not_judged']]}")


if __name__ == '__main__':
    main()
