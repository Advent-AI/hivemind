"""The store states and calls the bound resolver is checked on (live-service/OPERATING-CONTRACT.md, row 3 and its product-facing
contract; proofs 2c and 2d). Shared by the recorder of today's outputs (`record_bound_baseline.py`, run once before the change) and
`test_bound_resolver.py`, so both run exactly the same calls.

Four states: a finished store (the sealed run through 2026-08-15: nothing after its last completed day), a store with work after its
last completed day (the running product's served store: 2026-08-29's steps after 2026-08-28), a first-day store (steps, no completed
day) and an empty store (the tables, no steps, no completed day). The two real stores are opened read-only."""
import hashlib
import json
import os
import shutil

from hivemind import bundle, dispatch, search, service
from hivemind.views import store

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FINISHED = os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite')
PARTIAL = os.path.join(ROOT, 'poc', 'data', 'served-2026-10-28-v34-nvda-3m-through-0828', 'views.sqlite')
STATES = {'finished': {'past': '2026-08-01', 'future': '2026-09-30', 'since': '2026-07-01'},
          'partial': {'past': '2026-08-20', 'future': '2026-09-30', 'since': '2026-08-01'},
          'first_day': {'past': '2026-09-01', 'future': '2026-09-30', 'since': '2026-08-01'},
          'empty': {'past': '2026-09-01', 'future': '2026-09-30', 'since': '2026-08-01'}}


def open_state(name, folder):
    """A connection to the state's store; the real stores are copied to `folder` first (by the backup API) so nothing writes beside
    them, then opened read-only."""
    if name in ('finished', 'partial'):
        source = service.open_ledger(FINISHED if name == 'finished' else PARTIAL)
        target_path = os.path.join(folder, f'{name}.sqlite')
        import sqlite3
        target = sqlite3.connect(target_path)
        source.backup(target)
        target.close()
        source.close()
        return service.open_ledger(target_path)
    path = os.path.join(folder, f'{name}.sqlite')
    conn = store.open_db(path)
    if name == 'first_day':
        dispatch.mark(conn, {'input_id': 'gnews:first', 'publication_day': '2026-09-01'}, 1, 'handed_over')
    conn.commit()
    conn.close()
    return service.open_ledger(path)


def first_view(conn):
    row = conn.execute('select view_id, created_seq from views order by created_seq limit 1').fetchone()
    return (row['view_id'], row['created_seq']) if row else ('v1', 0)


def calls(conn, state):
    """(name, bound kind, a function of no arguments) for every public function that takes a date, with an omitted, a past and a
    future upper bound; and the ranges."""
    days = STATES[state]
    view_id, created_seq = first_view(conn)
    item_of = bundle.item_lookup(None)
    out = []
    for kind, bound in (('omitted', None), ('past', days['past']), ('future', days['future'])):
        out += [
            ('service.summaries', kind, lambda b=bound: service.summaries(conn, b, include_closed=True)),
            ('service.views', kind, lambda b=bound: service.views(conn, None, b, include_closed=True)),
            ('service.view', kind, lambda b=bound: service.view(conn, view_id, b)),
            ('service.evidence', kind, lambda b=bound: service.evidence(conn, view_id, b)),
            ('service.record', kind, lambda b=bound: service.record(conn, view_id, b)),
            ('service.evaluate', kind, lambda b=bound: service.evaluate(conn, view_id, '>=', 1.0, b)),
            ('service.history', kind, lambda b=bound: service.history(conn, view_id, days['since'], b)),
            ('service.changes', kind, lambda b=bound: service.changes(conn, days['since'], b)),
            ('bundle.days', kind, lambda b=bound: bundle.days(conn, b)),
            ('bundle.not_judged', kind, lambda b=bound: bundle.not_judged(conn, view_id, created_seq, b)),
            ('bundle.view_bundle', kind, lambda b=bound: bundle.view_bundle(conn, item_of, view_id, b)),
            ('bundle.thesis_bundles', kind, lambda b=bound: bundle.thesis_bundles(conn, None, [view_id], b)),
            ('bundle.library', kind, lambda b=bound: bundle.library(conn, None, b)),
            ('search.search', kind, lambda b=bound: search.search(conn, None, 'revenue data center', 10, b, semantic=False)),
        ]
    out += [('service.changes', 'since equal to end', lambda: service.changes(conn, days['past'], days['past'])),
            ('service.history', 'from equal to to', lambda: service.history(conn, view_id, days['past'], days['past']))]
    return out


def range_after_end_calls(conn, state):
    """A start after an explicit, completed end: refused for both ranges (council round 124). Not in the recorded baseline."""
    days = STATES[state]
    view_id, _ = first_view(conn)
    out = [('service.changes', 'since after end', lambda: service.changes(conn, days['future'], days['past'])),
           ('service.history', 'from after to', lambda: service.history(conn, view_id, days['future'], days['past']))]
    return out


def outcome(call):
    """('ok', sha256 of the canonical JSON) or ('error', the exception's type and message)."""
    try:
        value = call()
    except Exception as error:                                   # noqa: BLE001 - the recorded outcome is the error itself
        return ['error', f'{type(error).__name__}: {error}']
    return ['ok', hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()]
