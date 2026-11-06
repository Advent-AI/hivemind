"""Build unsent real extraction requests for the two-article draft; never call a model."""
import hashlib
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe  # noqa: E402

if len(sys.argv) != 3:
    raise SystemExit('usage: prepare_request_preview.py /absolute/items.sqlite /new/output.json')
db_path, output = Path(sys.argv[1]), Path(sys.argv[2])
if not db_path.is_absolute() or not output.is_absolute() or output.exists():
    raise SystemExit('supply absolute paths and a new output file')
packet = json.loads((Path(__file__).parent / 'draft-two-article-inputs.json').read_text())
cfg = config.load(ROOT / 'poc/config/poc-v117.json')
uni = universe.load(ROOT / 'poc/universe.json')
report = packet['report']
sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
if sha(report['text_page']) != report['text_page_sha256'] or '63,956' not in report['text_page']:
    raise SystemExit('report text changed or expected table is absent')
with sqlite3.connect(db_path.resolve().as_uri() + '?mode=ro', uri=True) as conn:
    conn.row_factory = sqlite3.Row
    report_row = conn.execute('select text_page, publication_day, source_uri from items where input_id=?', (report['input_id'],)).fetchone()
    if report_row is None or sha(report_row['text_page']) != report['text_page_sha256'] or report_row['publication_day'] != report['publication_day'] or report_row['source_uri'] != report['source_uri']:
        raise SystemExit('report identity does not match the supplied items database')
    previews = []
    for source in packet['articles']:
        row = conn.execute('select * from items where input_id=?', (source['input_id'],)).fetchone()
        if row is None:
            raise SystemExit('missing article ' + source['input_id'])
        item = testdb.item_of(row)
        text = item['text']
        if any(item[key] != source[key] for key in ('input_id', 'title', 'publication_day', 'published_at', 'source_uri', 'category')):
            raise SystemExit('article metadata changed: ' + source['input_id'])
        if sha(source['text']) != source['text_sha256'] or sha(text) != source['text_sha256'] or len(text) > extraction.MAX_TEXT_CHARS:
            raise SystemExit('article changed or would be truncated: ' + source['input_id'])
        if report['publication_day'] >= item['publication_day']:
            raise SystemExit('report not published on an earlier day')
        setting, system, user, schema = extraction.request_for(cfg, item, text, [], uni)
        boundary = '\n\n' + extraction.CLOSING
        if user.count(boundary) != 1:
            raise SystemExit('cannot locate unique article/closing boundary')
        block = ('\n\n[Earlier earnings report: background] Source: ' + report['source_uri'] + '\n'
                 + 'Publication day: ' + report['publication_day'] + '\n' + report['text_page'])
        treatment = user.replace(boundary, block + boundary, 1)
        if treatment.replace(block, '', 1) != user:
            raise SystemExit('arms differ beyond the report block')
        control = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
        treated = model.build_request(setting, system, treatment, schema, 'extraction', cfg.provider)
        rebuilt = json.loads(json.dumps(treated))
        rebuilt['messages'][1]['content'] = rebuilt['messages'][1]['content'].replace(block, '', 1)
        if json.dumps(rebuilt) != json.dumps(control):
            raise SystemExit('complete requests differ beyond the report block or key order')
        recorded = []
        def fake_transport(provider, request):
            recorded.append(json.dumps(request))
            return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}]}
        with tempfile.TemporaryDirectory() as temp:
            archive = model.Archive(str(Path(temp) / 'calls.sqlite'))
            model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=fake_transport)
            model.call(archive, cfg, setting, system, treatment, schema, 'extraction', 'extract', transport=fake_transport)
        if recorded != [json.dumps(control), json.dumps(treated)]:
            raise SystemExit('fake transport received a request or key order different from the preview')
        report_quote = 'NVIDIA will pay its next quarterly cash dividend of $0.25 per share on October 1, 2026, to all shareholders of record on September 10, 2026.'
        if report_quote not in report['text_page'] or report_quote in text:
            raise SystemExit('report-only quote positive control is not valid')
        fake_evidence = {'id': 'e1', 'quote': report_quote, 'one_line': 'NVIDIA will pay a dividend.', 'speaker': 'NVIDIA',
                         'original_who': 'NVIDIA', 'original_day': '2026-08-26', 'tier': 'party_statement', 'event_time': '', 'links': []}
        evidence, _, dropped = extraction.sift({'evidence': [fake_evidence], 'candidates': []}, item, text, set(), uni)
        if evidence or not any(reason == 'quote not in item' for _, reason in dropped):
            raise SystemExit('report-only quote did not fail article quote validation')
        article_quote = next((line for line in text.splitlines() if 80 <= len(line) <= 400), None)
        if article_quote is None:
            raise SystemExit('no suitable source quote positive control')
        positive = dict(fake_evidence, quote=article_quote, original_day='')
        accepted, _, refusal = extraction.sift({'evidence': [positive], 'candidates': []}, item, text, set(), uni)
        if len(accepted) != 1 or refusal:
            raise SystemExit('source quote positive control was not accepted: ' + str(refusal))
        previews.append({'input_id': item['input_id'], 'article_sha256': sha(text), 'report_sha256': sha(report['text_page']),
                         'control_identity': model.request_identity(control)[1], 'treatment_identity': model.request_identity(treated)[1],
                         'control': control, 'treatment': treated})
output.write_text(json.dumps({'status': 'UNSENT DRAFT; NOT A FROZEN EXPERIMENT', 'config': cfg.version, 'pairs': previews}, ensure_ascii=False, indent=2) + '\n')
print(f'{len(previews)} unsent pairs; source hashes, complete fake-transport requests, key order, and report-only quote refusal checked')
for pair in previews:
    print(pair['input_id'], 'control chars', len(pair['control']['messages'][1]['content']), 'with-report chars', len(pair['treatment']['messages'][1]['content']))
