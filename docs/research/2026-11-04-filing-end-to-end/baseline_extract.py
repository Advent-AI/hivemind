"""Step 1 of the coverage-start baseline (baseline-design.md, D363): the company's latest earnings release read by the frozen extraction as the
first item at coverage start. The request is built by the production code (`extraction.build_prompt`, the frozen v74i setting for the item's
category) with the questions open at the start of the release's day (`extraction.shown_views` on draw 1's ledger: the seeds, at sequence 0), from
the release's page text, which keeps the financial tables the cleaned text dropped. Answers go through the production checks and filing
(`resend_filing.file_like_production`).

usage: python3 baseline_extract.py check            (builds the request and prints it; sends nothing)
       python3 baseline_extract.py send <out.json>  (three sends)
"""
import concurrent.futures
import json
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts', HERE]
import resend_filing as rf  # noqa: E402
from hivemind import config, extraction, model, testdb, universe  # noqa: E402

RELEASE = 'edgar:NVDA:0001045810-26-000051:q1fy27pr.htm'
PAGES = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.page.sqlite'


def build():
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    uni = universe.load(f'{ROOT}/poc/universe.json')
    items = sqlite3.connect(f'file:{rf.ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    item = testdb.item_of(items.execute('select * from items where input_id=?', (RELEASE,)).fetchone())
    page_text = sqlite3.connect(f'file:{PAGES}?mode=ro', uri=True).execute('select text from items where input_id=?', (RELEASE,)).fetchone()[0]
    item = dict(item, text=page_text)
    setting = cfg.extraction_setting(item['category'])
    version = setting.prompt_version.rpartition('-')[2]
    views = sqlite3.connect(f'file:{rf.DRAW}/views.sqlite?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    objects = [o['value'] for o in item.get('object_identifiers') or []]
    shown = extraction.shown_views(views, cfg, item, objects)
    system, user = extraction.build_prompt(item, page_text, shown, uni, version)
    body = model.build_request(setting, system, user, extraction.schema_for(version), 'extraction', cfg.provider)
    return cfg, uni, item, shown, body


def main():
    cfg, uni, item, shown, body = build()
    shown_ids = [v['view_id'] for v in shown]
    parents = {v['view_id']: v['parents'] for v in shown}
    if sys.argv[1] == 'check':
        print(f'item {item["input_id"]} day {item["publication_day"]} category {item["category"]} objects {[o["value"] for o in item.get("object_identifiers") or []]}; '
              f'{len(item["text"])} characters of page text; questions shown {shown_ids}; request {len(json.dumps(body))} characters, key {model.request_identity(body)[1][:16]}')
        print(body['messages'][1]['content'])
        return
    out = sys.argv[2]

    def one(n):
        reply = model.openai_transport(cfg.provider, body, timeout=300)
        data = json.loads(reply['choices'][0]['message']['content'])
        kept, homeless, dropped, candidates = rf.file_like_production(data, item, shown_ids, parents, uni)
        usage = reply.get('usage') or {}
        return {'raw': data.get('evidence', []), 'kept': kept, 'homeless': homeless, 'dropped': dropped, 'candidates': candidates,
                'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]}

    with concurrent.futures.ThreadPoolExecutor(3) as pool:
        results = list(pool.map(one, range(3)))
    json.dump({'item': item['input_id'], 'request_sha256': model.request_identity(body)[1], 'sends': results}, open(out, 'w'), indent=1, ensure_ascii=False)
    for n, r in enumerate(results):
        print(f'\n--- send {n}: kept {len(r["kept"])}, no home {len(r["homeless"])}, refused {len(r["dropped"])}, candidates {r["candidates"]}, tokens {r["tokens"]}')
        for s in r['kept']:
            mark = '  <==' if set(s['links']) & {'v10', 'v12'} else ''
            print(f'   {s["links"]} [{s.get("tier")}] {s["one_line"][:150]}{mark}')
        for s in r['homeless']:
            print(f'   [no home] {s["one_line"][:150]}')
        for d in r['dropped']:
            print(f'   [refused] {d}')


if __name__ == '__main__':
    main()
