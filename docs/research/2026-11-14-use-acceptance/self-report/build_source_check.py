"""The source check's cases and packets ($0; SOURCE-CHECK-DESIGN.md): the baseline reading's figure answers settled INSUFFICIENT or
UNSUPPORTED (rejected) and an equal number both first readers passed, drawn by a fixed seed from the same question paths. Each case
is the stored request and answer, blind to the verdict and the set; shuffled into two packets; the key outside the repository.

  python3 build_source_check.py <key folder holding stage-b-baseline-key.json>
"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'))
import baseline_count, stored_judgements  # noqa: E402

READING = ROOT / 'poc/data/clean-stage-b-baseline-2026-11-10'
FAMILIES = ('codex', 'claude')
SEED = 20261118
# Checked by Claude before any reading (SOURCE-CHECK-DESIGN.md, "Controls"); Stage B answers outside the 22.
CONTROLS = [  # (store folder, judgement id, expected marks); every recorded mark is checked
    (ROOT / 'poc/data/clean-carried-run-2026-11-16/c1/judge/draw-c1', 89,
     {'bears': 'direct', 'supports_band': 'yes', 'step_decides': 'no'}),     # e674: NVIDIA's stated $1.3T for calendar 2027, inside rung 3
    (ROOT / 'poc/data/clean-stage-b-2026-11-11/draw-u3', 39, {'bears': 'none_shown'}),   # HBM wafer capacity: no capacity figure shown
    (ROOT / 'poc/data/clean-stage-b-2026-11-11/draw-u3', 15,
     {'bears': 'comparable', 'step_decides': 'yes'}),                       # Sharon AI's stated $4.88bn scaled by GPU count to Firmus decides rung 5
]


def store_of(folder):
    for candidate in (folder, *sorted(p for p in folder.iterdir() if p.is_dir())):
        if (candidate / 'views.sqlite').exists() and (candidate / 'archive.sqlite').exists():
            return candidate
    raise SystemExit(f'no store under {folder}: refused')


def main(key_folder):
    key = json.loads((Path(key_folder) / 'stage-b-baseline-key.json').read_text())
    first = {f: {} for f in FAMILIES}
    third = {f: {} for f in FAMILIES}
    for f in FAMILIES:
        for p in sorted((READING / 'readers-answers').glob(f'reader-{f}-packet-*.jsonl')):
            first[f].update(baseline_count.rows_in(p)[0])
        for p in sorted((READING / 'third-reader').glob(f'rulings-{f}-*.jsonl')):
            third[f].update(baseline_count.rows_in(p)[0])
    rejected, passed = [], []
    for number, entry in key.items():
        if entry['kind'] != 'stored' or entry['shape'] != 'figure':
            continue
        n = int(number)
        pair = [first[f][n]['verdict'] for f in FAMILIES]
        rulings = {third[f].get(n, {}).get('verdict') for f in FAMILIES}
        settled = pair[0] if pair[0] == pair[1] else (rulings.pop() if len(rulings) == 1 else 'unresolved')
        if settled in ('INSUFFICIENT', 'UNSUPPORTED'):
            rejected.append((n, entry, settled))
        elif pair == ['SUPPORTED', 'SUPPORTED']:
            passed.append((n, entry, 'SUPPORTED by both'))
    paths = {(e['draw'], e['view']) for _, e, _ in rejected}
    same_path = [p for p in passed if (p[1]['draw'], p[1]['view']) in paths]
    rng = random.Random(SEED)
    accepted = rng.sample(same_path, len(rejected)) if len(same_path) >= len(rejected) else same_path
    cases = []
    for group, rows in (('rejected', rejected), ('accepted', accepted)):
        for n, entry, verdict in rows:
            folder = store_of(stored_judgements.DRAWS[entry['draw']])
            views = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
            archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
            sha = views.execute('select request_sha256 from judgements where judgement_id = ?', (entry['judgement_id'],)).fetchone()[0]
            request_json, answer_json = archive.execute('select request_json, answer_json from model_calls where request_sha256 = ? and answer_json is not null', (sha,)).fetchone()
            user = next(m['content'] for m in json.loads(request_json)['messages'] if m['role'] == 'user')
            answer = json.loads(answer_json)
            cases.append({'group': group, 'verdict': verdict, 'draw': entry['draw'], 'view': entry['view'], 'day': entry['day'], 'judgement': n,
                          'request': user, 'answer': {k: answer.get(k) for k in ('rung', 'reference', 'reasons', 'implied_outcome')}})
    for folder, judgement_id, expected in CONTROLS:
        draw = folder.name
        views = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        view, day, sha = views.execute('select view_id, publication_day, request_sha256 from judgements where judgement_id = ?', (judgement_id,)).fetchone()
        request_json, answer_json = archive.execute('select request_json, answer_json from model_calls where request_sha256 = ? and answer_json is not null', (sha,)).fetchone()
        user = next(m['content'] for m in json.loads(request_json)['messages'] if m['role'] == 'user')
        answer = json.loads(answer_json)
        cases.append({'group': 'control', 'verdict': expected, 'draw': draw, 'view': view, 'day': day, 'judgement': judgement_id,
                      'request': user, 'answer': {k: answer.get(k) for k in ('rung', 'reference', 'reasons', 'implied_outcome')}})
    rng.shuffle(cases)
    packet = [{'case': f'K{i}', 'request': c['request'], 'answer': c['answer']} for i, c in enumerate(cases, 1)]
    parts = [packet[i::4] for i in range(4)]
    for n, part in enumerate(parts, 1):
        path = HERE / f'packet-source-check-{n}.json'
        path.write_text(json.dumps(part, indent=1, ensure_ascii=False) + '\n')
        print(f'packet {n}: {len(part)} cases, {len(path.read_text()):,} characters')
    (Path(key_folder) / 'key-source-check.json').write_text(json.dumps(
        {f'K{i}': {k: c[k] for k in ('group', 'verdict', 'draw', 'view', 'day', 'judgement')} for i, c in enumerate(cases, 1)}, indent=1) + '\n')
    print(f"controls {len(CONTROLS)}; rejected {len(rejected)} on paths {sorted(paths)}; accepted {len(accepted)} drawn from {len(same_path)} on the same paths")


if __name__ == '__main__':
    main(sys.argv[1])
