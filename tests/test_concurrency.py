"""D172/D181/D183: the parallel day preserves ordered knowledge on real temporary storage, under the production configuration
(poc-v108). Its requests read the questions open at the start of the day (D251), so a commit never changes a waiting request; the
turn still validates every prepared request against the one it would build now, and the tests that exercise that guard make the
request read the questions open now (`reading_the_questions_open_now`)."""
import collections
import dataclasses
import json
from pathlib import Path
import shutil
import sqlite3
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'poc'))
from test_sequential_replay import CASES, setup_run, v108_send  # noqa: E402
from hivemind import config, extraction, jev, model, parallel_day, replay  # noqa: E402
from hivemind.parallel_day import ParallelDay, extraction_key  # noqa: E402
from hivemind.views import store  # noqa: E402
from concurrency_study.proof import ledger_rows as logical_rows  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def runner(args, tmp_path):
    return ParallelDay(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=1)


def reading_the_questions_open_now(monkeypatch):
    """The request shows every question open now, not only those open at the day's start, so the first item's commit changes the
    second item's waiting request: the case the turn's validation exists for."""
    day_start = extraction.shown_views

    def open_now(conn, cfg, item, objects):
        shown = day_start(conn, cfg, item, objects)
        ids = {v['view_id'] for v in shown}
        return shown + [dict(store.view(conn, view_id), key=store.view_key(conn, view_id) or {}, groups=[], parents=[])
                        for view_id in store.open_views(conn) if view_id not in ids]
    monkeypatch.setattr(extraction, 'shown_views', open_now)


def test_reversed_answers_match_the_serial_ledger(tmp_path):
    """D172 current-prefix rule: answers that arrive in reverse order write the serial ledger; each item is read once."""
    a = tmp_path / 'serial'; a.mkdir()
    b = tmp_path / 'parallel'; b.mkdir()
    serial, parallel = setup_run(a), setup_run(b)
    expected = replay.run(**serial, transport=v108_send())
    calls = []
    day = runner(parallel, b)
    actual = replay.run(**parallel, transport=v108_send(calls, require_overlap=True), day_runner=day)
    assert logical_rows(serial['views_path']) == logical_rows(parallel['views_path'])
    assert (actual['new_views'], actual['evidence'], actual['judged']) == (2, 2, 2) and expected['new_views'] == actual['new_views']
    assert [e['input_id'] for e in day.events if e['event'] == 'accepted'] == [c['item']['input_id'] for c in CASES]
    assert not [e for e in day.events if e['event'] == 'stale']          # the day-start list does not move within the day
    assert collections.Counter(stage for stage, _, _ in calls)['extraction'] == 2


def test_stale_request_is_prepared_again_right_after_the_commit_that_changed_it(tmp_path, monkeypatch):
    """D181 scheduling row: the changed request is sent before its turn, and the turn accepts it after validation."""
    reading_the_questions_open_now(monkeypatch)
    args, calls = setup_run(tmp_path), []
    day = runner(args, tmp_path)
    result = replay.run(**args, transport=v108_send(calls, require_overlap=True), day_runner=day)
    later = CASES[1]['item']['input_id']
    order = [(e['input_id'], e['event']) for e in day.events]
    assert order.index((later, 'stale')) < order.index((later, 'turn'))
    assert (later, 'reused') in order and (later, 'reextracted') not in order
    assert sum(stage == 'extraction' and second for stage, second, _ in calls) == 2
    assert (result['new_views'], result['evidence']) == (1, 2)      # the current request files the second statement under v1


