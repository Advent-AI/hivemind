"""Tests of D431's reading at 07-14 (DESIGN-1.6.md §3; D442's procedure, steps 3 to 6). Real stores on temporary paths, written by
the product's own store writer; the reader sessions are a fake `census_readers.run` that answers from a script. No session is run.

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider docs/research/2026-11-17-product-comparison/stage0/test_d431_reading.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import d431_reading as d431  # noqa: E402
from hivemind.views import store  # noqa: E402

DAYS = {1: '2026-07-01', 2: '2026-07-01', 3: '2026-07-01', 4: '2026-07-10', 5: '2026-07-10', 6: '2026-07-10',
        7: '2026-07-14', 8: '2026-07-14', 9: '2026-07-14', 10: '2026-07-15', 11: '2026-07-15', 12: '2026-07-15'}
YES_NO = [('Yes', None, None), ('No', None, None)]
ANSWER_CHOICE = [('Yes', None, None), ('Ruled out', None, None), ('Still open', None, None)]

Q_FABS = 'How many wafers per month will the new fabs start by end-2026?'
Q_CREDIT = 'How much credit support will NVIDIA have committed under its AI-cloud programme by its FY2027 annual report?'
Q_CAPEX26 = 'How much will the four largest AI hyperscalers spend on data-center capital expenditures in calendar 2026?'
Q_CAPEX27 = 'How much will the four largest AI hyperscalers spend on data-center capital expenditures in calendar 2027?'
Q_KYBER28 = 'Will NVIDIA launch the Kyber NVL144 rack architecture by 2028-12-31?'
Q_KYBER27 = 'Will NVIDIA begin shipping Rubin Ultra in Kyber NVL144 racks by 2027-12-31?'
Q_CHINA = 'Will Chinese authorities authorize imports of NVIDIA H200 chips by 2027-01-31?'
Q_OHIO = "Will NVIDIA sign a financial guarantee for OpenAI's Ohio data-center lease by 2027-06-30?"
Q_RUBIN = 'Will NVIDIA begin shipping its Rubin generation by 2026-12-31?'
Q_RUBIN_AGAIN = 'Will NVIDIA make first customer shipments of Vera Rubin by 2026-12-31?'


def make_store(path, system, views, judgements=(), closed=()):
    """A views store as the writers leave it: every article's processing step, every day completed at its last sequence (07-14 at 9),
    the views with their rungs, the judgements and the closings; a figure view's stored unit (the old system's view_keys row, the new
    system's checked answer `figure.unit`; USD unless given); a new-system store also holds each view's clean_ladders row.
    views: [(view_id, created_seq, question, due_day, rungs[, {'unit', 'thesis', 'period'}])]; judgements: [(view_id, seq, rung)];
    closed: [(view_id, seq)]."""
    conn = store.open_db(str(path))
    for seq, day in DAYS.items():
        store.mark_step(conn, f'gnews:item{seq:02d}', seq, 'handed_over', 'ok', None, day, day)
    for day in sorted(set(DAYS.values())):
        store.complete_day(conn, day, max(seq for seq, d in DAYS.items() if d == day), day)
    if system == 'new':
        conn.execute('create table clean_ladders (thesis_id, period not null default \'\', view_id, status, reason, reference_status, '
                     'checked_answer, outcome_record, config_checksum, article_seq, article_day)')
    for number, (view_id, seq, question, due_day, rungs, *extra) in enumerate(views, 1):
        extra = extra[0] if extra else {}
        store.create_view(conn, view_id=view_id, object_id='NVDA', object_kind='company', kind='asset', looks_at=question, question=question,
                          due_day=due_day, year=due_day[:4], rungs=[{'label': label, 'condition': f'{label}.', 'lo': lo, 'hi': hi} for label, lo, hi in rungs],
                          seq=seq, input_id=f'gnews:item{seq:02d}', created_at=f'{DAYS[seq]}T00:00:00Z')
        bounded = any(lo is not None or hi is not None for _, lo, hi in rungs)
        unit = extra.get('unit', 'USD' if bounded else 'n/a')
        if system == 'new':
            figure = {'unit': unit, 'ranges': [{'lo': lo, 'hi': hi} for _, lo, hi in rungs]} if bounded else None
            store.insert(conn, 'clean_ladders', thesis_id=extra.get('thesis', f'clean-{number}'), period=extra.get('period', ''), view_id=view_id,
                         status='ladder', checked_answer=json.dumps({'ladder': {'figure': figure}}), article_seq=seq, article_day=DAYS[seq])
        else:
            store.insert(conn, 'view_keys', view_id=view_id, measure='spend_total' if bounded else 'event', unit=unit, seq=seq)
    for view_id, seq, rung in judgements:
        store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id=f'gnews:item{seq:02d}', rung=rung, reasons='because',
                     publication_day=DAYS[seq], changed=0)
    for view_id, seq in closed:
        store.close_view(conn, view_id, 'due', 'pull', seq)
    conn.commit()
    conn.close()
    return path


def fake_reader(script):
    """A closed session that answers from the script, keyed by the question texts the prompt shows (never by an id it is not shown).
    script: match {question: {family: (match, relation)}} (default none/unrelated); match_third {(question, ruler question): {family:
    bool}}; eligibility {question: {family: (same_question, same_due)}} (default yes/yes); eligibility_third {(question, field):
    {family: ruling}}."""
    def run(family, prompt):
        packet = json.loads(prompt[prompt.rindex('\n\n[') + 2:])
        title = prompt.splitlines()[0]
        if title.startswith('# Question identity'):
            lines = [{'run': row['run'], 'id': row['id'], 'match': match, 'relation': relation, 'reason': 'one sentence'}
                     for row in packet for match, relation in [script.get('match', {}).get(row['description'], {}).get(family, ('none', 'unrelated'))]]
        elif title.startswith('# Third reader: disputed identities'):
            lines = [{'dispute': pair['dispute'], 'same': script['match_third'][(pair['opened_question']['description'], pair['reference_question'])][family],
                      'reason': 'one sentence'} for pair in packet]
        elif title.startswith('# Reading the control questions'):
            lines = [{'control': item['control'], 'same_question': same_question, 'same_due': same_due, 'why': 'one sentence'} for item in packet
                     for same_question, same_due in [script.get('eligibility', {}).get(item['judged_question']['question'], {}).get(family, ('yes', 'yes'))]]
        else:
            lines = [{'control': item['control'], 'field': field, 'ruling': script['eligibility_third'][(item['judged_question']['question'], field)][family],
                      'why': 'one sentence'} for item in packet for field in item['points_to_rule']]
        return '\n'.join(json.dumps(line) for line in lines), None
    return run


def both(match, relation='same'):
    return {'codex': (match, relation), 'claude': (match, relation)}


def read(tmp_path, monkeypatch, stores, script, prompts=None):
    """The reading as its command runs it, with the fake reader; every prompt sent is appended to `prompts` when given."""
    fake = fake_reader(script)

    def recording(family, prompt):
        if prompts is not None:
            prompts.append(prompt)
        return fake(family, prompt)
    monkeypatch.setattr(d431.census_readers, 'run', recording)
    reading = d431.Reading(stores, tmp_path / 'out', tmp_path / 'keys' / 'd431-key.json')
    return d431.read(reading)


def test_the_0714_listing_keeps_a_view_closed_before_it_and_drops_one_created_after_it(tmp_path):
    """DESIGN-1.6.md §3: every view created on or before 07-14, by created_seq up to the day's last sequence, closed views included."""
    path = make_store(tmp_path / 'views.sqlite', 'new', [('v1', 2, Q_RUBIN, '2026-12-31', ANSWER_CHOICE),
                                                         ('v2', 8, Q_CHINA, '2027-01-31', ANSWER_CHOICE),
                                                         ('v3', 11, Q_OHIO, '2027-06-30', ANSWER_CHOICE)],
                      judgements=[('v1', 3, 1), ('v2', 9, 3)], closed=[('v1', 5)])
    listed = d431.read_store({'system': 'new', 'views': path})
    assert (listed['last_sequence'], listed['from']) == (9, 'days_completed')
    assert [view['view_id'] for view in listed['listed']] == ['v1', 'v2']           # v1 closed on 07-10 kept; v3 of 07-15 left out
    assert listed['listed'][0]['state']['position'] == 1 and listed['listed'][0]['thesis'] == 'clean-1'


