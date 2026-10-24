"""Stability of the idea route (docs/poc/idea-card.md, tuning plan Q5): the same ideas asked N times against fresh
archives, so every sample is a real model call. Reports, per idea and overall: agreement of the parts' objects, of the
first part's direct view, the pairwise overlap (Jaccard) of the direct+driver set and of the full mapped set,
language slips, seconds and cost. Writes nothing into the service's archive.

Usage: python3 scripts/idea_stability.py [--samples 3] [--only N] [--ideas FILE] [--tag SUFFIX] [--config JSON] [--out DIR]
"""
import argparse
import itertools
import json
import os
import statistics
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, idea, model, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

IDEAS = ["Can NVIDIA's data center revenue top $300B this year?", 'Hyperscaler capex peaks in 2026 and falls in 2027',
         'Vera Rubin volume shipments will slip past H2', '数据中心需求见顶了吗？', "NVIDIA can't hold a 75% gross margin",
         "AMD's MI450 will take data center share from NVIDIA in 2027", 'Is the AI trade over?', 'CoreWeave is power-constrained: active capacity below 1GW at year end']


def jaccard(a, b):
    return len(a & b) / len(a | b) if a | b else 1.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--index', default=os.path.join(ROOT, 'poc', 'data', 'service', 'search-index.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v9.json'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--samples', type=int, default=3)
    parser.add_argument('--out', default=os.path.join(ROOT, 'poc', 'data', 'service', 'stability'), help='fresh archives, one per sample, named by config version')
    parser.add_argument('--only', type=int, default=None, help='the first N ideas only: a small run before a full one')
    parser.add_argument('--ideas', default=None, help='a JSON file with an "ideas" list instead of the built-in eight (the held-out set)')
    parser.add_argument('--tag', default='', help='a suffix for the archive and summary names, so two idea sets never share an archive')
    args = parser.parse_args()
    ideas = json.load(open(args.ideas, encoding='utf-8'))['ideas'] if args.ideas else IDEAS
    tag = f'-{args.tag}' if args.tag else ''
    ledger, items = service.open_ledger(args.views), store.open_read_only(args.items)
    index, cfg = search.open_index(args.index), config.load(args.config)
    aliases = search.object_aliases(args.universe)
    os.makedirs(args.out, exist_ok=True)
    archives = [model.Archive(os.path.join(args.out, f'{cfg.version}{tag}-sample-{k}.sqlite')) for k in range(args.samples)]
    rows = []
    for text in ideas[:args.only]:
        samples = []
        for archive in archives:
            started = time.time()
            card = idea.read_idea(ledger, index, items, archive, cfg, text, aliases=aliases)
            samples.append((card, time.time() - started))
        readings = [c['reading'] for c, _ in samples]
        objects = [tuple(p['object'] for p in r['parts']) for r in readings]
        firsts = [(r['parts'][0]['view_ids'] or [None])[0] if r['parts'] else None for r in readings]
        core = [set(c['view_id'] for c in r['chosen']) for r in readings]
        full = [s | set(v for p in r['parts'] for v in p.get('context', [])) for s, r in zip(core, readings)]
        pairs = list(itertools.combinations(range(len(samples)), 2))
        row = {'idea': text, 'objects_agree': len(set(objects)) == 1, 'first_agree': len(set(firsts)) == 1, 'firsts': firsts,
               'core_overlap': statistics.mean(jaccard(core[a], core[b]) for a, b in pairs) if pairs else 1.0,     # one sample: nothing to compare, timing only
               'full_overlap': statistics.mean(jaccard(full[a], full[b]) for a, b in pairs) if pairs else 1.0,
               'core_sizes': [len(s) for s in core], 'slips': sum(r.get('language_slips', 0) for r in readings),
               'seconds': statistics.median(s for _, s in samples), 'usd': sum(c['cost']['usd'] for c, _ in samples) / len(samples)}
        rows.append(row)
        print(f"{text[:52]:52s} objects {'same' if row['objects_agree'] else 'DIFFER'} | first {row['firsts']} | core {row['core_sizes']} overlap {row['core_overlap']:.2f} | full overlap {row['full_overlap']:.2f} | slips {row['slips']} | {row['seconds']:.1f}s ${row['usd']:.4f}")
    print(f"\n{cfg.version}: {len(rows)} ideas × {args.samples} samples: objects agree {sum(r['objects_agree'] for r in rows)}/{len(rows)}; first view agrees {sum(r['first_agree'] for r in rows)}/{len(rows)}; "
          f"core overlap median {statistics.median(r['core_overlap'] for r in rows):.2f}; full overlap median {statistics.median(r['full_overlap'] for r in rows):.2f}; "
          f"language slips {sum(r['slips'] for r in rows)}; seconds per idea median {statistics.median(r['seconds'] for r in rows):.1f}; cost per idea mean ${statistics.mean(r['usd'] for r in rows):.4f}")
    with open(os.path.join(args.out, f'{cfg.version}{tag}-summary.json'), 'w', encoding='utf-8') as handle:
        json.dump(rows, handle, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