def test_earlier_failure_accepts_no_later_handover_and_resume_preserves_order(tmp_path):
    """D172 failure row: early calls may finish, but later knowledge cannot commit."""
    args = setup_run(tmp_path)
    with pytest.raises(RuntimeError, match='first request unavailable'):
        replay.run(**args, transport=v108_send(require_overlap=True, fail_first=True), day_runner=runner(args, tmp_path))
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from handovers').fetchone()[0] == 0
        assert db.execute('select count(*) from views').fetchone()[0] == 0
        assert db.execute('select count(*) from days_completed').fetchone()[0] == 0
    resumed = replay.run(**args, transport=v108_send(), day_runner=runner(args, tmp_path))
    assert (resumed['new_views'], resumed['evidence']) == (2, 2)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute("select input_id,sequence_no from processing_steps where step='extracted' and result='ok' order by id").fetchall() == [(c['item']['input_id'], n) for n, c in enumerate(CASES, 1)]


def test_writer_failure_resumes_the_accepted_handover_without_reextracting(tmp_path):
    """D172 restart row: accepted extraction survives a rolled-back write."""
    args = setup_run(tmp_path)
    db = store.open_db(args['views_path'])
    db.execute("create trigger refuse_piece before insert on evidence begin select raise(abort, 'offline storage fault'); end")
    db.commit(); db.close()
    calls = []
    with pytest.raises(RuntimeError, match='offline storage fault'):
        replay.run(**args, transport=v108_send(calls), day_runner=runner(args, tmp_path))
    first_calls = sum(stage == 'extraction' and not second for stage, second, _ in calls)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from views').fetchone()[0] == 0
        assert db.execute('select count(*) from handovers').fetchone()[0] == 1
        db.execute('drop trigger refuse_piece')
    result = replay.run(**args, transport=v108_send(calls), day_runner=runner(args, tmp_path))
    assert result['new_views'] == 2
    assert sum(stage == 'extraction' and not second for stage, second, _ in calls) == first_calls


def test_unused_stale_failure_does_not_replace_the_current_request(tmp_path, monkeypatch):
    """D172 stale failure: an unavailable old request cannot poison a changed valid request."""
    reading_the_questions_open_now(monkeypatch)
    args = setup_run(tmp_path)
    day = runner(args, tmp_path)
    result = replay.run(**args, transport=v108_send(require_overlap=True, fail_stale_second=True), day_runner=day)
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
    send, requests = v108_send(fail_stale_second=True), []      # the second item's only request (it shows no v1) is unavailable

    def checked(*parameters):
        if len(parameters) == 2:
            requests.append(parameters[1]['messages'][1]['content'])
        return send(*parameters)
    with pytest.raises(RuntimeError, match='unused speculative request unavailable'):
        replay.run(**args, transport=checked, day_runner=runner(args, tmp_path))
    assert not any('test:next-day' in request for request in requests)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from views').fetchone()[0] == 1
        assert db.execute('select count(*) from days_completed').fetchone()[0] == 0


@pytest.mark.parametrize('change', ['source', 'config'])
def test_changed_source_or_configuration_refuses_before_more_calls(tmp_path, change):
    """D172 manifest row: restarting is not permission to replace the input contract."""
    args = setup_run(tmp_path)
    with pytest.raises(RuntimeError):
        replay.run(**args, transport=v108_send(fail_first=True), day_runner=runner(args, tmp_path))
    if change == 'source':
        with sqlite3.connect(args['testdb_path']) as db:
            db.execute('update items set text=text || ?', (' changed',))
    else:
        args['cfg'] = dataclasses.replace(args['cfg'], version='different-configuration')

    def forbidden(*args):
        raise AssertionError('manifest mismatch reached a model call')
    with pytest.raises(ValueError, match='manifest .* changed'):
        replay.run(**args, transport=forbidden, day_runner=runner(args, tmp_path))


