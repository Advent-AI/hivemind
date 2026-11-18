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
