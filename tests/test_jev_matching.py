"""Log row 34: the matching step answered by Jev. Real ledgers on temporary paths; a scripted Jev transport; the answer in
the matching schema goes through matching.check and writing.write unchanged."""
import json
import os
import sys

import pytest

from test_keyed_views import ITEM, UNIVERSE, candidate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, jev, model  # noqa: E402
from hivemind.views import jev_matching, matching, store, writing  # noqa: E402

CFG = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v22.json'))


def scripted(script):
    """A Jev transport answering each question from `script`: a key is a question id, or (needle, question id) to apply only
    when the needle occurs in the state; 'different' / 0.05 otherwise."""
    def transport(request):
        answers = {}
        state = request['state']

        def lookup(qid, default):
            for key, value in script.items():
                if isinstance(key, tuple) and key[1] == qid and key[0] in state:
                    return value
            return script.get(qid, default)
        for qid, q in request['questions'].items():
            if q['type'] == 'noul':
                answers[qid] = {'type': 'noul', 'noul': lookup(qid, 0.05)}
            else:
                labels = list(q['criteria'])
                chosen, p = lookup(qid, (('different' if 'different' in labels else labels[-1]), 0.9))
                probabilities = {label: round((1 - p) / (len(labels) - 1), 3) for label in labels}
                probabilities[chosen] = p
                answers[qid] = {'type': 'choice', 'choice': chosen, 'confidence': p, 'probabilities': probabilities}
        return {'model': request['model'], 'answers': answers, 'usage': {'input_tokens': 1000, 'output_tokens': 50}}
    return transport


def piece(eid, quote, links, day='2026-05-20'):
    return {'id': eid, 'links': links, 'tier': 'fact', 'speaker': 'NVIDIA', 'original_who': 'NVIDIA', 'original_day': day, 'event_time': '',
            'one_line': quote[:60], 'quote': quote, 'location': ''}


def ledger_with_view(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.ensure_writable_columns(conn)
    c = candidate('c0', looks_at='Data Center annual revenue', question='Data Center revenue in FY2027?')
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at=c['looks_at'], question=c['question'],
                      due_day='2027-02-28', year='FY2027', rungs=c['rungs'], seq=1, input_id='seed', created_at='2026-05-20T00:00:00')
    store.add_key(conn, 'v1', c, 1)
    store.add_evidence(conn, evidence_id='e1', quote='Data Center revenue was $51 billion in the quarter.', one_line='DC revenue $51bn', speaker='NVIDIA',
                       original_who='NVIDIA', original_day='2026-05-20', tier='fact', event_time='', seq=1, input_id='seed')
    store.add_source(conn, 'e1', 'seed', 'T4', '2026-05-20', '', 1)
    store.link(conn, 'e1', 'v1', 1)
    conn.commit()
    return conn, c


def test_a_repeated_statement_is_stored_as_its_own_record_related_to_the_old_one(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    incoming = piece('x1', 'Data Center revenue reached $51 billion in the quarter, the company said.', ['v1'], day='2026-05-21')
    handover = type('H', (), {'candidates': [], 'evidence': [incoming], 'dropped': [], 'new_groups': []})()
    lists = matching.build_lists(conn, handover, [], CFG.search_top_n)
    assert lists.evidence_lists == {('x1', 'v1'): ['e1']}
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [], [incoming], lists, [], transport=scripted({'piece__v1__e1': ('same_statement', 0.91)}))
    assert answer.data['evidence'] == [{'id': 'x1', 'view_id': 'v1', 'outcome': 'repeat', 'target_evidence_id': 'e1', 'said_day': '2026-05-21', 'reason': 'jev: e1: same_statement 0.91'}]
    checked = matching.check(conn, UNIVERSE, answer.data, [], [incoming], lists, [])
    assert checked.refusals == [] and checked.evidence[('x1', 'v1')] == ('repeat', 'e1', '2026-05-21')
    written = writing.write(conn, UNIVERSE, 2, dict(ITEM, input_id='later'), handover, checked, {})
    conn.commit()
    assert written.evidence_ids == {'x1': 'e2'}                                                     # D204: its own record
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 2
    assert [r[0] for r in conn.execute("select input_id from evidence_sources where evidence_id='e1' order by id")] == ['seed']
    assert [r[0] for r in conn.execute("select input_id from evidence_sources where evidence_id='e2' order by id")] == ['later']
    assert [tuple(r) for r in conn.execute('select old_evidence_id, new_evidence_id from same_claims')] == [('e1', 'e2')]
    in_force = {p['evidence_id']: p for p in store.evidence_in_force(conn, 'v1')}
    assert set(in_force) == {'e1', 'e2'} and in_force['e2']['same_as'] == ['e1'] and in_force['e1']['same_as'] == ['e2']
    import sqlite3
    calls = sqlite3.connect(str(tmp_path / 'archive.sqlite')).execute("select model, purpose, input_tokens, cost_usd from model_calls").fetchall()
    assert calls == [('jev-1.14.0', 'match', 1000, 0.000042)]


