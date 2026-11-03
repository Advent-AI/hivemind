"""Seed questions (D208 step one, D253): `seeding.seed_views` writes a seed file's questions into a ledger before the first day, with
ladder, key, open switch and the driver's dependency on its root; a second call writes nothing; a seed is listed to the extraction and
the placer like any open question and carries the keyed 'takes' line; a candidate for the same quantity is found by exact key. Real
ledger on a temporary path; the repository's NVDA seed file."""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import placement, seeding  # noqa: E402
from hivemind.views import store  # noqa: E402

SEED = os.path.join(ROOT, 'poc', 'seeds', 'nvda-2026-07-01.json')


def test_seeding_writes_every_question_once_with_key_ladder_switch_and_dependency(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    written = seeding.seed_views(conn, SEED, created_at='2026-07-01T00:00:00Z')
    questions = json.load(open(SEED))['questions']
    assert written == [q['view_id'] for q in questions] and len(written) == 10
    assert all(re.fullmatch(r'v\d+', q['view_id']) for q in questions)                      # the judge parses the theme ids it showed as v<N> (judging.themes_shown_in); the first seeded run failed on 's9'
    assert sorted(store.open_views(conn)) == sorted(written)                                 # every seed is open
    assert store.view_key(conn, 'v1')['measure'] == 'total_revenue' and store.view_key(conn, 'v1')['period_end'] == '2027-01-31'
    assert [r['label'] for r in conn.execute("select label from rungs where view_id='v1' order by position")][0] == 'Strongly bullish'
    assert conn.execute("select depends_on from dependencies where view_id='v2'").fetchone()['depends_on'] == 'v1'   # the driver feeds its root (D208)
    assert conn.execute("select created_from_input, created_seq from views where view_id='v4'").fetchone()[:] == ('seed:nvda-2026-07-01.json', 0)
    assert seeding.seed_views(conn, SEED, created_at='2026-07-02T00:00:00Z') == []            # a resumed run seeds nothing twice
    assert conn.execute('select count(*) from views').fetchone()[0] == 10


def test_a_seed_is_shown_like_an_open_question_and_takes_its_measure(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    seeding.seed_views(conn, SEED, created_at='2026-07-01T00:00:00Z')
    shown = store.views_open_at_day_start(conn, ['NVDA'], '2026-07-01')
    assert sorted(v['view_id'] for v in shown) == sorted(f'v{n}' for n in range(1, 11))       # before the first completed day the open questions are the seeds
    view = dict(next(v for v in shown if v['view_id'] == 'v2'), key=store.view_key(conn, 'v2'), groups=[])
    assert placement.takes(view) == "takes: segment_revenue figures, guidance, estimates and revisions for Data Center, this question's period 2026-02-01..2027-01-31"   # D268, D274
    candidate = {'object': 'NVDA', 'measure': 'total_revenue', 'scope': '', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'GAAP', 'unit': 'USD', 'event_type': 'n/a',
                 'scope_source': 'none', 'key_version': 2}                                     # the key the pipeline writes for an article-born candidate
    assert store.exact_key_views(conn, candidate) == ['v1']                                  # an article-born FY2027 revenue candidate merges into the seed (D190)


def test_a_changed_seed_under_an_existing_id_is_refused(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    seeding.seed_views(conn, SEED, created_at='2026-07-01T00:00:00Z')
    changed = json.load(open(SEED))
    changed['questions'][0]['question'] = 'Something else?'
    path = tmp_path / 'changed.json'
    path.write_text(json.dumps(changed))
    try:
        seeding.seed_views(conn, str(path), created_at='2026-07-02T00:00:00Z')
        assert False, 'a changed seed under an existing id must be refused'
    except ValueError as error:
        assert 'v1' in str(error)


SEED_V2 = os.path.join(ROOT, 'poc', 'seeds', 'nvda-2026-07-01-v2.json')


def test_second_seed_file_traces_every_watch_seed_to_the_universe_and_seeds_whole(tmp_path):
    """D208: keys by code from the watch list. Every seed whose source says 'watch:' matches a universe watch entry of its object by
    measure (and scope and event type when the entry names them); ids run v1..vN without gaps; the file seeds whole; a Vera CPU revenue
    candidate keyed from the watch list merges into its seed by exact key."""
    import re as _re
    from hivemind import universe as _universe
    seed = json.load(open(SEED_V2))
    watch = _universe.load(os.path.join(ROOT, 'poc', 'universe.json'))
    assert [q['view_id'] for q in seed['questions']] == [f'v{n}' for n in range(1, len(seed['questions']) + 1)]
    for q in seed['questions']:
        assert q['source'], q['view_id']
        if q['source'].startswith('watch:'):
            entries = watch.watch_list(q['object_id'])
            k = q['key']
            assert any(e['measure'] == k['measure'] and (not e.get('scope') or _universe.scope_key(e['scope']) == _universe.scope_key(k['scope']))
                       and (not e.get('event_type') or e['event_type'] == k['event_type']) for e in entries), (q['view_id'], k)
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    assert len(seeding.seed_views(conn, SEED_V2, created_at='2026-07-01T00:00:00Z')) == len(seed['questions'])
    candidate = {'object': 'NVDA', 'measure': 'product_revenue', 'scope': 'Vera', 'period_start': '2026-02-01', 'period_end': '2027-01-31', 'basis': 'GAAP',
                 'unit': 'USD', 'event_type': 'n/a', 'scope_source': 'watch', 'key_version': 2}
    vera_seed = next(q['view_id'] for q in seed['questions'] if q['key']['measure'] == 'product_revenue' and q['key'].get('scope') == 'Vera')
    assert store.exact_key_views(conn, candidate) == [vera_seed]       # the id follows the file (2026-11-01: v20 became v19 when the rack-price seed was removed)
