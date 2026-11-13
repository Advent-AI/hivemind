"""Checks of the adapter's ladder mode (DESIGN.md §5.4, §7.1; D429) on the stored unseeded draw u1 and the fourth Stage A's first-send
ladders. A fake judge answers; no model is called."""
import json
import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / 'e2e-2026-11-09')]
import adapter  # noqa: E402
import budget  # noqa: E402
import ladder_adapter  # noqa: E402
import run_stage_b  # noqa: E402

FIRST_SEND = {json.loads(line)['case']: json.loads(line) for line in ladder_adapter.LADDERS.read_text().splitlines()}
U1 = {name.split('/', 1)[1]: row for name, row in FIRST_SEND.items() if name.startswith('u1/')}
LADDERED = sorted((thesis for thesis, row in U1.items() if row['status'] == 'ladder'), key=lambda name: int(name.split('-')[1]))
UNLADDERED = sorted(thesis for thesis, row in U1.items() if row['status'] != 'ladder')


@pytest.fixture(autouse=True)
def no_credentials(monkeypatch):
    """No test reads a credential (AGENTS §4): a call that escapes its fake transport fails the test instead of reaching a provider."""
    from hivemind import jev, model

    def refuse(*arguments):
        pytest.fail('a test read a credential: a model or Jev call escaped its fake transport')
    monkeypatch.setattr(model, '_key', refuse)
    monkeypatch.setattr(jev, '_key', refuse)


def fake_judge(provider, request):
    shown = adapter.SHOWN_EVIDENCE.findall(request['messages'][-1]['content'])
    answer = {'rung': 1, 'reference': 'as stated', 'implied_outcome': 'the figure implied', 'reasons': 'test', 'cites': shown[:1],
              'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'test', 'theme_pushes': []}
    return {'choices': [{'message': {'content': json.dumps(answer)}}], 'usage': {'prompt_tokens': 1000, 'completion_tokens': 100}}


@pytest.fixture(scope='module')
def replayed(tmp_path_factory):
    from hivemind import jev, model
    saved = (model._key, jev._key)
    def refuse(*arguments):
        pytest.fail('a test read a credential: a model or Jev call escaped its fake transport')
    model._key = jev._key = refuse                    # the module-scoped replay runs outside the function-scoped guard
    try:
        folder = tmp_path_factory.mktemp('u1') / 'out'
        runner = ladder_adapter.replay('u1', folder, transport=fake_judge, cap_usd=5.0)
    finally:
        model._key, jev._key = saved
    return runner, folder, sqlite3.connect(folder / 'views.sqlite')


def test_u1_has_both_kinds_of_thesis():
    """Precondition of the tests below: the stored first send gives u1 laddered theses and theses with no ladder."""
    assert len(U1) == 12 and LADDERED and UNLADDERED


def test_every_laddered_thesis_is_a_view_with_its_stored_ladder_and_there_is_no_other_view(replayed):
    """§5.4: a written ladder is one view v<N> for clean-<N>, carrying the view the ladder step built; no seed and no ruler view."""
    _, _, conn = replayed
    views = {row[0] for row in conn.execute('select view_id from views')}
    assert views == {f"v{thesis.split('-')[1]}" for thesis in LADDERED}
    for thesis in LADDERED:
        stored, view_id = U1[thesis]['view'], f"v{thesis.split('-')[1]}"
        row = conn.execute('select object_id, object_kind, kind, looks_at, question, due_day, year from views where view_id=?', (view_id,)).fetchone()
        assert row == (stored['object_id'], stored['object_kind'], stored['kind'], stored['looks_at'], stored['question'], stored['due_day'], stored['year'])
        rungs = conn.execute('select label, condition, lo, hi from rungs where view_id=? order by position', (view_id,)).fetchall()
        assert rungs == [(r['label'], r['condition'], r.get('lo'), r.get('hi')) for r in stored['rungs']]


def test_every_opened_thesis_has_one_ladder_row_and_a_thesis_with_no_ladder_has_no_view(replayed):
    """§5.4: one clean_ladders row a thesis; a no-ladder row carries the model's reason and no view id."""
    _, _, conn = replayed
    rows = {row[0]: row[1:] for row in conn.execute('select thesis_id, view_id, status, reason from clean_ladders')}
    assert set(rows) == set(U1)
    for thesis in UNLADDERED:
        view_id, status, reason = rows[thesis]
        assert view_id is None and status == ladder_adapter.STATUS[U1[thesis]['status']]
        assert reason == (U1[thesis]['reason'] if status == 'no ladder' else None)
    for thesis in LADDERED:
        assert rows[thesis][:2] == (f"v{thesis.split('-')[1]}", 'ladder')


def test_links_reach_a_laddered_view_and_the_judge_and_links_to_a_thesis_with_no_ladder_are_counted_not_written(replayed):
    """§5.4 Links: a link to clean-<N> with a ladder is written to v<N> and the view is judged; one with no ladder is counted."""
    runner, _, conn = replayed
    linked = {row[0] for row in conn.execute('select distinct view_id from evidence_links')}
    assert linked <= {f"v{thesis.split('-')[1]}" for thesis in LADDERED}
    assert not linked & set(UNLADDERED)
    judged = {entry['view'] for entry in runner.sent}
    assert judged and judged <= linked
    assert runner.counts['links to an unjudged thesis'] > 0
    assert runner.counts['links to other clean-opened theses dropped'] == 0


def test_the_ledger_holds_every_attempt_and_sums_to_the_spend(replayed):
    """D429: each judge attempt's reserve and charge are on disk as they happen; their sum is what the limit counted."""
    runner, folder, _ = replayed
    lines = [json.loads(line) for line in (folder / 'spend.jsonl').read_text().splitlines()]
    reserves = {line['attempt'] for line in lines if 'reserve' in line}
    charges = {line['attempt'] for line in lines if 'charge' in line}
    assert reserves == charges and len(reserves) == len(runner.sent)
    assert ladder_adapter.ledger_total(folder / 'spend.jsonl') == pytest.approx(runner.budget.spent_usd)


def test_the_cap_stops_the_replay(tmp_path):
    """D429: the spending cap refuses the send that would pass it, before it is sent."""
    with pytest.raises(budget.OverBudget):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=0.0001)


