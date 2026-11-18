"""D463's probe, the request step ($0): write the c8 requests Step 1 would send for fresh articles, against a fixed library snapshot, into a
trace file shaped like the runner's, so that the reviewed c14 probe (`clean-arch/step1-diagnosis-2026-11-12/probe_c14.py`) sends them
unchanged with its arms, ceilings, format rule and records.

Each request is built exactly as `clean-arch/step1/runner.py` builds one (the payload of current_entity, company_tags, open_theses and
source_item, the closing check after the item, `model.build_request` with the stored settings), and its `sent_request` is production's
adaptation (`live.deepseek_json_mode`, reasoning effort high). Before writing anything, the builder must rebuild one stored request of the
full run byte for byte from that row's own before-state and item (c3, the last sequence), or it refuses.

  python3 build_fresh_trace.py <selection.json> <output trace.sqlite>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
from hivemind import config, model, testdb  # noqa: E402
import live  # noqa: E402

ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
ARMS = ROOT / 'clean-arch/step1-unfiled-2026-11-08/arms'
REFERENCE = ROOT / 'poc/data/clean-e2e-full-2026-11-13/c3/step1/trace.sqlite'
SNAPSHOT = HERE / 'snapshot-c3-2026-07-14.json'
ENTITY = 'NVDA'


def item_by_id(input_id):
    conn = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    row = conn.execute('select * from items where input_id = ?', (input_id,)).fetchone()
    conn.close()
    if row is None:
        raise SystemExit(f'unknown item: {input_id}')
    item = testdb.item_of(row)
    tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
    if ENTITY not in tags or not item.get('text') or item.get('feed') != 1 or item.get('copy_of') or item.get('supersedes'):
        raise SystemExit(f'item outside the runner selection rule: {input_id}')
    return item


def build_request(settings, theses, item):
    """The runner's request for one item (runner.run's loop body), with c8's texts and schema."""
    prompt = (ARMS / 'c8-system.txt').read_text(encoding='utf-8')
    closing = (ARMS / 'c8-closing.txt').read_text(encoding='utf-8')
    schema = json.loads((ARMS / 'c8-schema.json').read_text(encoding='utf-8'))
    dump = lambda obj: json.dumps(obj, ensure_ascii=False)
    shown = [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in theses]
    tags = [x['value'] for x in item['object_identifiers'] if x.get('kind') == 'ticker']
    payload = {'current_entity': ENTITY, 'company_tags': tags, 'open_theses': shown, 'source_item': {
        'id': item['input_id'], 'publisher': item['publisher'], 'publication_date': item['publication_day'],
        'published_at': item['published_at'], 'publisher_type': item.get('publisher_type'),
        'authors': item.get('authors'), 'category': item.get('category'),
        'source_uri': item['source_uri'], 'title': item['title'], 'text': item['text']}}
    user = dump(payload) + f'\n\n{closing}'
    setting = config.Setting('clean-step1', settings['model'], 'clean-step1', settings['reasoning_effort'], settings['max_output_tokens'])
    return model.build_request(setting, prompt, user, schema, 'clean_step1', settings['provider'])


def check_reference():
    conn = sqlite3.connect(f'file:{REFERENCE}?mode=ro', uri=True)
    settings = json.loads(conn.execute('select settings from run').fetchone()[0])
    sequence, input_id, before, stored, raw = conn.execute(
        "select sequence, input_id, before_state, request, raw_response from trace where status = 'complete' order by sequence desc limit 1").fetchone()
    conn.close()
    rebuilt = build_request(settings, json.loads(before), item_by_id(input_id))
    if json.dumps(rebuilt) != stored:
        raise SystemExit(f'the builder does not rebuild the stored request of c3 sequence {sequence}')
    if json.dumps(live.deepseek_json_mode(rebuilt, 'high')) != json.dumps(json.loads(raw)['sent_request']):
        raise SystemExit(f'the adapter does not rebuild the stored sent request of c3 sequence {sequence}')
    return settings, sequence


def main():
    selection, output = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2])
    if output.exists():
        raise SystemExit(f'{output} exists')
    settings, reference_sequence = check_reference()
    theses = json.loads(SNAPSHOT.read_text())
    conn = sqlite3.connect(output)
    conn.execute('create table trace (sequence integer primary key, input_id text not null, before_state text not null, request text not null, '
                 'raw_response text, status text not null)')
    for sequence, entry in enumerate(selection, 1):
        request = build_request(settings, theses, item_by_id(entry['input_id']))
        conn.execute('insert into trace values (?, ?, ?, ?, ?, ?)', (sequence, entry['input_id'], json.dumps(theses, ensure_ascii=False),
                     json.dumps(request), json.dumps({'sent_request': live.deepseek_json_mode(request, 'high')}), 'complete'))
    conn.commit()
    conn.close()
    print(f'reference c3 sequence {reference_sequence} rebuilt byte for byte; {len(selection)} fresh requests written to {output}')


if __name__ == '__main__':
    main()
