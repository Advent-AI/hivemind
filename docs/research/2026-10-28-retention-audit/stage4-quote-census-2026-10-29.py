"""Compare stored original quotes to what the historical step-4 experiment sent."""
import copy
import json
import sqlite3
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind/poc')
PREPARED = ROOT / 'reports/2026-10-27-stage34-gold/fresh2/prepared.json'
LEDGER = ROOT / 'data/english-v29-nvda-3m-2026-10-27/views.sqlite'
cases = json.loads(PREPARED.read_text())
if not cases:
    raise ValueError('no cases')
observations, clipped, affected, ids, clipped_ids = 0, 0, set(), set(), set()
before_bytes = after_bytes = 0
with sqlite3.connect(f'file:{LEDGER}?mode=ro', uri=True) as db:
    for name, case in cases.items():
        full_payload = copy.deepcopy(case['payload'])
        before_bytes += len(json.dumps(case['payload'], ensure_ascii=False, separators=(',', ':')).encode())
        for piece in full_payload['stored_pieces']:
            found = db.execute('select quote from evidence where evidence_id=?', (piece['id'],)).fetchone()
            if not found:
                raise ValueError(f'missing {piece["id"]}')
            quote, sent = found[0] or '', piece['quote']
            if not quote.startswith(sent):
                raise ValueError(f'not a stored quote prefix: {name} {piece["id"]}')
            observations += 1
            ids.add(piece['id'])
            if len(quote) > len(sent):
                clipped += 1
                affected.add(name)
                clipped_ids.add(piece['id'])
            if name == 'F03' and piece['id'] == 'e121':
                assert len(sent) == 300 and 'in memory' in quote[300:]
            piece['quote'] = quote
            if name == 'F03' and piece['id'] == 'e121':
                assert 'in memory' in piece['quote']
        after_bytes += len(json.dumps(full_payload, ensure_ascii=False, separators=(',', ':')).encode())
if not observations or 'F03' not in affected or 'e121' not in clipped_ids:
    raise ValueError('known clipped-quote control missing')
print(f'cases {len(cases)}, cases with clipped quote {len(affected)}')
print(f'quote observations {observations}, clipped {clipped}; unique pieces {len(ids)}, unique clipped pieces {len(clipped_ids)}')
print(f'payload bytes original {before_bytes}, restored {after_bytes}, increase {after_bytes - before_bytes}')
