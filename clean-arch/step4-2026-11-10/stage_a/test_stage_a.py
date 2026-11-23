"""Tests of Stage A's runner and spending limit (DESIGN.md §8: the cap, one stop for all workers, the spend on disk, a case and
its files, three sends as three samples). Real archive, real limit arithmetic, real ladder step; only the transport is faked.

Run: python3 -m pytest clean-arch/step4-2026-11-10/stage_a/test_stage_a.py
"""
import json
import sys
import threading
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(HERE), str(STEP / 'ladder'), str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402
import stage_a  # noqa: E402
from hivemind import universe  # noqa: E402

RESEARCH_LIST = universe.load(str(ROOT / 'poc' / 'universe.json'))
CASES = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
EXAMPLES = {tuple(entry['thesis']): entry for entry in json.loads((STEP / 'ladder' / 'examples.json').read_text())[1:]}
ANSWERS = {'clean-3': json.dumps(EXAMPLES[('u1', 'clean-3')]['answer']), 'clean-7': json.dumps(EXAMPLES[('u1', 'clean-7')]['answer'])}
TEXTS = stage_a.request_texts()
USAGE = {'prompt_tokens': 1000, 'completion_tokens': 200}
ONE_CALL_USD = (1000 * 0.10 + 200 * 0.50) / 1e6


def thesis_id_of(request):
    return json.loads(request['messages'][1]['content'].rsplit('\n\n', 1)[0])['thesis']['id']


def answering_transport(calls):
    """A fake transport that answers each request with the fixture answer of its thesis and records the call."""
    def transport(provider, request):
        calls.append(thesis_id_of(request))
        return {'choices': [{'message': {'content': ANSWERS[thesis_id_of(request)]}}], 'usage': USAGE}
    return transport


def a_request():
    return stage_a.model.build_request(stage_a.SETTING, 'system', 'user', TEXTS['schema'], 'clean_ladder', 'openai')


def ledger_lines(folder):
    return [json.loads(line) for line in (Path(folder) / 'spend.jsonl').read_text().splitlines()]


def test_three_sends_are_three_samples_each_pass_in_its_own_archive(tmp_path):
    """An identical request is sent again in each pass and never answered from a stored answer."""
    calls = []
    written, limit, job_count = stage_a.run([CASES['u1/clean-3'], CASES['u1/clean-7']], [1, 2, 3], tmp_path / 'run', 1.00,
                                             research_list=RESEARCH_LIST, texts=TEXTS, transport=answering_transport(calls))
    assert len(calls) == 6 == job_count == len(written) and not limit.stopped
    for pass_number in (1, 2, 3):
        rows = [json.loads(line) for line in (tmp_path / 'run' / f'send-{pass_number}' / 'outcomes.jsonl').read_text().splitlines()]
        assert sorted(row['case'] for row in rows) == ['u1/clean-3', 'u1/clean-7'] and all(row['pass'] == pass_number for row in rows)
        assert all(row['status'] == 'ladder' and row['view']['rungs'] for row in rows)
        assert (tmp_path / 'run' / f'send-{pass_number}' / 'archive.sqlite').exists()


def test_two_cases_with_one_thesis_id_from_two_draws_give_two_outcomes(tmp_path):
    """A case is the pair of draw and thesis id; `clean-3` exists in more than one draw."""
    same_id_other_draw = {**CASES['u1/clean-3'], 'case': 'u2/clean-3'}
    written, _, _ = stage_a.run([CASES['u1/clean-3'], same_id_other_draw], [1], tmp_path / 'run', 1.00, research_list=RESEARCH_LIST,
                                texts=TEXTS, transport=answering_transport([]))
    assert sorted(case for case, _, _ in written) == ['u1/clean-3', 'u2/clean-3']


def test_a_second_start_on_an_existing_folder_is_refused(tmp_path):
    """A stop is not restarted: the folder is created once."""
    stage_a.run([CASES['u1/clean-3']], [1], tmp_path / 'run', 1.00, research_list=RESEARCH_LIST, texts=TEXTS, transport=answering_transport([]))
    with pytest.raises(FileExistsError):
        stage_a.run([CASES['u1/clean-3']], [1], tmp_path / 'run', 1.00, research_list=RESEARCH_LIST, texts=TEXTS, transport=answering_transport([]))


def test_the_spend_on_disk_is_two_whole_lines_an_attempt_and_equals_the_limits_spend(tmp_path):
    calls = []
    _, limit, _ = stage_a.run([CASES['u1/clean-3'], CASES['u1/clean-7']], [1, 2], tmp_path / 'run', 1.00, research_list=RESEARCH_LIST,
                              texts=TEXTS, transport=answering_transport(calls), workers=4)
    lines = ledger_lines(tmp_path / 'run')
    assert len(lines) == 8 and sum('reserve' in line for line in lines) == 4 and sum('charge' in line for line in lines) == 4
    assert len({line['attempt'] for line in lines}) == 4 and 'u1/clean-3|2|1|1' in {line['attempt'] for line in lines}
    known, in_full, dropped = stage_a.ledger_total(tmp_path / 'run' / 'spend.jsonl')
    assert known == pytest.approx(4 * ONE_CALL_USD) == pytest.approx(limit.spent_usd) and in_full == 0 and not dropped


