"""D172: the opt-in coordinator preserves ordered knowledge on real temporary storage."""
import collections
import dataclasses
import json
from pathlib import Path
import re
import sqlite3
import sys
import threading

import pytest

from test_sequential_replay import CASES, setup_run
from hivemind import config, extraction, model, replay, vocabulary
from hivemind.views import store

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'poc'))
from concurrency_study.runner import DayRunner, extraction_key  # noqa: E402


def responses(*, reverse=False, fail_first=False, fail_current_second=False, fail_stale_second=False):
    """Only the external model is faked. Both quotations come from the recorded Rubin cases."""
    later_finished, lock = threading.Event(), threading.Lock()
    calls = []

    def send(provider, request):
        name = request['response_format']['json_schema']['name']
        text = request['messages'][1]['content']
        second = CASES[1]['item']['input_id'] in text
        current = CASES[0]['candidate']['question'] in text
        with lock:
            calls.append((name, second, current))
        if name == 'extraction':
            if second:
                later_finished.set()
                if current and fail_current_second:
                    raise model.TransportError('second current request unavailable')
                if not current and fail_stale_second:
                    raise model.TransportError('unused speculative request unavailable')
                data = ({'candidates': [], 'evidence': [dict(CASES[1]['evidence'], links=['v1'])]}
                        if current else {'candidates': [CASES[1]['candidate']], 'evidence': [CASES[1]['evidence']]})
            else:
                if reverse:
                    assert later_finished.wait(5), 'later extraction did not overlap the first'
                if fail_first:
                    raise model.TransportError('first request unavailable')
                data = {'candidates': [CASES[0]['candidate']], 'evidence': [CASES[0]['evidence']]}
        elif name == 'matching':
            if '【候选观点】' in text:
                data = {'candidates': [{'id': 'c1', 'outcome': '新观点', 'target_view_id': '', 'reason': 'new', 'dependencies': []}], 'evidence': []}
            else:
                data = {'candidates': [], 'evidence': [{'id': 'e1', 'view_id': 'v1', 'outcome': '新证据', 'target_evidence_id': '', 'said_day': '', 'reason': 'another statement'}]}
        else:
            assert name == 'judgement'
            data = {'rung': 1, 'reasons': 'Production shipments are expected.',
                    'cites': list(dict.fromkeys(re.findall(r'^- (e\d+)［', text, re.M))), 'cites_views': [], 'pushes': [],
                    'changed': True, 'why_changed': 'First judgement.'}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    return send, calls


def runner(args, tmp_path):
    return DayRunner(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=1)


def logical_rows(path):
    """Compare product records, excluding call identities and audit timestamps."""
    ignored = {'created_at', 'call_id', 'request_sha256'}
    with sqlite3.connect(path) as db:
        db.row_factory = sqlite3.Row
        return {table: [{k: row[k] for k in row.keys() if k not in ignored} for row in db.execute(f'select * from {table} order by rowid')]
                for table in ('views', 'rungs', 'evidence', 'evidence_sources', 'evidence_links', 'dependencies',
                              'successions', 'thesis_groups', 'thesis_group_members', 'judgements')}


def test_reversed_answers_and_stale_context_match_the_serial_ledger(tmp_path):
    """D172 current-prefix rule: the later speculative answer cannot create a second thesis."""
    a = tmp_path / 'serial'; a.mkdir()
    b = tmp_path / 'parallel'; b.mkdir()
    serial, parallel = setup_run(a), setup_run(b)
    send, _ = responses()
    expected = replay.run(**serial, transport=send)
    send, calls = responses(reverse=True)
    day = runner(parallel, b)
    actual = replay.run(**parallel, transport=send, day_runner=day)
    assert logical_rows(serial['views_path']) == logical_rows(parallel['views_path'])
    assert (actual['new_views'], actual['evidence'], actual['judged']) == (1, 2, 1)
    assert expected['new_views'] == actual['new_views']
    assert [e['input_id'] for e in day.events if e['event'] == 'accepted'] == [c['item']['input_id'] for c in CASES]
    assert [e['input_id'] for e in day.events if e['event'] == 'stale'] == [CASES[1]['item']['input_id']]
    assert collections.Counter((name, second) for name, second, _ in calls)[('extraction', True)] == 2


def test_stale_request_is_prepared_again_right_after_the_commit_that_changed_it(tmp_path):
    """D181 scheduling row: the changed request is sent before its turn, and the turn accepts it after validation."""
    args = setup_run(tmp_path)
    send, calls = responses(reverse=True)
    day = runner(args, tmp_path)
    replay.run(**args, transport=send, day_runner=day)
    later = CASES[1]['item']['input_id']
    order = [(e['input_id'], e['event']) for e in day.events]
    assert order.index((later, 'stale')) < order.index((later, 'turn'))
    assert (later, 'reused') in order and (later, 'reextracted') not in order
    assert sum(name == 'extraction' and second for name, second, _ in calls) == 2