def test_several_same_views_the_first_created_is_judged_and_the_others_listed(tmp_path, monkeypatch):
    """D442 step 6 (iv): of several views matched SAME, the one created first is judged (not the lowest id); the others are listed."""
    path = make_store(tmp_path / 'views.sqlite', 'old', [('v7', 2, Q_RUBIN, '2026-12-31', YES_NO), ('v3', 5, Q_RUBIN_AGAIN, '2026-12-31', YES_NO)],
                      judgements=[('v7', 3, 1), ('v3', 6, 2)])
    result = read(tmp_path, monkeypatch, {'old-1': {'system': 'old', 'views': path}},
                  {'match': {Q_RUBIN: both('q07'), Q_RUBIN_AGAIN: both('q07')}})
    q07 = result['outcomes']['q07']['old-1']
    assert (q07['judged_view'], q07['outcome']) == ('v7', 'agree')                  # v3 answered No: judging it would disagree
    assert q07['listed_views'] == [{'view': 'v3', 'status': 'same'}]


def test_outcomes_take_the_first_that_applies_in_d442_order(tmp_path, monkeypatch):
    """D442 step 6, (i) to (ix) in order: not graded before matching; matching unresolved; not opened; eligibility unresolved before no
    judgement; not eligible before an agreeing answer; no judgement by 07-14; agree by the frozen scorer's rule (prod_records.outcome)."""
    path = make_store(tmp_path / 'views.sqlite', 'old', [
        ('v1', 1, Q_FABS, '2026-12-31', [('below 100,000', None, 100000.0), ('100,000 or more', 100000.0, None)]),
        ('v2', 2, Q_CREDIT, '2027-02-28', [('below $10bn', None, 1e10), ('$10bn or more', 1e10, None)]),
        ('v3', 4, Q_CAPEX26, '2027-03-31', [('below $650bn', None, 6.5e11), ('$650bn or more', 6.5e11, None)]),
        ('v4', 5, Q_KYBER28, '2028-12-31', YES_NO),
        ('v5', 7, Q_CHINA, '2027-01-31', YES_NO),
        ('v6', 8, Q_CAPEX27, '2028-03-31', [('below $800bn', None, 8e11), ('$800bn to below $1.1tn', 8e11, 1.1e12), ('$1.1tn or more', 1.1e12, None)]),
        ('v7', 9, Q_OHIO, '2027-06-30', YES_NO)],
        judgements=[('v1', 3, 1), ('v2', 3, 2), ('v4', 6, 2), ('v5', 10, 1), ('v6', 9, 2), ('v7', 9, 1)])
    script = {'match': {Q_FABS: both('q14'), Q_CREDIT: {'codex': ('q09', 'same'), 'claude': ('q09', 'narrower')}, Q_CAPEX26: both('q04'),
                        Q_KYBER28: both('q18'), Q_CHINA: both('q08'), Q_CAPEX27: both('q13'), Q_OHIO: both('q23')},
              'match_third': {(Q_CREDIT, 'q09'): {'codex': False, 'claude': True}},
              'eligibility': {Q_CAPEX26: {'codex': ('yes', 'yes'), 'claude': ('no', 'yes')}, Q_KYBER28: both('no', 'no')},
              'eligibility_third': {(Q_CAPEX26, 'same_question'): {'codex': 'no', 'claude': 'yes'}}}
    result = read(tmp_path, monkeypatch, {'old-1': {'system': 'old', 'views': path}}, script)
    got = {q: (r['old-1']['outcome'], r['old-1']['detail']) for q, r in result['outcomes'].items()
           if q in ('q14', 'q15', 'q09', 'q05', 'q04', 'q18', 'q08', 'q13', 'q23')}
    assert got == {'q14': ('not graded', 'reader B opens no view'),                  # (i), though both families matched it
                   'q15': ('not graded', 'reader B opens no view'),                  # (i) before (iii): no view opened on it
                   'q09': ('unresolved', 'matching: the third readers split'),       # (ii)
                   'q05': ("not opened in the ruler's shape", ''),                   # (iii)
                   'q04': ('unresolved', 'eligibility: the third readers split'),    # (v), though it has no judgement (vii)
                   'q18': ('opened, not eligible', 'question due'),                  # (vi), though its No agrees with reader B
                   'q08': ('no judgement', ''),                                      # (vii): judged only on 07-15
                   'q13': ('agree', ''), 'q23': ('agree', '')}                        # (ix)
    assert result['outcomes']['q18']['old-1']['answer_vs_reader_b'] == 'agree'
    assert result['agreements']['old-1'] == {'system': 'old', 'agree': 2, 'of': 7, 'questions': ['q13', 'q23'],
                                             'literal_reading_agree': 1, 'literal_reading_questions': ['q23']}


