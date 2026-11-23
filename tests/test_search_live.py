"""Search on a store being written (docs/research/2026-11-14-use-acceptance/live-service/OPERATING-CONTRACT.md, row 4a; proofs 8a to 8c):
the lexical ranking counts only views visible at the request's bound; the index embeds only views visible at the last completed day;
a vector is used only for a visible view whose text and model match; a newly visible view is served from a matching cached vector or
lexically; a service started on a first-day store builds no index; a build committing during a search changes nothing in it. Real
stores in WAL mode on temporary paths; embeddings from a deterministic fake; no network."""
import importlib.util
import json
import os
import sqlite3
import sys
import threading

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(ROOT, 'src'), os.path.join(ROOT, 'scripts')]
from hivemind import dispatch, search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

RUNGS = [{'label': 'Yes', 'condition': 'It ships by 2027-01-31.'}, {'label': 'Ruled out', 'condition': 'It is cancelled.'},
         {'label': 'Still open', 'condition': 'Neither holds on 2027-01-31.'}]
QUERY = 'accelerator shipments'


def add_view(writer, day, seq, view_id, question, *, complete=True):
    dispatch.mark(writer, {'input_id': f'gnews:{view_id}', 'publication_day': day}, seq, 'handed_over')
    store.create_view(writer, view_id=view_id, object_id='NVDA', object_kind='asset', kind='asset', looks_at=question, question=question,
                      due_day='2027-01-31', year='2027', rungs=RUNGS, seq=seq, input_id=f'gnews:{view_id}', created_at=f'{day}T00:00:00Z')
    if complete:
        store.complete_day(writer, day, seq, day)
    writer.commit()


def a_store(path, *, first_day=False):
    writer = store.open_db(str(path))
    writer.execute('pragma journal_mode=wal')
    if first_day:
        dispatch.mark(writer, {'input_id': 'gnews:first', 'publication_day': '2026-10-01'}, 1, 'handed_over')
        writer.commit()
        return writer
    for n, question in enumerate(('Will accelerator shipments reach 5 million units?', 'Will data center revenue grow 50%?',
                                  'Will memory prices rise in 2027?'), start=1):
        add_view(writer, '2026-10-01', n, f'v{n}', question)
    return writer


def backup(writer, path):
    """A copy by SQLite's backup API, taken out of WAL mode: a backup of a WAL store keeps WAL mode, and a read-only reader of it then
    fails ("unable to open database file") because it cannot create the shared-memory file (a finding of this slice, for row 7)."""
    target = sqlite3.connect(str(path))
    writer.backup(target)
    target.execute('pragma journal_mode=delete')
    target.close()
    return service.open_ledger(str(path))


def unfinished_views(writer, count):
    """`count` views of 2026-10-02 written and committed, the day not completed: what an unfinished day leaves."""
    for n in range(count):
        add_view(writer, '2026-10-02', 100 + n, f'u{n}', f'Will accelerator shipments of model {n} accelerate accelerator shipments?', complete=False)


def text_of(ledger, view_id):
    record = ledger.execute('select * from views where view_id=?', (view_id,)).fetchone()
    return search.view_text(record, store.rungs_of(ledger, view_id))


def put_vector(index, ledger, view_id, vector, model=search.EMBEDDING_MODEL):
    index.execute('insert or replace into view_vectors (view_id, text_sha256, model, vector_json, tokens, built_at) values (?,?,?,?,?,?)',
                  (view_id, search.sha(text_of(ledger, view_id)), model, json.dumps(vector), 1, '2026-10-01T00:00:00'))
    index.commit()


def put_query(index, text, vector, model=search.EMBEDDING_MODEL):
    index.execute('insert or replace into query_vectors (text_sha256, model, vector_json, tokens, built_at) values (?,?,?,?,?)',
                  (search.sha(text), model, json.dumps(vector), 1, '2026-10-01T00:00:00'))
    index.commit()


def fake(texts, model=search.EMBEDDING_MODEL):
    """`search.fake_embed` already answers (vectors, tokens), as the embedding call does."""
    return search.fake_embed(texts, model, dims=8)


def test_lexical_search_at_the_last_completed_day_equals_the_same_search_on_its_backup(tmp_path):
    writer = a_store(tmp_path / 'views.sqlite')
    kept = backup(writer, tmp_path / 'backup.sqlite')
    unfinished_views(writer, 60)                                   # more than the 50 the ranking keeps, every one matching the query
    live = service.open_ledger(str(tmp_path / 'views.sqlite'))
    got = search.search(live, None, QUERY, 10, semantic=False)
    assert got == search.search(kept, None, QUERY, 10, semantic=False)
    assert [r['view_id'] for r in got['results']][:1] == ['v1'] and got['mode'] == 'lexical'


