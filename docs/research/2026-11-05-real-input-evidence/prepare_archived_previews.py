"""Prepare model-free request previews from unaccepted same-day archive sources."""
import datetime
import hashlib
import gzip
import json
import sqlite3
import sys
import tempfile
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe  # noqa: E402
from hivemind.views import store  # noqa: E402

if len(sys.argv) not in (4, 5) or not all(Path(p).is_absolute() for p in sys.argv[1:]):
    raise SystemExit('usage: prepare_archived_previews.py /absolute/items.sqlite /absolute/packet.json /new/output.json [/absolute/prior-ledger.sqlite]')
items_path, packet_path, output = map(Path, sys.argv[1:4])
prior_path = Path(sys.argv[4]) if len(sys.argv) == 5 else None
if output.exists():
    raise SystemExit('output already exists')
base = Path(__file__).parent
packet = json.loads(packet_path.read_text())
archive_index = json.loads((base / 'source-snapshots/draft-archive-index.json').read_text())
report = json.loads((base / 'draft-two-article-inputs.json').read_text())['report']
sha = lambda data: hashlib.sha256(data.encode('utf-8')).hexdigest()
parse = lambda s: datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))
if sha(report['text_page']) != report['text_page_sha256']:
    raise SystemExit('report hash mismatch')
cfg = config.load(ROOT / 'poc/config/poc-v117.json')
uni = universe.load(ROOT / 'poc/universe.json')
prior_temp = tempfile.TemporaryDirectory() if prior_path else None
prior_conn = None
if prior_path:
    prior_src = sqlite3.connect(prior_path.resolve().as_uri() + '?mode=ro', uri=True)
    copy_path = Path(prior_temp.name) / 'prior.sqlite'
    copied = sqlite3.connect(str(copy_path))
    prior_src.backup(copied)
    copied.close()
    prior_src.close()
    prior_conn = store.open_db(str(copy_path))
