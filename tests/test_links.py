"""Reading links between number questions (D694, D695): each test names the row of
docs/research/2026-11-20-production-readiness/dependency-design/DESIGN.md it proves (section and test number of its §11).
Real ledgers on temporary paths; a scripted Jev transport and a scripted judge; no paid service."""
import dataclasses
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys

import pytest

from test_jev_matching import scripted
from test_keyed_views import ITEM, KEY, RUNGS, UNIVERSE, candidate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, extraction, model  # noqa: E402
from hivemind.views import judging, links, matching, store, writing  # noqa: E402
from hivemind.views import round as rounds  # noqa: E402

V118 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v118.json'))
V119 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v119.json'))
V120 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v120.json'))
CFG = dataclasses.replace(V119, collision=None)                       # Jev alone: the collision judge is not under test here
CFG_JEV = dataclasses.replace(V118, collision=None)
TOTAL = dict(KEY, measure='total_revenue', scope='', scope_source='none')      # as the product stores a total (view_keys: scope_source none)
SCALE = 1.2                                                           # the total's ladder sits above the segment's
TOTAL_RUNGS = [dict(r, lo=None if r['lo'] is None else r['lo'] * SCALE, hi=None if r['hi'] is None else r['hi'] * SCALE) for r in RUNGS]
DAY_BEFORE = '2026-05-19'


def rising(rungs):
    """The same ladder stored with its values rising from the first rung (labels kept in place)."""
    bounds = [(r['lo'], r['hi']) for r in rungs][::-1]
    return [dict(r, lo=lo, hi=hi) for r, (lo, hi) in zip(rungs, bounds)]


