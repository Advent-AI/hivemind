"""The acceptance's measure (acceptance-design.md, written and pinned before launch): each draw of the candidate (poc-v116) and of the same-day control
(poc-v108) scored by the frozen judgement scorer at the window end, then the conditions:
  1. v10 and v12 each agree in at least 2 of the 3 candidate draws;
  2. for each scored question, candidate agreements >= control agreements - 1; a question that drops by two or more is listed to be read (it counts
     against the candidate only when its reasons show the starting figures caused the wrong answer);
  3. the totals, reported.
Also printed: each candidate draw's coverage-start record (questions linked, records, figures kept and refused), and each draw's cost from tokens at the
published rates. Reads finished runs only (run.out ends with RUN-ARM-DONE); never a live ledger.

usage: python3 acceptance_measure.py <candidate arm folder> <control arm folder>
"""
import json
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src']
from hivemind import model  # noqa: E402

SCORER = f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold/score_judgement.py'
NEEDS = ('v10', 'v12')


def finished(run):
    out = Path(run) / 'run.out'
    return not out.exists() or 'RUN-ARM-DONE' in out.read_text()      # a copied, sealed run has no run.out


def outcomes(run):
    printed = subprocess.run([sys.executable, SCORER, str(run)], capture_output=True, text=True, check=True).stdout
    return {f'v{int(m.group(1))}': m.group(2) for m in re.finditer(r'^q(\d\d) (agree|DISAGREE|no judgement)', printed, re.M) if int(m.group(1)) <= 22}


def cost(run):
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    total = 0.0
    for name, tokens_in, tokens_out in archive.execute('select model, sum(input_tokens), sum(output_tokens) from model_calls group by model'):
        price_in, price_out = model.PRICES.get(name, (0.0, 0.0))
        total += (tokens_in or 0) / 1e6 * price_in + (tokens_out or 0) / 1e6 * price_out
    return total


def coverage_start_record(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    row = views.execute("select reason from processing_steps where step='baseline'").fetchone()
    return json.loads(row[0]) if row else None


def main():
    candidate, control = (sorted(p for p in Path(arm).iterdir() if p.is_dir() and p.name.startswith('d')) for arm in sys.argv[1:3])
    unfinished = [str(r) for r in candidate + control if not finished(r)]
    if unfinished:
        raise SystemExit(f'not finished: {unfinished}')
    by_arm = {'candidate': [outcomes(r) for r in candidate], 'control': [outcomes(r) for r in control]}
    questions = sorted({q for o in by_arm['candidate'] + by_arm['control'] for q in o}, key=lambda v: int(v[1:]))
    agree = lambda arm, q: sum(1 for o in by_arm[arm] if o.get(q) == 'agree')
    print(f'{"question":9} {"candidate":28} {"control":28} agree c/k')
    to_read = []
    for q in questions:
        c, k = agree('candidate', q), agree('control', q)
        flag = 'DROP of 2+: read the reasons' if c <= k - 2 else ''
        if flag:
            to_read.append(q)
        print(f'{q:9} {" ".join(o.get(q, "-")[:8] for o in by_arm["candidate"]):28} {" ".join(o.get(q, "-")[:8] for o in by_arm["control"]):28} {c}/{k}  {flag}')
    total_c = sum(agree('candidate', q) for q in questions)
    total_k = sum(agree('control', q) for q in questions)
    gap = {q: agree('candidate', q) for q in NEEDS}
    print(f'\ncondition 1 (v10, v12 each agree in at least 2 of 3 candidate draws): {"pass" if all(v >= 2 for v in gap.values()) else "FAIL"} {gap}')
    print(f'condition 2 (no question drops by two or more without its reasons read): {"nothing to read" if not to_read else "READ " + str(to_read)}')
    print(f'condition 3 (totals, reported): candidate {total_c}, control {total_k} agreements over {len(questions)} questions x 3 draws')
    for run in candidate:
        record = coverage_start_record(run)
        if record:
            print(f'{run.name}: coverage-start reading linked {record["changed"]}, {record.get("records")} records, {record["kept"]} figures kept, '
                  f'{len(record["refused"])} refused {[(r["view_id"], r["value"], r["reason"]) for r in record["refused"]]}')
    print('cost: ' + '; '.join(f'{r.parent.name}/{r.name} ${cost(r):.2f}' for r in candidate + control))


if __name__ == '__main__':
    main()
