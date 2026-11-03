"""Renders gold-extraction.json as a Markdown table per article for reading and correction; the JSON stays the source."""
import json
D='/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-28-extraction-quality'
g=json.load(open(f'{D}/gold-extraction.json')); out=['# 抽取金标（渲染自 gold-extraction.json；改要改 JSON）\n', g['_about'], '']
for a in g['articles']:
    out.append(f"## {a['input_id']} · {a['day']} · {a['category']} · {'留出' if a['held_out'] else '开发'}")
    out.append(f"展示的论点：{', '.join(a['shown'])}；当时开放的主题：{', '.join(a['themes_open']) or '无'}")
    if a['statements']:
        out.append('\n| id | 分量 | 类 | 级别 | 说话人 | 现在挂 | 加主题后挂 | 原文片段 | 为什么 |\n|---|---|---|---|---|---|---|---|---|')
        for s in a['statements']:
            out.append(f"| {s['id']} | {s['weight']} | {s['kind']} | {s['tier']} | {s['who']} | {' '.join(s['bears_on_now']) or '—'} | {' '.join(s['bears_on_with_themes']) or '—'} | {s['span']}{(' ／ '+' ／ '.join(s['also'])) if s['also'] else ''} | {s['note']} |")
    else: out.append('\n金标为空（阴性对照）。')
    out.append(f"\n不进金标：{a.get('rejected_note','（无）')}\n")
open(f'{D}/gold-extraction.md','w').write('\n'.join(out)); print('rendered', sum(len(a['statements']) for a in g['articles']), 'statements')
