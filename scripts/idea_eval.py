"""Read the evaluation sentences as ideas (docs/poc/idea-card.md): the four example theses and the sixteen day-0
sentences (poc/eval/mappings.csv; mapped_view_id is the day-0 mapper's choice, a lead rather than gold). Prints,
per idea, the views the model chose against the lead, the claim and its verdict, cost and seconds, and the totals.
Calls are archived in the service's archive, so a rerun of the same ideas on the same ledger is free.

Usage: python3 scripts/idea_eval.py [--views DB] [--items DB] [--index DB] [--archive DB] [--config JSON]
"""
import argparse
import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, idea, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

EXAMPLES = ["Can NVIDIA's data center revenue top $300B this year?", 'The AI capex bubble is about to pop',
            'Vera Rubin volume shipments will slip past H2', "NVIDIA can't hold a 75% gross margin"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service', 'search-index.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'service', 'idea-archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v7.json'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--mappings', default=os.path.join(ROOT, 'poc', 'eval', 'mappings.csv'))
    parser.add_argument('--as-of', default=None)
    args = parser.parse_args()
    ledger, items = service.open_ledger(args.views), store.open_read_only(args.items)
    index, archive, cfg = search.open_index(args.index), model.Archive(args.archive), config.load(args.config)
    aliases = search.object_aliases(args.universe)
    sentences = [(s, None) for s in EXAMPLES]
    with open(args.mappings, encoding='utf-8') as handle:
        for row in csv.DictReader(handle):
            lead = (row['mapped_view_id'] or '').strip()
            sentences.append((row['sentence'], lead if lead and lead.lower() != 'none' else None))
    usd = seconds = calls = agree = judged = 0
    for sentence, lead in sentences:
        card = idea.read_idea(ledger, index, items, archive, cfg, sentence, args.as_of, aliases=aliases)
        chosen = [c['view_id'] for c in card['reading']['chosen']] if card['reading'] else None
        if lead:
            judged += 1
            agree += bool(chosen and lead in chosen)
        if card['reading']:
            calls += 1
            usd += card['cost']['usd']
            seconds += card['cost']['seconds']
        verdict = card['evaluation']['verdict'] if card['evaluation'] else ('-' if not card['reading'] or not card['reading']['claim'] else 'claim dropped')
        print(f'\n"{sentence[:72]}"')
        print(f'   lead {lead or "-":4s}  chosen {chosen if chosen is not None else "null (no recorded view)"}  claim {card["reading"]["claim"] if card["reading"] else "-"}  verdict {verdict}'
              f'  ${card["cost"]["usd"]:.4f} {card["cost"]["seconds"]}s{" cached" if card["cost"]["cached"] else ""}')
        if card['reading']:
            print(f'   summary: {card["reading"]["summary"]}')
            for c in card['reading']['chosen']:
                print(f'     {c["view_id"]}: {c["why"]}')
            if card['reading']['dropped']:
                print(f'   dropped: {card["reading"]["dropped"]}')
    print(f'\n{len(sentences)} ideas, {calls} model calls, ${usd:.4f} this run, {seconds:.1f}s model time; the day-0 lead is among the chosen views in {agree}/{judged} (a lead, not gold)')


if __name__ == '__main__':
    main()
