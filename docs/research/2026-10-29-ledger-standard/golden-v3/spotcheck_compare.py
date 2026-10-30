"""Compare the blind spot-check reader with golden-v3 on the same 15 articles: which golden items the reader kept (and at
which weight), which it did not, and what it kept that golden does not. Spans match when one contains the other or their
word sets overlap by half or more of the shorter."""
import json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
gold = {a['input_id']: a for a in json.loads((HERE / 'golden-v3.json').read_text())['articles']}
read = json.loads((HERE / 'spotcheck-codex.json').read_text())
W = lambda t: set(re.findall(r"[A-Za-z0-9$%.]+", t.lower()))


def same(a, b):
    if a in b or b in a:
        return True
    x, y = W(a), W(b)
    return bool(x and y) and len(x & y) >= 0.5 * min(len(x), len(y))


tot = dict(gold_items=0, found=0, weight_same=0, missed=0, extra=0)
lines = []
for r in read:
    g = gold[r['input_id']]
    gi = [it for it in g['items'] if it['weight_current'] != 'excluded']
    ri = [it for it in r['items'] if it.get('weight_current') != 'excluded']
    used = set()
    for it in gi:
        tot['gold_items'] += 1
        hit = [j for j, x in enumerate(ri) if same(it['span'], x['span'])]
        if hit:
            tot['found'] += 1; used.update(hit)
            ws = {ri[j].get('weight_current') for j in hit}
            if it['weight_current'] in ws:
                tot['weight_same'] += 1
            else:
                lines.append(f"WEIGHT {r['input_id'][-10:]} gold {it['weight_current']} reader {sorted(ws)} | {it['span'][:110]}")
        else:
            tot['missed'] += 1; lines.append(f"MISSED {r['input_id'][-10:]} gold {it['weight_current']} | {it['span'][:120]}")
    for j, x in enumerate(ri):
        if j not in used:
            tot['extra'] += 1; lines.append(f"EXTRA  {r['input_id'][-10:]} reader {x.get('weight_current')} | {x['span'][:120]} || {x.get('reason', '')[:80]}")
    gq = sorted((q.get('type') for q in g['questions'].get('must_open', [])), key=str)
    rq = sorted((q.get('type') for q in r.get('must_open', [])), key=str)
    if gq != rq:
        lines.append(f"QUESTIONS {r['input_id'][-10:]} gold {gq} reader {rq}")
print(tot)
print('\n'.join(lines))
