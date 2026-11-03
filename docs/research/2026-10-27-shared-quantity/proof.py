#!/usr/bin/env python3
"""Cheapest proof for D197 ($0): walk every candidate of a stored ledger in sequence order and apply the shared-quantity rule
against the theses that existed before it (a stored theme thesis with a quantity measure counts as shared, which is what the
writer now records); print, per aggregate candidate, the stored outcome and the rule's, and count the flips and everything
else the rule touches (any candidate it fires on that is not an aggregate of a theme).

  python3 docs/research/2026-10-27-shared-quantity/proof.py --ledger /abs/run-dir [...]
"""
import argparse
import collections
import json
import sqlite3
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind.views import identity  # noqa: E402


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', action='append', required=True)
    args = ap.parse_args()
    for ledger in args.ledger:
        conn = ro(f'{ledger}/views.sqlite')
        views = {r['view_id']: dict(r) for r in conn.execute('select v.*, k.measure, k.period_start, k.period_end, k.scope from views v join view_keys k using(view_id)')}
        successions = {r['succeeds'] for r in conn.execute('select succeeds from successions')}
        fired, flips, touched_other = 0, collections.Counter(), []
        print(f'== {ledger}')
        for h in conn.execute('select input_id, seq, handover_json from handovers order by seq'):
            decided = {}
            for r in conn.execute('select decisions_json from match_records where input_id=?', (h['input_id'],)):
                for d in json.loads(r['decisions_json']).get('candidates', []):
                    decided[d['id']] = d
            for c in json.loads(h['handover_json'])['candidates']:
                if not identity.is_shared(c):
                    continue
                fired += 1
                if views.get(c.get('object')) is None and not any(v['object_kind'] == 'theme' for v in views.values() if v['object_id'] == c.get('object')):
                    touched_other.append((h['seq'], c.get('object'), c.get('measure'), c.get('opens_as')))
                before = [v for v in views.values() if v['object_id'] == c['object'] and v['measure'] == c.get('measure') and v['created_seq'] < h['seq'] and v['object_kind'] == 'theme']
                same = [v['view_id'] for v in before if v['period_start'] == c.get('period_start')]      # open status: no theme thesis closed in these windows
                earlier = sorted([v for v in before if v['period_end'] < c.get('period_start', '') and v['view_id'] not in successions], key=lambda v: v['period_end'], reverse=True)
                rule = ('merge', same[0]) if same else (('succession', earlier[0]['view_id']) if earlier else ('new', ''))
                stored = decided.get(c['id'], {})
                was = (stored.get('outcome', '?'), stored.get('target_view_id', ''))
                flips[(was[0], rule[0])] += 1
                mark = '' if was[0] == rule[0] else '  <-- flip'
                print(f"  seq {h['seq']:4d} {c.get('object')} {c.get('measure')} {c.get('period_start','')[:4]} [{(c.get('scope') or '')[:55]}] stored {was} rule {rule}{mark}")
        print(f'  shared candidates the rule fires on: {fired}; stored outcome -> rule outcome: {dict(flips)}; non-theme objects touched: {touched_other}')


if __name__ == '__main__':
    main()
