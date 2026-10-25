"""D156 offline acceptance tables, exercised on saved records and scratch copies."""
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import review_subject_names as audit


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = Path(audit.__file__).resolve()
ARCHIVE = ROOT / 'poc/reports/2026-10-25-subject-names-01'
NONEMPTY = ROOT / 'poc/reports/2026-10-25-direct-subjects-01/sample-2-retained'


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False))


def run(out, *args):
    result = subprocess.run([sys.executable, str(SCRIPT), '--out', str(out), '--json', *args],
                            cwd=out.parent, text=True, capture_output=True)
    return result.returncode, json.loads(result.stdout)


def fixture(tmp_path, names=False):
    """Real nonempty D147 result, optionally with its choices restated as names.

    Only the representation changes. The expected projection is the original
    archived set of references, not output from the projection being examined.
    """
    out = tmp_path / 'audit'
    sample = out / 'sample-real'
    sample.mkdir(parents=True)
    prefix = out / 'prefix'
    prefix.mkdir()
    shutil.copyfile(NONEMPTY / 'item2-result.json', prefix / 'item2-result.json')
    shutil.copyfile(ARCHIVE / 'items.json', out / 'items.json')
    for name in ('item3-extract.json', 'item3-match.json', 'item3-result.json'):
        shutil.copyfile(NONEMPTY / name, sample / name)
    shutil.copyfile(ARCHIVE / 'sample-dev-1-names/checks.json', sample / 'checks.json')
    write(out / 'manifest.json', {'version': 'subject-names-v1', 'source': str(prefix), 'plan': {'dev': ['real']}})
    if names:
        extract = read(sample / 'item3-extract.json')
        answer = extract['answer']
        payload = json.loads(extract['request']['messages'][1]['content'])
        offered = {t['thread_id']: t for t in payload['existing_subjects']}
        declarations = {t['id']: t for t in answer['threads']}
        original = copy.deepcopy(answer)
        for candidate in answer['candidates']:
            choices = []
            for ref in candidate.pop('thread_ids'):
                if ref in offered:
                    choices.append({'existing': offered[ref]['name'], 'new_name': '', 'new_scope': ''})
                else:
                    choices.append({'existing': 'none', 'new_name': declarations[ref]['name'],
                                    'new_scope': declarations[ref]['scope']})
            candidate['subjects'] = choices
        answer.pop('threads')
        write(sample / 'item3-extract.json', extract)
        write(sample / 'item3-extract-projection.json', {
            'subjects': [c['subjects'] for c in answer['candidates']],
            'thread_ids': [c['thread_ids'] for c in original['candidates']], 'threads': original['threads']})
    return out, sample


def test_empty_population_is_unexercised_not_a_grouping_success(tmp_path):
    """Empty-candidate row: original four runs contain only prior memberships."""
    code, report = run(ARCHIVE)
    assert code == 0 and report['states'] == {'complete': 4}
    assert [(r['grouping'], r['references_checked'], r['new_memberships']) for r in report['samples']] == [
        ('unexercised', 0, 0)] * 4
    assert sum(len(r['evidence']) for r in report['samples']) == 8
    assert sum(bool(e['rejection']) for r in report['samples'] for e in r['evidence']) == 2
    assert report['acceptance'] == 'not_established' and report['semantic_cases_judged'] == 0


def test_unstarted_samples_remain_in_the_denominator():
    """Pre-first-step row: six registered holdout samples have never run."""
    code, report = run(ARCHIVE, '--case', 'all')
    assert code == 1 and report['samples_registered'] == 10
    assert report['states'] == {'complete': 4, 'not_started': 6}


@pytest.mark.parametrize('names', [False, True])
def test_nonempty_old_and_names_formats_through_entrypoint(tmp_path, names):
    """Both formats: references survive the rejected candidate and final IDs."""
    out, _ = fixture(tmp_path, names)
    code, report = run(out)
    assert code == 0, report
    row = report['samples'][0]
    assert (row['references_checked'], row['bindings_checked'], row['new_memberships']) == (3, 2, 2)
    assert [c['disposition'] for c in row['candidates']] == ['rejected', 'new', 'new']
    assert row['semantic_status'] == 'pending'


