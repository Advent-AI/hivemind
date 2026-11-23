"""Exploratory calibration of the Stage 2 decision rule (D392, plan v4): how often would the rule call a difference between two sets of
three draws of the same configuration? The six stored v108 draws (r9 d1-d3 and the r10 control d1-d3) are scored with the frozen scorer
and every split into two sets of three is compared. The threshold chosen is the smallest total difference whose false-call rate is at
most 10%, with and without the reader-noise questions (q09, q12, q23). Six historical draws cannot establish today's rate or rule out
model drift; the result is labelled exploratory."""
import itertools, json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCORER = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py'
DRAWS = [ROOT / f'poc/data/e2e-r9-frozen-v108-2026-11-03/d{d}' for d in (1, 2, 3)] + \
        [ROOT / f'docs/research/2026-11-01-e2e-loop/arms/r10-control-v108/d{d}' for d in (1, 2, 3)]
NOISE = {'q09', 'q12', 'q23'}


def outcomes(run):
    out = subprocess.run([sys.executable, str(SCORER), str(run)], capture_output=True, text=True, check=True).stdout
    return {m.group(1): m.group(2) for m in re.finditer(r'^(q\d\d) (\S+)', out, re.M)}


def total(draw_set, exclude=()):
    return sum(1 for o in draw_set for q, v in o.items() if q not in exclude and v == 'agree')


def collapse(a, b):
    """A question that set a agrees in at least 2 of 3 and set b in 0 of 3."""
    return any(sum(o[q] == 'agree' for o in a) >= 2 and sum(o[q] == 'agree' for o in b) == 0 for q in a[0])


def main():
    scored = [outcomes(run) for run in DRAWS]
    rows = []
    for exclude, label in (((), 'all questions'), (NOISE, 'without q09, q12, q23')):
        splits = [(list(a), [scored[i] for i in range(6) if i not in a_idx]) for a_idx in itertools.combinations(range(6), 3)
                  for a in [[scored[i] for i in a_idx]]]
        diffs = [abs(total(a, exclude) - total(b, exclude)) for a, b in splits]
        collapses = sum(collapse(a, b) for a, b in splits)
        for threshold in range(1, 8):
            rate = sum(d >= threshold for d in diffs) / len(diffs)
            rows.append({'set': label, 'threshold': threshold, 'false_call_rate': round(rate, 3)})
        chosen = next(r['threshold'] for r in rows if r['set'] == label and r['false_call_rate'] <= 0.10)
        print(f'{label}: totals per draw {[total([o], exclude) for o in scored]}; split differences {sorted(diffs)}; '
              f'collapse in {collapses} of {len(splits)} splits; threshold {chosen}')
    (HERE / 'calibration.json').write_text(json.dumps({'draws': [str(d.relative_to(ROOT)) for d in DRAWS], 'rows': rows}, indent=1))


if __name__ == '__main__':
    main()
