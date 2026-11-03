"""The replay of the production configuration (poc-v108) over two recorded items of one day, with only the providers faked: a failed
item stops the day and a resume keeps the sequence (D159), and a ledger an older parallel run left unfinished is refused."""
import json
import re
import shutil
import sqlite3
import threading
from pathlib import Path

import pytest

from hivemind import config, model, replay, universe, vocabulary
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
                cfg=config.load(ROOT / 'poc/config/poc-v108.json'), universe=universe.load(ROOT / 'poc/universe.json'),
                from_day='2026-02-25', until_day='2026-02-25', log=lambda *args: None)


def v108_send(calls=None, *, require_overlap=False, fail_first=False, fail_current_second=False, fail_stale_second=False, fail_judging=False):
    """Fake OpenAI and Jev providers for poc-v108 over the two recorded Rubin cases. `calls` records (stage, second, current) per
    model request: second says the request is the second item's, current that it shows the question v1. With `require_overlap` the
    first extraction answers only after the second was sent."""
    later, lock = threading.Event(), threading.Lock()
    calls = [] if calls is None else calls

    def send(*parameters):
        request = parameters[-1]
        if len(parameters) == 1:  # Jev uses its typed endpoint
            result = {}
            for qid, question in request['questions'].items():
                if question['type'] == 'noul':
                    result[qid] = {'type': 'noul', 'noul': 0.9}
                else:
                    labels = question['criteria']
                    result[qid] = {'type': 'choice', 'choice': 'different', 'confidence': 1.0,
                                   'probabilities': {label: float(label == 'different') for label in labels}}
            return {'answers': result, 'usage': {}}
        text = request['messages'][1]['content']
        stage = request['response_format']['json_schema']['name']
        second = CASES[1]['item']['input_id'] in text
        current = '  - v1 (' in text
        with lock:
            calls.append((stage, second, current))
        if stage == 'extraction':
            if second:
                later.set()
                if current and fail_current_second:
                    raise model.TransportError('second current request unavailable')
                if not current and fail_stale_second:
                    raise model.TransportError('unused speculative request unavailable')
            else:
                if require_overlap:
                    assert later.wait(5), 'later extraction did not overlap the first'
                if fail_first:
                    raise model.TransportError('first request unavailable')
            case = CASES[int(second)]
            raw = vocabulary.extraction_answer({'candidates': [case['candidate']], 'evidence': [case['evidence']]})
            raw['candidates'][0].update(opens_as='main_driver', settled_by='the FY2027 annual report')
            if second and current:
                raw['candidates'], raw['new_groups'] = [], []
                raw['evidence'][0]['links'] = ['v1']
            else:
                raw['candidates'][0]['group_refs'] = ['n1']
                raw['new_groups'] = [{'id': 'n1', 'name': 'Rubin rollout', 'scope': 'Rubin production and deployment', 'aliases': ['Rubin']}]
            return {'choices': [{'message': {'content': json.dumps(raw)}}]}
        if stage == 'collision':                       # D190: the judge answers no verdict here, so Jev's decision stands
            return {'choices': [{'message': {'content': json.dumps({'relations': []})}}]}
        assert stage == 'judgement'
        if fail_judging:
            raise model.TransportError('judging unavailable')
        result = {'rung': 1, 'reference': 'consensus expects production this year', 'implied_outcome': 'production shipments in the year',
                  'reasons': 'Both original sources expect production.', 'cites': list(dict.fromkeys(re.findall(r'^- (e\d+) \[', text, re.M))),
                  'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'First judgement.', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(result)}}]}

    return send


def test_failure_stops_later_extraction_and_resume_keeps_sequence(tmp_path):
    """D159 refused/crash row: a failed item stops the day before any later extraction; the resume uses the original ids."""
    args, calls = setup_run(tmp_path), []
    with pytest.raises(RuntimeError, match='remains resumable'):
        replay.run(**args, transport=v108_send(calls, fail_first=True))
    assert calls == [('extraction', False, False)]
    db = store.open_db(args['views_path'])
    assert store.last_completed_day(db) is None
    result = replay.run(**args, transport=v108_send(calls))
    assert result['new_views'] == 2 and store.last_completed_day(db) == '2026-02-25'
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
        replay.run(**args, transport=v108_send(calls))
    assert all(ident in str(caught.value) for ident in pending)
    assert not calls and db.execute('select count(*) from processing_steps').fetchone()[0] == before
