"""A question closed by pull mode on a day without items is closed at the start of the next day (D251's day-start state, D54, D356):
the replay completes the day at the last sequence the day wrote, the closing's own sequence included, so the next day's items
are not shown a question that closed the day before. Driven through `replay.run` as the replay script calls it; no item, so no
provider is reached."""
import sqlite3
from pathlib import Path

from hivemind import config, dispatch, model, replay, universe
from hivemind.views import store

ROOT = Path(__file__).resolve().parents[1]
RUNGS = [{'label': 'Yes', 'condition': 'it ships'}, {'label': 'No', 'condition': 'it does not ship'}]


def test_a_question_closed_on_a_day_without_items_is_closed_when_the_next_day_starts(tmp_path):
    items = tmp_path / 'items.sqlite'
    with sqlite3.connect(items) as db:
        db.execute('create table items (input_id, publisher, published_at, publication_day, category, '
                   'source_uri, text, object_identifiers, feed, copy_of, klass)')
    views = str(tmp_path / 'views.sqlite')
    conn = store.open_db(views)
    dispatch.mark(conn, {'input_id': 'feed:item-1', 'publication_day': '2026-12-30'}, 1, 'handed_over')
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at='Model X',
                      question='Will NVIDIA ship Model X by 2026-12-31?', due_day='2026-12-31', year=2026, rungs=RUNGS, seq=1,
                      input_id='feed:item-1', created_at='2026-12-30T09:00:00+00:00')
    store.complete_day(conn, '2026-12-30', 1, '2026-12-30T23:00:00')
    conn.commit()
    conn.close()
    replay.run(testdb_path=str(items), views_path=views, archive=model.Archive(str(tmp_path / 'archive.sqlite')),
               cfg=config.load(ROOT / 'poc/config/poc-v118.json'), universe=universe.load(ROOT / 'poc/universe.json'),
               from_day='2026-12-31', until_day='2027-01-01', log=lambda *args: None)
    conn = store.open_db(views)
    assert not store.is_open(conn, 'v1')                                           # closed on 2026-12-31, a day with no item
    assert [v['view_id'] for v in store.views_open_at_day_start(conn, ['NVDA'], '2027-01-01')] == []
