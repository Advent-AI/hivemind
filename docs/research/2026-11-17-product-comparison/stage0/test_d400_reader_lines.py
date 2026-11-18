"""Tests of D400's reader lines on the new draws (DESIGN-1.6.md §0 and §1, "Reader lines 1–5"; D452's scaled line 5; D675).

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider docs/research/2026-11-17-product-comparison/stage0/test_d400_reader_lines.py
"""
import json
import subprocess
import sys
import threading
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d400_reader_lines  # noqa: E402
import eligibility  # noqa: E402

FIGURE_RUNGS = [{'label': 'Strongly bullish', 'condition': 'Fiscal 2027 data-centre revenue is above $230 billion.'},
                {'label': 'Bullish', 'condition': 'It is above $210 billion and at most $230 billion.'},
                {'label': 'Neutral', 'condition': 'It is at least $190 billion and at most $210 billion; the reference is $200 billion.'},
                {'label': 'Bearish', 'condition': 'It is at least $170 billion and below $190 billion.'},
                {'label': 'Strongly bearish', 'condition': 'It is below $170 billion.'}]
THESES = {
    'clean-1': ('How much data-centre revenue will NVIDIA report for fiscal 2027?', 'NVIDIA data-centre revenue, fiscal 2027'),
    'clean-2': ('How much will NVIDIA spend on research and development in fiscal 2027?', 'NVIDIA research and development expense, fiscal 2027'),
}


def thesis_case(draw, thesis_id):
    description, outcome = THESES[thesis_id]
    return {'case': f'{draw}/{thesis_id}',
            'thesis': {'id': thesis_id, 'description': description, 'outcome': outcome, 'period': 'NVIDIA fiscal year 2027',
                       'opens_as': 'figure', 'settled_by': "NVIDIA's annual report (Form 10-K) for fiscal 2027"},
            'item': {'publication_date': '2026-07-01', 'publisher': 'Reuters', 'title': 'Analysts raise NVIDIA estimates',
                     'text': 'Analysts expect NVIDIA fiscal 2027 data-centre revenue of about $200 billion and research spending of '
                             'about $20 billion.'}}


def figure_outcome(draw, thesis_id, pass_number):
    _, outcome = THESES[thesis_id]
    return {'case': f'{draw}/{thesis_id}', 'pass': pass_number, 'status': 'ladder', 'reason': None, 'requests': [],
            'passage': 'Analysts expect NVIDIA fiscal 2027 data-centre revenue of about $200 billion',
            'answer': {'ladder': {'reference': {'kind': 'expected', 'value': 200e9, 'value_to': None},
                                  'figure': {'favourable_end': 'higher', 'favourable_why': 'More of it is more profit for the business.'},
                                  'event': None, 'not_judged': [], 'due_day_basis': 'expected_publication'}},
            'view': {'object_id': 'NVDA', 'kind': 'asset', 'looks_at': outcome, 'question': f'What is {outcome} (Form 10-K)?',
                     'year': 2027, 'due_day': '2027-04-01', 'rungs': FIGURE_RUNGS}}


def make_run_root(root, ladder_states):
    """Three new draws. A draw whose ladder is 'completed' holds two company-figure theses over three passes; the others record
    the ladder state given (as run_fresh records a draw that opened no question). Returns the eligibility output fingerprinting them."""
    fingerprints = {}
    for draw, state in ladder_states.items():
        folder = root / draw
        folder.mkdir(parents=True)
        cases_state = 'completed' if state == 'completed' else 'skipped'
        record = {'state': 'complete', 'components': {'cases': {'state': cases_state, 'folder': 'cases'},
                                                      'ladder': {'state': state, 'folder': 'ladder'}}}
        (folder / 'run.json').write_text(json.dumps(record))
        if state == 'completed':
            (folder / 'cases').mkdir()
            (folder / 'cases' / 'cases.json').write_text(json.dumps([thesis_case(draw, thesis_id) for thesis_id in THESES]))
            for pass_number in (1, 2, 3):
                (folder / 'ladder' / f'send-{pass_number}').mkdir(parents=True)
                (folder / 'ladder' / f'send-{pass_number}' / 'outcomes.jsonl').write_text(
                    '\n'.join(json.dumps(figure_outcome(draw, thesis_id, pass_number)) for thesis_id in THESES) + '\n')
        fingerprints[draw] = {'inputs': {relative: eligibility.sha256(folder / relative)
                                         for relative in eligibility.section_inputs(root, draw, record)}}
    return {'eligible': True, 'problems': [], 'draws': fingerprints}


