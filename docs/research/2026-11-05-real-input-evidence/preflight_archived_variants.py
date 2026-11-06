"""Validate identity-safe archived article request pairs with fake transport; no network."""
import argparse
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
from hivemind import bundle, config, extraction, model, testdb, universe  # noqa: E402


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def run(path, original_items):
    manifest = json.loads((path / 'manifest.json').read_text())
    reference = json.loads((path / 'reference-draft.json').read_text())
    report = json.loads((HERE / 'draft-two-article-inputs.json').read_text())['report']
    require(digest(report['text_page']) == report['text_page_sha256'], 'report hash mismatch')
    cfg = config.load(ROOT / 'poc/config/poc-v117.json')
    uni = universe.load(ROOT / 'poc/universe.json')
    require(cfg.baseline is None, 'seeded baseline is not permitted')
    references = {a['input_id']: a for a in reference['articles']}
    records = manifest['articles']
    require(len(records) == 3 and len(references) == 3, 'wrong source/reference count')
    require(len({r['variant_id'] for r in records}) == 3, 'duplicate variant')
    db = sqlite3.connect((path / 'items.sqlite').resolve().as_uri() + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    original = sqlite3.connect(original_items.resolve().as_uri() + '?mode=ro', uri=True)
    report_row = original.execute('select text_page,published_at,source_uri from items where input_id=?', (report['input_id'],)).fetchone()
    require(report_row is not None and digest(report_row[0]) == report['text_page_sha256'] and report_row[1] == report['published_at']
            and report_row[2] == report['source_uri'], 'report origin mismatch')
    require(db.execute('select count(*) from items').fetchone()[0] == 3, 'unexpected local source rows')
    lookup = bundle.item_lookup(db)
    report_quote = ('NVIDIA will pay its next quarterly cash dividend of $0.25 per share on October 1, 2026, '
                    'to all shareholders of record on September 10, 2026.')
    require(report_quote in report['text_page'], 'negative control absent from report')
    results = []
    for rec in records:
        row = db.execute('select * from items where input_id=?', (rec['variant_id'],)).fetchone()
        require(row is not None and dict(row) == rec['fields'], 'local source row differs from manifest')
        raw = dict(row)
        body = raw['text']
        require(raw['feed'] == 0 and raw['coverage'] == 'unverified', 'variant incorrectly admitted to feed')
        require(raw['text_page'] is None and raw['text_article'] is None and raw['text_chars'] == len(body), 'stale article fields')
        require(digest(body) == raw['content_sha256'] == rec['body_sha256'], 'body fingerprint mismatch')
        cleaning = json.loads(raw['cleaning'])
        fields = {k: v for k, v in raw.items() if k != 'input_id'}
        payload = {'derivation': manifest['derivation'], 'original_id': rec['original_id'], 'capture_utc': rec['capture_utc'],
                   'archive_html_sha256': cleaning['archive_html_sha256'], 'body_sha256': rec['body_sha256'], 'fields': fields}
        require('archive:' + digest(canonical(payload)) == rec['variant_id'], 'variant identity mismatch')
        metadata = lookup(rec['variant_id'])
        require(all(metadata[k] == raw[k] for k in ('title', 'publisher', 'publisher_type', 'category', 'publication_day', 'source_uri')),
                'reader source lookup mismatch')
        require(metadata['source_uri'] == rec['archive_url'], 'reader source is not archive URL')
        ref = references.get(rec['variant_id'])
        require(ref and ref['original_input_id'] == rec['original_id'] and ref['variant_body_sha256'] == rec['body_sha256'], 'reference identity mismatch')
        for entry in ref['entries'] + ref['exclusions']:
            for span in entry['source_spans']:
                require(span in body, 'reference span missing from article')
        parse = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00'))
        require(parse(report['published_at']) < parse(raw['published_at']) <= parse(raw['retrieved_at']), 'chronology mismatch')
        require(raw['publication_day'] == parse(raw['published_at']).date().isoformat() == parse(raw['retrieved_at']).date().isoformat(), 'capture day differs')
        require(report_quote not in body, 'negative control appears in article')
        positive_quote = ref['entries'][0]['source_spans'][0]
        item = testdb.item_of(row)
        setting, system, user, schema = extraction.request_for(cfg, item, body, [], uni)
        boundary = '\n\n' + extraction.CLOSING
        require(user.count(boundary) == 1, 'article boundary not unique')
        block = ('\n\n[Earlier earnings report: background] Source: ' + report['source_uri'] + '\n'
                 + 'Publication day: ' + report['publication_day'] + '\n' + report['text_page'])
        treatment = user.replace(boundary, block + boundary, 1)
        requests = [model.build_request(setting, system, u, schema, 'extraction', cfg.provider) for u in (user, treatment)]
        unwrapped = json.loads(json.dumps(requests[1])); unwrapped['messages'][1]['content'] = treatment.replace(block, '', 1)
        require(json.dumps(unwrapped).encode('utf-8') == json.dumps(requests[0]).encode('utf-8'), 'arms differ beyond report')
        def fact(ident, quote):
            return {'id': ident, 'quote': quote, 'one_line': 'A source-backed statement.', 'speaker': 'Source',
                    'original_who': '', 'original_day': '', 'tier': 'fact', 'event_time': '', 'links': []}
        answer_data = {'evidence': [fact('e1', positive_quote), fact('e2', report_quote)], 'candidates': [], 'new_groups': []}
        for arm, u, expected in zip(('control', 'treatment'), (user, treatment), requests):
            sent = []
            def fake_transport(provider, request):
                sent.append((provider, json.dumps(request).encode('utf-8')))
                return {'choices': [{'message': {'content': json.dumps(answer_data)}}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0}}
            with tempfile.TemporaryDirectory() as tmp:
                archive = model.Archive(str(Path(tmp) / 'archive.sqlite'))
                result = model.call(archive, cfg, setting, system, u, schema, 'extraction', 'extract', transport=fake_transport)
                wire = json.dumps(expected).encode('utf-8')
                require(sent == [(cfg.provider, wire)] and not result.cached, 'dispatch/cache mismatch')
                with sqlite3.connect(str(Path(tmp) / 'archive.sqlite')) as archived:
                    archived_request = archived.execute('select request_sha256,request_json from model_calls').fetchone()
                canonical_json, identity = model.request_identity(expected)
                require(archived_request == (identity, canonical_json), 'archive identity mismatch')
                kept, candidates, dropped, groups = extraction.sift_with_groups(result.data, item, body, set(), uni)
                require(any(e['id'] == 'e1' for e in kept), 'article quote rejected')
                require(('e2', 'quote not in item') in dropped, 'report-only quote accepted')
                handover = extraction.file_reading(extraction.Reading(kept, candidates, dropped, groups, result, 'v74i'), item, [])
                require(('e1', 'no home') in handover.dropped and not handover.evidence, 'no-home check differs')
            results.append({'variant_id': rec['variant_id'], 'arm': arm, 'request_identity': identity,
                            'wire_sha256': hashlib.sha256(wire).hexdigest(), 'source_lookup': 'archive URL',
                            'article_quote': 'accepted then no home', 'report_quote': 'quote not in item'})
    db.close(); original.close()
    require(len(results) == 6, 'unexercised arm')
    return {'status': 'unpaid fake-transport contract test; no quality score or paid call', 'articles': 3, 'arms': results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--variants', type=Path, required=True)
    ap.add_argument('--items', type=Path, required=True)
    args = ap.parse_args()
    if not args.variants.is_absolute() or not args.items.is_absolute():
        raise SystemExit('absolute paths required')
    try:
        print(json.dumps(run(args.variants, args.items), ensure_ascii=False, indent=2))
    except (OSError, ValueError, KeyError, IndexError, TypeError, sqlite3.Error) as error:
        print('PREFLIGHT REFUSED: ' + str(error), file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
