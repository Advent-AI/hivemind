"""Tests of the card builder (card-spec.md; D673, D675). Synthetic requests in the judge's own format (`judging._lines_english`).

Run: python3 -m pytest docs/research/2026-11-17-product-comparison/stage0/test_build_cards.py
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_cards  # noqa: E402

REQUEST = '\n'.join([
    'Thesis v3 (NVDA, asset, focus "data-centre revenue", 2027, due 2027-02-28): What will data-centre revenue be in FY2027?',
    'Ladder: rung 1 low: below 150bn / rung 2 high: 150bn or more', '',
    '[Evidence in view under this thesis, 2 items]',
    '- e135 [fact; Yahoo Finance (finance.yahoo.com); Jensen Huang quoted; original source NVIDIA ; from gnews:3e5f 2026-09-10] Orders rose.',
    '    Quote: "We see demand',
    'well beyond supply," he said.',
    '    Opinion, not verified: the matcher read this as the same claim as e101; the argument counts one claim, one more outlet.',
    '- e140 [estimate; Reuters; analyst; original source Morgan Stanley 2026-09-08; from gnews:9a1c 2026-09-09] Estimate raised to 160bn.',
    '    Quote: "We raise our estimate to $160bn."',
    '', '[Current conclusions of the theses it depends on]', '- v1 (open; supports) other thesis: now rung 2'])


def test_every_evidence_item_is_read_whole_with_its_speaker_and_without_matcher_notes():
    """card-spec 3 and D673: each item the request contained, its speaker as written (a speaker may hold ';'), a quote over several lines
    kept whole, matcher notes removed, nothing after the evidence section read as evidence."""
    items = build_cards.material(json.dumps({'messages': [{'role': 'user', 'content': REQUEST}]}))
    assert len(items) == 2
    first = items[0]
    assert (first['tier'], first['speaker'], first['original'], first['input_id'], first['day']) == (
        'fact', 'Yahoo Finance (finance.yahoo.com); Jensen Huang quoted', 'NVIDIA', 'gnews:3e5f', '2026-09-10')
    assert first['quote'] == '"We see demand\nwell beyond supply," he said.' and 'matcher' not in first['quote']
    assert items[1]['summary'] == 'Estimate raised to 160bn.' and 'Current conclusions' not in items[1]['quote']


def test_the_card_shows_no_reference_annotation_and_orders_material_by_day():
    """D673 form check: the answer step's reference annotations are removed; card-spec 3: material by day."""
    for suffix in (' (no reference figure when the question opened)', ' (the reference when the question opened: "a (b) c")',
                   ' (the amount last reported when the question opened: "Supply commitments of $119 billion")'):
        assert build_cards.ANNOTATION.sub('', 'below 150bn' + suffix) == 'below 150bn'
    entry = {'question_id': 'Q1', 'question': 'q', 'opened': '2026-07-04', 'due': '2027-02-28', 'possible_answers': ['a', 'b'], 'answer': 'a', 'reasons': 'r',
             'material': [{'tier': 'fact', 'publisher': 'Reuters', 'speaker': 's', 'original': 'o', 'day': '2026-09-10', 'summary': 'later', 'quote': ''},
                          {'tier': 'fact', 'publisher': 'Bloomberg', 'speaker': 's', 'original': 'o', 'day': '2026-09-08', 'summary': 'earlier', 'quote': ''}]}
    text = build_cards.card_text(entry, [entry])
    assert text.index('earlier') < text.index('later') and 'publisher Bloomberg' in text   # card-spec 3: the source's publisher and day


CONTEXT = '\n'.join([
    '[Evidence in view under this thesis, 0 items]',
    '[Not shown: 104 more pieces in force, read in earlier judgements; the previous conclusion carries them]',
    '', '[Themes in force, 1]',
    '- v5 (ai-capex, due 2028-02-01) How much will hyperscalers spend in 2027?: now rung 3 Middle; judged 2026-07-10; '
    'updated since this thesis was last judged; reasons: The reference sits in rung 3.',
    '', '[Previous conclusion, for comparison only] rung 2; reasons: Guidance implies strong growth.',
    'It continues on a second line.',
    '', 'Answer per the JSON schema. cites may name only the evidence ids listed above.'])


def test_the_card_carries_what_the_request_gave_besides_its_evidence(tmp_path):
    """card-spec 3 as D675 reads it: the hidden-items line, the themes in force and the previous answer the answering request carried,
    each rung shown by its condition and no thesis id (D673)."""
    conn = sqlite3.connect(tmp_path / 'views.sqlite')
    conn.execute('create table rungs (view_id text, position integer, label text, condition text)')
    conn.executemany('insert into rungs values (?, ?, ?, ?)', [('v5', 3, 'Middle', 'from 500bn to 700bn'), ('v9', 2, 'Up', 'from 150bn to 200bn')])
    conn.commit()
    ctx = build_cards.context(json.dumps({'messages': [{'role': 'user', 'content': CONTEXT}]}), build_cards.ro(tmp_path / 'views.sqlite'))
    assert ctx['hidden'] == 104 and ctx['previous'] == {'rung': 2, 'reasons': 'Guidance implies strong growth.\nIt continues on a second line.'}
    assert ctx['themes'] == [{'question': 'How much will hyperscalers spend in 2027?', 'due': '2028-02-01', 'rung': 3, 'answer': 'from 500bn to 700bn',
                              'possible_answers': ['from 500bn to 700bn'], 'judged': '2026-07-10', 'updated': True,
                              'reasons': 'The reference sits in rung 3.'}]
    entry = {'question_id': 'Q2', 'question': 'q', 'opened': '2026-07-04', 'due': '2027-02-28', 'possible_answers': ['below 150bn', 'from 150bn to 200bn'],
             'answer': 'below 150bn', 'reasons': 'r', 'material': [], 'context': dict(ctx, previous=dict(ctx['previous'], answer='from 150bn to 200bn'))}
    other = {'question_id': 'Q1', 'question': 'earlier question', 'opened': '2026-07-04'}
    text = build_cards.card_text(entry, [other, entry])
    assert 'Not shown to the answer: 104 more items' in text and 'answered 3. from 500bn to 700bn on 2026-07-10; updated since' in text
    assert 'Its possible answers: 1. from 500bn to 700bn' in text
    assert 'Previous answer, given for comparison: 2. from 150bn to 200bn' in text and 'v5' not in text and 'Middle' not in text
    assert 'q   <- this question' in text and 'Opened: 2026-07-04' in text
    assert text.index('earlier question') < text.index('q   <- this question')


def test_a_request_whose_items_the_card_cannot_all_read_is_refused():
    """card-spec 3: every evidence item the request contained; a quote line opening with '[' must not cut the material silently (D675)."""
    text = REQUEST.replace('well beyond supply," he said.', '[sic] well beyond supply," he said.\n\n[Analyst note] x')
    try:
        build_cards.material(json.dumps({'messages': [{'role': 'user', 'content': text}]}))
    except ValueError as e:
        assert 'states 2 evidence items' in str(e)
    else:
        raise AssertionError('a cut material list was accepted')
