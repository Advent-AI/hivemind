"""Every dependency row in every stored ledger under poc/data, classed by the writer that left it ($0; council round 30).

Two writers have ever written the table (`git log -S"'dependencies'"`: the seeding module, D253; the writer step from a matching
answer). A row of the first carries the seeding module's marks (sequence 0, direction 'last_end', on a question created from a
seed file); a row of the second sits at an article's sequence on a question opened from an article, with a direction label of the
matching vocabulary (English or its earlier Chinese form). Anything else is counted as "other". Reads only.

What the count covers: every SQLite file under poc/data whose name contains "views" (snapshot folders included), by these marks.
It does not identify a writer beyond its marks, and it says nothing of ledgers kept elsewhere.

  python3 edge_inventory.py
"""
import collections
import json
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import vocabulary  # noqa: E402

MATCHING_LABELS = set(vocabulary.DIRECTIONS) | {'对方第一格是看多', '对方最后一格是看多', '同向', '反向'}


def family(row):
    seeded = (row['origin'] or '').lower().startswith('seed:')
    if seeded and row['seq'] == 0 and row['direction'] == 'last_end':
        return 'seeding module'
    if not seeded and row['seq'] > 0 and row['direction'] in MATCHING_LABELS:
        return 'matching answer, at the article that opened its question' if row['seq'] == row['opened'] else 'matching answer, at a later article'
    return 'other'


def main():
    stores, counts, with_rows, empty, others, waiting = 0, collections.Counter(), 0, 0, [], 0
    for folder, _, files in os.walk(ROOT / 'poc/data'):
        for name in files:
            if not (name.endswith('.sqlite') and 'views' in name):
                continue
            stores += 1
            db = sqlite3.connect(f'file:{Path(folder) / name}?mode=ro', uri=True)
            db.row_factory = sqlite3.Row
            if not db.execute("select 1 from sqlite_master where name = 'dependencies'").fetchone():
                continue
            rows = db.execute('select d.*, (select created_from_input from views v where v.view_id = d.view_id) as origin, '
                              '(select created_seq from views v where v.view_id = d.view_id) as opened from dependencies d').fetchall()
            waiting += sum(1 for row in rows if not row['depends_on'])
            empty += not rows
            with_rows += bool(rows)
            for row in rows:
                counts[family(row)] += 1
                if family(row) == 'other':
                    others.append(str(Path(folder).relative_to(ROOT)))
    out = {'ledgers_scanned': stores, 'ledgers_with_rows': with_rows, 'ledgers_with_the_table_and_no_row': empty, 'rows_by_writer': dict(counts), 'rows_waiting_for_a_year': waiting, 'ledgers_with_other_rows': sorted(set(others)),
           'covers': 'SQLite files under poc/data whose name contains "views", snapshot folders included; rows classed by their marks only'}
    (Path(__file__).parent / 'edge-inventory.json').write_text(json.dumps(out, indent=1) + '\n')
    print(out)


if __name__ == '__main__':
    main()
