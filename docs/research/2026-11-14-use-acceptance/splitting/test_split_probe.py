"""The split probe end to end at $0 (DESIGN.md v4 §3; council round 161): the check's record, the send of both arms through the real
runners and limits with a fake transport, the reading folder, made-up reader rows, and the verdict. The transport answers the frozen
arm with each topic's stored answer, and the split arm's two T topics with a split and a ladder for each year (quoting the articles),
the other topics with their stored answer in the split schema's shape. Nothing is sent.

Run: python3 -m pytest docs/research/2026-11-14-use-acceptance/splitting/test_split_probe.py
"""
import json
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_split  # noqa: E402
import accounting  # noqa: E402
import ladder_split  # noqa: E402
import reading_split  # noqa: E402
import score_split  # noqa: E402

USAGE = {'prompt_tokens': 5000, 'completion_tokens': 1500}
B = 10 ** 9
YEARLY = {   # (topic, year): (the article's words, the unit, its value, the four bounds of the ranges); amounts in full (the schema's USD)
    ('c1/clean-4', '2026'): ('plan to spend approximately $800 billion in capital expenditures (capex) in 2026 alone', 'USD', 800 * B, [600 * B, 700 * B, 900 * B, 1000 * B]),
    ('c1/clean-4', '2027'): ('roughly $1.3 trillion in 2027', 'USD', 1300 * B, [900 * B, 1100 * B, 1500 * B, 1700 * B]),
    ('c1/clean-12', '2026'): ('Goldman Sachs forecasts $1 trillion in global spend this year', 'USD', 1000 * B, [700 * B, 900 * B, 1100 * B, 1300 * B]),
    ('c1/clean-12', '2027'): ('rising to 2.5% in 2027', 'percent', 2.5, [1.5, 2, 3, 3.5]),
}


def yearly_ladder(topic, year):
    words, unit, value, bounds = YEARLY[(topic, year)]
    ranges = [{'lo': None, 'hi': bounds[0]}] + [{'lo': a, 'hi': b} for a, b in zip(bounds, bounds[1:])] + [{'lo': bounds[-1], 'hi': None}]
    return json.dumps({'no_ladder': None, 'ladder': {
        'question': f'What will the quantity this topic tracks be for calendar {year}?', 'object': 'ai-capex', 'not_judged': [], 'event': None,
        'figure': {'unit': unit, 'year': year, 'ranges': ranges, 'favourable_end': 'n/a', 'favourable_why': ''},
        'reference': {'words': words, 'kind': 'expected', 'value': value, 'value_to': None},
        'due_day': f'{int(year) + 1}-02-28', 'due_day_basis': 'expected_publication'}})


def in_split_shape(text):
    """A stored frozen answer as the split schema writes it: a decline's text becomes the reason of the case no_main."""
    answer = json.loads(text)
    if isinstance(answer.get('no_ladder'), str):
        answer['no_ladder'] = {'case': 'no_main', 'reason': answer['no_ladder'], 'periods': None}
    return json.dumps(answer)


def transport_for(split_controls=(), declining_controls=(), declining_years=()):
    topics = {case['thesis']['description']: (group, f'{source}:{name}', name) for group, source, name, case in probe_split.load_topics()}
    stored = {f'{source}:{name}': probe_split.stored_first(source, name)['requests'][-1]['answer_text'] for _, source, name, _ in probe_split.load_topics()}

    def transport(provider, request):
        user = request['messages'][1]['content']
        group, topic, name = next(value for description, value in topics.items() if json.dumps(description, ensure_ascii=False)[1:-1] in user)
        split_arm = request['response_format']['json_schema']['schema']['properties']['no_ladder']['anyOf'][1].get('type') == 'object'
        year = next((y for y in ('2026', '2027') if f'Write the question for {y} only' in user), None)
        if not split_arm:
            text = stored[topic]
        elif year is not None:
            text = yearly_ladder(name, year) if group == 'T' and (name, year) not in declining_years else json.dumps(
                {'no_ladder': {'case': 'no_main', 'reason': 'the year is only a base', 'periods': None}, 'ladder': None})
        elif topic in declining_controls:
            text = json.dumps({'no_ladder': {'case': 'no_main', 'reason': 'several figures, none the main one', 'periods': None}, 'ladder': None})
        elif group == 'T' or topic in split_controls:
            text = json.dumps({'no_ladder': {'case': ladder_split.SPLIT_CASE, 'reason': 'one quantity for each of two years', 'periods': ['2026', '2027']},
                               'ladder': None})
        else:
            text = in_split_shape(stored[topic])
        return {'choices': [{'message': {'content': text}}], 'usage': USAGE}
    return transport


