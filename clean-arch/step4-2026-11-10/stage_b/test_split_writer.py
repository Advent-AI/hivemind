"""The period split's writer and readers (splitting/DESIGN.md v4 §0b and §0c, D616) on the real stored topic c1/clean-4 (the five
largest hyperscalers' capex, 2026 and 2027), its outcomes built by the split step from a fake model; nothing is sent."""
import importlib.util
import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(HERE.parent / 'ladder'), str(HERE.parents[1] / 'e2e-2026-11-09'), str(ROOT / 'src')]
import ladder_adapter  # noqa: E402
import ladder_split  # noqa: E402
import ladder_step  # noqa: E402
import stored_judgements  # noqa: E402
import test_ladder_split as split_case  # noqa: E402
from test_ladder_adapter import FIRST_SEND, fake_judge, no_credentials  # noqa: E402,F401
from hivemind import bundle, live_lock, service  # noqa: E402
from hivemind.views import store  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load('preflight', ROOT / 'scripts' / 'preflight.py')


def split_outcome(years):
    """The split step's outcome for c1/clean-4 with each year's answers as given, and each written year's view as the runner builds
    it (`ladder_step.write_view`)."""
    outcome, _ = split_case.run(split_case.FakeModel([split_case.SPLIT], years))
    for child in outcome['children'].values():
        child['view'] = (ladder_step.write_view(child['answer']['ladder'], child['passage'], thesis=split_case.CASE['thesis'],
                                                article_day=split_case.DAY, company='NVDA', research_list=split_case.RESEARCH_LIST)
                         if child['status'] == 'ladder' else None)
    return json.loads(ladder_step.as_json(outcome))         # as the runner writes it to outcomes.jsonl and the writer reads it back


MODEL_PARTS = [{'part': 'The roughly $1.3 trillion expected for 2027', 'why': 'A different year.'},
               {'part': "Oracle's share of the total, and the comparison with 2027", 'why': 'A second figure and a comparison.'}]


def with_parts(text, parts):
    answer = json.loads(text)
    answer['ladder']['not_judged'] = parts
    return json.dumps(answer)


BOTH = {'2026': [split_case.ladder_text('2026')], '2027': [split_case.ladder_text('2027')]}
BOTH_WITH_PARTS = {'2026': [with_parts(split_case.ladder_text('2026'), MODEL_PARTS)], '2027': [split_case.ladder_text('2027')]}
ONE = {'2026': [with_parts(split_case.ladder_text('2026'), MODEL_PARTS)],
       '2027': [split_case.decline('no_main', 'The 2027 plan names no single total.')]}
TWICE = {'2026': [split_case.ladder_text('2026')], '2027': [split_case.ladder_text('2026'), split_case.ladder_text('2026')]}
NONE = {'2026': [split_case.decline('no_main', 'none main')], '2027': [split_case.decline('no_main', 'none main')]}


@pytest.fixture
def writer(tmp_path):
    runner = ladder_adapter.LadderAdapter(tmp_path / 'views.sqlite', tmp_path / 'archive.sqlite', tmp_path / 'ledger.jsonl',
                                          transport=fake_judge, cap_usd=1.0)
    yield runner, tmp_path / 'views.sqlite'
    runner.close()


def write(runner, outcome):
    runner.open_thesis('clean-4', outcome, 1, 1, split_case.DAY, 'gnews:capex', 'test')
    runner.conn.commit()


def rows(path):
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        return conn.execute('select period, view_id, status, reason from clean_ladders order by period').fetchall()


def stored_parts(path, view_id):
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        return json.loads(conn.execute('select checked_answer from clean_ladders where view_id = ?', (view_id,)).fetchone()[0])['ladder']['not_judged']


def test_both_years_written_give_two_views_and_one_row_per_attempt(writer):
    runner, path = writer
    write(runner, split_outcome(BOTH))
    assert rows(path) == [('', None, 'split', None), ('2026', 'v042026', 'ladder', None), ('2027', 'v042027', 'ladder', None)]
    assert runner.mapping['clean-4'] == ['v042026', 'v042027']
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        assert [r[0] for r in conn.execute('select year from views order by view_id')] == ['2026', '2027']
    assert stored_parts(path, 'v042026') == [] and stored_parts(path, 'v042027') == []           # code adds nothing when both are written


