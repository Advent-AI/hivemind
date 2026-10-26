"""D195 (the theme block, design.md §8): under judging-v4 an asset thesis is judged with every open, judged theme thesis in
view and answers which way each one it weighed pushes it; theme theses are judged before asset theses in a round; a changed
theme conclusion queues every open asset thesis once; the round's queue is derived from the ledger, so a resumed round recovers
what an earlier commit had queued. Real ledger on a temporary path; the model is a scripted transport."""
import dataclasses
import json
import os
import sys
import types

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config, model, service  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

DAY = {'input_id': 'day:2026-07-29', 'publication_day': '2026-07-29'}
ASSET_RUNGS = [{'label': 'Strongly bullish', 'condition': '>=80'}, {'label': 'Bullish', 'condition': '77-80'}, {'label': 'Neutral', 'condition': '73-77'},
               {'label': 'Bearish', 'condition': '70-73'}, {'label': 'Strongly bearish', 'condition': '<70'}]
THEME_RUNGS = [{'label': 'Imports allowed', 'condition': 'China permits H200 imports by the due day'}, {'label': 'Not allowed', 'condition': 'no permission by the due day'}]
V4 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v29.json'))
V3 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v26.json'))


def ledger(tmp_path):
    """One asset thesis (v1, NVDA data-center revenue) and one theme thesis (v2, China H200 permission), both with evidence in force."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='FY2027 data center revenue',
                      question='Where will NVIDIA FY2027 data center revenue land?', due_day='2027-02-24', year='FY2027', rungs=ASSET_RUNGS, seq=1,
                      input_id='truenorth:transcript:NVDA:2026-02-25', created_at='2026-02-25T22:00:00Z')
    store.create_view(conn, view_id='v2', object_id='chip-export-controls', object_kind='theme', kind='theme', looks_at='H200 imports into China',
                      question='Will the Chinese authorities allow any H200 imports into China by January 31, 2027?', due_day='2027-01-31', year='2026',
                      rungs=THEME_RUNGS, seq=1, input_id='truenorth:transcript:NVDA:2026-02-25', created_at='2026-02-25T22:00:00Z')
    for evidence_id, view_id, quote in (('e1', 'v1', 'On a full year basis, data center generated revenue of $194 billion.'),
                                        ('e2', 'v2', 'We do not know whether any imports will be allowed into China.')):
        store.add_evidence(conn, evidence_id=evidence_id, quote=quote, one_line=quote[:40], speaker='CFO', original_who='NVIDIA', original_day='2026-02-25',
                           tier='party_statement', event_time='', seq=1, input_id='truenorth:transcript:NVDA:2026-02-25')
        store.add_source(conn, evidence_id, 'truenorth:transcript:NVDA:2026-02-25', 'T4', '2026-02-25', 'p1', 1)
        store.link(conn, evidence_id, view_id, 1)
    conn.commit()
    return conn


def judged(conn, view_id, rung, reasons, seq, *, changed=True, theme_pushes=None):
    answer = types.SimpleNamespace(data={'rung': rung, 'reasons': reasons, 'cites': [], 'cites_views': [], 'pushes': [], 'changed': changed,
                                         'why_changed': 'test', **({'theme_pushes': theme_pushes} if theme_pushes is not None else {})},
                                   call_id=0, request_sha256='x', cached=False, cost_usd=0.0)
    judging._record(conn, V4, view_id, seq, DAY, answer)


def scripted(order, answers=None):
    """A transport that records which thesis each judgement request is for and answers 'changed' with the scripted pushes."""
    def send(provider, request):
        assert request['response_format']['json_schema']['name'] == 'judgement'
        user = request['messages'][1]['content']
        view_id = user.split('Thesis ', 1)[1].split(' ', 1)[0]
        order.append(view_id)
        data = {'rung': 1, 'reasons': f'scripted for {view_id}', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'scripted'}
        if 'theme_pushes' in request['response_format']['json_schema']['schema']['properties']:
            data['theme_pushes'] = (answers or {}).get(view_id, [])
        return {'choices': [{'message': {'content': json.dumps(data)}}]}
    return send


def test_v4_asset_request_lists_open_judged_theme_theses_and_marks_what_changed_since_its_last_judgement(tmp_path):
    conn = ledger(tmp_path)
    _, before = judging.build_prompt(conn, 'v1', 'judging-v4')
    assert '[Themes in force' not in before                                  # v2 has no judgement yet: nothing to read
    judged(conn, 'v2', 2, 'No permission has been reported; small U.S. approvals only.', 2)
    _, user = judging.build_prompt(conn, 'v1', 'judging-v4')
    assert '[Themes in force, 1]' in user
    assert '- v2 (chip-export-controls, due 2027-01-31) Will the Chinese authorities allow any H200 imports' in user
    assert 'now rung 2 Not allowed' in user and 'reasons: No permission has been reported' in user and 'judged 2026-07-29' in user
    assert 'updated since this thesis was last judged' not in user       # v1 has no judgement yet: there is no "since"
    judged(conn, 'v1', 3, 'first', 2, theme_pushes=[{'view_id': 'v2', 'push': 'toward_last'}])
    judged(conn, 'v2', 1, 'Permission granted.', 3)
    _, user = judging.build_prompt(conn, 'v1', 'judging-v4')
    assert 'now rung 1 Imports allowed' in user and 'updated since this thesis was last judged' in user
    _, v3_user = judging.build_prompt(conn, 'v1', 'judging-v3')
    assert '[Themes in force' not in v3_user and 'theme_pushes' not in judging.schema_for('judging-v3')['properties']
    _, theme_user = judging.build_prompt(conn, 'v2', 'judging-v4')
    assert '[Themes in force' not in theme_user                           # a theme thesis's own judgement carries no block
    store.close_view(conn, 'v2', 'due', 'pull', 4)
    _, user = judging.build_prompt(conn, 'v1', 'judging-v4')
    assert '[Themes in force' not in user                                 # a closed theme leaves the block


def test_theme_pushes_are_checked_against_the_block_stored_and_served(tmp_path):
    conn = ledger(tmp_path)
    judged(conn, 'v2', 2, 'not allowed', 2)
    schema = judging.schema_for('judging-v4')
    assert 'theme_pushes' in schema['required'] and schema['properties']['theme_pushes']['items']['properties']['push']['enum'] == ['toward_first', 'toward_last', 'none']
    base = {'rung': 3, 'reasons': 'r', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'first'}
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v2', 'push': 'toward_last'}]), 'judging-v4') == []
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v9', 'push': 'none'}]), 'judging-v4') == ['v9 is not a theme in force shown to v1']
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v2', 'push': 'none'}, {'view_id': 'v2', 'push': 'toward_last'}]), 'judging-v4') == ['v2 is named twice in theme_pushes']
    assert judging.check_answer(conn, 'v2', dict(base, rung=1, theme_pushes=[{'view_id': 'v2', 'push': 'none'}]), 'judging-v4') == ['v2 is not a theme in force shown to v2']
    assert judging.check_answer(conn, 'v1', base, 'judging-v3') == []       # v3 answers carry no field and are not asked for one
    judged(conn, 'v1', 3, 'first', 2, theme_pushes=[{'view_id': 'v2', 'push': 'toward_last'}])
    assert json.loads(conn.execute("select theme_pushes_json from judgements where view_id='v1'").fetchone()[0]) == [{'view_id': 'v2', 'push': 'toward_last'}]
    assert service.state_as_of(conn, 'v1', '2026-07-29')['theme_pushes'] == [{'view_id': 'v2', 'push': 'toward_last'}]   # behind service.view
    assert service.history(conn, 'v1')['judgements'][0]['theme_pushes'] == [{'view_id': 'v2', 'push': 'toward_last'}]
    old = store.open_read_only(str(tmp_path / 'views.sqlite'))
    assert 'theme_pushes_json' in [r[1] for r in old.execute('pragma table_info(judgements)')]
    legacy = store.open_db(str(tmp_path / 'legacy.sqlite'))
    legacy.execute('drop table judgements')
    legacy.execute('create table judgements (judgement_id integer primary key autoincrement, view_id text, seq integer, input_id text, rung integer, reasons text, '
                   'cited_evidence_json text, cited_views_json text, pushes_json text, changed integer, why_changed text, config_checksum text, call_id integer, request_sha256 text, publication_day text)')
    legacy.execute("insert into judgements (view_id, seq, input_id, rung, reasons, cited_evidence_json, cited_views_json, pushes_json, changed, why_changed, publication_day) "
                   "values ('v1', 1, 'day:2026-07-29', 2, 'old', '[]', '[]', '[]', 1, 'first', '2026-07-29')")
    store.create_view(legacy, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='x', question='x?', due_day='2027-02-24', year='FY2027',
                      rungs=ASSET_RUNGS, seq=1, input_id='i', created_at='2026-02-25T22:00:00Z')
    legacy.commit()
    assert service.state_as_of(legacy, 'v1', '2026-07-29')['theme_pushes'] == [] and service.history(legacy, 'v1')['judgements'][0]['theme_pushes'] == []


def test_v4_round_judges_themes_first_and_a_changed_theme_queues_every_open_asset_thesis_once(tmp_path):
    conn = ledger(tmp_path)
    store.create_view(conn, view_id='v3', object_id='AMD', object_kind='company', kind='asset', looks_at='FY2027 data center revenue', question='AMD?',
                      due_day='2028-02-01', year='2027', rungs=ASSET_RUNGS, seq=1, input_id='truenorth:transcript:AMD:2026-08-04', created_at='2026-08-04T22:00:00Z')
    store.link(conn, 'e1', 'v3', 1)
    store.create_view(conn, view_id='v4', object_id='MSFT', object_kind='company', kind='asset', looks_at='no evidence', question='MSFT?',
                      due_day='2027-07-30', year='FY2027', rungs=ASSET_RUNGS, seq=1, input_id='i', created_at='2026-07-29T22:00:00Z')
    conn.commit()
    order = []
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    results = judging.round_of_judgements(archive, V4, conn, ['v1', 'v2'], 5, DAY, transport=scripted(order, {'v1': [{'view_id': 'v2', 'push': 'toward_last'}]}))
    assert order == ['v2', 'v1', 'v3']                                    # the theme first; v3 was not in the day's changes but the theme changed; v4 has no evidence (D59)
    assert sorted(r['view_id'] for r in results) == ['v1', 'v2', 'v3'] and order.count('v3') == 1
    assert json.loads(conn.execute("select theme_pushes_json from judgements where view_id='v1' and seq=5").fetchone()[0]) == [{'view_id': 'v2', 'push': 'toward_last'}]
    order_v3 = []
    results = judging.round_of_judgements(model.Archive(str(tmp_path / 'archive3.sqlite')), V3, conn, ['v2'], 6, DAY, transport=scripted(order_v3))
    assert order_v3 == ['v2'] and [r['view_id'] for r in results] == ['v2']  # under judging-v3 a theme's change reaches no asset thesis


def test_resumed_round_recovers_what_an_earlier_commit_queued(tmp_path):
    conn = ledger(tmp_path)
    judged(conn, 'v2', 2, 'not allowed', 5, changed=True)                 # the theme's judgement at this seq committed; the round then died
    order = []
    results = judging.round_of_judgements(model.Archive(str(tmp_path / 'archive.sqlite')), V4, conn, [], 5, DAY, transport=scripted(order))
    assert order == ['v1'] and [r['view_id'] for r in results] == ['v1']
    # the same recovery for an explicit dependant, under any version: A judged changed at this seq, B depends on A, B unjudged
    store.create_view(conn, view_id='v5', object_id='TSM', object_kind='company', kind='asset', looks_at='FY2026 revenue', question='TSM?',
                      due_day='2027-01-31', year='2026', rungs=ASSET_RUNGS, seq=1, input_id='i', created_at='2026-07-29T22:00:00Z')
    store.link(conn, 'e1', 'v5', 1)
    store.insert(conn, 'dependencies', view_id='v5', depends_on='v1', wait_chain_view_id='', wait_year='', direction='last_end', seq=1)
    conn.commit()
    judged(conn, 'v1', 2, 'moved', 7, changed=True)
    order = []
    judging.round_of_judgements(model.Archive(str(tmp_path / 'archive2.sqlite')), V3, conn, [], 7, DAY, transport=scripted(order))
    assert order == ['v5']


def test_theme_pushes_are_checked_against_the_block_the_request_carried(tmp_path):
    conn = ledger(tmp_path)
    judged(conn, 'v2', 2, 'not allowed', 2)
    _, request_text = judging.build_prompt(conn, 'v1', 'judging-v4')
    base = {'rung': 3, 'reasons': 'r', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'first'}
    store.close_view(conn, 'v2', 'due', 'pull', 3)                                            # the theme closed while the request was out
    conn.commit()
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v2', 'push': 'none'}]), 'judging-v4', request_text) == []
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v2', 'push': 'none'}]), 'judging-v4') == ['v2 is not a theme in force shown to v1']
    store.create_view(conn, view_id='v9', object_id='ai-capex', object_kind='theme', kind='theme', looks_at='capex', question='capex?', due_day='2027-04-30', year='2026',
                      rungs=THEME_RUNGS, seq=3, input_id='i', created_at='2026-07-29T22:00:00Z')
    judged(conn, 'v9', 1, 'new theme judged after the request was built', 3)
    assert judging.check_answer(conn, 'v1', dict(base, theme_pushes=[{'view_id': 'v9', 'push': 'none'}]), 'judging-v4', request_text) == ['v9 is not a theme in force shown to v1']


def test_a_ledger_written_before_the_theme_block_gains_the_column_when_opened_for_writing(tmp_path):
    legacy = store.open_db(str(tmp_path / 'legacy.sqlite'))
    legacy.execute('drop table judgements')
    legacy.execute('create table judgements (judgement_id integer primary key autoincrement, view_id text, seq integer, input_id text, rung integer, reasons text, '
                   'cited_evidence_json text, cited_views_json text, pushes_json text, changed integer, why_changed text, config_checksum text, call_id integer, request_sha256 text, publication_day text)')
    legacy.commit(); legacy.close()
    reopened = store.open_db(str(tmp_path / 'legacy.sqlite'))
    assert 'theme_pushes_json' in [r[1] for r in reopened.execute('pragma table_info(judgements)')]
    store.create_view(reopened, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='x', question='x?', due_day='2027-02-24', year='FY2027',
                      rungs=ASSET_RUNGS, seq=1, input_id='i', created_at='2026-02-25T22:00:00Z')
    judged(reopened, 'v1', 2, 'first', 2, theme_pushes=[])
    assert reopened.execute("select theme_pushes_json from judgements where view_id='v1'").fetchone()[0] == '[]'


def test_a_judgement_the_code_refused_is_not_served_from_the_archive_again(tmp_path):
    """2026-10-27 05:30, day 2026-08-07: v11's two refused answers were archived under their requests' hashes, so every resume
    replayed the same two answers and failed again. A refused answer stays on record but answers no later identical request."""
    import pytest
    conn = ledger(tmp_path)
    judged(conn, 'v2', 2, 'not allowed', 1)
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    attempts = []

    def theme_cited_as_dependency_twice_then_right(provider, request):
        attempts.append(1)
        data = {'rung': 1, 'reasons': 'r', 'cites': [], 'cites_views': ['v2'] if len(attempts) <= 2 else [], 'pushes': [], 'changed': True,
                'why_changed': 'first', 'theme_pushes': [{'view_id': 'v2', 'push': 'none'}]}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    with pytest.raises(judging.JudgementRefused):
        judging.round_of_judgements(archive, V4, conn, ['v1'], 2, DAY, transport=theme_cited_as_dependency_twice_then_right)
    assert len(attempts) == 2
    results = judging.round_of_judgements(archive, V4, conn, ['v1'], 2, DAY, transport=theme_cited_as_dependency_twice_then_right)   # the resume
    assert len(attempts) == 3 and [r['view_id'] for r in results] == ['v1']       # re-sampled, not replayed from the archive
    assert archive.conn.execute('select count(*) from model_calls').fetchone()[0] == 3   # the refused answers stay on record


def test_the_request_names_the_closed_set_for_cites_views_when_no_dependency_is_listed(tmp_path):
    """Four of the three-month run's five retried first answers (2026-10-27) put theme ids from the block into cites_views: the
    request said "the dependency thesis ids listed above" when none were listed, and the theme ids were the only thesis ids shown."""
    conn = ledger(tmp_path)
    judged(conn, 'v2', 2, 'not allowed', 2)
    _, request_text = judging.build_prompt(conn, 'v1', 'judging-v4')
    assert 'cites_views must be empty: this thesis depends on no other thesis' in request_text
    assert 'a theme id goes only in theme_pushes, never in cites or cites_views' in request_text
    assert '.;' not in request_text
