"""The tally of the two article marks on July's 40 topics against the prediction registered beforehand ($0).

  python3 tally_july_articles.py <key folder outside the repository>
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
    key = json.loads((Path(keys) / 'july-topics-key.json').read_text())
    answers = {family: {row['id'].replace('j', 't'): row for row in lines_of(HERE / f'{family}-july-articles.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        assert set(answers[family]) == set(key), (family, len(answers[family]))
    both = {}
    for field in ('article', 'matter_is'):
        tally = collections.Counter()
        for topic in key:
            marks = [answers[family][topic][field] for family in FAMILIES]
            both[(topic, field)] = marks[0] if marks[0] == marks[1] else 'split'
            tally[both[(topic, field)]] += 1
        print(f'{field} (both families, 40 topics):', dict(tally))
    packet = {item['id']: item for item in json.loads((HERE / 'july-topics-packet.json').read_text())}
    declined = {topic: sum(1 for attempt in packet[topic]['attempts'] if 'declined' in attempt) >= 2 for topic in packet}
    print('declined twice, by the article mark:', dict(collections.Counter((both[(t, 'article')], declined[t]) for t in key)))
    matters = [row for row in lines_of(HERE / 'claude-same-question.jsonl') if 'matter' in row]
    codex = {frozenset(row['topics']): row for row in lines_of(HERE / 'codex-same-question.jsonl') if 'matter' in row}
    print('exploratory: shared matters, the two families\' verdicts, and their topics\' article marks')
    for row in matters:
        if len(set(row['runs'])) < 2:
            continue
        other = codex[frozenset(row['topics'])]['verdict']
        marks = collections.Counter(both[(topic, 'article')] for topic in row['topics'])
        kinds = collections.Counter(both[(topic, 'matter_is')] for topic in row['topics'])
        print(f"   {row['matter'][:52]:52} {other:10}/{row['verdict']:10} article {dict(marks)} matter {dict(kinds)}")
    print('one-run-only matters:')
    for row in matters:
        if len(set(row['runs'])) < 2:
            topic = row['topics'][0]
            print(f"   {row['matter'][:52]:52} article {both[(topic, 'article')]:10} matter {both[(topic, 'matter_is')]}")


if __name__ == '__main__':
    main(sys.argv[1])
