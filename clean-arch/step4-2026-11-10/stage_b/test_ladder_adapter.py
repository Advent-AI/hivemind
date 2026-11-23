"""Checks of the adapter's ladder mode (DESIGN.md §5.4, §7.1; D429) on the stored unseeded draw u1 and the fourth Stage A's first-send
ladders. A fake judge answers; no model is called."""
import datetime
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
DRAW_SPEND = 'judging usd this draw (charged: from tokens, or the reserve when no usage came back)'


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
    checked = {row[0]: row[1] for row in conn.execute('select thesis_id, checked_answer from clean_ladders')}
    for thesis in UNLADDERED:
        view_id, status, reason = rows[thesis]
        assert view_id is None and status == ladder_adapter.STATUS[U1[thesis]['status']]
        assert reason == (U1[thesis]['reason'] if status == 'no ladder' else None)
        if status == 'no ladder':
            assert checked[thesis] is not None, f'{thesis} keeps no answer'
            assert json.loads(checked[thesis])['ladder'] is None and json.loads(checked[thesis])['no_ladder'] == U1[thesis]['reason']
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


def test_the_page_can_place_every_judged_view_in_time(replayed):
    """Gate 5's first defect (carried-run/INTEGRATION-CHECK.md): the product's read side places questions in time by the processing
    record and the completed days; a store without them shows an empty library. Every completed article has its step at its own
    sequence and day, every day its end at its last sequence, and the page's own listing shows every view the replay judged."""
    from hivemind import service
    _, folder, conn = replayed
    days_of, _, _ = adapter.trace_articles(ladder_adapter.DRAWS['u1'][0])
    steps = dict(conn.execute('select sequence_no, publication_day from processing_steps'))
    assert {k: days_of[k] for k in days_of} == {k: steps.get(k) for k in days_of}
    ends = dict(conn.execute('select day, seq from days_completed'))
    assert ends == {day: max(k for k in days_of if days_of[k] == day) for day in set(days_of.values())}
    page = sqlite3.connect(folder / 'views.sqlite')
    page.row_factory = sqlite3.Row
    listed = {view['view_id'] for view in service.views(page, include_closed=True)}
    judged = {row[0] for row in page.execute('select distinct view_id from judgements')}
    assert judged and judged <= listed


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


def with_due_day(tmp_path, monkeypatch, due_day, thesis=None):
    """The stored first send with one laddered thesis's due day (the first by default) set to `due_day`; returns its view."""
    thesis = thesis or LADDERED[0]
    rows = json.loads(json.dumps(FIRST_SEND))
    rows[f'u1/{thesis}']['view']['due_day'] = due_day
    path = tmp_path / 'outcomes.jsonl'
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows.values()))
    monkeypatch.setattr(ladder_adapter, 'LADDERS', path)
    return f"v{thesis.split('-')[1]}"


def page_of(folder):
    page = sqlite3.connect(folder / 'views.sqlite')
    page.row_factory = sqlite3.Row
    return page


def test_a_question_due_inside_the_window_closes_at_the_end_of_its_due_day_and_is_never_judged_after(tmp_path, monkeypatch):
    """D566, CLOSING-DESIGN.md §2: production's closing step runs at each day's end; a question due on a day with articles is
    frozen at its last answer on that day, is not judged later, and later links to it are written, not judged, and counted."""
    from hivemind import service
    view_id = with_due_day(tmp_path, monkeypatch, '2026-07-03')
    runner = ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    closing = page.execute("select reason, after_seq from view_switches where view_id=? and open=0", (view_id,)).fetchall()
    assert len(closing) == 1 and closing[0]['reason'].startswith('due 2026-07-03, frozen on 2026-07-03 at rung 1')
    assert service.seq_day_map(page)[closing[0]['after_seq']] == '2026-07-03'
    assert service.is_open_as_of(page, view_id, '2026-07-02') and not service.is_open_as_of(page, view_id, '2026-07-03')
    assert page.execute("select count(*) from judgements where view_id=? and publication_day > '2026-07-03'", (view_id,)).fetchone()[0] == 0
    later = page.execute('select count(*) from evidence_links where view_id=? and seq > ?', (view_id, closing[0]['after_seq'])).fetchone()[0]
    assert later > 0 and runner.counts['links to a closed question written (not judged)'] == later



