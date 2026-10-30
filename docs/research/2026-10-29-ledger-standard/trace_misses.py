"""Reading sheet for the misses of a scored run (D244: read the traces every time). For each core or supporting gold
entry not kept in every draw: the gold entry, the article sentence around it, and for each draw the statements the
answer kept, plus anything the code dropped with its reason. No judgement is made here.

    python3 trace_misses.py SCORE_DIR GOLD.json TAG1 TAG2 TAG3 [--weights core supporting] [--max-hits 1]
"""
import json, sys
from pathlib import Path
import score_gold as sg

args = sys.argv[1:]
max_hits = 2
if '--max-hits' in args:
    i = args.index('--max-hits'); max_hits = int(args[i + 1]); del args[i:i + 2]
out_dir, gold_path, tags = Path(args[0]), args[1], args[2:]
gold = {a['input_id']: a for a in json.loads(Path(gold_path).read_text())['articles']}
misses = [m for m in json.loads((out_dir / 'misses.json').read_text()) if sum(m['hits']) <= max_hits]
runs = {t: sg.answers(t) for t in tags}
import sqlite3
db = sqlite3.connect('file:/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite?mode=ro', uri=True)
lines = []
for n, m in enumerate(sorted(misses, key=lambda m: (m['weight'] != 'core', sum(m['hits']))), 1):
    a = gold[m['input_id']]
    text = db.execute('select text from items where input_id=?', (m['input_id'],)).fetchone()[0]
    k = text.find(m['span'])
    lines += [f'## {n}. {m["weight"]} · kept in {sum(m["hits"])} of {len(tags)} · {a["title"][:90]}', f'gold: {m["span"]}',
              f'rule: {m["rule"][:200]}', f'context: …{text[max(0, k - 250):k + len(m["span"]) + 150]}…']
    for t in tags:
        s = sg.kept(runs[t].get(m['input_id']), m['input_id'])
        if not s:
            lines.append(f'- {t}: no usable answer'); continue
        lines.append(f'- {t}: kept {len(s["evidence"])} statements' + ('' if not s['dropped'] else f'; code dropped {s["dropped"]}'))
        for e in s['evidence']:
            lines.append(f'    · {e["quote"][:170]}')
    lines.append('')
(out_dir / 'trace-misses.md').write_text('\n'.join(lines) + '\n')
print(len(misses), 'misses written')
