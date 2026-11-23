"""What Step 2 would do to each incoming record on the product path (no model calls): Jev over the item's search results (R1 top 10,
union of its associations), then the proposed precedence: any same_statement → merged away (its source added to the matched records);
else any supersedes → new record linked as a later version; else a new record. Compared with reference v2; pairs never labelled count as
different and are listed apart, since some may be repeats the reference missed.

Usage: score_product_path.py <folder> <jev answers.json> [...]"""
import collections, json, sys
from pathlib import Path


def main():
    folder = Path(sys.argv[1])
    items = {it['key']: it for it in json.loads((folder / 'items.json').read_text())}
    reference = {(r['earlier'], r['later']): r for r in json.loads((folder / 'reference-v2.json').read_text())}
    for name in sys.argv[2:]:
        by_item = collections.defaultdict(dict)
        for a in json.loads((folder / name).read_text()):
            by_item[a['later']][a['earlier']] = a['choice']
        outcome = collections.Counter()
        unlabelled_same = []
        for later, answers in by_item.items():
            truth = {e: reference[(e, later)]['relation'] for e in answers if (e, later) in reference}
            said_same = [e for e, c in answers.items() if c == 'same_statement']
            true_same = [e for e, rel in truth.items() if rel == 'same_statement']
            unlabelled_same += [(e, later) for e in said_same if e not in truth]
            if said_same:
                right = [e for e in said_same if truth.get(e) == 'same_statement']
                if not right:
                    outcome['merged away, no matched record is the same statement'] += 1
                else:
                    outcome['merged away into a true same statement'] += 1
                    if all(reference[(e, later)]['source_only_merge_loses'] for e in right):
                        outcome['  of which readers say every true match lacks something the incoming record holds'] += 1
                    if len(right) < len(said_same):
                        outcome['  of which the source is also added to a record that is not the same statement'] += 1
            elif true_same:
                outcome['kept as new although a same statement was among the results (duplicate)'] += 1
            elif any(c == 'supersedes' for c in answers.values()):
                outcome['kept as a later version of a result'] += 1
            else:
                outcome['kept as new'] += 1
        print(f'{name}: {len(by_item)} incoming records')
        for k, v in sorted(outcome.items(), key=lambda kv: (kv[0].startswith('  '), -kv[1])):
            print(f'  {v:4d}  {k}')
        print(f'  same_statement said on never-labelled pairs: {len(unlabelled_same)}')
        (folder / f'{Path(name).stem}-unlabelled-same.json').write_text(json.dumps(unlabelled_same))


if __name__ == '__main__':
    main()
