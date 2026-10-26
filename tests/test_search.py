"""The search engine over the sealed ledger with a deterministic fake embedding (no network), and the HTTP front
as a user starts it. Requirements: docs/poc/service.md: the index is derived and keyed by the view's own text
(never evidence); the ranking is semantic only when every candidate has a fresh vector, lexical otherwise and says
so; the query cache is by text and model; as_of filters what can be found; the front answers over HTTP.

Run: python3 -m pytest tests/test_search.py -q
"""
import json
import os
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import search, service  # noqa: E402
from hivemind.views import store  # noqa: E402

LEDGER = os.path.join(ROOT, 'poc', 'data', 'sealed-2026-10-24-run3-through-0815', 'views.sqlite')
UNIVERSE = os.path.join(ROOT, 'poc', 'universe.json')


@pytest.fixture(scope='module')
def ledger():
    return service.open_ledger(LEDGER)


@pytest.fixture
def index(tmp_path):
    return search.open_index(str(tmp_path / 'index.sqlite'))


def test_index_is_derived_keyed_by_the_views_own_text(ledger, index, tmp_path):
    embedded, unchanged, _, error = search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    assert error is None and embedded == ledger.execute('select count(*) from views').fetchone()[0] and unchanged == 0
    again = search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    assert again[0] == 0 and again[1] == embedded
    # the indexed text is the view's own: none of its evidence sentences is in it
    record = store.view(ledger, 'v3')
    text = search.view_text(record, store.rungs_of(ledger, 'v3'))
    assert record['question'] in text and all(e['one_line'] not in text for e in service.evidence(ledger, 'v3'))
    # a changed question (on a scratch copy of the ledger, its append-only trigger dropped) re-embeds only that view
    scratch = str(tmp_path / 'ledger.sqlite')
    shutil.copy(LEDGER, scratch)
    os.chmod(scratch, 0o644)                      # the sealed file is read-only; the scratch copy is ours to edit
    conn = sqlite3.connect(scratch)
    conn.row_factory = sqlite3.Row
    conn.execute('drop trigger views_no_update')
    conn.execute("update views set question=question||'（改）' where view_id='v3'")
    conn.commit()
    assert search.build_index(conn, index, embed=search.fake_embed, embedding_model='fake')[0] == 1


def test_search_ranks_views_with_the_object_boost_and_as_of_filter(ledger, index):
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    aliases = search.object_aliases(UNIVERSE)
    result = search.search(ledger, index, 'NVIDIA FY2027 全年数据中心收入 数据中心', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases)
    assert result['mode'] == 'semantic' and result['missing_vectors'] == [] and len(result['results']) == 10
    assert result['results'][0]['view_id'] == 'v3' and result['results'][0]['parts']['object_hit'] is True
    assert all(r['open'] for r in result['results'])
    early = search.search(ledger, index, 'CPU 收入', 10, as_of='2026-07-23', embed=search.fake_embed, embedding_model='fake', aliases=aliases)
    assert early['results'] is None      # D91: no recorded CPU thesis before it opened on 2026-07-24
    calls = []
    def counting(texts, m): calls.append(texts); return search.fake_embed(texts, m)
    search.search(ledger, index, 'CPU 收入', 10, embed=counting, embedding_model='fake', aliases=aliases)
    assert calls == []          # the query vector came from the cache


def test_search_says_lexical_when_a_vector_is_missing_stale_or_empty(ledger, index):
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    aliases = search.object_aliases(UNIVERSE)
    index.execute("update view_vectors set text_sha256='stale' where view_id='v3'")
    index.commit()
    result = search.search(ledger, index, 'FY2027 数据中心全年收入', 5, embed=search.fake_embed, embedding_model='fake', aliases=aliases)
    assert result['mode'] == 'lexical' and result['missing_vectors'] == ['v3']
    assert all(r['parts']['semantic'] == 0.0 for r in result['results'])
    # an empty vector with the right hash is not a usable vector
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    index.execute("update view_vectors set vector_json='[]' where view_id='v3'")
    index.commit()
    result = search.search(ledger, index, 'FY2027 数据中心全年收入', 5, embed=search.fake_embed, embedding_model='fake', aliases=aliases)
    assert result['mode'] == 'lexical' and result['missing_vectors'] == ['v3']
    assert search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')[0] == 1    # and it is rebuilt
    empty = search.open_index(':memory:')
    assert search.search(ledger, empty, 'anything', 3, embed=search.fake_embed, embedding_model='fake')['mode'] == 'lexical'


