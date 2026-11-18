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
    entry = {'possible_answers': ['below 1', 'from 1 to 2', 'over 2'], 'answer': 'from 1 to 2', 'answer_index': 1}
    assert 'Latest answer at the cutoff: over 2' in mark_cards.plant('x\nLatest answer at the cutoff: from 1 to 2\ny', entry)
    entry.update(answer='over 2', answer_index=2)
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


def test_a_card_without_a_different_adjacent_rung_is_not_planted():
    """controls: a plant must move the answer to a different rung; a one-rung ladder cannot be planted."""
    assert mark_cards.plant('Latest answer at the cutoff: yes', {'possible_answers': ['yes'], 'answer': 'yes', 'answer_index': 0}) is None


def test_a_debate_round_reads_only_earlier_rounds(tmp_path):
    """debate: round r compares the marks of rounds before r; a mark already written in round r is never shown (D675)."""
    for label, family, mark in (('round-0', 'codex', {'worth': 'worth', 'answer': None}), ('round-0', 'claude', {'worth': 'trivia', 'answer': None}),
                                ('round-1', 'claude', {'worth': 'worth', 'answer': None})):
        (tmp_path / label).mkdir(exist_ok=True)
        (tmp_path / label / f'C003-{family}.json').write_text(json.dumps(mark))
    assert mark_cards.current(tmp_path, 'C003', 'claude', 0) == {'worth': 'trivia', 'answer': None}
    assert mark_cards.current(tmp_path, 'C003', 'claude', 1) == {'worth': 'worth', 'answer': None}


def test_readings_refuse_a_deck_whose_debate_rounds_are_not_complete(tmp_path, monkeypatch):
    """debate: no readings before rounds 0, 1 and 2 are complete, even when every card has its round-0 marks (D675)."""
    monkeypatch.setattr(mark_cards, 'KEY', tmp_path / 'deck-key.json')
    monkeypatch.setattr(mark_cards.mapping_tool, 'MATTERS', tmp_path / 'matters.json')
    (tmp_path / 'deck-key.json').write_text(json.dumps({'C001': {'draw': 'new-1', 'question': 'Q1', 'role': 'product', 'guardrail': True,
                                                                  'covering': False, 'type': 'figure', 'answered': True}}))
    (tmp_path / 'matters.json').write_text(json.dumps({'matters': [{'matter': 'M01', 'company_figure': False}]}))
    (tmp_path / 'mapping.json').write_text(json.dumps({'mapping': {}, 'distinct': {}, 'eligibility_sha256': 'e'}))
    (tmp_path / 'round-0').mkdir()
    for family in ('codex', 'claude'):
        (tmp_path / 'round-0' / f'C001-{family}.json').write_text(json.dumps({'worth': 'worth', 'answer': 'supported'}))
    (tmp_path / 'round-0.done').write_text('')
    try:
        mark_cards.readings(tmp_path, tmp_path)
    except SystemExit as e:
        assert 'round 1 is not complete' in str(e)
    else:
        raise AssertionError('readings ran without the debate')


def test_a_field_agreed_in_a_round_stays_settled(tmp_path):
    """debate: a later round changes only disputed fields; a field both agreed on keeps its agreed mark (D675)."""
    for label, family, mark in (('round-0', 'codex', {'worth': 'worth', 'answer': 'supported'}),
                                ('round-0', 'claude', {'worth': 'worth', 'answer': 'unsupported'}),
                                ('round-1', 'codex', {'worth': 'trivia', 'answer': 'unsupported'})):
        (tmp_path / label).mkdir(exist_ok=True)
        (tmp_path / label / f'C004-{family}.json').write_text(json.dumps(mark))
    assert mark_cards.final(tmp_path, 'C004') == {'worth': 'worth', 'answer': 'unsupported'}


def test_the_guardrail_sample_draws_from_the_system_ids_sorted_as_strings():
    """guardrails.sample: random.Random(20261117).sample(sorted system ids, 35), mapped to the neutral ids, on ids with gaps (D675)."""
    import random
    source = [f'v{n}' for n in range(1, 61) if n % 7]                      # gaps, as the new system's ids have
    lib = [{'question_id': f'Q{k}', 'source_id': s} for k, s in enumerate(source, 1)]
    expected = {lib[source.index(s)]['question_id'] for s in random.Random(20261117).sample(sorted(source), 35)}
    assert mark_cards.guardrail_sample(lib) == expected


def test_an_empty_answer_written_as_the_string_null_is_null():
    """marks: "null" and null are the same empty answer, so two readers who both leave it empty agree."""
    assert mark_cards.normalised({'worth': 'worth', 'answer': 'null'})['answer'] is None
    assert not mark_cards.valid({'worth': 'worth', 'answer': None, 'why': ' '.join(['w'] * 41)}, False)


