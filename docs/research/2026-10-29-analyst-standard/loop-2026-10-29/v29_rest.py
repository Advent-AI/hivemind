import json, sys, sqlite3, collections
from pathlib import Path
A = Path('/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard')
sys.path.insert(0, str(A))
import bench_v23 as bench, score_week as sw
db = sqlite3.connect(f"file:{A / 'loop-2026-10-29/v29/answers.sqlite'}?mode=ro", uri=True)
recs = {i: bench.sift_answer(json.loads(c) if c else None, d, i, cfg) for i, c, d, cfg in db.execute('select input_id, content, completed, config from answers')}
refs = {}
for name, label in (('reference-week-v2.json', 'week'), ('reference-holdout-v2.json', 'holdout')):
    for art in json.loads((A / name).read_text())['articles']:
        refs[art['input_id']] = dict(art, set=label)
print('=== kept on articles whose reference keeps nothing')
for i, art in refs.items():
    if art.get('statements'): continue
    ev = recs[i]['sift']['evidence']
    if ev:
        print(f"\n## {i[:60]} | {art.get('title', '')[:90]}")
        for e in ev:
            print('  -', e['tier'], '|', (e.get('original_who') or e.get('speaker') or '')[:30], '|', e['one_line'][:170])
print('\n=== core/supporting lost')
for i, art in refs.items():
    ev = (recs[i]['answer'] or {}).get('evidence', []); kept = {e['id'] for e in recs[i]['sift']['evidence']}
    for item in art.get('statements', []):
        if item['weight'] not in ('core', 'supporting'): continue
        hits = [e for e in ev if sw.matches(e['quote'], item)]
        if not any(e['id'] in kept for e in hits):
            print('-', item['weight'], i[:50], '|', item['note'][:200], '| refused' if hits else '| omitted')
