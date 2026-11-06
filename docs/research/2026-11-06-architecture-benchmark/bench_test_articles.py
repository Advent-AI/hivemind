"""golden-v5 test (the frozen ruler's 30 held-out articles, 2026-09-01..10-24, outside the window) through each architecture's extraction stage
(plan-final C-8.1: extraction on dev and test). Both arms read the same questions: the 22 frozen seed questions of the fixture ledger (`bench_run.py`),
each arm by its own production rule (the frozen extraction: the item's objects' questions open at the start of its day, `extraction.shown_views`;
the split: every question open before the item, `split.latest_library`). Every article is read on its own against that fixture; a draw has its own
archive, so a draw re-sends every request. The checked handover of each article (what the extraction stage hands to matching) is stored for
`bench_measure.py --test`.

    PYTHONPATH=src python3 bench_test_articles.py --arm split|control --draw 1|2|3"""
import argparse
import concurrent.futures
import json
import os
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path[:0] = [os.path.join(ROOT, 'src'), HERE]
import bench_run  # noqa: E402
from hivemind import config, extraction, model, split, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

GOLD_TEST = '/Users/lchingen/hivemind/docs/research/2026-10-29-ledger-standard/golden-v5/golden-v5-test.json'
CONFIGS = {'split': os.path.join(ROOT, 'poc/config/poc-split-v3.json'), 'control': os.path.join(ROOT, 'poc/config/poc-v108.json')}


def fixture_copy():
    """An in-memory copy of the fixture ledger: a split article may write research subjects, and every article starts from the same ledger."""
    source = sqlite3.connect(f'file:{bench_run.fixture()}?mode=ro', uri=True)
    copy = sqlite3.connect(':memory:', check_same_thread=False)
    source.backup(copy)
    source.close()
    copy.row_factory = sqlite3.Row
    return copy


def one(arm, cfg, archive, row):
    item = testdb.item_of(row)
    uni = universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
    conn = fixture_copy()
    objects = [o['value'] for o in item.get('object_identifiers') or [] if uni.has(o['value'])]
    if arm == 'split':
        shown = split.latest_library(conn, 1)
        handover = split.extract(archive, cfg, item, item['text'], shown, uni, conn=conn, seq=1, log=lambda *a: None)
    else:
        shown = extraction.shown_views(conn, cfg, item, objects)
        handover = extraction.extract(archive, cfg, item, item['text'], shown, uni)
    return item['input_id'], {'evidence': handover.evidence, 'candidates': handover.candidates, 'dropped': [list(d) for d in handover.dropped],
                              'shown': [v['view_id'] for v in shown]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--arm', choices=sorted(CONFIGS), required=True)
    parser.add_argument('--draw', type=int, choices=(1, 2, 3), required=True)
    args = parser.parse_args()
    folder = os.path.join(HERE, 'runs', f'test-{args.arm}-d{args.draw}')
    os.makedirs(folder, exist_ok=True)
    out_path = os.path.join(folder, 'handovers.json')
    done = json.load(open(out_path)) if os.path.exists(out_path) else {}
    cfg = config.load(CONFIGS[args.arm])
    ids = [a['input_id'] for a in json.load(open(GOLD_TEST))['articles']]
    if bench_run.sha(bench_run.ITEMS) != bench_run.ITEMS_SHA256:
        raise SystemExit('the items database differs from the one the frozen ruler\'s draws read')
    items = testdb.open_db(bench_run.ITEMS)
    rows = [items.execute('select * from items where input_id=?', (i,)).fetchone() for i in ids if i not in done]
    missing = [i for i, r in zip([i for i in ids if i not in done], rows) if r is None]
    if missing:
        raise SystemExit(f'articles not in the items database: {missing}')
    manifest = {'arm': args.arm, 'draw': args.draw, 'config': CONFIGS[args.arm], 'config_version': cfg.version, 'fixture_sha256': bench_run.sha(bench_run.fixture()),
                'gold_test_sha256': bench_run.sha(GOLD_TEST), 'files_sha256': bench_run.pinned_files(CONFIGS[args.arm]), 'articles': len(ids)}
    manifest_path = os.path.join(folder, 'manifest.json')
    if os.path.exists(manifest_path):
        first = json.load(open(manifest_path))
        if {k: v for k, v in first.items() if k != 'resumed'} != manifest:
            raise SystemExit('refused: this draw began under other files or inputs; a resumed draw must run the same version; use a new folder')
        manifest['resumed'] = first.get('resumed', 0) + 1
    elif done or os.path.exists(os.path.join(folder, 'archive.sqlite')):
        raise SystemExit(f'{folder} holds answers without a manifest: use a new folder')
    json.dump(manifest, open(manifest_path, 'w'), indent=1)
    archive = model.Archive(os.path.join(folder, 'archive.sqlite'))
    failures = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(one, args.arm, cfg, archive, row): row['input_id'] for row in rows}
        for future in concurrent.futures.as_completed(futures):
            try:
                input_id, handover = future.result()
                done[input_id] = handover
                json.dump(done, open(out_path, 'w'), ensure_ascii=False)
            except Exception as error:
                failures.append((futures[future], repr(error)[:300]))
    print(f'{args.arm} d{args.draw}: {len(done)} of {len(ids)} articles handed over; failures {len(failures)}')
    for input_id, error in failures:
        print('  failed', input_id, error)
    print('TEST-DONE' if not failures and len(done) == len(ids) else 'TEST-INCOMPLETE')


if __name__ == '__main__':
    main()