def test_a_still_open_answer_counts_no(tmp_path, monkeypatch):
    """Stage B's count (control_theses.agrees), the frozen scorer's rule for the new system: "Still open" answers no."""
    path = make_store(tmp_path / 'views.sqlite', 'new', [('v1', 2, Q_KYBER27, '2027-12-31', ANSWER_CHOICE), ('v2', 4, Q_RUBIN, '2026-12-31', ANSWER_CHOICE)],
                      judgements=[('v1', 9, 3), ('v2', 9, 3)])
    result = read(tmp_path, monkeypatch, {'new-1': {'system': 'new', 'views': path}}, {'match': {Q_KYBER27: both('q18'), Q_RUBIN: both('q07')}})
    assert result['outcomes']['q18']['new-1']['outcome'] == 'agree'                 # reader B: no
    assert result['outcomes']['q07']['new-1']['outcome'] == 'disagree'              # reader B: yes


Q_MARGIN = 'What non-GAAP gross margin will NVIDIA report for FY2027?'
Q_EPS = 'What non-GAAP earnings per share will NVIDIA report for FY2027?'
CAPEX_RUNGS = [('below $600bn', None, 6e11), ('$600bn to below $750bn', 6e11, 7.5e11), ('$750bn or more', 7.5e11, None)]


