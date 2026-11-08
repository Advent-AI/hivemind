"""Tally the blind readers' verdicts on a probe by arm (no model calls): new theses bet / small / duplicate, unfiled items fine /
existing / should_open, wrong links, per reader and where both readers agree.

Usage: tally_readers.py <probe folder> <key.json>"""
import collections, glob, json, sys
from pathlib import Path


def main():
    folder, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    readers = {}
    for path in sorted(glob.glob(str(folder / 'reader-answer-*-*.json'))):
        reader = Path(path).stem.split('-')[2]
        for entry in json.loads(Path(path).read_text()):
            for label, verdict in entry['answers'].items():
                readers.setdefault(reader, {})[f"{entry['case']}/{label}"] = verdict
    arms = [a for a in ['k6b', 'u1', 'u3', 'u1u3', 'u1k', 'u1ku3', 'u1c'] if any(v['arm'] == a for v in key.values())]
    for reader, verdicts in readers.items():
        table = collections.defaultdict(collections.Counter)
        for label, v in verdicts.items():
            arm = key[label]['arm']
            for t in v.get('new_theses', []):
                table[arm][f"thesis {t['verdict']}"] += 1
            for u in v.get('unfiled', []):
                table[arm][f"unfiled {u['verdict']}"] += 1
            table[arm]['wrong links'] += v.get('wrong_links', 0)
            table[arm]['answers'] += 1
        cols = ['answers', 'thesis bet', 'thesis small', 'thesis duplicate', 'unfiled fine', 'unfiled existing', 'unfiled should_open', 'wrong links']
        print(f'reader {reader}: ' + ' | '.join(cols))
        for arm in arms:
            print(f'  {arm:5s} ' + '  '.join(f'{table[arm][c]:>4d}' for c in cols))
    by_case = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for reader, verdicts in readers.items():
        for label, v in verdicts.items():
            case = label.split('/')[0]
            arm = key[label]['arm']
            by_case[case][arm]['dup+small'] += sum(t['verdict'] != 'bet' for t in v.get('new_theses', []))
            by_case[case][arm]['should file'] += sum(u['verdict'] != 'fine' for u in v.get('unfiled', []))
    print('\nper case, both readers summed: (theses small or duplicate) / (unfiled items that should have been filed or opened)')
    for case, row in by_case.items():
        print(f'  {case:10s} ' + '  '.join(f"{arm}:{row[arm]['dup+small']}/{row[arm]['should file']}" for arm in arms))


if __name__ == '__main__':
    main()
