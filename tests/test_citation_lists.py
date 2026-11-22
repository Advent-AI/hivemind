"""judging-v12 (D712, D713; docs/research/2026-11-21-citation-lists/DESIGN.md): the judge's four id fields take only the ids its request
lists, from the rows that render the request, and the check reads the same lists. Real ledger on a temporary path; the model is a
scripted transport; every answer goes through the real `model.call` and `model.check_schema`."""
import json
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402
import test_theme_block as fixtures  # noqa: E402

V121 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v121.json'))
DAY = {'input_id': 'day:2026-07-29', 'publication_day': '2026-07-29'}


def answer(view_id, **fields):
    data = {'rung': 2, 'reference': 'consensus expects about 78', 'implied_outcome': 'about 78 on the evidence', 'reasons': f'scripted for {view_id}',
            'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'scripted', 'theme_pushes': []}
    data.update(fields)
    return {'choices': [{'message': {'content': json.dumps(data)}}], 'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}


def judged_theme(conn):
    """v2 (the theme) holds a conclusion, so it is in force for v1."""
    fixtures.judged(conn, 'v2', 1, 'theme judged', 2)
    conn.commit()


def add_evidence(conn, evidence_id, view_id, quote, seq=1):
    store.add_evidence(conn, evidence_id=evidence_id, quote=quote, one_line=quote[:40], speaker='CFO', original_who='NVIDIA', original_day='2026-02-25',
                       tier='party_statement', event_time='', seq=seq, input_id='truenorth:transcript:NVDA:2026-02-25')
    store.add_source(conn, evidence_id, 'truenorth:transcript:NVDA:2026-02-25', 'T4', '2026-02-25', 'p1', seq)
    store.link(conn, evidence_id, view_id, seq)


def test_the_lists_are_the_rendered_rows_and_a_waiting_dependency_gives_no_id(tmp_path):
    """DESIGN §3: evidence printed, resolved dependencies with an entry, themes printed; a dependency still waiting has no citable id."""
    conn = fixtures.ledger(tmp_path)
    judged_theme(conn)
    store.create_view(conn, view_id='v3', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 total revenue',
                      question='How much total revenue will NVIDIA report for FY2027?', due_day='2027-02-24', year='FY2027', rungs=fixtures.ASSET_RUNGS,
                      seq=1, input_id='truenorth:transcript:NVDA:2026-02-25', created_at='2026-02-25T22:00:00Z')
    store.insert(conn, 'dependencies', view_id='v1', depends_on='v3', wait_chain_view_id='', wait_year='', direction='first_is_bullish', seq=1)
    store.insert(conn, 'dependencies', view_id='v1', depends_on='', wait_chain_view_id='v3', wait_year='FY2029', direction='same', seq=1)
    conn.commit()
    system, user, lists = judging.request_parts(conn, 'v1', 'judging-v12')
    assert lists == {'evidence': ['e1'], 'dependencies': ['v3'], 'themes': ['v2']}
    assert (system, user) == judging.build_prompt(conn, 'v1', 'judging-v12') == judging.build_prompt(conn, 'v1', 'judging-v7')
    assert '- e1 [' in user and '- v3 (' in user and '- v2 (' in user and 'not yet created' in user


def test_every_id_field_takes_only_its_listed_ids_through_the_real_validator():
    """T3: an allowed id passes and an unlisted id fails in each of the four fields; an empty list allows only [], and a correctly typed
    item fails on the array's length, not on its type."""
    schema = judging.schema_for('judging-v12', {'evidence': ['e1', 'e3'], 'dependencies': ['v3'], 'themes': ['v2']})
    valid = json.loads(answer('v1')['choices'][0]['message']['content'])
    check = lambda **fields: model.check_schema(dict(valid, **fields), schema)
    assert check(cites=['e3'], pushes=[{'evidence_id': 'e1', 'push': 'none'}], cites_views=['v3'], theme_pushes=[{'view_id': 'v2', 'push': 'none'}]) == []
    assert check(cites=['e362'])
    assert check(pushes=[{'evidence_id': 'e3111', 'push': 'none'}])
    assert check(cites_views=['v5'])
    assert check(theme_pushes=[{'view_id': 'v14', 'push': 'none'}])
    empty = judging.schema_for('judging-v12', {'evidence': [], 'dependencies': [], 'themes': []})
    filled = {'cites': ['e1'], 'cites_views': ['v3'], 'pushes': [{'evidence_id': 'e1', 'push': 'none'}], 'theme_pushes': [{'view_id': 'v2', 'push': 'none'}]}
    assert model.check_schema(dict(valid, cites=[], cites_views=[], pushes=[], theme_pushes=[]), empty) == []
    for field, items in filled.items():
        assert model.check_schema(dict(valid, **{field: items}), empty) == [f'$.{field}: more than 0 items'], field


def test_one_owner_of_membership_a_footnote_in_a_quote_does_not_hide_a_later_id(tmp_path):
    """T3b: a quote holding a blank line and "[1]" ends the evidence block for the text parser, so a real later entry looks unlisted;
    under judging-v12 the format and the check both read the rendered rows."""
    conn = fixtures.ledger(tmp_path)
    store.create_view(conn, view_id='v6', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 total revenue',
                      question='How much total revenue will NVIDIA report for FY2027?', due_day='2027-02-24', year='FY2027', rungs=fixtures.ASSET_RUNGS,
                      seq=1, input_id='truenorth:transcript:NVDA:2026-02-25', created_at='2026-02-25T22:00:00Z')
    add_evidence(conn, 'e4', 'v6', 'Data center revenue rose sharply.\n\n[1] Excludes networking.', seq=1)
    add_evidence(conn, 'e5', 'v6', 'Guidance for the next quarter is $91 billion.', seq=2)
    conn.commit()
    _, user, lists = judging.request_parts(conn, 'v6', 'judging-v12')
    assert lists['evidence'] == ['e4', 'e5'] and '- e5 [' in user
    data = json.loads(answer('v6', cites=['e5'], pushes=[{'evidence_id': 'e5', 'push': 'toward_first'}])['choices'][0]['message']['content'])
    assert judging.check_answer(conn, 'v6', data, user, lists) == []
    assert model.check_schema(data, judging.schema_for('judging-v12', lists)) == []
    assert 'e5 is not among the evidence shown to v6' in judging.check_answer(conn, 'v6', data, user)       # the frozen text parser narrows


def test_a_judging_v12_round_sends_the_closed_format_and_its_retry_carries_the_same_format(tmp_path):
    """T1c: the first answer names a theme twice (a refusal that is not about membership); the retry carries exactly the first
    request's format and lists, plus the code's note; the accepted answer is recorded."""
    conn = fixtures.ledger(tmp_path)
    judged_theme(conn)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    sent = []

    def transport(provider, request):
        sent.append(request)
        if len(sent) == 1:
            return answer('v1', cites=['e1'], theme_pushes=[{'view_id': 'v2', 'push': 'none'}, {'view_id': 'v2', 'push': 'none'}])
        return answer('v1', cites=['e1'], pushes=[{'evidence_id': 'e1', 'push': 'toward_first'}], theme_pushes=[{'view_id': 'v2', 'push': 'none'}])
    results = judging.round_of_judgements(archive, V121, conn, ['v1'], 3, DAY, transport=transport)
    assert [r['view_id'] for r in results] == ['v1'] and len(sent) == 2
    first, retry = sent
    expected = judging.schema_for('judging-v12', {'evidence': ['e1'], 'dependencies': [], 'themes': ['v2']})
    assert first['response_format'] == {'type': 'json_schema', 'json_schema': {'name': 'judgement', 'strict': True, 'schema': expected}}
    assert retry['response_format'] == first['response_format']
    assert retry['messages'][1]['content'].startswith(first['messages'][1]['content'])
    assert 'v2 is named twice in theme_pushes' in retry['messages'][1]['content'][len(first['messages'][1]['content']):]
    assert store.current_state(conn, 'v1')['rung'] == 2


def test_an_answer_outside_the_lists_is_refused_by_the_format_before_the_check(tmp_path):
    """DESIGN §4.1: a membership error the provider should never return under strict mode is refused by `model.check_schema`
    (a `:schema:` row and SchemaError), not by the check's retry."""
    conn = fixtures.ledger(tmp_path)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    with pytest.raises(model.SchemaError, match='e362'):
        judging.round_of_judgements(archive, V121, conn, ['v1'], 3, DAY, transport=lambda provider, request: answer('v1', cites=['e362']))
    assert archive.conn.execute("select count(*) from model_calls where request_sha256 like '%:schema:%'").fetchone()[0] == 1
    assert store.current_state(conn, 'v1') is None


def test_preflight_fails_on_a_refused_judge_row_without_its_saved_format(tmp_path, capsys):
    """T5: judge rows are checked against the format saved with their request; one without a format is named and fails preflight."""
    import preflight
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    closed = judging.schema_for('judging-v12', {'evidence': ['e1'], 'dependencies': [], 'themes': []})
    rows = [('judge', 'a' * 64 + ':refused:1', {'response_format': {'json_schema': {'name': 'judgement', 'strict': True, 'schema': closed}}},
             json.loads(answer('v1', cites=['e9'])['choices'][0]['message']['content'])),
            ('judge', 'b' * 64 + ':refused:2', {'messages': []}, json.loads(answer('v1')['choices'][0]['message']['content'])),
            ('judge', 'd' * 64 + ':malformed:4', {'messages': []}, None)]        # no format and no readable answer (Codex r39)
    for purpose, sha, request, data in rows:
        archive.record(purpose=purpose, config_version='poc-v121', config_checksum='x', model='gpt-6-luna', request_sha256=sha,
                       request_json=json.dumps(request), response_json='{}', answer_json=None if data is None else json.dumps(data), prompt_chars=1,
                       input_tokens=1, output_tokens=1, cost_usd=0.0, seconds=0.1, created_at='2026-11-21T20:00:00')
    archive.conn.row_factory = None
    judged, missing = preflight.part_a(archive.conn)
    out = capsys.readouterr().out
    assert judged == 3 and missing == ['b' * 64 + ':refused:2', 'd' * 64 + ':malformed:4']
    assert "'e9' not in" in out and 'judge: no saved answer format' in out


def test_preflights_entry_point_exits_non_zero_on_a_judge_row_without_its_saved_format(tmp_path, monkeypatch, capsys):
    """T5, as the user runs it: `main` finishes the other parts, then exits 1 naming the judge row part A could not check."""
    import preflight
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    archive.record(purpose='judge', config_version='poc-v121', config_checksum='x', model='gpt-6-luna', request_sha256='c' * 64 + ':refused:3',
                   request_json=json.dumps({'messages': []}), response_json='{}',
                   answer_json=answer('v1')['choices'][0]['message']['content'], prompt_chars=1, input_tokens=1, output_tokens=1,
                   cost_usd=0.0, seconds=0.1, created_at='2026-11-21T20:00:00')
    for name in ('part_b', 'part_d'):
        monkeypatch.setattr(preflight, name, lambda *arguments: 1)
    monkeypatch.setattr(preflight, 'part_c', lambda *arguments: 1)
    monkeypatch.setattr(preflight, 'part_e', lambda *arguments: None)
    monkeypatch.setattr(preflight, 'store_copies', lambda paths: [])
    monkeypatch.setattr(sys, 'argv', ['preflight.py', '--archive', str(tmp_path / 'archive.sqlite'), '--items', str(tmp_path / 'items.sqlite'),
                                      '--views', str(tmp_path / 'views.sqlite')])
    with pytest.raises(SystemExit) as stopped:
        preflight.main()
    assert stopped.value.code == 1 and 'FAILED: 1 refused judge rows carry no saved answer format' in capsys.readouterr().out