def test_an_open_view_due_inside_the_window_stops_the_replay(tmp_path, monkeypatch):
    """§7.1: the due-day guard stops the replay when an open view is due on or before a replay day."""
    early = json.loads(json.dumps(FIRST_SEND))
    early[f'u1/{LADDERED[0]}']['view']['due_day'] = '2026-07-03'
    path = tmp_path / 'outcomes.jsonl'
    path.write_text(''.join(json.dumps(row) + '\n' for row in early.values()))
    monkeypatch.setattr(ladder_adapter, 'LADDERS', path)
    with pytest.raises(SystemExit, match='due 2026-07-03'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)


def test_a_stored_case_that_describes_another_thesis_is_refused(tmp_path, monkeypatch):
    """Identity: the stored ladders are used only for the theses the trace opened, each with the same description."""
    cases = json.loads(ladder_adapter.CASES.read_text())
    next(case for case in cases if case['case'] == f'u1/{LADDERED[0]}')['thesis']['description'] += ' (another thesis)'
    path = tmp_path / 'cases.json'
    path.write_text(json.dumps(cases))
    monkeypatch.setattr(ladder_adapter, 'CASES', path)
    with pytest.raises(SystemExit, match='describe different theses'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)


def test_a_live_replay_writes_only_under_its_output_root(tmp_path):
    """The run folder of a live replay sits under the Stage B data folder."""
    with pytest.raises(SystemExit, match='writes only under'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=None, cap_usd=0.66)


def refusing_judge(provider, request):
    """An answer the frozen judge's check refuses every time: a rung no ladder has."""
    response = fake_judge(provider, request)
    answer = json.loads(response['choices'][0]['message']['content'])
    answer['rung'] = 99
    response['choices'][0]['message']['content'] = json.dumps(answer)
    return response


def test_every_ladder_row_names_the_configuration_that_wrote_it(replayed):
    """§5.4: config_checksum is the ladder configuration's checksum, as the ladder step's own archive records it."""
    _, _, conn = replayed
    assert {row[0] for row in conn.execute('select config_checksum from clean_ladders')} == {ladder_adapter.ladder_configuration()}


