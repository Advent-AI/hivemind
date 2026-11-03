"""Evidence refused as 'quote not in item' per run, and how many of those quotes join text from separate places of the item."""
import json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bench_v23 as bench
base = json.loads((bench.RUN / 'sifted.json').read_text())
runs = {d: base[d] for d in ('luna-1', 'luna-2', 'luna-3', 'v23-1')}
for tag in sys.argv[1:]:
    db = sqlite3.connect(f"file:{HERE / tag / 'answers.sqlite'}?mode=ro", uri=True)
    runs[tag] = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
for tag, recs in runs.items():
    written = refused = joined = 0
    for i, rec in recs.items():
        if not rec or not rec['sift']:
            continue
        ev = {e['id']: e for e in (rec['answer'] or {}).get('evidence', [])}
        written += len(ev)
        for eid, why in rec['sift']['dropped']:
            if why == 'quote not in item' and eid in ev:
                refused += 1
                joined += len([s for s in ev[eid]['quote'].replace('…', '. ').split('. ') if len(s) > 25]) >= 3
    print(f'{tag:7} written {written:4}  quote refused {refused:3} ({100 * refused / max(written, 1):.1f}%)  of which 3+ sentences {joined}')