def test_a_question_opened_already_due_is_judged_and_closed_on_its_opening_day(tmp_path, monkeypatch):
    """D566, CLOSING-DESIGN.md §2: production's order: opened, judged in the day's round, closed at that day's end."""
    opening = {case['case']: case['item']['publication_date'] for case in json.loads(ladder_adapter.CASES.read_text())}
    day = opening[f'u1/{LADDERED[0]}']
    view_id = with_due_day(tmp_path, monkeypatch, day)
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    assert page.execute('select count(*) from judgements where view_id=? and publication_day=?', (view_id, day)).fetchone()[0] >= 1
    reason = page.execute("select reason from view_switches where view_id=? and open=0", (view_id,)).fetchone()['reason']
    assert reason.startswith(f'due {day}, frozen on {day} at rung 1')


def test_every_earlier_day_must_close_its_due_questions(tmp_path, monkeypatch):
    """CLOSING-DESIGN.md §2: the invariant at each day's start refuses a run in which an open question was due before that day."""
    with_due_day(tmp_path, monkeypatch, '2026-07-03')
    monkeypatch.setattr(ladder_adapter.pull, 'end_of_day', lambda conn, day, seq: [])
    with pytest.raises(SystemExit, match='was due 2026-07-03, before 2026-07-04'):
        ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)


def test_a_revision_of_a_statement_linked_to_a_closed_question_is_linked_to_it_not_judged_and_counted(tmp_path, monkeypatch):
    """D566, CLOSING-DESIGN.md §2: as production's writer does, a later account of a statement linked to a closed question is linked
    to it too; the closed question is not judged again; each new link is counted once."""
    view_id = with_due_day(tmp_path, monkeypatch, '2026-07-05', thesis='clean-3')   # e92, linked on 07-05, is revised on 07-06
    runner = ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    after = page.execute("select after_seq from view_switches where view_id=? and open=0", (view_id,)).fetchone()[0]
    revised = page.execute('select count(*) from evidence_links l join revisions r on r.new_evidence_id = l.evidence_id '
                           'join evidence_links o on o.evidence_id = r.old_evidence_id and o.view_id = l.view_id '
                           'where l.view_id = ? and l.seq > ?', (view_id, after)).fetchone()[0]
    later = page.execute('select count(*) from evidence_links where view_id=? and seq > ?', (view_id, after)).fetchone()[0]
    assert revised > 0 and runner.counts['links to a closed question written (not judged)'] == later
    assert page.execute("select count(*) from judgements where view_id=? and publication_day > '2026-07-05'", (view_id,)).fetchone()[0] == 0


def test_a_question_never_judged_by_its_due_day_closes_with_no_data(tmp_path, monkeypatch):
    """D566, pull.py: a question that has no statement, and so no judgement, by its due day closes "no data to verify" (AGENTS §8).
    The fixture drops the opening day's links to the first laddered thesis, so its question opens with no statement."""
    real = adapter.load_draw
    def without_opening_links(trace_path, step2_folder):
        by_article, library = real(trace_path, step2_folder)
        days_of, _, _ = adapter.trace_articles(trace_path)
        for k, records in by_article.items():
            for record in records if days_of.get(k) == '2026-07-01' else []:
                record['thesis_ids'] = [t for t in record['thesis_ids'] if t != LADDERED[0]]
        return by_article, library
    monkeypatch.setattr(adapter, 'load_draw', without_opening_links)
    view_id = with_due_day(tmp_path, monkeypatch, '2026-07-01')
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    assert page.execute('select count(*) from judgements where view_id=?', (view_id,)).fetchone()[0] == 0
    reason = page.execute("select reason from view_switches where view_id=? and open=0", (view_id,)).fetchone()['reason']
    assert reason == 'due 2026-07-01, closed on 2026-07-01 with no judgement: no data to verify'


