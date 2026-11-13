"""Tally the blind readers' census answers ($0): per field, how many of the 34 cases each reader put in each class, on how many the
two readers agree, and the cases they disagree on (for the third reader). With `--final <adjudicated file>` it prints the final counts.

Usage: python3 tally.py reader-codex.jsonl reader-claude.jsonl [--final adjudicated.jsonl]"""
import collections, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ('things', 'ladder_type', 'due_day_basis', 'kind', 'favourable_end', 'one_ladder_keeps_the_question')


def load(name):
    rows = [json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')]
    cases = sorted(r['case'] for r in rows)
    if cases != list(range(1, 35)):
        raise SystemExit(f'{name}: cases {cases}, not 1..34: the tally would judge an incomplete reading')
    return {r['case']: r for r in rows}


def derived(row):
    return dict({f: str(row[f]) for f in FIELDS}, reference='stated' if row['reference'] else 'none')


def counts(rows, title):
    print(f'\n{title} (34 cases)')
    for field in FIELDS + ('reference',):
        print(f'  {field}: ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(derived(r)[field] for r in rows.values()).items())))
    numbers = [r for r in rows.values() if r['ladder_type'] == 'number']
    print(f'  number questions {len(numbers)}: with no reference in the article {sum(1 for r in numbers if not r["reference"])}; '
          f'asset with favourable end unclear {sum(1 for r in numbers if r["kind"] == "asset" and r["favourable_end"] == "unclear")} of '
          f'{sum(1 for r in numbers if r["kind"] == "asset")}')


def main():
    args = sys.argv[1:]
    final = args[args.index('--final') + 1] if '--final' in args else None
    names = [a for a in args if a != '--final' and a != final]
    packet = json.loads((HERE / 'packet.json').read_text())
    readers = {name: load(name) for name in names}
    for name, rows in readers.items():
        counts(rows, name)
    if len(readers) == 2:
        a, b = readers.values()
        print('\nagreement between the two readers, by field:')
        disputed = collections.defaultdict(list)
        for field in FIELDS + ('reference',):
            same = [c for c in range(1, 35) if derived(a[c])[field] == derived(b[c])[field]]
            print(f'  {field}: {len(same)} of 34')
            for c in range(1, 35):
                if c not in same:
                    disputed[c].append(f'{field}: {derived(a[c])[field]} / {derived(b[c])[field]}')
        print(f'\ncases with any disagreement: {len(disputed)} of 34')
        for c, fields in sorted(disputed.items()):
            print(f'  case {c} ({packet[c - 1]["run"]} {packet[c - 1]["id"]}): ' + '; '.join(fields))
    if final:
        counts(load(final), f'FINAL after adjudication: {final}')


if __name__ == '__main__':
    main()
