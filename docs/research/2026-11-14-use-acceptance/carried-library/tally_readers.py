"""The two reader families' marks on the small comparison, joined to the sealed key ($0). It judges nothing.

  python3 tally_readers.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')


def lines_of(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip().startswith('{')]


def main(keys):
    key = json.loads((Path(keys) / 'reader-key.json').read_text())
    packet = json.loads((HERE / 'reader-packet.json').read_text())
    rows = {family: {row['ref']: row for row in lines_of(HERE / f'{family}-readers.jsonl')} for family in FAMILIES}
    expected = {'opened': [], 'filed': [], 'read': []}
    for article in packet:
        for label, read in article['reads'].items():
            expected['read'].append(f"{article['article']}:{label}")
            expected['opened'] += [f"{article['article']}:{t['ref']}" for t in read['opened']]
            expected['filed'] += [f"{article['article']}:{s['ref']}" for s in read['statements'] if any(f.startswith('library') for f in s['filed_under'])]
    for family in FAMILIES:
        missing = [ref for kind in expected.values() for ref in kind if ref not in rows[family]]
        print(f'{family}: {len(rows[family])} rows; refs not answered: {len(missing)} {missing[:6]}')
    condition = lambda ref: key[ref.split(':')[0] + ref.split(':')[1][0]]

    print('\nOPENED QUESTIONS, by condition (both families; split when they differ):')
    for field in ('in_library', 'worth'):
        tally = collections.defaultdict(collections.Counter)
        for ref in expected['opened']:
            marks = [rows[f].get(ref, {}).get(field) for f in FAMILIES]
            tally[condition(ref)['condition']][marks[0] if marks[0] == marks[1] else 'split:' + '/'.join(map(str, marks))] += 1
        for name in ('empty', 'carried'):
            print(f'  {field:<10} {name:<8} {dict(tally[name])}')
    print('\n  opened questions one by one:')
    for ref in expected['opened']:
        c = condition(ref)
        article = packet[int(ref.split(':')[0]) - 1]
        topic = next(t for t in article['reads'][ref.split(':')[1][0]]['opened'] if t['ref'] == ref.split(':')[1])
        marks = ' | '.join(f"{f}: {rows[f].get(ref, {}).get('in_library')}, worth {rows[f].get(ref, {}).get('worth')}" for f in FAMILIES)
        print(f"   art {c['sequence']:>3} {c['condition']:<7} {marks} || {topic['question'][:100]}")

    print('\nSTATEMENTS FILED UNDER A QUESTION OF THE LIBRARY SHOWN (carried reads):')
    tally = collections.Counter()
    for ref in expected['filed']:
        marks = [rows[f].get(ref, {}).get('home') for f in FAMILIES]
        tally[marks[0] if marks[0] == marks[1] else 'split:' + '/'.join(map(str, marks))] += 1
        if 'wrong' in marks:
            article = packet[int(ref.split(':')[0]) - 1]
            statement = next(s for s in article['reads'][ref.split(':')[1][0]]['statements'] if s['ref'] == ref.split(':')[1])
            reasons = ' | '.join(f"{f}: {rows[f].get(ref, {}).get('home')} ({rows[f].get(ref, {}).get('why')})" for f in FAMILIES)
            print(f"   art {condition(ref)['sequence']:>3} {statement['filed_under']} {statement['statement'][:90]} || {reasons}")
    print('  all:', dict(tally))

    print('\nMATTERS A READ NEITHER OPENED NOR HELD (per read):')
    for ref in expected['read']:
        c = condition(ref)
        lists = {f: rows[f].get(ref, {}).get('missing') or [] for f in FAMILIES}
        if any(lists.values()):
            print(f"   art {c['sequence']:>3} {c['condition']:<7} codex {lists['codex']} | claude {lists['claude']}")
    for name in ('empty', 'carried'):
        counts = [len(rows[f].get(ref, {}).get('missing') or []) for ref in expected['read'] if condition(ref)['condition'] == name for f in FAMILIES]
        print(f'  {name}: missing matters named, both families together: {sum(counts)}')


if __name__ == '__main__':
    main(sys.argv[1])