def test_earlier_failure_accepts_no_later_handover_and_resume_preserves_order(tmp_path):
    """D172 failure row: early calls may finish, but later knowledge cannot commit."""
    args = setup_run(tmp_path)
    day = runner(args, tmp_path)
    send, _ = responses(reverse=True, fail_first=True)
    with pytest.raises(RuntimeError, match='first request unavailable'):
        replay.run(**args, transport=send, day_runner=day)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from handovers').fetchone()[0] == 0
        assert db.execute('select count(*) from views').fetchone()[0] == 0
        assert db.execute('select count(*) from days_completed').fetchone()[0] == 0
    send, _ = responses()
    resumed = replay.run(**args, transport=send, day_runner=runner(args, tmp_path))
    assert (resumed['new_views'], resumed['evidence']) == (1, 2)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute("select input_id,sequence_no from processing_steps where step='extracted' and result='ok' order by id").fetchall() == [(c['item']['input_id'], n) for n, c in enumerate(CASES, 1)]


def test_writer_failure_resumes_the_accepted_handover_without_reextracting(tmp_path):
    """D172 restart row: accepted extraction survives a rolled-back write."""
    args = setup_run(tmp_path)
    db = store.open_db(args['views_path'])
    db.execute("create trigger refuse_piece before insert on evidence begin select raise(abort, 'offline storage fault'); end")
    db.commit(); db.close()
    send, calls = responses()
    with pytest.raises(RuntimeError, match='offline storage fault'):
        replay.run(**args, transport=send, day_runner=runner(args, tmp_path))
    first_calls = sum(name == 'extraction' and not second for name, second, _ in calls)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from views').fetchone()[0] == 0
        assert db.execute('select count(*) from handovers').fetchone()[0] == 1
        db.execute('drop trigger refuse_piece')
    result = replay.run(**args, transport=send, day_runner=runner(args, tmp_path))
    assert result['new_views'] == 1
    assert sum(name == 'extraction' and not second for name, second, _ in calls) == first_calls


def test_unused_stale_failure_does_not_replace_the_current_request(tmp_path):
    """D172 stale failure: an unavailable old request cannot poison a changed valid request."""
    args = setup_run(tmp_path)
    day = runner(args, tmp_path)
    send, _ = responses(reverse=True, fail_stale_second=True)
    result = replay.run(**args, transport=send, day_runner=day)
    assert (result['new_views'], result['evidence']) == (1, 2)
    assert any(e['event'] == 'speculative_error' for e in day.events)


def test_later_day_does_not_run_after_current_day_failure(tmp_path):
    """D172 day boundary: a committed prefix is not a completed day."""
    args = setup_run(tmp_path)
    with sqlite3.connect(args['testdb_path']) as db:
        columns = [r[1] for r in db.execute('pragma table_info(items)')]
        db.row_factory = sqlite3.Row
        item = dict(db.execute('select * from items limit 1').fetchone())
        item.update(input_id='test:next-day', publication_day='2026-02-26', published_at='2026-02-26T21:00:00Z')
        db.execute(f'insert into items ({",".join(columns)}) values ({",".join("?" for _ in columns)})', [item[c] for c in columns])
    args['until_day'] = '2026-02-26'
    send, _ = responses(fail_current_second=True)
    requests = []
    def checked(provider, request):
        requests.append(request['messages'][1]['content'])
        return send(provider, request)
    with pytest.raises(RuntimeError, match='second current request unavailable'):
        replay.run(**args, transport=checked, day_runner=runner(args, tmp_path))
    assert not any('test:next-day' in request for request in requests)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from views').fetchone()[0] == 1
        assert db.execute('select count(*) from days_completed').fetchone()[0] == 0


@pytest.mark.parametrize('change', ['source', 'config'])
def test_changed_source_or_configuration_refuses_before_more_calls(tmp_path, change):
    """D172 manifest row: restarting is not permission to replace the input contract."""
    args = setup_run(tmp_path)
    send, _ = responses(fail_first=True)
    with pytest.raises(RuntimeError):
        replay.run(**args, transport=send, day_runner=runner(args, tmp_path))
    if change == 'source':
        with sqlite3.connect(args['testdb_path']) as db:
            db.execute('update items set text=text || ?', (' changed',))
    else:
        args['cfg'] = dataclasses.replace(args['cfg'], version='different-configuration')
    def forbidden(*args):
        raise AssertionError('manifest mismatch reached a model call')
    with pytest.raises(ValueError, match='manifest .* changed'):
        replay.run(**args, transport=forbidden, day_runner=runner(args, tmp_path))