@pytest.fixture(scope='module')
def checked(tmp_path_factory):
    record = tmp_path_factory.mktemp('record') / 'check-passed.json'
    original, probe_split.RECORD = probe_split.RECORD, record
    try:
        probe_split.check()
    finally:
        probe_split.RECORD = original
    return record


@pytest.fixture(scope='module')
def sent(checked, tmp_path_factory):
    folder = tmp_path_factory.mktemp('probe') / 'run'
    original, probe_split.RECORD = probe_split.RECORD, checked
    try:
        assert probe_split.send(folder, transport=transport_for()) == 0
    finally:
        probe_split.RECORD = original
    return folder


def test_the_send_files_both_arms_and_the_t_topics_split_into_two_written_years(sent):
    split_rows = reading_split.rows_of(sent / 'split')
    assert len(split_rows) == len(reading_split.rows_of(sent / 'frozen')) == 12 * 3
    t_rows = [row for row in split_rows if row['case'].split('|')[1] in ('week-10-06:c1/clean-4', 'week-10-06:c1/clean-12')]
    assert [row['status'] for row in t_rows] == ['split'] * 6
    assert all({year: child['status'] for year, child in row['children'].items()} == {'2026': 'ladder', '2027': 'ladder'} for row in t_rows)
    assert all(row['children'][year]['view']['year'] == year for row in t_rows for year in ('2026', '2027'))


def test_a_request_changed_after_the_check_is_refused_before_any_send(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe_split, 'RECORD', checked)
    monkeypatch.setattr(ladder_split, 'RESTRICTION', ladder_split.RESTRICTION + ' ')
    calls = []
    with pytest.raises(SystemExit, match='REFUSED: the requests differ|no check record'):
        probe_split.send(tmp_path / 'run', transport=lambda provider, request: calls.append(request))
    assert calls == [] and not (tmp_path / 'run').exists()


def test_the_counts_pass_when_the_t_topics_split_and_no_control_moves(sent):
    counted = score_split.counts(sent)
    assert counted['pass'] and all(entry['sends succeeding'] == [1, 2, 3] for entry in counted['T'].values())
    assert all(entry['passes'] and not entry['sends naming the case'] for entry in counted['controls'].values())


def test_a_control_naming_the_split_case_fails_the_counts(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe_split, 'RECORD', checked)
    assert probe_split.send(tmp_path / 'run', transport=transport_for(split_controls=('fortnight:c1/clean-9',))) == 0
    counted = score_split.counts(tmp_path / 'run')
    assert not counted['pass'] and counted['controls']['fortnight:c1/clean-9']['sends naming the case'] == [1, 2, 3]
    assert score_split.verdict(tmp_path / 'run', tmp_path / 'keys')[0] == 'negative'


def test_a_control_whose_kind_changes_in_two_of_three_sends_fails_the_counts(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe_split, 'RECORD', checked)
    assert probe_split.send(tmp_path / 'run', transport=transport_for(declining_controls=('july:c3/clean-5',))) == 0
    entry = score_split.counts(tmp_path / 'run')['controls']['july:c3/clean-5']
    assert entry['frozen kinds'] == ['ladder'] * 3 and entry['split kinds'] == ['no ladder'] * 3
    assert entry['kind changed'] and not entry['sends naming the case'] and not entry['passes']


