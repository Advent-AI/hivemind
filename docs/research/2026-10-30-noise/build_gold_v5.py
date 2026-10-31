"""Write the gold for standard version 5 (D250) from the frozen version-3 development gold and version-4 test gold, which stay untouched
(D243 item 11). Every entry of gold-v5/key.json was read by two independent blind readers (A: Codex, verdicts-A*.jsonl; B: Claude,
verdicts-B*.jsonl) under the version-5 page. An entry changes only by a decision in gold-v5/adjudication.json, written after reading the
entry against its article; the candidates are listed by `python3 build_gold_v5.py candidates`:
  - an evidence entry (core, supporting, optional) that at least one reader drops under a D250 rule, or both readers drop;
  - a not-kept entry that both readers keep, or one reader keeps and the gold's reason cites D238 or another company;
  - a Singapore case entry marked not kept (5.3 makes the case optional).
`python3 build_gold_v5.py write` applies the decisions and writes golden-v5/golden-v5-dev.json, golden-v5/golden-v5-test.json (evidence part
standard_version 5; the opening part keeps the version it was made for, questions_standard_version), golden-v5/corrections-v5.json
(every change: before, after, both readers' verdicts, the reason) and golden-v5/golden-v5.sha256."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
SOURCES = {'dev': LEDGER / 'golden-v3/golden-v3-signed.json', 'test': LEDGER / 'test-set/golden-test-signed.json'}
OUT = LEDGER / 'golden-v5'
FOLDER = HERE / 'gold-v5'
KEPT = ('core', 'supporting', 'optional')


def verdicts(reader):
    out = {}
    for path in sorted(FOLDER.glob(f'verdicts-{reader}*.jsonl')):
        for line in path.read_text().splitlines():
            if line.strip().startswith('{'):
                o = json.loads(line)
                out[o['id']] = o
    return out


def candidates(key, a, b):
    rows = []
    for gid, k in key.items():
        va, vb = a.get(gid), b.get(gid)
        if va is None or vb is None:
            raise SystemExit(f'{gid} lacks a verdict from reader {"A" if va is None else "B"}')
        drops = [v for v in (va, vb) if v['weight'] == 'not_kept']
        keeps = [v for v in (va, vb) if v['weight'] in ('core', 'supporting')]
        if k['list'] == 'items':
            hit = any(v['d250'] in ('1', '2', '3', '4') for v in drops) or len(drops) == 2
        else:
            other_company = 'D238' in k['gold_reason'] or '别家公司' in k['gold_reason']
            hit = len(keeps) == 2 or (keeps and other_company) or ('新加坡' in k['gold_reason'] and k['gold_weight'] == 'not_kept')
        if hit:
            rows.append(gid)
    return rows


def main():
    key = json.loads((FOLDER / 'key.json').read_text())
    a, b = verdicts('A'), verdicts('B')
    listed = candidates(key, a, b)
    if sys.argv[1] == 'candidates':
        for gid in listed:
            k = key[gid]
            print(f"{gid} {k['set']} {k['list']} gold={k['gold_weight']} | A={a[gid]['weight']}/{a[gid]['d250']} B={b[gid]['weight']}/{b[gid]['d250']} | "
                  f"{k['input_id'][:34]} | {k['span'][:160]}\n    gold: {k['gold_reason'][:140]}\n    A: {a[gid]['reason'][:220]}\n    B: {b[gid]['reason'][:220]}")
        print(len(listed), 'candidates')
        return
    decisions = json.loads((FOLDER / 'adjudication.json').read_text())
    missing = [gid for gid in listed if gid not in decisions]
    if missing:
        raise SystemExit(f'no decision for {len(missing)} candidates: {missing[:10]}')
    OUT.mkdir(exist_ok=True)
    corrections, digests = [], {}
    for set_name, source in SOURCES.items():
        gold = json.loads(source.read_text())
        by_span = {}
        for art in gold['articles']:
            for entry in art['items']:
                by_span[(art['input_id'], 'items', entry['span'])] = (art, entry)
            for entry in art['not_kept']:
                by_span[(art['input_id'], 'not_kept', entry['span'])] = (art, entry)
        for gid, d in decisions.items():
            k = key[gid]
            if k['set'] != set_name or d['after'] == 'unchanged':
                continue
            art, entry = by_span[(k['input_id'], k['list'], k['span'])]
            before = {'list': k['list'], 'weight': entry['weight'], 'reason': entry.get('rule', entry.get('row', ''))}
            if k['list'] == 'items' and d['after'] == 'not_kept':
                art['items'].remove(entry)
                art['not_kept'].append({'span': entry['span'], 'row': d['row'], 'depends_on': [], 'weight': 'not_kept', 'was_item': entry})
            elif k['list'] == 'not_kept' and d['after'] in ('optional', 'not_kept'):
                entry['weight'] = d['after']
                entry['row'] = d['row']
            elif k['list'] == 'not_kept' and d['after'] in ('core', 'supporting'):
                art['not_kept'].remove(entry)
                art['items'].append({'span': entry['span'], 'weight': d['after'], 'rule': d['row'], 'kind': d.get('kind', ''), 'meaning': d.get('meaning', {}),
                                     'who': d.get('who', ''), 'tier': d.get('tier', ''), 'was_not_kept': entry})
            elif k['list'] == 'items' and d['after'] in KEPT:
                entry['weight'] = d['after']
                entry['rule'] = d['row']
            else:
                raise SystemExit(f'{gid}: cannot apply {d}')
            corrections.append({'id': gid, 'set': set_name, 'input_id': k['input_id'], 'span': k['span'], 'before': before,
                                'after': {'list': 'not_kept' if d['after'] in ('not_kept', 'optional') and k['list'] == 'not_kept' or d['after'] == 'not_kept' else 'items',
                                          'weight': d['after'], 'reason': d['row']},
                                'reader_a': a[gid], 'reader_b': b[gid], 'decision': d['reason']})
        gold['questions_standard_version'] = gold['standard_version']
        gold['standard_version'] = 5
        gold['about'] = (f"Evidence part re-derived for standard version 5 (D250) from {source.name} (sha256 {hashlib.sha256(source.read_bytes()).hexdigest()}), "
                         "which is untouched: every evidence entry and every not-kept entry citing D238, another company, a 5.1 judgement or the Singapore case, "
                         "plus the 35 entries a blind reader would keep (blind4/), read by two independent blind readers; changes only by a recorded decision "
                         "(corrections-v5.json). The opening part is the source's (questions_standard_version). Model-authored. Before: " + gold['about'])
        path = OUT / f'golden-v5-{set_name}.json'
        path.write_text(json.dumps(gold, ensure_ascii=False, indent=1) + '\n')
        digests[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    (OUT / 'corrections-v5.json').write_text(json.dumps(corrections, ensure_ascii=False, indent=1) + '\n')
    digests['corrections-v5.json'] = hashlib.sha256((OUT / 'corrections-v5.json').read_bytes()).hexdigest()
    (OUT / 'golden-v5.sha256').write_text(''.join(f'{h}  {n}\n' for n, h in digests.items()))
    print(len(corrections), 'changes;', digests)


if __name__ == '__main__':
    main()
