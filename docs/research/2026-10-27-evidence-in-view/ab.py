"""Arm beside control on three live theses (AGENTS §6): the same ledger state, judging-v4 (everything in force; a fresh
sample, not the stored answer) against judging-v5 (evidence in view). Answers go to a scratch archive in this folder.
Run: python3 ab.py <views.sqlite> <v4 config> <v5 config> <view ids...>"""
import json
import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402


def main(views_path, cfg4_path, cfg5_path, view_ids):
    conn = sqlite3.connect(f'file:{views_path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    archive = model.Archive(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ab-archive.sqlite'))
    rows = []
    for cfg_path in (cfg4_path, cfg5_path):
        cfg = config.load(cfg_path)
        version = cfg.rejudging.prompt_version
        for view_id in view_ids:
            system, user = judging.build_prompt(conn, view_id, version)
            answer = model.call(archive, cfg, cfg.rejudging, system, user, judging.schema_for(version), 'judgement', 'judge')
            errors = judging.check_answer(conn, view_id, answer.data, version, user)
            d = answer.data
            rows.append((view_id, version, len(user), answer.input_tokens, answer.output_tokens, answer.cost_usd, d['rung'], d['changed'], len(d['cites']), len(d['pushes']), errors, d['reasons'][:400].replace('\n', ' ')))
    print('| thesis | prompt | request chars | in tokens | out tokens | USD | rung | changed | cites | pushes | check |')
    print('|---|---|---|---|---|---|---|---|---|---|---|')
    for r in rows:
        print(f'| {r[0]} | {r[1]} | {r[2]:,} | {r[3]:,} | {r[4]:,} | {r[5]:.4f} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10] or "ok"} |')
    for r in rows:
        print(f'\n{r[0]} {r[1]}: {r[11]}')
    print(f'\ntotal USD {sum(r[5] for r in rows):.4f}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
