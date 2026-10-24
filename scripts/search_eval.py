"""Build the search index over a ledger and run the evaluation sentences through it: the four example theses of
the mock and the sixteen day-0 sentences (poc/eval/mappings.csv, whose mapped_view_id is the day-0 mapper's choice,
a lead rather than gold). Prints the top-k for each with scores, and how often the lead view is in the top 1 and
top 3. Embeddings cost about $0.0002 for the ledger and are cached; a rerun is free.

Usage: python3 scripts/search_eval.py [--views DB] [--index DB] [--k 10]
"""
import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import search, service  # noqa: E402

# the four example theses with the views a reader would accept in the top 3 (the check that must pass); the day-0
# sentences carry the day-0 mapper's choice as a lead, reported but not required
EXAMPLES = [
    ("Can NVIDIA's data center revenue top $300B this year?", {'v3'}),
    ('The AI capex bubble is about to pop', {'v1', 'v23', 'v72', 'v89', 'v20', 'v88'}),      # any hyperscaler / AI capex spend view
    ('Vera Rubin volume shipments will slip past H2', {'v7'}),
    ("NVIDIA can't hold a 75% gross margin", {'v4'}),
]


def lead_of(row):
    """The day-0 mapper's view for a sentence, or None: the mapper wrote the literal 'none' when nothing fit."""
    lead = (row.get('mapped_view_id') or '').strip()
    return lead if lead and lead.lower() != 'none' else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'search-index.sqlite'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--mappings', default=os.path.join(ROOT, 'poc', 'eval', 'mappings.csv'))
    parser.add_argument('--k', type=int, default=10)
    parser.add_argument('--as-of', default=None)
    args = parser.parse_args()
    ledger = service.open_ledger(args.views)
    index = search.open_index(args.index)
    embedded, unchanged, tokens, error = search.build_index(ledger, index)
    print(f'index: {embedded} views embedded, {unchanged} unchanged, {tokens} tokens (~${tokens / 1e6 * search.EMBEDDING_PRICE_PER_M:.4f})')
    if error:
        print(f'index incomplete: {error}')
        sys.exit(1)
    aliases = search.object_aliases(args.universe)
    failures = []
    for sentence, accepted in EXAMPLES:
        result = search.search(ledger, index, sentence, args.k, args.as_of, aliases=aliases)
        ids = [r['view_id'] for r in result['results'] or []]
        hit = bool(set(ids[:3]) & accepted)
        if not hit:
            failures.append(sentence)
        print(f'\n"{sentence}"  accepted {sorted(accepted)}  mode {result["mode"]}  {"PASS" if hit else "FAIL"}')
        print_results(result, accepted)
    top1 = top3 = judged = nulls = 0
    with open(args.mappings, encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            lead = lead_of(row)
            result = search.search(ledger, index, row['sentence'], args.k, args.as_of, aliases=aliases)
            ids = [r['view_id'] for r in result['results'] or []]
            if lead:
                judged += 1
                top1 += ids[:1] == [lead]
                top3 += lead in ids[:3]
                if result['results'] is None:
                    failures.append(row['sentence'])        # the mapper placed it on a view; null is a miss
            elif result['results'] is None:
                nulls += 1
            print(f'\n"{row["sentence"][:70]}"  day-0 lead {lead or "none"}  mode {result["mode"]}')
            print_results(result, {lead} if lead else set())
    print(f'\nexamples: {len(EXAMPLES) - sum(s in dict(EXAMPLES) for s in failures)}/{len(EXAMPLES)} with an accepted view in the top 3' + (f'; FAILED: {failures}' if failures else ''))
    print(f'day-0 sentences with a lead ({judged}): lead in top 1 {top1}, in top 3 {top3} (a lead, not gold); of the sentences the mapper left on none, {nulls} got null')
    if failures:
        sys.exit(1)


def print_results(result, marked):
    if result['results'] is None:
        print('    null: no recorded view on anything the idea names')
        return
    for r in result['results'][:5]:
        print(f'  {"*" if r["view_id"] in marked else " "} {r["view_id"]:4s} {r["score"]:.3f} (sem {r["parts"]["semantic"]:.3f}{" obj" if r["parts"]["object_hit"] else ""}{" txt" if r["parts"]["text_hit"] else ""})  {r["looks_at"][:60]}')


if __name__ == '__main__':
    main()