def test_with_both_years_written_the_model_s_own_parts_pass_unchanged_even_when_they_name_the_other_year(writer):
    """Whether a left-out part is the other year's quantity is meaning (746 of 3,335 stored parts name a year, most of them not the
    question's year, such as a monthly peak); the yearly line tells the model, and code neither removes nor rewrites a part."""
    runner, path = writer
    write(runner, split_outcome(BOTH_WITH_PARTS))
    assert stored_parts(path, 'v042026') == MODEL_PARTS


def test_a_statement_linked_to_the_parent_reaches_every_written_year(writer):
    runner, path = writer
    write(runner, split_outcome(BOTH))
    runner._link('e1', 'clean-4', 1, set())
    runner.conn.commit()
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        assert sorted(r[0] for r in conn.execute("select view_id from evidence_links where evidence_id = 'e1'")) == ['v042026', 'v042027']


@pytest.mark.parametrize('years, shown', [(ONE, 'The 2027 plan names no single total.'), (TWICE, ladder_split.FAILED_TWICE)])
def test_one_year_written_lists_the_other_as_not_judged_with_the_model_s_reason_or_code_s_words(writer, years, shown):
    runner, path = writer
    write(runner, split_outcome(years))
    status = 'no ladder' if years is ONE else 'no ladder: refused'
    assert rows(path) == [('', None, 'split', None), ('2026', 'v042026', 'ladder', None), ('2027', None, status, shown)]
    assert runner.mapping['clean-4'] == ['v042026']
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        conn.row_factory = sqlite3.Row
        created = conn.execute("select created_seq from views where view_id = 'v042026'").fetchone()[0]
        parts = bundle.not_judged(conn, 'v042026', created)
    assert {'part': '2027: no question written', 'why': shown} in parts
    if years is ONE:
        assert stored_parts(path, 'v042026') == MODEL_PARTS + [{'part': '2027: no question written', 'why': shown}]


def test_no_year_written_leaves_no_view_and_both_attempts_recorded(writer):
    runner, path = writer
    write(runner, split_outcome(NONE))
    assert rows(path) == [('', None, 'split', None), ('2026', None, 'no ladder', 'none main'), ('2027', None, 'no ladder', 'none main')]
    assert 'clean-4' in runner.unjudged and 'clean-4' not in runner.mapping


KILLED_SPLIT_WRITER = '''
import json, os, signal, sys
from pathlib import Path
here, out, marker, locks, ladders = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4], sys.argv[5]
sys.path[:0] = [str(here), str(here.parents[0] / 'e2e-2026-11-09'), str(here.parents[2] / 'src')]
import ladder_adapter
from hivemind import jev, live_lock, model
from hivemind.views import store
live_lock.LOCK_FOLDER = locks
def refuse(*arguments):
    raise SystemExit('a credential was read')
model._key = jev._key = refuse
from test_ladder_adapter import fake_judge
real = store.insert
def insert(conn, table, **values):
    result = real(conn, table, **values)
    if table == 'clean_ladders' and values.get('period'):      # the first yearly row is inserted; the process dies before its commit
        marker.write_text(json.dumps({'thesis': values['thesis_id'], 'day': values['article_day'], 'period': values['period']}))
        os.kill(os.getpid(), signal.SIGKILL)
    return result
store.insert = insert
ladder_adapter.replay('u1', out, transport=fake_judge, cap_usd=5.0, inputs={'ladders': ladders})
'''


