"""Tally a question reader's answers (no model calls): opened theses by verdict, and must_open entries covered.

Usage: tally_questions.py <packet.json> <answer.json>"""
import collections, json, sys

packet = {c['id']: c for c in json.load(open(sys.argv[1]))}
text = open(sys.argv[2]).read()
answers = {a['id']: a for a in json.loads(text[text.index('['):text.rindex(']') + 1])}
verdicts = collections.Counter()
covered = total = 0
missing = []
if set(answers) != set(packet):
    raise SystemExit(f'answer ids differ from the packet: missing {sorted(set(packet) - set(answers))}, extra {sorted(set(answers) - set(packet))}')
for cid, case in packet.items():
    a = answers[cid]
    if len(a.get('opened', [])) != len(case['opened']) or len(a.get('must_open', [])) != len(case['must_open']):
        raise SystemExit(f'{cid}: answer counts differ from the packet')
    for v in a.get('opened', []):
        verdicts[v['verdict']] += 1
    for entry, m in zip(case['must_open'], a.get('must_open', [])):
        total += 1
        covered += bool(m.get('covered'))
        if not m.get('covered'):
            missing.append(entry[:100])
print(f"opened theses {sum(verdicts.values())}: {dict(verdicts)} | must_open covered {covered}/{total}")
for m in missing:
    print('   not covered:', m)
