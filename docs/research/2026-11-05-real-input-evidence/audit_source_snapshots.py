"""Compare archived publisher timestamps with the supplied corpus; no network calls."""
import datetime
import email.utils
import gzip
import json
import re
import sqlite3
import sys
from pathlib import Path

from bs4 import BeautifulSoup

if len(sys.argv) != 2 or not Path(sys.argv[1]).is_absolute():
    raise SystemExit('usage: audit_source_snapshots.py /absolute/items.sqlite')
index = json.loads((Path(__file__).parent / 'source-snapshots/draft-archive-index.json').read_text())
normalize = lambda s: re.sub(r'\s+', ' ', s).strip()

def date(value):
    try:
        return datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return email.utils.parsedate_to_datetime(value)

results = []
with sqlite3.connect(Path(sys.argv[1]).resolve().as_uri() + '?mode=ro', uri=True) as conn:
    for record in index:
        if not record['status'].startswith('downloaded'):
            results.append({'input_id': record['input_id'], 'status': record['status']})
            continue
        raw = gzip.decompress(Path(record['file']).read_bytes())
        soup = BeautifulSoup(raw, 'html.parser')
        db_row = conn.execute('select published_at,text from items where input_id=?', (record['input_id'],)).fetchone()
        if not db_row:
            raise SystemExit('missing article: ' + record['input_id'])
        times = dict(record.get('metadata') or {})
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                item = json.loads(script.get_text())
            except (ValueError, TypeError):
                continue
            if isinstance(item, dict) and item.get('datePublished'):
                times['ld_datePublished'] = item['datePublished']
        published = times.get('article:published_time') or times.get('ld_datePublished')
        row = {'input_id': record['input_id'], 'capture_utc': record['capture_utc'], 'database_published_at': db_row[0],
               'source_published_at': published, 'comparison': 'unavailable'}
        if published:
            delta = (date(published) - date(db_row[0])).total_seconds()
            row.update(comparison='source later' if delta > 0 else 'same' if delta == 0 else 'source earlier', delta_seconds=delta)
        results.append(row)
print(json.dumps({'status': 'source timestamps are publisher metadata, not proof of content immutability', 'results': results}, indent=2))
