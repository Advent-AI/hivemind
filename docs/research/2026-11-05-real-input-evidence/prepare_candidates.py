"""List reproducible candidate articles for source review; this is not a benchmark or acceptance set."""
import hashlib
import json
import sqlite3
import sys

if len(sys.argv) != 2:
    raise SystemExit('usage: python3 prepare_candidates.py /absolute/path/to/items.sqlite')
conn = sqlite3.connect('file:' + sys.argv[1] + '?mode=ro', uri=True)
conn.row_factory = sqlite3.Row
windows = [('development', '2026-09-01', '2026-09-15'), ('held-out-candidates', '2026-10-01', '2026-10-15')]
selected, seen = [], set()
for group, start, end in windows:
    for category in ('T6', 'T7', 'T8'):
        rows = conn.execute('select input_id, publication_day, category, title, source_uri, object_identifiers, text from items '
                            'where feed=1 and publication_day between ? and ? and category=? and length(text) between 500 and 15000',
                            (start, end, category)).fetchall()
        eligible = [r for r in rows if any(o.get('value') == 'NVDA' for o in json.loads(r['object_identifiers'] or '[]'))]
        eligible.sort(key=lambda r: hashlib.sha256(('real-evidence-v1:' + r['input_id']).encode()).hexdigest())
        picked = 0
        for row in eligible:
            digest = hashlib.sha256(row['text'].encode()).hexdigest()
            if digest in seen:
                continue
            selected.append({'split': group, 'input_id': row['input_id'], 'date': row['publication_day'],
                             'category': row['category'], 'title': row['title'], 'source_uri': row['source_uri'],
                             'text_sha256': digest, 'status': 'candidate - source and dates not yet reviewed'})
            seen.add(digest)
            picked += 1
            if picked == 2:
                break
        if picked != 2:
            raise SystemExit(f'not enough NVDA items in {group} {category}: {picked}')
print(json.dumps({'description': 'Preliminary candidates, not accepted references; manual source/date/duplicate review required',
                  'selection': 'sha256(real-evidence-v1:<input_id>), 2/category/split', 'items': selected}, ensure_ascii=False, indent=2))
