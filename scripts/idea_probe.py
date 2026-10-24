"""Probe the idea route with realistic ideas (poc/eval/idea-probes-<date>.json): for each, what search put in the
top-k and where the expected views rank, what the model chose, the claim and its verdict, and a flag per failure
class. Prints the per-probe detail and a census by flag. Calls are archived in the service's archive (a rerun is $0).

Flags: MISS (an expected view is not among the candidates), NOISE (an expected view ranks below an unexpected one
in the chosen list), NULL (search found nothing), EMPTY (the model chose nothing), UNEXPECTED (a chosen view is
outside the expected set), CLAIM_DROPPED, NOT_EVALUABLE (the claimed ladder is not money), OBJECT_WITHOUT_VIEWS (the
idea names a universe object that has no view as of the day).

Usage: python3 scripts/idea_probe.py [--probes JSON] [--k 10] [--only N]
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, idea, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service', 'search-index.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'service', 'idea-archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v9.json'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--probes', default=os.path.join(ROOT, 'poc', 'eval', 'idea-probes-2026-10-24.json'))
    parser.add_argument('--k', type=int, default=20)
    parser.add_argument('--only', type=int, default=None, help='run only the first N probes')
    parser.add_argument('--search-only', action='store_true', help='candidates and flags from search alone, no model call ($0)')
    args = parser.parse_args()
    ledger, items = service.open_ledger(args.views), store.open_read_only(args.items)
    index, archive, cfg = search.open_index(args.index), model.Archive(args.archive), config.load(args.config)
    aliases = search.object_aliases(args.universe)
    with open(args.probes, encoding='utf-8') as handle:
        probes = json.load(handle)['probes'][:args.only]
    census, usd = {}, 0.0
    for n, probe in enumerate(probes, 1):
        text, expect, as_of = probe['text'], set(probe['expect']), probe.get('as_of')
        found = search.search(ledger, index, text, args.k, as_of, aliases=aliases)
        card = idea.read_idea(ledger, index, items, archive, cfg, text, as_of, args.k, aliases=aliases) if not args.search_only else \
            {'idea': {'text': text, 'as_of': found['as_of']}, 'reading': None, 'evaluation': None, 'no_recorded_view': found['results'] is None, 'cost': dict(idea.NO_COST)}
        usd += card['cost']['usd']
        ranked = [(r['view_id'], r['score'], r['parts']) for r in found['results'] or []]
        rank_of = {v: i + 1 for i, (v, _, _) in enumerate(ranked)}
        chosen = [c['view_id'] for c in card['reading']['chosen']] if card['reading'] else None
        flags = []
        missing = sorted(v for v in expect if v not in rank_of)
        if missing:
            flags.append('MISS')
        if card['no_recorded_view']:
            flags.append('NULL')
        elif chosen == []:
            flags.append('EMPTY')
        if chosen:
            if any(v not in expect for v in chosen):
                flags.append('UNEXPECTED')
            if expect and chosen[0] not in expect and any(v in expect for v in chosen):
                flags.append('NOISE')
        if card['reading'] and any('claim' in d['why'] for d in card['reading']['dropped']):
            flags.append('CLAIM_DROPPED')
        if card['evaluation'] and card['evaluation'].get('evaluable') is False:
            flags.append('NOT_EVALUABLE')
        named = search.objects_in(text, aliases)
        as_of_day = card['idea']['as_of']
        without = sorted(o for o in named if not service.views(ledger, o, as_of_day, include_closed=True))
        if without:
            flags.append('OBJECT_WITHOUT_VIEWS')
        for f in flags:
            census[f] = census.get(f, 0) + 1
        print(f'\n{n:2d}. "{text}"' + (f'  as of {as_of}' if as_of else '') + f'   [{", ".join(flags) or "ok"}]')
        print(f'    search {found["mode"]}: ' + '  '.join(f'{v}{"*" if v in expect else ""} {s:.2f}{"o" if p["object_hit"] else ""}{"t" if p["text_hit"] else ""}' for v, s, p in ranked))
        if missing:
            print(f'    MISSING from the candidates: {missing}')
        if without:
            print(f'    names objects without a view as of {as_of_day}: {without}')
        if card['reading']:
            print(f'    chosen {chosen}  claim {card["reading"]["claim"]}  verdict {card["evaluation"]["verdict"] if card["evaluation"] and card["evaluation"].get("verdict") else (card["evaluation"].get("reason") if card["evaluation"] else "-")}  ${card["cost"]["usd"]:.4f}{" cached" if card["cost"]["cached"] else ""}')
            print(f'    summary: {card["reading"]["summary"]}')
            for part in card['reading'].get('parts', []):
                print(f'      part: {part["object"]} · {part["looks_for"]} · {part["period"]} → {part["view_ids"] or "no view"}' + ''.join(' *' for v in part['view_ids'] if v in expect)
                      + f'   [candidates {len(part["candidates"])}; direct {part.get("direct", [])} driver {part.get("driver", [])} context {part.get("context", [])}' + (f'; service direct {part["service_direct"]}' if part.get('service_direct') else '') + (' ; MARKET' if part.get('market_reading') else '') + ']')
                print(f'            {part["why"]}')
            if card.get('related'):
                print('      related (graph): ' + ', '.join(f"{r['view_id']} {r['relation']} of {r['via']}" for r in card['related']))
            if card['reading'].get('trace'):
                print('    trace: ' + '; '.join(f"search({x['query']!r})→{len(x['returned'])}" for x in card['reading']['trace']) + f"  turns {card['cost'].get('turns')}  tokens in {card['cost']['input_tokens']} out {card['cost']['output_tokens']}  seconds {card['cost']['seconds']}  slips {card['reading'].get('language_slips', 0)}")
            if card['reading']['dropped']:
                print(f'    dropped: {card["reading"]["dropped"]}')
        else:
            print('    null: no recorded view on anything the idea names')
    print(f'\n{len(probes)} probes, ${usd:.4f} this run; flags: ' + ', '.join(f'{k} {v}' for k, v in sorted(census.items(), key=lambda kv: -kv[1])))


if __name__ == '__main__':
    main()
