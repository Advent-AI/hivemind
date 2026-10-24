#!/usr/bin/env python3
"""The stack-side day-0 step: map each belief sentence onto the day-0 snapshot of the views database, record the
mapping, and set the personas' exit conditions. Then (or later, after more replay days) scan for events.

  python3 scripts/agent_day0.py map   [--snapshot poc/data/views.sqlite.day0.sqlite] [--beliefs poc/eval/beliefs.csv]
  python3 scripts/agent_day0.py set   --user alex --view v3 --rung 4 --action 清掉 --belief "数据中心需求撑到年底"
  python3 scripts/agent_day0.py scan  [--views poc/data/views.sqlite]
  python3 scripts/agent_day0.py card  --user alex --view v3
"""
import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'poc'))
from hivemind import config, model  # noqa: E402
from hivemind.views import store  # noqa: E402
from agent import beliefs, card, conditions  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['map', 'set', 'scan', 'card'])
    parser.add_argument('--snapshot', default=os.path.join(ROOT, 'poc', 'data', 'views.sqlite.day0.sqlite'))
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'views.sqlite'))
    parser.add_argument('--agent', default=os.path.join(ROOT, 'poc', 'data', 'agent.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'agent-archive.sqlite'))
    parser.add_argument('--config', default=os.path.join(ROOT, 'poc', 'config', 'poc-v1.json'))
    parser.add_argument('--beliefs', default=os.path.join(ROOT, 'poc', 'eval', 'beliefs.csv'))
    parser.add_argument('--objects', default='NVDA')
    parser.add_argument('--user'); parser.add_argument('--view'); parser.add_argument('--rung', type=int)
    parser.add_argument('--action'); parser.add_argument('--belief', default=''); parser.add_argument('--day', default='')
    args = parser.parse_args()
    conn_agent = conditions.open_db(args.agent)
    if args.command == 'map':
        cfg = config.load(args.config)
        archive = model.Archive(args.archive)
        snapshot = store.open_read_only(args.snapshot)
        rows = list(csv.DictReader(open(args.beliefs, encoding='utf-8')))
        out_path = os.path.join(ROOT, 'poc', 'eval', 'mappings.csv')
        with open(out_path, 'w', encoding='utf-8', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(['user', 'sentence', 'mapped_view_id', 'mapped_question', 'difference', 'nearest', 'settlement_day', 'gold_view_id', 'gold_is_none'])
            for row in rows:
                mapping = beliefs.map_sentence(snapshot, archive, cfg, row['sentence'], args.objects.split(','))
                conditions.record_mapping(conn_agent, row['user'], mapping)
                question = store.view(snapshot, mapping['view_id'])['question'] if mapping['view_id'] else ''
                writer.writerow([row['user'], row['sentence'], mapping['view_id'] or 'none', question, mapping['difference'], ' '.join(mapping['nearest']),
                                 mapping['settlement_day'] or '', row.get('gold_view_id', ''), row.get('gold_is_none', '')])
                print(f'{row["user"]:6s} → {mapping["view_id"] or "none":5s} | {row["sentence"][:36]} | {question[:50]} | 差别：{mapping["difference"][:90]}')
        print('written', out_path)
    elif args.command == 'set':
        views = store.open_read_only(args.views)
        seq = store.next_sequence(views) - 1
        condition_id = conditions.set_condition(conn_agent, args.user, args.view, args.rung, args.action, seq, args.day, args.belief)
        print('condition', condition_id, 'set after seq', seq)
    elif args.command == 'scan':
        views = store.open_read_only(args.views)
        events = conditions.scan(views, conn_agent, 0)
        print(f'{len(events)} new events')
        for e in events:
            print(json.dumps(e, ensure_ascii=False))
        for row in conn_agent.execute('select kind, user, view_id, publication_day, rung_before, rung_after, action, cited_json from events order by event_id'):
            cited = json.loads(row['cited_json'])
            print(f'\n[{row["kind"]}] {row["publication_day"]} {row["user"]} {row["view_id"]}: 第 {row["rung_before"]} 格 → 第 {row["rung_after"]} 格 {row["action"]}')
            for c in cited[:3]:
                print(f'   {c["tier"]} · {c["publication_day"]} · {c["one_line"][:120]}\n      原句：{c["quote"][:200]}')
    elif args.command == 'card':
        views = store.open_db(args.views)
        print(card.render(views, conn_agent, args.user, args.view))


if __name__ == '__main__':
    main()
