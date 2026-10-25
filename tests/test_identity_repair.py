"""D155 / grouping-improvement-plan Step B: identity repair on stored cases and real temporary ledgers."""
import json
import sqlite3
from pathlib import Path

import pytest

from test_keyed_views import UNIVERSE, ITEM, TEXT, EVIDENCE, candidate
from hivemind import config, dispatch, extraction, model, replay
from hivemind.views import matching, store, writing
from hivemind.views import round as rounds

CASES = json.loads((Path(__file__).parent / 'fixtures/keyed-repair-cases.json').read_text())


def handover(candidates, evidence=()):
    return extraction.Handover(list(evidence), candidates, [], 0, '', False, 0)


def checked_new(candidates):
    return matching.Checked({c['id']: ('new', None, []) for c in candidates}, {}, [], {})


def test_stored_multiyear_and_ambiguous_scope_survive_unchanged():
    """B periods/scopes: the recorded failures, not invented descriptions, retain their meaning."""
    for case in CASES[:2]:
        _, kept, _ = extraction.sift(case['answer'], case['item'], case['text'], set(case['shown_ids']), UNIVERSE)
        raw = case['answer']['candidates'][0]
        assert [(c['scope'], c['period_start'], c['period_end']) for c in kept] == [
            (raw['scope'], raw['period_start'], raw['period_end'])]
    assert UNIVERSE.scope_and_source('ai-capex', 'spend_total', 'AI hyperscalers') == ('AI hyperscalers', 'watch')


def test_restored_candidates_keep_department_and_cash_qualifiers():
    """B value/reader: lifting the gate must not expose the old blanket scope erasure."""
    for case, measure, scope in [(CASES[2], 'operating_loss', 'Reality Labs'), (CASES[3], 'capex', 'cash CapEx')]:
        _, kept, _ = extraction.sift(case['answer'], case['item'], case['text'], set(case['shown_ids']), UNIVERSE)
        assert any(c['measure'] == measure and c['scope'] == scope and c['scope_source'] == 'model' for c in kept)


@pytest.mark.parametrize('year,expected', [
    ('FY2027', ('2026-02-01', '2027-01-31')),
    ('2026自然年', ('2026-01-01', '2026-12-31')),
    ('CY 2026', ('2026-01-01', '2026-12-31')),
    ('2025-2027自然年', None), ('not a year 2027', None),
])
def test_period_conversion_is_a_full_match(year, expected):
    assert UNIVERSE.fiscal_period('NVDA', year) == expected


def test_invalid_period_does_not_reach_writer():
    c = candidate('c1', year='2025-2027自然年', period_end='2027-02-30')
    _, kept, dropped = extraction.sift({'candidates': [c], 'evidence': EVIDENCE}, ITEM, TEXT, set(), UNIVERSE)
    assert not kept and any(reason.startswith('invalid period:') for _, reason in dropped)


