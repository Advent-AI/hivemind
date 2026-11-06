"""Send the saved article against the actual full pre-item question snapshot."""
import concurrent.futures
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as p  # noqa: E402
from hivemind import config, model, testdb, universe  # noqa: E402

RUN = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05'
OUT = ROOT / 'poc/data/all-open-context-probe-2026-11-05'
SEQ = 1285
TARGET = 'v105'


def build():
    conn = p.store.open_read_only(str(RUN / 'snapshot/views.sqlite'))
    input_id = conn.execute('select input_id from handovers where seq=?', (SEQ,)).fetchone()[0]
    items = testdb.open_db(str(p.INPUT))
    item = testdb.item_of(items.execute('select * from items where input_id=?', (input_id,)).fetchone())
    items.close()
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    for row in conn.execute('select p.object_id,p.name,p.kind from poc_subjects p where exists(select 1 from views v where v.object_id=p.object_id and v.created_seq<?)', (SEQ,)):
        record = {'id': row['object_id'], 'name': row['name'], 'categories': [], 'aliases': []}
        if row['kind'] == 'theme':
            uni.themes[row['object_id']] = record
            uni.theme_names[row['name']] = row['object_id']
        else:
            uni.companies[row['object_id']] = record
    old_shown = p.read(RUN / 'items' / str(SEQ) / 'shown.json')
    shown = p.latest_library(conn, SEQ)
    if TARGET in {v['view_id'] for v in old_shown} or TARGET not in {v['view_id'] for v in shown}:
        raise ValueError('expected previously hidden question not found')
    if not {v['view_id'] for v in old_shown} <= {v['view_id'] for v in shown}:
        raise ValueError('a previously shown question disappeared')
    setting, old_requests = p.item_requests(cfg, uni, item, old_shown)
    for arm, spec in old_requests.items():
        original = p.read(RUN / 'items' / str(SEQ) / (arm + '-request.json'))
        rebuilt = model.build_request(setting, spec[0], spec[1], spec[2], spec[3], cfg.provider)
        if json.dumps(rebuilt) != json.dumps(original):
            raise ValueError(arm + ' historical request bytes differ')
    _, requests = p.item_requests(cfg, uni, item, shown)
    if not all(('  - ' + TARGET + ' ') in requests[arm][1] for arm in ('a', 'b')):
        raise ValueError('target question is not in both new requests')
    conn.close()
    return cfg, setting, item, old_shown, shown, requests


def main():
    cfg, setting, item, old_shown, shown, requests = build()
    OUT.mkdir(exist_ok=False)
    p.write(OUT / 'shown.json', shown)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures = {arm: pool.submit(p.call, cfg, setting, arm, spec, OUT) for arm, spec in requests.items()}
        a, b = futures['a'].result(), futures['b'].result()
    for arm, answer in (('a', a), ('b', b)):
        if p.completed_answer(cfg, setting, arm, requests[arm], OUT) != answer:
            raise ValueError(arm + ' request/provider/answer mismatch')
    invalid_b = [e['id'] for e in b['evidence'] if p.source_quote(e['quote'], item['text'][:p.extraction.MAX_TEXT_CHARS]) is None]
    invalid_a = [e['quote'] for q in a['questions'] for e in q['evidence'] if p.source_quote(e['quote'], item['text'][:p.extraction.MAX_TEXT_CHARS]) is None]
    print(json.dumps({'old_shown': len(old_shown), 'full_shown': len(shown), 'questions': [q['question'] for q in a['questions']],
                      'target_evidence': [{'quote': e['quote'], 'links': e['links']} for e in b['evidence'] if TARGET in e['links']],
                      'other_evidence': len(b['evidence']), 'invalid_a_quotes': invalid_a, 'invalid_b_ids': invalid_b}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
