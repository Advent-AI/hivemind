#!/usr/bin/env python3
"""Cheapest proof for the main_driver wording (AGENTS §1.4): re-send the NVDA 2026-02-25 call with an empty library under
poc-v25 three times and list the candidates each answer proposes. Scratch archive in the scratchpad; nothing written to any ledger.

  python3 docs/research/2026-10-26-thesis-admission-v12/probe_main_driver.py <scratch archive path> [samples]
"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model, universe  # noqa: E402

ITEMS = '/Users/lchingen/hivemind/poc/data/items-window-tags2-2026-10-24.sqlite'
ITEM_ID = 'truenorth:transcript:NVDA:2026-02-25'


def main():
    archive = model.Archive(sys.argv[1])
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v25.json'))
    uni = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
    with sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        item = dict(db.execute('select * from items where input_id=?', (ITEM_ID,)).fetchone())
    item['object_identifiers'] = json.loads(item['object_identifiers']) if isinstance(item['object_identifiers'], str) else item['object_identifiers']
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], [], uni)
    total = 0.0
    for sample in range(samples):
        answer = model.call(archive, cfg, setting, system, user + f'\n\n[sample {sample + 1}]', schema, 'extraction', 'extract')     # the tag makes each sample a fresh call
        total += answer.cost_usd
        evidence, candidates, dropped, _ = extraction.sift_with_groups(answer.data, item, item['text'], set(), uni, english=True)
        print(f'--- sample {sample + 1}: evidence {len(evidence)}, candidates kept {len(candidates)}, dropped {[d[1][:40] for d in dropped]}, ${answer.cost_usd:.4f}')
        for c in candidates:
            print(f"    {c['object']:>22} {c['measure']:<16} {c.get('scope', ''):<42} {c['year']:<7} {c['opens_as']:<18} folds_into={c.get('folds_into')!r}")
    print(f'total ${total:.4f}')


if __name__ == '__main__':
    main()
