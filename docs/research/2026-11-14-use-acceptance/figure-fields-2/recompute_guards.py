"""The second figure-fields probe: the two guards the tally counted too coarsely, recomputed as the design words them (council mx rounds
10 and 11), with their working printed. (1) Every statement-to-question link over all kept statements of the target and control cases, one
statement matched across sends and arms by shared passages. (2) The statement's own party and date on every statement holding a named
figure, by send, both arms, with the fresh pair's marks where the first two families differ.

  python3 recompute_guards.py <records.jsonl> <cases.json> <key folder outside the repository>
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARMS = ('c8', 'c22')


def normal(text):
    return re.sub(r'\W+', ' ', text or '').strip().lower()


def related(a, b):
    for p in a['passages']:
        for q in b['passages']:
            short, long = (p, q) if len(p) <= len(q) else (q, p)
            if len(short) >= 25 and (short[:60] in long or short[-60:] in long):
                return True
    return False


def main():
    records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
    cases = {case['case']: case for case in json.loads(Path(sys.argv[2]).read_text())}
    key = {row['answer']: row for row in json.loads((Path(sys.argv[3]) / 'figure-fields-2-key.json').read_text())}
    by_case = collections.defaultdict(list)
    for record in records:
        if record['case'].endswith('-keep'):
            continue
        for statement in record.get('links') or []:
            passages = [normal(p) for p in (statement.get('verified_source_passages') or statement.get('source_passages') or []) if p]
            by_case[record['case']].append({'arm': record['arm'], 'send': record['send'], 'passages': passages,
                                            'questions': {l['target_id'] for l in statement.get('links') or [] if l['target_type'] == 'existing'}})
    print('LINKS: every statement-to-question pair (sends with the link / sends keeping the statement), by case')
    most_none = 0
    for case_name, statements in sorted(by_case.items()):
        parent = list(range(len(statements)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i
        for i in range(len(statements)):
            for j in range(i + 1, len(statements)):
                if related(statements[i], statements[j]):
                    parent[find(i)] = find(j)
        clusters = collections.defaultdict(list)
        for index, statement in enumerate(statements):
            clusters[find(index)].append(statement)
        for members in clusters.values():
            questions = set().union(*(m['questions'] for m in members))
            for question in sorted(questions):
                rate = {arm: len({m['send'] for m in members if m['arm'] == arm and question in m['questions']}) for arm in ARMS}
                kept = {arm: len({m['send'] for m in members if m['arm'] == arm}) for arm in ARMS}
                flag = (rate['c8'] >= 2 and rate['c22'] == 0) or (rate['c22'] >= 2 and rate['c8'] == 0)
                most_none += flag
                text = members[0]['passages'][0][:64] if members[0]['passages'] else ''
                print(f"  {case_name} | {text} -> {question}: c8 {rate['c8']}/{kept['c8']}, c22 {rate['c22']}/{kept['c22']}{'   <-- most against none' if flag else ''}")
    print(f'  pairs "most against none": {most_none}')

    def load(name):
        return {json.loads(line)['answer']: json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')}
    first = {family: load(f'{family}-reader-1.jsonl') for family in ('codex', 'claude')}
    fresh = {family: load(f'{family}-reader-1-settle.jsonl') for family in ('codex', 'claude')}
    print("\nTHE STATEMENT'S OWN PARTY AND DATE: every statement holding a named figure, by answer")
    totals = {arm: collections.Counter() for arm in ARMS}
    for label, row in sorted(key.items(), key=lambda kv: (kv[1]['case'], kv[1]['arm'], kv[1]['send'])):
        if not cases[row['case']]['named_figures']:
            continue
        holders = sorted({n.get('statement') for family in first for n in first[family][label].get('named') or [] if n.get('statement')})
        parts = []
        for statement_id in holders:
            marks = {}
            for field in ('statement_party', 'statement_date'):
                pair = [next((s.get(field) for s in first[family][label].get('statements') or [] if s.get('id') == statement_id), None) for family in ('codex', 'claude')]
                if pair[0] == pair[1]:
                    marks[field] = pair[0]
                else:
                    again = [next((s.get(field) for s in fresh[family].get(label, {}).get('statements') or [] if s.get('id') == statement_id), None)
                             for family in ('codex', 'claude')]
                    marks[field] = again[0] if again[0] is not None and again[0] == again[1] else f'open {pair}'
                totals[row['arm']][f"{field}: {marks[field] if not str(marks[field]).startswith('open') else 'open'}"] += 1
            parts.append(f"{statement_id}: party {marks['statement_party']}, date {marks['statement_date']}")
        print(f"  {row['case']} {row['arm']} #{row['send']}: " + '; '.join(parts))
    for arm in ARMS:
        print(f'  {arm}: {dict(sorted(totals[arm].items()))}')


if __name__ == '__main__':
    main()
