"""D157 tables: real SQLite and stored Ohio sentences; only model responses are controlled."""
import copy
import json
import re
import sqlite3
import time
from pathlib import Path

import pytest

from hivemind import model as hivemind_model

import ohio_sequence as ohio


@pytest.fixture
def case(tmp_path):
    conn = sqlite3.connect(f'file:{ohio.ITEMS_DB}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    items = [dict(conn.execute('select * from items where input_id=?', (i,)).fetchone()) for i in ohio.ITEM_IDS]
    conn.close()
    for item in items:
        item['object_identifiers'] = json.loads(item['object_identifiers'])
    archive = sqlite3.connect(f'file:{ohio.ROOT}/poc/data/keyed-2026-10-25/archive-T2.sqlite?mode=ro', uri=True)
    raw = json.loads(archive.execute('select answer_json from model_calls where call_id=304').fetchone()[0])
    second = json.loads(archive.execute('select answer_json from model_calls where call_id=349').fetchone()[0])
    archive.close()
    # A controlled reference fixture: actual stored candidate, theme ownership and a verbatim source sentence.
    c = dict(raw['candidates'][0], object='ai-capex', evidence_ids=['e2'], thread_ids=['t1'])
    e = dict(raw['evidence'][1], links=['c1'])
    first = {'candidates': [c], 'evidence': [e], 'threads': [{'id': 't1', 'name': 'Ohio project', 'scope': 'OpenAI Ohio financing and deployment'}]}
    followup = {'candidates': [], 'evidence': [dict(second['evidence'][4], links=['v1'])], 'threads': []}
    new = {'candidates': [{'id': 'c1', 'outcome': '新观点', 'target_view_id': '', 'reason': 'new project', 'dependencies': []}], 'evidence': []}
    update = {'candidates': [], 'evidence': [{'id': 'e5', 'view_id': 'v1', 'outcome': '新证据', 'target_evidence_id': '', 'said_day': '2026-07-27', 'reason': 'analyst risk'}]}
    db = ohio.groups.open_db(tmp_path / 'views.sqlite')
    calls = ohio.model.Archive(str(tmp_path / 'calls.sqlite'))
    cfg = ohio.config.load(ohio.ROOT / 'poc/config/poc-v16.json')
    uni = ohio.universe.load(ohio.ROOT / 'poc/universe.json')
    yield db, calls, cfg, uni, items, first, followup, new, update
    db.close()
    calls.conn.close()


def answers(values, requests):
    stream = iter(values)
    def transport(provider, request):
        requests.append(copy.deepcopy(request))
        return {'choices': [{'message': {'content': json.dumps(next(stream), ensure_ascii=False)}}],
                'usage': {'prompt_tokens': 200, 'completion_tokens': 100}}
    return transport


def test_d157_sequential_theme_evidence_and_history(case, tmp_path):
    """State table: next article sees committed theme member; evidence-only update, history and resend."""
    db, archive, cfg, uni, items, first, followup, new, update = case
    requests = []
    transport = answers([first, new, followup, update], requests)
    one = ohio.process(db, archive, cfg, uni, items[0], True, tmp_path / 'one', transport)
    assert len(one['snapshot']['thread_members']) == 1
    two = ohio.process(db, archive, cfg, uni, items[1], True, tmp_path / 'two', transport)
    assert [e['evidence_id'] for e in two['snapshot']['details'][0]['members'][0]['evidence']] == ['e1', 'e2']
    assert two['new_views'] == {} and two['bindings'] == []
    assert ohio.groups.thread_detail(db, 'g1', one['seq']) == one['snapshot']['details'][0]
    assert 'v1（ai-capex' in requests[2]['messages'][1]['content']
    assert '你是一位资深对冲基金分析师' in requests[0]['messages'][0]['content']
    assert db.execute('select key_version from view_keys').fetchone()[0] == 2
    assert 'thread_ids' not in json.dumps(requests[1], ensure_ascii=False)
    assert ohio.process(db, archive, cfg, uni, items[0], True, tmp_path / 'resend', transport)['route'] == 'skipped'
    assert len(requests) == 4


@pytest.mark.parametrize('bad', ['g999', 't2', ''])
def test_d157_unknown_reference_refuses_before_write(case, tmp_path, bad):
    """Closed reference contract: only declared/actually offered IDs can reach the writer."""
    db, archive, cfg, uni, items, first, _, _, _ = case
    first['candidates'][0]['thread_ids'] = [bad]
    with pytest.raises(ohio.Refused, match='invalid group references|does not match'):
        ohio.validate_references(first, [])
    # the model boundary refuses the shape first now that the local validator enforces string patterns (D164); either way nothing is written
    with pytest.raises((ohio.Refused, hivemind_model.SchemaError), match='invalid group references|does not match'):
        ohio.process(db, archive, cfg, uni, items[0], True, tmp_path / 'one', answers([first], []))
    assert db.execute('select count(*) from views').fetchone()[0] == 0


def test_d157_group_failure_rolls_back_view_and_evidence(case, tmp_path):
    """Write state: a real SQLite failure inserting a member must undo the whole product write."""
    db, archive, cfg, uni, items, first, _, new, _ = case
    db.execute("create trigger reject_member before insert on thread_members begin select raise(abort,'test member failure'); end")
    with pytest.raises(sqlite3.IntegrityError, match='test member failure'):
        ohio.process(db, archive, cfg, uni, items[0], True, tmp_path / 'one', answers([first, new], []))
    assert {table: db.execute(f'select count(*) from {table}').fetchone()[0] for table in ('views', 'evidence', 'threads')} == {'views': 0, 'evidence': 0, 'threads': 0}
    assert not ohio.store.is_processed(db, items[0]['input_id'])


def test_d157_control_request_is_current_extraction(case, tmp_path):
    """Control means the exact current Chinese request, with no grouping data or membership writes."""
    db, archive, cfg, uni, items, first, _, new, _ = case
    first.pop('threads')
    first['candidates'][0].pop('thread_ids')
    requests = []
    result = ohio.process(db, archive, cfg, uni, items[0], False, tmp_path / 'one', answers([first, new], requests))
    system, user = ohio.extraction.build_prompt(items[0], items[0]['text'], [], uni, 'v5')
    expected = ohio.model.build_request(cfg.extraction_setting('T7'), system, user, ohio.extraction.keyed_schema(), 'extraction', cfg.provider)
    assert requests[0] == expected
    assert result['snapshot']['threads'] == [] and len(result['snapshot']['views']) == 1


def test_d157_budget_refuses_before_network(tmp_path):
    """Budget state: a used-up request allocation sends zero further requests."""
    ohio.write(tmp_path / 'budget.json', {'attempts': [{}] * ohio.MAX_REQUESTS, 'reserved_or_spent': 0})
    sent = []
    call = ohio.BoundedTransport(tmp_path, 'control-1', time.monotonic() + 60, send=answers([{}], sent))
    request = {'model': 'gpt-6-luna', 'max_completion_tokens': 8000}
    with pytest.raises(RuntimeError, match='limit reached'):
        call('openai', request)
    assert sent == []


def test_d157_failed_network_is_reserved_once(tmp_path):
    """Unknown external result keeps its reservation and is not secretly retried."""
    ohio.write(tmp_path / 'budget.json', {'attempts': [], 'reserved_or_spent': 0})
    sent = []
    def fail(provider, request):
        sent.append(request)
        raise TimeoutError('simulated external timeout')
    call = ohio.BoundedTransport(tmp_path, 'control-1', time.monotonic() + 60, send=fail)
    with pytest.raises(RuntimeError, match='no resend'):
        call('openai', {'model': 'gpt-6-luna', 'max_completion_tokens': 8000})
    assert len(sent) == 1 and ohio.read(tmp_path / 'budget.json')['reserved_or_spent'] > 0


def test_d157_wire_schema_refuses_real_unoffered_ids():
    """Request contract: the four actually refused references cannot pass the wire schema."""
    path = ohio.DEFAULT_OUT / 'grouped-2/item1'
    raw = ohio.read(path / 'extraction.json')
    offered = ohio.read(path / 'context.json')['offered']
    rule = ohio.schema(offered)['properties']['candidates']['items']['properties']['thread_ids']['items']
    assert 'pattern' in rule
    assert sum(re.fullmatch(rule['pattern'], ref) is None for c in raw['candidates'] for ref in c['thread_ids']) == 4
    assert all(re.fullmatch(rule['pattern'], g['thread_id']) for g in offered)
    assert all(re.fullmatch(rule['pattern'], g['id']) for g in raw['threads'])


@pytest.mark.parametrize('explicit_control', [False, True])
def test_d158_prepared_role_experiment_runs_two_grouped_arms(case, tmp_path, monkeypatch, explicit_control):
    """D158/D161 entry point: each arm receives its frozen role; omitting the control keeps v5."""
    _, _, _, _, _, first, followup, new, update = case
    c = first['candidates'][0]
    c.update(measure='event', event_type='deal_close', unit='n/a', year='2027',
             period_start='2026-01-01', period_end='2027-07-26', due_day='2027-07-26',
             scope='OpenAI Ohio project financing guarantee', looks_at='Ohio 项目担保协议签署',
             question='截至2027-07-26，英伟达是否已签署为 OpenAI Ohio 项目提供融资担保的协议？',
             rungs=[{'label': '是', 'condition': '到检查日已签署担保协议', 'lo': None, 'hi': None},
                    {'label': '否', 'condition': '到检查日未签署担保协议', 'lo': None, 'hi': None}])
    out = tmp_path / 'experiment'
    out.mkdir()
    (out / 'preflight.txt').write_text('Controlled test; no external calls.')
    role_path = out / 'role.txt'
    role_text = (ohio.ROOT / 'poc/reports/2026-10-25-ohio-grouping-02/role-questions.txt').read_text()
    role_path.write_text(role_text)
    control_path = ohio.ROOT / 'poc/reports/2026-10-25-ohio-grouping-03/role-questions.txt' if explicit_control else None
    ohio.prepare(out, role_path=role_path, control_role_path=control_path)
    sent = {}

    def transport_factory(out, label, deadline):
        sent[label] = []
        return answers(copy.deepcopy([first, new, followup, update]), sent[label])

    monkeypatch.setattr(ohio, 'BoundedTransport', transport_factory)
    ohio.run(out)
    assert set(ohio.read(out / 'status.json').values()) == {'complete'}
    for label, requests in sent.items():
        expected_control = control_path.read_text() if control_path else ohio.extraction._read('role-v5.txt')
        expected_role = role_text if label.startswith('grouped') else expected_control
        for request in requests[::2]:
            assert request['messages'][0]['content'] == expected_role + '\n\n' + ohio.GROUP_PROMPT
        result = ohio.read(out / label / 'item2/result.json')
        assert len(result['snapshot']['thread_members']) == 1
        assert len(result['snapshot']['details'][-1]['members'][0]['evidence']) == 2
        assert len(requests) == 4
    if control_path:
        assert ohio.read(out / 'manifest.json')['dependencies'][str(control_path)] == ohio.digest(control_path)


def test_d160_three_real_inputs_reach_the_same_project(case, tmp_path, monkeypatch):
    """D160 input/reader table: all three frozen articles run sequentially in each fresh arm."""
    _, _, _, _, _, first, followup, new, update = case
    with sqlite3.connect(f'file:{ohio.ROOT}/poc/data/keyed-2026-10-25/archive-T2.sqlite?mode=ro', uri=True) as source:
        raw = json.loads(source.execute('select answer_json from model_calls where call_id=460').fetchone()[0])
    third = {'candidates': [], 'threads': [], 'evidence': [dict(next(e for e in raw['evidence'] if e['id'] == 'e3'), links=['v1'])]}
    third_match = {'candidates': [], 'evidence': [{'id': 'e3', 'view_id': 'v1', 'outcome': '新证据',
                    'target_evidence_id': '', 'said_day': '2026-07-28', 'reason': 'controlled third article'}]}
    ids = (*ohio.ITEM_IDS, 'gnews:eb74b9d16d227f0c2b7a39d8')
    out = tmp_path / 'three'
    out.mkdir()
    (out / 'preflight.txt').write_text('Controlled test; external model only is fake.')
    role = tmp_path / 'role.txt'
    role.write_text(ohio.extraction._read('role-v5.txt'))
    ohio.prepare(out, role_path=role, item_ids=ids, max_requests=54)
    sent = {}

    def transport_factory(folder, label, deadline):
        sent[label] = []
        return answers(copy.deepcopy([first, new, followup, update, third, third_match]), sent[label])

    monkeypatch.setattr(ohio, 'BoundedTransport', transport_factory)
    ohio.run(out)
    assert set(ohio.read(out / 'status.json').values()) == {'complete'}
    assert ohio.read(out / 'manifest.json')['max_requests'] == 54
    for label, requests in sent.items():
        assert len(requests) == 6
        result = ohio.read(out / label / 'item3/result.json')
        assert result['input_id'] == ids[2] and result['seq'] == 3
        assert len(requests) == 6 and 'v1（ai-capex' in requests[4]['messages'][1]['content']
        assert len(result['snapshot']['evidence']) == 3
        assert len(result['snapshot']['thread_members']) == 1


def test_d160_manifest_attempt_limit_is_enforced(tmp_path):
    """D160 budget table: transport reads the frozen limit, without changing the dollar cap."""
    ohio.write(tmp_path / 'manifest.json', {'max_requests': 1})
    ohio.write(tmp_path / 'budget.json', {'attempts': [{}], 'reserved_or_spent': 0})
    (tmp_path / 'control-1').mkdir()
    sent = []
    call = ohio.BoundedTransport(tmp_path, 'control-1', time.monotonic() + 60, send=answers([{}], sent))
    with pytest.raises(RuntimeError, match='limit reached'):
        call('openai', {'model': 'gpt-6-luna', 'max_completion_tokens': 8000})
    assert sent == []