def test_a_t_topic_whose_second_year_is_declined_in_every_send_fails_the_counts(checked, tmp_path, monkeypatch):
    monkeypatch.setattr(probe_split, 'RECORD', checked)
    assert probe_split.send(tmp_path / 'run', transport=transport_for(declining_years=(('c1/clean-12', '2027'),))) == 0
    counted = score_split.counts(tmp_path / 'run')
    assert counted['T']['week-10-06:c1/clean-12'] == {'sends succeeding': [], 'passes': False}
    assert counted['T']['week-10-06:c1/clean-4']['passes'] and not counted['pass']


def test_a_send_filed_twice_is_not_scored(sent, tmp_path):
    probe = tmp_path / 'probe'
    shutil.copytree(sent, probe)
    outcomes = probe / 'split' / 'send-1' / 'outcomes.jsonl'
    first = outcomes.read_text().splitlines()[0]
    outcomes.write_text(outcomes.read_text() + first + '\n')
    with pytest.raises(SystemExit, match='NOT SCORED: the split arm does not hold every topic and pass exactly once'):
        score_split.counts(probe)


def test_no_topic_of_the_probe_is_one_of_the_44():
    descriptions = probe_split.descriptions_of_the_44()
    assert len(descriptions) == 44 and not any(case['thesis']['description'] in descriptions for *_, case in probe_split.load_topics())
    assert not any(source == 'stage-b' for entries in probe_split.TOPICS.values() for source, _ in entries)


def test_the_check_refuses_a_topic_that_is_one_of_the_44(tmp_path, monkeypatch):
    monkeypatch.setattr(probe_split, 'RECORD', tmp_path / 'check-passed.json')
    monkeypatch.setitem(probe_split.SOURCES, 'stage-b', ([probe_split.THE_44], probe_split.DATA / 'clean-ladder-stage-a-2026-11-10/run-4'))
    monkeypatch.setattr(probe_split, 'TOPICS', dict(probe_split.TOPICS, C2=[('stage-b', 'acc/clean-9'), ('july', 'c2/clean-10')]))
    with pytest.raises(SystemExit, match=r"among the 44 \(D426\): \['stage-b:acc/clean-9'\]"):
        probe_split.check()
    assert not (tmp_path / 'check-passed.json').exists()


def reader_row(item, outcome, field_values):
    kind = accounting.kind_of(outcome)
    applicable = accounting.marks_that_apply(kind)
    row = {'item': item}
    for mark in accounting.ALL_MARKS:
        row[mark] = ('not_assessable' if kind in ('company figure', 'theme figure') else 'n/a') if mark == 'G' else 'holds' if mark in applicable else 'n/a'
    row.update(B=['not_a_bet'] * len(outcome['answer']['ladder']['not_judged']), W='', why='', BY='no', LQ='no')
    row.update(field_values)
    if 'yes' in field_values.values() or 'fails' in field_values.values():
        row['why'] = 'named'
    return row


@pytest.fixture
def reading(sent, tmp_path):
    """A copy of the sent probe with its reading folder and key; made-up rows for both families, every plant marked."""
    probe = tmp_path / 'probe'
    shutil.copytree(sent, probe)
    keys = tmp_path / 'keys'
    reading_split.prep(probe, keys)
    return probe, keys


def write_rows(probe, keys, change=None):
    """Both families' rows: every mark holds, BY and LQ no, each plant's field yes; `change(family, case, row)` edits a row."""
    key = json.loads((keys / 'key.json').read_text())
    outcomes = {(row['case'], row['pass']): row for row in reading_split.rows_of(probe / 'reading')}
    plants = json.loads((keys / 'plants-expected.json').read_text())
    answers = probe / 'reading' / 'readers-answers'
    answers.mkdir(exist_ok=True)
    for family in ('codex', 'claude'):
        lines = []
        for item, (case, pass_number) in key.items():
            values = {plants[case]['field']: 'yes'} if case in plants else {}
            row = reader_row(int(item), outcomes[(case, pass_number)], values)
            if change:
                change(family, case, row)
            lines.append(json.dumps(row))
        (answers / f'reader-{family}-packet-1.jsonl').write_text('\n'.join(lines) + '\n')


