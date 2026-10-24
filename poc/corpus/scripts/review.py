"""Review the assembled corpus and write manifest.md: counts per day and class, sources, body coverage by domain,
empty days, the big price-move days and their coverage, the Google News cross-check, copies before and after,
and a random sample of 30 news items for a human read (sample.md).
"""
import collections
import csv
import json
import os
import random
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT, RAW, WINDOW_START, WINDOW_END, read_json, days_between, log, main_guard  # noqa: E402
from assemble import normalise_title  # noqa: E402

DB = os.path.join(ROOT, 'items.sqlite')
PRICES = os.path.join(RAW, 'prices', 'nvda-daily.csv')
SEED = 20261023


def query(conn, sql, *args):
    return conn.execute(sql, args).fetchall()


def big_moves():
    moves = []
    if not os.path.exists(PRICES):
        return moves
    rows = list(csv.DictReader(open(PRICES)))
    for before, after in zip(rows, rows[1:]):
        if WINDOW_START <= after['day'] <= WINDOW_END and before['close'] and after['close']:
            change = float(after['close']) / float(before['close']) - 1
            if abs(change) >= 0.04:
                moves.append((after['day'], round(change * 100, 1)))
    return moves


def gnews_cross_check(conn):
    """Share of Google News headlines per day whose normalised title also appears in the corpus that day or the next."""
    titles = collections.defaultdict(set)
    for day, title in query(conn, "select publication_day, title from items where klass='新闻'"):
        titles[day].add(normalise_title(title))
    results = []
    gdir = os.path.join(RAW, 'gnews')
    for day in days_between(WINDOW_START, WINDOW_END):
        record = read_json(os.path.join(gdir, day + '.json'))
        if not record:
            continue
        total = hit = 0
        for entry in record['items']:
            headline = normalise_title(re.sub(r'\s+-\s+[^-]+$', '', entry['title']))
            if len(headline) < 20:
                continue
            total += 1
            pool = titles.get(day, set()) | titles.get(next_day(day), set())
            if any(headline[:50] in t or t[:50] in headline for t in pool if t):
                hit += 1
        results.append((day, total, hit))
    return results


def codex_events():
    """(day, event) rows from the research checklist's first table; a checklist for coverage, never fed."""
    path = os.path.join(ROOT, '..', '..', 'docs', 'research', '2026-10-23-poc-corpus', 'codex-events.md')
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding='utf-8') as handle:
        for line in handle:
            match = re.match(r'\|\s*(\d{2})-(\d{2})\s*\|\s*(.*?)\s*\|\s*([CORT])\s*\|', line)
            if match:
                rows.append((f'2026-{match.group(1)}-{match.group(2)}', f'[{match.group(4)}] {match.group(3)}'))
    return rows