def test_event_type_distinguishes_search_identity_and_merge(tmp_path):
    """B class: a product's announcement and shipment are distinct events at every reader."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    ship = candidate('c1', measure='event', scope='Rubin', scope_source='watch', event_type='shipment')
    vid = writing.write(conn, UNIVERSE, 1, ITEM, handover([ship]), checked_new([ship]), {}).new_views['c1']
    launch = dict(ship, id='c2', event_type='launch')
    assert matching.key_matches(conn, launch) == []
    assert not matching._same_key(store.view_key(conn, vid), launch, 'NVDA')
    for outcome, target in [('new', ''), ('merge', vid)]:
        raw = {'candidates': [{'id': 'c2', 'outcome': outcome, 'target_view_id': target, 'dependencies': []}], 'evidence': []}
        result = matching.check(conn, UNIVERSE, raw, [launch], [], matching.Lists({'c2': [vid]}, {}), [])
        assert result.outcomes['c2'][0] == 'new'


def test_same_answer_coalesces_without_losing_evidence(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    a = candidate('c1', scope_source='watch')
    b = dict(a, id='c2', question='Another wording')
    e = [dict(EVIDENCE[0], links=['c1']), dict(EVIDENCE[1], links=['c2'])]
    written = writing.write(conn, UNIVERSE, 1, ITEM, handover([a, b], e), checked_new([a, b]), {})
    assert written.new_views['c1'] == written.new_views['c2']
    assert len(store.evidence_in_force(conn, written.new_views['c1'])) == 2


def test_coalesced_dependency_is_refused_before_matching_retry_ends(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    a = candidate('c1', scope_source='watch')
    b = dict(a, id='c2')
    dep = {'view_id': 'c2', 'wait_chain_view_id': '', 'wait_year': '', 'direction': 'same'}
    raw = {'candidates': [{'id': c['id'], 'outcome': 'new', 'target_view_id': '', 'dependencies': [dep] if c is a else []} for c in [a, b]], 'evidence': []}
    result = matching.check(conn, UNIVERSE, raw, [a, b], [], matching.Lists({'c1': [], 'c2': []}, {}), [])
    assert any('coalesced dependencies' in reason for reason in result.refusals)
    raw['candidates'][0]['dependencies'] = []
    assert not matching.check(conn, UNIVERSE, raw, [a, b], [], matching.Lists({'c1': [], 'c2': []}, {}), []).refusals


def test_unknown_basis_and_legacy_key_never_authorize_automatic_merge():
    c = candidate('c1', scope_source='watch')
    key = dict(c, scope_key='data center')
    assert matching._same_key(key, c, 'NVDA')
    assert not matching._same_key(key, dict(c, basis='GAAP'), 'NVDA')
    assert not matching._same_key(dict(key, key_version=None), c, 'NVDA')


def test_conflict_rolls_back_entire_write_and_free_scope_remains_free(tmp_path):
    """B write-in-progress: an earlier insert cannot leak when a later key conflicts."""
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    old = candidate('old', scope_source='watch')
    writing.write(conn, UNIVERSE, 1, ITEM, handover([old]), checked_new([old]), {})
    conn.commit()
    free = candidate('free', scope='Uncertain new business', scope_source='model')
    duplicate = dict(old, id='duplicate')
    with pytest.raises(writing.WriteConflict, match='existing exact identity'):
        writing.write(conn, UNIVERSE, 2, ITEM, handover([free, duplicate]), checked_new([free, duplicate]), {})
    assert conn.execute('select count(*) from views').fetchone()[0] == 1
    free2 = dict(free, id='free2')
    result = writing.write(conn, UNIVERSE, 3, ITEM, handover([free, free2]), checked_new([free, free2]), {})
    assert result.new_views['free'] != result.new_views['free2']


def test_writer_failure_resumes_from_same_handover_without_partial_rows(tmp_path):
    """B state table: a storage failure retains the handover, retries the same sequence, then skips a resend."""
    root = Path(__file__).resolve().parents[1]
    cfg = config.load(root / 'poc/config/poc-v17.json')
    archive = model.Archive(str(tmp_path / 'archive.sqlite'))
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    item = dict(ITEM, text=TEXT, publisher='NVIDIA', published_at='2026-05-20T12:00:00Z', source_uri='https://example.test/earnings')
    raw_candidate = {k: v for k, v in candidate('c1').items() if k not in ('key_version', 'scope_source')}
    calls = []

    def transport(provider, request):
        name = request['response_format']['json_schema']['name']
        calls.append(name)
        if name == 'extraction':
            data = {'candidates': [raw_candidate], 'evidence': EVIDENCE[:1]}
        else:
            data = {'candidates': [{'id': 'c1', 'outcome': 'new', 'target_view_id': '', 'reason': 'new', 'dependencies': []}], 'evidence': []}
        return {'choices': [{'message': {'content': json.dumps(data)}}]}

    route = dispatch.route(conn, item, UNIVERSE)
    conn.execute("create trigger fail_write before insert on evidence begin select raise(abort, 'storage fault'); end")
    result = rounds.run(conn, archive, cfg, UNIVERSE, item, route.sequence_no, transport=transport)
    assert 'storage fault' in result.failed
    assert conn.execute('select count(*) from views').fetchone()[0] == 0
    saved_calls = len(calls)
    again = dispatch.route(conn, item, UNIVERSE)
    assert (again.sequence_no, again.resume_from) == (route.sequence_no, 'written')
    conn.execute('drop trigger fail_write')
    result = rounds.run(conn, archive, cfg, UNIVERSE, item, again.sequence_no, resume_from=again.resume_from, transport=transport)
    assert not result.failed and result.new_views == 1 and len(calls) == saved_calls
    assert dispatch.route(conn, item, UNIVERSE).kind == 'skipped'


def test_failed_replay_day_is_not_completed_and_can_resume(tmp_path):
    """B state table: entry-point failure cannot advance past the failed date."""
    root = Path(__file__).resolve().parents[1]
    path = tmp_path / 'items.sqlite'
    conn = sqlite3.connect(path)
    conn.execute('create table items (input_id, publisher, published_at, publication_day, category, source_uri, text, object_identifiers, feed, copy_of, klass)')
    conn.execute('insert into items values (?,?,?,?,?,?,?,?,?,?,?)',
                 ('news:one', 'NVIDIA', '2026-05-20T12:00:00Z', '2026-05-20', 'T7', 'https://example.test/one', TEXT,
                  json.dumps([{'value': 'NVDA'}]), 1, None, '新闻'))
    conn.commit()
    args = dict(testdb_path=str(path), views_path=str(tmp_path / 'views.sqlite'), archive=model.Archive(str(tmp_path / 'archive.sqlite')),
                cfg=config.load(root / 'poc/config/poc-v16.json'), universe=UNIVERSE,
                from_day='2026-05-20', until_day='2026-05-20', log=lambda *args: None)

    def unavailable(*args):
        raise model.TransportError('offline')

    with pytest.raises(RuntimeError, match='remains resumable'):
        replay.run(**args, transport=unavailable)
    ledger = store.open_db(args['views_path'])
    assert store.last_completed_day(ledger) is None
    result = replay.run(**args, transport=lambda *args: {'choices': [{'message': {'content': '{"candidates":[],"evidence":[]}'}}]})
    assert result['failed'] == 0 and store.last_completed_day(ledger) == '2026-05-20'
    assert ledger.execute('select count(distinct sequence_no) from processing_steps where input_id=?', ('news:one',)).fetchone()[0] == 1


def test_legacy_database_reads_without_schema_mutation_then_upgrades_at_open(tmp_path):
    """B legacy value/reader row: reads stay read-only, new columns never certify old keys."""
    path = tmp_path / 'views.sqlite'
    conn = store.open_db(str(path))
    c = candidate('c1', scope_source='watch')
    writing.write(conn, UNIVERSE, 1, ITEM, handover([c]), checked_new([c]), {})
    conn.commit()
    conn.execute('alter table view_keys drop column key_version')
    conn.execute('alter table view_keys drop column scope_source')
    conn.execute('alter table rungs drop column lo')
    conn.execute('alter table rungs drop column hi')
    conn.commit()
    readonly = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    readonly.row_factory = sqlite3.Row
    assert store.view_key(readonly, 'v1')['scope_source'] == 'model'
    assert 'key_version' not in {r[1] for r in readonly.execute('pragma table_info(view_keys)')}
    upgraded = store.open_db(str(path))
    assert store.view_key(upgraded, 'v1')['key_version'] is None
    assert {'lo', 'hi'} <= {r[1] for r in upgraded.execute('pragma table_info(rungs)')}
