"""Merge the four first-pass classifications, check completeness against the log, and print the summary the register is built from.

usage: python3 merge.py            (writes merged.jsonl and prints counts, gaps and the in-force list by area)
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOG = Path('/Users/lchingen/hivemind/docs/DECISIONS.md')
KEYS = ['id', 'date', 'title', 'area', 'status', 'rule', 'by', 'amends', 'authority', 'quote', 'home', 'home_agrees', 'conflicts', 'note']
AREAS = {'system', 'universe', 'classification', 'config', 'dispatch', 'extraction', 'library', 'closing', 'review-pool', 'filing-phase',
         'ruler', 'idea-service', 'frontend', 'data', 'operations', 'working-rules'}
STATUSES = {'in-force', 'superseded', 'retired', 'record'}


def log_ids():
    return [m.group(1) for m in re.finditer(r'^## (D\d+) ', LOG.read_text(encoding='utf-8'), re.M)]


def main():
    records, problems = {}, []
    for part in sorted(HERE.glob('claude-*.jsonl')):
        for number, line in enumerate(part.read_text(encoding='utf-8').splitlines(), 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as error:
                problems.append(f'{part.name}:{number}: not JSON ({error})')
                continue
            missing = [k for k in KEYS if k not in record]
            if missing:
                problems.append(f'{part.name}:{number} {record.get("id")}: missing {missing}')
            if record.get('area') not in AREAS:
                problems.append(f'{record.get("id")}: area {record.get("area")!r}')
            if record.get('status') not in STATUSES:
                problems.append(f'{record.get("id")}: status {record.get("status")!r}')
            if record.get('id') in records:
                problems.append(f'{record.get("id")}: duplicate')
            records[record.get('id')] = record
    expected = log_ids()
    absent = [d for d in expected if d not in records]
    extra = [d for d in records if d not in expected]
    ordered = [records[d] for d in expected if d in records]
    (HERE / 'merged.jsonl').write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in ordered), encoding='utf-8')
    print(f'{len(records)} records; log has {len(expected)}; absent {absent}; extra {extra}')
    print('problems:', len(problems)); [print('  ', p) for p in problems[:30]]
    print('status:', dict(collections.Counter(r['status'] for r in ordered)))
    print('authority:', dict(collections.Counter(r['authority'] for r in ordered)))
    by_area = collections.defaultdict(list)
    for r in ordered:
        by_area[r['area']].append(r)
    for area in sorted(by_area):
        rows = by_area[area]
        print(f'{area}: {len(rows)} ({dict(collections.Counter(r["status"] for r in rows))})')
    if '--in-force' in sys.argv:
        for area in sorted(by_area):
            print(f'\n## {area}')
            for r in by_area[area]:
                if r['status'] == 'in-force':
                    print(f'- {r["id"]} [{r["authority"]}] {r["rule"]}  (home: {r["home"]}; agrees: {r["home_agrees"]})')
    if '--conflicts' in sys.argv:
        print('\n## conflicts named')
        for r in ordered:
            for c in r['conflicts'] or []:
                print(f'- {r["id"]} ({r["status"]}): {c}')
    if '--disagree' in sys.argv:
        print('\n## homes that disagree')
        for r in ordered:
            if r['home_agrees'] == 'no':
                print(f'- {r["id"]} -> {r["home"]}: {r["note"]}')


if __name__ == '__main__':
    main()
