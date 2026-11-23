"""The tally of the blind review of the stored runs' questions against the predictions registered beforehand ($0).

  python3 tally_review.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind')
DATA = ROOT / 'poc/data'
FAMILIES = ('codex', 'claude')


def lines_of(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line.startswith('{'):
            rows.append(json.loads(line))
    return rows


def kinds_of(name):
    """{topic id: 'stated' | 'chosen' | 'split'} from the two families' task K answers, with each family's own answer."""
    by_family = {family: {row['id']: row for row in lines_of(HERE / f'{family}-{name}.jsonl')} for family in FAMILIES}
    out = {}
    for topic in by_family['codex']:
        marks = [by_family[family][topic]['yardstick'] for family in FAMILIES]
        out[topic] = marks[0] if marks[0] == marks[1] else 'split'
    return out, by_family


def declined_twice(attempts):
    return sum(1 for attempt in attempts if 'declined' in attempt) >= 2


def main(keys):
    keys = Path(keys)
    key = json.loads((keys / 'july-topics-key.json').read_text())
    packet = {item['id']: item for item in json.loads((HERE / 'july-topics-packet.json').read_text())}
    kind, kind_rows = kinds_of('stated-or-chosen')
    print('JULY, 40 topics. Yardstick by both families:', dict(collections.Counter(kind.values())),
          '| families agree on', sum(1 for value in kind.values() if value != 'split'), 'of', len(kind))
    declined = {topic: declined_twice(item['attempts']) for topic, item in packet.items()}
    table = collections.Counter((kind[topic], declined[topic]) for topic in packet)
    print('P2. declined in at least two of three attempts, by yardstick:')
    for name in ('stated', 'chosen', 'split'):
        total = table[(name, True)] + table[(name, False)]
        print(f'     {name}: {table[(name, True)]} of {total} declined twice')
    declined_topics = [topic for topic in packet if declined[topic]]
    print('     the declined topics:', [(key[topic], kind[topic]) for topic in declined_topics])
    print('P1. shared matters, by each family\'s own grouping in task S:')
    for family in FAMILIES:
        rows = [row for row in lines_of(HERE / f'{family}-same-question.jsonl') if 'matter' in row]
        shared = [row for row in rows if len(set(row['runs'])) >= 2]
        tally = collections.Counter()
        listing = []
        for row in shared:
            marks = [kind.get(topic, 'split') for topic in row['topics']]
            matter_kind = 'chosen' if 'chosen' in marks else 'stated' if all(mark == 'stated' for mark in marks) else 'split'
            tally[(matter_kind, row['verdict'])] += 1
            listing.append((row['matter'][:44], matter_kind, row['verdict'], ','.join(row.get('differs', []))[:60]))
        print(f'   {family}: {len(rows)} matters, {len(shared)} shared by two or three runs; one-run-only {sum(1 for row in rows if len(set(row["runs"])) < 2)}')
        for name in ('stated', 'chosen', 'split'):
            total = sum(count for (matter_kind, _), count in tally.items() if matter_kind == name)
            same = tally[(name, 'same')]
            print(f'        {name}: same {same} of {total}' + (f' ({100 * same // total}%)' if total else ''), {verdict: count for (matter_kind, verdict), count in tally.items() if matter_kind == name})
        for entry in listing:
            print('           ', entry)
    topic_rows = {family: {row['id']: row for row in lines_of(HERE / f'{family}-same-question.jsonl') if 'id' in row} for family in FAMILIES}
    for field in ('answerable', 'worth_tracking'):
        both = collections.Counter()
        for topic in packet:
            marks = [topic_rows[family].get(topic, {}).get(field, 'missing') for family in FAMILIES]
            both[marks[0] if marks[0] == marks[1] else 'split'] += 1
        print(f'{field} (both families):', dict(both))
    unworthy = [key[topic] for topic in packet if all(topic_rows[family].get(topic, {}).get('worth_tracking') == 'no' for family in FAMILIES)]
    print('topics both families call not worth tracking:', unworthy, '| of them declined twice:', [key[t] for t in packet if declined[t] and key[t] in unworthy])
    later = HERE / 'codex-stated-or-chosen-later-weeks.jsonl'
    if later.exists() and (HERE / 'claude-stated-or-chosen-later-weeks.jsonl').exists():
        later_key = json.loads((keys / 'later-weeks-key.json').read_text())
        later_kind, _ = kinds_of('stated-or-chosen-later-weeks')
        attempts = {}
        for name, folder in (('week 09-22', DATA / 'clean-lean-week-2026-11-14/week-r2/c1'), ('week 10-06', DATA / 'clean-second-week-2026-11-15/week-continued/c1')):
            for send in sorted((folder / 'ladder').glob('send-*')):
                for line in (send / 'outcomes.jsonl').read_text().splitlines():
                    row = json.loads(line)
                    attempts.setdefault(f"{name} {row['case']}", []).append(row['status'] != 'ladder')
        print('\nP3, HELD OUT: the two later weeks, 20 topics. Yardstick by both families:', dict(collections.Counter(later_kind.values())))
        table = collections.Counter((later_kind[topic], sum(attempts[later_key[topic]]) >= 2) for topic in later_kind)
        for name in ('stated', 'chosen', 'split'):
            total = table[(name, True)] + table[(name, False)]
            print(f'     {name}: {table[(name, True)]} of {total} declined twice')
        print('     the declined topics:', [(later_key[topic], later_kind[topic]) for topic in later_kind if sum(attempts[later_key[topic]]) >= 2])
        print('     declined at least once:', [(later_key[topic], later_kind[topic], sum(attempts[later_key[topic]])) for topic in later_kind if sum(attempts[later_key[topic]]) >= 1])


if __name__ == '__main__':
    main(sys.argv[1])