def test_the_reading_holds_the_yearly_items_the_c1_ladders_of_both_arms_and_two_plants(reading):
    probe, keys = reading
    rows = reading_split.rows_of(probe / 'reading')
    yearly = [row for row in rows if row['split'] and not row['case'].startswith('plant|')]
    assert len(yearly) == 2 * 3 * 2 and all(row['case'].startswith('split|') for row in yearly)
    c1 = [row for row in rows if not row['split'] and not row['case'].startswith('plant|')]
    assert {row['case'].split('|')[0] for row in c1} == {'frozen', 'split'} and len(c1) == 2 * 6 * 3
    packet = json.loads((probe / 'reading' / 'readers' / 'packet-1.json').read_text())
    assert all('split' in item for item in packet) and not any('frozen|' in json.dumps(item) or 'split|' in json.dumps(item) for item in packet)
    assert not (probe / 'reading' / 'key.json').exists() and (keys / 'key.json').exists()


def test_a_clean_reading_gives_a_lead(reading):
    probe, keys = reading
    write_rows(probe, keys)
    assert score_split.verdict(probe, keys)[0] == 'lead'


@pytest.mark.parametrize('breach', ['extra', 'missing'])
def test_a_reading_holding_an_item_its_sends_do_not_give_or_lacking_one_is_void(reading, breach):
    probe, keys = reading
    write_rows(probe, keys)
    outcomes = probe / 'reading' / 'send-2' / 'outcomes.jsonl'
    lines = outcomes.read_text().splitlines()
    if breach == 'extra':
        row = json.loads(lines[0])
        outcomes.write_text(outcomes.read_text() + json.dumps(dict(row, case=row['case'] + '-copy')) + '\n')
    else:
        outcomes.write_text('\n'.join(lines[1:]) + '\n')
    assert score_split.verdict(probe, keys)[0] == 'void'


def test_a_packet_item_given_twice_voids_the_reading(reading):
    probe, keys = reading
    write_rows(probe, keys)
    packet_path = probe / 'reading' / 'readers' / 'packet-1.json'
    packet = json.loads(packet_path.read_text())
    packet_path.write_text(json.dumps(packet + [packet[0]], ensure_ascii=False))
    assert score_split.verdict(probe, keys)[0] == 'void'


@pytest.mark.parametrize('where', ['reading row', 'packet item', 'plant mark'])
def test_an_item_changed_in_content_but_not_in_its_name_voids_the_reading(reading, where):
    """For the plant mark, the expected file is changed before the rows are written, so the readers agree with it and only the
    comparison with the plants reading_split.py builds can find it."""
    probe, keys = reading
    if where != 'plant mark':
        write_rows(probe, keys)
    if where == 'reading row':
        outcomes = probe / 'reading' / 'send-1' / 'outcomes.jsonl'
        rows = [json.loads(line) for line in outcomes.read_text().splitlines()]
        target = next(row for row in rows if row['split'] and not row['case'].startswith('plant|'))
        target['view']['question'] = target['view']['question'].replace(target['split']['asked_year'], target['split']['asked_separately'])
        outcomes.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    elif where == 'packet item':
        packet_path = probe / 'reading' / 'readers' / 'packet-1.json'
        packet = json.loads(packet_path.read_text())
        packet[0]['ladder_as_the_judge_is_shown_it']['year'] = '1999'
        packet_path.write_text(json.dumps(packet, ensure_ascii=False))
    else:
        plants_path = keys / 'plants-expected.json'
        plants = json.loads(plants_path.read_text())
        plants['plant|1']['field'] = 'LQ'
        plants_path.write_text(json.dumps(plants))
        write_rows(probe, keys)
    assert score_split.verdict(probe, keys)[0] == 'void'


