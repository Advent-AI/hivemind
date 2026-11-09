"""Stage 1 evaluation (stage1-frozen.md): write the blind adjudication packet of every matched (gold item, passage) pair, then, given the
reader's verdicts, apply the four frozen conditions using only confirmed pairs. Errors and refusals count as draws that delivered and
wrote nothing.

Usage: stage1_evaluate.py packet <records.json> <packet.md> <key.json>
       stage1_evaluate.py score <records.json> <key.json> <verdicts.md>"""
import json, random, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage1_probe as probe  # noqa: E402

GOLD = {i['id']: i for i in json.loads(probe.PACKET.read_text())['items']}


def pairs(records):
    seen = {}
    for r in records:
        for item, passages in (r.get('matched') or {}).items():
            for passage in passages:
                seen.setdefault((item, passage), None)
    return list(seen)


def write_packet(records, packet_path, key_path):
    unique = pairs(records)
    random.Random(20261109).shuffle(unique)
    key, lines = {}, ['For each pair, say whether the passage states the fact described (same company, same figure or event). Answer one line',
                      'per pair: `<label> | yes|no | <short reason>`. End with the count judged.', '']
    for n, (item, passage) in enumerate(unique, 1):
        label = f'P{n}'
        key[label] = [item, passage]
        meaning = GOLD[item].get('meaning')
        lines += [f'## {label}', f'Fact: {json.dumps(meaning, ensure_ascii=False)}', f'Passage: {passage}', '']
    Path(packet_path).write_text('\n'.join(lines), encoding='utf-8')
    Path(key_path).write_text(json.dumps(key, ensure_ascii=False, indent=1))
    print(f'{len(unique)} pairs written')


def score(records, key_path, verdicts_path):
    key = json.loads(Path(key_path).read_text())
    confirmed = set()
    judged = 0
    for line in Path(verdicts_path).read_text().splitlines():
        m = re.match(r'^`?(P\d+)\s*\|\s*(yes|no)\b', line.strip(), re.I)
        if m:
            judged += 1
            if m.group(2).lower() == 'yes':
                confirmed.add(tuple(key[m.group(1)]))
    if judged != len(key):
        raise SystemExit(f'the reader judged {judged} of {len(key)} pairs: refused')
    cited = probe.gold_questions()
    cases = {c['case']: c for c in json.loads((HERE / 'stage1_cases.json').read_text())}
    seeded = [r for r in records if r['arm'] == 'seeded']

    def delivered(r, item, question):
        if 'kept' not in r:
            return False
        return any(question in [l['target_id'] for l in e['links'] if l['target_type'] == 'existing']
                   and any((item, p) in confirmed for p in (e.get('verified_source_passages') or e['source_passages']))
                   for e in r['kept'])

    def written(r, item):
        return 'kept' in r and any(any((item, p) in confirmed for p in (e.get('verified_source_passages') or e['source_passages']))
                                   for e in r['kept'])

    def D(case, question):
        items = [g for g in cases[case]['gold'] if question in cited.get(g, set())]
        return sum(1 for r in seeded if r['case'] == case and any(delivered(r, g, question) for g in items))

    table = {case: {q: D(case, q) for q in cases[case]['targets'] if q.startswith('v')} for case in cases}
    for case, row in table.items():
        print(f'{case:20} {row}')
    c1 = max(table['q10-margin'].get('v10', 0), table['q10-guidance'].get('v10', 0)) >= 2
    c2 = max(table['q12-cashflow'].get('v12', 0), table['q12-capex'].get('v12', 0)) >= 2
    c3 = {q: max((row.get(q, 0) for row in table.values()), default=0) >= 2 for q in ('v1', 'v3', 'v11', 'v22')}
    c4 = {g: sum(1 for r in seeded if r['case'] == c['case'] and written(r, g)) >= 2 for c in cases.values() for g in c['gold']}
    print('1 q10 delivered:', c1); print('2 q12 delivered:', c2); print('3 figure questions kept:', c3)
    print('4 nothing written lost:', all(c4.values()), [g for g, ok in c4.items() if not ok])
    print('STAGE 1 HOLDS' if c1 and c2 and all(c3.values()) and all(c4.values()) else 'STAGE 1 FAILS')


if __name__ == '__main__':
    records = json.loads(Path(sys.argv[2]).read_text())
    if sys.argv[1] == 'packet':
        write_packet(records, sys.argv[3], sys.argv[4])
    else:
        score(records, sys.argv[3], sys.argv[4])