def test_a_reserve_with_no_charge_is_counted_in_full_and_reported_apart(tmp_path):
    ledger = tmp_path / 'spend.jsonl'
    ledger.write_text(json.dumps({'attempt': 'a|1|1|1', 'reserve': 0.01}) + '\n' + json.dumps({'attempt': 'a|1|1|1', 'charge': 0.002, 'known': True}) + '\n'
                      + json.dumps({'attempt': 'b|1|1|1', 'reserve': 0.01}) + '\n'
                      + json.dumps({'attempt': 'c|1|1|1', 'reserve': 0.01}) + '\n' + json.dumps({'attempt': 'c|1|1|1', 'charge': 0.01, 'known': False}) + '\n')
    known, in_full, dropped = stage_a.ledger_total(ledger)
    assert known == pytest.approx(0.002) and in_full == pytest.approx(0.02) and not dropped


def test_a_last_ledger_line_that_is_not_whole_is_dropped_and_reported(tmp_path):
    ledger = tmp_path / 'spend.jsonl'
    ledger.write_text(json.dumps({'attempt': 'a|1|1|1', 'reserve': 0.01}) + '\n' + '{"attempt": "b|1|1|1", "rese')
    known, in_full, dropped = stage_a.ledger_total(ledger)
    assert known == 0 and in_full == pytest.approx(0.01) and dropped


def test_no_send_begins_after_the_stop_flag_is_set(tmp_path):
    calls = []
    limit = stage_a.StageALimit(1.00, tmp_path / 'spend.jsonl', attempt=answering_transport(calls))
    limit.stop('a reason')
    with pytest.raises(stage_a.Stopped):
        limit.send_labelled('u1/clean-3|1|1', 'openai', a_request())
    assert calls == [] and not (tmp_path / 'spend.jsonl').exists()


def test_a_send_already_begun_finishes_and_is_charged_and_none_begins_after_the_cap_refuses_another(tmp_path):
    """One worker is held inside its send while another is refused by the cap; the first is then released."""
    inside, release, calls = threading.Event(), threading.Event(), []

    def held_transport(provider, request):
        calls.append('sent')
        inside.set()
        release.wait(timeout=10)
        return {'choices': [{'message': {'content': '{}'}}], 'usage': USAGE}

    reserve = budget.worst_cost(a_request())
    limit = stage_a.StageALimit(reserve * 1.5, tmp_path / 'spend.jsonl', attempt=held_transport)        # room for one reserve, not two
    results = {}
    first = threading.Thread(target=lambda: results.update(first=limit.send_labelled('a|1|1', 'openai', a_request())))
    first.start()
    assert inside.wait(timeout=10)
    with pytest.raises(budget.OverBudget):
        limit.send_labelled('b|1|1', 'openai', a_request())
    assert limit.stopped and limit.stop_reason == 'the spending cap'
    release.set()
    first.join(timeout=10)
    assert 'first' in results and limit.spent_usd == pytest.approx(ONE_CALL_USD) and limit.reserved_usd == pytest.approx(0)
    with pytest.raises(stage_a.Stopped):
        limit.send_labelled('c|1|1', 'openai', a_request())
    assert calls == ['sent']
    assert [('reserve' in line, line['attempt']) for line in ledger_lines(tmp_path)] == [(True, 'a|1|1|1'), (False, 'a|1|1|1')]


def test_the_cap_stops_the_run_and_the_sends_without_an_outcome_are_counted(tmp_path):
    """Each answer is charged 1.3 cents from its tokens; under a cap of 3 cents the third send would pass it and is refused."""
    calls = []

    def costly_transport(provider, request):
        calls.append(thesis_id_of(request))
        return {'choices': [{'message': {'content': ANSWERS[thesis_id_of(request)]}}], 'usage': {'prompt_tokens': 50000, 'completion_tokens': 16000}}

    written, limit, job_count = stage_a.run([CASES['u1/clean-3'], CASES['u1/clean-7']], [1, 2, 3], tmp_path / 'run', 0.03,
                                             research_list=RESEARCH_LIST, texts=TEXTS, transport=costly_transport, workers=1)
    assert limit.stopped and limit.stop_reason == 'the spending cap'
    assert len(calls) == 2 == len(written) and job_count == 6                           # four sends have no outcome
    assert limit.spent_usd == pytest.approx(2 * (50000 * 0.10 + 16000 * 0.50) / 1e6) and limit.spent_usd <= 0.03
    known, in_full, _ = stage_a.ledger_total(tmp_path / 'run' / 'spend.jsonl')
    assert known == pytest.approx(limit.spent_usd) and in_full == 0                    # the refused send reserved nothing


def test_an_error_that_is_not_an_answers_own_stops_every_worker(tmp_path):
    calls = []

    def failing_transport(provider, request):
        calls.append(thesis_id_of(request))
        raise RuntimeError('the disk is full')

    written, limit, job_count = stage_a.run([CASES['u1/clean-3'], CASES['u1/clean-7']], [1, 2], tmp_path / 'run', 1.00,
                                             research_list=RESEARCH_LIST, texts=TEXTS, transport=failing_transport, workers=1)
    assert written == [] and limit.stopped and 'RuntimeError: the disk is full' in limit.stop_reason and len(calls) == 1 and job_count == 4


def test_an_outcome_that_cannot_be_written_stops_every_worker(tmp_path, monkeypatch):
    """One stop for all workers covers the writing of an outcome, not only the model call."""
    calls = []

    def unwritable(row):
        raise OSError('no space left on device')

    monkeypatch.setattr(stage_a.ladder_step, 'as_json', unwritable)
    written, limit, job_count = stage_a.run([CASES['u1/clean-3'], CASES['u1/clean-7']], [1, 2], tmp_path / 'run', 1.00,
                                             research_list=RESEARCH_LIST, texts=TEXTS, transport=answering_transport(calls), workers=1)
    assert written == [] and limit.stopped and 'OSError: no space left on device' in limit.stop_reason and len(calls) == 1 and job_count == 4

