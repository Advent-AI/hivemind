"""The small comparison of D559, to be started only on Alex's word: the unchanged first step reads each of the week of
10-06's opening articles twice, once from an empty library and once from the week of 09-22's completed library. Each read is
its own one-article run of the real launcher (`clean-arch/step1/run_live.py`) from a fixed starting library, on one shared
ledger. One draw.

  python3 <budget_replay.py> --init-ledger <ledger> --ceiling 1.00        # a new ledger, once
  python3 run_probe.py --root <new folder> --ledger <ledger>

Stopping rule: the probe stops at the first read that the ledger refuses, that fails in transport after its retries, or
whose launcher prints no result; what was read stays. An answer the first step's own checks reject is that read's outcome
and does not stop the others.
"""
import argparse
import concurrent.futures
import json
import os
import subprocess
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
RUN_LIVE = ROOT / 'clean-arch/step1/run_live.py'
INPUTS = HERE / 'inputs'
CONDITIONS = ('empty', 'carried')
LIMITS = {'max_usd': 40.0, 'max_seconds': 1800, 'max_calls': 6, 'input_usd_per_million': 0.5, 'output_usd_per_million': 1.2}
WORKERS = 2
MUTANT = os.environ.get('PROBE_MUTANT', '')


def stops(result):
    error = str(result.get('error') or '')
    return result.get('status') == 'no result' or 'live run limit reached' in error or error.startswith('TransportError')


def read_once(root, ledger, article, condition, base):
    folder = root / f"{article['sequence']:03d}-{condition}"
    folder.mkdir()
    (folder / 'manifest.json').write_text(json.dumps(dict(base, item_ids=[article['input_id']], item_limit=1), indent=1))
    (folder / 'initial.json').write_text((INPUTS / f'initial-{condition}.json').read_text())
    (folder / 'settings.json').write_text((INPUTS / 'settings.json').read_text())
    (folder / 'limits.json').write_text(json.dumps(LIMITS, indent=1))
    completed = subprocess.run([sys.executable, str(RUN_LIVE), '--source', str(ITEMS), '--output', str(folder / 'trace.sqlite'),
                                '--manifest', str(folder / 'manifest.json'), '--initial', str(folder / 'initial.json'),
                                '--settings', str(folder / 'settings.json'), '--limits', str(folder / 'limits.json'),
                                '--shared-ledger', str(ledger)], capture_output=True, text=True)
    (folder / 'stdout.txt').write_text(completed.stdout)
    (folder / 'stderr.txt').write_text(completed.stderr)
    result = {'status': 'no result', 'error': completed.stderr.strip()[-400:]}
    for line in reversed(completed.stdout.strip().splitlines()):
        if line.startswith('{'):
            result = json.loads(line)
            break
    return {'sequence': article['sequence'], 'input_id': article['input_id'], 'condition': condition, 'exit': completed.returncode,
            **{key: result.get(key) for key in ('status', 'error', 'calls', 'reserved_usd', 'failed_items')}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--ledger', required=True)
    args = parser.parse_args()
    root, ledger = Path(args.root), Path(args.ledger)
    if not ledger.exists():
        raise SystemExit('the ledger does not exist: initialise it first')
    root.mkdir(parents=True, exist_ok=False)
    articles = json.loads((INPUTS / 'articles.json').read_text())
    base = json.loads((INPUTS / 'manifest-base.json').read_text())
    jobs = [(article, condition) for article in articles for condition in CONDITIONS]
    stop, lock, outcomes = threading.Event(), threading.Lock(), []

    def work(job):
        if stop.is_set():
            return
        row = read_once(root, ledger, job[0], job[1], base)
        with lock:
            outcomes.append(row)
            with open(root / 'outcomes.jsonl', 'a') as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + '\n')
            if stops(row) and MUTANT != 'no-stop':
                stop.set()

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(work, jobs))
    summary = {'planned': len(jobs), 'read': len(outcomes), 'stopped': stop.is_set(),
               'complete': sum(1 for row in outcomes if row['status'] == 'complete')}
    (root / 'summary.json').write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary))
    return 0 if summary['read'] == summary['planned'] and not summary['stopped'] else 1


if __name__ == '__main__':
    sys.exit(main())
