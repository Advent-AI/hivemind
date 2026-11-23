"""List every view a production run opened by itself (none is seeded under poc-v118), for the matching read under MATCHING-v2.md, in
the shape `clean-arch/unseeded-2026-11-10/extract_opened.py` writes for the clean draws: run, id, the input where it opened,
description (the view's question), outcome (what the view looks at), period (its year and due day).

  python3 extract_opened_prod.py <label> <run folder> <output.json>
"""
import json, sqlite3, sys
from pathlib import Path

label, folder, output = sys.argv[1:4]
conn = sqlite3.connect(f"file:{Path(folder) / 'views.sqlite'}?mode=ro", uri=True)
seeded = conn.execute("select count(*) from views where lower(substr(created_from_input, 1, 5))='seed:'").fetchone()[0]
if seeded:
    raise SystemExit(f'{folder}: {seeded} seeded views: refused (production as it now runs opens its own)')
rows = [{'run': label, 'id': view_id, 'article': created_from_input, 'description': question, 'outcome': looks_at,
         'period': f'year {year}; due {due_day}'}
        for view_id, created_from_input, question, looks_at, year, due_day in
        conn.execute('select view_id, created_from_input, question, looks_at, year, due_day from views order by created_seq')]
Path(output).write_text(json.dumps(rows, indent=1, ensure_ascii=False))
print(f'{label}: {len(rows)} opened views written to {output}')
