"""Replay recorded pilot answers through extraction handover, matching, writer and reader without network."""
import dataclasses
import glob
import json
import sqlite3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle, config, extraction, jev, model, testdb, universe
from hivemind.views import round as round_module, store

BASE = ROOT / 'poc/data/pilot-d369-run-20261105'
ITEMS = ROOT / 'poc/data/real-evidence-d369-variants-draft-v1/items.sqlite'
OUT = BASE / 'writer-replay-v1'
if OUT.exists():
    raise SystemExit('writer output exists')
OUT.mkdir()
cfg = config.load(ROOT / 'poc/config/poc-v117.json')
uni = universe.load(ROOT / 'poc/universe.json')
items = sqlite3.connect(ITEMS.resolve().as_uri() + '?mode=ro', uri=True)
items.row_factory = sqlite3.Row

def refuse(*args, **kwargs):
    raise RuntimeError('writer replay refuses external calls')
model._key = refuse
jev._key = refuse
summaries = []
for path in sorted(BASE.glob('draw[123]/*/result.json')):
    source = json.loads(path.read_text())
    intent = json.loads((path.parent / 'intent.json').read_text())
    row = items.execute('select * from items where input_id=?', (intent['input_id'],)).fetchone()
    item = testdb.item_of(row)
    if source['status'] != 'ok':
        raise ValueError('missing extraction answer')
    sift = extraction.sift_with_groups(source['answer'], item, item['text'], set(), uni)
    answer = type('StoredAnswer', (), {'call_id': 0, 'request_sha256': intent['request_identity'], 'cached': False, 'cost_usd': 0.0})()
    handover = extraction.file_reading(extraction.Reading(*sift, answer, cfg.extraction_setting(item['category']).prompt_version.rpartition('-')[2]), item, [])
    actual = {'evidence': handover.evidence, 'candidates': handover.candidates, 'dropped': [list(x) for x in handover.dropped], 'new_groups': handover.new_groups}
    if actual != source['handover']:
        raise ValueError('saved handover does not replay')
    output = OUT / (path.parent.parent.name + '-' + path.parent.name)
    output.mkdir()
    conn = store.open_db(str(output / 'views.sqlite'))
    archive = model.Archive(str(output / 'archive.sqlite'))
    result = round_module.run(conn, archive, cfg, uni, item, 1, extractor=lambda *a, **kw: handover, transport=refuse, log=lambda *a: None)
    views = [r[0] for r in conn.execute('select view_id from views').fetchall()]
    read = [bundle.view_bundle(conn, bundle.item_lookup(items), view_id) for view_id in views]
    summary = {'draw': intent['draw'], 'arm': intent['arm'], 'input_id': item['input_id'], 'result': dataclasses.asdict(result), 'reader_views': read}
    (output / 'reader.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    summaries.append({'draw': intent['draw'], 'arm': intent['arm'], 'input_id': item['input_id'], 'raw_evidence': len(source['answer']['evidence']), 'handover_evidence': len(handover.evidence), 'views': len(views), 'reader_evidence': sum(len(v['evidence']) for v in read), 'failed': result.failed})
    conn.close(); archive.conn.close()
(OUT / 'summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
print(json.dumps(summaries, indent=2))
