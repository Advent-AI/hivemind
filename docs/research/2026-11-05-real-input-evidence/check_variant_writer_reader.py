"""Unpaid source-provenance check through extraction, matching, writing and the actual reader."""
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle, config, jev, model, testdb, universe  # noqa: E402
from hivemind.views import round as round_module, store  # noqa: E402

if len(sys.argv) != 2 or not Path(sys.argv[1]).is_absolute():
    raise SystemExit('usage: check_variant_writer_reader.py /absolute/variants/items.sqlite')
items = sqlite3.connect(Path(sys.argv[1]).resolve().as_uri() + '?mode=ro', uri=True)
items.row_factory = sqlite3.Row
row = items.execute("select * from items where category='T6'").fetchone()
if row is None:
    raise SystemExit('T6 variant missing')
item = testdb.item_of(row)
quote = ('Among the announcements Huang and Nadella outlined Wednesday, RTX Spark puts the full NVIDIA AI stack into Windows laptops and compact desktops, '
         'with laptop preorders open today and available October 16. Compact desktops will be available for sale in November.')
if quote not in item['text'] or item['feed'] != 0:
    raise SystemExit('test quote or direct-extraction source invalid')
answer = {'candidates': [{'id': 'c1', 'object': 'NVDA', 'kind': 'asset', 'looks_at': 'RTX Spark laptop availability',
          'question': 'Will RTX Spark laptops become available by the end of 2026?',
          'rungs': [{'label': 'Yes', 'condition': 'Laptops become available by 2026-12-31.', 'lo': None, 'hi': None},
                    {'label': 'No', 'condition': 'Laptops do not become available by 2026-12-31.', 'lo': None, 'hi': None}],
          'due_day': '2026-12-31', 'year': '2026', 'evidence_ids': ['e1'], 'measure': 'event', 'scope': 'RTX Spark laptops',
          'period_start': '2026-01-01', 'period_end': '2026-12-31', 'basis': 'n/a', 'unit': 'n/a', 'event_type': 'shipment',
          'group_refs': [], 'opens_as': 'main_driver', 'settled_by': 'Public availability announcements.'}],
          'evidence': [{'id': 'e1', 'quote': quote, 'one_line': 'NVIDIA reported laptop preorders and planned October 16 availability.',
                        'speaker': 'NVIDIA', 'original_who': 'NVIDIA', 'original_day': '2026-10-07', 'tier': 'fact',
                        'event_time': '', 'links': ['c1']}], 'new_groups': []}


def refuse(*args):
    raise RuntimeError('a test attempted to read a credential')


model._key = refuse
jev._key = refuse
calls = []


def transport(*args):
    if len(args) == 1:
        req = args[0]; results = {}
        for key, q in req['questions'].items():
            if q['type'] == 'noul':
                results[key] = {'type': 'noul', 'noul': 0.9}
            else:
                labels = q['criteria']; chosen = 'different' if 'different' in labels else labels[-1]
                results[key] = {'type': 'choice', 'choice': chosen, 'confidence': 1.0,
                                'probabilities': {label: float(label == chosen) for label in labels}}
        calls.append('jev')
        return {'model': req['model'], 'answers': results, 'usage': {}}
    provider, req = args
    name = req['response_format']['json_schema']['name']
    if name != 'extraction':
        raise RuntimeError('unexpected model call: ' + name)
    calls.append(name)
    return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}


with tempfile.TemporaryDirectory() as tmp:
    conn = store.open_db(str(Path(tmp) / 'views.sqlite'))
    archive = model.Archive(str(Path(tmp) / 'archive.sqlite'))
    cfg = config.load(ROOT / 'poc/config/poc-v117.json')
    uni = universe.load(ROOT / 'poc/universe.json')
    result = round_module.run(conn, archive, cfg, uni, item, 1, transport=transport, log=lambda *a: None)
    if result.failed or result.new_views != 1 or result.evidence != 1:
        raise SystemExit(f'pipeline did not write source-backed example: {result}')
    view_id = conn.execute('select view_id from views').fetchone()[0]
    read = bundle.view_bundle(conn, bundle.item_lookup(items), view_id)
    evidence = read['evidence']
    if len(evidence) != 1 or evidence[0]['quote'] != quote:
        raise SystemExit('reader did not receive exact article quote')
    sources = evidence[0]['sources']
    if not sources or sources[0]['source']['source_uri'] != item['source_uri'] or sources[0]['input_id'] != item['input_id']:
        raise SystemExit('reader source provenance did not resolve archived variant')
    if item['source_uri'].find('/web/') < 0:
        raise SystemExit('reader URL does not identify an archived capture')
    print('1 fake extraction → real matching/writing → 1 reader evidence with exact archive URL; no credentials or paid calls')
    print('source:', item['input_id'], 'calls:', ', '.join(calls))
