"""D604's $0 trace of line 5 on the fresh topics (control arm): for every send, the kind, each applicable mark as the two first
readers gave it, the two third-reader families' rulings where they differ, and the marks failed under each counting of unresolved
points; then, per topic, which marks keep it from being right under each counting. Reads only the stored reading; judges nothing.

  python3 line5_trace.py <cases.json> <population.json> <reading folder> <key path> <plants-expected path>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1])]
import fresh_probe  # noqa: E402
import probe_score as ps  # noqa: E402


def main(cases_path, population_path, reading, key_path, plants_path):
    fresh_probe.configure(cases_path, population_path)
    loaded = ps.load_reading(reading, key_path, plants_path)
    outcomes, readers, item_of, of_family, families, h_given, _ = loaded
    topic_of = lambda send: send[0].split('|', 1)[1].split(':', 1)[1]
    by_topic = collections.defaultdict(list)
    for send, outcome in sorted(outcomes.items()):
        if not send[0].startswith('control|'):
            continue
        kind = ps.accounting.kind_of(outcome)
        rows = (readers['reader 1'].get(send), readers['reader 2'].get(send))
        failed = {counting: ps.failed_marks(send, outcome, rows, of_family, families, h_given, item_of.get(send), counting)
                  for counting in ('holds', 'fails')}
        split = {}
        for mark in ps.accounting.marks_that_apply(kind):
            first, second = rows[0][mark], rows[1][mark]
            if first != second:
                rulings = [of_family[family].get(send, {}).get('marks', {}).get(mark) for family in families]
                split[mark] = {'first readers': (first, second), 'third readers': dict(zip(families, rulings))}
        settled_fail = sorted(m for m in ps.accounting.marks_that_apply(kind) if rows[0][m] == rows[1][m] == 'fails')
        by_topic[topic_of(send)].append({'pass': send[1], 'kind': kind, 'both first readers fail': settled_fail, 'split': split,
                                         'failed, unresolved for': sorted(failed['holds']), 'failed, unresolved against': sorted(failed['fails'])})
    for topic, sends in by_topic.items():
        print(f'== {topic}')
        for row in sends:
            print(json.dumps(row, ensure_ascii=False))
        for counting, label in (('failed, unresolved for', 'for'), ('failed, unresolved against', 'against')):
            blocking = sorted({m for row in sends for m in row[counting] if m not in ('refusal',)} - {'refusal'})
            justified = all(row['kind'] == 'refusal' and 'N' not in row[counting] for row in sends)
            right = justified or not any(set(row[counting]) - {'refusal'} for row in sends)
            print(f'   counting {label}: right = {right}; blocking marks = {blocking}')


if __name__ == '__main__':
    main(*sys.argv[1:])
