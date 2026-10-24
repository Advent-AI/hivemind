"""Score the idea route against the sealed gold set (poc/eval/gold/idea-gold-<date>.json, authored by Claude in the
analyst's role at Alex's request, 2026-10-25). The gold file's SHA-256 must match poc/eval/gold/SHA256SUMS, or the
script refuses: a changed gold is a new dated file, never an edit. Per idea: whether a direct view the card shows for the
idea's first part is one the gold accepts (or none when the gold says the library has none), whether a trap view is
shown as direct anywhere, how many of the gold's drivers reach the canvas, how much of the canvas is neither direct,
driver nor acceptable (noise), and whether the stated amount is judged against the gold's view. Model calls go through
the service's archive, so a repeat costs nothing.

Usage: python3 scripts/idea_gold.py [--gold FILE] [--config JSON] [--only N] [--archive FILE]
"""
import argparse
import hashlib
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, idea, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

GOLD_DIR = os.path.join(ROOT, 'poc', 'eval', 'gold')


def sealed(path):
    """The gold file's recorded digest, or a refusal."""
    digest = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    sums = os.path.join(GOLD_DIR, 'SHA256SUMS')
    recorded = {line.split()[1].lstrip('*'): line.split()[0] for line in open(sums, encoding='utf-8') if line.strip()} if os.path.exists(sums) else {}
    name = os.path.basename(path)
    if recorded.get(name) != digest:
        raise SystemExit(f'refused: {name} is not the sealed file (digest {digest[:12]}…, recorded {str(recorded.get(name))[:12]}…)')
    return digest


def score(card, gold):
    parts = card['reading']['parts'] if card['reading'] else []
    first_direct = parts[0]['direct'] if parts else []
    all_direct = {v for p in parts for v in p['direct']}
    canvas = {c['view_id'] for c in card['reading']['chosen']} if card['reading'] else set()
    accepted = set(gold['direct'])
    direct_ok = (first_direct[0] in accepted) if first_direct else not accepted          # no direct shown is right only when the gold has none
    traps_as_direct = sorted(all_direct & set(gold['traps']))
    drivers = set(gold['drivers'])
    driver_recall = len(canvas & drivers) / len(drivers) if drivers else None
    fine = accepted | drivers | set(gold['acceptable'])
    noise = sorted(canvas - fine)
    claim = card['reading']['claim'] if card['reading'] else None
    if gold['claim']:
        claim_ok = bool(claim) and claim.get('view_id') == gold['claim']['view_id'] and claim.get('comparator') == gold['claim']['comparator'] and float(claim.get('value_usd', 0)) == float(gold['claim']['value_usd'])
    else:
        claim_ok = claim is None
    return {'direct_ok': direct_ok, 'first_direct': first_direct[:1], 'traps_as_direct': traps_as_direct, 'driver_recall': driver_recall,
            'noise': noise, 'canvas': len(canvas), 'claim_ok': claim_ok, 'claim_view': claim.get('view_id') if claim else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gold', default=os.path.join(GOLD_DIR, 'idea-gold-2026-10-25.json'))
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service', 'search-index.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'service', 'idea-archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v9.json'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--only', type=int, default=None, help='the first N ideas only: a small run before a full one')
    args = parser.parse_args()
    digest = sealed(args.gold)
    gold = json.load(open(args.gold, encoding='utf-8'))
    ledger, items = service.open_ledger(args.views), store.open_read_only(args.items)
    index, cfg = search.open_index(args.index), config.load(args.config)
    aliases, archive = search.object_aliases(args.universe), model.Archive(args.archive)
    rows, spent = [], 0.0
    print(f"gold {gold['name']} ({digest[:12]}…, {gold['authored_by'][:60]}…) · config {cfg.version} · as of {gold['as_of']}")
    for g in gold['ideas'][:args.only]:
        card = idea.read_idea(ledger, index, items, archive, cfg, g['text'], as_of=gold['as_of'], aliases=aliases, bundles=False)
        spent += card['cost']['usd']
        s = score(card, g)
        rows.append(s)
        recall = '-' if s['driver_recall'] is None else f"{s['driver_recall']:.2f}"
        print(f"{g['id']:2d}. {'direct ok ' if s['direct_ok'] else 'DIRECT NO '}{str(s['first_direct']):8s} traps {str(s['traps_as_direct'] or '-'):<14} drivers {recall:>5} "
              f"noise {len(s['noise'])}/{s['canvas']} {s['noise'] or ''} claim {'ok' if s['claim_ok'] else 'NO ' + str(s['claim_view'])}  {g['text'][:48]}")
    n = len(rows)
    recalls = [r['driver_recall'] for r in rows if r['driver_recall'] is not None]
    noise = sum(len(r['noise']) for r in rows); canvas = sum(r['canvas'] for r in rows)
    print(f"\n{n} ideas judged: direct view right {sum(r['direct_ok'] for r in rows)}/{n}; ideas with a trap shown as direct {sum(bool(r['traps_as_direct']) for r in rows)}/{n}; "
          f"driver recall median {statistics.median(recalls):.2f} over {len(recalls)} ideas; canvas noise {noise}/{canvas} views ({100 * noise / max(1, canvas):.0f}%); "
          f"claims right {sum(r['claim_ok'] for r in rows)}/{n}; spent ${spent:.4f}")


if __name__ == '__main__':
    main()
