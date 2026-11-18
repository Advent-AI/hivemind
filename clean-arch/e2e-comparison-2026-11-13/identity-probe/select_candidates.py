"""D463's fresh-article selection, step 1 ($0): the items Step 1 could receive (feed = 1, NVDA among the tickers, text present, not a copy
or a superseded item; runner.selected_items' rule) published 2026-07-15 to 2026-09-04 (after the clean window; before the 2026-09-05..07
acceptance set, D386), matched by one pattern per probe category, in an order fixed by a seed. The patterns only find candidates; a blind
reader decides fit and the expected behaviour (`reader-brief.md`), and the first four fits per category in this order form the probe set.

  python3 select_candidates.py > candidates.json
"""
import json
import random
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ITEMS = ROOT / 'poc/data/items-nvda-2026-07-01-10-27.sqlite'
SEED = 20261113
PATTERNS = {
    'T1 another year of a shared quantity': lambda t: (re.search(r'(?i)capital expenditure|capex|capital spending|data[- ]center spending', t)
        and re.search(r'(?i)\b2027\b|next year', t) and re.search(r'(?i)\b2026\b|this year', t)
        and re.search(r'(?i)hyperscaler|Microsoft|Alphabet|Amazon|\bMeta\b', t)),
    'T2 an unsigned single deal beside a programme': lambda t: re.search(
        r'(?i)nvidia[^.]{0,80}(in talks|negotiat|nearing a deal|in discussions|considering|weighing)[^.]{0,80}(invest|stake|guarantee|backstop|financ|lease)', t),
    'T3 one price compared across two years': lambda t: (re.search(r'(?i)(DRAM|HBM|NAND|memory|wafer|contract)[^.]{0,60}price', t)
        and re.search(r'(?i)\b2027\b[^.]{0,80}(compared|versus|vs\.?|from|than|year[- ]over[- ]year)|(rise|increase|grow|climb|fall)[^.]{0,40}\b2027\b', t)),
    'T4 a statement that must merge into an open thesis': lambda t: re.search(
        r'(?i)(\$5 billion|5 billion)[^.]{0,60}intel|intel[^.]{0,60}(\$5 billion|5 billion)|firmus|vera rubin[^.]{0,80}(delay|push|slip|on track|on schedule)|(big four|hyperscalers)[^.]{0,80}(spend|capex|capital expenditure)[^.]{0,60}\b2026\b|h100[^.]{0,60}(rental|spot|per hour)', t),
}


def eligible(row):
    tags = [x.get('value') for x in json.loads(row['object_identifiers'] or '[]') if x.get('kind') == 'ticker']
    return 'NVDA' in tags and row['text'] and row['feed'] == 1 and not row['copy_of'] and not row['supersedes']


def main():
    conn = sqlite3.connect(f'file:{ITEMS}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    rows = [r for r in conn.execute("select * from items where publication_day between '2026-07-15' and '2026-09-04' order by input_id") if eligible(r)]
    out = {'pool': len(rows), 'seed': SEED, 'categories': {}}
    for name, pattern in PATTERNS.items():
        hits = [r for r in rows if pattern(r['text'])]
        order = random.Random(f'{SEED}:{name}').sample(hits, len(hits))
        out['categories'][name] = {'hits': len(hits), 'order': [{'input_id': r['input_id'], 'day': r['publication_day'], 'title': r['title'],
                                                                 'chars': len(r['text'])} for r in order[:12]]}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