def next_day(day):
    import datetime
    return (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat()


def run():
    conn = sqlite3.connect(DB)
    out = []
    total, originals = query(conn, 'select count(*), sum(copy_of is null) from items')[0]
    out.append(f'# NVDA 素材库审视\n\n生成：{__import__("datetime").date.today().isoformat()}。窗口 {WINDOW_START} 到 {WINDOW_END}；开题用的更早材料另标。\n')
    out.append(f'总条数 {total}，去掉转载和重复后 {originals}。\n')
    out.append('## 每类多少条\n\n| 类 | 细标签 | 条数 | 其中原件 | 窗口内原件 |\n|---|---|---|---|---|')
    for klass, category, n, orig, inwin in query(conn, "select klass, category, count(*), sum(copy_of is null), sum(copy_of is null and bootstrap=0) from items group by klass, category order by klass, category"):
        out.append(f'| {klass} | {category} | {n} | {orig} | {inwin} |')
    out.append('\n## 按层和话题（原件；进管线 = 原件齐全的）\n\n| 层 | 话题 | 条数 | 进管线 | 正文完整 |\n|---|---|---|---|---|')
    for tier, topic, n, fed, full in query(conn, "select tier, topic, count(*), sum(feed), sum(coverage='full') from items where copy_of is null group by tier, topic order by tier, count(*) desc"):
        out.append(f'| {tier} | {topic} | {n} | {fed} | {full} |')
    out.append('\n## 讲的是哪个对象（原件，一条可以讲几个）\n\n| 对象 | 条数 | 进管线 |\n|---|---|---|')
    objects = collections.Counter()
    fed_objects = collections.Counter()
    for identifiers, feed in query(conn, "select object_identifiers, feed from items where copy_of is null"):
        for obj in json.loads(identifiers or '[]'):
            key = f'{obj.get("kind")}:{obj.get("value")}'
            objects[key] += 1
            if feed:
                fed_objects[key] += 1
    for key, n in objects.most_common():
        out.append(f'| {key} | {n} | {fed_objects[key]} |')
    out.append('\n## 来源\n\n| 来源 | 条数 | 原件 | 整页原文 | 空壳页 | 被拦 | 被截断 | 只有标题 | 只有供应商摘要 |\n|---|---|---|---|---|---|---|---|---|')
    for row in query(conn, "select source, count(*), sum(copy_of is null), sum(coverage='full'), sum(coverage='stub'), sum(coverage='blocked'), sum(coverage='truncated'), sum(coverage='title'), sum(coverage='provider_summary') from items group by source order by count(*) desc"):
        out.append('| ' + ' | '.join(str(v if v is not None else 0) for v in row) + ' |')
    out.append('\n## 每天多少条（窗口内，原件）\n\n| 日 | 新闻 | 公司材料 | 新闻正文完整 |\n|---|---|---|---|')
    per_day = {d: [0, 0, 0] for d in days_between(WINDOW_START, WINDOW_END)}
    for day, klass, coverage, n in query(conn, "select publication_day, klass, coverage, count(*) from items where copy_of is null and bootstrap=0 group by 1,2,3"):
        if day in per_day:
            per_day[day][0 if klass == '新闻' else 1] += n
            if klass == '新闻' and coverage == 'full':
                per_day[day][2] += n
    empty = [d for d, v in per_day.items() if v[0] == 0]
    for day, (news, company, full) in per_day.items():
        out.append(f'| {day} | {news} | {company} | {full} |')
    out.append(f'\n新闻为零的日子：{len(empty)} 天 {empty if empty else ""}\n')
    out.append('## 正文抓取按域名（新闻原件，前 40 个域名）\n\n| 域名 | 作者类型 | 条数 | 整页原文 | 空壳或被拦 | 只有标题 |\n|---|---|---|---|---|---|')
    for domain, kind, n, full, blocked, title_only in query(conn, "select publisher, publisher_type, count(*), sum(coverage='full'), sum(coverage in ('stub','blocked','truncated')), sum(coverage='title') from items where klass='新闻' and copy_of is null group by publisher order by count(*) desc limit 40"):
        out.append(f'| {domain} | {kind} | {n} | {full} | {blocked} | {title_only} |')
    out.append('\n## 进管线的有多少（整页原件才进）\n\n| 类 | 进管线 | 不进：只有标题 | 不进：只有供应商摘要 | 不进：空壳、被拦、截断 | 不进：其他 |\n|---|---|---|---|---|---|')
    for klass, fed, title_only, summary_only, bad_page, other in query(conn, "select klass, sum(feed), sum(coverage='title'), sum(coverage='provider_summary'), sum(coverage in ('stub','blocked','truncated')), sum(feed=0 and coverage not in ('title','provider_summary','stub','blocked','truncated')) from items where copy_of is null group by klass"):
        out.append(f'| {klass} | {fed} | {title_only} | {summary_only} | {bad_page} | {other} |')
    out.append('\n## 大事件在不在（Codex 网搜列的清单 + 申报日 + 股价大动的日子）\n')
    out.append('| 日 | 事 | 当天新闻原件 | 其中进管线 | 公司材料 |\n|---|---|---|---|---|')
    events = [('2026-08-26', 'Q2 FY27 财报、电话会、10-Q'), ('2026-09-03', '8-K（8.01）'), ('2026-08-17', '8-K（1.01、2.03、7.01）')]
    events += [(day, f'股价单日 {change:+.1f}%') for day, change in big_moves()]
    events += codex_events()
    seen = set()
    for day, what in sorted(events):
        if (day, what) in seen:
            continue
        seen.add((day, what))
        news, fed = query(conn, "select count(*), sum(feed) from items where klass='新闻' and copy_of is null and publication_day=?", day)[0]
        company = query(conn, "select group_concat(category || ' ' || substr(title,1,40), '；') from items where klass='公司材料' and publication_day=?", day)[0][0] or ''
        out.append(f'| {day} | {what[:70]} | {news} | {fed or 0} | {company[:120]} |')
    out.append('\n## Google News 标题对照（每天 100 条里，素材库里也有的占几成）\n\n| 日 | Google 标题数 | 对上的 | 占比 |\n|---|---|---|---|')
    checks = gnews_cross_check(conn)
    for day, total_g, hit in checks:
        out.append(f'| {day} | {total_g} | {hit} | {hit / total_g:.0%} |' if total_g else f'| {day} | 0 | 0 | - |')
    if checks:
        all_total = sum(t for _, t, _ in checks)
        all_hit = sum(h for _, _, h in checks)
        out.append(f'\n合计 {all_hit}/{all_total} = {all_hit / all_total:.0%}（对照的是标题前 50 个字符，粗略）\n')
    out.append('## 开题用的更早材料（窗口前）\n\n| 日 | 细标签 | 标题 | 字符 |\n|---|---|---|---|')
    for day, category, title, chars in query(conn, "select publication_day, category, substr(title,1,60), text_chars from items where bootstrap=1 order by publication_day"):
        out.append(f'| {day} | {category} | {title} | {chars} |')
    out.append('\n## 蹭热度的标题（粗数：标题含 "forget nvidia"、"instead of nvidia"、"better than nvidia"、"vs. nvidia"、"the next nvidia"）\n')
    noisy = query(conn, "select count(*) from items where klass='新闻' and copy_of is null and (lower(title) like '%forget nvidia%' or lower(title) like '%instead of nvidia%' or lower(title) like '%better than nvidia%' or lower(title) like '%vs. nvidia%' or lower(title) like '%the next nvidia%' or lower(title) like '%nvidia rival%')")[0][0]
    out.append(f'{noisy} 条，占新闻原件的 {noisy / max(originals, 1):.0%}（只是下限）。\n')
    with open(os.path.join(ROOT, 'manifest.md'), 'w', encoding='utf-8') as handle:
        handle.write('\n'.join(out) + '\n')
    sample_rows = query(conn, "select input_id, publication_day, publisher, coverage, title, substr(text, 1, 700) from items where klass='新闻' and copy_of is null and bootstrap=0")
    random.Random(SEED).shuffle(sample_rows)
    with open(os.path.join(ROOT, 'sample.md'), 'w', encoding='utf-8') as handle:
        handle.write(f'# 随机 30 条新闻（种子 {SEED}）\n\n')
        for input_id, day, publisher, coverage, title, text in sample_rows[:30]:
            handle.write(f'## {day} · {publisher} · {coverage} · {input_id}\n\n**{title}**\n\n{text}\n\n---\n\n')
    log('manifest.md and sample.md written')


if __name__ == '__main__':
    main_guard(run)