def deck_inputs(tmp_path, monkeypatch, plant_supported):
    """Six libraries of four answered questions on two-rung ladders; a fake closed reader that calls a card supported when its latest
    answer is 'low' and calls a planted 'high' answer `plant_supported`."""
    keys = tmp_path / 'keys'
    keys.mkdir()
    monkeypatch.setattr(mark_cards.mapping_tool, 'KEY_FOLDER', keys)
    monkeypatch.setattr(mark_cards, 'KEY', keys / 'deck-key.json')
    out = tmp_path / 'mapping-out'
    out.mkdir()
    draws = ['new-1', 'new-2', 'new-3', 'old-1', 'old-2', 'old-3']
    (keys / 'mapping-key.json').write_text(json.dumps({d: f'L{n}' for n, d in enumerate(draws, 1)}))
    for n, d in enumerate(draws, 1):
        lib = [{'question_id': f'Q{k}', 'source_id': f'v{2 * k - 1}', 'question': f'{d} question {k}', 'due': '2027-01-31', 'opened': '2026-07-10',
                'type': 'yes/no', 'possible_answers': ['low', 'high'], 'answer': 'low', 'answer_index': 0, 'reasons': 'r', 'material': []}
               for k in range(1, 5)]
        (out / f'library-L{n}.json').write_text(json.dumps(lib))
    (out / 'mapping.json').write_text(json.dumps({'mapping': {}, 'distinct': {}}))
    def fake_run(family, prompt):
        supported = plant_supported if 'Latest answer at the cutoff: high' in prompt else True
        return json.dumps({'supported': supported, 'why': 'fake'}), None
    monkeypatch.setattr(mark_cards.census_readers, 'run', fake_run)
    return out


def test_the_deck_admits_a_plant_only_when_a_reader_confirms_it_is_not_supported(tmp_path, monkeypatch):
    """controls: a plant enters the deck only when a separate closed reader confirms the moved answer is not supported (D675)."""
    out = deck_inputs(tmp_path, monkeypatch, plant_supported=True)
    try:
        mark_cards.deck(out, tmp_path / 'deck')
    except SystemExit as e:
        assert 'plants confirmed not supported' in str(e)
    else:
        raise AssertionError('a plant the reader called supported was admitted')


def test_the_deck_holds_six_plants_four_supported_controls_three_repeats_and_never_overwrites_its_key(tmp_path, monkeypatch):
    """controls: 3 plants per system, 4 supported controls, 3 repeats; the key is written once (D675)."""
    out = deck_inputs(tmp_path, monkeypatch, plant_supported=False)
    mark_cards.deck(out, tmp_path / 'deck')
    roles = [k['role'] for k in json.loads(mark_cards.KEY.read_text()).values()]
    assert (roles.count('plant'), roles.count('supported control'), roles.count('repeat'), roles.count('product')) == (6, 4, 3, 24)
    try:
        mark_cards.deck(out, tmp_path / 'deck-2')
    except SystemExit as e:
        assert 'never overwrites' in str(e)
    else:
        raise AssertionError('a second deck overwrote the key')


def test_the_scorer_scores_what_the_writer_builds_and_keeps_an_empty_draw(tmp_path, monkeypatch):
    """One writer of the readings: a draw that opened no question keeps an empty card map, and `score_comparison.score` refuses a
    readings.json that differs from what the writer builds from the named inputs (D675, Codex round 18)."""
    import score_comparison
    monkeypatch.setattr(mark_cards, 'KEY', tmp_path / 'deck-key.json')
    monkeypatch.setattr(mark_cards.mapping_tool, 'MATTERS', tmp_path / 'matters.json')
    monkeypatch.setattr(mark_cards, 'matter_first_days', lambda: {'M01': '2026-09-07'})
    (tmp_path / 'deck-key.json').write_text(json.dumps({'C001': {'draw': 'new-1', 'question': 'Q1', 'role': 'product', 'guardrail': True,
                                                                  'covering': False, 'type': 'figure', 'answered': True, 'opened': None}}))
    (tmp_path / 'matters.json').write_text(json.dumps({'matters': [{'matter': 'M01', 'company_figure': False}]}))
    (tmp_path / 'mapping.json').write_text(json.dumps({'mapping': {'new-1': {}, 'new-2': {}}, 'distinct': {}, 'eligibility_sha256': 'e'}))
    (tmp_path / 'round-0').mkdir()
    for family in ('codex', 'claude'):
        (tmp_path / 'round-0' / f'C001-{family}.json').write_text(json.dumps({'worth': 'worth', 'answer': 'supported'}))
    for n in (0, 1, 2):
        (tmp_path / f'round-{n}.done').write_text('')
    built = mark_cards.build_readings(tmp_path, tmp_path)
    assert built['cards']['new-2'] == {}
    mark_cards.readings(tmp_path, tmp_path)
    recorded = json.loads((tmp_path / 'readings.json').read_text())
    recorded['cards']['new-1']['Q1']['answer'] = 'no answer'
    (tmp_path / 'readings.json').write_text(json.dumps(recorded))
    try:
        score_comparison.score(tmp_path, tmp_path)
    except SystemExit as e:
        assert 'differs from the readings its writer builds' in str(e)
    else:
        raise AssertionError('an edited readings.json was scored')
    mark_cards.readings(tmp_path, tmp_path)                                  # control: the unedited record passes this check
    try:
        score_comparison.score(tmp_path, tmp_path)
    except SystemExit as e:
        assert 'differs from the readings its writer builds' not in str(e)
