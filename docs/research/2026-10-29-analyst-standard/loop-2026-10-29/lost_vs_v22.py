import json, sys, sqlite3
from pathlib import Path
A = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard')
sys.path.insert(0, str(A))
import bench_v23 as bench, score_week as sw
base = json.loads((bench.RUN / 'sifted.json').read_text())
db = sqlite3.connect(f"file:{A / 'loop-2026-10-29/v29/answers.sqlite'}?mode=ro", uri=True)
v29 = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
refs = {}
for name in ('reference-week-v2.json', 'reference-holdout-v2.json'):
    for art in json.loads((A / name).read_text())['articles']:
        refs[art['input_id']] = art
def state(rec, item):
    ev = (rec['answer'] or {}).get('evidence', []); kept = {e['id'] for e in rec['sift']['evidence']}
    return any(e['id'] in kept for e in ev if sw.matches(e['quote'], item))
for i, art in refs.items():
    for item in art.get('statements', []):
        if item['weight'] in ('core', 'supporting') and not state(v29[i], item):
            v22 = sum(state(base[d][i], item) for d in ('luna-1', 'luna-2', 'luna-3'))
            print(f"{item['weight']:10} v22 kept {v22}/3 | {i[:30]} | {item['note'][:90]}")
            print('      v29 one_lines:', ' ‖ '.join(e['one_line'][:110] for e in v29[i]['sift']['evidence'])[:600])
