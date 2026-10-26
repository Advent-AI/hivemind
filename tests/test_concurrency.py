"""D172/D181: the parallel day preserves ordered knowledge on real temporary storage."""
import collections
import dataclasses
import json
from pathlib import Path
import re
import shutil
import sqlite3
import sys
import threading

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'poc'))
from test_sequential_replay import CASES, setup_run  # noqa: E402
from hivemind import config, extraction, jev, model, parallel_day, replay, vocabulary  # noqa: E402
from hivemind.parallel_day import ParallelDay, extraction_key  # noqa: E402
from hivemind.views import store  # noqa: E402
from concurrency_study.proof import ledger_rows as logical_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


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
    return ParallelDay(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=1)


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


def test_group_membership_and_schema_changes_change_the_request_identity(tmp_path, monkeypatch):
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
    groups = store.groups_for_prompt(conn, ['NVDA'], item['title'])
    _, system, user, schema = extraction.request_for(CFG, item, item['text'], shown, UNIVERSE, groups)
    schema_for = extraction.schema_for
    monkeypatch.setattr(extraction, 'schema_for', lambda version, ids, views=(): dict(schema_for(version, ids, views), description='changed schema only'))
    _, system2, user2, schema2 = extraction.request_for(CFG, item, item['text'], shown, UNIVERSE, groups)
    assert (system2, user2) == (system, user) and schema2 != schema
    assert extraction_key(CFG, item, item['text'], shown, UNIVERSE, groups) != after


@pytest.mark.parametrize('extra_arguments, parallel', [([], True), (['--workers', '1'], False)])
def test_replay_script_runs_the_parallel_day_by_default_and_serially_with_one_worker(tmp_path, monkeypatch, extra_arguments, parallel):
    """D183 entry point: `scripts/replay.py` with its defaults runs the parallel day (16 workers; one matching question at
    a time for a non-Jev matcher), `--workers 1` the serial path; both write the serial ledger."""
    import runpy
    serial_dir = tmp_path / 'serial'; serial_dir.mkdir()
    serial = setup_run(serial_dir)
    send, _ = responses()
    replay.run(**serial, transport=send)
    args = setup_run(tmp_path)
    send, calls = responses(reverse=parallel)
    monkeypatch.setattr(model, 'openai_transport', send)
    monkeypatch.setattr(model, '_key', lambda provider: pytest.fail('credentials read'))
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-02-25', '--until', '2026-02-25', '--testdb', args['testdb_path'],
                                      '--views', args['views_path'], '--archive', str(tmp_path / 'cli-archive.sqlite'),
                                      '--config', str(ROOT / 'poc/config/poc-v16.json')] + extra_arguments)
    runpy.run_path(str(ROOT / 'scripts/replay.py'), run_name='__main__')
    assert (tmp_path / 'manifests' / 'day-2026-02-25.json').is_file() == parallel
    assert sum(name == 'extraction' and second for name, second, _ in calls) == (2 if parallel else 1)
    assert logical_rows(serial['views_path']) == logical_rows(args['views_path'])


def test_replay_script_defaults_run_the_default_jev_configuration_with_sixteen_and_eight_workers(tmp_path, monkeypatch):
    """D183/D189 entry point as the user calls it: no --config, --workers or --jev-workers; the default configuration (poc-v25,
    extraction v12 on Jev) runs the parallel day with 16 extraction and 8 Jev workers and writes the serial ledger."""
    import runpy
    serial_dir = tmp_path / 'serial'; serial_dir.mkdir()
    serial = setup_run(serial_dir)
    serial['cfg'] = config.load(ROOT / 'poc/config/poc-v25.json')
    replay.run(**serial, transport=english_jev_send(require_overlap=False))
    args = setup_run(tmp_path)
    send = english_jev_send(require_overlap=True)
    monkeypatch.setattr(model, 'openai_transport', lambda provider, request, timeout=600: send(provider, request))
    monkeypatch.setattr(jev, 'transport', lambda request, timeout=60: send(request))
    monkeypatch.setattr(model, '_key', lambda provider: pytest.fail('credentials read'))
    monkeypatch.setattr(jev, '_key', lambda: pytest.fail('credentials read'))
    built = []

    class RecordedParallelDay(ParallelDay):
        def __init__(self, *arguments, **options):
            built.append(options)
            super().__init__(*arguments, **options)
    monkeypatch.setattr(parallel_day, 'ParallelDay', RecordedParallelDay)
    monkeypatch.setattr(sys, 'argv', ['replay.py', '--from', '2026-02-25', '--until', '2026-02-25', '--testdb', args['testdb_path'],
                                      '--views', args['views_path'], '--archive', str(tmp_path / 'cli-archive.sqlite')])
    runpy.run_path(str(ROOT / 'scripts/replay.py'), run_name='__main__')
    assert built == [{'extraction_workers': 16, 'jev_workers': 8}]
    assert logical_rows(serial['views_path']) == logical_rows(args['views_path'])


