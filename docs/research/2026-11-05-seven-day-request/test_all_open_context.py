"""Every open question committed before an item reaches both split requests."""
import copy
import sqlite3
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / 'src')]
import split_seven_day_poc as p  # noqa: E402
from hivemind import config, extraction, testdb, universe  # noqa: E402
from hivemind.views import matching, store, writing  # noqa: E402


def create(conn, view_id, object_id, kind, seq):
    store.create_view(conn, view_id=view_id, object_id=object_id, object_kind='theme' if kind == 'theme' else 'company',
                      kind=kind, looks_at=f'{object_id} subject', question=f'What will {object_id} report?',
                      due_day='', year='2026', rungs=[], seq=seq, input_id=f'item-{seq}', created_at='2026-08-29T00:00:00')


def test_all_open_respects_creation_and_closing_sequence(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    create(conn, 'v1', 'NVDA', 'asset', 1)
    create(conn, 'v2', 'research:unknown', 'asset', 1)
    create(conn, 'v3', 'research:policy', 'theme', 1)
    create(conn, 'v4', 'TSM', 'asset', 10)
    store.close_view(conn, 'v2', 'closed', 'test', 8)
    store.close_view(conn, 'v3', 'closed later', 'test', 11)
    conn.commit()
    assert [v['view_id'] for v in p.latest_library(conn, 10)] == ['v1', 'v3']
    assert [v['view_id'] for v in p.latest_library(conn, 11)] == ['v1', 'v3', 'v4']
    assert [v['view_id'] for v in p.latest_library(conn, 12)] == ['v1', 'v4']


def test_an_untagged_new_company_is_read_by_both_calls_and_accepts_next_article_evidence():
    items = testdb.open_db(str(p.INPUT))
    first_id = 'gnews:bf364ee004415128400cd52e'
    later_id = 'gnews:37f2a2391b7dce0b35fb82c1'
    first = testdb.item_of(items.execute('select * from items where input_id=?', (first_id,)).fetchone())
    later = testdb.item_of(items.execute('select * from items where input_id=?', (later_id,)).fetchone())
    assert 'IREN' not in {x['value'] for x in later['object_identifiers']}
    folder = ROOT / 'poc/data/split-fresh-seven-day-matching-v4-2026-11-05/items/1321'
    saved = p.read(folder / 'handover.json')
    c = copy.deepcopy(saved['candidates'][0])
    c['object'] = 'IREN'
    evidence = [copy.deepcopy(e) for e in saved['evidence'] if c['id'] in e['links']]
    assert evidence and all(e['quote'] in first['text'] for e in evidence)
    quote = 'IREN reported fiscal fourth-quarter revenue of $137.2 million, while AI Cloud revenue jumped 110% sequentially to $70.5 million.'
    assert quote in later['text']
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    with tempfile.TemporaryDirectory(prefix='all-open-writer-') as d:
        dest = Path(d) / 'views.sqlite'
        with sqlite3.connect(p.prior.SNAP.resolve().as_uri() + '?mode=ro', uri=True) as source, sqlite3.connect(dest) as target:
            source.backup(target)
        conn = store.open_db(str(dest))
        seq = store.next_sequence(conn)
        p.register_subjects(uni, [c], conn)
        h = extraction.Handover(evidence, [c], [], 0, '', False, 0.0)
        checked = matching.Checked({c['id']: ('new', None, [])}, {}, [], {})
        written = writing.write(conn, uni, seq, first, h, checked, {})
        conn.commit()
        view_id = written.new_views[c['id']]
        shown = p.latest_library(conn, seq + 1)
        assert view_id in {v['view_id'] for v in shown}
        _, requests = p.item_requests(cfg, uni, later, shown)
        assert all(('  - ' + view_id + ' ') in requests[arm][1] for arm in ('a', 'b'))
        b = {'evidence': [{'id': 'b1', 'quote': quote, 'one_line': 'IREN reported quarterly and AI Cloud revenue.',
                           'speaker': 'Article author', 'original_who': 'IREN', 'original_day': '', 'tier': 'fact',
                           'event_time': '', 'links': [view_id]}]}
        later_handover = p.build_handover(later, shown, uni, {'questions': []}, b, {'candidates': [], 'evidence': []})
        later_checked = matching.Checked({}, {('e1', view_id): ('new', None, '')}, [], {})
        later_written = writing.write(conn, uni, seq + 1, later, later_handover, later_checked, {})
        conn.commit()
        stored = later_written.evidence_ids['e1']
        assert view_id in store.views_linked_to(conn, stored)
        assert store.evidence(conn, stored)['quote'] == quote
