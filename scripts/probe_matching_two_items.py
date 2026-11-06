"""Replay two saved A handovers through matching and writing, updating the library between items."""
import copy
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import round as rounds, store  # noqa: E402

SOURCE = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/poc/data')
OUT = ROOT / 'poc/data/matching-identity-two-items-2026-11-05'


def latest_library(conn, before_sequence, objects):
    seq = before_sequence - 1
    shown = []
    for row in conn.execute('select view_id,object_id,object_kind,kind,looks_at,question,due_day,year,created_seq from views where created_seq<=? order by created_seq,view_id', (seq,)):
        view = dict(row)
        switch = conn.execute('select open from view_switches where view_id=? and after_seq<=? order by after_seq desc,id desc limit 1', (view['view_id'], seq)).fetchone()
        if not switch or not switch['open'] or (view['object_kind'] != 'theme' and view['object_id'] not in objects):
            continue
        key = store.view_key(conn, view['view_id']) or {}
        if key and key.get('seq', 0) > seq:
            key = {}
        view.update(snapshot_seq=seq, key=key,
                    groups=[{'name': g['name'], 'scope': g['scope'], 'aliases': g.get('aliases') or []} for g in store.groups_of_view_at(conn, view['view_id'], seq)],
                    parents=store.direct_parents(conn, view['view_id'], seq))
        shown.append(view)
    return shown


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    seed = SOURCE / 'pilot-d369-existing-library-v2/views.sqlite'
    with sqlite3.connect(seed.resolve().as_uri() + '?mode=ro', uri=True) as original, sqlite3.connect(OUT / 'views.sqlite') as target:
        original.backup(target)
    conn = store.open_db(str(OUT / 'views.sqlite'))
    if conn.execute('select count(*) from views').fetchone()[0] != 68:
        raise ValueError('unexpected starting library')
    saved = sqlite3.connect((SOURCE / 'split-fresh-seven-day-2026-11-05-v2/snapshot/views.sqlite').resolve().as_uri() + '?mode=ro', uri=True)
    items = testdb.open_db(str(SOURCE / 'parallel-thesis-evidence-input-2026-11-05/items.sqlite'))
    cfg = config.load(str(ROOT / 'poc/config/poc-v118-matching-identity.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    archive = model.Archive(str(OUT / 'archive.sqlite'))
    results = []
    for source_seq in (1209, 1213):
        input_id, raw = saved.execute('select input_id,handover_json from handovers where seq=?', (source_seq,)).fetchone()
        item = testdb.item_of(items.execute('select * from items where input_id=?', (input_id,)).fetchone())
        data = json.loads(raw)
        if len(data['candidates']) != 1:
            raise ValueError('unexpected saved candidate count')
        candidate = data['candidates'][0]
        evidence = [e for e in data['evidence'] if candidate['id'] in e['links']]
        if not evidence or any(e['quote'] not in item['text'] for e in evidence):
            raise ValueError('saved candidate evidence absent from source')
        handover = extraction.Handover(evidence, [candidate], [], 0, '', False, 0.0)
        seq = store.next_sequence(conn)
        shown = latest_library(conn, seq, ['NVDA'])
        if results and results[0]['new_id'] not in {v['view_id'] for v in shown}:
            raise ValueError('first written question missing from next item snapshot')
        def extractor(*args, **kwargs):
            return copy.deepcopy(handover)
        result = rounds.run(conn, archive, cfg, uni, item, seq, extractor=extractor, shown_views=shown, matching_workers=8)
        records = [json.loads(r[0]) for r in conn.execute('select decisions_json from match_records where seq=? order by call_no', (seq,))]
        written = conn.execute("select reason from processing_steps where sequence_no=? and step='written' order by id desc limit 1", (seq,)).fetchone()
        new_ids = json.loads(written[0])['new'] if written else {}
        row = {'source_seq': source_seq, 'seq': seq, 'input_id': input_id, 'new_id': new_ids.get('c1', ''), 'failed': result.failed,
               'shown': len(shown), 'decisions': records, 'evidence': len(evidence)}
        results.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        if result.failed:
            raise RuntimeError(result.failed)
    (OUT / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
