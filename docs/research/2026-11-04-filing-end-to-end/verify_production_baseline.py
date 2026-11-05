"""$0 verification of the product's coverage-start reading (production-design.md, "$0 verification before any paid run", items 1-4): the product
step (`hivemind.baseline.run`, configuration poc-v116) on a new ledger seeded with the 22 seed questions, coverage start 2026-07-01, with a
transport that serves the stored answers of the validated third-version reading (baseline-v3-reading.json, each of its three sends in turn):
  1. every request the product sends is, byte for byte as the transport serializes it, a request of the validated builder (baseline_all.build(3));
     a request with its schema keys reordered is the negative control (same archive key, different bytes);
  2. the records and links it writes equal what the validated reading kept, re-checked with the product's check (per question: the set of item and
     quote), and the step's record lists the same refused figures;
  3. the first day's round would judge exactly the questions it linked (round.changed_views_of_day);
  4. the service and the bundles show the seeded questions and the records from the coverage-start day, not before.
Sends nothing.

usage: python3 verify_production_baseline.py
"""
import json
import os
import sys
import tempfile

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/scripts', HERE]
import baseline_all  # noqa: E402
from hivemind import baseline, bundle, config, model, seeding, service, testdb  # noqa: E402
from hivemind.views import round as round_module, store  # noqa: E402

SEED = f'{ROOT}/poc/seeds/nvda-2026-07-01-v2.json'
ITEMS = f'{ROOT}/poc/data/items-nvda-2026-07-01-10-27.sqlite'
START = '2026-07-01'
FIELDS = ('quote', 'value', 'unit', 'period', 'basis', 'one_line')


def main():
    cfg = config.load(f'{ROOT}/poc/config/poc-v116.json')
    reading = json.load(open(f'{HERE}/baseline-v3-reading.json'))
    _, report, texts, validated = baseline_all.build(3)
    by_bytes = {json.dumps(body): key for key, body in validated.items()}
    # 1 (negative control): a reordered schema keeps the archive key and changes the bytes
    some_key, some_body = next(iter(validated.items()))
    reordered = json.loads(json.dumps(some_body))
    schema = reordered['response_format']['json_schema']['schema']
    reordered['response_format']['json_schema']['schema'] = dict(reversed(list(schema.items())))
    assert model.request_identity(reordered)[1] == model.request_identity(some_body)[1], 'the control should share the archive key'
    assert json.dumps(reordered) not in by_bytes, 'the byte comparison must catch a reordered schema'
    print('1. negative control: a reordered schema shares the archive key and is caught by the byte comparison')
    failures = 0
    for n in range(3):
        sent = []

        def transport(provider, request):
            key = by_bytes.get(json.dumps(request))
            if key is None:
                raise AssertionError('the product sent a request that is not byte-equal to a validated one')
            sent.append(key)
            view_id, input_id = key
            raw = [{k: f.get('quote_as_written', f[k]) if k == 'quote' else f[k] for k in FIELDS} for f in reading['results'][view_id][input_id][n]['figures']]
            return {'choices': [{'message': {'content': json.dumps({'figures': raw}, ensure_ascii=False)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}

        with tempfile.TemporaryDirectory() as tmp:
            conn = store.open_db(os.path.join(tmp, 'views.sqlite'))
            seeding.seed_views(conn, SEED, created_at=f'{START}T00:00:00Z')
            archive = model.Archive(os.path.join(tmp, 'archive.sqlite'))
            record = baseline.run(conn, testdb.open_db(ITEMS), archive, cfg, ticker='NVDA', coverage_start=START, transport=transport, log=lambda *a: None)
            # 1
            ok1 = sorted(sent) == sorted(validated)
            # 2: expected = the validated answers re-checked with the product's check
            expected, expected_refused = {}, []
            for (view_id, input_id) in validated:
                raw = [{k: f.get('quote_as_written', f[k]) if k == 'quote' else f[k] for k in FIELDS} for f in reading['results'][view_id][input_id][n]['figures']]
                for f in baseline.check_figures(raw, texts[input_id]):
                    if f['kept']:
                        expected.setdefault(view_id, set()).add((input_id, baseline.comparable(f['quote'])))
                    else:
                        expected_refused.append((view_id, input_id, f['quote'][:300]))
            written = {}
            for row in conn.execute('select l.view_id, s.input_id, e.quote from evidence_links l join evidence e on e.evidence_id=l.evidence_id '
                                    'join evidence_sources s on s.evidence_id=e.evidence_id'):
                written.setdefault(row['view_id'], set()).add((row['input_id'], baseline.comparable(row['quote'])))
            refused = sorted((r['view_id'], r['input_id'], r['quote']) for r in record['refused'])
            ok2 = written == expected and refused == sorted(expected_refused)
            # 3
            ok3 = round_module.changed_views_of_day(conn, START) == set(record['changed']) and set(record['changed']) == set(written)
            # 4
            seq_day = service.seq_day_map(conn)
            first_view = record['changed'][0]
            visible_now = service.view_exists(conn, store.view(conn, first_view), START)
            visible_before = service.view_exists(conn, store.view(conn, first_view), '2026-06-30')
            items_db = testdb.open_db(ITEMS)
            shown_now = bundle.thesis_bundles(conn, items_db, [first_view], START)['views'][0]['evidence']
            try:
                bundle.thesis_bundles(conn, items_db, [first_view], '2026-06-30')
                hidden_before = False
            except KeyError:
                hidden_before = True
            records_of_view = {r[0] for r in conn.execute('select evidence_id from evidence_links where view_id=?', (first_view,))}
            pieces_now = [p for p in shown_now if p['id'] in records_of_view]
            ok4 = visible_now and not visible_before and seq_day.get(0) == START and hidden_before and len(pieces_now) == len(records_of_view) \
                and all(p['day'] for p in pieces_now)
            evidence_count = conn.execute('select count(*) from evidence').fetchone()[0]
            print(f'send {n}: requests byte-equal {ok1} ({len(sent)}); records equal {ok2} ({evidence_count} records over {len(written)} questions, '
                  f'{len(refused)} refused); first-day round {ok3}; service shows from coverage start {ok4} (seq 0 -> {seq_day.get(0)}, '
                  f'bundle pieces {None if pieces_now is None else len(pieces_now)})')
            if not (ok1 and ok2 and ok3 and ok4):
                failures += 1
                print('   written minus expected:', {v: written.get(v, set()) - expected.get(v, set()) for v in set(written) | set(expected) if written.get(v, set()) != expected.get(v, set())})
            conn.close()
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()