class FakeSessions:
    """Stands in for census_readers.run, the external closed sessions. A reader marks every company figure as holding, except that the
    Codex reader fails Q on clean-1; a third reader rules every point `holds`. The first `voids` calls of a family come back void with
    `void_reason`. A family's first answers take the faults listed in `bad_answers`, one a call: 'short' leaves out the packet's last
    row; 'float item' adds a second row for the first item with its number written 1.0; 'repeated row' gives the first row twice."""

    def __init__(self, voids=None, void_reason='a tool use', bad_answers=None):
        self.voids_left = dict(voids or {})
        self.void_reason = void_reason
        self.bad_answers_left = {family: list(faults) for family, faults in (bad_answers or {}).items()}
        self.calls = []
        self.lock = threading.Lock()

    def __call__(self, family, prompt):
        with self.lock:
            self.calls.append((family, prompt))
            if self.voids_left.get(family, 0) > 0:
                self.voids_left[family] -= 1
                return None, self.void_reason
            fault = self.bad_answers_left.get(family, []).pop(0) if self.bad_answers_left.get(family) else None
        packet = json.loads(prompt.rsplit('## The packet\n\n', 1)[1])
        if 'to_rule' in packet[0]:
            return '\n'.join(json.dumps({'id': point['id'], 'ruling': 'holds', 'why': 'The question names fiscal 2027 and the 10-K.'})
                             for entry in packet for point in entry['to_rule']), None
        rows = []
        for item in packet:
            row = {'item': item['item'], **{mark: 'holds' for mark in ('Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'L', 'XR')},
                   'G': 'not_assessable', 'N': 'n/a', 'B': [], 'W': '', 'why': ''}
            if family == 'codex' and item['thesis']['outcome'] == THESES['clean-1'][1]:
                row.update(Q='fails', why='The question does not say whether it counts networking inside data-centre revenue.')
            rows.append(json.dumps(row))
        if fault == 'short':
            rows = rows[:-1]
        elif fault == 'float item':
            rows.append(json.dumps({**json.loads(rows[0]), 'item': float(packet[0]['item']), 'Q': 'fails', 'why': 'second thoughts'}))
        elif fault == 'repeated row':
            rows.append(rows[0])
        return '\n'.join(rows), None


def test_line_5_is_met_at_the_scaled_minimums():
    """D452: right >= ceil(35N/44) and right by a ladder >= ceil(28N/44); at N = 40 these are the 32 and 26 the full run printed."""
    assert d400_reader_lines.scaled_line_5(35, 28, 44)[0] == 'met'
    verdict, details = d400_reader_lines.scaled_line_5(32, 26, 40)
    assert (verdict, details['minimum right'], details['minimum right by a ladder']) == ('met', 32, 26)


def test_line_5_below_a_scaled_minimum_is_missed():
    """D452: one short of either scaled minimum misses the line."""
    for right, right_by_a_ladder, theses in ((34, 28, 44), (35, 27, 44), (31, 26, 40), (32, 25, 40)):
        assert d400_reader_lines.scaled_line_5(right, right_by_a_ladder, theses)[0] == 'missed'


def test_line_5_with_no_thesis_is_not_measured():
    """D452: N = 0 reads NOT MEASURED (zero minimums would pass vacuously)."""
    assert d400_reader_lines.scaled_line_5(0, 0, 0)[0] == 'NOT MEASURED'


def test_a_file_not_fingerprinted_or_changed_is_refused_before_anything_is_written(tmp_path):
    """DESIGN-1.6.md §0: every file a tool reads is checked against its eligibility fingerprint, and a tool refuses a file whose sha256
    differs."""
    states = {'new-1': 'completed', 'new-2': 'skipped', 'new-3': 'skipped'}
    check = make_run_root(tmp_path / 'unlisted', states)
    del check['draws']['new-1']['inputs']['ladder/send-3/outcomes.jsonl']
    with pytest.raises(SystemExit, match='new-1/ladder/send-3/outcomes.jsonl is not fingerprinted'):
        d400_reader_lines.build_packets(tmp_path / 'unlisted', check, tmp_path / 'out-unlisted', tmp_path / 'keys')
    check = make_run_root(tmp_path / 'changed', states)
    (tmp_path / 'changed' / 'new-1' / 'cases' / 'cases.json').write_text('[]')
    with pytest.raises(SystemExit, match='new-1/cases/cases.json is not fingerprinted by the eligibility check, or changed since'):
        d400_reader_lines.build_packets(tmp_path / 'changed', check, tmp_path / 'out-changed', tmp_path / 'keys')
    assert not (tmp_path / 'out-unlisted').exists() and not (tmp_path / 'out-changed').exists()


def test_a_skipped_ladder_is_not_measured(tmp_path):
    """DESIGN-1.6.md §1: a skipped ladder component (no question opened) is "not measured"; it gets no reading and every line reads NOT
    MEASURED."""
    states = {'new-1': 'skipped', 'new-2': 'skipped', 'new-3': 'skipped'}
    manifest = d400_reader_lines.build_packets(tmp_path / 'run', make_run_root(tmp_path / 'run', states), tmp_path / 'out', tmp_path / 'keys')
    assert manifest['draws']['new-2']['status'] == "not measured: the ladder component is 'skipped'"
    result = d400_reader_lines.report(tmp_path / 'out')
    assert result['draws']['new-2']['line 5'] == 'NOT MEASURED' and not (tmp_path / 'out' / 'new-2').exists()


def test_packets_read_third_report_end_to_end(tmp_path, monkeypatch):
    """DESIGN-1.6.md §1: Stage A's packets, two closed readers a packet (brief and packet inline), two third readers a dispute, Stage A's
    report, and line 5 recomputed from its counts under D452 (N = 2: minimums 2 and 2, met), never the accounting's own 35/28 verdict."""
    sessions = FakeSessions(voids={'claude': 1})
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', sessions)
    states = {'new-1': 'completed', 'new-2': 'skipped', 'new-3': 'skipped'}
    out, keys = tmp_path / 'out', tmp_path / 'keys'
    manifest = d400_reader_lines.build_packets(tmp_path / 'run', make_run_root(tmp_path / 'run', states), out, keys)
    key_path = Path(manifest['draws']['new-1']['key'])
    assert key_path.is_relative_to(keys) and len(json.loads(key_path.read_text())) == 6

    assert [void for _, _, void in d400_reader_lines.read_packets(out)] == [None, None]
    reader_prompts = [prompt for _, prompt in sessions.calls]
    packet_text = (out / 'new-1' / 'readers' / 'packet-1.json').read_text()
    assert all(d400_reader_lines.READER_BRIEF.read_text() in prompt and packet_text in prompt for prompt in reader_prompts)
    assert [family for family, _ in sessions.calls].count('claude') == 2         # the void Claude session was sent again once

    assert [void for _, _, void in d400_reader_lines.read_disputes(out)] == [None, None]
    assert (out / 'new-1' / 'third-reader' / 'rulings-codex-1.jsonl').exists()

    result = d400_reader_lines.report(out)['draws']['new-1']
    stored = json.loads((out / 'new-1' / 'stage-a-report.json').read_text())
    assert stored[d400_reader_lines.TWO_COUNTINGS[0]]['lines']['5'][0] == 'missed'   # the accounting's 35 of 44, not the verdict
    assert result['line 1'] == 'met' and result['line 5'] == 'met'
    assert result['line 5 by counting'][d400_reader_lines.TWO_COUNTINGS[1]] == {
        'verdict': 'met', 'right': 2, 'right by a ladder': 2, 'of': 2, 'minimum right': 2, 'minimum right by a ladder': 2}


def one_draw_with_packets(base):
    """new-1 with its packets built (two company figures over three passes, one packet of six items); new-2 and new-3 skipped."""
    states = {'new-1': 'completed', 'new-2': 'skipped', 'new-3': 'skipped'}
    d400_reader_lines.build_packets(base / 'run', make_run_root(base / 'run', states), base / 'out', base / 'keys')
    return base / 'out'


def all_reader_lines(result):
    return [result[f'line {number}'] for number in (1, 2, 3, 4, 5)]


def voids_logged(out):
    return [(launch['session'], launch['void']) for launch in
            map(json.loads, (out / 'new-1' / 'attempts' / 'launches.jsonl').read_text().splitlines())]


def test_a_session_still_void_after_one_retry_is_reported_missing(tmp_path, monkeypatch):
    """DESIGN-1.6.md, state x event: a reader session that voids (a closed-session breach, or an answer without a valid row for every
    item of its packet) is retried once, then reported missing. Council rounds 8 and 9: a draw with a session missing has every reader
    line 1–5 not measured, none of the collector's results kept (its line 4 would read "no refusal occurred"), and the one-line note that
    no ask-again round follows."""
    sessions = FakeSessions(voids={'claude': 2}, bad_answers={'codex': ['short']})
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', sessions)
    out = one_draw_with_packets(tmp_path)
    results = sorted(d400_reader_lines.read_packets(out))
    assert [void for _, _, void in results] == ['a tool use', None]
    assert [family for family, _ in sessions.calls].count('codex') == 2          # the answer short of a row was asked again
    assert not (out / 'new-1' / 'readers-answers' / 'reader-claude-packet-1.jsonl').exists()
    result = d400_reader_lines.report(out)['draws']['new-1']
    assert all_reader_lines(result) == ['NOT MEASURED'] * 5
    assert result['missing sessions'] == ['reader-claude-packet-1 (reported missing: a tool use)']
    assert result['note'] == d400_reader_lines.NO_ASK_AGAIN


def test_an_exhausted_session_is_not_run_again(tmp_path, monkeypatch):
    """Council round 9: a session reported missing is terminal. Its marker sits beside where its answer would be, and a later `read`
    or `third` sends nothing for it."""
    out = one_draw_with_packets(tmp_path / 'readers')
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', FakeSessions(voids={'claude': 2}))
    d400_reader_lines.read_packets(out)
    marker = out / 'new-1' / 'readers-answers' / 'reader-claude-packet-1.missing'
    assert json.loads(marker.read_text()) == {'void after two attempts': 'a tool use'}
    later = FakeSessions()
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', later)
    assert d400_reader_lines.read_packets(out) == [] and later.calls == []

    out = one_draw_with_packets(tmp_path / 'third-readers')
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', FakeSessions())
    d400_reader_lines.read_packets(out)
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', FakeSessions(voids={'claude': 2}))
    assert [void for _, _, void in sorted(d400_reader_lines.read_disputes(out))] == ['a tool use', None]
    assert (out / 'new-1' / 'third-reader' / 'rulings-claude-1.missing').exists()
    later = FakeSessions()
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', later)
    assert d400_reader_lines.read_disputes(out) == [] and later.calls == []
    result = d400_reader_lines.report(out)['draws']['new-1']
    assert all_reader_lines(result) == ['NOT MEASURED'] * 5 and result['note'] == d400_reader_lines.NO_ASK_AGAIN


def test_an_answer_the_collector_would_read_otherwise_is_void(tmp_path, monkeypatch):
    """Council round 8: a packet answer is validated as `collect_readings.rows_of` reads it. A row whose item the collector would drop
    (written 1.0) and two rows for one item each void the answer, which is then asked again, so nothing accepted is later discarded."""
    sessions = FakeSessions(bad_answers={'codex': ['float item'], 'claude': ['repeated row']})
    monkeypatch.setattr(d400_reader_lines.census_readers, 'run', sessions)
    out = one_draw_with_packets(tmp_path)
    assert [void for _, _, void in sorted(d400_reader_lines.read_packets(out))] == [None, None]
    voids = dict((session, void) for session, void in voids_logged(out) if void)
    assert voids['reader-codex-packet-1'].startswith('1 lines the collector would not read as a row: line 7:')
    assert voids['reader-claude-packet-1'].startswith('more than one row for items')


def test_a_ruling_answer_is_read_as_the_collector_reads_it():
    """Council round 8: a third reader's answer is read line by line as `collect_readings.read_rulings` reads it; a point ruled twice
    and a line it would skip (an `id` that cannot key a ruling) void the answer instead of being dropped or stopping the tool."""
    points = {'4-Q': 'Q', '4-W-a': 'W'}
    good = [json.dumps({'id': '4-Q', 'ruling': 'fails', 'why': 'No fiscal year is named.'}),
            json.dumps({'id': '4-W-a', 'upheld': False, 'why': 'The rungs do name the year.'})]
    assert d400_reader_lines.rulings_problem('\n'.join(good), points) is None
    assert d400_reader_lines.rulings_problem('\n'.join(good + [good[0]]), points) == "more than one ruling for points ['4-Q']"
    unkeyable = json.dumps({'id': ['4-Q'], 'ruling': 'holds'})
    assert d400_reader_lines.rulings_problem('\n'.join(good + [unkeyable]), points).startswith('1 lines the collector would not read')


def test_a_reader_timeout_is_a_void_retried_once_then_reported_missing(tmp_path, monkeypatch):
    """DESIGN-1.6.md, state x event, with the shared launcher's timeout: `census_readers.run` returns a session with no answer within
    3600 s as a void, so it is retried once, then reported missing. Only the command-line process is faked: the Claude one times out,
    the Codex one answers in Codex's event stream."""
    launched = []

    def command_line(command, input, **options):
        family = 'claude' if command[0] == 'claude' else 'codex'
        launched.append(family)
        if family == 'claude':
            raise subprocess.TimeoutExpired(command, options['timeout'])
        answer, _ = FakeSessions()(family, input)
        events = [{'type': 'turn.started'}, {'type': 'item.completed', 'item': {'type': 'agent_message', 'text': answer}}]
        return subprocess.CompletedProcess(command, 0, stdout='\n'.join(map(json.dumps, events)), stderr='')
    monkeypatch.setattr(d400_reader_lines.census_readers, 'subprocess',
                        types.SimpleNamespace(run=command_line, TimeoutExpired=subprocess.TimeoutExpired))
    out = one_draw_with_packets(tmp_path)
    results = sorted(d400_reader_lines.read_packets(out))
    assert [void for _, _, void in results] == ['no answer within 3600 s', None] and launched.count('claude') == 2
    assert [void for session, void in voids_logged(out) if session == 'reader-claude-packet-1'] == ['no answer within 3600 s'] * 2
    result = d400_reader_lines.report(out)['draws']['new-1']
    assert result['missing sessions'] == ['reader-claude-packet-1 (reported missing: no answer within 3600 s)']
    assert all_reader_lines(result) == ['NOT MEASURED'] * 5 and result['note'] == d400_reader_lines.NO_ASK_AGAIN