pairs = []
with sqlite3.connect(items_path.resolve().as_uri() + '?mode=ro', uri=True) as conn:
    conn.row_factory = sqlite3.Row
    report_row = conn.execute('select text_page, published_at, source_uri from items where input_id=?', (report['input_id'],)).fetchone()
    if not report_row or sha(report_row['text_page']) != report['text_page_sha256'] or report_row['published_at'] != report['published_at'] or report_row['source_uri'] != report['source_uri']:
        raise SystemExit('report differs from stored source')
    for source in packet['articles']:
        row = conn.execute('select * from items where input_id=?', (source['input_id'],)).fetchone()
        if row is None:
            raise SystemExit('missing item ' + source['input_id'])
        item = testdb.item_of(row)
        if any(item[k] != source[k] for k in ('input_id', 'title', 'publication_day', 'published_at', 'source_uri', 'category')):
            raise SystemExit('stored metadata changed')
        if sha(item['text']) != source['database_text_sha256'] or sha(source['archive_body']) != source['archive_body_sha256']:
            raise SystemExit('article hash mismatch')
        archive_source = next((entry for entry in archive_index if entry['input_id'] == source['input_id'] and entry.get('file')), None)
        if not archive_source:
            raise SystemExit('missing archive source')
        html = gzip.decompress((ROOT / archive_source['file']).read_bytes())
        if hashlib.sha256(html).hexdigest() != source['archive_html_sha256']:
            raise SystemExit('archived HTML hash mismatch')
        page = BeautifulSoup(html, 'html.parser')
        if source['input_id'].startswith('nvblog:'):
            node = page.find(class_='entry-content')
            body = node.get_text('\n', strip=True) if node else None
        elif source['input_id'] == 'gnews:df63c0bccb7dbb77885ad5ef':
            node = page.find(id='article-body')
            cards = node.select('section.shadow-card') if node else []
            if len(cards) != 1 or 'Moneyball' not in cards[0].get_text(' ', strip=True):
                raise SystemExit('stock widget identity changed')
            removed = cards[0].get_text('\n', strip=True)
            if sha(removed) != source.get('removed_widget_sha256'):
                raise SystemExit('stock widget hash changed')
            cards[0].decompose()
            body = node.get_text('\n', strip=True)
        else:
            scripts = []
            for script in page.find_all('script', type='application/ld+json'):
                try:
                    scripts.append(json.loads(script.get_text()))
                except (ValueError, TypeError):
                    continue
            bodies = [data['articleBody'] for data in scripts if isinstance(data, dict) and data.get('articleBody')]
            if len(bodies) != 1:
                raise SystemExit('publisher article body not unique')
            body = bodies[0]
        if body != source['archive_body']:
            raise SystemExit('archive extraction does not reproduce article body')
        if parse(report['published_at']) >= parse(source['archived_publication_time']):
            raise SystemExit('report is not earlier than source publication')
        if len(source['archive_body']) > extraction.MAX_TEXT_CHARS:
            raise SystemExit('article would be truncated')
        observed_at = datetime.datetime.strptime(source['archive_capture_utc'], '%Y%m%d%H%M%S').replace(tzinfo=datetime.timezone.utc)
        if observed_at < parse(source['archived_publication_time']):
            raise SystemExit('archive capture precedes published time')
        item['published_at'] = source['archived_publication_time']
        item['text'] = source['archive_body']
        objects = [o['value'] for o in item.get('object_identifiers') or []]
        shown = extraction.shown_views(prior_conn, cfg, item, objects) if prior_conn else []
        setting, system, user, schema = extraction.request_for(cfg, item, item['text'], shown, uni)
        boundary = '\n\n' + extraction.CLOSING
        if user.count(boundary) != 1:
            raise SystemExit('article/closing boundary is not unique')
        block = ('\n\n[Earlier earnings report: background] Source: ' + report['source_uri'] + '\n'
                 + 'Publication day: ' + report['publication_day'] + '\n' + report['text_page'])
        treated_user = user.replace(boundary, block + boundary, 1)
        control = model.build_request(setting, system, user, schema, 'extraction', cfg.provider)
        treated = model.build_request(setting, system, treated_user, schema, 'extraction', cfg.provider)
        reversed_treatment = json.loads(json.dumps(treated))
        reversed_treatment['messages'][1]['content'] = treated_user.replace(block, '', 1)
        if json.dumps(reversed_treatment) != json.dumps(control):
            raise SystemExit('requests differ beyond report block')
        captured = []
        def fake_transport(provider, request):
            captured.append(json.dumps(request))
            return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}]}
        with tempfile.TemporaryDirectory() as temp:
            archive = model.Archive(str(Path(temp) / 'archive.sqlite'))
            model.call(archive, cfg, setting, system, user, schema, 'extraction', 'extract', transport=fake_transport)
            model.call(archive, cfg, setting, system, treated_user, schema, 'extraction', 'extract', transport=fake_transport)
        if captured != [json.dumps(control), json.dumps(treated)]:
            raise SystemExit('fake transport did not see expected requests')
        pairs.append({'input_id': source['input_id'], 'split': source['split'], 'source_publication': item['published_at'],
                      'snapshot_capture_utc': source['archive_capture_utc'], 'knowledge_cutoff_utc': observed_at.isoformat(),
                      'body_sha256': source['archive_body_sha256'],
                      'shown_questions': len(shown), 'shown_question_ids': [q['view_id'] for q in shown],
                      'prior_snapshot_sequence': store.day_start_seq(prior_conn, item['publication_day']) if prior_conn else None,
                      'item_metadata': {k: v for k, v in item.items() if k not in ('text', 'text_page')},
                      'control_wire_sha256': sha(json.dumps(control)), 'treatment_wire_sha256': sha(json.dumps(treated)),
                      'control_sha256': model.request_identity(control)[1],
                      'treatment_sha256': model.request_identity(treated)[1], 'control': control, 'treatment': treated})
output.write_text(json.dumps({'status': 'UNSENT, NOT REVIEWED OR FROZEN; do not score', 'config': cfg.version, 'config_checksum': cfg.checksum, 'prior_ledger_sha256': hashlib.sha256(prior_path.read_bytes()).hexdigest() if prior_path else None, 'universe_sha256': hashlib.sha256((ROOT / 'poc/universe.json').read_bytes()).hexdigest(), 'packet_sha256': hashlib.sha256(packet_path.read_bytes()).hexdigest(), 'pairs': pairs}, ensure_ascii=False, indent=2) + '\n')
print(f'{len(pairs)} archived-source draft request pairs, verified on fake transport; no model requests sent')
for p in pairs:
    print(p['input_id'], p['split'], 'shown questions:', p['shown_questions'], 'news characters:', len(p['control']['messages'][1]['content']),
          'with report:', len(p['treatment']['messages'][1]['content']))
