"""Pull the data a front-end mock needs from a sealed views database: every view of the chosen objects with its
ladder, its judgement history (rung per round with the model's reason and the evidence it cited), the evidence in
force with tiers, speakers and sources, dependencies, replacements and the freeze switches. Writes one JSON file.
The shaping is src/hivemind/bundle.py, the same one POST /ideas answers with. Read-only on every database; nothing
is sent to a model.

Usage: python3 scripts/mock_data.py --out poc/mock/data.json [--objects NVDA ai-capex]
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import bundle  # noqa: E402
from hivemind.views import store  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite'))
    parser.add_argument('--items', default=os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'))
    parser.add_argument('--objects', nargs='*', default=['NVDA', 'ai-capex'])
    parser.add_argument('--out', default=os.path.join(ROOT, 'poc', 'mock', 'data.json'))
    args = parser.parse_args()
    views_db, items_db = store.open_read_only(args.views), store.open_read_only(args.items)
    marks = ','.join('?' * len(args.objects))
    ids = [r[0] for r in views_db.execute(f'select view_id from views where object_id in ({marks}) order by created_seq', args.objects)]
    item_of = bundle.item_lookup(items_db)
    out = {'objects': args.objects, 'views': [bundle.view_bundle(views_db, item_of, view_id) for view_id in ids], 'days': bundle.days(views_db)}
    with open(args.out, 'w', encoding='utf-8') as handle:
        json.dump(out, handle, ensure_ascii=False, indent=0)
    print(f'{len(out["views"])} views, {sum(len(v["judgements"]) for v in out["views"])} judgements, {sum(len(v["evidence"]) for v in out["views"])} evidence links → {args.out} ({os.path.getsize(args.out) // 1024} KB)')


if __name__ == '__main__':
    main()
