"""Unpaid contract preflight for archived-source report-context drafts; no network."""
import argparse
import gzip
import hashlib
import json
import sqlite3
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, extraction, model, testdb, universe  # noqa: E402


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def run(preview_path, packet_path, report_path, items_path):
    preview = json.loads(gzip.decompress(preview_path.read_bytes()))
    packet = json.loads(packet_path.read_text())
    report = json.loads(report_path.read_text())['report']
    gold_draft = json.loads((HERE / 'draft-gold-independent-archived.json').read_text())
    sources = {a['input_id']: a for a in packet['articles']}
    references = {a['input_id']: a for a in gold_draft['articles']}
    require(len(preview['pairs']) == 3 and len(sources) == 3, 'expected the three draft inputs')
    require(set(sources) == {p['input_id'] for p in preview['pairs']}, 'source IDs differ')
    require(hashlib.sha256(packet_path.read_bytes()).hexdigest() == preview['packet_sha256'], 'packet hash differs')
    require(sha(report['text_page']) == report['text_page_sha256'], 'report hash differs')
    require(items_path.is_absolute() and items_path.exists(), 'source database missing or not absolute')
    source_conn = sqlite3.connect(items_path.resolve().as_uri() + '?mode=ro', uri=True)
    source_conn.row_factory = sqlite3.Row
    report_row = source_conn.execute('select text_page, published_at, source_uri from items where input_id=?', (report['input_id'],)).fetchone()
    require(report_row is not None and sha(report_row['text_page']) == report['text_page_sha256']
            and report_row['published_at'] == report['published_at'] and report_row['source_uri'] == report['source_uri'],
            'report disagrees with source database')
    cfg = config.load(ROOT / 'poc/config/poc-v117.json')
    require(cfg.checksum == preview['config_checksum'] and cfg.version == preview['config'], 'configuration differs')
    require(hashlib.sha256((ROOT / 'poc/universe.json').read_bytes()).hexdigest() == preview['universe_sha256'], 'universe differs')
    uni = universe.load(ROOT / 'poc/universe.json')
    report_quote = ('NVIDIA will pay its next quarterly cash dividend of $0.25 per share on October 1, 2026, '
                    'to all shareholders of record on September 10, 2026.')
    require(report_quote in report['text_page'], 'negative-control quote absent from report')
    rows = []
    for pair in preview['pairs']:
        source = sources[pair['input_id']]
        text = source['archive_body']
        require(sha(text) == source['archive_body_sha256'] == pair['body_sha256'], 'article hash differs: ' + pair['input_id'])
        require(report_quote not in text, 'negative-control quote is present in article: ' + pair['input_id'])
        require(datetime.fromisoformat(report['published_at'].replace('Z', '+00:00')) <
                datetime.fromisoformat(source['archived_publication_time'].replace('Z', '+00:00')), 'report not earlier')
        item = dict(pair['item_metadata'], text=text)
        raw_item = source_conn.execute('select * from items where input_id=?', (source['input_id'],)).fetchone()
        require(raw_item is not None, 'source article missing from database')
        original = testdb.item_of(raw_item)
        require(sha(original['text']) == source['database_text_sha256'], 'original article differs from database')
        original['published_at'] = source['archived_publication_time']
        original_metadata = {k: v for k, v in original.items() if k not in ('text', 'text_page')}
        require(original_metadata == pair['item_metadata'], 'article metadata differs from database')
        require(item['input_id'] == source['input_id'] and item['published_at'] == source['archived_publication_time'], 'item identity differs')
        require(item['publication_day'] == source['publication_day'] and item['category'] == source['category'], 'item metadata differs')
        setting, system, user, schema = extraction.request_for(cfg, item, text, [], uni)
        require(len(text) <= extraction.MAX_TEXT_CHARS, 'article truncated')
        boundary = '\n\n' + extraction.CLOSING
        require(user.count(boundary) == 1, 'article boundary not unique')
        block = ('\n\n[Earlier earnings report: background] Source: ' + report['source_uri'] + '\n'
                 + 'Publication day: ' + report['publication_day'] + '\n' + report['text_page'])
        treated = user.replace(boundary, block + boundary, 1)
        positive_quote = references[pair['input_id']]['entries'][0]['source_spans'][0]
        require(positive_quote in text and len(positive_quote) >= 30, 'positive-control quote absent from article')
        def evidence(ident, quote):
            return {'id': ident, 'quote': quote, 'one_line': 'A source-backed statement.', 'speaker': 'Source',
                    'original_who': '', 'original_day': '', 'tier': 'fact', 'event_time': '', 'links': []}
        fake_answer = {'evidence': [evidence('e1', positive_quote), evidence('e2', report_quote)], 'candidates': [], 'new_groups': []}
        for arm, user_text in [('control', user), ('treatment', treated)]:
            request = model.build_request(setting, system, user_text, schema, 'extraction', cfg.provider)
            saved = pair[arm]
            wire = json.dumps(request).encode('utf-8')
            require(wire == json.dumps(saved).encode('utf-8'), 'wire request differs: ' + pair['input_id'] + '/' + arm)
            require(hashlib.sha256(wire).hexdigest() == pair[arm + '_wire_sha256'], 'wire hash differs')
            require(model.request_identity(request)[1] == pair[arm + '_sha256'], 'archive identity differs')
            sent = []
            def fake_transport(provider, request):
                sent.append((provider, json.dumps(request).encode('utf-8')))
                return {'choices': [{'message': {'content': json.dumps(fake_answer)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
            with tempfile.TemporaryDirectory() as tmp:
                archive = model.Archive(str(Path(tmp) / 'archive.sqlite'))
                answer = model.call(archive, cfg, setting, system, user_text, schema, 'extraction', 'extract', transport=fake_transport)
                require(len(sent) == 1 and sent[0] == (cfg.provider, wire) and not answer.cached, 'fake dispatch/cache mismatch')
                with sqlite3.connect(str(Path(tmp) / 'archive.sqlite')) as conn:
                    stored = conn.execute('select request_sha256, request_json from model_calls').fetchone()
                canonical, identity = model.request_identity(request)
                require(stored == (identity, canonical), 'archive canonical request differs')
                kept, candidates, dropped, groups = extraction.sift_with_groups(answer.data, item, text, set(), uni)
                require(any(e['id'] == 'e1' for e in kept), 'article quote not retained')
                require(('e2', 'quote not in item') in dropped, 'report-only quote not refused')
                reading = extraction.Reading(kept, candidates, dropped, groups, answer, 'v74i')
                handover = extraction.file_reading(reading, item, [])
                require(('e1', 'no home') in handover.dropped and not handover.evidence, 'no-home behavior differs')
            rows.append({'input_id': pair['input_id'], 'arm': arm, 'fake_dispatches': len(sent),
                         'article_quote': 'accepted then no home', 'report_quote': 'quote not in item'})
    source_conn.close()
    require(len(rows) == 6, 'unexercised draft arm')
    return {'status': 'unpaid fake-transport contract preflight only; not efficacy, gold approval, or paid send',
            'articles': 3, 'arms_judged': len(rows), 'results': rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', type=Path, default=HERE / 'draft-archived-clean-request-preview-v3.json.gz')
    ap.add_argument('--packet', type=Path, default=HERE / 'draft-three-archived-clean-v2.json')
    ap.add_argument('--report', type=Path, default=HERE / 'draft-two-article-inputs.json')
    ap.add_argument('--items', type=Path, default=Path('/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'))
    args = ap.parse_args()
    try:
        print(json.dumps(run(args.preview, args.packet, args.report, args.items), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, OSError, IndexError, TypeError) as error:
        print('PREFLIGHT REFUSED: ' + str(error), file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
