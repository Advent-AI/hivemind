"""For every core gold entry whose kept-draw count differs between two versions of a full run (the counting aid of final_scores.py),
print the gold entry and, per draw, each version's statements on that article that share content words with it, so a reader decides
whether the matter is kept under another sentence (a counting miss) or truly lost.   python3 adjudicate_core.py Y2 v53 v61 dev"""
import json
import sqlite3
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

prefix, control, arm, set_name = sys.argv[1:5]
weight, key = (sys.argv[5], 'supp') if len(sys.argv) > 5 and sys.argv[5] == 'supporting' else ('core', 'core')
rows = json.loads((LEDGER / 'final-2026-10-30' / f'per-article-{prefix}-{set_name}.json').read_text())
articles = {a['input_id']: a for a in json.loads(Path(fs.GOLDS[set_name]).read_text())['articles']}
for iid, a in articles.items():
    items = [i for i in a['items'] if i['weight'] == weight]
    for idx, item in enumerate(items):
        c, r = rows[control][iid][key][idx], rows[arm][iid][key][idx]
        if sum(c) == sum(r):
            continue
        g = sg.words(item['span'] + ' ' + str((item.get('meaning') or {}).get('what', ''))) - sg.STOP
        print(f"\n### {iid} | {control} {sum(c)}/3 vs {arm} {sum(r)}/3 | gold: {item['span'][:200]}")
        for version, hits in ((control, c), (arm, r)):
            for d in (1, 2, 3):
                s = sg.kept(sg.answers(f'{prefix}-{version}-d{d}').get(iid), iid)
                near = [e for e in (s or {}).get('evidence', []) if len(g & (sg.words(e['quote'] + ' ' + e.get('one_line', '')) - sg.STOP)) >= 3]
                mark = 'HIT ' if hits[d - 1] else 'miss'
                print(f"   {version} d{d} {mark}: " + (' || '.join(e['quote'][:110] for e in near[:2]) or '(nothing near)'))