def test_the_index_embeds_only_views_visible_at_the_last_completed_day(tmp_path):
    writer = a_store(tmp_path / 'views.sqlite')
    unfinished_views(writer, 5)
    sent = []
    recording = lambda texts, model: (sent.extend(texts) or fake(texts, model))
    ledger, index = service.open_ledger(str(tmp_path / 'views.sqlite')), search.open_index(str(tmp_path / 'index.sqlite'))
    assert search.build_index(ledger, index, embed=recording)[0] == 3
    assert sorted(sent) == sorted(text_of(ledger, v) for v in ('v1', 'v2', 'v3'))


def test_a_build_on_a_first_day_store_is_refused_and_sends_nothing(tmp_path):
    a_store(tmp_path / 'views.sqlite', first_day=True)
    ledger, index = service.open_ledger(str(tmp_path / 'views.sqlite')), search.open_index(str(tmp_path / 'index.sqlite'))
    with pytest.raises(service.FirstDayNotCompleted):
        search.build_index(ledger, index, embed=lambda texts, model: pytest.fail('nothing may be sent'))


def test_an_invisible_view_with_another_vector_length_changes_no_visible_vector(tmp_path):
    """Round 129's control, made decisive: the invisible view has the lower sequence (its step is dated after the last completed day,
    as a restored or reordered store can hold), so a check over every view in sequence order meets it first and would take its
    vector's length, rejecting the visible view's."""
    path = tmp_path / 'views.sqlite'
    writer = store.open_db(str(path))
    writer.execute('pragma journal_mode=wal')
    dispatch.mark(writer, {'input_id': 'gnews:u0', 'publication_day': '2026-10-02'}, 1, 'handed_over')
    store.create_view(writer, view_id='u0', object_id='NVDA', object_kind='asset', kind='asset', looks_at='later', question='Later?',
                      due_day='2027-01-31', year='2027', rungs=RUNGS, seq=1, input_id='gnews:u0', created_at='2026-10-02T00:00:00Z')
    dispatch.mark(writer, {'input_id': 'gnews:v1', 'publication_day': '2026-10-01'}, 2, 'handed_over')
    store.create_view(writer, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at=QUERY, question=QUERY,
                      due_day='2027-01-31', year='2027', rungs=RUNGS, seq=2, input_id='gnews:v1', created_at='2026-10-01T00:00:00Z')
    store.complete_day(writer, '2026-10-01', 2, '2026-10-01')
    writer.commit()
    ledger, index = service.open_ledger(str(path)), search.open_index(str(tmp_path / 'index.sqlite'))
    assert service.resolve_bound(ledger, None) == '2026-10-01' and not service.view_exists(ledger, {'created_seq': 1}, '2026-10-01')
    put_vector(index, ledger, 'u0', [1.0, 0.0, 0.0])
    put_vector(index, ledger, 'v1', [0.0, 1.0])
    assert search.fresh_vectors(ledger, index, view_ids=['v1']) == {'v1': [0.0, 1.0]}
    put_query(index, QUERY, [0.0, 1.0])
    got = search.search(ledger, index, QUERY, 10, embed=fake)
    assert (got['mode'], got['missing_vectors'], [r['view_id'] for r in got['results']]) == ('semantic', [], ['v1'])


