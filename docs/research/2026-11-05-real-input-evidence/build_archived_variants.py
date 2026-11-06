"""Build an unapproved experiment-local source DB with identity-safe archive variants; no calls."""
import argparse
import gzip
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import bundle  # noqa: E402

INHERITED = ('klass', 'category', 'publisher', 'publisher_type', 'authors', 'document_format', 'channel_category',
             'media_type', 'language', 'object_identifiers', 'title', 'topic', 'tier', 'is_structured',
             'has_readable_text', 'bootstrap')
SCHEMA = set(INHERITED) | {'input_id', 'source_uri', 'text', 'text_page', 'text_article', 'content_sha256', 'text_chars',
                           'published_at', 'publication_day', 'page_day', 'retrieved_at', 'day_source', 'listing_day',
                           'copy_of', 'supersedes', 'channel', 'source', 'coverage', 'feed', 'extra', 'cleaning'}
VERSION = 'archive-derived-item-v1'


def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def canonical(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def archived_body(source, entry):
    raw = gzip.decompress((ROOT / entry['file']).read_bytes())
    if hashlib.sha256(raw).hexdigest() != source['archive_html_sha256']:
        raise ValueError('archive HTML hash mismatch')
    page = BeautifulSoup(raw, 'html.parser')
    published_meta = page.find('meta', attrs={'property': 'article:published_time'})
    if published_meta is None or not published_meta.get('content'):
        raise ValueError('publisher publication time missing from archived HTML')
    actual_published = datetime.fromisoformat(published_meta['content'].replace('Z', '+00:00'))
    expected_published = datetime.fromisoformat(source['archived_publication_time'].replace('Z', '+00:00'))
    if actual_published.tzinfo is None or actual_published != expected_published:
        raise ValueError('publisher publication time differs from archived HTML')
    if source['input_id'].startswith('nvblog:'):
        node = page.find(class_='entry-content')
        if node is None:
            raise ValueError('missing publisher content')
        body = node.get_text('\n', strip=True)
    elif source['input_id'] == 'gnews:df63c0bccb7dbb77885ad5ef':
        node = page.find(id='article-body')
        cards = node.select('section.shadow-card') if node else []
        if len(cards) != 1 or 'Moneyball' not in cards[0].get_text(' ', strip=True):
            raise ValueError('unidentifiable stock widget')
        if digest(cards[0].get_text('\n', strip=True)) != source['removed_widget_sha256']:
            raise ValueError('stock widget identity differs')
        cards[0].decompose()
        body = node.get_text('\n', strip=True)
    else:
        values = []
        for script in page.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.get_text())
            except (ValueError, TypeError):
                continue
            if isinstance(data, dict) and data.get('articleBody'):
                values.append(data['articleBody'])
        if len(values) != 1:
            raise ValueError('publisher article body is not unique')
        body = values[0]
    if body != source['archive_body'] or digest(body) != source['archive_body_sha256']:
        raise ValueError('derived article body differs')
    return body


