"""Cheapest paid proof of extraction v72 (design-v72.md §4 step 2; AGENTS §1 step 4): rebuild named articles' extraction requests under
a one-decider configuration from a finished run's ledger (the day-start snapshot that ledger held when the article's day began, with
its takes lines), send each n times, run every code check and the v72 filing on each answer, and print, per send, every statement
with the questions it is filed under (the view id and its looks_at), the candidates, and the no-home drops, marking the statements
whose quote carries a named fragment (the class under test); then the stored outcome of the same article in that run (the control:
what reached the ledger and under which questions, what was dropped). About $0.004 a send.

    python3 resend_extract_v72.py <run folder> <config json> <n> --match TITLE... [--span FRAGMENT...] [--items ITEMS_DB]
"""
import argparse
import json
import shutil
import sqlite3
import sys
import tempfile
import types
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

SENDERS = 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run'); ap.add_argument('config'); ap.add_argument('n', type=int)
    ap.add_argument('--match', nargs='+', required=True, help='article title fragments (case-insensitive)')
    ap.add_argument('--span', nargs='*', default=[], help='quote fragments that mark the statements under test')
    ap.add_argument('--items', default=str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    args = ap.parse_args()
    cfg = config.load(args.config)
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    scratch = Path(tempfile.mkdtemp(prefix='v72-proof-'))
    shutil.copy(Path(args.run) / 'views.sqlite', scratch / 'views.sqlite')          # never the run's own ledger
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    control = sqlite3.connect(f'file:{args.run}/views.sqlite?mode=ro', uri=True); control.row_factory = sqlite3.Row
    items_db = testdb.open_db(args.items)
    wanted = [m.lower() for m in args.match]; marks = [s.lower() for s in args.span]
    days = [r[0] for r in control.execute('select day from days_completed order by day')]
    articles = [it for it in testdb.feed(items_db, days[0], days[-1]) if any(w in (it.get('title') or '').lower() for w in wanted)]
    print(f'articles {len(articles)}; config {cfg.version}; n {args.n} sends each; snapshot from {args.run}', flush=True)

    def looks(view_id):
        row = control.execute('select looks_at from views where view_id=?', (view_id,)).fetchone()
        return row[0][:70] if row else '?'

    def send(body):
        content = model.openai_transport(cfg.provider, body)['choices'][0]['message']['content']
        return json.loads(content)

    jobs = []
    with ThreadPoolExecutor(SENDERS) as pool:
        for item in articles:
            objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
            shown = extraction.shown_views(ledger, cfg, item, objects)
            setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
            body = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
            futures = [pool.submit(send, body) for _ in range(args.n)]
            jobs.append((item, shown, user, schema, futures))
        for item, shown, user, schema, futures in jobs:
            shown_ids = {v['view_id'] for v in shown}
            print(f"\n## {item['publication_day']} | {item['title']}")
            print(f"   snapshot: {len(shown)} open questions; request {len(user):,} chars; links definition in schema: "
                  f"{'yes' if schema['properties']['evidence']['items']['properties']['links'].get('description') else 'no'}")
            for number, future in enumerate(futures, 1):
                data = future.result()
                evidence, candidates, dropped, new_groups = extraction.sift_with_groups(data, item, item['text'], shown_ids, uni, english=True, version='v72', keep_unlinked=True)
                reading = extraction.Reading(evidence, candidates, dropped, new_groups, types.SimpleNamespace(cost_usd=0.0, cached=False, call_id=0, request_sha256=''), 'v72')
                handover = extraction.file_reading(reading, None, cfg, item, shown)
                filed = {e['id']: e for e in handover.evidence}
                written = data.get('evidence', [])
                to_open = sum(1 for e in filed.values() if any(l in shown_ids for l in e['links']))
                print(f"### send {number}: {len(written)} statements written, {len(filed)} filed ({to_open} to open questions), "
                      f"{sum(1 for _, r in handover.dropped if r == 'no home')} no home, {len(handover.candidates)} candidates kept of {len(data.get('candidates', []))}")
                for c in handover.candidates:
                    print(f"      candidate {c['id']}: {c.get('question', '')[:110]}")
                for e in written:
                    mark = '<<' if any(m in (e.get('quote') or '').lower() for m in marks) else '  '
                    state = filed.get(e['id'])
                    links = ', '.join(f"{l} ({looks(l)})" if l in shown_ids else l for l in (state['links'] if state else [])) if state else next((r for i, r in handover.dropped if i == e['id']), 'dropped')
                    print(f"  - {e['id']} {mark} [{links}] | {(e.get('quote') or '')[:100]}")
            stored = [dict(r) for r in control.execute('select evidence_id, quote from evidence where created_from_input=? order by evidence_id', (item['input_id'],))]
            h = control.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (item['input_id'],)).fetchone()
            dropped_stored = json.loads(h[0]).get('dropped', []) if h else []
            print(f"### control (stored in {Path(args.run).name}): {len(stored)} statements reached the ledger, {sum(1 for _, r in dropped_stored if r == 'no home')} dropped no home")
            for s in stored:
                links = [r[0] for r in control.execute('select view_id from evidence_links where evidence_id=? order by id', (s['evidence_id'],))]
                mark = '<<' if any(m in (s['quote'] or '').lower() for m in marks) else '  '
                print(f"  - {s['evidence_id']} {mark} [{', '.join(f'{l} ({looks(l)})' for l in links)}] | {(s['quote'] or '')[:100]}")
    shutil.rmtree(scratch, ignore_errors=True)


if __name__ == '__main__':
    main()