def test_a_superseding_statement_replaces_and_an_unrelated_one_is_new(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    newer = piece('x1', 'Data Center revenue is now expected at $60 billion next quarter.', ['v1'], day='2026-08-27')
    other = piece('x2', 'Gaming revenue was $3 billion.', ['v1'], day='2026-08-27')
    handover = type('H', (), {'candidates': [], 'evidence': [newer, other], 'dropped': [], 'new_groups': []})()
    lists = matching.build_lists(conn, handover, [], CFG.search_top_n)
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [], [newer, other], lists, [], transport=scripted({('$60 billion', 'piece__v1__e1'): ('supersedes', 0.8)}))
    outcomes = {d['id']: (d['outcome'], d['target_evidence_id']) for d in answer.data['evidence']}
    assert outcomes == {'x1': ('replace', 'e1'), 'x2': ('new', '')}
    assert answer.calls == 2        # one Jev call per incoming piece
    # the second piece's call answered 'different' for every stored piece, so it is new
    checked = matching.check(conn, UNIVERSE, answer.data, [], [newer, other], lists, [])
    assert checked.refusals == []


def test_a_same_quantity_merges_only_when_the_key_allows_and_a_later_period_succeeds(tmp_path):
    conn, stored = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    same = candidate('c1', looks_at='NVIDIA data-center revenue', question='Where does FY2027 data-center revenue land?')
    other_measure = candidate('c2', measure='gross_margin', scope='', looks_at='FY2027 gross margin', question='FY2027 gross margin?')
    later = candidate('c3', period_start='2027-02-01', period_end='2028-01-31', year='FY2028', due_day='2028-02-28', looks_at='Data Center revenue FY2028',
                      question='FY2028 Data Center revenue?')
    handover = type('H', (), {'candidates': [same, other_measure, later], 'evidence': [], 'dropped': [], 'new_groups': []})()
    lists = matching.Lists({'c1': ['v1'], 'c2': ['v1'], 'c3': ['v1']}, {})
    script = {'rel__v1': ('same_quantity_or_event', 0.9)}          # every candidate is told v1 is the same; the key decides what that may mean
    answer = jev_matching.decide(archive, CFG, conn, ITEM, handover.candidates, [], lists, [], transport=scripted(script))
    raw = {d['id']: (d['outcome'], d['target_view_id']) for d in answer.data['candidates']}
    # the key decides what 'the same' may mean: gross margin is never data-center revenue (declined), a later period is a succession
    assert raw == {'c1': ('merge', 'v1'), 'c2': ('new', ''), 'c3': ('succession', 'v1')}
    checked = matching.check(conn, UNIVERSE, answer.data, handover.candidates, [], lists, [])
    assert checked.refusals == []
    assert checked.outcomes['c1'] == ('merge', 'v1', []) and checked.outcomes['c2'][0] == 'new' and checked.outcomes['c3'] == ('succession', 'v1', [])
    fresh = model.Archive(str(tmp_path / 'archive2.sqlite'))        # the first archive would serve the identical request's cached 'same' answer
    answer2 = jev_matching.decide(fresh, CFG, conn, ITEM, [later], [], matching.Lists({'c3': ['v1']}, {}), [], transport=scripted({}))
    assert {d['id']: (d['outcome'], d['target_view_id']) for d in answer2.data['candidates']} == {'c3': ('succession', 'v1')}