def test_the_shown_questions_takes_lines_and_the_schema_change_the_request_identity(tmp_path, monkeypatch):
    """D172 read set: the request identity covers each shown question's takes line (its research group and aliases) and the allowed
    response schema, not just the question ids."""
    cfg = config.load(ROOT / 'poc/config/poc-v108.json')
    args = setup_run(tmp_path)
    item = dict(CASES[0]['item'], text=CASES[0]['item']['text'])
    shown = [{'view_id': 'v1', 'object_id': 'NVDA', 'kind': 'asset', 'due_day': '2027-01-31', 'question': CASES[0]['candidate']['question'],
              'looks_at': 'Rubin', 'key': {'measure': 'event', 'event_type': 'shipment', 'scope': 'Rubin'}, 'groups': [], 'parents': []}]
    before = extraction_key(cfg, item, item['text'], shown, args['universe'])
    grouped = [dict(shown[0], groups=[{'name': 'Rubin rollout', 'scope': 'production and deployment', 'aliases': ['Rubin']}])]
    after = extraction_key(cfg, item, item['text'], grouped, args['universe'])
    assert before != after
    _, system, user, schema = extraction.request_for(cfg, item, item['text'], grouped, args['universe'])
    schema_for = extraction.schema_for
    monkeypatch.setattr(extraction, 'schema_for', lambda version, *rest: dict(schema_for(version, *rest), description='changed schema only'))
    _, system2, user2, schema2 = extraction.request_for(cfg, item, item['text'], grouped, args['universe'])
    assert (system2, user2) == (system, user) and schema2 != schema
    assert extraction_key(cfg, item, item['text'], grouped, args['universe']) != after


@pytest.mark.parametrize('extra_arguments, parallel', [([], True), (['--workers', '1'], False)])
def test_replay_script_runs_the_parallel_day_by_default_and_serially_with_one_worker(tmp_path, monkeypatch, extra_arguments, parallel):
    """D183 entry point as the user calls it: `scripts/replay.py` with its worker defaults runs the parallel day (16 extraction and 8 Jev
    workers), with `--workers 1` the serial path; both write the serial ledger. Run under the frozen pipeline poc-v108: the default poc-v116 is
    the same plus the coverage-start reading, which needs --seed (test_baseline runs that entry)."""
    import runpy
    serial_dir = tmp_path / 'serial'; serial_dir.mkdir()
    serial = setup_run(serial_dir)
    replay.run(**serial, transport=v108_send())
    args, calls = setup_run(tmp_path), []
    send = v108_send(calls, require_overlap=parallel)
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
                                      '--views', args['views_path'], '--archive', str(tmp_path / 'cli-archive.sqlite'),
                                      '--config', str(ROOT / 'poc/config/poc-v108.json')] + extra_arguments)
    runpy.run_path(str(ROOT / 'scripts/replay.py'), run_name='__main__')
    assert (tmp_path / 'manifests' / 'day-2026-02-25.json').is_file() == parallel
    assert built == ([{'extraction_workers': 16, 'jev_workers': 8}] if parallel else [])
    assert sum(stage == 'extraction' for stage, _, _ in calls) == 2
    assert logical_rows(serial['views_path']) == logical_rows(args['views_path'])


def test_restart_counts_the_days_items_already_written_toward_its_item_limit(tmp_path):
    """D183 restart row: `max_items_per_day` counts the day's items an earlier run already wrote, so a restart selects
    the same items (the parallel day's manifest accepts it) and never dispatches an item beyond the limit."""
    args = setup_run(tmp_path)
    with pytest.raises(RuntimeError, match='judging failed'):
        replay.run(**args, transport=v108_send(fail_judging=True), max_items_per_day=1, day_runner=runner(args, tmp_path))
    replay.run(**args, transport=v108_send(), max_items_per_day=1, day_runner=runner(args, tmp_path))
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select count(*) from processing_steps where input_id=?', (CASES[1]['item']['input_id'],)).fetchone()[0] == 0
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]


def test_fresh_ledger_starts_its_day_over_a_manifest_another_ledger_left(tmp_path):
    """D183 manifest row: a manifest guards a ledger's unfinished day; a fresh ledger in the same folder, with nothing of
    that day written, starts the day under its own configuration instead of refusing it."""
    first_dir = tmp_path / 'first'; first_dir.mkdir()
    first = setup_run(first_dir)
    replay.run(**first, transport=v108_send(), day_runner=ParallelDay(Path(first['testdb_path']), tmp_path / 'manifests',
                                                                       extraction_workers=2, jev_workers=1))
    second = setup_run(tmp_path)
    second['cfg'] = dataclasses.replace(second['cfg'], version='changed-after-the-first-ledger')
    replay.run(**second, transport=v108_send(), day_runner=runner(second, tmp_path))
    with sqlite3.connect(second['views_path']) as db:
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]