def test_a_closed_theme_leaves_the_theme_block_and_its_closing_alone_queues_no_judgement(tmp_path, monkeypatch):
    """D566, CLOSING-DESIGN.md §2: production's judging leaves a closed theme out of every later asset request's theme block; a
    closing on a day without articles writes no judgement."""
    themes = [t for t in LADDERED if U1[t]['view']['kind'] == 'theme']
    with_an_empty_day(monkeypatch, empty_day='2026-07-10')
    view_id = with_due_day(tmp_path, monkeypatch, '2026-07-10', thesis=themes[0])
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    assert not ladder_adapter.store.is_open(page, view_id)
    assert page.execute("select count(*) from judgements where publication_day = '2026-07-10'").fetchone()[0] == 0
    archive = sqlite3.connect(tmp_path / 'out' / 'archive.sqlite')
    request_of = lambda sha: json.loads(archive.execute('select request_json from model_calls where request_sha256=?', (sha,)).fetchone()[0])
    texts = {day: [request_of(row['request_sha256'])['messages'][-1]['content'] for row in page.execute(
        "select j.request_sha256 from judgements j join views v on v.view_id = j.view_id where j.publication_day=? and v.object_kind != 'theme'", (day,))]
        for day in ('2026-07-09', '2026-07-11')}
    shown = lambda text: f'- {view_id} (' in text.split('[Themes in force', 1)[1] if '[Themes in force' in text else False
    assert any(shown(text) for text in texts['2026-07-09'])           # in force before it closed
    assert texts['2026-07-11'] and not any(shown(text) for text in texts['2026-07-11'])


def with_an_empty_day(monkeypatch, empty_day='2026-07-04', drop=()):
    """The stored draw with every article from `empty_day` on moved one day later, so `empty_day` has none and the trace numbers
    run on across it; `drop` leaves articles out as Step 1 failures do."""
    real = adapter.trace_articles
    def moved(trace_path):
        days_of, opened, failed = real(trace_path)
        shift = lambda day: (datetime.date.fromisoformat(day) + datetime.timedelta(days=1)).isoformat() if day >= empty_day else day
        return {k: shift(day) for k, day in days_of.items() if k not in drop}, opened, failed
    monkeypatch.setattr(adapter, 'trace_articles', moved)


def test_a_closing_on_a_day_without_articles_is_dated_on_it_and_the_next_article_comes_after_it(tmp_path, monkeypatch):
    """D566, CLOSING-DESIGN.md §1: the loop owns the store's sequence; a closing on a day without articles takes its own sequence
    on that day, the next article takes the one after it and is dated on its own day, and the next day starts with it closed."""
    from hivemind import service
    from hivemind.views import store
    with_an_empty_day(monkeypatch, empty_day='2026-07-10')          # after the last opening (07-09): the stored cases' days hold
    view_id = with_due_day(tmp_path, monkeypatch, '2026-07-10')
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    page = page_of(tmp_path / 'out')
    sequences = {int(k): s for k, s in json.loads((tmp_path / 'out' / 'sequences.json').read_text()).items()}
    days_of, _, _ = adapter.trace_articles(ladder_adapter.DRAWS['u1'][0])
    last_before = max(k for k, day in days_of.items() if day < '2026-07-10')
    closing_seq = page.execute("select after_seq from view_switches where view_id=? and open=0", (view_id,)).fetchone()[0]
    assert closing_seq == last_before + 1 and service.seq_day_map(page)[closing_seq] == '2026-07-10'
    assert all(sequences[k] == k for k in sequences if k <= last_before)
    assert all(sequences[k] == k + 1 for k in sequences if k > last_before)
    assert service.seq_day_map(page)[sequences[last_before + 1]] == '2026-07-11'
    assert view_id not in [v['view_id'] for v in store.views_open_at_day_start(page, ['NVDA'], '2026-07-11')]
    assert dict(page.execute('select day, seq from days_completed'))['2026-07-10'] == closing_seq


def test_a_gap_in_the_trace_numbers_is_kept_when_nothing_closes(tmp_path, monkeypatch):
    """CLOSING-DESIGN.md §1: an article's store sequence is its trace number, gaps included, unless a closing took that number."""
    with_an_empty_day(monkeypatch, empty_day='2026-08-01', drop=(50,))
    ladder_adapter.replay('u1', tmp_path / 'out', transport=fake_judge, cap_usd=5.0)
    sequences = {int(k): s for k, s in json.loads((tmp_path / 'out' / 'sequences.json').read_text()).items()}
    assert 50 not in sequences and all(sequences[k] == k for k in sequences)


def another_thesis(tmp_path, monkeypatch):
    """The stored cases with the first laddered thesis described as another thesis: a stop code decides (the identity check)."""
    cases = json.loads(ladder_adapter.CASES.read_text())
    next(case for case in cases if case['case'] == f'u1/{LADDERED[0]}')['thesis']['description'] += ' (another thesis)'
    path = tmp_path / 'cases.json'
    path.write_text(json.dumps(cases))
    monkeypatch.setattr(ladder_adapter, 'CASES', path)


