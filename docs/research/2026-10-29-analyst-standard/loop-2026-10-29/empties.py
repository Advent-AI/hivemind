"""Articles whose answer is empty in a run, with what the reference keeps there and what the other run kept."""
import json, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import bench_v23 as bench
refs = {}
for name in ('reference-week-v2.json', 'reference-holdout-v2.json'):
    for art in json.loads((HERE.parent / name).read_text())['articles']:
        refs[art['input_id']] = art
def load(tag):
    db = sqlite3.connect(f"file:{HERE / tag / 'answers.sqlite'}?mode=ro", uri=True)
    return {i: (bench.sift_answer(json.loads(c) if c else None, d, i, cfg), json.loads(c) if c else None) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
old, new = load(sys.argv[1]), load(sys.argv[2])
items = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True)
for i, (rec, raw) in new.items():
    if rec['sift']['evidence'] or rec['sift']['candidates']:
        continue
    title = (items.execute('select title from items where input_id=?', (i,)).fetchone() or [''])[0]
    st = [f"{s['weight']}: {s['note'][:90]}" for s in refs[i].get('statements', []) if s['weight'] in ('core', 'supporting')]
    o = old[i][0]['sift']['evidence'] if old.get(i) and old[i][0]['sift'] else []
    print(f"## {i} | {title[:90]}\n   raw evidence {len((raw or {}).get('evidence', []))}, dropped {rec['sift']['dropped'][:3]}\n   reference: {st or 'nothing core/supporting'}\n   {sys.argv[1]} kept {len(o)}: " + ' ‖ '.join(e['one_line'][:90] for e in o[:4]))