def test_ledger_comparison_covers_every_product_table(tmp_path):
    """D182/D183 check: the serial-against-parallel comparison reads every product table; a replacement row, which the
    earlier ten-table comparison did not read, makes two otherwise identical ledgers differ."""
    args = setup_run(tmp_path)
    replay.run(**args, transport=v108_send())
    changed = tmp_path / 'changed.sqlite'
    shutil.copyfile(args['views_path'], changed)
    assert logical_rows(changed) == logical_rows(args['views_path'])
    with sqlite3.connect(changed) as db:
        db.execute("insert into replacements(old_evidence_id,new_evidence_id,said_day,seq) values ('e1','e2','2026-02-25',2)")
    before, after = logical_rows(args['views_path']), logical_rows(changed)
    assert set(after) == set(store.TABLES)
    assert [table for table in after if after[table] != before[table]] == ['replacements']


def test_the_production_pipeline_preserves_sources_groups_and_call_trace(tmp_path):
    """D172 product path: extraction v74i, Jev with the collision judge, grouping, write, daily judgement and close marker."""
    args = setup_run(tmp_path)
    day = ParallelDay(Path(args['testdb_path']), tmp_path / 'manifests', extraction_workers=2, jev_workers=2)
    result = replay.run(**args, transport=v108_send(require_overlap=True), day_runner=day)
    assert (result['new_views'], result['evidence'], result['judged']) == (2, 2, 2)
    with sqlite3.connect(args['views_path']) as db:
        assert db.execute('select name from thesis_groups').fetchall() == [('Rubin rollout',)]      # the second declaration folds into the first (D166)
        assert db.execute('select group_id,view_id from thesis_group_members').fetchall() == [('g1', 'v1'), ('g1', 'v2')]
        assert db.execute('select quote from evidence order by rowid').fetchall() == [(c['evidence']['quote'],) for c in CASES]
        assert db.execute('select day from days_completed').fetchall() == [('2026-02-25',)]
        records = [json.loads(r[0]) for r in db.execute('select shown_json from match_records')]
        requests = [entry for record in records for entry in record.get('requests', [])]
    assert requests
    for entry in requests:
        assert args['archive'].conn.execute('select request_sha256 from model_calls where call_id=?', (entry['call_id'],)).fetchone()[0] == entry['request_sha256']


def test_day_cost_includes_discarded_speculative_calls(tmp_path, monkeypatch):
    """D172 cost reader: stale work is still billed and must remain in the day total."""
    reading_the_questions_open_now(monkeypatch)
    args = setup_run(tmp_path)
    lines = []
    args['log'] = lines.append
    base = v108_send(require_overlap=True)

    def billed(*parameters):
        result = base(*parameters)
        result['usage'] = {'prompt_tokens': 100_000, 'completion_tokens': 0} if len(parameters) == 2 else {}
        return result
    replay.run(**args, transport=billed, day_runner=runner(args, tmp_path))
    cost = args['archive'].totals()[1]
    assert args['archive'].totals()[0] == 5      # two accepted extractions and one stale extraction, one Jev match, one judgement
    assert cost > 0 and f'day ${cost:.2f}' in lines[-1]


def test_audit_binds_each_handover_to_the_request_the_runner_accepted(tmp_path, monkeypatch):
    """D181 review: the proof checks which request each turn accepted, not only that the handover content matches."""
    reading_the_questions_open_now(monkeypatch)
    from concurrency_study.proof import accepted_requests, handover_errors
    args = setup_run(tmp_path)
    day = runner(args, tmp_path)
    replay.run(**args, transport=v108_send(require_overlap=True), day_runner=day)
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
