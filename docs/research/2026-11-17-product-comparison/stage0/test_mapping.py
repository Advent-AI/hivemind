"""Tests of the mapping's rules (verdict-rule.json `covers`, `same_question`; D672). Synthetic reader answers; no session is run.

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_mapping.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mapping  # noqa: E402


def run_mapping(tmp_path, monkeypatch, codex, claude, thirds=None):
    out = tmp_path / 'out'
    out.mkdir()
    keys = tmp_path / 'keys'
    keys.mkdir()
    monkeypatch.setattr(mapping, 'KEY_FOLDER', keys)
    (keys / 'mapping-key.json').write_text(json.dumps({'new-1': 'L1'}))
    lib = [{'question_id': q, 'question': f'question {q}', 'due': '2027-01-31', 'opened': '2026-07-0' + q[-1], 'possible_answers': ['a', 'b']}
           for q in ('v1', 'v2', 'v3')]
    (out / 'library-L1.json').write_text(json.dumps(lib))
    (out / 'eligibility.json').write_text(json.dumps({'eligible': True}))
    (out / 'map-L1-codex.txt').write_text('\n'.join(json.dumps(r) for r in codex))
    (out / 'map-L1-claude.txt').write_text('\n'.join(json.dumps(r) for r in claude))
    for (matter, q, reader), covers in (thirds or {}).items():
        (out / 'third').mkdir(exist_ok=True)
        (out / 'third' / f'L1--{matter}--{q}--{reader}.json').write_text(json.dumps({'covers': covers}))
    mapping.result(out)
    return json.loads((out / 'mapping.json').read_text())


def test_both_opened_covers_and_a_narrower_covers_only_with_its_main_outcome(tmp_path, monkeypatch):
    """covers: both mark opened, or narrower carrying the main outcome; a narrower without it does not cover."""
    codex = [{'matter': 'M01', 'status': 'opened', 'ids': ['v1']}, {'matter': 'M02', 'status': 'narrower', 'ids': ['v2'], 'main_outcome': False}]
    claude = [{'matter': 'M01', 'status': 'narrower', 'ids': ['v1'], 'main_outcome': True}, {'matter': 'M02', 'status': 'narrower', 'ids': ['v2'], 'main_outcome': False}]
    result = run_mapping(tmp_path, monkeypatch, codex, claude)
    assert result['mapping']['new-1'] == {'M01': [{'question': 'v1', 'covers': True}]}


def test_a_family_split_is_settled_by_two_third_readers_or_stays_split(tmp_path, monkeypatch):
    """A question one family maps and the other not: both third readers yes covers, both no does not, otherwise split."""
    codex = [{'matter': 'M01', 'status': 'opened', 'ids': ['v1']}, {'matter': 'M02', 'status': 'opened', 'ids': ['v2']},
             {'matter': 'M03', 'status': 'opened', 'ids': ['v3']}]
    claude = [{'matter': 'M01', 'status': 'missed', 'ids': []}, {'matter': 'M02', 'status': 'missed', 'ids': []},
              {'matter': 'M03', 'status': 'missed', 'ids': []}]
    thirds = {('M01', 'v1', 'codex'): True, ('M01', 'v1', 'claude'): True, ('M02', 'v2', 'codex'): False, ('M02', 'v2', 'claude'): False,
              ('M03', 'v3', 'codex'): True, ('M03', 'v3', 'claude'): False}
    result = run_mapping(tmp_path, monkeypatch, codex, claude, thirds)
    assert result['mapping']['new-1'] == {'M01': [{'question': 'v1', 'covers': True}], 'M03': [{'question': 'v3', 'covers': 'split'}]}


def test_duplicates_count_both_and_split(tmp_path, monkeypatch):
    """distinct bets: duplicates both families mark, and those one marks, are counted apart."""
    codex = [{'matter': 'M01', 'status': 'missed', 'ids': []}, {'duplicate': 'v2', 'of': 'v1'}, {'duplicate': 'v3', 'of': 'v1'}]
    claude = [{'matter': 'M01', 'status': 'missed', 'ids': []}, {'duplicate': 'v2', 'of': 'v1'}]
    result = run_mapping(tmp_path, monkeypatch, codex, claude)
    assert result['distinct']['new-1'] == {'ids': 3, 'duplicates_both': 1, 'duplicates_split': 1}


def test_a_pair_named_in_either_order_has_the_later_opened_question_as_its_duplicate(tmp_path, monkeypatch):
    """same_question: the duplicate is the later-opened question of the pair, whichever way a reader names it (D675)."""
    codex = [{'matter': 'M01', 'status': 'missed', 'ids': []}, {'duplicate': 'v2', 'of': 'v1'}]
    claude = [{'matter': 'M01', 'status': 'missed', 'ids': []}, {'duplicate': 'v1', 'of': 'v2'}]
    result = run_mapping(tmp_path, monkeypatch, codex, claude)
    assert result['distinct']['new-1'] == {'ids': 3, 'duplicates_both': 1, 'duplicates_split': 0}


def test_a_disagreement_without_both_third_marks_is_refused(tmp_path, monkeypatch):
    """covers: a split needs both third readers' marks; a missing one is refused, never read as a split (D675)."""
    codex = [{'matter': 'M01', 'status': 'opened', 'ids': ['v1']}]
    claude = [{'matter': 'M01', 'status': 'missed', 'ids': []}]
    try:
        run_mapping(tmp_path, monkeypatch, codex, claude, {('M01', 'v1', 'codex'): True})
    except SystemExit as e:
        assert 'third-reader marks missing' in str(e)
    else:
        raise AssertionError('a missing third mark was counted')