@pytest.mark.parametrize('names', [False, True])
@pytest.mark.parametrize('breach', ['swap', 'missing', 'stored_target'])
def test_same_count_wrong_target_and_missing_references_fail(tmp_path, names, breach):
    """Both-format counterexamples: valid IDs, wrong target; no length proxy."""
    out, sample = fixture(tmp_path, names)
    if breach == 'stored_target':
        path = sample / 'item3-result.json'
        value = read(path)
        value['bindings'][0]['thread_id'] = 'g1'
    elif names:
        path = sample / 'item3-extract-projection.json'
        value = read(path)
        value['thread_ids'][1] = ['g1'] if breach == 'swap' else []
    else:
        path = sample / 'item3-extract.json'
        value = read(path)
        value['answer']['candidates'][1]['thread_ids'] = ['g1'] if breach == 'swap' else []
    write(path, value)
    code, report = run(out)
    assert code == 1 and report['states'] == {'invalid': 1}, report
    assert report['samples'][0]['errors']


def test_identical_name_does_not_hide_changed_scope(tmp_path):
    """Value-reader row: preserve both name and scope when creating a group."""
    out, sample = fixture(tmp_path, True)
    path = sample / 'item3-extract-projection.json'
    value = read(path)
    value['threads'][0]['scope'] = 'A different customer-only deployment.'
    write(path, value)
    code, report = run(out)
    assert code == 1 and 'Projection changed new target' in report['samples'][0]['errors'][0]


@pytest.mark.parametrize('index,ref,reason', [(0, 'g2', 'changed existing target'),
                                             (1, 't2', 'changed new target')])
def test_projection_itself_checks_exact_targets(tmp_path, index, ref, reason):
    """Projection row: another valid target of the same type must be caught here."""
    _, sample = fixture(tmp_path, True)
    extract = read(sample / 'item3-extract.json')
    payload = json.loads(extract['request']['messages'][1]['content'])
    projection = read(sample / 'item3-extract-projection.json')
    projection['thread_ids'][index] = [ref]
    with pytest.raises(audit.RecordError, match=reason):
        audit.projected_answer(extract['answer'], payload['existing_subjects'], projection)


@pytest.mark.parametrize('breach,state', [('missing_checks', 'incomplete'), ('failed_checks', 'failed'),
                                         ('failed_with_result', 'failed'), ('missing_match', 'incomplete')])
def test_result_file_alone_never_proves_completion(tmp_path, breach, state):
    """State table: failed.json wins and final completion checks are mandatory."""
    out, sample = fixture(tmp_path)
    if breach == 'missing_checks':
        (sample / 'checks.json').unlink()
    elif breach == 'failed_checks':
        write(sample / 'checks.json', {'history_unchanged': False, 'resend': 'skipped'})
    elif breach == 'missing_match':
        (sample / 'item3-match.json').unlink()
    else:
        write(sample / 'failed.json', {'error': 'History check failed after result was written'})
    code, report = run(out)
    assert code == 1 and report['states'] == {state: 1}


def test_unidentified_input_is_not_a_negative_semantic_case(tmp_path):
    """Precondition row: wrong registered input fails before judging choices."""
    out, _ = fixture(tmp_path)
    path = out / 'items.json'
    value = read(path)
    value['dev']['input_id'] = 'gnews:different-input'
    write(path, value)
    code, report = run(out)
    assert code == 1 and 'registered item' in report['samples'][0]['errors'][0]


def test_snapshot_rejects_changes_including_late_failure(tmp_path):
    """Concurrent-writer row: absent failure files are part of the snapshot."""
    path = tmp_path / 'failed.json'
    snapshot = audit.Snapshot()
    assert snapshot.read(path, optional=True) is None
    write(path, {'error': 'late failure'})
    with pytest.raises(audit.RecordError, match='changed during audit'):
        snapshot.verify()


def test_structural_agreement_is_not_business_correctness(tmp_path):
    """Semantic boundary: consistently misgrouping a PC does not gain a pass."""
    out, sample = fixture(tmp_path)
    path = sample / 'item3-extract.json'
    extract = read(path)
    extract['answer']['candidates'][1]['thread_ids'] = ['g1']
    write(path, extract)
    path = sample / 'item3-result.json'
    result = read(path)
    result['bindings'][0]['thread_id'] = 'g1'
    result['threads'] = [t for t in result['threads'] if t['thread_id'] != 'g3']
    for member in result['memberships']:
        if member['view_id'] == 'v3':
            member['thread_id'] = 'g1'
    write(path, result)
    code, report = run(out)
    assert code == 0, report
    assert report['acceptance'] == 'not_established' and report['semantic_cases_judged'] == 0


def test_plain_default_entrypoint_from_other_directory(tmp_path):
    """User entrypoint: default dev case and no --json, independent of cwd."""
    result = subprocess.run([sys.executable, str(SCRIPT), '--out', str(ARCHIVE)],
                            cwd=tmp_path, capture_output=True, text=True)
    assert result.returncode == 0 and result.stdout.count('grouping=unexercised') == 4
    assert 'semantic acceptance is NOT established' in result.stdout
