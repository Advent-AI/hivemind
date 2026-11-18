"""Tests of the card marking's rules (verdict-rule.json marks and controls; Deck 1's protocol; D672). Synthetic marks; no session runs.

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_mark_cards.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import mark_cards  # noqa: E402


def test_a_plant_moves_the_latest_answer_one_rung():
    """controls: a planted wrong answer is a real card with its latest answer moved one rung (the next, or the previous at the end)."""
    entry = {'possible_answers': ['below 1', 'from 1 to 2', 'over 2'], 'answer': 'from 1 to 2'}
    assert 'Latest answer at the cutoff: over 2' in mark_cards.plant('x\nLatest answer at the cutoff: from 1 to 2\ny', entry)
    entry['answer'] = 'over 2'
    assert 'Latest answer at the cutoff: from 1 to 2' in mark_cards.plant('Latest answer at the cutoff: over 2', entry)


def test_a_mark_still_split_after_debate_is_kept_as_a_split(tmp_path):
    """marks: agreed fields take the value; a field still different after the last round is {"split": [codex, claude]}."""
    for family, mark in (('codex', {'worth': 'worth', 'answer': 'supported'}), ('claude', {'worth': 'worth', 'answer': 'insufficient'})):
        (tmp_path / 'round-0').mkdir(exist_ok=True)
        (tmp_path / 'round-0' / f'C001-{family}.json').write_text(json.dumps(mark))
    (tmp_path / 'round-1').mkdir()
    (tmp_path / 'round-1' / 'C001-claude.json').write_text(json.dumps({'worth': 'worth', 'answer': 'insufficient'}))
    assert mark_cards.final(tmp_path, 'C001') == {'worth': 'worth', 'answer': {'split': ['supported', 'insufficient']}}


def test_a_later_round_replaces_an_earlier_mark(tmp_path):
    """debate: each family's latest round is its mark."""
    for label, family, mark in (('round-0', 'codex', {'worth': 'trivia', 'answer': None}), ('round-0', 'claude', {'worth': 'worth', 'answer': None}),
                                ('round-1', 'codex', {'worth': 'worth', 'answer': None})):
        (tmp_path / label).mkdir(exist_ok=True)
        (tmp_path / label / f'C002-{family}.json').write_text(json.dumps(mark))
    assert mark_cards.final(tmp_path, 'C002') == {'worth': 'worth', 'answer': None}


def test_a_mark_is_valid_only_with_the_frozen_values():
    """marks: worth in worth/trivia/duplicate; answer in supported/unsupported/insufficient, and none on a card with no answer."""
    assert mark_cards.valid({'worth': 'worth', 'answer': 'supported'}, True)
    assert not mark_cards.valid({'worth': 'yes', 'answer': 'supported'}, True)
    assert not mark_cards.valid({'worth': 'worth', 'answer': None}, True)
    assert mark_cards.valid({'worth': 'trivia', 'answer': None}, False)