def test_a_writer_process_killed_after_the_first_yearly_row_leaves_nothing_of_that_day(tmp_path):
    """DESIGN.md v4 §0b item 3, the real-path proof: the replay loop runs in its own process with the last u1 topic's stored outcome
    replaced by the split outcome above (a stand-in: the transaction is what is tested, not the topic's wording); the process is
    killed right after the first yearly row's insert. Preflight's copy of the crashed store holds no row, view or processing record
    of that day, and its completed days all end before it."""
    lines = [json.loads(line) for line in ladder_adapter.LADDERS.read_text().splitlines()]
    target = max((row['case'] for row in lines if row['case'].startswith('u1/')), key=lambda name: int(name.split('-')[1]))
    ladders = tmp_path / 'ladders.jsonl'
    ladders.write_text(''.join(json.dumps(dict(split_outcome(BOTH), case=row['case'], **{'pass': 1}) if row['case'] == target else row,
                                          ensure_ascii=False) + '\n' for row in lines))
    (tmp_path / 'writer.py').write_text(KILLED_SPLIT_WRITER)
    out, marker = tmp_path / 'out', tmp_path / 'killed.json'
    writer = subprocess.Popen([sys.executable, str(tmp_path / 'writer.py'), str(HERE), str(out), str(marker), live_lock.LOCK_FOLDER,
                               str(ladders)])
    deadline = time.monotonic() + 120
    while writer.poll() is None and time.monotonic() < deadline:
        time.sleep(0.1)
    assert writer.returncode == -signal.SIGKILL and marker.exists(), writer.returncode
    killed = json.loads(marker.read_text())
    assert killed['thesis'] == target.split('/')[1] and killed['period'] == '2026'
    number = killed['thesis'].split('-')[1]
    [copy] = preflight.store_copies([str(out / 'views.sqlite')])
    with service.open_ledger(copy) as conn:
        assert conn.execute('select count(*) from clean_ladders where thesis_id = ?', (killed['thesis'],)).fetchone()[0] == 0
        assert conn.execute('select count(*) from views where view_id in (?, ?)', (f'v0{number}2026', f'v0{number}2027')).fetchone()[0] == 0
        assert conn.execute('select count(*) from processing_steps where publication_day = ?', (killed['day'],)).fetchone()[0] == 0
        completed = [r[0] for r in conn.execute('select day from days_completed order by id')]
        assert completed and completed[-1] < killed['day']                     # earlier days committed; this one not
        assert conn.execute('select count(*) from clean_ladders').fetchone()[0] > 0


def test_the_library_shows_the_two_years_as_two_ordinary_questions(writer):
    runner, path = writer
    from hivemind import dispatch
    dispatch.mark(runner.conn, {'input_id': 'gnews:capex', 'publication_day': split_case.DAY}, 1, 'handed_over')   # as the loop records its article
    write(runner, split_outcome(BOTH))
    store.complete_day(runner.conn, split_case.DAY, 1, split_case.DAY)
    runner.conn.commit()
    with service.open_ledger(str(path)) as conn:
        library = bundle.library(conn, None, None)
    assert sorted((v['view_id'], v['year']) for v in library['views']) == [('v042026', '2026'), ('v042027', '2027')]


ORDINARY = next(row for name, row in sorted(FIRST_SEND.items()) if name.startswith('u1/') and row['status'] == 'ladder')


def test_an_ordinary_topic_whose_number_reads_like_a_yearly_id_keeps_its_own_view_beside_the_split(writer):
    """The collision council round 160 named: clean-42026's ordinary view is v42026; clean-4's 2026 view is v042026."""
    runner, path = writer
    runner.open_thesis('clean-42026', ORDINARY, 1, 1, split_case.DAY, 'gnews:other', 'test')
    write(runner, split_outcome(BOTH))
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        assert sorted(r[0] for r in conn.execute('select view_id from views')) == ['v042026', 'v042027', 'v42026']
    assert runner.mapping['clean-42026'] == ['v42026'] and runner.mapping['clean-4'] == ['v042026', 'v042027']


@pytest.mark.parametrize('thesis_id', ['clean-04', 'clean-0', 'clean-4a', 'other-4'])
def test_a_topic_id_that_is_not_step_1_s_canonical_form_is_refused_before_anything_is_written(writer, thesis_id):
    runner, path = writer
    with pytest.raises(SystemExit, match='a topic id is clean- and a number without a leading zero'):
        runner.open_thesis(thesis_id, ORDINARY, 1, 1, split_case.DAY, 'gnews:other', 'test')
    runner.conn.commit()
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        assert conn.execute('select count(*) from clean_ladders').fetchone()[0] == 0


