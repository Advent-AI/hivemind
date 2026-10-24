#!/usr/bin/env python3
"""Run the POC replay.

  python3 scripts/replay.py --from 2026-02-25 --until 2026-02-25 [--day0 2026-07-24] [--only NVDA] [--cap 50]
  python3 scripts/replay.py --views poc/data/views.sqlite --archive poc/data/archive.sqlite ...

Defaults: test database poc/corpus/items.sqlite, views poc/data/views.sqlite, archive poc/data/archive.sqlite,
config poc/config/poc-v1.json, universe poc/universe.json. The log goes to stdout and poc/data/replay.log.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

from hivemind import config, model, replay, universe  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_day', required=True)
    parser.add_argument('--until', dest='until_day', required=True)
    parser.add_argument('--day0', default=None)
    parser.add_argument('--testdb', default=os.path.join(ROOT, 'poc', 'corpus', 'items.sqlite'))
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'views.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v1.json'))
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--only', default=None, help='comma-separated object ids to restrict the stream to')
    parser.add_argument('--cap', type=float, default=None, help='USD spend cap for this run')
    parser.add_argument('--max-items-per-day', type=int, default=None)
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.views), exist_ok=True)
    log_path = os.path.join(os.path.dirname(args.views), 'replay.log')

    def log(*parts):
        line = ' '.join(str(p) for p in parts)
        print(line, flush=True)
        with open(log_path, 'a', encoding='utf-8') as handle:
            handle.write(line + '\n')

    cfg = config.load(args.config)
    uni = universe.load(args.universe)
    archive = model.Archive(args.archive)
    log(f'--- replay {args.from_day}..{args.until_day} config {cfg.version}/{cfg.checksum} provider {cfg.provider} universe {uni.version}')
    totals = replay.run(testdb_path=args.testdb, views_path=args.views, archive=archive, cfg=cfg, universe=uni,
                        from_day=args.from_day, until_day=args.until_day, day0=args.day0, spend_cap_usd=args.cap, log=log,
                        only_objects=set(args.only.split(',')) if args.only else None, max_items_per_day=args.max_items_per_day)
    log('totals:', totals)


if __name__ == '__main__':
    main()
