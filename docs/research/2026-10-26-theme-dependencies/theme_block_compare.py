#!/usr/bin/env python3
"""D195 measurement step 3: r5 (poc-v29, the theme block) beside r4 (poc-v26). Counts judgements, the judgements whose request
carried a block and whose answer named a theme push, propagation-only judgements (an asset thesis judged in a round where
none of its own inputs changed that day) and their changed share, judging cost at model.PRICES, and prints ten pairs of
reasons for the same thesis question side by side. $0.

  python3 docs/research/2026-10-26-theme-dependencies/theme_block_compare.py --control /abs/r4 --arm /abs/r5 [--pairs 10]
"""
import argparse
import json
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def summary(run):
    views, archive = ro(run / 'views.sqlite'), ro(run / 'archive.sqlite')
    kind = {r['view_id']: r['object_kind'] for r in views.execute('select view_id, object_kind from views')}
    columns = [r[1] for r in views.execute('pragma table_info(judgements)')]
    judgements = [dict(r) for r in views.execute('select * from judgements order by judgement_id')]
    changed_by_day = {}
    for r in views.execute("select publication_day, reason from processing_steps where step='written' and result='ok'"):
        changed_by_day.setdefault(r['publication_day'], set()).update(json.loads(r['reason']).get('changed', []))
    out = {'theses': len(kind), 'theme_theses': sum(1 for k in kind.values() if k == 'theme'), 'judgements': len(judgements),
           'asset_judgements': sum(1 for j in judgements if kind[j['view_id']] == 'company'),
           'with_theme_push': sum(1 for j in judgements if 'theme_pushes_json' in columns and j['theme_pushes_json'] not in (None, '', '[]')),
           'propagation_only': 0, 'propagation_only_changed': 0, 'rung_moves': 0}
    last_rung = {}
    for j in judgements:
        if kind[j['view_id']] == 'company' and j['view_id'] not in changed_by_day.get(j['publication_day'], set()):
            out['propagation_only'] += 1
            out['propagation_only_changed'] += int(bool(j['changed']))
        if j['view_id'] in last_rung and last_rung[j['view_id']] != j['rung']:
            out['rung_moves'] += 1
        last_rung[j['view_id']] = j['rung']
    rows = archive.execute("select purpose, count(*), sum(input_tokens), sum(output_tokens), model from model_calls group by purpose, model").fetchall()
    cost = {}
    for purpose, n, tin, tout, model_name in rows:
        price_in, price_out = model.PRICES.get(model_name, (0.0, 0.0))
        cost[purpose] = cost.get(purpose, 0.0) + (tin or 0) / 1e6 * price_in + (tout or 0) / 1e6 * price_out
        if purpose == 'judge':
            out['judge_calls'], out['judge_input_tokens'] = n, tin
    out['cost'] = {k: round(v, 3) for k, v in cost.items()}
    out['cost_total'] = round(sum(cost.values()), 3)
    blocks = archive.execute("select count(*) from model_calls where purpose='judge' and instr(request_json, '[Themes in force,')>0").fetchone()[0]
    out['requests_with_block'] = blocks
    return out, views, judgements, kind


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--control', required=True)
    ap.add_argument('--arm', required=True)
    ap.add_argument('--pairs', type=int, default=10)
    args = ap.parse_args()
    control, c_views, c_j, c_kind = summary(pathlib.Path(args.control))
    arm, a_views, a_j, a_kind = summary(pathlib.Path(args.arm))
    keys = ['theses', 'theme_theses', 'judgements', 'asset_judgements', 'requests_with_block', 'with_theme_push', 'propagation_only', 'propagation_only_changed', 'rung_moves', 'judge_calls', 'judge_input_tokens', 'cost', 'cost_total']
    print('| | r4 control (poc-v26) | r5 arm (poc-v29) |\n|---|---|---|')
    for k in keys:
        print(f'| {k} | {control.get(k)} | {arm.get(k)} |')
    # the same question in both ledgers: last reasons side by side
    def last_by_question(views, judgements, kind):
        q = {r['view_id']: (r['object_id'], r['question']) for r in views.execute('select view_id, object_id, question from views')}
        out = {}
        for j in judgements:
            if kind[j['view_id']] == 'company':
                out[q[j['view_id']]] = j
        return out
    c_last, a_last = last_by_question(c_views, c_j, c_kind), last_by_question(a_views, a_j, a_kind)
    shared = [k for k in a_last if k in c_last]
    print(f'\nasset theses with the same question in both ledgers: {len(shared)}; first {args.pairs} with their last reasons:\n')
    for obj, question in shared[:args.pairs]:
        c, a = c_last[(obj, question)], a_last[(obj, question)]
        print(f'### {obj}: {question}\n- r4 rung {c["rung"]} ({c["publication_day"]}): {c["reasons"][:500]}\n- r5 rung {a["rung"]} ({a["publication_day"]}): {a["reasons"][:500]}\n- r5 theme pushes: {a.get("theme_pushes_json")}\n')


if __name__ == '__main__':
    main()