def test_restart_counts_the_days_items_already_written_toward_its_item_limit(tmp_path):
    """D183 restart row: `max_items_per_day` counts the day's items an earlier run already wrote, so a restart selects
    the same items (the parallel day's manifest accepts it) and never dispatches an item beyond the limit."""
    args = setup_run(tmp_path)
    send, _ = responses()

    def judging_fails(provider, request):
        if request['response_format']['json_schema']['name'] == 'judgement':
            raise model.TransportError('judging unavailable')
        return send(provider, request)
    with pytest.raises(RuntimeError, match='judging failed'):
        replay.run(**args, transport=judging_fails, max_items_per_day=1, day_runner=runner(args, tmp_path))
    replay.run(**args, transport=send, max_items_per_day=1, day_runner=runner(args, tmp_path))
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from processing_steps where input_id=?', (CASES[1]['item']['input_id'],)).fetchone()[0] == 0
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]


def test_fresh_ledger_starts_its_day_over_a_manifest_another_ledger_left(tmp_path):
    """D183 manifest row: a manifest guards a ledger's unfinished day; a fresh ledger in the same folder, with nothing of
    that day written, starts the day under its own configuration instead of refusing it."""
    first_dir = tmp_path / 'first'; first_dir.mkdir()
    first = setup_run(first_dir)
    send, _ = responses()
    replay.run(**first, transport=send, day_runner=ParallelDay(Path(first['testdb_path']), tmp_path / 'manifests',
                                                                extraction_workers=2, jev_workers=1))
    second = setup_run(tmp_path)
    second['cfg'] = dataclasses.replace(second['cfg'], version='changed-after-the-first-ledger')
    send, _ = responses()
    replay.run(**second, transport=send, day_runner=runner(second, tmp_path))
    with sqlite3.connect(second['views_path']) as db:
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]


def test_ledger_comparison_covers_every_product_table(tmp_path):
    """D182/D183 check: the serial-against-parallel comparison reads every product table; a replacement row, which the
    earlier ten-table comparison did not read, makes two otherwise identical ledgers differ."""
    args = setup_run(tmp_path)
    send, _ = responses()
    replay.run(**args, transport=send)
    changed = tmp_path / 'changed.sqlite'
    shutil.copyfile(args['views_path'], changed)
    assert logical_rows(changed) == logical_rows(args['views_path'])
    with sqlite3.connect(changed) as db:
        db.execute("insert into replacements(old_evidence_id,new_evidence_id,said_day,seq) values ('e1','e2','2026-02-25',2)")
    before, after = logical_rows(args['views_path']), logical_rows(changed)
    assert set(after) == set(store.TABLES)
    assert [table for table in after if after[table] != before[table]] == ['replacements']


def english_jev_send(*, require_overlap):
    """Fake OpenAI and Jev providers for the v23 English pipeline over the two recorded Rubin cases; with
    `require_overlap` the first extraction answers only after the second was sent."""
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
            elif require_overlap:
                assert later.wait(5), 'later extraction did not overlap the first'
            case = CASES[int(second)]
            raw = vocabulary.extraction_answer({'candidates': [case['candidate']], 'evidence': [case['evidence']]})
            raw['new_groups'] = []
            if 'opens_as' in request['response_format']['json_schema']['schema']['properties']['candidates']['items']['properties']:     # a version-12 request (D184)
                raw['candidates'][0].update(opens_as='main_driver', folds_into='', lost_if_folded='', settled_by='the FY2027 annual report')
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

    return send


def test_current_english_jev_pipeline_preserves_sources_groups_and_call_trace(tmp_path):
    """D172 product path: v23 extraction, Jev, grouping, write, daily judgement and close marker."""
    args = setup_run(tmp_path)
    args['cfg'] = config.load(ROOT / 'poc/config/poc-v23.json')
    send = english_jev_send(require_overlap=True)
    day = ParallelDay(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=2)
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


def test_audit_binds_each_handover_to_the_request_the_runner_accepted(tmp_path):
    """D181 review: the proof checks which request each turn accepted, not only that the handover content matches."""
    sys.path.insert(0, str(ROOT / 'poc'))
    from concurrency_study.proof import accepted_requests, handover_errors
    args = setup_run(tmp_path)
    send, _ = responses(reverse=True)
    day = runner(args, tmp_path)
    replay.run(**args, transport=send, day_runner=day)
    archive = args['archive'].conn
    def answer_for(key):
        row = archive.execute('select answer_json from model_calls where request_sha256=?', (key,)).fetchone()
        return row[0] if row else None
    accepted = accepted_requests(day.events)
    with sqlite3.connect(args['views_path']) as conn:
        conn.row_factory = sqlite3.Row
        items = [c['item'] for c in CASES]
        assert handover_errors(conn, items, args['cfg'], args['universe'], 1, answer_for, accepted)[0] == []
        stale = [e['before'] for e in day.events if e['event'] == 'stale'][0]
        accepted[CASES[1]['item']['input_id']] = stale
        errors = handover_errors(conn, items, args['cfg'], args['universe'], 1, answer_for, accepted)[0]
    assert errors == ['the runner accepted another request: ' + CASES[1]['item']['input_id']]