def load_mcp(tmp_path, monkeypatch, *, lexical=False):
    argv = ['hivemind_mcp.py', '--views', str(tmp_path / 'views.sqlite'), '--index', str(tmp_path / 'index.sqlite'), '--items', str(tmp_path / 'none.sqlite')]
    monkeypatch.setattr(sys, 'argv', argv + (['--lexical'] if lexical else []))
    spec = importlib.util.spec_from_file_location(f'hivemind_mcp_search_{tmp_path.name}', os.path.join(ROOT, 'scripts', 'hivemind_mcp.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('cached', [True, False])
def test_mcp_serves_a_newly_visible_view_from_a_matching_cached_vector_or_lexically(tmp_path, monkeypatch, cached):
    writer = a_store(tmp_path / 'views.sqlite')
    ledger, index = service.open_ledger(str(tmp_path / 'views.sqlite')), search.open_index(str(tmp_path / 'index.sqlite'))
    for view_id in ('v1', 'v2', 'v3'):
        put_vector(index, ledger, view_id, fake([text_of(ledger, view_id)])[0][0])
    put_query(index, QUERY, fake([QUERY])[0][0])
    mcp = load_mcp(tmp_path, monkeypatch)                          # start-up finds every visible view embedded: nothing is sent
    add_view(writer, '2026-10-02', 4, 'v4', 'Will accelerator shipments double in 2027?')
    if cached:
        put_vector(index, service.open_ledger(str(tmp_path / 'views.sqlite')), 'v4', fake([text_of(service.open_ledger(str(tmp_path / 'views.sqlite')), 'v4')])[0][0])
    got = mcp.search(QUERY, 10)
    assert (got['mode'], got['missing_vectors']) == (('semantic', []) if cached else ('lexical', ['v4']))
    assert 'v4' in [r['view_id'] for r in got['results']]


@pytest.mark.parametrize('cached', [True, False])
def test_a_service_started_on_a_first_day_store_builds_nothing_and_is_semantic_only_when_every_view_is_cached(tmp_path, monkeypatch, cached):
    writer = a_store(tmp_path / 'views.sqlite', first_day=True)
    import hivemind_api
    monkeypatch.setitem(hivemind_api.PATHS, 'views', str(tmp_path / 'views.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'index', str(tmp_path / 'index.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'items', str(tmp_path / 'none.sqlite'))
    monkeypatch.setitem(hivemind_api.PATHS, 'archive', str(tmp_path / 'archive.sqlite'))
    assert hivemind_api.index_at_start(embed=lambda texts, model: pytest.fail('nothing may be sent')).startswith('index: not built')
    mcp = load_mcp(tmp_path, monkeypatch)
    assert mcp.OBJECTS.startswith('No day of this ledger has completed yet')
    add_view(writer, '2026-10-01', 2, 'v1', 'Will accelerator shipments reach 5 million units?')
    index = search.open_index(str(tmp_path / 'index.sqlite'))
    ledger = service.open_ledger(str(tmp_path / 'views.sqlite'))
    put_query(index, QUERY, fake([QUERY])[0][0])                   # a successful (fake) query embedding, as round 130 asks
    if cached:
        put_vector(index, ledger, 'v1', fake([text_of(ledger, 'v1')])[0][0])
    expected = ('semantic', []) if cached else ('lexical', ['v1'])
    got = mcp.search(QUERY, 10)
    assert (got['mode'], got['missing_vectors']) == expected
    with hivemind_api.Connections() as db:
        api_got = hivemind_api.route(db, ['search'], {'q': QUERY})
    assert (api_got['mode'], api_got['missing_vectors']) == expected


def test_two_concurrent_searches_for_one_new_query_each_answer_and_the_cache_keeps_one_vector(tmp_path, monkeypatch):
    a_store(tmp_path / 'views.sqlite')
    mcp = load_mcp(tmp_path, monkeypatch, lexical=True)
    answers, errors, start = [], [], threading.Barrier(2)

    def call():
        try:
            with mcp.connections() as (_, _, index):
                start.wait(timeout=5)
                answers.append(search.query_vector(index, 'a query never asked', fake)[0])
        except Exception as error:                                   # noqa: BLE001 - any error is the finding
            errors.append(repr(error))
    threads = [threading.Thread(target=call) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert errors == [] and len(answers) == 2 and all(search.usable(a) for a in answers)
    count = sqlite3.connect(str(tmp_path / 'index.sqlite')).execute('select count(*) from query_vectors where text_sha256=?', (search.sha('a query never asked'),)).fetchone()[0]
    assert count == 1


def test_a_build_committing_during_a_search_changes_nothing_in_that_search(tmp_path, monkeypatch):
    writer = a_store(tmp_path / 'views.sqlite')
    ledger, index = service.open_ledger(str(tmp_path / 'views.sqlite')), search.open_index(str(tmp_path / 'index.sqlite'))
    put_vector(index, ledger, 'v1', fake([text_of(ledger, 'v1')])[0][0])
    put_query(index, QUERY, fake([QUERY])[0][0])
    before = search.search(ledger, index, QUERY, 10, embed=fake)
    real = search.fresh_vectors

    def then_a_build_commits(*args, **kwargs):
        vectors = real(*args, **kwargs)
        other = search.open_index(str(tmp_path / 'index.sqlite'))
        for view_id in ('v2', 'v3'):
            put_vector(other, ledger, view_id, fake([text_of(ledger, view_id)])[0][0])
        return vectors
    monkeypatch.setattr(search, 'fresh_vectors', then_a_build_commits)
    during = search.search(ledger, index, QUERY, 10, embed=fake)
    assert during == before and during['missing_vectors'] == ['v2', 'v3']
