"""The new replay starts from real material, without the retired seeded questions."""
import json
import runpy
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest
from hivemind import model, seeding
from hivemind.views import store
from test_placement import ITEM, TEXT

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/replay.py'
SEED = ROOT / 'poc/seeds/nvda-2026-07-01-v2.json'


@pytest.mark.parametrize('category', ['T7', 'T1'])
def test_default_entry_reads_a_source_without_report_import(tmp_path, monkeypatch, category):
    db = tmp_path / 'items.sqlite'
    source_text = TEXT if category == 'T7' else 'NVIDIA reported quarterly revenue of $30 billion for fiscal 2026 Q2.'
    item = dict(ITEM, category=category, published_at='2026-08-10T12:00:00Z', source_uri='https://example.com/article',
                feed=1, copy_of=None, klass='新闻' if category == 'T7' else '公司材料', text=source_text)
    with sqlite3.connect(db) as conn:
        conn.execute('create table items (input_id text, category text, publication_day text, publisher text, publisher_type text, title text, object_identifiers text, text text, published_at text, source_uri text, feed integer, copy_of text, klass text)')
        keys = list(item)
        conn.execute(f'insert into items ({",".join(keys)}) values ({",".join("?" for _ in keys)})',
                     [json.dumps(item[k]) if k == 'object_identifiers' else item[k] for k in keys])
    calls = []
    def transport(provider, request, timeout=600):
        calls.append(request)
        return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}],
                'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
    monkeypatch.setattr(model, 'openai_transport', transport)
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-08-10', '--until', '2026-08-10', '--testdb', str(db),
                                      '--views', str(tmp_path / 'run/views.sqlite'), '--archive', str(tmp_path / 'run/archive.sqlite')])
    runpy.run_path(str(SCRIPT), run_name='__main__')
    assert len(calls) == 1 and '[Open questions at the start of 2026-08-10]\n  None yet.' in calls[0]['messages'][1]['content']
    assert source_text in calls[0]['messages'][1]['content'] and '[Earlier earnings report: background]' not in calls[0]['messages'][1]['content']
    with sqlite3.connect(tmp_path / 'run/views.sqlite') as conn:
        assert conn.execute('select count(*) from views').fetchone()[0] == 0
        assert conn.execute("select count(*) from processing_steps where step='baseline'").fetchone()[0] == 0
        assert conn.execute("select count(*) from processing_steps where step='extracted' and result='ok'").fetchone()[0] == 1


def test_entry_refuses_seeded_ledger_and_legacy_baseline(tmp_path):
    path = tmp_path / 'run/views.sqlite'
    conn = store.open_db(str(path))
    seeding.seed_views(conn, str(SEED), created_at='2026-07-01T00:00:00Z')
    conn.close()
    args = [sys.executable, str(SCRIPT), '--from', '2026-07-01', '--until', '2026-07-01', '--views', str(path), '--archive', str(tmp_path / 'run/a.sqlite')]
    seeded = subprocess.run(args, capture_output=True, text=True)
    assert seeded.returncode != 0 and '22 seeded' in seeded.stderr
    legacy = subprocess.run(args + ['--config', str(ROOT / 'poc/config/poc-v116.json')], capture_output=True, text=True)
    assert legacy.returncode != 0 and 'retired seeded-question baseline' in legacy.stderr
    with sqlite3.connect(path) as conn:
        assert conn.execute('select count(*) from views').fetchone()[0] == 22


def test_default_entry_writes_article_evidence_for_the_reader(tmp_path, monkeypatch):
    """An article-created question and its evidence reach the normal reader with an empty starting ledger."""
    from hivemind import jev, service
    from test_sequential_replay import setup_run, v108_send
    args = setup_run(tmp_path)
    send = v108_send()
    monkeypatch.setattr(model, 'openai_transport', lambda provider, request, timeout=600: send(provider, request))
    monkeypatch.setattr(jev, 'transport', lambda request, timeout=60: send(request))
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-02-25', '--until', '2026-02-25', '--testdb', args['testdb_path'],
                                      '--views', str(tmp_path / 'views.sqlite'), '--archive', str(tmp_path / 'new-archive.sqlite'), '--workers', '1'])
    runpy.run_path(str(SCRIPT), run_name='__main__')
    conn = service.open_ledger(str(tmp_path / 'views.sqlite'))
    view_ids = [r[0] for r in conn.execute('select view_id from views')]
    assert len(view_ids) == 2 and service.evidence(conn, view_ids[0], as_of='2026-02-25')