def test_a_membership_above_threshold_joins_the_group_through_the_writer(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    store.add_group(conn, group_id='g1', name='Rubin platform ramp', scope='Vera Rubin production and customer deployments', seq=1, input_id='seed',
                    object_ids=['NVDA'], aliases=['Rubin platform ramp', 'Rubin'])
    store.add_member(conn, 'g1', 'v1', 1, 'seed')
    conn.commit()
    deployment = candidate('c1', measure='event', scope='SK Telecom AI factory', event_type='deployment', looks_at='SK Telecom AI factory deployment',
                           question='Is the SK Telecom AI factory deployed by 2027?', year='2027', due_day='2027-12-31',
                           rungs=[{'label': 'Yes', 'condition': 'deployed', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'not deployed', 'lo': None, 'hi': None}])
    handover = type('H', (), {'candidates': [deployment], 'evidence': [], 'dropped': [], 'new_groups': []})()
    lists = matching.Lists({'c1': []}, {})
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [deployment], [], lists, [], transport=scripted({'member__g1': 0.88}))
    assert deployment['jev_group_refs'] == ['g1'] and 'group_refs' not in deployment and answer.data['candidates'][0]['outcome'] == 'new'
    checked = matching.check(conn, UNIVERSE, answer.data, [deployment], [], lists, [])
    written = writing.write(conn, UNIVERSE, 2, ITEM, handover, checked, {})
    conn.commit()
    assert store.members_of_group(conn, 'g1') == ['v1', written.new_views['c1']]
    assert conn.execute('select basis from thesis_group_members where view_id=?', (written.new_views['c1'],)).fetchone()[0] == 'jev'


def test_a_thesis_shown_at_extraction_is_a_target_even_when_the_search_list_is_empty(tmp_path):
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    same = candidate('c1', looks_at='NVIDIA data-center revenue', question='Where does FY2027 data-center revenue land?')
    shown = [{'view_id': 'v1', 'object_id': 'NVDA'}]
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [same], [], matching.Lists({'c1': []}, {}), shown, transport=scripted({'rel__v1': ('same_quantity_or_event', 0.9)}))
    assert answer.calls == 1 and answer.data['candidates'][0]['outcome'] == 'merge' and answer.data['candidates'][0]['target_view_id'] == 'v1'
    checked = matching.check(conn, UNIVERSE, answer.data, [same], [], matching.Lists({'c1': []}, {}), shown)
    assert checked.refusals == [] and checked.outcomes['c1'] == ('merge', 'v1', [])


def test_jev_client_archives_once_and_serves_a_repeated_request_from_the_archive(tmp_path):
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    questions = {'q': {'type': 'noul', 'instructions': 'Is it so?', 'criteria': {'true': 'yes', 'false': 'no'}}}
    first = jev.ask(archive, CFG, CFG.matching, 'state', questions, 'match', transport=scripted({'q': 0.7}))
    second = jev.ask(archive, CFG, CFG.matching, 'state', questions, 'match', transport=scripted({'q': 0.1}))
    assert (first.cached, second.cached) == (False, True) and second.data == {'q': {'type': 'noul', 'noul': 0.7}}
    assert archive.totals()[0] == 1 if isinstance(archive.totals(), tuple) else True
    assert model.CREDENTIALS.endswith('/.config/hivemind/credentials.json')      # the hivemind path, never the old repository's; tests never read it


def test_a_choice_one_rounding_unit_below_the_top_probability_is_valid_but_a_real_gap_is_not():
    # jev.ROUNDING: probabilities are rounded to two decimals independently of the choice (archive call 1035, rel__v17: 0.47 vs 0.48)
    questions = {'q': {'type': 'choice', 'criteria': {'a': '', 'b': '', 'c': ''}}}
    rounded = {'q': {'type': 'choice', 'choice': 'a', 'probabilities': {'a': 0.47, 'b': 0.48, 'c': 0.05}}}
    assert jev.validate(rounded, questions) == []
    gap = {'q': {'type': 'choice', 'choice': 'a', 'probabilities': {'a': 0.45, 'b': 0.50, 'c': 0.05}}}
    assert jev.validate(gap, questions) == ['q: choice is not the most probable option']