def test_search_is_null_only_for_an_idea_off_the_librarys_subject(ledger, index, monkeypatch):
    # D91 as amended 2026-10-24: null when the idea names no object, matches no view text, and sits below the
    # similarity floor that only off-subject ideas reach; everything else goes to the caller to judge (D76).
    # The fake embedder's similarities are not on the real scale, so the floor is moved to show each leg decides.
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    aliases = search.object_aliases(UNIVERSE)
    monkeypatch.setattr(search, 'NULL_FLOOR', 1.01)          # every similarity is below: no name, no text match → null
    answer = search.search(ledger, index, 'Should I buy a house in Austin', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases)
    assert answer['results'] is None and answer['as_of'] == '2026-08-15'
    monkeypatch.setattr(search, 'NULL_FLOOR', 0.0)           # nothing is below: the same idea comes back for the caller to judge
    assert search.search(ledger, index, 'Should I buy a house in Austin', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases)['results']
    monkeypatch.setattr(search, 'NULL_FLOOR', 1.01)
    # a Chinese idea written without spaces is found by the text index's three-character windows (it was null before)
    assert search.lexical_terms('数据中心需求见顶了吗？')[:3] == ['数据中', '据中心', '中心需']
    assert search.search(ledger, index, '数据中心需求见顶了吗？', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases)['results']
    # a product name stands for its company: Blackwell → NVDA, and the data-center view is among the candidates
    assert search.objects_in('Blackwell demand is softening', aliases) == {'NVDA'}
    blackwell = search.search(ledger, index, 'Blackwell demand is softening', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases)['results']
    assert blackwell and all(r['parts']['object_hit'] == (r['object'] == 'NVDA') for r in blackwell)    # exactly the named company's views get the boost
    # single words of a name are not aliases: 'rate' is not the Fed theme, 'meta' is not in 'metadata'
    assert search.objects_in("NVIDIA's tax rate will rise in FY2027", aliases) == {'NVDA'}
    assert search.objects_in('metadata platforms and the rate of change', aliases) == set()
    assert search.objects_in('Micron benefits most from HBM demand', aliases) == {'MU'}
    # lexical mode has no similarity to fall back on: no name and no text match is null
    assert search.search(ledger, index, 'Tesla will go bankrupt next year', 10, embed=search.fake_embed, embedding_model='fake', aliases=aliases, semantic=False)['results'] is None
    # a day before the first view was opened: nothing recorded, whatever the idea
    assert search.search(ledger, index, 'NVIDIA data center revenue', 10, as_of='2026-01-01', embed=search.fake_embed, embedding_model='fake', aliases=aliases)['results'] is None


def test_lexical_mode_never_calls_the_embedder_even_with_a_full_index(ledger, index):
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    calls = []
    def counting(texts, m): calls.append(texts); return search.fake_embed(texts, m)
    result = search.search(ledger, index, 'a query never seen before 1234', 3, embed=counting, embedding_model='fake', semantic=False)
    assert result['mode'] == 'lexical' and calls == []


def test_a_failed_batch_reports_the_work_already_done(ledger, index):
    calls = []
    def flaky(texts, m):
        calls.append(len(texts))
        if len(calls) == 2:
            raise search.model.TransportError('embeddings HTTP 500')
        return search.fake_embed(texts, m)
    embedded, unchanged, tokens, error = search.build_index(ledger, index, embed=flaky, embedding_model='fake', batch=40)
    assert embedded == 40 and error == 'embeddings HTTP 500' and tokens > 0
    assert index.execute('select count(*) from view_vectors').fetchone()[0] == 40


def test_search_falls_back_to_lexical_when_no_embedding(ledger, index):
    search.build_index(ledger, index, embed=search.fake_embed, embedding_model='fake')
    def failing(texts, m): raise search.model.TransportError('offline')
    result = search.search(ledger, index, 'Vera Rubin 量产 出货', 5, embed=failing, embedding_model='fake', aliases=search.object_aliases(UNIVERSE))
    assert result['mode'] == 'lexical' and result['results'] and result['results'][0]['parts']['text_hit'] is True
    assert result['results'][0]['view_id'] in ('v7', 'v48', 'v15', 'v60')