def test_entry_accepts_existing_question_without_requiring_its_old_source_in_the_new_feed(tmp_path):
    """A new feed may omit the historical article that originally created a question."""
    path = tmp_path / 'run/views.sqlite'
    conn = store.open_db(str(path))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='Rubin rollout',
                      question='Will Rubin ship?', due_day='2026-12-31', year='2026', rungs=[], seq=1,
                      input_id='unverified', created_at='2026-07-01T00:00:00Z')
    conn.commit(); conn.close()
    replay_module = runpy.run_path(str(SCRIPT))
    replay_module['refuse_seeded_ledger'](str(path))


def test_default_entry_reads_existing_question_with_only_new_article_in_feed(tmp_path, monkeypatch):
    """D370: an existing library is input even when the feed omits its historical sources."""
    path = tmp_path / 'run/views.sqlite'
    conn = store.open_db(str(path))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='Rubin rollout',
                      question='Will Rubin ship by year end?', due_day='2026-12-31', year='2026', rungs=[], seq=1,
                      input_id='earlier-article', created_at='2026-08-09T12:00:00Z')
    store.complete_day(conn, '2026-08-09', 1, '2026-08-09T23:59:00Z')
    conn.commit(); conn.close()
    db = tmp_path / 'items.sqlite'
    item = dict(ITEM, published_at='2026-08-10T12:00:00Z', source_uri='https://example.com/news', feed=1,
                copy_of=None, klass='新闻', text=TEXT)
    with sqlite3.connect(db) as items:
        items.execute('create table items (input_id text, category text, publication_day text, publisher text, publisher_type text, title text, object_identifiers text, text text, published_at text, source_uri text, feed integer, copy_of text, klass text)')
        keys = list(item)
        items.execute(f'insert into items ({",".join(keys)}) values ({",".join("?" for _ in keys)})',
                      [json.dumps(item[k]) if k == 'object_identifiers' else item[k] for k in keys])
    calls = []
    def transport(provider, request, timeout=600):
        calls.append(request)
        return {'choices': [{'message': {'content': json.dumps({'evidence': [], 'candidates': [], 'new_groups': []})}}],
                'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
    monkeypatch.setattr(model, 'openai_transport', transport)
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-08-10', '--until', '2026-08-10', '--testdb', str(db),
                                      '--views', str(path), '--archive', str(tmp_path / 'run/archive.sqlite')])
    runpy.run_path(str(SCRIPT), run_name='__main__')
    assert len(calls) == 1 and 'Will Rubin ship by year end?' in calls[0]['messages'][1]['content']


def test_default_entry_records_unlinked_fact_as_no_home(tmp_path, monkeypatch):
    """An unlinked source quotation is not written when no question takes it."""
    from hivemind import jev
    from test_sequential_replay import setup_run, v108_send
    args = setup_run(tmp_path)
    with sqlite3.connect(args['testdb_path']) as conn:
        conn.execute('delete from items where rowid > 1')
    send = v108_send()
    def openai(provider, request, timeout=600):
        response = send(provider, request)
        if request['response_format']['json_schema']['name'] == 'extraction':
            answer = json.loads(response['choices'][0]['message']['content'])
            source_fact = dict(answer['evidence'][0], id='e9', links=[],
                               quote='We shipped our first Vera Rubin samples to customers earlier this week')
            answer['evidence'].append(source_fact)
            response['choices'][0]['message']['content'] = json.dumps(answer)
        return response
    monkeypatch.setattr(model, 'openai_transport', openai)
    monkeypatch.setattr(jev, 'transport', lambda request, timeout=60: send(request))
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-02-25', '--until', '2026-02-25', '--testdb', args['testdb_path'],
                                      '--views', str(tmp_path / 'views.sqlite'), '--archive', str(tmp_path / 'new-archive.sqlite'), '--workers', '1'])
    runpy.run_path(str(SCRIPT), run_name='__main__')
    with sqlite3.connect(tmp_path / 'views.sqlite') as conn:
        handover = json.loads(conn.execute('select handover_json from handovers').fetchone()[0])
        assert ['e9', 'no home'] in handover['dropped']
