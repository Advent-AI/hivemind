#!/usr/bin/env python3
"""D197 small-scale validation: replay the r5 window with every extraction answer pinned to r5's recorded answer (ids translated),
Jev and the collision judge live under the changed identity code, judging synthetic. Only matching differs from r5, so the
count of aggregate theses is the rule's. Reuses the D190 pinned study's transport.

  python3 docs/research/2026-10-27-shared-quantity/pinned_arm.py --source /abs/r5 --out /abs/out-dir
"""
import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'docs' / 'research' / '2026-10-26-thesis-admission-v12'))
import pinned_matching_study as study  # noqa: E402

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    study.run_arm('arm-v29-shared', ROOT / 'poc' / 'config' / 'poc-v29.json', pathlib.Path(args.source), pathlib.Path(args.out))
    print('DONE', flush=True)
