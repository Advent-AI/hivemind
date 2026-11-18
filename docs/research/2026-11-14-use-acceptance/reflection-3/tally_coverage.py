"""The tally of the coverage trace against the predictions registered beforehand ($0).

  python3 tally_coverage.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
FAULTED = ('clean-1', 'clean-3', 'clean-4', 'clean-7', 'clean-10', 'clean-12', 'clean-13')


def lines_of(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip().startswith('{')]


def main(keys):
    key = json.loads((Path(keys) / 'coverage-key.json').read_text())
    answers = {family: {row['id']: row for row in lines_of(HERE / f'{family}-coverage.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        assert len(answers[family]) == 20, (family, len(answers[family]))
    covered = {}
    for topic, source in sorted(key.items(), key=lambda pair: (pair[1][:10], int(pair[1].rsplit('-', 1)[-1]))):
        marks = [answers[family][topic] for family in FAMILIES]
        both_covered = all(mark['coverage'] != 'none' for mark in marks)
        neither = all(mark['coverage'] == 'none' for mark in marks)
        covered[source] = 'covered' if both_covered else 'none' if neither else 'split'
        print(f"{source:24} coverage {marks[0]['coverage']:14}/{marks[1]['coverage']:14} prior {','.join(marks[0]['prior']):18}/{','.join(marks[1]['prior']):18} "
              f"article {marks[0]['article']:10}/{marks[1]['article']:10} matter {marks[0]['matter_is']:8}/{marks[1]['matter_is']}")
    for week, size in (('week 09-22', 7), ('week 10-06', 13)):
        tally = collections.Counter(value for source, value in covered.items() if source.startswith(week))
        print(f'Q1 {week}: covered by both {tally["covered"]} of {size}; none by both {tally["none"]}; split {tally["split"]}')
    for field in ('article', 'matter_is', 'coverage'):
        both = collections.Counter()
        for topic in key:
            marks = [answers[family][topic][field] for family in FAMILIES]
            both[marks[0] if marks[0] == marks[1] else 'split'] += 1
        print(f'{field} (both families, 20 topics):', dict(both))
    faulted = {source: value for source, value in covered.items() if source.startswith('week 10-06') and source.rsplit('/', 1)[-1] in FAULTED}
    print('Q3 the seven faulted or refused topics of the week of 10-06:', faulted, '| covered by both:', sum(1 for value in faulted.values() if value == 'covered'))
    new_and_uncovered = [source for topic, source in key.items() if all(answers[family][topic]['matter_is'] == 'new' for family in FAMILIES)]
    print('matters both families call new:', sorted(new_and_uncovered))


if __name__ == '__main__':
    main(sys.argv[1])
