"""Partition each draw's kept not-kept gold entries (final_scores.py's count) into three parts, in this order: carried (every statement
matching the span also matches a kept gold entry, as in carried_rejected.py), disputed (the blind reader of blind4/ gave the entry a
weight other than not_kept), and noise (both the gold and the blind reader say not kept). Prints per draw and, for the noise part, the
gold row class with draws.   python3 partition_rejected.py Y3 v63 [v53]"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30'), str(HERE)]
import final_scores as fs  # noqa: E402
import score_gold as sg  # noqa: E402
from kept_rejected import row_class  # noqa: E402

key = json.loads((HERE / 'blind4' / 'key.json').read_text())
verdicts = {}
for p in (1, 2, 3):
    for line in (HERE / 'blind4' / f'verdicts-{p}.jsonl').read_text().splitlines():
        if line.strip().startswith('{'):
            o = json.loads(line)
            verdicts[o['id']] = o
reader = {(k['input_id'], k['span']): verdicts[s]['weight'] for s, k in key.items()}
prefix, versions = sys.argv[1], sys.argv[2:]
articles = json.loads(Path(fs.GOLDS['dev']).read_text())['articles']
for version in versions:
    parts, noise_rows = [], collections.Counter()
    for d in (1, 2, 3):
        run = sg.answers(f'{prefix}-{version}-d{d}')
        count = collections.Counter()
        for a in articles:
            s = sg.kept(run.get(a['input_id']), a['input_id'])
            if not s:
                continue
            kept_gold = [i for i in a['items'] if i['weight'] in ('core', 'supporting', 'optional')]
            for n in a['not_kept']:
                if n['weight'] != 'not_kept':
                    continue
                matching = [e for e in s['evidence'] if sg.same(n['span'], e['quote'])]
                if not matching:
                    continue
                if all(any(sg.same_matter(k, e) for k in kept_gold) for e in matching):
                    count['carried'] += 1
                elif reader.get((a['input_id'], n['span']), 'unread') not in ('not_kept', 'unread'):
                    count['disputed'] += 1
                elif (a['input_id'], n['span']) not in reader:
                    count['unread'] += 1
                else:
                    count['noise'] += 1
                    noise_rows[row_class(n.get('row', ''))] += 1
        parts.append(dict(count))
    print(version, parts, {k: round(sum(p.get(k, 0) for p in parts) / 3, 1) for k in ('carried', 'disputed', 'noise', 'unread')})
    for row, n in noise_rows.most_common():
        print(f'   {n:>3}  {row[:90]}')
