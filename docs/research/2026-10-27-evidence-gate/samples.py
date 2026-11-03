"""Extraction is a sampler: the same stored request re-sent gives a different piece count each time (0 to 8 pieces for one
CoreWeave article within an hour). So the gate is judged on several samples per arm: S fresh sends of the unchanged request
(control) and S sends with role-v15 (arm), per stored article; a control piece the judge later cited counts as kept when a
sample contains it. Run: python3 samples.py <run folder> <items.sqlite> <scratch archive> <S> <input_id...>"""
import json
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pinned_arm import ROLE_V15, REVENUE, same_piece, send  # noqa: E402
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402


def main(run, items_path, scratch, samples, input_ids):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    stored = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    items = sqlite3.connect(f'file:{items_path}?mode=ro', uri=True)
    archive = model.Archive(scratch)
    cited = set()
    for j in views.execute('select cited_evidence_json from judgements'):
        cited |= set(json.loads(j[0] or '[]'))
    total = 0.0
    agg = {'control': [0, 0, 0, 0], 'arm': [0, 0, 0, 0]}        # pieces, cited kept, never kept, on v6/v11
    n_cited = n_never = 0
    always_lost = []
    for input_id in input_ids:
        text = items.execute('select text from items where input_id=?', (input_id,)).fetchone()[0]
        probe = text[:160].replace('\n', ' ')[:80]
        found = [r for r in stored.execute("select request_json, answer_json from model_calls where purpose='extract' and request_json like ? order by call_id", (f'%{input_id}%',))
                 if probe in json.loads(r[0])['messages'][1]['content'].replace('\n', ' ')]
        request, control = json.loads(found[0][0]), json.loads(found[0][1])
        ledger = [dict(r) for r in views.execute('select evidence_id, quote from evidence where created_from_input=?', (input_id,))]
        pieces = [dict(p, stored=next((e['evidence_id'] for e in ledger if same_piece(e, p)), None)) for p in control.get('evidence', [])]
        for p in pieces:
            p['cited'] = p['stored'] in cited
        n_cited += sum(p['cited'] for p in pieces)
        n_never += sum(not p['cited'] for p in pieces)
        seen = {'control': [], 'arm': []}
        for name, system in (('control', None), ('arm', ROLE_V15)):
            for _ in range(samples):
                data, cost = send(archive, request, system, name if name == 'arm' else 'fresh-control')
                total += cost
                out = data.get('evidence', [])
                seen[name].append(out)
                agg[name][0] += len(out)
                agg[name][1] += sum(1 for p in pieces if p['cited'] and any(same_piece(p, a) for a in out))
                agg[name][2] += sum(1 for p in pieces if not p['cited'] and any(same_piece(p, a) for a in out))
                agg[name][3] += sum(1 for a in out if any(v in REVENUE for v in a.get('links', [])))
        for p in pieces:
            if p['cited'] and not any(any(same_piece(p, a) for a in out) for out in seen['arm']) and any(any(same_piece(p, a) for a in out) for out in seen['control']):
                always_lost.append((input_id, p['one_line'][:120]))
        print(f'{input_id}: control pieces per sample {[len(o) for o in seen["control"]]}, arm {[len(o) for o in seen["arm"]]}')
    s = samples * len(input_ids)
    print(f'\nstored control pieces: cited {n_cited}, never cited {n_never}; {samples} samples per arm per article')
    print('| arm | pieces per article (mean) | cited pieces kept (mean per sample) | never-cited kept (mean per sample) | pieces on v6/v11 per article |')
    print('|---|---|---|---|---|')
    for name in ('control', 'arm'):
        a = agg[name]
        print(f'| {name} | {a[0] / s:.1f} | {a[1] / samples:.1f} of {n_cited} | {a[2] / samples:.1f} of {n_never} | {a[3] / s:.1f} |')
    print('\ncited pieces the control keeps in some sample but the arm in none:')
    for x in always_lost:
        print('  -', x[0], '|', x[1])
    print(f'\ntotal USD {total:.4f}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5:])
