#!/usr/bin/env python3
"""The POC report, from the views database, the agent database and the archive:
timeline.md (every view's judgements with citations), events.md, hindsight-reviewer.csv (one row per item that
produced evidence, no states) and hindsight-key.csv (with states), beliefs.md (mapped versus gold), cost.md,
limits.md. The reviewer file is for a person blind to the states; the key joins their marks afterwards.

  python3 scripts/report.py [--out poc/reports/<date>]
"""
import argparse
import csv
import datetime
import json
import os
import random
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind.views import store  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--views', default=os.path.join(ROOT, 'poc', 'data', 'views.sqlite'))
    parser.add_argument('--agent', default=os.path.join(ROOT, 'poc', 'data', 'agent.sqlite'))
    parser.add_argument('--archive', default=os.path.join(ROOT, 'poc', 'data', 'archive.sqlite'))
    parser.add_argument('--testdb', default=os.path.join(ROOT, 'poc', 'corpus', 'items.sqlite'))
    parser.add_argument('--out', default=os.path.join(ROOT, 'poc', 'reports', datetime.date.today().isoformat()))
    parser.add_argument('--seed', type=int, default=20261023)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    conn = store.open_db(args.views)
    items = sqlite3.connect(args.testdb); items.row_factory = sqlite3.Row

    # timeline
    lines = ['# 每条观点的时间线\n']
    for v in conn.execute('select * from views order by created_seq'):
        rungs = store.rungs_of(conn, v['view_id'])
        lines.append(f'## {v["view_id"]} · {v["object_id"]} · {v["question"]}\n\n到期 {v["due_day"]}；{"开着" if store.is_open(conn, v["view_id"]) else "关了"}；梯子：' + ' / '.join(f'{r["position"]} {r["label"]}：{r["condition"]}' for r in rungs) + '\n')
        lines.append('| 日 | 格 | 变了 | 依据的证据 | 为什么变 |\n|---|---|---|---|---|')
        for j in conn.execute('select * from judgements where view_id=? order by judgement_id', (v['view_id'],)):
            cited = json.loads(j['cited_evidence_json'] or '[]')
            quotes = '；'.join(f'{c}' for c in cited[:6])
            lines.append(f'| {j["publication_day"]} | {j["rung"]} {rungs[j["rung"] - 1]["label"]} | {"是" if j["changed"] else ""} | {quotes} | {(j["why_changed"] or "")[:80]} |')
        lines.append('')
    open(os.path.join(args.out, 'timeline.md'), 'w', encoding='utf-8').write('\n'.join(lines))

    # events
    lines = ['# 事件（判断变了 / 碰到出场条件）\n']
    if os.path.exists(args.agent):
        agent = sqlite3.connect(args.agent); agent.row_factory = sqlite3.Row
        for e in agent.execute('select * from events order by event_id'):
            cited = json.loads(e['cited_json'])
            lines.append(f'## [{e["kind"]}] {e["publication_day"]} · {e["user"]} · {e["view_id"]} · 第 {e["rung_before"]} 格 → 第 {e["rung_after"]} 格 {e["action"]}\n')
            for c in cited[:4]:
                lines.append(f'- {c["tier"]} · {c["publication_day"]} · {c["input_id"]}\n  {c["one_line"]}\n  > {c["quote"][:300]}\n')
    open(os.path.join(args.out, 'events.md'), 'w', encoding='utf-8').write('\n'.join(lines))

    # hindsight worksheet: every item that produced evidence, plus 10% of the rest that were fed
    produced = {}
    for row in conn.execute('select s.input_id, s.publication_day, e.one_line, l.view_id from evidence_sources s join evidence e on e.evidence_id=s.evidence_id join evidence_links l on l.evidence_id=e.evidence_id and l.seq=s.seq'):
        produced.setdefault(row['input_id'], {'day': row['publication_day'], 'lines': [], 'views': set()})
        produced[row['input_id']]['lines'].append(row['one_line'])
        produced[row['input_id']]['views'].add(row['view_id'])
    fed = [dict(r) for r in items.execute("select input_id, publication_day, title from items where feed=1 and copy_of is null and publication_day >= '2026-07-24'")]
    rest = [r for r in fed if r['input_id'] not in produced]
    random.Random(args.seed).shuffle(rest)
    sample_rest = rest[:max(1, len(rest) // 10)]
    changed_days = {}
    for j in conn.execute('select view_id, publication_day, changed, rung from judgements order by judgement_id'):
        changed_days.setdefault((j['view_id'], j['publication_day']), []).append((j['rung'], j['changed']))
    with open(os.path.join(args.out, 'hindsight-reviewer.csv'), 'w', encoding='utf-8', newline='') as rev, \
            open(os.path.join(args.out, 'hindsight-key.csv'), 'w', encoding='utf-8', newline='') as key:
        w1, w2 = csv.writer(rev), csv.writer(key)
        w1.writerow(['day', 'input_id', 'title', 'evidence_one_lines', 'views_linked', 'should_have_moved(填 是/否)', 'which_view', 'note'])
        w2.writerow(['day', 'input_id', 'views_linked', 'judgements_that_day(view:rung:changed)'])
        for input_id, info in sorted(produced.items(), key=lambda kv: kv[1]['day']):
            title = items.execute('select title from items where input_id=?', (input_id,)).fetchone()
            w1.writerow([info['day'], input_id, (title[0] if title else '')[:100], ' ｜ '.join(info['lines'])[:1500], ' '.join(sorted(info['views'])), '', '', ''])
            w2.writerow([info['day'], input_id, ' '.join(sorted(info['views'])), ' '.join(f'{v}:{r}:{c}' for v in sorted(info['views']) for r, c in changed_days.get((v, info['day']), []))])
        for r in sample_rest:
            w1.writerow([r['publication_day'], r['input_id'], (r['title'] or '')[:100], '（没有抽出证据）', '', '', '', ''])
            w2.writerow([r['publication_day'], r['input_id'], '', ''])

    # beliefs
    path = os.path.join(ROOT, 'poc', 'eval', 'mappings.csv')
    lines = ['# 落题：20 句话落到哪个问题\n', '| 谁 | 原话 | 落到 | 问题 | 差别 | 到期 | 金标 |', '|---|---|---|---|---|---|---|']
    if os.path.exists(path):
        for row in csv.DictReader(open(path, encoding='utf-8')):
            lines.append(f'| {row["user"]} | {row["sentence"][:40]} | {row["mapped_view_id"]} | {row["mapped_question"][:50]} | {row["difference"][:80]} | {row["settlement_day"]} | {row["gold_view_id"] or ("none" if row["gold_is_none"] else "")} |')
    open(os.path.join(args.out, 'beliefs.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # cost
    a = sqlite3.connect(args.archive)
    rows = a.execute('select purpose, count(*), round(sum(cost_usd),2), sum(input_tokens), sum(output_tokens), round(avg(seconds),1) from model_calls group by purpose').fetchall()
    total = a.execute('select count(*), round(sum(cost_usd),2) from model_calls').fetchone()
    lines = ['# 费用\n', '| 用途 | 次数 | 美元 | 输入 tokens | 输出 tokens | 平均秒 |', '|---|---|---|---|---|---|'] + [f'| {r[0]} | {r[1]} | {r[2]} | {r[3]:,} | {r[4]:,} | {r[5]} |' for r in rows] + [f'\n合计 {total[0]} 次，{total[1]} 美元。']
    open(os.path.join(args.out, 'cost.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    # limits
    open(os.path.join(args.out, 'limits.md'), 'w', encoding='utf-8').write(
        '# 这份结果的边界\n\n'
        '- 模型 gpt-6-luna 的知识截止日没有公开数；它可能知道窗口里后来发生的事。提示词禁止用外部知识，判断只能引用列出的证据，代码核过；但选格可能受影响。\n'
        '- 新闻正文是抓取当天的页面，发布后被改过的看不出来；TrueNorth 的新闻只用了目录，正文抓不到的没进管线。\n'
        '- 回放里一条信息发布当天就处理，延迟为零，不代表上线后的延迟。\n'
        '- 修正版（supersedes）的信息不处理，进复核池。\n'
        '- 同一天的抽取并行跑，看到的是当天开始时的观点；当天先开的观点由比对归入处理。\n'
        '- 被反爬拦住的站（Benzinga、Bloomberg、Reuters、WSJ、FT）没有正文，它们报的事只在别家转述里。\n')
    print('report written to', args.out)


if __name__ == '__main__':
    main()