def ledger(tmp_path, views):
    """A ledger holding `views` [(view_id, key, rungs, question)] created at seq 1 and open at the start of ITEM's day."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    for view_id, key, rungs, question in views:
        c = candidate('x', rungs=rungs, question=question, looks_at=question, **key)
        store.create_view(conn, view_id=view_id, object_id='NVDA', object_kind='company', kind='asset', looks_at=question, question=question,
                          due_day='2027-02-25', year='FY2027', rungs=rungs, seq=1, input_id='seed', created_at='2026-05-19T00:00:00')
        store.add_key(conn, view_id, c, 1)
        evidence_id = f'e{view_id[1:]}'
        store.add_evidence(conn, evidence_id=evidence_id, quote=f'{question} statement', one_line=question, speaker='NVIDIA', original_who='NVIDIA',
                           original_day='2026-05-19', tier='fact', event_time='', seq=1, input_id='seed')
        store.add_source(conn, evidence_id, 'seed', 'T4', '2026-05-19', '', 1)
        store.link(conn, evidence_id, view_id, 1)
    store.insert(conn, 'days_completed', day=DAY_BEFORE, seq=1, at='2026-05-19T23:59:59')
    conn.commit()
    return conn


def handover_of(*candidates):
    evidence = [{'id': f'h{c["id"]}', 'quote': f'{c["question"]} figure', 'one_line': c['question'], 'speaker': 'NVIDIA', 'original_who': 'NVIDIA',
                 'original_day': '2026-05-20', 'tier': 'fact', 'event_time': '', 'location': '', 'links': [c['id']]} for c in candidates]
    candidates = [dict(c, evidence_ids=[f'h{c["id"]}']) for c in candidates]
    return extraction.Handover(evidence, candidates, [], 0, '', True, 0.0)


def checked_new(*ids, outcome='new', target=None):
    return matching.Checked({cid: (outcome, target, []) for cid in ids}, {}, [], {})


def recording(script):
    sent = []
    inner = scripted(script)

    def transport(request):
        sent.append(request)
        return inner(request)
    transport.sent = sent
    return transport


def link_questions(sent):
    return [qid for request in sent for qid in request['questions'] if qid.startswith(('reads__', 'sign__'))]


# ---------- §5, test 1: the typed direction and the label ----------

def test_typed_direction_reads_bounds_in_rung_order_and_never_prose():
    assert links.typed_direction(RUNGS) == -1 and links.typed_direction(rising(RUNGS)) == 1
    shuffled = [RUNGS[0], RUNGS[2], RUNGS[1], RUNGS[3], RUNGS[4]]
    assert links.typed_direction(shuffled) is None
    overlapping = [dict(r) for r in RUNGS]
    overlapping[1]['lo'] = 260e9                                       # rung 2 reaches below rung 3's top
    assert links.typed_direction(overlapping) is None
    open_inner = [dict(r) for r in RUNGS]
    open_inner[2]['lo'] = None
    assert links.typed_direction(open_inner) is None
    assert links.typed_direction([{'label': r['label'], 'condition': r['condition']} for r in RUNGS]) is None   # prose only


def test_the_label_follows_the_sign_and_both_ladders():
    assert links.label_for(RUNGS, TOTAL_RUNGS, links.TOGETHER) == 'first_is_bullish'          # the worked case (old-2 07-10)
    assert links.label_for(RUNGS, TOTAL_RUNGS, links.OPPOSITE) == 'last_is_bullish'
    assert links.label_for(rising(RUNGS), TOTAL_RUNGS, links.TOGETHER) == 'last_is_bullish'    # the reader's values rise, its bullish end first
    assert links.label_for(RUNGS, rising(TOTAL_RUNGS), links.TOGETHER) == 'last_is_bullish'
    reversed_successor = list(reversed(RUNGS))                         # stored reversed with its labels: bullish end last, values rising
    assert links.typed_direction(reversed_successor) == 1 and links.favourable_end(reversed_successor) == 'last'
    assert links.label_for(reversed_successor, TOTAL_RUNGS, links.TOGETHER) == 'first_is_bullish'
    assert links.label_for(RUNGS, TOTAL_RUNGS, links.NO_SIGN) is None


# ---------- §1–§2, test 2: selection ----------

def test_an_existing_segment_reads_a_newly_opened_total(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', looks_at='total revenue', **TOTAL)
    transport = recording({'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.8)})
    proposed, record = links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(total), checked_new('c1'),
                                    matching.Lists({'c1': ['v1']}, {}), [], transport=transport)
    assert proposed == [{'reader': 'v1', 'read': 'c1', 'candidate': 'c1', 'thesis': 'v1', 'direction': links.THESIS_READS, 'sign': links.TOGETHER}]
    assert [c['stage'] for c in record['calls']] == ['reads', 'sign']
    assert transport.sent[1]['questions']['sign__v1']['instructions'].startswith(links.SIGN_INSTRUCTIONS[links.THESIS_READS])


def test_one_sign_job_holds_both_reading_directions(tmp_path):
    conn = ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?'),
                             ('v2', dict(KEY, scope='Networking'), RUNGS, 'Networking revenue FY2027?')])
    dc = candidate('c1', question='Data Center revenue FY2027?')
    transport = recording({'reads__v1': (links.CANDIDATE_READS, 0.8), 'reads__v2': (links.THESIS_READS, 0.7),
                           'sign__v1': (links.TOGETHER, 0.8), 'sign__v2': (links.OPPOSITE, 0.6)})
    proposed, _ = links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(dc), checked_new('c1'),
                               matching.Lists({'c1': ['v1', 'v2']}, {}), [], transport=transport)
    signs = transport.sent[1]['questions']
    assert signs['sign__v1']['instructions'].startswith(links.SIGN_INSTRUCTIONS[links.CANDIDATE_READS])
    assert signs['sign__v2']['instructions'].startswith(links.SIGN_INSTRUCTIONS[links.THESIS_READS])
    assert [(p['reader'], p['read'], p['sign']) for p in proposed] == [('c1', 'v1', links.TOGETHER), ('v2', 'c1', links.OPPOSITE)]


@pytest.mark.parametrize('script', [{'reads__v1': (links.NEITHER, 0.9)},
                                    {'reads__v1': (links.THESIS_READS, 0.45)},
                                    {'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.NO_SIGN, 0.8)},
                                    {'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.4)}])
def test_no_link_without_a_direction_and_a_sign_at_the_threshold(tmp_path, script):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', **TOTAL)
    proposed, _ = links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(total), checked_new('c1'),
                               matching.Lists({'c1': ['v1']}, {}), [], transport=recording(script))
    assert proposed == []


@pytest.mark.parametrize('change', ['theme', 'two_rungs', 'event', 'merged', 'thesis_event'])
def test_pairs_outside_number_questions_are_not_asked(tmp_path, change):
    yes_no = [{'label': 'Yes', 'condition': 'yes', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'no', 'lo': None, 'hi': None}]
    thesis_key = dict(KEY, measure='event', event_type='deployment') if change == 'thesis_event' else KEY
    conn = ledger(tmp_path, [('v1', thesis_key, RUNGS, 'Data Center revenue FY2027?')])
    over = {'theme': {'kind': 'theme'}, 'two_rungs': {'rungs': yes_no}, 'event': {'measure': 'event', 'event_type': 'deployment'}}.get(change, {})
    total = candidate('c1', question='Total revenue FY2027?', **dict(TOTAL, **{'rungs': TOTAL_RUNGS, **over}))
    checked = checked_new('c1', outcome='merge', target='v1') if change == 'merged' else checked_new('c1')
    transport = recording({})
    proposed, _ = links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(total), checked,
                               matching.Lists({'c1': ['v1']}, {}), [], transport=transport)
    assert proposed == [] and link_questions(transport.sent) == []


def test_two_candidates_of_one_question_are_asked_once(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    first = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', **TOTAL)
    second = candidate('c2', rungs=TOTAL_RUNGS, question='Total company revenue in FY2027?', **TOTAL)
    transport = recording({'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.8)})
    links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(first, second), checked_new('c1', 'c2'),
                 matching.Lists({'c1': ['v1'], 'c2': ['v1']}, {}), [], transport=transport)
    assert link_questions(transport.sent) == ['reads__v1', 'sign__v1']


# ---------- §4, test 3: the graph and the correction ----------

def stored_link(conn, reader, read):
    store.insert(conn, 'dependencies', view_id=reader, depends_on=read, wait_chain_view_id='', wait_year='', direction='first_is_bullish', seq=1, kind=links.KIND)
    conn.commit()


def two_totals(tmp_path):
    return ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?'), ('v2', dict(TOTAL, period_start='2027-02-01', period_end='2028-01-31'), TOTAL_RUNGS, 'Total revenue FY2028?')])


def test_a_circle_through_a_stored_link_is_corrected_once(tmp_path):
    conn = two_totals(tmp_path)
    stored_link(conn, 'v2', 'v1')                                     # v2 reads v1
    dc = candidate('c1', question='Data Center revenue FY2027?')
    # c1 reads v2 and v1 reads c1 close c1 -> v2 -> v1 -> c1; each correction answers neither
    first = recording({'reads__v1': (links.THESIS_READS, 0.8), 'reads__v2': (links.CANDIDATE_READS, 0.8),
                       'sign__v1': (links.TOGETHER, 0.8), 'sign__v2': (links.TOGETHER, 0.8)})
    correction = scripted({'reads__v1': (links.NEITHER, 0.9), 'reads__v2': (links.NEITHER, 0.9)})

    def transport(request):
        if any('read itself' in q['instructions'] for q in request['questions'].values()):
            first.sent.append(request)
            return correction(request)
        return first(request)
    transport.sent = first.sent
    proposed, record = links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(dc), checked_new('c1'),
                                    matching.Lists({'c1': ['v1', 'v2']}, {}), [], transport=transport)
    corrections = [r for r in record['corrections'] if 'rejected' in r]
    assert {r['thesis'] for r in corrections} == {'v1', 'v2'} and all(r['path'][0] == r['path'][-1] for r in corrections)
    assert proposed == [] and links.circles(conn, proposed) == []
    correction_requests = [q for request in transport.sent for q in request['questions'].values() if 'read itself' in q['instructions']]
    assert correction_requests and all(len(q['criteria']) == 2 for q in correction_requests)        # the offending direction removed


def test_a_circle_through_two_openings_is_found_and_a_persistent_one_fails(tmp_path):
    conn = ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?'), ('v2', dict(KEY, scope='Networking'), RUNGS, 'Networking revenue FY2027?')])
    a = candidate('c1', question='Data Center revenue FY2027?')
    b = candidate('c2', question='Gaming revenue FY2027?', **dict(KEY, scope='Gaming'))
    # c1 -> v1 -> c2 -> v2 -> c1, no stored path; every correction flips the pair, which closes the reverse circle
    script = {('Data Center', 'reads__v1'): (links.CANDIDATE_READS, 0.8), ('Data Center', 'reads__v2'): (links.THESIS_READS, 0.8),
              ('Gaming', 'reads__v1'): (links.THESIS_READS, 0.8), ('Gaming', 'reads__v2'): (links.CANDIDATE_READS, 0.8),
              'sign__v1': (links.TOGETHER, 0.8), 'sign__v2': (links.TOGETHER, 0.8)}
    flipped = dict(script)

    def transport(request):
        if any('read itself' in q['instructions'] for q in request['questions'].values()):
            answers = {}
            for qid, q in request['questions'].items():
                remaining = [k for k in q['criteria'] if k != links.NEITHER][0]
                answers[qid] = {'type': 'choice', 'choice': remaining, 'confidence': 0.8,
                                'probabilities': {k: (0.8 if k == remaining else 0.2) for k in q['criteria']}}
            return {'model': request['model'], 'answers': answers, 'usage': {'input_tokens': 10, 'output_tokens': 5}}
        return scripted(flipped)(request)
    with pytest.raises(links.Refused) as refused:
        links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(a, b), checked_new('c1', 'c2'),
                     matching.Lists({'c1': ['v1', 'v2'], 'c2': ['v1', 'v2']}, {}), [], transport=transport)
    assert refused.value.record['error'].startswith('persistent cycle')


def test_a_store_with_an_unbound_wait_is_refused_and_a_bound_wait_counts_through_its_target(tmp_path):
    conn = two_totals(tmp_path)
    store.insert(conn, 'dependencies', view_id='v1', depends_on='', wait_chain_view_id='v2', wait_year='FY2029', direction='same', seq=1)
    conn.commit()
    dc = candidate('c1', question='Data Center revenue FY2027?')
    with pytest.raises(links.Refused):
        links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(dc), checked_new('c1'),
                     matching.Lists({'c1': ['v1']}, {}), [], transport=recording({}))
    dependency_id = conn.execute('select dependency_id from dependencies').fetchone()[0]
    store.insert(conn, 'dependency_resolutions', dependency_id=dependency_id, resolved_to='v2', reason='waited year created', seq=1)
    conn.commit()
    assert links.unbound_waits(conn) == 0
    assert links.circles(conn, [{'reader': 'v2', 'read': 'c1'}, {'reader': 'c1', 'read': 'v1'}]) != []   # v1 -> v2 through the bound wait


# ---------- §4, test 4: the writer ----------

def write_with(conn, proposed, *handover_candidates, seq=2):
    conn.execute('begin immediate')
    written = writing.write(conn, UNIVERSE, seq, ITEM, handover_of(*handover_candidates), checked_new(*[c['id'] for c in handover_candidates]), {},
                            proposed_links=proposed)
    conn.commit()
    return written


def test_an_existing_question_gains_a_reads_link_and_is_judged_that_day(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', **TOTAL)
    written = write_with(conn, [{'reader': 'v1', 'read': 'c1', 'candidate': 'c1', 'thesis': 'v1', 'direction': links.THESIS_READS, 'sign': links.TOGETHER}], total)
    new = written.new_views['c1']
    row = conn.execute('select view_id, depends_on, direction, kind, seq from dependencies').fetchone()
    assert tuple(row) == ('v1', new, 'first_is_bullish', 'reads', 2)
    assert 'v1' in written.changed_views and written.links[0]['label'] == 'first_is_bullish'


def test_a_closed_endpoint_refuses_the_whole_write(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    store.insert(conn, 'view_switches', view_id='v1', open=0, reason='closed', by_whom='test', after_seq=1)
    conn.commit()
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', **TOTAL)
    with pytest.raises(writing.WriteConflict):
        write_with(conn, [{'reader': 'v1', 'read': 'c1', 'candidate': 'c1', 'thesis': 'v1', 'direction': links.THESIS_READS, 'sign': links.TOGETHER}], total)
    conn.rollback()
    assert conn.execute("select count(*) from views where view_id != 'v1'").fetchone()[0] == 0


def test_a_circle_closed_by_a_later_insertion_rolls_back_the_whole_write(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', **TOTAL)
    proposed = [{'reader': 'v1', 'read': 'c1', 'candidate': 'c1', 'thesis': 'v1', 'direction': links.THESIS_READS, 'sign': links.TOGETHER},
                {'reader': 'c1', 'read': 'v1', 'candidate': 'c1', 'thesis': 'v1', 'direction': links.CANDIDATE_READS, 'sign': links.TOGETHER}]
    with pytest.raises(writing.WriteConflict, match='circle'):
        write_with(conn, proposed, total)
    # the writer's savepoint already undid the new view and the first link, inside the still open transaction
    assert conn.in_transaction
    assert conn.execute('select count(*) from dependencies').fetchone()[0] == 0
    assert conn.execute("select count(*) from views where view_id != 'v1'").fetchone()[0] == 0
    conn.rollback()


# ---------- §4, test 5: filing ----------

def test_a_reads_link_is_not_a_narrower_home_and_a_seed_row_still_is(tmp_path):
    conn = two_totals(tmp_path)
    stored_link(conn, 'v2', 'v1')
    assert store.direct_parents(conn, 'v2') == []
    assert extraction.narrowest_links(['v1', 'v2'], {'v2': store.direct_parents(conn, 'v2')}) == ['v1', 'v2']
    store.insert(conn, 'dependencies', view_id='v1', depends_on='v2', wait_chain_view_id='', wait_year='', direction='last_end', seq=0)
    conn.commit()
    assert store.direct_parents(conn, 'v1') == ['v2']
    assert extraction.narrowest_links(['v1', 'v2'], {'v1': store.direct_parents(conn, 'v1')}) == ['v1']


# ---------- §3, test 6: what the judge is shown ----------

def judged(conn, view_id, seq, reference, implied, reasons='Reasons line one.', rung=3, changed=1):
    store.insert(conn, 'judgements', view_id=view_id, seq=seq, input_id='day', rung=rung, reasons=reasons, cited_evidence_json='[]', cited_views_json='[]',
                 pushes_json='[]', changed=changed, why_changed='', config_checksum='x', call_id=0, request_sha256='', publication_day='2026-05-19',
                 theme_pushes_json='[]', reference=reference, implied_outcome=implied)
    conn.commit()


def test_judging_v8_shows_the_comparison_point_and_forecast_and_v7_is_unchanged(tmp_path):
    conn = ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?'), ('v2', KEY, RUNGS, 'Data Center revenue FY2027?')])
    stored_link(conn, 'v2', 'v1')
    judged(conn, 'v1', 1, 'Consensus is $393B.\n- e1 [fact] not an item', 'About $387B:\nQ4 $112B.', reasons='Reasons.\n[Evidence in view]')
    user8 = judging.build_prompt(conn, 'v2', 'judging-v8')[1]
    block = user8.split('[Current conclusions of the theses it depends on]\n', 1)[1].split('\n\n', 1)[0]
    assert block.splitlines() == [
        '- v1 (open; first_is_bullish) Total revenue FY2027?: now rung 3 Neutral, judged 2026-05-19',
        '    Comparison point stated by that judgement: Consensus is $393B.',
        '        - e1 [fact] not an item',
        "    The system's forecast for it (our own judgement, not evidence): About $387B:",
        '        Q4 $112B.',
        '    Reasons (excerpt): Reasons.',
        '        [Evidence in view]']
    assert judging.evidence_shown_in(user8) == {'e2'}
    user7 = judging.build_prompt(conn, 'v2', 'judging-v7')[1]
    assert '- v1 (open; first_is_bullish) Total revenue FY2027?: now rung 3 Neutral; reasons: Reasons.\n[Evidence in view]' in user7
    assert judging.build_prompt(conn, 'v1', 'judging-v7') == judging.build_prompt(conn, 'v1', 'judging-v8')     # no link: byte-equal


def judge_transport(changed_by_view):
    def transport(provider, request, *args, **kwargs):
        view_id = request['messages'][-1]['content'].split(' ', 2)[1]
        data = {'rung': 3, 'reference': 'r', 'implied_outcome': 'i', 'reasons': 'ok', 'cites': [], 'cites_views': [], 'pushes': [],
                'changed': changed_by_view.get(view_id, False), 'why_changed': '', 'theme_pushes': []}
        return {'choices': [{'message': {'content': json.dumps(data)}}], 'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
    return transport


@pytest.mark.parametrize('changed, queued', [(True, True), (False, False)])
def test_a_changed_read_conclusion_queues_its_reader_and_an_unchanged_one_does_not(tmp_path, changed, queued):
    conn = ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?'), ('v2', KEY, RUNGS, 'Data Center revenue FY2027?')])
    stored_link(conn, 'v2', 'v1')
    judged(conn, 'v1', 1, 'old point', 'old forecast')
    judged(conn, 'v2', 1, 'r', 'i')
    results = judging.round_of_judgements(model.Archive(str(tmp_path / 'a.sqlite')), V119, conn, ['v1'], 5, {'input_id': 'day:2026-05-20', 'publication_day': '2026-05-20'},
                                          transport=judge_transport({'v1': changed}))
    assert [r['view_id'] for r in results] == (['v1', 'v2'] if queued else ['v1'])


# ---------- §0, test 7: entry points ----------

def scripts_replay():
    spec = importlib.util.spec_from_file_location('scripts_replay_under_test', os.path.join(ROOT, 'scripts', 'replay.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_links_engine_loads_but_ordinary_launchers_refuse_it():
    assert V119.matching.engine == links.ENGINE and V119.rejudging.prompt_version == 'judging-v8'
    for version in (V119, V120):
        with pytest.raises(SystemExit):
            scripts_replay().refuse_links_engine(version)
    scripts_replay().refuse_links_engine(V118)


# ---------- WORDING-V2.md §5 (D705): the link question version ----------

def test_the_question_version_is_read_from_the_matching_setting_and_refused_when_unknown(tmp_path):
    assert (V119.matching.link_questions, V120.matching.link_questions, V118.matching.link_questions) == ('links-v1', 'links-v2', '')
    assert config.LINK_QUESTIONS == tuple(links.QUESTION_SETS)
    raw = json.load(open(os.path.join(ROOT, 'poc', 'config', 'poc-v120.json')))
    refused = {'an unknown version': dict(raw, matching=dict(raw['matching'], link_questions='links-v9')),
               'the field under the jev engine': dict(raw, matching=dict(raw['matching'], engine='jev')),
               'null under the jev engine': dict(raw, matching=dict(raw['matching'], engine='jev', link_questions=None)),
               'null under jev-links (never a silent first version)': dict(raw, matching=dict(raw['matching'], link_questions=None)),
               'the field in another setting': dict(raw, rejudging=dict(raw['rejudging'], engine='jev-links', link_questions='links-v2'))}
    for index, (case, broken) in enumerate(refused.items()):
        path = tmp_path / f'refused-{index}.json'
        path.write_text(json.dumps(broken))
        with pytest.raises(config.ConfigError):
            config.load(str(path))
            pytest.fail(f'accepted: {case}')


def test_version_two_asks_its_own_criteria_at_every_stage_and_version_one_keeps_its_own(tmp_path):
    for cfg, (reads, sign) in ((dataclasses.replace(V120, collision=None), (links.READS_V2, links.SIGN_V2)), (CFG, (links.READS, links.SIGN))):
        folder = tmp_path / cfg.version
        folder.mkdir()
        conn = two_totals(folder)
        stored_link(conn, 'v2', 'v1')                                     # as the circle test: a first answer, a correction, no link
        first = recording({'reads__v1': (links.THESIS_READS, 0.8), 'reads__v2': (links.CANDIDATE_READS, 0.8),
                           'sign__v1': (links.TOGETHER, 0.8), 'sign__v2': (links.TOGETHER, 0.8)})
        correction = scripted({'reads__v1': (links.NEITHER, 0.9), 'reads__v2': (links.NEITHER, 0.9)})

        def transport(request):
            if any('read itself' in q['instructions'] for q in request['questions'].values()):
                first.sent.append(request)
                return correction(request)
            return first(request)
        links.choose(model.Archive(str(folder / 'a.sqlite')), cfg, conn, handover_of(candidate('c1', question='Data Center revenue FY2027?')),
                     checked_new('c1'), matching.Lists({'c1': ['v1', 'v2']}, {}), [], transport=transport)
        asked = [(qid, q) for request in first.sent for qid, q in request['questions'].items()]
        assert {qid.split('__')[0] for qid, _ in asked} == {'reads', 'sign'} and any('read itself' in q['instructions'] for _, q in asked)
        for qid, q in asked:
            expected = reads if qid.startswith('reads__') else sign
            assert q['criteria'] == {k: v for k, v in expected.items() if k in q['criteria']} and len(q['criteria']) >= 2


def test_an_ordinary_replay_refuses_a_harness_only_ledger_before_routing(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    conn.execute('create table harness_only (name text, day text)')
    conn.commit()
    conn.close()
    before = os.path.getmtime(tmp_path / 'views.sqlite')
    run = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'replay.py'), '--from', '2026-05-20', '--until', '2026-05-20',
                          '--views', str(tmp_path / 'views.sqlite'), '--archive', str(tmp_path / 'archive.sqlite'), '--workers', '1'],
                         capture_output=True, text=True, cwd=str(tmp_path))
    assert run.returncode != 0 and 'harness-only' in run.stderr
    assert os.path.getmtime(tmp_path / 'views.sqlite') == before and not (tmp_path / 'archive.sqlite').exists()


# ---------- §1, tests 2 and 8: the link step inside the article, and its record ----------

def run_article(tmp_path, cfg, script, conn):
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', looks_at='total revenue', **TOTAL)
    transport = recording(dict({'rel__v1': ('different', 0.9)}, **script))
    item = dict(ITEM, text='Total revenue guidance.', publication_day='2026-05-20')
    result = rounds.run(conn, model.Archive(str(tmp_path / 'archive.sqlite')), cfg, UNIVERSE, item, 2, transport=transport,
                        extractor=lambda *args, **kwargs: handover_of(total))
    return result, transport


def test_the_article_writes_the_link_and_records_proposed_then_committed(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    result, transport = run_article(tmp_path, CFG, {'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.8)}, conn)
    assert result.failed == ''
    assert [tuple(r) for r in conn.execute('select view_id, kind from dependencies')] == [('v1', 'reads')]
    rows = conn.execute('select attempt_id, status, config_checksum, record_json from link_selections order by id').fetchall()
    assert [(r[0], r[1]) for r in rows] == [(ITEM['input_id'] + '#1', 'proposed'), (ITEM['input_id'] + '#1', 'committed')]
    assert rows[0][2] == CFG.checksum and json.loads(rows[1][3])['links'][0]['label'] == 'first_is_bullish'
    written = json.loads(conn.execute("select reason from processing_steps where step='written'").fetchone()[0])
    assert 'v1' in written['changed']


def test_under_the_jev_engine_no_link_question_is_asked(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    result, transport = run_article(tmp_path, CFG_JEV, {'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.8)}, conn)
    assert result.failed == '' and link_questions(transport.sent) == []
    assert conn.execute('select count(*) from dependencies').fetchone()[0] == 0
    assert conn.execute('select count(*) from link_selections').fetchone()[0] == 0


def test_a_jev_failure_after_an_answered_job_records_each_job_and_the_failing_one(tmp_path):
    """§1 step 6 (council R round 9): the first job answered, the second fails, the third not asked."""
    conn = ledger(tmp_path, [('v1', TOTAL, TOTAL_RUNGS, 'Total revenue FY2027?')])
    parts = [candidate('c1', question='Data Center revenue FY2027?'), candidate('c2', question='Gaming revenue FY2027?', scope='Gaming'),
             candidate('c3', question='Networking revenue FY2027?', scope='Networking')]
    answered = scripted({'reads__v1': (links.NEITHER, 0.9)})
    count = []

    def transport(request):
        count.append(1)
        if len(count) == 2:
            raise model.TransportError('Jev transport failed: URLError')
        return answered(request)
    with pytest.raises(links.Refused) as refused:
        links.choose(model.Archive(str(tmp_path / 'a.sqlite')), CFG, conn, handover_of(*parts), checked_new('c1', 'c2', 'c3'),
                     matching.Lists({'c1': ['v1'], 'c2': ['v1'], 'c3': ['v1']}, {}), [], transport=transport)
    calls = refused.value.record['calls']
    assert [c['status'] for c in calls] == ['answered', 'failed', 'not asked'] and isinstance(calls[0]['call_id'], int)
    assert refused.value.record['failed_request_sha256'] == calls[1]['request_sha256']


def test_a_jev_failure_records_failed_alone_with_the_failing_request(tmp_path):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    total = candidate('c1', rungs=TOTAL_RUNGS, question='Total revenue FY2027?', looks_at='total revenue', **TOTAL)
    inner = scripted({'rel__v1': ('different', 0.9)})

    def transport(request):
        if any(qid.startswith('reads__') for qid in request['questions']):
            raise model.TransportError('Jev transport failed: URLError')
        return inner(request)
    item = dict(ITEM, text='Total revenue guidance.')
    result = rounds.run(conn, model.Archive(str(tmp_path / 'archive.sqlite')), CFG, UNIVERSE, item, 2, transport=transport,
                        extractor=lambda *args, **kwargs: handover_of(total))
    assert result.failed.startswith('linking: link question failed')
    rows = conn.execute('select status, record_json from link_selections').fetchall()
    assert [r[0] for r in rows] == ['failed']
    call = json.loads(rows[0][1])['calls'][0]
    assert call['stage'] == 'reads' and len(call['request_sha256']) == 64 and 'error' in json.loads(rows[0][1])


def test_a_write_conflict_after_the_proposal_records_proposed_then_failed(tmp_path, monkeypatch):
    conn = ledger(tmp_path, [('v1', KEY, RUNGS, 'Data Center revenue FY2027?')])
    monkeypatch.setattr(links, 'label_for', lambda *args: None)           # the stored rungs give no label: the write refuses
    result, _ = run_article(tmp_path, CFG, {'reads__v1': (links.THESIS_READS, 0.8), 'sign__v1': (links.TOGETHER, 0.8)}, conn)
    assert result.failed.startswith('writing:')
    assert [r[0] for r in conn.execute('select status from link_selections order by id')] == ['proposed', 'failed']
    assert conn.execute('select count(*) from dependencies').fetchone()[0] == 0