def test_a_view_opened_on_its_due_day_is_stopped_before_it_is_judged(tmp_path, monkeypatch):
    """§7.1: the guard runs after the day's writes too, so a view opened already due is never judged."""
    opening = {case['case']: case['item']['publication_date'] for case in json.loads(ladder_adapter.CASES.read_text())}
    due_now = json.loads(json.dumps(FIRST_SEND))
    name = f'u1/{LADDERED[0]}'
    due_now[name]['view']['due_day'] = opening[name]
    path = tmp_path / 'outcomes.jsonl'
    path.write_text(''.join(json.dumps(row) + '\n' for row in due_now.values()))
    monkeypatch.setattr(ladder_adapter, 'LADDERS', path)
    with pytest.raises(SystemExit, match=f'due {opening[name]}'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    view_id = f"v{LADDERED[0].split('-')[1]}"
    conn = sqlite3.connect(tmp_path / 'out' / 'views.sqlite')
    assert conn.execute('select count(*) from judgements where view_id=?', (view_id,)).fetchone()[0] == 0


def test_a_limit_starts_from_its_ledger_so_a_later_process_cannot_pass_the_cap(tmp_path):
    """D429: one cap over every draw and redo; a limit built on an existing ledger counts what it already records."""
    ledger = tmp_path / 'spend.jsonl'
    first = ladder_adapter.LedgerBudget(5.0, ledger, attempt=fake_judge)
    ladder_adapter.replay('u1', tmp_path / 'a', transport=fake_judge, limit=first)
    spent = ladder_adapter.ledger_total(ledger)
    later = ladder_adapter.LedgerBudget(spent + 0.0001, ledger, attempt=fake_judge)
    assert later.spent_usd == pytest.approx(spent)
    with pytest.raises(budget.OverBudget):
        ladder_adapter.replay('u1', tmp_path / 'b', transport=fake_judge, limit=later)


def test_the_launcher_resends_a_draw_stopped_by_a_refused_judgement_once_then_marks_it_incomplete(tmp_path):
    """STAGE_B_RUN.md: a stop a second send can change gets one redo in a new folder; a second stop leaves the draw incomplete."""
    record = run_stage_b.send(tmp_path, transport=refusing_judge, sleep=lambda seconds: None)
    for run in run_stage_b.RUNS:
        assert record[run]['state'] == 'incomplete'
        assert [attempt['folder'] for attempt in record[run]['attempts']] == [f'draw-{run}', f'draw-{run}-redo']
        assert all('JudgementRefused' in attempt['stopped'] for attempt in record[run]['attempts'])


def test_the_launcher_does_not_resend_a_stop_that_code_decides(tmp_path, monkeypatch):
    """STAGE_B_RUN.md: a stop code decides the same way every time (here the due-day guard) is not resent."""
    early = json.loads(json.dumps(FIRST_SEND))
    early[f'u1/{LADDERED[0]}']['view']['due_day'] = '2026-07-03'
    path = tmp_path / 'outcomes.jsonl'
    path.write_text(''.join(json.dumps(row) + '\n' for row in early.values()))
    monkeypatch.setattr(ladder_adapter, 'LADDERS', path)
    record = run_stage_b.send(tmp_path / 'root', transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and [a['folder'] for a in record['u1']['attempts']] == ['draw-u1']
    assert record['u2']['state'] == record['u3']['state'] == 'complete'


def test_the_launcher_stops_every_draw_at_the_cap(tmp_path, monkeypatch):
    """D429: the cap stops the whole send; no later draw starts."""
    monkeypatch.setattr(run_stage_b, 'CAP_USD', 0.0001)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record.get('stopped') == 'the spending cap' and record['u1']['state'] == 'incomplete'
    assert 'u2' not in record and 'u3' not in record


def test_a_second_launch_while_one_runs_sends_nothing(tmp_path):
    """D429: one $2 limit; a second launcher holding no lock never spends against the balance of one that runs."""
    import fcntl
    root = tmp_path / 'root'
    root.mkdir()
    sent = []
    with open(root / 'launch.lock', 'w') as held:
        fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with pytest.raises(run_stage_b.AlreadyRunning):
            run_stage_b.send(root, transport=lambda provider, request: sent.append(1) or fake_judge(provider, request))
    assert sent == [] and not (root / 'draw-u1').exists()


def test_an_attempt_in_flight_when_the_process_died_is_counted_at_its_reserve(tmp_path):
    """D429: a reserve with no charge (a call in flight when the process died) counts in full against the next limit."""
    ledger = tmp_path / 'spend.jsonl'
    ledger.write_text(json.dumps({'attempt': 1, 'reserve': 0.25}) + '\n' + json.dumps({'attempt': 1, 'charge': 0.01, 'known': True}) + '\n'
                      + json.dumps({'attempt': 2, 'reserve': 0.30}) + '\n')
    limit = ladder_adapter.LedgerBudget(2.0, ledger, attempt=fake_judge)
    assert limit.spent_usd == pytest.approx(0.31) and limit.attempts == 2


def test_an_attempt_whose_reserve_cannot_be_written_is_not_sent(tmp_path, monkeypatch):
    """D429: the reserve line is written before the call; if it cannot be written, nothing is sent."""
    sent = []
    limit = ladder_adapter.LedgerBudget(2.0, tmp_path / 'spend.jsonl', attempt=lambda provider, request: sent.append(1) or fake_judge(provider, request))
    def broken(line):
        raise OSError('disk full')
    monkeypatch.setattr(limit, '_write', broken)
    request = {'model': next(iter(budget.model.PRICES)), 'messages': [{'role': 'user', 'content': 'x'}], 'max_completion_tokens': 10}
    with pytest.raises(OSError):
        limit.send('openai', request)
    assert sent == []


def test_each_draw_reports_its_own_spend_and_the_limit_so_far(tmp_path):
    """Readability: under one shared limit, a draw's spend is its own; the cumulative figure is labelled as such."""
    limit = ladder_adapter.LedgerBudget(5.0, tmp_path / 'spend.jsonl', attempt=fake_judge)
    first = ladder_adapter.replay('u1', tmp_path / 'a', transport=fake_judge, limit=limit)
    second = ladder_adapter.replay('u2', tmp_path / 'b', transport=fake_judge, limit=limit)
    total = second.counts['judging usd of the whole limit so far (from its ledger)']
    assert total == pytest.approx(first.counts['judging usd this draw (from tokens)'] + second.counts['judging usd this draw (from tokens)'], abs=2e-4)
    assert second.counts['judging usd this draw (from tokens)'] < total