def test_group_membership_and_schema_changes_change_the_request_identity(tmp_path):
    """D172 read set includes group members and the allowed response schema, not just thesis IDs."""
    from test_jev_matching import ledger_with_view, CFG, UNIVERSE
    conn, _ = ledger_with_view(tmp_path)
    store.add_group(conn, group_id='g1', name='Rubin rollout', scope='production and deployment', seq=1,
                    input_id='seed', object_ids=['NVDA'], aliases=['Rubin'])
    store.add_member(conn, 'g1', 'v1', 1, 'seed')
    item = dict(CASES[0]['item'], title='Rubin rollout')
    shown = store.views_for_prompt(conn, ['NVDA'])
    before = extraction_key(CFG, item, item['text'], shown, UNIVERSE, store.groups_for_prompt(conn, ['NVDA'], item['title']))
    store.create_view(conn, view_id='v2', object_id='AMD', object_kind='company', kind='asset', looks_at='Rubin customer deployment',
                      question='Will the customer deploy?', due_day='2027-12-31', year='2027', rungs=CASES[0]['candidate']['rungs'],
                      seq=2, input_id='other', created_at='2026-02-25T22:00:00')
    store.add_member(conn, 'g1', 'v2', 2, 'other')
    assert store.views_for_prompt(conn, ['NVDA']) == shown
    after = extraction_key(CFG, item, item['text'], shown, UNIVERSE, store.groups_for_prompt(conn, ['NVDA'], item['title']))
    assert before != after
    request = {'messages': [{'content': 'unchanged'}], 'response_format': {'schema': {'enum': ['v1']}}}
    original = model.request_identity(request)[1]
    request['response_format']['schema']['enum'].append('v2')
    assert model.request_identity(request)[1] != original


def test_opt_in_runner_never_implicitly_uses_credentials(tmp_path):
    """D172 live-launch boundary: the offline POC cannot silently use default network transport."""
    args = setup_run(tmp_path)
    with pytest.raises(ValueError, match='explicit transport'):
        replay.run(**args, day_runner=runner(args, tmp_path))


def test_current_english_jev_pipeline_preserves_sources_groups_and_call_trace(tmp_path):
    """D172 product path: v23 extraction, Jev, grouping, write, daily judgement and close marker."""
    args = setup_run(tmp_path)
    args['cfg'] = config.load(ROOT / 'poc/config/poc-v23.json')
    later = threading.Event()
    def send(*parameters):
        request = parameters[-1]
        if len(parameters) == 1:  # Jev uses its typed endpoint.
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
        if stage == 'extraction':
            second = CASES[1]['item']['input_id'] in text
            if second:
                later.set()
            else:
                assert later.wait(5)
            case = CASES[int(second)]
            raw = vocabulary.extraction_answer({'candidates': [case['candidate']], 'evidence': [case['evidence']]})
            raw['new_groups'] = []
            if second and '  - v1 (' in text:
                raw['candidates'] = []
                raw['evidence'][0]['links'] = ['v1']
            else:
                raw['candidates'][0]['group_refs'] = ['n1']
                raw['new_groups'] = [{'id': 'n1', 'name': 'Rubin rollout', 'scope': 'Rubin production and deployment', 'aliases': ['Rubin']}]
            return {'choices': [{'message': {'content': json.dumps(raw)}}]}
        assert stage == 'judgement'
        result = {'rung': 1, 'reasons': 'Both original sources expect production.',
                  'cites': list(dict.fromkeys(re.findall(r'^- (e\d+) \[', text, re.M))), 'cites_views': [],
                  'pushes': [], 'changed': True, 'why_changed': 'First judgement.'}
        return {'choices': [{'message': {'content': json.dumps(result)}}]}
    day = DayRunner(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=2)
    result = replay.run(**args, transport=send, day_runner=day)
    assert (result['new_views'], result['evidence'], result['judged']) == (1, 2, 1)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select name from thesis_groups').fetchall() == [('Rubin rollout',)]
        assert db.execute('select group_id,view_id from thesis_group_members').fetchall() == [('g1', 'v1')]
        assert db.execute('select quote from evidence order by rowid').fetchall() == [(c['evidence']['quote'],) for c in CASES]
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]
        records = [json.loads(r[0]) for r in db.execute('select shown_json from match_records')]
        requests = [entry for record in records for entry in record.get('requests', [])]
    assert requests
    for entry in requests:
        assert args['archive'].conn.execute('select request_sha256 from model_calls where call_id=?', (entry['call_id'],)).fetchone()[0] == entry['request_sha256']


def test_day_cost_includes_discarded_speculative_calls(tmp_path):
    """D172 cost reader: stale work is still billed and must remain in the day total."""
    args = setup_run(tmp_path)
    lines = []
    args['log'] = lines.append
    base, _ = responses()
    def billed(provider, request):
        result = base(provider, request)
        result['usage'] = {'prompt_tokens': 100_000, 'completion_tokens': 0}
        return result
    replay.run(**args, transport=billed, day_runner=runner(args, tmp_path))
    cost = args['archive'].totals()[1]
    assert args['archive'].totals()[0] == 6  # Two accepted extractions plus one stale extraction, two matches, one judgement.
    assert f'day ${cost:.2f}' in lines[-1]