def last_packet(prompt):
    return json.loads(prompt[prompt.rindex('\n\n[') + 2:])


def test_a_figure_answer_is_withheld_when_the_units_differ_or_cannot_be_established(tmp_path, monkeypatch):
    """Council round 8, item 1: the eligibility packet carries the judged question's stored unit (old view_keys.unit, new figure.unit);
    at (viii)'s place, after (vii), a figure answer is "no comparison (unit)" when the stored unit and the ruler's differ or either cannot
    be established; no conversion; a yes/no answer is not touched."""
    old = make_store(tmp_path / 'old.sqlite', 'old', [
        ('v1', 2, Q_CAPEX26, '2027-03-31', CAPEX_RUNGS, {'unit': 'GW'}),                                          # q04 is USD
        ('v2', 4, Q_MARGIN, '2027-02-28', [('below 74%', None, 74.0), ('74% to below 76%', 74.0, 76.0), ('76% or more', 76.0, None)],
         {'unit': 'percent'}),                                                                                      # 'percent (75 means 75%)'
        ('v3', 5, Q_EPS, '2027-02-28', [('below $9', None, 9.0), ('$9 to below $10.5', 9.0, 10.5), ('$10.5 or more', 10.5, None)],
         {'unit': 'USD'}),                                                                                          # 'USD per share': not in the list
        ('v4', 7, Q_CAPEX27, '2028-03-31', CAPEX_RUNGS, {'unit': 'n/a'}),
        ('v5', 8, Q_CHINA, '2027-01-31', YES_NO)],
        judgements=[('v1', 3, 2), ('v2', 6, 2), ('v3', 6, 2), ('v5', 9, 1)])
    new = make_store(tmp_path / 'new.sqlite', 'new', [('v1', 2, Q_CAPEX26, '2027-03-31', CAPEX_RUNGS, {'unit': 'other'})], judgements=[('v1', 3, 2)])
    prompts = []
    result = read(tmp_path, monkeypatch, {'old-1': {'system': 'old', 'views': old}, 'new-1': {'system': 'new', 'views': new}},
                  {'match': {Q_CAPEX26: both('q04'), Q_MARGIN: both('q03'), Q_EPS: both('q11'), Q_CAPEX27: both('q13'), Q_CHINA: both('q08')}},
                  prompts)
    got = {(q, draw): r['outcome'] for q in ('q04', 'q03', 'q11', 'q13', 'q08') for draw, r in result['outcomes'][q].items() if 'judged_view' in r}
    assert got == {('q04', 'old-1'): d431.NO_UNIT, ('q04', 'new-1'): d431.NO_UNIT,           # GW, and the new system's "other"
                   ('q03', 'old-1'): 'agree',                                                # percent read as the ruler's percent
                   ('q11', 'old-1'): d431.NO_UNIT,                                           # the ruler's unit cannot be established
                   ('q13', 'old-1'): 'no judgement',                                         # (vii) before (viii)
                   ('q08', 'old-1'): 'agree'}                                                # a yes/no answer
    shown = {(item['judged_question']['question'], item['judged_question'].get('unit')) for prompt in prompts
             if prompt.startswith('# Reading the control questions') for item in last_packet(prompt)}
    assert {(Q_CAPEX26, 'GW'), (Q_MARGIN, 'percent'), (Q_CHINA, 'n/a')} <= shown


