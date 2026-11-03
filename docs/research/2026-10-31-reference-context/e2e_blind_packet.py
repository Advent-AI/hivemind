"""Blind packet for an end-to-end comparison (two arms, up to three ledgers each): every core or supporting gold entry whose number of
draws reaching judgement (stored, not replaced) differs between the arms by the counting aid, with each draw's statements stored from that
article under labels A and B assigned at random per entry; the key is written apart. The reader's format is blind3/prompt.md's.

    python3 e2e_blind_packet.py <out folder> <seed> control=run1,run2,run3 seeded=run4,run5,run6
"""
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
arms = {}
for arg in sys.argv[3:]:
    name, paths = arg.split('=', 1)
    arms[name] = [str(ROOT / p) if not p.startswith('/') else p for p in paths.split(',')]
names = list(arms)
rng = random.Random(seed)


def stored(run, iid):
    v = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); v.row_factory = sqlite3.Row
    replaced = {r[0] for r in v.execute('select old_evidence_id from replacements')}
    return [dict(r) for r in v.execute('select evidence_id, quote, one_line from evidence where created_from_input=?', (iid,)) if r['evidence_id'] not in replaced]


entries, key = [], {}
for a in sr.articles:
    iid = a['input_id']
    per_arm = {n: [stored(run, iid) for run in runs] for n, runs in arms.items()}
    for it in a['items']:
        if it['weight'] not in ('core', 'supporting'):
            continue
        hits = {n: [any(sr.sg.same_matter(it, s) for s in draw) for draw in draws] for n, draws in per_arm.items()}
        if sum(hits[names[0]]) == sum(hits[names[1]]):
            continue
        labels = names[:]; rng.shuffle(labels)
        eid = f'E{len(entries) + 1:03d}'
        key[eid] = {'A': labels[0], 'B': labels[1], 'input_id': iid, 'weight': it['weight'], 'span': it['span'], 'counting_aid': hits}
        m = it.get('meaning') or {}
        entries.append({'entry': eid, 'article': a['title'], 'gold_statement': it['span'],
                        'gold_meaning': {k: m.get(k) for k in ('who', 'what', 'how_much', 'period', 'status') if m.get(k)},
                        'draws': {f'{lab}{d + 1}': [s['quote'] for s in per_arm[arm][d]] for lab, arm in zip('AB', labels) for d in range(len(per_arm[arm]))}})
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / 'packet.json').write_text(json.dumps(entries, ensure_ascii=False, indent=1))
(out_dir / 'key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
print(len(entries), 'entries;', sum(v['weight'] == 'core' for v in key.values()), 'core')