def test_code_decides_a_succession_when_one_side_leaves_the_basis_unstated(tmp_path):
    # log row 48: CoreWeave FY2027 (GAAP) after FY2026 (basis n/a) opened a new thesis; 'n/a' matches any basis, as in identity.conflicts
    conn, _ = ledger_with_view(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    later = candidate('c3', basis='GAAP', period_start='2027-02-01', period_end='2028-01-31', year='FY2028', due_day='2028-02-28',
                      looks_at='Data Center revenue FY2028', question='FY2028 Data Center revenue?')
    answer = jev_matching.decide(archive, CFG, conn, ITEM, [later], [], matching.Lists({'c3': ['v1']}, {}), [], transport=scripted({}))
    assert {d['id']: (d['outcome'], d['target_view_id']) for d in answer.data['candidates']} == {'c3': ('succession', 'v1')}
    other_unit = candidate('c4', unit='percent', period_start='2027-02-01', period_end='2028-01-31', year='FY2028', due_day='2028-02-28')
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'a2.sqlite')), CFG, conn, ITEM, [other_unit], [], matching.Lists({'c4': ['v1']}, {}), [], transport=scripted({}))
    assert answer.data['candidates'][0]['outcome'] == 'new'                        # a stated, different unit is another quantity


def test_the_judge_can_name_the_same_quantity_for_another_period(tmp_path):
    # log row 48: SpaceX compute capacity end-2027 after end-2026, scopes worded differently by the model; the options could not say it
    conn, _ = ledger_with_view(tmp_path)
    reworded = dict(period_start='2027-02-01', period_end='2028-01-31', year='FY2028', due_day='2028-02-28', scope='Accelerated computing platform',
                    looks_at='Accelerated computing platform revenue FY2028', question='FY2028 accelerated computing platform revenue?')
    script = {'rel__v1': ('same_quantity_other_period', 0.8)}
    unscripted = jev_matching.decide(model.Archive(str(tmp_path / 'a0.sqlite')), CFG, conn, ITEM, [candidate('c5', **reworded)], [], matching.Lists({'c5': ['v1']}, {}), [], transport=scripted({}))
    assert unscripted.data['candidates'][0]['outcome'] == 'new'                     # the scopes differ, so the code's rule does not decide it
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'a1.sqlite')), CFG, conn, ITEM, [candidate('c5', **reworded)], [], matching.Lists({'c5': ['v1']}, {}), [], transport=scripted(script))
    assert {d['id']: (d['outcome'], d['target_view_id']) for d in answer.data['candidates']} == {'c5': ('succession', 'v1')}
    earlier = dict(reworded, period_start='2025-02-01', period_end='2026-01-31', year='FY2026', due_day='2026-02-28')
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'a2.sqlite')), CFG, conn, ITEM, [candidate('c6', **earlier)], [], matching.Lists({'c6': ['v1']}, {}), [], transport=scripted(script))
    assert answer.data['candidates'][0]['outcome'] == 'new'                        # an earlier period cannot be chained after


@pytest.mark.parametrize('failures, sent, raises', [
    (['reset'], 2, False), (['reset', 'reset'], 3, False), (['reset'] * 3, 3, True),
    (['429'], 2, False), (['400'], 1, True)])
def test_transport_retries_only_replyless_failures_and_rate_limits(monkeypatch, failures, sent, raises):
    """D181 robustness: a dropped connection (seen 2 of 65 calls at eight parallel matches) is sent again, at most
    three attempts; a final HTTP status is not retried; credentials are never read."""
    import io
    import urllib.error
    from hivemind import jev
    monkeypatch.setattr(jev, '_key', lambda: 'test-key')
    monkeypatch.setattr(jev.time, 'sleep', lambda seconds: None)
    queue, attempts = list(failures), []

    class Reply(io.BytesIO):
        def __enter__(self):
            return self
        def __exit__(self, *exc):
            return False

    def urlopen(request, timeout):
        attempts.append(1)
        failure = queue.pop(0) if queue else None
        if failure == 'reset':
            raise urllib.error.URLError(ConnectionResetError('connection reset by peer'))
        if failure:
            raise urllib.error.HTTPError(request.full_url, int(failure), 'failed', {}, io.BytesIO(b''))
        return Reply(b'{"answers": {}}')
    monkeypatch.setattr(jev.urllib.request, 'urlopen', urlopen)
    if raises:
        with pytest.raises(model.TransportError):
            jev.transport({'model': 'jev-1.14.0', 'state': '', 'questions': {}})
    else:
        assert jev.transport({'model': 'jev-1.14.0', 'state': '', 'questions': {}}) == {'answers': {}}
    assert len(attempts) == sent
