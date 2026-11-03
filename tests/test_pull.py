"""Closing at the due day (D54, D356): pull mode freezes a due view where its state stands and closes it; the closing record names
the frozen rung, and a view that was never judged closes with "no data to verify" (AGENTS §8). Views not yet due stay open, and a
closing is dated on the day it happens, also on a day without items."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import dispatch, pull, service  # noqa: E402
from hivemind.views import store  # noqa: E402

RUNGS = [{'label': 'Yes', 'condition': 'it ships'}, {'label': 'No', 'condition': 'it does not ship'}]


def make_view(conn, view_id, due_day):
    store.create_view(conn, view_id=view_id, object_id='ABC', object_kind='asset', kind='asset', looks_at='Model X',
                      question=f'Will ABC ship Model X by {due_day}?', due_day=due_day, year=2026, rungs=RUNGS, seq=1,
                      input_id='feed:item-1', created_at='2026-07-01T09:00:00+00:00')


def test_due_views_freeze_at_their_last_rung_or_close_with_no_data_and_later_views_stay_open(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    make_view(conn, 'v1', '2026-12-31')
    make_view(conn, 'v2', '2026-12-31')
    make_view(conn, 'v3', '2027-06-30')
    store.insert(conn, 'judgements', view_id='v1', seq=2, input_id='feed:item-1', rung=1, reasons='shipping confirmed', changed=1)
    store.insert(conn, 'judgements', view_id='v1', seq=3, input_id='feed:item-2', rung=2, reasons='launch slipped', changed=1)
    closed = pull.end_of_day(conn, '2027-01-01', 4)
    assert closed == ['v1', 'v2']
    reasons = {r['view_id']: r['reason'] for r in conn.execute("select view_id, reason from view_switches where open=0")}
    assert reasons['v1'] == 'due 2026-12-31, frozen on 2027-01-01 at rung 2 No'
    assert reasons['v2'] == f'due 2026-12-31, closed on 2027-01-01 with no judgement: {pull.NO_DATA}'
    assert store.is_open(conn, 'v3') and not store.is_open(conn, 'v1') and not store.is_open(conn, 'v2')
    assert pull.end_of_day(conn, '2027-01-02', 5) == []          # a closed view is not closed again


def test_a_closing_on_a_day_without_items_is_dated_on_that_day_not_the_day_before(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    dispatch.mark(conn, {'input_id': 'feed:item-1', 'publication_day': '2026-12-30'}, 1, 'handed_over')
    make_view(conn, 'v1', '2026-12-31')
    assert pull.end_of_day(conn, '2026-12-31', 1) == ['v1']      # no item on 2026-12-31: the day's last number is still 2026-12-30's
    assert service.is_open_as_of(conn, 'v1', '2026-12-30') and not service.is_open_as_of(conn, 'v1', '2026-12-31')
