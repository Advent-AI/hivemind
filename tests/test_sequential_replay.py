"""D159: the next extraction reads the committed predecessor, including after a failed run."""
import json
import shutil
import sqlite3
from pathlib import Path

import pytest

from hivemind import config, model, replay, universe
from hivemind.views import store

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'tests/fixtures/sequential-rubin.json').read_text())


def setup_run(tmp_path):
    path = tmp_path / 'items.sqlite'
    with sqlite3.connect(path) as db:
        db.execute('create table items (input_id, publisher, published_at, publication_day, category, '
                   'source_uri, text, object_identifiers, feed, copy_of, klass)')
        for case in CASES:
            item = dict(case['item'], object_identifiers=json.dumps(case['item']['object_identifiers']))
            columns = list(item)
            db.execute(f'insert into items ({",".join(columns)}) values ({",".join("?" for _ in columns)})',
                       [item[k] for k in columns])
    return dict(testdb_path=str(path), views_path=str(tmp_path / 'views.sqlite'),
                archive=model.Archive(str(tmp_path / 'archive.sqlite')),
                cfg=config.load(ROOT / 'poc/config/poc-v16.json'), universe=universe.load(ROOT / 'poc/universe.json'),
                from_day='2026-02-25', until_day='2026-02-25', log=lambda *args: None)


def transport_for(args, calls, *, fail_first=False):
    def send(provider, request):
        name = request['response_format']['json_schema']['name']
        text = request['messages'][1]['content']
        second = name in ('extraction', 'matching') and CASES[1]['item']['input_id'] in text
        calls.append((name, second))
        if name == 'extraction':
            if fail_first and not second:
                raise model.TransportError('offline')
            if second:
                # The connection sees committed data, not the writer's uncommitted transaction.
                with sqlite3.connect(args['views_path']) as db:
                    rows = db.execute('select question from views').fetchall()
                assert rows == [(CASES[0]['candidate']['question'],)]
                assert CASES[0]['candidate']['question'] in text
                data = {'candidates': [], 'evidence': [dict(CASES[1]['evidence'], links=['v1'])]}
            else:
                data = {'candidates': [CASES[0]['candidate']], 'evidence': [CASES[0]['evidence']]}
        elif name == 'matching':
            data = ({'candidates': [], 'evidence': [{'id': 'e1', 'view_id': 'v1', 'outcome': '新证据',
                      'target_evidence_id': '', 'said_day': '', 'reason': 'The filing supplies another statement.'}]}
                    if second else {'candidates': [{'id': 'c1', 'outcome': '新观点', 'target_view_id': '',
                      'reason': 'No earlier view.', 'dependencies': []}], 'evidence': []})
        else:
            assert name == 'judgement'
            data = {'rung': 1, 'reasons': 'Both statements expect production shipments.', 'cites': ['e1', 'e2'],
                    'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'First judgement.'}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}
    return send


def test_next_extraction_reads_committed_prior_view(tmp_path):
    """D159 normal same-day row: two real statements pass the public replay entry point."""
    args, calls = setup_run(tmp_path), []
    result = replay.run(**args, transport=transport_for(args, calls))
    assert calls == [('extraction', False), ('matching', False), ('extraction', True),
                     ('matching', True), ('judgement', False)]
    assert (result['extracted'], result['new_views'], result['evidence'], result['judged']) == (2, 1, 2, 1)
    db = store.open_db(args['views_path'])
    assert store.last_completed_day(db) == '2026-02-25'
    assert len(store.evidence_in_force(db, 'v1')) == 2


def test_failure_stops_later_extraction_and_resume_keeps_sequence(tmp_path):
    """D159 refused/crash row: failure cannot launch later extraction; normal resume uses the original IDs."""
    args, calls = setup_run(tmp_path), []
    with pytest.raises(RuntimeError, match='remains resumable'):
        replay.run(**args, transport=transport_for(args, calls, fail_first=True))
    assert calls == [('extraction', False)]
    db = store.open_db(args['views_path'])
    assert store.last_completed_day(db) is None
    result = replay.run(**args, transport=transport_for(args, calls))
    assert result['new_views'] == 1
    assert [(r['input_id'], r['sequence_no']) for r in db.execute(
        "select input_id, sequence_no from processing_steps where step='extracted' and result='ok' order by id"
    )] == [(case['item']['input_id'], n) for n, case in enumerate(CASES, 1)]


def test_old_parallel_handover_refuses_without_new_calls_or_processing(tmp_path):
    """D159 legacy row: the actual five unfinished pre-extractions must not silently resume."""
    args = setup_run(tmp_path)
    source = ROOT / 'poc/data/views-2026-10-25-v15-T2b-aborted-fresh-archive.sqlite'
    shutil.copyfile(source, args['views_path'])
    db = store.open_db(args['views_path'])
    before = db.execute('select count(*) from processing_steps').fetchone()[0]
    pending = [r[0] for r in db.execute("select input_id from processing_steps where step='extracted'")]
    assert len(pending) == 5
    calls = []
    with pytest.raises(replay.StaleHandoverError) as caught:
        replay.run(**args, transport=transport_for(args, calls))
    assert all(ident in str(caught.value) for ident in pending)
    assert not calls and db.execute('select count(*) from processing_steps').fetchone()[0] == before
