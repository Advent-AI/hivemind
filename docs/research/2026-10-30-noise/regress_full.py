"""Core and supporting gold entries whose kept-draw count fell from the control to the arm on a full run (per-article files of
final_scores.py), and those that rose, listed for reading.   python3 regress_full.py Y v53 v59 dev"""
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402

prefix, control, arm, set_name = sys.argv[1:5]
rows = json.loads((LEDGER / 'final-2026-10-30' / f'per-article-{prefix}-{set_name}.json').read_text())
articles = {a['input_id']: a for a in json.loads(Path(fs.GOLDS[set_name]).read_text())['articles']}
for weight, key in (('core', 'core'), ('supporting', 'supp')):
    lost, gained = [], []
    for iid, a in articles.items():
        items = [i for i in a['items'] if i['weight'] == weight]
        for idx, item in enumerate(items):
            c, r = sum(rows[control][iid][key][idx]), sum(rows[arm][iid][key][idx])
            if r < c:
                lost.append((c, r, iid, a['title'][:50], item['span'][:150]))
            elif r > c:
                gained.append((c, r, iid, a['title'][:50], item['span'][:150]))
    print(f'== {weight}: lost {len(lost)} entries ({sum(c - r for c, r, *_ in lost)} draws), gained {len(gained)} ({sum(r - c for c, r, *_ in gained)} draws)')
    for c, r, iid, title, span in sorted(lost, key=lambda x: x[1] - x[0]):
        print(f'   - {c}->{r} {iid[:26]} | {title} | {span}')
