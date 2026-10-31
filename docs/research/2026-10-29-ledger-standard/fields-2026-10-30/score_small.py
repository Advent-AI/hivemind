"""Scores the field class's decisive records on the small sample against the frozen key (key-small.json, sha256 printed):
per row and draw, whether a kept statement carries the row's quote, and whether its original_who and original_day match.
Also prints tier counts on the tier-watch articles and who/day on the company pages (guards). One quantity per column.

    python3 score_small.py <tag> [<tag> ...]          # e.g. P-v51-d1 P-v51-d2 P-v51-d3
"""
import collections
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import score_gold as sg  # noqa: E402
import haiku_week as hw  # noqa: E402

KEY = HERE / 'key-small.json'


def squash(text):
    return re.sub(r'[^a-z0-9$]', '', (text or '').lower().replace('’', "'"))


def main(tags):
    key = json.loads(KEY.read_text())
    print('key sha256', hashlib.sha256(KEY.read_bytes()).hexdigest()[:16])
    db = sqlite3.connect(f'file:{hw.ITEMS}?mode=ro', uri=True)
    pubs = {i: d for i, d in db.execute('select input_id, publication_day from items')}
    totals = collections.defaultdict(collections.Counter)
    lines = []
    for tag in tags:
        runs = sg.answers(tag)
        kept = {}
        for row in key['rows']:
            iid = row[1]
            if iid not in kept:
                kept[iid] = sg.kept(runs.get(iid), iid)
        for name, iid, span, whos, day in key['rows']:
            s = kept[iid]
            match = [e for e in (s or {}).get('evidence', []) if squash(span) in squash(e['quote'])]
            if not match:
                verdict = 'absent'
            else:
                e = match[0]
                who_ok = any(t in (e.get('original_who') or '').lower() for t in whos)
                got = e.get('original_day') or ''
                day_ok = day == '*' or got == day
                verdict = ('who ok' if who_ok else 'who WRONG') + ', ' + ('day ok' if day_ok else f'day WRONG ({got or "empty"})')
                totals[tag]['kept ' + name[0]] += 1
                totals[tag]['who ok ' + name[0]] += who_ok
                totals[tag]['day ok ' + name[0]] += day_ok
                totals[tag]['both ok ' + name[0]] += who_ok and day_ok
            lines.append((name, tag, verdict, (match[0].get('original_who') if match else '')))
        for iid in key['tier_watch']:
            s = sg.kept(runs.get(iid), iid)
            for e in (s or {}).get('evidence', []):
                totals[tag]['tier watch ' + e['tier']] += 1
        for iid in key['company_guard']:
            s = sg.kept(runs.get(iid), iid)
            for e in (s or {}).get('evidence', []):
                totals[tag]['company records'] += 1
                totals[tag]['company who names nvidia'] += 'nvidia' in (e.get('original_who') or '').lower()
                totals[tag]['company day = publication day'] += (e.get('original_day') or '') == pubs[iid]
    for name in dict.fromkeys(n for n, *_ in lines):
        print(name.ljust(4), ' | '.join(f'{v} [{w[:24]}]' for n, t, v, w in lines if n == name))
    cols = sorted({k for c in totals.values() for k in c})
    print('\n' + 'measure'.ljust(32) + ''.join(t.rjust(12) for t in tags))
    for k in cols:
        print(k.ljust(32) + ''.join(str(totals[t][k]).rjust(12) for t in tags))
    print('rows: K', sum(r[0][0] == 'K' for r in key['rows']), 'G', sum(r[0][0] == 'G' for r in key['rows']))


if __name__ == '__main__':
    main(sys.argv[1:])
