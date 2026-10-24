#!/usr/bin/env python3
"""Print what the views database holds, for a human read: every view with its ladder, state, evidence in force,
dependencies and history; the processing record; the review pool; the archive's cost.

  python3 scripts/show_views.py [--views poc/data/views.sqlite] [--archive poc/data/archive.sqlite] [--object NVDA]
"""
import argparse
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import store  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'views.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--object', default=None)
    parser.add_argument('--evidence', action='store_true', help='print every piece of evidence in force')
    args = parser.parse_args()
    conn = store.open_db(args.views)
    views = [dict(r) for r in conn.execute('select * from views order by created_seq')]
    if args.object:
        views = [v for v in views if v['object_id'] == args.object]
    print(f'{len(views)} views')
    for v in views:
        state = store.current_state(conn, v['view_id'])
        rungs = store.rungs_of(conn, v['view_id'])
        label = rungs[state['rung'] - 1]['label'] if state else '还没判'
        print(f'\n== {v["view_id"]} [{"开着" if store.is_open(conn, v["view_id"]) else "关了"}] {v["object_id"]} · {v["kind"]} · 看的是「{v["looks_at"]}」 · {v["year"] or ""} · 到期 {v["due_day"]} · 来自 {v["created_from_input"][:50]}')
        print(f'   问：{v["question"]}')
        print('   梯子：' + ' | '.join(f'{r["position"]} {r["label"]}：{r["condition"]}' for r in rungs))
        print(f'   状态：第 {state["rung"] if state else "-"} 格 {label}' + (f'；理由：{state["reasons"][:400]}' if state else ''))
        deps = store.dependencies_of(conn, v['view_id'])
        if deps:
            print('   依赖：' + '；'.join(f'{d["resolved_to"] or ("等 " + str(d["wait_chain_view_id"]) + " 的 " + str(d["wait_year"]))}（{d["direction"]}）' for d in deps))
        history = conn.execute('select publication_day, rung, changed, substr(why_changed,1,80) from judgements where view_id=? order by judgement_id', (v['view_id'],)).fetchall()
        if len(history) > 1:
            print('   历史：' + ' → '.join(f'{h[0]} 第{h[1]}格{"*" if h[2] else ""}' for h in history))
        pieces = store.evidence_in_force(conn, v['view_id'])
        print(f'   证据 {len(pieces)} 条' + ('：' if args.evidence else ''))
        if args.evidence:
            for p in pieces:
                src = p['sources'][0] if p['sources'] else {}
                print(f'     - {p["evidence_id"]} [{p["tier"]}] {p["one_line"][:140]}  ({src.get("publication_day")} {str(src.get("input_id"))[:40]})')
    print('\n== 处理记录')
    for row in conn.execute("select input_id, step, result, reason from processing_steps where step in ('handed_over','merged') or result='failed' order by id"):
        print(f'   {row["result"]:6s} {row["step"]:11s} {row["input_id"][:70]} {row["reason"][:80]}')
    pool = conn.execute('select kind, key, count(*) from review_pool_entries group by kind, key').fetchall()
    if pool:
        print('\n== 人工复核池')
        for row in pool:
            print(f'   {row[0]} · {row[1]} × {row[2]}')
    if os.path.exists(args.archive):
        a = sqlite3.connect(args.archive)
        calls, cost, tin, tout = a.execute('select count(*), coalesce(sum(cost_usd),0), coalesce(sum(input_tokens),0), coalesce(sum(output_tokens),0) from model_calls').fetchone()
        by_purpose = a.execute('select purpose, count(*), round(sum(cost_usd),3), round(avg(seconds),1) from model_calls group by purpose').fetchall()
        print(f'\n== 模型调用 {calls} 次，${cost:.2f}，输入 {tin:,} 输出 {tout:,} tokens；按用途：{by_purpose}')


if __name__ == '__main__':
    main()
