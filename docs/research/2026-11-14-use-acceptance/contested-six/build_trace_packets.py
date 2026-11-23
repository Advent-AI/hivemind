"""Blind reading of the six contested answers and two controls (council round 12; $0). Per question: the whole last request,
the answer, and candidate statements not in the request, dated by its day, each with its source passage. Candidates are found by a
text pattern per matter (a hint written by Claude, listed in PATTERNS; code judges nothing). Controls: the July custom-chip answer
with the five facts that moved it in PRD 10's test (a group), and the supply-commitments answer (uncontested) whose candidates
are repeats of statements already shown. Shuffled; the key outside the repository.

  python3 build_trace_packets.py <key folder>
"""
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RUN = ROOT / 'poc/data/clean-carried-run-2026-11-16/c1/judge/draw-c1'
JULY = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
SEED = 20261117
PATTERNS = {
    'v1': r'guarantee|credit support|backstop|residual[- ]value',
    'v5': r'capex|capital expenditure|capital spending|data[- ]center spending',
    'v10': r'(GW|gigawatt)',
    'v11': r'memory price|DRAM|HBM price|contract price',
    'v12': r'residual[- ]value|\$125 billion|backstop',
    'v13': r'CPO|co-packaged|optical|photonic|Lumentum',
    'v2': r'supply commitment|purchase obligation|\$279 billion',
}
CONTROL_FACTS = ['e219', 'e136', 'e387', 'e153', 'e139']


def last_of(store, archive, view):
    day, sha = store.execute('select publication_day, request_sha256 from judgements where view_id=? order by seq desc, judgement_id desc limit 1', (view,)).fetchone()
    request = json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])['messages'][-1]['content']
    answer = json.loads(archive.execute('select answer_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])
    return day, request, {k: answer.get(k) for k in ('rung', 'reference', 'reasons', 'implied_outcome')}


def statement(store, evidence_id):
    one_line, quote, who = store.execute('select one_line, quote, original_who from evidence where evidence_id=?', (evidence_id,)).fetchone()
    day = store.execute('select min(publication_day) from evidence_sources where evidence_id=?', (evidence_id,)).fetchone()[0]
    return {'day': day, 'party': who, 'statement': one_line, 'passage': quote}


def main(keys):
    store = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    archive = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True)
    shown = {r['view']: set(r['shown']) for r in json.loads((RUN / 'judge-requests.json').read_text())}
    cases = []
    for view, pattern in PATTERNS.items():
        day, request, answer = last_of(store, archive, view)
        candidates = []
        for evidence_id, one_line in store.execute('select evidence_id, one_line from evidence'):
            if evidence_id in shown[view] or not re.search(pattern, one_line or '', re.I):
                continue
            entry = statement(store, evidence_id)
            if entry['day'] and entry['day'] <= day:
                candidates.append(entry)
        cases.append({'source': view, 'day': day, 'request': request, 'answer': answer, 'candidates': candidates})
    july = sqlite3.connect(f"file:{JULY / 'views.sqlite'}?mode=ro", uri=True)
    july_archive = sqlite3.connect(f"file:{JULY / 'archive.sqlite'}?mode=ro", uri=True)
    day, request, answer = last_of(july, july_archive, 'v16')
    cases.append({'source': 'positive control: July custom-chip v16 (PRD 10 test: these facts moved it 9 of 9)', 'day': day,
                  'request': request, 'answer': answer, 'candidates': [statement(july, e) for e in CONTROL_FACTS]})
    rng = random.Random(SEED)
    rng.shuffle(cases)
    for case in cases:
        rng.shuffle(case['candidates'])
    packet = [{'question': f'Q{n}', 'answered_on': c['day'], 'request': c['request'], 'answer': c['answer'],
               'candidates': [dict(s, ref=f'C{k}') for k, s in enumerate(c['candidates'], 1)]} for n, c in enumerate(cases, 1)]
    halves = [packet[:4], packet[4:]]
    for n, half in enumerate(halves, 1):
        path = HERE / f'packet-trace-{n}.json'
        path.write_text(json.dumps(half, indent=1, ensure_ascii=False) + '\n')
        print(f'packet {n}: {[q["question"] for q in half]}, candidates {[len(q["candidates"]) for q in half]}, {len(path.read_text()):,} characters')
    Path(keys).mkdir(parents=True, exist_ok=True)
    (Path(keys) / 'key-trace.json').write_text(json.dumps({f'Q{n}': c['source'] for n, c in enumerate(cases, 1)}, indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1])