def test_a_stored_case_that_describes_another_thesis_is_refused(tmp_path, monkeypatch):
    """Identity: the stored ladders are used only for the theses the trace opened, each with the same description."""
    another_thesis(tmp_path, monkeypatch)
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
    """STAGE_B_RUN.md: a stop a second send can change gets one redo in a new folder; a second stop leaves the draw incomplete,
    which ends the send: no later draw starts."""
    record = run_stage_b.send(tmp_path, transport=refusing_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete'
    assert [attempt['folder'] for attempt in record['u1']['attempts']] == ['draw-u1', 'draw-u1-redo']
    assert all('JudgementRefused' in attempt['stopped'] for attempt in record['u1']['attempts'])
    assert record['stopped'].startswith('u1 incomplete') and 'u2' not in record and not (tmp_path / 'draw-u2').exists()


def test_the_launcher_does_not_resend_a_stop_that_code_decides(tmp_path, monkeypatch):
    """STAGE_B_RUN.md: a stop code decides the same way every time (here the identity check of the stored cases) is not resent."""
    another_thesis(tmp_path, monkeypatch)
    record = run_stage_b.send(tmp_path / 'root', transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and [a['folder'] for a in record['u1']['attempts']] == ['draw-u1']
    assert 'u2' not in record and record['stopped'].startswith('u1 incomplete')


def test_the_launcher_stops_every_draw_at_the_cap(tmp_path, monkeypatch):
    """D429: the cap stops the whole send; no later draw starts."""
    monkeypatch.setattr(run_stage_b, 'CAP_USD', 0.0001)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record.get('stopped', '').startswith('the spending cap') and record['u1']['state'] == 'incomplete'
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
    assert total == pytest.approx(first.counts[DRAW_SPEND] + second.counts[DRAW_SPEND], abs=2e-4)
    assert second.counts[DRAW_SPEND] < total


def test_a_later_launch_after_the_cap_stop_sends_nothing(tmp_path, monkeypatch):
    """STAGE_B_RUN.md: the cap ends the whole send; a later launch that finds the stop recorded sends nothing."""
    monkeypatch.setattr(run_stage_b, 'CAP_USD', 0.0001)
    run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    monkeypatch.setattr(run_stage_b, 'CAP_USD', 2.0)
    sent = []
    with pytest.raises(run_stage_b.Stopped):
        run_stage_b.send(tmp_path, transport=lambda provider, request: sent.append(1) or fake_judge(provider, request), sleep=lambda seconds: None)
    assert sent == [] and not (tmp_path / 'draw-u2').exists()


def test_a_draw_with_no_judgement_is_incomplete(tmp_path, monkeypatch):
    """Design §8: a draw with no judgement is incomplete, though its replay returned."""
    def no_judgements(run, folder, **keywords):
        Path(folder).mkdir(parents=True)
        class Runner:
            counts = {'judgements': 0, 'views written from a ladder': 9}
        return Runner()
    monkeypatch.setattr(run_stage_b.ladder_adapter, 'replay', no_judgements)
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and record['stopped'] == 'u1 incomplete: no judgement' and 'u2' not in record


def test_a_folder_left_by_a_crash_is_recorded_and_never_resumed(tmp_path):
    """STAGE_B_RUN.md: a draw folder with no recorded outcome is a crash: recorded as such, not resumed; the redo runs once."""
    (tmp_path / 'draw-u1').mkdir()
    (tmp_path / 'draw-u1' / 'views.sqlite').write_text('')        # what a dead process left
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    attempts = record['u1']['attempts']
    assert attempts[0] == {'folder': 'draw-u1', 'stopped': 'the process ended without recording an outcome (a crash)'}
    assert attempts[1]['folder'] == 'draw-u1-redo' and record['u1']['state'] == 'complete'
    assert (tmp_path / 'draw-u1' / 'views.sqlite').read_text() == ''


def test_a_crash_of_the_redo_leaves_the_draw_incomplete(tmp_path):
    """STAGE_B_RUN.md: one redo only; a redo folder with no recorded outcome leaves the draw incomplete."""
    for name in ('draw-u1', 'draw-u1-redo'):
        (tmp_path / name).mkdir()
    record = run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)
    assert record['u1']['state'] == 'incomplete' and len(record['u1']['attempts']) == 2
    assert 'u2' not in record and record['stopped'].startswith('u1 incomplete')


def test_a_cap_refusal_stops_every_later_send_at_once(tmp_path):
    """One stop rule: once the cap refuses a request, no other request is sent, however small; the stop is in the ledger."""
    sent = []
    limit = ladder_adapter.LedgerBudget(0.001, tmp_path / 'spend.jsonl', attempt=lambda provider, request: sent.append(1) or fake_judge(provider, request))
    model_name = next(iter(budget.model.PRICES))
    large = {'model': model_name, 'messages': [{'role': 'user', 'content': 'x' * 200000}], 'max_completion_tokens': 10}
    small = {'model': model_name, 'messages': [{'role': 'user', 'content': 'x'}], 'max_completion_tokens': 1}
    with pytest.raises(budget.OverBudget):
        limit.send('openai', large)
    with pytest.raises(budget.OverBudget, match='stopped'):
        limit.send('openai', small)
    assert sent == [] and (ladder_adapter.ledger_stop(tmp_path / 'spend.jsonl') or '').startswith('the spending cap')


def test_a_stop_in_the_ledger_survives_a_crash_and_a_later_launch_sends_nothing(tmp_path):
    """One stop rule: a stop written before a crash makes a limit built later start stopped, and the launcher sends nothing."""
    (tmp_path / 'spend.jsonl').write_text(json.dumps({'stop': 'the spending cap: test'}) + '\n')
    assert ladder_adapter.LedgerBudget(2.0, tmp_path / 'spend.jsonl').stopped == 'the spending cap: test'
    sent = []
    with pytest.raises(run_stage_b.Stopped):
        run_stage_b.send(tmp_path, transport=lambda provider, request: sent.append(1) or fake_judge(provider, request), sleep=lambda seconds: None)
    assert sent == [] and not (tmp_path / 'draw-u1').exists()


def test_an_incomplete_draw_is_written_to_the_ledger_and_ends_later_launches(tmp_path, monkeypatch):
    """One stop rule: a draw ending incomplete records the stop in the ledger; a later launch sends nothing."""
    run_stage_b.send(tmp_path, transport=refusing_judge, sleep=lambda seconds: None)
    assert (ladder_adapter.ledger_stop(tmp_path / 'spend.jsonl') or '').startswith('u1 incomplete')
    with pytest.raises(run_stage_b.Stopped):
        run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None)


