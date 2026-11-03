"""Recount core and supporting gold entries on a full run with one consistency rule on top of final_scores.py's counting aid: a draw
counts as a hit when it keeps a statement whose quote is identical to a quote that hit the same gold entry in any draw of any version
compared (the aid matches quote and one_line together, so the same quote with a reworded summary can hit in one draw and miss in another).

    python3 recount_consistent.py Y2 v53 v60 v61
"""
import json
import sys
from pathlib import Path

LEDGER = Path(__file__).resolve().parent.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

prefix, versions = sys.argv[1], sys.argv[2:]
for set_name in ('dev', 'test'):
    articles = json.loads(Path(fs.GOLDS[set_name]).read_text())['articles']
    kept = {v: [{a['input_id']: sg.kept(run.get(a['input_id']), a['input_id']) for a in articles}
                for run in (sg.answers(f'{prefix}-{v}-d{d}') for d in (1, 2, 3))] for v in versions}
    totals = {v: {'core every draw': 0, 'core draws': 0, 'supporting >=2 draws': 0, 'supporting draws': 0, 'recovered draws': 0} for v in versions}
    for a in articles:
        iid = a['input_id']
        for item in a['items']:
            if item['weight'] not in ('core', 'supporting'):
                continue
            hit_quotes = {sg.norm(e['quote']) for v in versions for s in kept[v] if s.get(iid) for e in s[iid]['evidence'] if sg.same_matter(item, e)}
            for v in versions:
                hits = 0
                for s in kept[v]:
                    ev = s[iid]['evidence'] if s.get(iid) else []
                    aid = any(sg.same_matter(item, e) for e in ev)
                    consistent = aid or any(sg.norm(e['quote']) in hit_quotes for e in ev)
                    hits += consistent
                    totals[v]['recovered draws'] += consistent and not aid
                if item['weight'] == 'core':
                    totals[v]['core every draw'] += hits == 3
                    totals[v]['core draws'] += hits
                else:
                    totals[v]['supporting >=2 draws'] += hits >= 2
                    totals[v]['supporting draws'] += hits
    print(f'== {set_name}')
    for v in versions:
        print(f'   {v}:', totals[v])
