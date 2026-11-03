"""Build a blind adjudication packet for a reader who did not write the change: every core and supporting gold entry whose kept-draw
count differs between two versions of a full run, with each draw's kept statements on that article under labels A and B assigned at
random per entry (seed fixed); the label key is written apart.   python3 blind_packet.py Y2 v53 v61 dev"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402

prefix, control, arm, set_name = sys.argv[1:5]
rows = json.loads((LEDGER / 'final-2026-10-30' / f'per-article-{prefix}-{set_name}.json').read_text())
articles = {a['input_id']: a for a in json.loads(Path(fs.GOLDS[set_name]).read_text())['articles']}
rng = random.Random(int(sys.argv[5]) if len(sys.argv) > 5 else 20261031)
entries, key = [], {}
for iid, a in articles.items():
    for weight, k in (('core', 'core'), ('supporting', 'supp')):
        items = [i for i in a['items'] if i['weight'] == weight]
        for idx, item in enumerate(items):
            if sum(rows[control][iid][k][idx]) == sum(rows[arm][iid][k][idx]):
                continue
            labels = [control, arm]
            rng.shuffle(labels)
            eid = f'E{len(entries) + 1:02d}'
            key[eid] = {'A': labels[0], 'B': labels[1], 'input_id': iid, 'weight': weight, 'span': item['span'],
                        'counting_aid': {control: rows[control][iid][k][idx], arm: rows[arm][iid][k][idx]}}
            draws = {}
            for label, version in zip('AB', labels):
                for d in (1, 2, 3):
                    s = sg.kept(sg.answers(f'{prefix}-{version}-d{d}').get(iid), iid)
                    draws[f'{label}{d}'] = [e['quote'] for e in (s or {}).get('evidence', [])]
            m = item.get('meaning') or {}
            entries.append({'entry': eid, 'article': a['title'], 'gold_statement': item['span'],
                            'gold_meaning': {k2: m.get(k2) for k2 in ('who', 'what', 'how_much', 'period', 'status') if m.get(k2)}, 'draws': draws})
(HERE / f'blind-{prefix}-{control}-{arm}-{set_name}{"-" + sys.argv[5] if len(sys.argv) > 5 else ""}.json').write_text(json.dumps(entries, ensure_ascii=False, indent=1))
(HERE / f'blind-{prefix}-{control}-{arm}-{set_name}{"-" + sys.argv[5] if len(sys.argv) > 5 else ""}.key.json').write_text(json.dumps(key, ensure_ascii=False, indent=1))
print(len(entries), 'entries;', sum(v['weight'] == 'core' for v in key.values()), 'core')
