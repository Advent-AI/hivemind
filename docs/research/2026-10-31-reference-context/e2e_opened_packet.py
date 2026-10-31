"""Blind packet of the questions each run's articles opened (end to end): every view with created_seq > 0, with the article's gold lists
and the questions already open in that ledger before it (seeds included), labels apart. Reader prompt: blind-seq/opened.md's format.
    python3 e2e_opened_packet.py <out folder> <seed> control=run1,run2,run3 seeded=run4,run5,run6"""
import json
import random
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import score_ref as sr  # noqa: E402

out_dir, seed = Path(sys.argv[1]), int(sys.argv[2])
arms = {a.split('=', 1)[0]: [str(ROOT / p) if not p.startswith('/') else p for p in a.split('=', 1)[1].split(',')] for a in sys.argv[3:]}
arts = {a['input_id']: a for a in sr.articles}
entries, key = [], {}
for name, runs in arms.items():
    for d, run in enumerate(runs, 1):
        v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
        rows = [dict(r) for r in v.execute('select view_id, question, looks_at, created_seq, created_from_input from views order by created_seq, view_id')]
        for q in rows:
            if q['created_seq'] == 0:
                continue
            a = arts.get(q['created_from_input'], {'title': q['created_from_input'], 'publication_day': '', 'questions': {}})
            oid = f'Q{len(entries) + 1:03d}'
            key[oid] = {'arm': name, 'draw': d, 'view_id': q['view_id'], 'input_id': q['created_from_input']}
            entries.append({'id': oid, 'article': a['title'], 'day': a.get('publication_day', ''), 'question': q['question'], 'looks_at': q['looks_at'],
                            'gold_must_open': [g['gist'] for g in a.get('questions', {}).get('must_open', [])],
                            'gold_may_open': [g['gist'] for g in a.get('questions', {}).get('may_open', [])],
                            'gold_must_not': [g['gist'] for g in a.get('questions', {}).get('must_not', [])],
                            'earlier_questions_in_this_run': [f'{x["view_id"]}: {x["question"]}' for x in rows if x['created_seq'] < q['created_seq']]})
random.Random(seed).shuffle(entries)
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'opened.json').write_text(json.dumps(entries, ensure_ascii=False, indent=1))
(out_dir / 'opened.key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
print(len(entries), 'opened questions across', sum(len(r) for r in arms.values()), 'runs')
