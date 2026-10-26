#!/usr/bin/env python3
"""Run the POC replay.

  python3 scripts/replay.py --from 2026-02-25 --until 2026-07-23 --views poc/data/<run>/views.sqlite \
      --archive poc/data/<run>/archive.sqlite [--only NVDA] [--day0 2026-07-24] [--cap 3] [--workers 1]

The ledger and the archive are named on every run (a new run gets a new dated folder; an existing ledger resumes after
its last completed day). Defaults: the item window poc/data/items-window-tags2-2026-10-24.sqlite, config
poc/config/poc-v26.json (D190: extraction v12 with the admission fields, Jev matching with the collision judge), universe poc/universe.json. The log goes to stdout and
replay.log beside the ledger. Each day runs with hivemind.parallel_day by default (D183): up to `--workers` (16)
extraction requests prepared early and validated against the committed ledger at each item's turn, `--jev-workers`
Jev matching questions at a time (8; one at a time for another matching engine); the ledger equals the serial one for
the same answers (D181, D182). Its per-day manifests are written beside the ledger. `--workers 1` runs the serial
path, which sends no call on a rerun over saved answers and resumes a day a serial run left unfinished.
"""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))

from hivemind import config, model, parallel_day, replay, universe  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_day', required=True)
    parser.add_argument('--until', dest='until_day', required=True)
    parser.add_argument('--day0', default=None)
    parser.add_argument('--testdb', default=os.path.join(ROOT, 'poc', 'data', 'items-window-tags2-2026-10-24.sqlite'))
    parser.add_argument('--views', required=True, help='the ledger this run writes (a new run: a new dated folder)')
    parser.add_argument('--archive', required=True, help='the model-call archive of this run')
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v26.json'))     # D190
    parser.add_argument('--universe', default=os.path.join(ROOT, 'poc', 'universe.json'))
    parser.add_argument('--only', default=None, help='comma-separated object ids to restrict the stream to')
    parser.add_argument('--cap', type=float, default=None, help='USD spend cap for this run')
    parser.add_argument('--max-items-per-day', type=int, default=None)
    parser.add_argument('--workers', type=int, default=16, help='extraction requests prepared at a time (D183); 1 is the serial path')
    parser.add_argument('--jev-workers', type=int, default=None,
                        help='Jev matching questions sent at a time when --workers > 1; default 8 for Jev, 1 for another engine')
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
    day_runner = None
    if args.workers > 1:
        jev_workers = args.jev_workers if args.jev_workers is not None else (8 if cfg.matching.engine == 'jev' else 1)
        day_runner = parallel_day.ParallelDay(os.path.abspath(args.testdb), os.path.join(os.path.dirname(os.path.abspath(args.views)), 'manifests'),
                                              extraction_workers=args.workers, jev_workers=jev_workers)
    log(f'--- replay {args.from_day}..{args.until_day} config {cfg.version}/{cfg.checksum} provider {cfg.provider} universe {uni.version}'
        f' workers {args.workers}')
    totals = replay.run(testdb_path=args.testdb, views_path=args.views, archive=archive, cfg=cfg, universe=uni,
                        from_day=args.from_day, until_day=args.until_day, day0=args.day0, spend_cap_usd=args.cap, log=log,
                        only_objects=set(args.only.split(',')) if args.only else None, max_items_per_day=args.max_items_per_day,
                        day_runner=day_runner)
    log('totals:', totals)


if __name__ == '__main__':
    main()