def test_an_answer_naming_an_id_outside_the_library_or_a_matter_twice_is_void():
    """read: every matter exactly once, every id in the library, every duplicate pair two library ids; opened names an id; narrower says
    whether it carries the main outcome (D675)."""
    ids = {'Q1', 'Q2'}
    good = [{'matter': 'M01', 'status': 'opened', 'ids': ['Q1']}, {'matter': 'M02', 'status': 'missed', 'ids': []}, {'duplicate': 'Q2', 'of': 'Q1'}]
    assert mapping.answer_problem(good, ['M01', 'M02'], ids) is None
    for rows, reason in (([dict(good[0], ids=['v9'])] + good[1:], 'not in the library'), (good + [good[1]], 'repeated'),
                         (good[:2] + [{'duplicate': 'Q2', 'of': 'Q2'}], 'duplicate pair'),
                         ([dict(good[0], ids=[])] + good[1:], 'names no id'),
                         ([dict(good[0], status='narrower')] + good[1:], 'main-outcome')):
        problem = mapping.answer_problem(rows, ['M01', 'M02'], ids)
        assert problem is not None and reason in problem


def test_export_gives_neutral_ids_in_opening_order_and_keeps_the_system_id():
    """blinding: libraries carry Q1..Qn in opening order; the system's id stays as source_id for the guardrail sample (D675)."""
    lib = mapping.neutral_ids([{'question_id': 'v1'}, {'question_id': 'v3'}, {'question_id': 'v14'}])
    assert [(e['question_id'], e['source_id']) for e in lib] == [('Q1', 'v1'), ('Q2', 'v3'), ('Q3', 'v14')]


def test_the_judge_store_is_the_attempt_its_record_completed_and_an_incomplete_draw_is_refused(tmp_path):
    """plan §1.4 item 10 and D449: the store read is the completed judge attempt (a redo's folder after a redo); an incomplete draw is refused."""
    draw = tmp_path / 'new-1'
    (draw / 'judge').mkdir(parents=True)
    (draw / 'run.json').write_text(json.dumps({'state': 'complete', 'components': {'judge': {'state': 'completed', 'folder': 'judge'}}}))
    (draw / 'judge' / 'run.json').write_text(json.dumps({'new-1': {'state': 'complete', 'attempts': [
        {'folder': 'draw-new-1', 'stopped': 'ReadTimeout'}, {'folder': 'draw-new-1-redo', 'judgements': 40, 'views': 30}]}}))
    assert mapping.store_paths(tmp_path, 'new-1')[0] == draw / 'judge' / 'draw-new-1-redo' / 'views.sqlite'
    (draw / 'run.json').write_text(json.dumps({'state': 'stopped', 'components': {'judge': {'state': 'completed', 'folder': 'judge'}}}))
    try:
        mapping.store_paths(tmp_path, 'new-1')
    except SystemExit as e:
        assert 'not complete' in str(e)
    else:
        raise AssertionError('an incomplete draw was read')


def test_export_refuses_draws_that_are_not_eligible(tmp_path, monkeypatch):
    """D667 and plan §1.4 item 10: no library is exported from draws the eligibility check did not pass."""
    monkeypatch.setattr(mapping, 'KEY_FOLDER', tmp_path / 'keys')
    (tmp_path / 'eligibility.json').write_text(json.dumps({'eligible': False, 'problems': ['launches span 2:00:00']}))
    try:
        mapping.export(tmp_path, tmp_path / 'out', tmp_path / 'eligibility.json')
    except SystemExit as e:
        assert 'not eligible' in str(e)
    except Exception as error:
        raise AssertionError(f'export went past the eligibility check: {error!r}')
    else:
        raise AssertionError('an ineligible run was exported')


def test_a_diagnostic_export_takes_only_finished_draws_under_its_own_key(tmp_path, monkeypatch):
    """Plan §1.4 item 10: what finished is read as a diagnostic, never as the release reading (D675)."""
    monkeypatch.setattr(mapping, 'KEY_FOLDER', tmp_path / 'keys')
    eligibility = {'eligible': False, 'problems': ['old-2 stopped'], 'draws': {d: {'stores': {}} for d in mapping.DRAWS}}
    (tmp_path / 'eligibility.json').write_text(json.dumps(eligibility))
    mapping.export(tmp_path, tmp_path / 'out', tmp_path / 'eligibility.json', diagnostic=True)
    assert (tmp_path / 'out' / 'DIAGNOSTIC').exists() and json.loads((tmp_path / 'keys' / 'mapping-key-diagnostic.json').read_text()) == {}
    assert not (tmp_path / 'keys' / 'mapping-key.json').exists()
