"""The held-out check: build the extraction request for an article no trial has used, from the paused run's ledger
(its open NVDA theses and groups as of its last day), with poc-v32's setting and a system prompt file, and send it
N times at low. Run: python3 fresh.py <arm> <system file> <universe json> <views.sqlite> <cleaned items db> <scratch archive> <N> <input_id>"""
import concurrent.futures
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '2026-10-27-evidence-gate'))
from hivemind import config, extraction, model, universe as universe_module  # noqa: E402
from hivemind.views import store  # noqa: E402
from benchmark import send  # noqa: E402
from pinned_arm import norm  # noqa: E402
from arm import OLD_CLOSING, NEW_CLOSING, T8_READ_OLD, T8_READ_NEW  # noqa: E402


def main(arm, system_file, universe_path, views_path, items_db, scratch, n, input_id):
    cfg = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v32.json'))
    uni = universe_module.load(universe_path)
    conn = store.open_db(views_path)
    items = sqlite3.connect(f'file:{items_db}?mode=ro', uri=True); items.row_factory = sqlite3.Row
    item = dict(items.execute('select * from items where input_id=?', (input_id,)).fetchone())
    item['object_identifiers'] = json.loads(item.get('object_identifiers') or '[]')
    objects = [o['value'] for o in item['object_identifiers'] if uni.has(o['value'])]
    shown = store.views_for_prompt(conn, objects)
    groups = store.groups_for_prompt(conn, objects, item.get('title') or '')
    setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni, groups)
    request = model.build_request(setting, open(system_file, encoding='utf-8').read(), user.replace(T8_READ_OLD, T8_READ_NEW), schema, 'extraction', cfg.provider)
    assert OLD_CLOSING not in request['messages'][1]['content']
    archive = model.Archive(scratch)
    print(f'{input_id}: {len(shown)} theses shown, {len(groups)} groups, user {len(user)} chars')
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(os.environ.get('ARM_WORKERS', '8'))) as pool:
        results = [pool.submit(send, archive, request, 'low', purpose=f'arm:{arm}') for _ in range(n)]
        results = [f.result() for f in results]
    for i, (pieces, reasoning, cost, seconds) in enumerate(results):
        print(f'  send {i+1}: {len(pieces)} pieces, reasoning {reasoning}, {seconds}s, ${cost:.4f}')
        for p in pieces:
            print(f"     [{p['tier'][:5]}] {','.join(p['links']) or '-':10} {p['one_line'][:120]}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], int(sys.argv[7]), sys.argv[8])