@pytest.mark.parametrize('periods', [['2026', '2026'], ['2026', 'FY2027'], ['26', '27'], ['2026']])
def test_a_stored_split_whose_years_are_malformed_is_refused_before_anything_is_written(writer, periods):
    runner, path = writer
    outcome = split_outcome(BOTH)
    outcome['periods'] = periods
    with pytest.raises(SystemExit, match='a split names two different years written alike'):
        runner.open_thesis('clean-4', outcome, 1, 1, split_case.DAY, 'gnews:capex', 'test')
    runner.conn.commit()
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        assert conn.execute('select count(*) from clean_ladders').fetchone()[0] == 0


@pytest.mark.parametrize('years', [BOTH, ONE])
def test_the_detail_page_and_the_idea_bundles_show_each_written_year_as_an_ordinary_question(writer, years):
    runner, path = writer
    from hivemind import dispatch
    dispatch.mark(runner.conn, {'input_id': 'gnews:capex', 'publication_day': split_case.DAY}, 1, 'handed_over')
    write(runner, split_outcome(years))
    store.complete_day(runner.conn, split_case.DAY, 1, split_case.DAY)
    runner.conn.commit()
    written = ['v042026', 'v042027'] if years is BOTH else ['v042026']
    with service.open_ledger(str(path)) as conn:
        details = {view_id: bundle.view_bundle(conn, bundle.item_lookup(None), view_id) for view_id in written}
        ideas = bundle.thesis_bundles(conn, None, written)
        if years is ONE:
            with pytest.raises(KeyError):
                bundle.view_bundle(conn, bundle.item_lookup(None), 'v042027')
    assert [details[v]['year'] for v in written] == [v[-4:] for v in written]
    assert all(f'calendar {v[-4:]}' in details[v]['question'] for v in written)
    assert [view['view_id'] for view in ideas['views']] == written
    expected = [] if years is BOTH else MODEL_PARTS + [{'part': '2027: no question written', 'why': 'The 2027 plan names no single total.'}]
    assert details['v042026']['not_judged'] == expected


def test_an_unsplit_thesis_keeps_its_single_row_with_an_empty_period(tmp_path):
    runner = ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    with sqlite3.connect(f'file:{tmp_path / "out" / "views.sqlite"}?mode=ro', uri=True) as conn:
        assert {r[0] for r in conn.execute('select period from clean_ladders')} == {''}
        assert not stored_judgements.split_rows_present(conn)
    assert runner.counts['views written from a ladder'] > 0


@pytest.fixture
def split_store(writer):
    runner, path = writer
    write(runner, split_outcome(BOTH))
    runner.close()
    return path


def test_control_theses_refuses_a_split_store_at_its_entry_point(split_store, monkeypatch, tmp_path):
    import control_theses
    monkeypatch.setattr(stored_judgements, 'stage_b_folders', lambda: {d: split_store.parent for d in ('u1', 'u2', 'u3')})
    with pytest.raises(SystemExit, match='control_theses: this store holds period-split rows'):
        control_theses.packets(tmp_path / 'readers', tmp_path / 'facts' / 'facts.json')
    assert not (tmp_path / 'readers' / 'controls').exists()


def test_stage_b_count_refuses_a_split_store_before_reading_its_arguments(split_store, monkeypatch):
    import stage_b_count
    monkeypatch.setattr(stored_judgements, 'stage_b_folders', lambda: {d: split_store.parent for d in ('u1', 'u2', 'u3')})
    monkeypatch.setattr(sys, 'argv', ['stage_b_count.py'])
    with pytest.raises(SystemExit, match='stage_b_count: this store holds period-split rows'):
        stage_b_count.main()


def test_control_census_refuses_a_split_store_at_its_entry_point(split_store, monkeypatch, tmp_path):
    census = load('control_census', ROOT / 'docs/research/2026-11-14-use-acceptance/stage-b-controls/control_census.py')
    for draw in ('u1', 'u2', 'u3'):
        (tmp_path / f'draw-{draw}').mkdir()
        os.symlink(split_store, tmp_path / f'draw-{draw}' / 'views.sqlite')
    monkeypatch.setattr(census, 'RUN', tmp_path)
    with pytest.raises(SystemExit, match='control_census: this store holds period-split rows'):
        census.main()