def test_the_embedding_error_never_carries_the_response_body(monkeypatch):
    class FakeHTTPError(urllib.error.HTTPError):
        def __init__(self):
            super().__init__('https://example', 401, 'Unauthorized', {}, None)
        def read(self):
            return b'{"error": {"message": "Incorrect API key provided: sk-review-dummy-key-000000000000", "type": "invalid_request_error"}}'
    def fake_urlopen(*args, **kwargs):
        raise FakeHTTPError()
    monkeypatch.setattr(search.urllib.request, 'urlopen', fake_urlopen)
    monkeypatch.setattr(search.model, '_key', lambda provider: 'not-a-real-key')
    with pytest.raises(search.model.TransportError) as caught:
        search.openai_embeddings(['x'])
    assert 'dummy' not in str(caught.value) and 'sk-' not in str(caught.value) and 'invalid_request_error' in str(caught.value)


def test_search_eval_reads_the_mappers_none_as_no_lead_and_fails_on_a_miss(monkeypatch, capsys, tmp_path):
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import search_eval
    assert search_eval.lead_of({'mapped_view_id': 'none'}) is None and search_eval.lead_of({'mapped_view_id': ''}) is None
    assert search_eval.lead_of({'mapped_view_id': 'v3'}) == 'v3'
    monkeypatch.setattr(search_eval.search, 'build_index', lambda *a, **k: (0, 94, 0, None))
    monkeypatch.setattr(search_eval.search, 'search', lambda *a, **k: {'mode': 'lexical', 'as_of': '2026-08-15', 'results': [{'view_id': 'v99', 'score': 0.1, 'parts': {'semantic': 0, 'object_hit': False, 'text_hit': False}, 'looks_at': 'x'}]})
    monkeypatch.setattr(sys, 'argv', ['search_eval.py', '--index', str(tmp_path / 'index.sqlite')])
    with pytest.raises(SystemExit) as stop:
        search_eval.main()
    assert stop.value.code == 1 and 'FAILED' in capsys.readouterr().out


def free_port():
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def test_http_front_answers_as_a_user_starts_it(tmp_path):
    port = free_port()
    proc = subprocess.Popen([sys.executable, os.path.join(ROOT, 'scripts', 'hivemind_api.py'), '--views', LEDGER, '--items', os.path.join(ROOT, 'poc', 'data', 'items-window.sqlite'), '--port', str(port), '--index', str(tmp_path / 'index.sqlite'), '--archive', str(tmp_path / 'idea-archive.sqlite'), '--lexical'],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        def get(path):
            for _ in range(40):
                try:
                    with urllib.request.urlopen(f'http://127.0.0.1:{port}{path}', timeout=5) as r:
                        return r.status, json.loads(r.read())
                except urllib.error.HTTPError as e:
                    return e.code, json.loads(e.read())
                except (urllib.error.URLError, ConnectionError):
                    time.sleep(0.25)
            raise AssertionError('the server did not answer')
        assert get('/days') == (200, {'first_day': '2026-02-25', 'last_day': '2026-08-15'})
        status, view = get('/views/v3?as_of=2026-05-19')
        assert status == 200 and view['state']['position'] == 3
        status, result = get('/search?q=Rubin&k=3')
        assert status == 200 and result['mode'] == 'lexical' and result['results']
        assert get('/search?q=Should%20I%20buy%20a%20house%20in%20Austin')[1]['results'] is None
        status, verdict = get('/evaluate?view_id=v3&comparator=%3E%3D&value_usd=300000000000')
        assert status == 200 and verdict['verdict'] == 'holds'
        assert get('/views/v999')[0] == 404 and get('/evaluate?view_id=v999&comparator=%3E%3D&value_usd=1')[0] == 404
        assert get('/evaluate?view_id=v3&comparator=%3E&value_usd=1')[0] == 400 and get('/changes')[0] == 400
        assert get('/changes?since=2026-08-14')[1][0]['view_id'] == 'v1'
    finally:
        proc.terminate()
        proc.wait(timeout=10)
