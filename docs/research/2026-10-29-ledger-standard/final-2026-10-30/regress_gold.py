"""Regressions and gains on the signed gold between two versions of one simultaneous run, entry by entry (page §9.2;
handoff plan §4: the old surprise.py read reference v2, not the signed gold). Reads per-article-<PREFIX>-<set>.json written
by final_scores.py and the frozen golds (sha256 printed): a core or supporting entry the control kept in at least two of
three draws and the arm in at most one is a regression to read; the reverse is a gain. Must-open questions likewise.
Every printed entry is a lead: read the arm's raw answer beside the article before calling it a regression.

    python3 regress_gold.py PREFIX v<control> v<arm>
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GOLDS = {'dev': HERE.parent / 'golden-v3/golden-v3-signed.json', 'test': HERE.parent / 'test-set/golden-test-signed.json'}


def main(prefix, control, arm):
    for name, path in GOLDS.items():
        print(f'## {name}: gold sha256 {hashlib.sha256(path.read_bytes()).hexdigest()[:16]}')
        gold = {a['input_id']: a for a in json.loads(path.read_text())['articles']}
        rows = json.loads((HERE / f'per-article-{prefix}-{name}.json').read_text())
        lost, won = [], []
        for iid, a in gold.items():
            c, x = rows[control][iid], rows[arm][iid]
            for weight in ('core', 'supp'):
                items = [it for it in a['items'] if it['weight'] == ('core' if weight == 'core' else 'supporting')]
                for it, hc, hx in zip(items, c[weight], x[weight]):
                    if sum(hc) >= 2 and sum(hx) <= 1:
                        lost.append((weight, iid, hc, hx, it['span'][:120]))
                    elif sum(hx) >= 2 and sum(hc) <= 1:
                        won.append((weight, iid, hc, hx, it['span'][:120]))
            for q, hc, hx in zip(a.get('questions', {}).get('must_open', []), c['must_open'], x['must_open']):
                if sum(hc) >= 2 and sum(hx) <= 1:
                    lost.append(('must_open', iid, hc, hx, q['gist'][:120]))
                elif sum(hx) >= 2 and sum(hc) <= 1:
                    won.append(('must_open', iid, hc, hx, q['gist'][:120]))
        for label, entries in (('LOST by ' + arm, lost), ('GAINED by ' + arm, won)):
            print(f'{label}: {len(entries)} (core {sum(e[0] == "core" for e in entries)}, supporting {sum(e[0] == "supp" for e in entries)}, '
                  f'must-open {sum(e[0] == "must_open" for e in entries)})')
            for w, iid, hc, hx, text in entries:
                print(f'  {w:9} {iid[:34]:34} {control} {sum(hc)}/3  {arm} {sum(hx)}/3  {text}')


if __name__ == '__main__':
    main(*sys.argv[1:4])
