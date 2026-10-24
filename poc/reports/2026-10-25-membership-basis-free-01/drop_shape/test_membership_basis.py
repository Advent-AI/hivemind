"""D150: source-preserving projection, original checks and the default experiment entry point."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

import ingestion_groups as base
import membership_basis as experiment
import retained_membership as retained
import study

SOURCE = study.ROOT / 'poc/reports/2026-10-25-direct-subjects-01'
CONTEXT = study.ROOT / 'poc/reports/2026-10-25-grouping-consistency-01'


def wire_fixture(raw):
    """Synthetic explanations test only representation; they are not semantic model samples."""
    result = copy.deepcopy(raw)
    for candidate in result['candidates']:
        candidate['memberships'] = [
            {'basis': 'Projection test placeholder; not a semantic judgement.', 'thread_id': ident}
            for ident in candidate.pop('thread_ids')]
    return result


def test_d150_all_stored_answers_project_without_altering_any_value():
    """Value/reader row: all 18 saved answers retain every original field, value and order."""
    paths = sorted(SOURCE.glob('sample-*-retained/item*-extract.json'))
    paths += sorted(CONTEXT.glob('sample-*/item3-extract.json'))
    assert len(paths) == 18
    for path in paths:
        record = json.loads(path.read_text())
        offered = json.loads(record['request']['messages'][1]['content'])['existing_subjects']
        wire = wire_fixture(record['answer'])
        before = copy.deepcopy(wire)
        assert experiment.project(wire, offered) == record['answer'], path
        assert wire == before


@pytest.mark.parametrize('breach', ['empty_basis', 'extra_field', 'old_field', 'unknown', 'duplicate', 'empty'])
def test_d150_projection_cannot_hide_invalid_input(breach):
    """New path/old checks: reject malformed new output and keep all old ID constraints."""
    record = json.loads((SOURCE / 'sample-2-retained/item3-extract.json').read_text())
    offered = json.loads(record['request']['messages'][1]['content'])['existing_subjects']
    raw = wire_fixture(record['answer'])
    candidate = raw['candidates'][0]
    if breach == 'empty_basis':
        candidate['memberships'][0]['basis'] = '  '
    elif breach == 'extra_field':
        candidate['memberships'][0]['extra'] = 'must be rejected before projection'
    elif breach == 'old_field':
        candidate['thread_ids'] = ['g1']
    elif breach == 'unknown':
        candidate['memberships'][0]['thread_id'] = 'g999'
    elif breach == 'duplicate':
        candidate['memberships'].append(copy.deepcopy(candidate['memberships'][0]))
    else:
        candidate['memberships'] = []
    with pytest.raises(ValueError):
        experiment.project(raw, offered)


@pytest.mark.parametrize('budget', [
    {'attempts': [{}] * 24, 'estimated_spent': 0},
    {'attempts': [], 'estimated_spent': 1},
])
def test_d150_bounds_refuse_before_external_service(tmp_path, monkeypatch, budget):
    """Budget row: both bounds stop the call before reaching the external model."""
    out = tmp_path / 'experiment'
    experiment.prepare(out, SOURCE)
    study.write_json(out / 'budget.json', budget)
    calls = experiment.Calls(out, 'dev-1-control', SOURCE / 'sample-2-retained')
    def external_service(*args, **kwargs):
        raise AssertionError('External service was reached')
    monkeypatch.setattr(study.model, 'call', external_service)
    try:
        with pytest.raises(experiment.BudgetReached):
            calls.stage('item3-extract', 'Test prompt', {}, study.obj({}), calls.cfg.matching)
        assert json.loads((out / 'budget.json').read_text()) == budget
    finally:
        calls.archive.conn.close()


def test_d150_default_cli_replays_real_requests_and_writes_same_members(tmp_path):
    """State/entry-point rows: six isolated streams, original checks, history and resend at zero calls."""
    out = tmp_path / 'experiment'
    experiment.prepare(out, SOURCE)
    original = CONTEXT / 'sample-3-control'
    for label in experiment.LABELS:
        folder = out / f'sample-dev-{label}'
        for stage in ('extract', 'match'):
            record = json.loads((original / f'item3-{stage}.json').read_text())
            if label.endswith('-basis') and stage == 'extract':
                payload = json.loads(record['request']['messages'][1]['content'])
                record['request']['messages'][0]['content'] = base.EXTRACT_PROMPT + experiment.MEMBERSHIP_PROMPT
                record['request']['response_format']['json_schema']['schema'] = experiment.extraction_schema(payload['existing_subjects'])
                record['answer'] = wire_fixture(record['answer'])
            study.write_json(folder / f'item3-{stage}.json', record)
    result = subprocess.run([sys.executable, str(Path(experiment.__file__)), 'run', '--out', str(out)],
                            cwd=tmp_path, capture_output=True, text=True, check=True)
    assert 'FINISHED dev requests=0' in result.stdout
    expected = json.loads((original / 'item3-result.json').read_text())
    for label in experiment.LABELS:
        folder = out / f'sample-dev-{label}'
        actual = json.loads((folder / 'item3-result.json').read_text())
        assert actual['memberships'] == expected['memberships']
        assert json.loads((folder / 'checks.json').read_text()) == {'history_unchanged': True, 'resend': 'skipped'}
    assert json.loads((out / 'budget.json').read_text())['attempts'] == []
    assert not list(out.glob('sample-google-*/item3-*.json'))