def test_page_store_refuses_a_split_store_before_it_replays(split_store, monkeypatch, tmp_path):
    page = load('page_store', ROOT / 'docs/research/2026-11-14-use-acceptance/not-judged-display/page_store.py')
    (tmp_path / 'draw' / 'judge' / 'draw-c1').mkdir(parents=True)
    os.symlink(split_store, tmp_path / 'draw' / 'judge' / 'draw-c1' / 'views.sqlite')
    monkeypatch.setattr(page, 'DRAW', tmp_path / 'draw')
    with pytest.raises(SystemExit, match='page_store: this store holds period-split rows'):
        page.main(tmp_path / 'new')
    assert not (tmp_path / 'new').exists()


USE = ROOT / 'docs/research/2026-11-14-use-acceptance'


def test_build_sources_refuses_a_split_store_at_its_entry_point(split_store, tmp_path):
    sources = load('build_sources', USE / 'carried-run/build_sources.py')
    (tmp_path / 'run/c1/judge/draw-c1').mkdir(parents=True)
    os.symlink(split_store, tmp_path / 'run/c1/judge/draw-c1/views.sqlite')
    with pytest.raises(SystemExit, match='build_sources: this store holds period-split rows'):
        sources.main(tmp_path / 'run', tmp_path / 'keys')


def test_build_side_by_side_refuses_a_split_store_where_it_opens_each_system_s_store(split_store, monkeypatch):
    side = load('build_side_by_side', USE / 'side-by-side/build_side_by_side.py')
    monkeypatch.setitem(side.FOLDERS, 'new', split_store.parent)
    with pytest.raises(SystemExit, match='build_side_by_side: this store holds period-split rows'):
        side.load_entries('new', {}, [], {}, {}, {})


def test_build_deck_refuses_a_split_store_at_its_entry_point(split_store, monkeypatch, tmp_path):
    deck = load('build_deck', USE / 'pilot-deck-1/build_deck.py')
    monkeypatch.setitem(deck.FOLDERS, 'new', split_store.parent)
    (tmp_path / 'week-keys').mkdir()
    for name in ('week-key-A2.json', 'week-key-B.json'):
        (tmp_path / 'week-keys' / name).write_text('[]')
    with pytest.raises(SystemExit, match='build_deck: this store holds period-split rows'):
        deck.main(tmp_path / 'week-keys', tmp_path / 'deck-keys')
    assert list((tmp_path / 'deck-keys').iterdir()) == []


def historical_stores():
    """Every store the seven readers that refuse a split store read in their recorded runs."""
    census = load('control_census', USE / 'stage-b-controls/control_census.py')
    page = load('page_store', USE / 'not-judged-display/page_store.py')
    side = load('build_side_by_side', USE / 'side-by-side/build_side_by_side.py')
    deck = load('build_deck', USE / 'pilot-deck-1/build_deck.py')
    paths = [folder / 'views.sqlite' for folder in stored_judgements.stage_b_folders().values()]
    paths += [census.RUN / f'draw-{draw}' / 'views.sqlite' for draw in ('u1', 'u2', 'u3')]
    paths += [page.DRAW / 'judge/draw-c1/views.sqlite', ROOT / 'poc/data/clean-carried-run-2026-11-16/c1/judge/draw-c1/views.sqlite']
    paths += [folder / 'views.sqlite' for folder in (*side.FOLDERS.values(), *deck.FOLDERS.values())]
    return sorted(set(paths))


def test_the_shared_refusal_passes_every_historical_store_the_readers_read():
    stores = historical_stores()
    assert len(stores) >= 6 and all(path.exists() for path in stores), [p for p in stores if not p.exists()]
    for path in stores:
        with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
            assert not stored_judgements.split_rows_present(conn), path
            stored_judgements.refuse_split_store(conn, 'any reader')                               # no refusal
