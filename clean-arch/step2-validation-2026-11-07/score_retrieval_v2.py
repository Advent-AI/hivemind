"""Retrieval recall at 10 on reference v2 (no model calls).

Targets: a later item's earlier counterparts labelled same_statement (a merge target) or revision (a link target); different facts of
the same matter are reported apart as context. Units:
  per association  each {thesis, evidence} query of the later item must hold the counterpart in its own top 10 (the product runs one
                   search per association);
  any association  the counterpart is in at least one of the item's searches.
Deduplicated history: every item labelled same_statement to an earlier item is merged into its earliest such counterpart (following the
chain), so it is no longer a separate candidate; a later item is then found when the surviving record of any counterpart is in the top 10
over surviving records only. Pairs never labelled count as different (the generator-miss estimate bounds this).

Usage: score_retrieval_v2.py <folder>"""
import collections, json, math, sys
from pathlib import Path

ARMS = ('R0', 'R0e', 'R1', 'R2')


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)) or 1)


def main():
    folder = Path(sys.argv[1])
    items = json.loads((folder / 'items.json').read_text())
    by_key = {it['key']: it for it in items}
    reference = json.loads((folder / 'reference-v2.json').read_text())
    retrieval = json.loads((folder / 'retrieval.json').read_text())
    associations = collections.defaultdict(list)
    for row in retrieval:
        associations[row['key']].append(row)
    for relations, name in ((('same_statement', 'revision'), 'same statement or revision'), (('same_statement',), 'same statement'),
                            (('revision',), 'revision'), (('different_fact_same_matter',), 'different fact, same matter')):
        pairs = [(r['earlier'], r['later']) for r in reference if r['relation'] in relations]
        print(f'{name}: {len(pairs)} pairs over {len({l for _, l in pairs})} later items')
        for arm in ARMS:
            per_assoc = [(e in set(a[arm])) for e, l in pairs for a in associations[l]]
            anywhere = [any(e in a[arm] for a in associations[l]) for e, l in pairs]
            items_found = {l for e, l in pairs if any(e in a[arm] for a in associations[l])}
            print(f'  {arm:4s} per association {sum(per_assoc)}/{len(per_assoc)} = {sum(per_assoc) / max(1, len(per_assoc)):.1%}; '
                  f'any association {sum(anywhere)}/{len(anywhere)}; later items with a counterpart found {len(items_found)}/{len({l for _, l in pairs})}')
    same = collections.defaultdict(set)
    for r in reference:
        if r['relation'] == 'same_statement':
            same[r['later']].add(r['earlier'])
    order = {it['key']: n for n, it in enumerate(items)}
    merged_into = {later: min(earliers, key=order.get) for later, earliers in same.items()}
    def survivor(key):
        while key in merged_into:
            key = merged_into[key]
        return key
    cache = json.loads((folder / 'embeddings.json').read_text())
    targets = collections.defaultdict(set)
    for r in reference:
        if r['relation'] in ('same_statement', 'revision'):
            targets[r['later']].add(survivor(r['earlier']))
    found = collections.Counter()
    total = collections.Counter()
    for j, it in enumerate(items):
        if it['key'] not in targets:
            continue
        pool = [e for e in items[:j] if e['article'] < it['article'] and e['key'] not in merged_into]
        r2 = {e['key'] for e in sorted(pool, key=lambda e: -cosine(cache[f"q2:{it['key']}"], cache[f"doc:{e['key']}"]))[:10]}
        for thesis in it['theses']:
            r1 = {e['key'] for e in sorted(pool, key=lambda e: -cosine(cache[f"q1:{it['key']}:{thesis['id']}"], cache[f"doc:{e['key']}"]))[:10]}
            total['R1'] += 1; found['R1'] += bool(targets[it['key']] & r1)
        total['R2'] += 1; found['R2'] += bool(targets[it['key']] & r2)
    print(f'deduplicated history ({len(merged_into)} items merged away): R1 per association, a surviving counterpart in the top 10 '
          f'{found["R1"]}/{total["R1"]}; R2 per item {found["R2"]}/{total["R2"]}')


if __name__ == '__main__':
    main()