def test_both_systems_no_unit_words_look_the_same_in_every_packet(tmp_path, monkeypatch):
    """Council round 8: readers are blind to the system, so the new system's "other" and the old system's "n/a" (and a question with no
    stored unit) are all shown "n/a" in every packet; the output keeps the stored value."""
    rungs = CAPEX_RUNGS
    new = make_store(tmp_path / 'new.sqlite', 'new', [('v1', 2, Q_CAPEX26, '2027-03-31', rungs, {'unit': 'other'}),
                                                      ('v2', 4, Q_CHINA, '2027-01-31', ANSWER_CHOICE)], judgements=[('v1', 3, 2), ('v2', 6, 1)])
    old = make_store(tmp_path / 'old.sqlite', 'old', [('v1', 2, Q_CAPEX26, '2027-03-31', rungs, {'unit': 'n/a'}),
                                                      ('v2', 4, Q_CHINA, '2027-01-31', YES_NO)], judgements=[('v1', 3, 2), ('v2', 6, 1)])
    prompts = []
    result = read(tmp_path, monkeypatch, {'new-1': {'system': 'new', 'views': new}, 'old-1': {'system': 'old', 'views': old}},
                  {'match': {Q_CAPEX26: both('q04'), Q_CHINA: both('q08')}}, prompts)
    shown = [item['judged_question']['unit'] for prompt in set(prompts) if prompt.startswith('# Reading the control questions')
             for item in last_packet(prompt)]                               # each family gets the same packet: read it once
    assert sorted(shown) == ['n/a'] * 4                                     # two systems, a figure and an event each
    assert result['outcomes']['q04']['new-1']['unit'] == 'other' and result['outcomes']['q04']['old-1']['unit'] == 'n/a'


def strings_in(value):
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings_in(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings_in(v)]
    return [value] if isinstance(value, str) else []


def test_no_packet_carries_a_view_or_thesis_id(tmp_path, monkeypatch):
    """D442 step 4, readers blind; council round 8, item 3: the matching and eligibility packets name no view id (a split child's
    v0<number><year> would name the system) and no thesis id."""
    path = make_store(tmp_path / 'views.sqlite', 'new', [('v3', 2, Q_CAPEX26, '2027-03-31', CAPEX_RUNGS, {'thesis': 'clean-3'}),
                                                         ('v0122027', 4, Q_CAPEX27, '2028-03-31', CAPEX_RUNGS, {'thesis': 'clean-12', 'period': '2027'})],
                      judgements=[('v3', 6, 2), ('v0122027', 6, 2)])
    prompts = []
    read(tmp_path, monkeypatch, {'new-1': {'system': 'new', 'views': path}}, {'match': {Q_CAPEX26: both('q04'), Q_CAPEX27: both('q13')}}, prompts)
    kinds = {prompt.splitlines()[0] for prompt in prompts}
    assert {'# Question identity reading for a measured run (read-only)', '# Reading the control questions (read-only)'} <= kinds
    for prompt in prompts:
        named = strings_in(last_packet(prompt))
        assert not [s for s in named if s in ('v3', 'v0122027', 'clean-3', 'clean-12') or s.startswith('clean-')]
        assert 'v0122027' not in prompt and 'clean-12' not in prompt


