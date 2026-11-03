"""Cheapest paid proof of a text change aimed at one class of written noise (AGENTS §1 step 4): the gold not-kept statements of one row of
the standard that the stored v92 draws wrote. Picks the articles where that row's statements were written at least twice over the three
stored draws, rebuilds their extraction requests under a changed configuration from the v92 draw-1 snapshot, sends each three times, and
counts per article the row's statements written per send against the stored draws, with the guard: the gold core and supporting matters
of the same articles present per send against the stored draws (score_gold.same_matter). About $0.004 a send.

    python3 resend_noise_row.py <changed config> <v92 d1,d2,d3> --row "D250 第 1 条" [--items ITEMS_DB] [--max-articles 10]
"""
import argparse
import collections
import json
import shutil
import sqlite3
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

SENDERS = 8


def answer_of(archive, iid):
    r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
    return json.loads(r[0]).get('evidence', []) if r and r[0] else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('config'); ap.add_argument('base'); ap.add_argument('--row', required=True)
    ap.add_argument('--items', default=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')); ap.add_argument('--max-articles', type=int, default=10)
    args = ap.parse_args()
    cfg = config.load(args.config)
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    base_dirs = args.base.split(',')
    archives = [sqlite3.connect(f'file:{p}/archive.sqlite?mode=ro', uri=True) for p in base_dirs]
    stored = {}                                         # iid -> (row noise written per draw, core/supporting present per draw)
    for a in sr.articles:
        row_spans = [x for x in a['not_kept'] if x['weight'] == 'not_kept' and (x.get('row') or '').startswith(args.row)]
        matters = [it for it in a['items'] if it['weight'] in ('core', 'supporting')]
        if not row_spans:
            continue
        noise, kept = [], []
        for archive in archives:
            ev = answer_of(archive, a['input_id'])
            noise.append(sum(any(sr.sg.same(x['span'], e.get('quote') or '') for e in ev) for x in row_spans))
            kept.append(sum(any(sr.sg.same_matter(it, e) for e in ev) for it in matters))
        if sum(noise) >= 2:
            stored[a['input_id']] = (noise, kept, len(row_spans), len(matters))
    chosen = sorted(stored, key=lambda i: -sum(stored[i][0]))[:args.max_articles]
    scratch = Path(tempfile.mkdtemp(prefix='noise-proof-'))
    shutil.copy(Path(base_dirs[0]) / 'views.sqlite', scratch / 'views.sqlite')
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    items = {it['input_id']: it for it in testdb.feed(testdb.open_db(args.items), '2026-07-01', '2026-07-14') if it['input_id'] in chosen}
    by_id = {a['input_id']: a for a in sr.articles}
    print(f'row {args.row!r}: {len(stored)} articles wrote it at least twice over the stored draws; sending the top {len(chosen)} three times under {cfg.version}', flush=True)

    def send(body):
        return json.loads(model.openai_transport(cfg.provider, body)['choices'][0]['message']['content'])

    totals = collections.Counter()
    with ThreadPoolExecutor(SENDERS) as pool:
        jobs = []
        for iid in chosen:
            item = items[iid]
            objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
            shown = extraction.shown_views(ledger, cfg, item, objects)
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
            body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
            jobs.append((iid, [pool.submit(send, body) for _ in range(3)]))
        for iid, futures in jobs:
            a = by_id[iid]; noise_s, kept_s, n_row, n_matters = stored[iid]
            row_spans = [x for x in a['not_kept'] if x['weight'] == 'not_kept' and (x.get('row') or '').startswith(args.row)]
            matters = [it for it in a['items'] if it['weight'] in ('core', 'supporting')]
            noise_n, kept_n = [], []
            for f in futures:
                ev = f.result().get('evidence', [])
                noise_n.append(sum(any(sr.sg.same(x['span'], e.get('quote') or '') for e in ev) for x in row_spans))
                kept_n.append(sum(any(sr.sg.same_matter(it, e) for e in ev) for it in matters))
            totals['noise stored'] += sum(noise_s); totals['noise new'] += sum(noise_n); totals['kept stored'] += sum(kept_s); totals['kept new'] += sum(kept_n)
            print(f"\n## {a['publication_day']} | {a['title'][:70]}\n   row statements written: stored {noise_s} of {n_row} -> new {noise_n}; core+supporting present: stored {kept_s} of {n_matters} -> new {kept_n}")
    print(f"\nover {len(chosen)} articles x 3: row statements written {totals['noise stored']} -> {totals['noise new']}; core+supporting present {totals['kept stored']} -> {totals['kept new']}")
    shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    main()
