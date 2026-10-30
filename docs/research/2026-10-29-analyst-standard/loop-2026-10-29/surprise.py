"""Per run: core and supporting statements every other run keeps but this run does not (a surprise loss), the regression signal
against the noise of single sends. Runs: role-v22 draws and the named loop runs."""
import json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bench_v23 as bench, score_week as sw
refs = {}
for name in ('reference-week-v2.json', 'reference-holdout-v2.json'):
    for art in json.loads((HERE.parent / name).read_text())['articles']:
        refs[art['input_id']] = art
base = json.loads((bench.RUN / 'sifted.json').read_text())
runs = {d: base[d] for d in ('luna-1', 'luna-2', 'luna-3')}
for tag in sys.argv[1:]:
    db = sqlite3.connect(f"file:{HERE / tag / 'answers.sqlite'}?mode=ro", uri=True)
    runs[tag] = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
table = {}
for i, art in refs.items():
    for item in art.get('statements', []):
        if item['weight'] not in ('core', 'supporting'):
            continue
        row = {}
        for tag, recs in runs.items():
            rec = recs.get(i)
            ev = (rec['answer'] or {}).get('evidence', []) if rec and rec['answer'] else []
            kept = {e['id'] for e in rec['sift']['evidence']} if rec and rec['sift'] else set()
            row[tag] = any(e['id'] in kept for e in ev if sw.matches(e['quote'], item))
        table[(i, item['note'])] = row
for tag in runs:
    lost = [k for k, row in table.items() if not row[tag] and all(v for t, v in row.items() if t != tag)]
    print(f'{tag:8} surprise losses {len(lost):2}  ' + ' ‖ '.join(f'{i[-8:]} {n[:50]}' for i, n in lost))
