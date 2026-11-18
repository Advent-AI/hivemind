"""D476's source check ($0): for each of the eleven theses the judge's first pass refused on the full run, the article that opened it and the
library at that step (phase 1, no thesis shown), and separately the thesis as opened (phase 2). Cases are numbered in an order fixed by a seed so
the draw and thesis ids are not shown; the key stays beside this script.

  python3 build_packets.py      # writes packet-phase1.json, packet-phase2.json, key.json
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'refused-shapes'))
import shape_accounts  # noqa: E402

ITEMS = HERE.parents[2] / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
REFUSED = [('c1', 'clean-10'), ('c1', 'clean-11'), ('c1', 'clean-12'), ('c1', 'clean-13'), ('c1', 'clean-15'), ('c1', 'clean-2'),
           ('c2', 'clean-6'), ('c3', 'clean-10'), ('c3', 'clean-3'), ('c3', 'clean-9'), ('c2', 'clean-10')]


def main():
    import sqlite3
    items = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    order = random.Random(20261113).sample(REFUSED, len(REFUSED))
    phase1, phase2, key = [], [], []
    for number, (draw, thesis_id) in enumerate(order, 1):
        conn = sqlite3.connect(f'file:{shape_accounts.TRACES[draw]}?mode=ro', uri=True)
        sequence, request, _answer, thesis = shape_accounts.opening(draw, thesis_id)
        input_id, before = conn.execute('select input_id, before_state from trace where sequence = ?', (sequence,)).fetchone()
        row = items.execute('select publication_day, publisher, title, text from items where input_id = ?', (input_id,)).fetchone()
        library = [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in json.loads(before)]
        phase1.append({'case': number, 'article': {'input_id': input_id, 'publication_day': row['publication_day'], 'publisher': row['publisher'],
                       'title': row['title'], 'text': row['text']}, 'library_before': library})
        phase2.append({'case': number, 'thesis': {k: thesis[k] for k in ('description', 'outcome', 'period')}})
        key.append({'case': number, 'draw': draw, 'thesis': thesis_id, 'sequence': sequence, 'input_id': input_id})
        print(number, draw, thesis_id, sequence, input_id, row['publication_day'], row['title'][:70])
    for name, data in (('packet-phase1.json', phase1), ('packet-phase2.json', phase2), ('key.json', key)):
        (HERE / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n')


if __name__ == '__main__':
    main()
