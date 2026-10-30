"""Whether chosen reference statements are kept in every stored run (role-v22 draws, v23 draw 1, loop runs): is a loss a trend or noise."""
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
for tag in sys.argv[2:]:
    db = sqlite3.connect(f"file:{HERE / tag / 'answers.sqlite'}?mode=ro", uri=True)
    runs[tag] = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
for want in sys.argv[1].split(','):
    i, _, word = want.partition('~')
    for item in refs[i].get('statements', []):
        if word.lower() not in item['note'].lower():
            continue
        row = []
        for tag, recs in runs.items():
            rec = recs.get(i)
            ev = (rec['answer'] or {}).get('evidence', []) if rec and rec['answer'] else []
            kept = {e['id'] for e in rec['sift']['evidence']} if rec and rec['sift'] else set()
            hits = [e for e in ev if sw.matches(e['quote'], item)]
            row.append('K' if any(e['id'] in kept for e in hits) else ('r' if hits else '.'))
        print(' '.join(row), '|', i[-8:], item['weight'], item['note'][:70])
print('runs:', ' '.join(runs))