def test_a_crash_right_after_a_terminal_stop_cannot_lead_to_a_redo(tmp_path, monkeypatch):
    """One stop rule: the stop reaches the ledger before the attempt reaches run.json, so a process that dies between the two
    leaves a stop a later launch obeys; it never starts the redo of a draw that ended."""
    another_thesis(tmp_path, monkeypatch)
    root = tmp_path / 'root'
    real_write = Path.write_text
    def dying_write(self, text, *arguments, **keywords):
        if self.name == 'run.json' and 'SystemExit' in text:
            raise KeyboardInterrupt('the process dies writing the attempt')
        return real_write(self, text, *arguments, **keywords)
    monkeypatch.setattr(Path, 'write_text', dying_write)
    with pytest.raises(KeyboardInterrupt):
        run_stage_b.send(root, transport=fake_judge, sleep=lambda seconds: None)
    monkeypatch.setattr(Path, 'write_text', real_write)
    with pytest.raises(run_stage_b.Stopped):
        run_stage_b.send(root, transport=fake_judge, sleep=lambda seconds: None)
    assert not (root / 'draw-u1-redo').exists()


def test_the_launcher_hands_each_draw_its_end_day_and_none_by_default(tmp_path, monkeypatch):
    """Release comparison, plan §1.5 E (D667): an `end_day` in a draw's inputs reaches the day-by-day replay; a draw without one replays
    to its last article as before."""
    seen = {}

    def recording(run, folder, **keywords):
        seen[run] = keywords.get('end_day')
        Path(folder).mkdir(parents=True)
        class Runner:
            counts = {'judgements': 1, 'views written from a ladder': 1}
        return Runner()
    monkeypatch.setattr(run_stage_b.ladder_adapter, 'replay', recording)
    run_stage_b.send(tmp_path, transport=fake_judge, sleep=lambda seconds: None, runs=('u1', 'u2'),
                     inputs_of={'u1': {'end_day': '2026-09-20'}})
    assert seen == {'u1': '2026-09-20', 'u2': None}
