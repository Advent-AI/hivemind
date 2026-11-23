"""Can the state of 2026-07-14 before that day's judging round be rebuilt and verified? ($0; D535, part b.) The stored frozen seeded draw
is rebuilt from its stored answers alone: the preset questions written by the seeding module as the stored run did, whole days through
the production replay (serial) to 2026-07-13, then the articles of 2026-07-14 through dispatch and the item's entry point without the
day's judging round. Every network call is refused. The rebuilt store is compared with the stored run table by table.

  python3 rebuild_seeded_state.py <scratch folder>
"""
import collections
import json
import shutil
import sqlite3
import sys
import threading
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'docs/research/2026-11-14-use-acceptance/duplicates')]
from hivemind import config, dispatch, model, replay, seeding, testdb, universe  # noqa: E402
from hivemind.views import round as rounds, store  # noqa: E402
import d375_proof  # noqa: E402  (its table reader: rows of a table up to a sequence, wall-clock columns set aside)

RUN = ROOT / 'poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
LAST_DAY, DAY_BEFORE = '2026-07-14', '2026-07-13'


SERVED = []
ARCHIVE_LOCK = threading.Lock()
STORED_ARCHIVE = sqlite3.connect(f"file:{RUN / 'archive.sqlite'}?mode=ro", uri=True, check_same_thread=False)


def refuse(*args, **kwargs):
    """No network. One kind of request is answered from the stored run itself: an answer the code's own check refused is archived
    under its request key with a ':refused:' suffix, so that a replay asks again instead of reusing it; here the stored refused
    reply is handed back as it was, the check refuses it again, and the retry that follows is found in the archive."""
    if len(args) == 2:
        key = model.request_identity(args[1])[1]
        with ARCHIVE_LOCK:                      # judging calls this from several threads; one connection is read by one thread at a time
            row = STORED_ARCHIVE.execute("select response_json from model_calls where request_sha256 like ? order by call_id limit 1", (key + ':refused:%',)).fetchone()
        if row:
            SERVED.append(key[:12])
            return json.loads(row[0])
    raise RuntimeError('a request was not in the stored archive: the network is refused in this rebuild')


def main():
    scratch = Path(sys.argv[1])
    if scratch.exists():
        shutil.rmtree(scratch)
    scratch.mkdir(parents=True)
    shutil.copy(RUN / 'archive.sqlite', scratch / 'archive.sqlite')
    cfg, uni = config.load(str(ROOT / 'poc/config/poc-v108.json')), universe.load(str(ROOT / 'poc/universe.json'))
    archive = model.Archive(str(scratch / 'archive.sqlite'))
    calls_before = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    ledger = store.open_db(str(scratch / 'views.sqlite'))
    written = seeding.seed_views(ledger, str(ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'), created_at='2026-07-01T00:00:00Z')
    ledger.commit()
    ledger.close()
    testdb_path = str(ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite')
    totals = replay.run(testdb_path=testdb_path, views_path=str(scratch / 'views.sqlite'), archive=archive, cfg=cfg, universe=uni, from_day='2026-07-01',
                        until_day=DAY_BEFORE, only_objects={'NVDA'}, transport=refuse, log=lambda *parts: None)
    conn = store.open_db(str(scratch / 'views.sqlite'))
    processed = 0
    for item in testdb.feed(testdb.open_db(testdb_path), LAST_DAY, LAST_DAY):       # the last day's articles, as the replay loop takes them, without the day's judging round
        if not any(o['value'] == 'NVDA' for o in item['object_identifiers']):
            continue
        route = dispatch.route(conn, item, uni)
        if route.kind != 'extract':
            if route.kind == 'merged':
                dispatch.mark(conn, item, 0, 'merged', 'ok', route.reason)
                conn.commit()
            continue
        result = rounds.run(conn, archive, cfg, uni, item, route.sequence_no, resume_from=route.resume_from, transport=refuse, log=lambda *parts: None)
        if result.failed:
            raise SystemExit(f'article {route.sequence_no} failed in the rebuild: {result.failed}')
        processed += 1
    conn.commit()
    conn.close()
    calls_after = sqlite3.connect(scratch / 'archive.sqlite').execute('select count(*) from model_calls').fetchone()[0]
    rebuilt = sqlite3.connect(f"file:{scratch / 'views.sqlite'}?mode=ro", uri=True)
    stored = sqlite3.connect(f"file:{RUN / 'views.sqlite'}?mode=ro", uri=True)
    top = rebuilt.execute('select max(sequence_no) from processing_steps').fetchone()[0]
    print(f"stored refused replies handed back from the archive: {len(SERVED)}")
    print(f"preset questions written {len(written)}; whole days to {DAY_BEFORE}: failed {totals.get('failed')}; articles of {LAST_DAY} processed {processed}; highest sequence {top} "
          f"(stored run: {stored.execute('select max(sequence_no) from processing_steps').fetchone()[0]}); archive rows {calls_before} -> {calls_after}")
    views = {row[0] for row in stored.execute('select view_id from views')}
    groups = {row[0] for row in stored.execute('select group_id from thesis_groups')}
    differing = []
    for table in d375_proof.tables_of(stored):
        ours, kept, _, rule = d375_proof.rows_of(rebuilt, table, top, views, groups)
        theirs, _, _, _ = d375_proof.rows_of(stored, table, top, views, groups)
        strip = [i for i, c in enumerate(kept) if c == 'id']
        ours = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in ours)
        theirs = collections.Counter(tuple(v for i, v in enumerate(r) if i not in strip) for r in theirs)
        if ours != theirs:
            only_ours, only_theirs = ours - theirs, theirs - ours
            differing.append(table)
            sample = [dict(zip([c for c in kept if c != 'id'], row)) for row in list(only_theirs)[:2]]
            print(f"  {table}: {sum(only_ours.values())} rows only rebuilt, {sum(only_theirs.values())} only stored; e.g. only stored: {str(sample)[:330]}")
    print('tables that differ by content:', differing or 'none')


if __name__ == '__main__':
    main()
