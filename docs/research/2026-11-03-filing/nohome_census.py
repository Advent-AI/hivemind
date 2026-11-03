"""Statements the extraction wrote and the handover dropped as 'no home', per draw, split by a keyword reading (rough, to be read by a
person): the covered company's own reported or guided figures, other statements about the company, and the rest. Samples of the first
kind. $0, read-only.

    python3 nohome_census.py
"""
import sqlite3, json, re, collections
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
RUNS = {'v94': ROOT.parent / 'hivemind-extraction-quality-2026-10-28/docs/research/2026-11-01-e2e-loop/arms/r7-combined-v94', 'v108': ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03'}
OWN = re.compile(r'\b(nvidia|nvda)\b.*\b(revenue|sales|margin|eps|earnings per share|cash flow|guid|net income|operating income|repurchas|buyback)', re.I)
for name, base in RUNS.items():
    for d in (1, 2, 3):
        c = sqlite3.connect(f'file:{base}/d{d}/views.sqlite?mode=ro', uri=True); a = sqlite3.connect(f'file:{base}/d{d}/archive.sqlite?mode=ro', uri=True)
        dropped = {}
        for inp, hj in c.execute('select input_id, handover_json from handovers'):
            ids = {eid for eid, why in json.loads(hj).get('dropped', []) if why == 'no home'}
            if ids: dropped[inp] = ids
        kinds = collections.Counter(); samples = []; written = 0
        for (rj, aj) in a.execute("select request_json, answer_json from model_calls where purpose='extract' and answer_json is not null"):
            m = re.search(r'\[Item\] id ([^,]+),', rj)
            if not m: continue
            ev = json.loads(aj).get('evidence', []); written += len(ev)
            for e in ev:
                if e['id'] in dropped.get(m.group(1), set()):
                    t = e.get('one_line', '')
                    k = 'own reported or guided figure' if OWN.search(t) else ('other, about the company' if re.search(r'\b(nvidia|nvda)\b', t, re.I) else 'other')
                    kinds[k] += 1
                    if k.startswith('own') and len(samples) < 4: samples.append(t[:130])
        print(f'{name} d{d}: written {written}, dropped no home {sum(kinds.values())}: {dict(kinds)}')
        for s in samples: print('     ', s)
