"""Builds gate 2's blind reader packets from the run's records (GATE2.md, "Structural rule" and "Memory marks"): a claims packet, one
entry per send of both arms on the claim controls, and a memory-theses packet, one entry per memory thesis. Labels are hidden and the
order shuffled with a fixed seed; the key (entry -> case, arm, send) is written outside the repository. It decides nothing.

  python3 clean-arch/step1-diagnosis-2026-11-12/gate2/build_reader_packets.py <records.jsonl> <key folder> [prefix] [--retention]

`prefix` names the packet and key files (default: none, gate 2's names); `--retention` gives the memory claims the diagnostic's rule
(D440): a claim is retained when a kept item states it, an empty link allowed.
"""
import json, random, re, sqlite3, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
records = [json.loads(line) for line in open(sys.argv[1])]
key_folder = Path(sys.argv[2])
options = [a for a in sys.argv[3:] if a != '--retention']
prefix = (options[0] + '-') if options else ''
retention = '--retention' in sys.argv[3:]
required = json.loads((HERE / 'required-statements.json').read_text())
cases = {c['case']: c for c in json.loads((HERE.parent / 'cases-c14.json').read_text())}
CLAIM_KINDS = ('capex-repeat-a', 'capex-repeat-b', 'population', 'kyber', 'memory')
LINK_RULE = {
    'capex-repeat-a': "Each claim must be linked to the capex thesis of its year when that year's thesis is open or newly opened in this answer; otherwise to the open capex thesis.",
    'population': "The claim must be linked to the open capex thesis.",
    'kyber': "Each claim must be linked to the one thesis that holds the Kyber timing (open or new).",
    'memory': "Each claim must be linked to at least one thesis.",
}
LINK_RULE['capex-repeat-b'] = LINK_RULE['capex-repeat-a']
if retention:
    LINK_RULE['memory'] = "No link is required: an empty link counts as linked as required (a statement no open thesis covers is kept without links by design)."


def open_theses(case):
    conn = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
    request = json.loads(conn.execute("select request from trace where sequence = ? and status = 'complete'", (case['sequence'],)).fetchone()[0])
    payload, _ = json.JSONDecoder().raw_decode(request['messages'][1]['content'])
    return [{'id': t['id'], 'question': t.get('description'), 'outcome': t.get('outcome')} for t in payload['open_theses']]

claim_entries, memory_entries = [], []
for record in records:
    kind = record['case'].split('-', 1)[1]
    usable = 'new_theses' in record
    if kind in CLAIM_KINDS:
        claim_entries.append({'case': record['case'], 'arm': record['arm'], 'send': record['send'], 'entry': {
            'claims': required['claims'][record['case']],
            'stored_reference_items': required['stored_items'][record['case']],
            'link_rule': LINK_RULE[kind],
            'open_theses': open_theses(cases[record['case']]),
            'answer_usable': usable,
            'new_theses': [{'id': t['local_id'], 'question': t['description'], 'outcome': t['outcome'], 'period': t.get('period')} for t in record.get('new_theses') or []],
            'kept_evidence': [{'id': e['local_id'], 'summary': e['summary'], 'source_passages': e['source_passages'],
                               'links': [l['target_id'] for l in e['links']]} for e in record.get('links') or []]}})
    if kind == 'memory':
        for t in record.get('new_theses') or []:
            text = ' '.join(str(t.get(k) or '') for k in ('description', 'outcome', 'period'))
            if re.search(r'memory|DRAM|NAND|HBM|LPDDR|DDR5', text, re.I):
                memory_entries.append({'case': record['case'], 'arm': record['arm'], 'send': record['send'], 'thesis_id': t['local_id'],
                                       'entry': {'question': t['description'], 'outcome': t['outcome'], 'period': t.get('period')}})
for name, entries, seed in (('claims', claim_entries, 20261113), ('memory', memory_entries, 20261114)):
    random.Random(seed).shuffle(entries)
    packet = [dict(n=n, **e['entry']) for n, e in enumerate(entries, start=1)]
    key = {str(n): {k: e[k] for k in e if k != 'entry'} for n, e in enumerate(entries, start=1)}
    (HERE / f'{prefix}packet-{name}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
    (key_folder / f'gate2-{prefix}key-{name}.json').write_text(json.dumps(key, indent=1) + '\n')
    print(f'{name}: {len(packet)} entries')
