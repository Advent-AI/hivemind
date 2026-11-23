"""The two-week run's readings 1 and 2, joined to their keys ($0; PLAN.md as frozen). It judges nothing.

  python3 tally_readings.py openings <run root> <key folder>
  python3 tally_readings.py answers <key folder>

Reading 2's supported controls are fixed by rule before any answer is joined: the first four candidates, by number, that the
separate reader marked SUPPORTED (`control-confirmation.jsonl`); fewer than four confirmed is reported, not filled.
"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def lines_of(path):
    path = Path(path)
    if not path.exists():
        return []
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out.append(row)
        except json.JSONDecodeError:
            position = start + 1


def both(values):
    return values[0] if values[0] == values[1] else 'split:' + '/'.join(str(v) for v in values)


def openings(run_root, keys):
    packet = json.loads((HERE / 'packet-openings.json').read_text())
    key = json.loads((Path(keys) / 'key-openings.json').read_text())
    rows = {f: {r['ref']: r for r in lines_of(HERE / f'{f}-openings.jsonl')} for f in FAMILIES}
    opened_refs = [f"{a['article']}:{t['ref']}" for a in packet['articles'] for t in a['opened']]
    article_refs = [str(a['article']) for a in packet['articles']]
    for f in FAMILIES:
        missing = [r for r in opened_refs + article_refs if r not in rows[f]]
        print(f'{f}: {len(rows[f])} rows; not answered {len(missing)} {missing[:5]}')
    print(f"\nWEEK 2 OPENINGS: {len(opened_refs)} questions opened by {len(key['opened_rows'])} articles")
    for field in ('in_library', 'worth'):
        print(f'  {field}:', dict(collections.Counter(both([rows[f].get(r, {}).get(field) for f in FAMILIES]) for r in opened_refs)))
    for article in packet['articles']:
        for topic in article['opened']:
            ref = f"{article['article']}:{topic['ref']}"
            marks = ' | '.join(f"{f}: {rows[f].get(ref, {}).get('in_library')}, worth {rows[f].get(ref, {}).get('worth')}" for f in FAMILIES)
            print(f"   art {article['article']:>2} ({article['day']}) {marks} || {topic['description'][:110]}")
    print('\nCONTROLS (every article in the packet: the openers and 20 sampled others)')
    for field in ('lost_questions', 'lost_facts', 'wrong_homes'):
        totals = {f: sum(len(rows[f].get(r, {}).get(field) or []) for r in article_refs) for f in FAMILIES}
        print(f'  {field}: entries per family {totals}')
    lost_facts = collections.Counter()
    for f in FAMILIES:
        for r in article_refs:
            for entry in rows[f].get(r, {}).get('lost_facts') or []:
                lost_facts[(r, entry.get('ref'), entry.get('question'))] += 1
    agreed = [k for k, n in lost_facts.items() if n == 2]
    print(f'  lost facts named by both families: {len(agreed)}', agreed[:12])
    wrong = collections.Counter((r, s) for f in FAMILIES for r in article_refs for s in rows[f].get(r, {}).get('wrong_homes') or [])
    print(f"  wrong homes named by both families: {[k for k, n in wrong.items() if n == 2]}")
    for r in article_refs:
        lists = {f: rows[f].get(r, {}).get('lost_questions') or [] for f in FAMILIES}
        if any(lists.values()):
            print(f'   art {r}: codex {lists["codex"]} | claude {lists["claude"]}')


def answers(keys):
    key = json.loads((Path(keys) / 'key-answers.json').read_text())
    confirmation = {row['candidate']: row for row in lines_of(HERE / 'control-confirmation.jsonl')}
    confirmed = sorted(c for c, row in confirmation.items() if row.get('verdict') == 'SUPPORTED')[:4]
    print(f'supported controls (first four confirmed by the separate reader): {confirmed} of {len(confirmation)} read')
    rows = {f: {r['item']: r for r in lines_of(HERE / f'{f}-answers.jsonl')} for f in FAMILIES}
    for f in FAMILIES:
        print(f'{f}: {len(rows[f])} of {len(key)} items answered')
    real = [k for k in key if not k['planted']]
    verdicts = collections.Counter(both([rows[f].get(k['item'], {}).get('verdict') for f in FAMILIES]) for k in real)
    print(f'\nLAST ANSWERS ({len(real)} questions): {dict(verdicts)}')
    for k in real:
        marks = ' | '.join(f"{f}: {rows[f].get(k['item'], {}).get('verdict')} ({(rows[f].get(k['item'], {}).get('why') or '')[:90]})" for f in FAMILIES)
        print(f"   {k['view']:>4} {marks}")
    print('\nPLANTED WRONG ANSWERS (each should be UNSUPPORTED):')
    for k in key:
        if k['planted']:
            print(f"   {k['planted']:<16} {[rows[f].get(k['item'], {}).get('verdict') for f in FAMILIES]}")
    print('\nCONFIRMED SUPPORTED CONTROLS (each should be SUPPORTED):')
    for k in key:
        if k['candidate'] in confirmed:
            print(f"   candidate {k['candidate']} ({k['view']}): {[rows[f].get(k['item'], {}).get('verdict') for f in FAMILIES]}")


if __name__ == '__main__':
    if sys.argv[1] == 'openings':
        openings(sys.argv[2], sys.argv[3])
    else:
        answers(sys.argv[2])
