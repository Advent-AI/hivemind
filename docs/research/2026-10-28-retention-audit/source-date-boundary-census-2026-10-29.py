"""Count conflicting source-day metadata among v38's handed-over items; not a date-error detector."""
import sqlite3

ITEMS = '/Users/lchingen/hivemind/poc/data/items-nvda-2026-07-01-10-27.sqlite'
VIEWS = '/Users/lchingen/hivemind/poc/data/english-v38-nvda-1w-2026-10-28/views.sqlite'
KNOWN = 'gnews:8d5c91ae833af14257a59b2b'

def has_different_dates(row):
    return bool(row[1] and row[2] and row[1] != row[2])

with sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True) as items, sqlite3.connect(f'file:{VIEWS}?mode=ro', uri=True) as views:
    ids = [row[0] for row in views.execute('select distinct input_id from handovers')]
    rows = [items.execute('select input_id, listing_day, page_day from items where input_id=?', (i,)).fetchone() for i in ids]
    if not rows or any(row is None for row in rows):
        raise ValueError('empty or missing input population')
    different = [row for row in rows if has_different_dates(row)]
    if not any(row[0] == KNOWN for row in different):
        raise ValueError('known differing-date control missing')
    known = next(row for row in rows if row[0] == KNOWN)
    equal_control = (known[0], known[1], known[1])
    if has_different_dates(equal_control):
        raise ValueError('equal-date negative control failed')
    print(f'handed-over inputs: {len(rows)}; both dates present and different: {len(different)}')
    for input_id, listing_day, page_day in different:
        print(input_id, listing_day, page_day)