def test_the_command_reads_the_stores_the_run_records_name_and_refuses_a_changed_one(tmp_path, monkeypatch):
    """DESIGN-1.6.md §0: each store is the one its run record names (the judge's completed attempt) and must carry the eligibility
    check's fingerprint; a store changed since is refused, and a run that is not eligible is read only as a diagnostic."""
    monkeypatch.setattr(d431.mapping, 'DRAWS', ['new-1', 'old-1'])
    root = tmp_path / 'run'
    new_store, old_store = root / 'new-1/judge/draw-new-1-redo/views.sqlite', root / 'old-1/prod/views.sqlite'
    stopped = root / 'new-1/judge/draw-new-1/views.sqlite'                  # the stopped first attempt leaves its own store
    for path in (new_store, old_store, stopped):
        path.parent.mkdir(parents=True)
    make_store(stopped, 'new', [('v1', 2, Q_RUBIN_AGAIN, '2026-12-31', ANSWER_CHOICE)])
    make_store(new_store, 'new', [('v1', 2, Q_RUBIN, '2026-12-31', ANSWER_CHOICE)])
    make_store(old_store, 'old', [('v1', 2, Q_RUBIN, '2026-12-31', YES_NO)])
    (root / 'new-1/run.json').write_text(json.dumps({'state': 'complete', 'components': {'judge': {'state': 'completed', 'folder': 'judge'}}}))
    (root / 'new-1/judge/run.json').write_text(json.dumps({'new-1': {'state': 'complete', 'attempts': [
        {'folder': 'draw-new-1', 'stopped': 'ReadTimeout'}, {'folder': 'draw-new-1-redo'}]}}))
    (root / 'old-1/run.json').write_text(json.dumps({'state': 'complete', 'components': {'prod': {'state': 'completed', 'folder': 'prod'}}}))
    fingerprints = {'new-1': new_store, 'old-1': old_store}
    eligibility = {'eligible': True, 'draws': {draw: {'stores': {'views.sqlite': {'sha256': d431.eligibility_tool.sha256(path)}}}
                                               for draw, path in fingerprints.items()}}
    (tmp_path / 'eligibility.json').write_text(json.dumps(eligibility))
    assert d431.stores_of_run(root, tmp_path / 'eligibility.json', False) == {'new-1': {'system': 'new', 'views': new_store},
                                                                            'old-1': {'system': 'old', 'views': old_store}}
    (tmp_path / 'ineligible.json').write_text(json.dumps(dict(eligibility, eligible=False, problems=['launches span 2:00:00'])))
    try:
        d431.stores_of_run(root, tmp_path / 'ineligible.json', False)
    except SystemExit as refusal:
        assert 'not eligible' in str(refusal)
    else:
        raise AssertionError('an ineligible run was read as a release reading')
    assert set(d431.stores_of_run(root, tmp_path / 'ineligible.json', True)) == {'new-1', 'old-1'}
    conn = store.open_db(str(old_store))                     # the old store gains a row after the eligibility check
    store.complete_day(conn, '2026-07-16', 13, '2026-07-16')
    conn.commit()
    conn.close()
    try:
        d431.stores_of_run(root, tmp_path / 'eligibility.json', False)
    except SystemExit as refusal:
        assert 'changed since' in str(refusal)
    else:
        raise AssertionError('a store changed after the eligibility check was read')


def test_a_figure_rung_with_no_bound_is_no_comparison(tmp_path, monkeypatch):
    """D442 step 6 (viii), in both systems: the chosen figure rung has neither bound, so no comparison is made (the frozen scorer would
    count it as agreeing)."""
    rungs = [('below $600bn', None, 6e11), ('$600bn or more', 6e11, None), ('Not settled', None, None)]
    new = make_store(tmp_path / 'new.sqlite', 'new', [('v1', 4, Q_CAPEX26, '2027-03-31', rungs)], judgements=[('v1', 9, 3)])
    old = make_store(tmp_path / 'old.sqlite', 'old', [('v1', 4, Q_CAPEX26, '2027-03-31', rungs)], judgements=[('v1', 9, 3)])
    result = read(tmp_path, monkeypatch, {'new-1': {'system': 'new', 'views': new}, 'old-1': {'system': 'old', 'views': old}},
                  {'match': {Q_CAPEX26: both('q04')}})
    assert {draw: r['outcome'] for draw, r in result['outcomes']['q04'].items()} == {'new-1': 'no comparison', 'old-1': 'no comparison'}
