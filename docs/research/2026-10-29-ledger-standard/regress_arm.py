"""Page §9.3 step 4 (D243 proposal 8): an arm's one send on the development set against the baseline's three draws.
A regression signal is a core or supporting gold entry the baseline kept in every draw and the arm lost. Also prints
the noise counts side by side. Every signal is then read (D244).

    python3 regress_arm.py BASELINE_SCORE_DIR ARM_SCORE_DIR
"""
import json, sys
from pathlib import Path
base, arm = Path(sys.argv[1]), Path(sys.argv[2])
bh = {(h['input_id'], h['k']): h for h in json.loads((base / 'hits.json').read_text())}
ah = {(h['input_id'], h['k']): h for h in json.loads((arm / 'hits.json').read_text())}
signals = [ah[k] for k in ah if ah[k]['weight'] in ('core', 'supporting') and all(bh[k]['hits']) and not any(ah[k]['hits'])]
gains = [ah[k] for k in ah if ah[k]['weight'] in ('core', 'supporting') and not any(bh[k]['hits']) and all(ah[k]['hits'])]
bs, as_ = json.loads((base / 'scores.json').read_text())['per_draw'], json.loads((arm / 'scores.json').read_text())['per_draw']
def mean(d, key): return round(sum(v.get(key, 0) for v in d.values()) / len(d), 1)
print('regression signals (kept in every baseline draw, lost by the arm):', len(signals))
for s in signals: print('  ', s['weight'], s['input_id'][-12:], '|', s['span'][:140])
print('entries never kept by the baseline and kept by the arm:', len(gains))
for g in gains: print('  ', g['weight'], g['input_id'][-12:], '|', g['span'][:140])
for key in ('statements kept', 'core kept', 'supporting kept', 'optional kept', 'kept a not-kept sentence', 'extra (not in gold)', 'candidates kept', 'statements dropped by code'):
    print(f'{key:28s} baseline mean {mean(bs, key):7} | arm {mean(as_, key):7}')