def test_a_missed_plant_voids_the_reading(reading):
    probe, keys = reading
    write_rows(probe, keys, lambda family, case, row: row.update(BY='no') if family == 'claude' and case == 'plant|1' else None)
    assert score_split.verdict(probe, keys)[0] == 'void'


def test_a_base_year_settled_by_both_families_on_a_yearly_item_is_negative(reading):
    probe, keys = reading
    target = next(row['case'] for row in reading_split.rows_of(probe / 'reading') if row['split'] and not row['case'].startswith('plant|'))
    write_rows(probe, keys, lambda family, case, row: row.update(BY='yes') if case == target else None)
    decision, _, found = score_split.verdict(probe, keys)
    assert decision == 'negative' and any(case == target and 'BY' in marks for case, _, marks in found['holds'])


def test_a_split_point_without_its_third_rulings_voids_and_with_split_rulings_is_inconclusive(reading):
    probe, keys = reading
    target = next(row['case'] for row in reading_split.rows_of(probe / 'reading') if row['split'] and not row['case'].startswith('plant|'))
    write_rows(probe, keys, lambda family, case, row: row.update(LQ='yes', why='a limit') if case == target and family == 'codex' else None)
    assert score_split.verdict(probe, keys)[0] == 'void'
    key = json.loads((keys / 'key.json').read_text())
    items = [item for item, (case, _) in key.items() if case == target]
    (probe / 'reading' / 'third-reader').mkdir()
    for family, ruling in (('codex', 'yes'), ('claude', 'no')):
        (probe / 'reading' / 'third-reader' / f'split-rulings-{family}-1.jsonl').write_text(
            ''.join(json.dumps({'id': f'{item}-LQ', 'ruling': ruling}) + '\n' for item in items))
    assert score_split.verdict(probe, keys)[0] == 'inconclusive'


def test_the_third_readers_packet_holds_each_disputed_point_once_with_the_marks_hidden_and_no_plant(reading):
    probe, keys = reading
    rows = reading_split.rows_of(probe / 'reading')
    targets = [row['case'] for row in rows if row['split'] and not row['case'].startswith('plant|')][:6]
    write_rows(probe, keys, lambda family, case, row: row.update(LQ='yes', why='a limit') if case in targets and family == 'codex'
               else row.update(BY='cannot_tell') if case == 'plant|2' else None)
    count = reading_split.disputes(probe / 'reading', keys / 'key.json')
    packet = json.loads((probe / 'reading' / 'third-reader' / 'split-packet-1.json').read_text())
    key = json.loads((keys / 'key.json').read_text())
    expected = {f'{item}-LQ' for item, (case, _) in key.items() if case in targets}
    assert count == len(packet) == len(expected) and {point['id'] for point in packet} == expected
    assert all(sorted(point['marks'].values()) == ['no', 'yes'] and point['item']['split'] for point in packet)
    assert {point['marks']['a'] for point in packet} == {'yes', 'no'}           # the codex reader's mark is shown as a in some, b in others
    with pytest.raises(SystemExit, match='exists: refused'):
        reading_split.disputes(probe / 'reading', keys / 'key.json')


def test_a_c1_fault_the_frozen_arm_shares_is_not_a_veto_but_a_new_one_is(reading):
    probe, keys = reading
    topic = 'fortnight:c1/clean-9'
    write_rows(probe, keys, lambda family, case, row: row.update(R='fails', why='gap') if case.endswith(topic) else None)
    assert score_split.verdict(probe, keys)[0] == 'lead'
    write_rows(probe, keys, lambda family, case, row: row.update(R='fails', why='gap') if case == f'split|{topic}' else None)
    decision, _, found = score_split.verdict(probe, keys)
    assert decision == 'negative' and {case for case, _, _ in found['holds']} == {f'split|{topic}'}