def build(items_path, packet_path, output_dir):
    if not items_path.is_absolute() or not packet_path.is_absolute() or not output_dir.is_absolute():
        raise ValueError('paths must be absolute')
    if output_dir.exists():
        raise ValueError('output directory already exists')
    packet = json.loads(packet_path.read_text())
    index = json.loads((HERE / 'source-snapshots/draft-archive-index.json').read_text())
    report = json.loads((HERE / 'draft-two-article-inputs.json').read_text())['report']
    source_db = sqlite3.connect(items_path.resolve().as_uri() + '?mode=ro', uri=True)
    source_db.row_factory = sqlite3.Row
    columns = [r[1] for r in source_db.execute('pragma table_info(items)')]
    if len(columns) != 37 or set(columns) != SCHEMA:
        raise ValueError('items schema differs from closed mapping')
    schema_sql = source_db.execute("select sql from sqlite_master where type='table' and name='items'").fetchone()[0]
    sources = packet.get('articles') or []
    if len(sources) != 3 or len({s['input_id'] for s in sources}) != 3:
        raise ValueError('expected three distinct source articles')
    records = []
    for s in sources:
        old = source_db.execute('select * from items where input_id=?', (s['input_id'],)).fetchone()
        if old is None or digest(old['text']) != s['database_text_sha256']:
            raise ValueError('original source missing or changed')
        origin = dict(old)
        entry = next((r for r in index if r['input_id'] == s['input_id'] and r.get('file')), None)
        if not entry:
            raise ValueError('missing archive index')
        if (entry['capture_utc'] != s['archive_capture_utc'] or entry['source_url'] != origin['source_uri']
                or entry['html_sha256'] != s['archive_html_sha256']
                or entry['archive_url'] != 'https://web.archive.org/web/' + entry['capture_utc'] + 'id_/' + entry['source_url']):
            raise ValueError('archive index differs from source and capture identity')
        body = archived_body(s, entry)
        timestamp = datetime.strptime(s['archive_capture_utc'], '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
        published = datetime.fromisoformat(s['archived_publication_time'].replace('Z', '+00:00'))
        report_time = datetime.fromisoformat(report['published_at'].replace('Z', '+00:00'))
        if timestamp < published or report_time >= published or timestamp.date().isoformat() != s['publication_day'] or published.date().isoformat() != s['publication_day']:
            raise ValueError('publication, report, and archive chronology not established')
        archive_url = 'https://web.archive.org/web/' + s['archive_capture_utc'] + '/' + origin['source_uri']
        cleaning = {'derivation': VERSION, 'original_id': s['input_id'], 'capture_utc': s['archive_capture_utc'],
                    'archive_html_sha256': s['archive_html_sha256'], 'removed_widget_sha256': s.get('removed_widget_sha256')}
        fields = {k: origin[k] for k in INHERITED}
        fields.update(source_uri=archive_url, text=body, text_page=None, text_article=None, content_sha256=digest(body),
                      text_chars=len(body), published_at=s['archived_publication_time'], publication_day=s['publication_day'],
                      page_day=s['publication_day'], retrieved_at=timestamp.isoformat(), day_source='archive_publisher', listing_day=None,
                      copy_of=None, supersedes=None, channel='historical_archive', source='archive', coverage='unverified', feed=0,
                      extra=None, cleaning=canonical(cleaning))
        if set(fields) != SCHEMA - {'input_id'}:
            raise ValueError('variant field mapping is incomplete')
        payload = {'derivation': VERSION, 'original_id': s['input_id'], 'capture_utc': s['archive_capture_utc'],
                   'archive_html_sha256': s['archive_html_sha256'], 'body_sha256': digest(body), 'fields': fields}
        variant_id = 'archive:' + digest(canonical(payload))
        fields['input_id'] = variant_id
        records.append({'original_id': s['input_id'], 'variant_id': variant_id, 'archive_url': archive_url,
                        'publisher_url': origin['source_uri'], 'capture_utc': s['archive_capture_utc'],
                        'body_sha256': digest(body), 'identity_payload_sha256': digest(canonical(payload)),
                        'inherited_unverified': list(INHERITED), 'split': s['split'], 'fields': fields})
    if len({r['variant_id'] for r in records}) != len(records):
        raise ValueError('duplicate variant identity')
    gold = json.loads((HERE / 'draft-gold-reconciled-three.json').read_text())
    mapped = {}
    for article in gold['articles']:
        record = next((r for r in records if r['original_id'] == article['input_id']), None)
        if not record or article['input_id'] in mapped:
            raise ValueError('gold-to-source map not one-to-one')
        for entry in article['entries'] + article['exclusions']:
            for span in entry['source_spans']:
                if span not in record['fields']['text']:
                    raise ValueError('reference span not found in variant body')
        article['original_input_id'] = article['input_id']
        article['input_id'] = record['variant_id']
        article['variant_body_sha256'] = record['body_sha256']
        mapped[record['original_id']] = record['variant_id']
    if set(mapped) != {r['original_id'] for r in records}:
        raise ValueError('gold source coverage differs')
    gold['status'] = 'AI-authored mapped draft; unresolved and unsigned; do not score'
    gold['mapping_note'] = 'IDs remapped to archive variants; the source standard and texts have not been reapproved.'
    source_db.close()
    output_dir.mkdir(parents=True)
    destination = sqlite3.connect(str(output_dir / 'items.sqlite'))
    destination.row_factory = sqlite3.Row
    destination.execute(schema_sql)
    placeholders = ','.join('?' for _ in columns)
    for record in records:
        destination.execute('insert into items (' + ','.join(columns) + ') values (' + placeholders + ')',
                            [record['fields'][k] for k in columns])
    destination.commit()
    lookup = bundle.item_lookup(destination)
    for record in records:
        found = lookup(record['variant_id'])
        fields = record['fields']
        if any(found[k] != fields[k] for k in ('title', 'publisher', 'publisher_type', 'category', 'publication_day', 'source_uri')):
            raise ValueError('reader lookup did not resolve archived source')
    destination.close()
    manifest = {'status': 'DRAFT: source and reference unapproved; no scoring', 'derivation': VERSION,
                'packet_sha256': hashlib.sha256(packet_path.read_bytes()).hexdigest(), 'articles': records}
    (output_dir / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (output_dir / 'reference-draft.json').write_text(json.dumps(gold, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(records)} distinct archived variants; {len(mapped)} references mapped; bundle lookup verified; no network')
    for r in records:
        print(r['original_id'], '=>', r['variant_id'], 'chars', r['fields']['text_chars'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--items', type=Path, required=True)
    ap.add_argument('--packet', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    try:
        build(args.items, args.packet, args.out)
    except (OSError, ValueError, KeyError, TypeError, IndexError, sqlite3.Error) as error:
        print('VARIANT BUILD REFUSED: ' + str(error), file=sys.stderr)
        raise SystemExit(1) from error


if __name__ == '__main__':
    main()
