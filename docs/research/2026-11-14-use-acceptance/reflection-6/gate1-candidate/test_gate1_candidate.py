"""The gate-1 handoff at $0 (council round 36): the byte check of both configurations, the refusals without Alex's authorization,
and a dry run through Stage A's real runner on cases outside the 44 with a fake transport (never the 44: D426)."""
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'astra-a2'), str(HERE.parent / 'astra'), str(HERE.parent / 'due-day')]
import gate1_candidate as gate  # noqa: E402
import refcontrol  # noqa: E402


@pytest.mark.parametrize('config', gate.CONFIGS)
def test_each_configuration_is_the_frozen_request_with_only_its_model_and_recorded_edits(config):
    assert gate.check(config)['sends'] == 132


def test_an_unrecorded_change_is_refused(monkeypatch):
    real = gate.texts_for
    monkeypatch.setattr(gate, 'texts_for', lambda config: dict(real(config), closing=real(config)['closing'] + ' Be brief.'))
    with pytest.raises(SystemExit, match='CHECK FAILED'):
        gate.check('astra-a2-v2')


def test_no_launch_without_alex_s_authorization(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, 'AUTHORIZATION', tmp_path / 'authorization.json')
    with pytest.raises(SystemExit, match='NOT AUTHORIZED: Stage A on the 44 is Alex'):
        gate.launch('astra-frozen', tmp_path / 'run')
    (tmp_path / 'authorization.json').write_text(json.dumps({'config': 'astra-a2-v2', 'cap_usd': 10, 'by': 'Alex'}))
    with pytest.raises(SystemExit, match="NOT AUTHORIZED: authorization.json does not name 'astra-frozen'"):
        gate.launch('astra-frozen', tmp_path / 'run')
    assert not (tmp_path / 'run').exists()


@pytest.mark.parametrize('config', gate.CONFIGS)
def test_a_dry_run_on_outside_cases_sends_every_case_three_times_with_the_chosen_request(config, tmp_path, monkeypatch):
    population = refcontrol.population()[:4]                      # outside the 44, never the 44 themselves
    cases = [dict(case, case=f'{source}:{name}') for source, name, case, _ in population]
    (tmp_path / 'cases.json').write_text(json.dumps(cases))
    monkeypatch.setattr(gate, 'CASES', tmp_path / 'cases.json')
    monkeypatch.setattr(gate, 'AUTHORIZATION', tmp_path / 'authorization.json')
    (tmp_path / 'authorization.json').write_text(json.dumps({'config': config, 'cap_usd': 10, 'by': 'Alex'}))
    stored = {case['thesis']['description']: row['requests'][-1]['answer_text'] for _, _, case, row in population}
    seen = []

    def fake(provider, request):
        seen.append((request['model'], request['messages'][0]['content']))
        user = request['messages'][1]['content']
        text = next(answer for description, answer in stored.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        return {'choices': [{'message': {'content': text}}], 'usage': {'prompt_tokens': 2000, 'completion_tokens': 400}}
    written, limit, jobs = gate.launch(config, tmp_path / 'run', transport=fake)
    assert jobs == 12 and len(written) == 12 and not limit.stopped
    assert {model for model, _ in seen} == {'gpt-6-astra'}
    assert all((gate.dueday_probe.V2_CLAUSE in system) == (config == 'astra-a2-v2') for _, system in seen)
    assert gate.stage_a.SETTING.model == 'gpt-6-luna'             # the module's setting is restored after the run


def test_a_run_that_stops_reads_not_measured(tmp_path, monkeypatch):
    population = refcontrol.population()[:2]
    (tmp_path / 'cases.json').write_text(json.dumps([dict(case, case=f'{s}:{n}') for s, n, case, _ in population]))
    monkeypatch.setattr(gate, 'CASES', tmp_path / 'cases.json')
    monkeypatch.setattr(gate, 'AUTHORIZATION', tmp_path / 'authorization.json')
    (tmp_path / 'authorization.json').write_text(json.dumps({'config': 'astra-frozen', 'cap_usd': 10, 'by': 'Alex'}))

    def refusing(provider, request):
        error = gate.model.TransportError('400 Bad Request: unsupported parameter')
        error.http_status = 400
        raise error
    with pytest.raises(SystemExit, match='STOPPED: .* NOT MEASURED'):
        gate.launch('astra-frozen', tmp_path / 'run', transport=refusing)


def test_the_preflight_refuses_when_it_finds_no_stored_attempt(tmp_path, monkeypatch):
    monkeypatch.setattr(gate, 'STORED_RUN', tmp_path / 'nothing-here')
    with pytest.raises(SystemExit, match='PREFLIGHT REFUSED: no stored attempt found'):
        gate.preflight()


def test_the_preflight_refuses_when_a_stored_verdict_differs(tmp_path, monkeypatch):
    import shutil
    run = tmp_path / 'run-4'
    shutil.copytree(gate.STORED_RUN, run, ignore=shutil.ignore_patterns('*.sqlite', 'code-as-sent'))
    path = sorted(run.glob('send-*/outcomes.jsonl'))[0]
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    rows[0]['requests'][0]['result'] = 'refused' if rows[0]['requests'][0].get('result') != 'refused' else 'ladder'
    path.write_text(''.join(json.dumps(row) + '\n' for row in rows))
    monkeypatch.setattr(gate, 'STORED_RUN', run)
    with pytest.raises(SystemExit, match='PREFLIGHT REFUSED: 1 stored verdicts differ'):
        gate.preflight()
