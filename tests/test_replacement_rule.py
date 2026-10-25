"""D167: the writer owns the replacement rule (06-views, the Replace row), the measure vocabulary is version-gated, and the relation
question carries both sides' defining quotes. Real ledgers on temporary paths."""
import os
import sys

from test_keyed_views import ITEM, UNIVERSE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction  # noqa: E402
from hivemind.views import jev_matching, matching, store, writing  # noqa: E402


def ledger(tmp_path, old_tier='fact', old_who='NVIDIA'):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.ensure_writable_columns(conn)
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at='Data Center annual revenue', question='FY2027 Data Center revenue?',
                      due_day='2027-02-28', year='FY2027', rungs=[{'label': 'high', 'condition': '> $300bn', 'lo': 300, 'hi': None}, {'label': 'low', 'condition': '< $300bn', 'lo': None, 'hi': 300}],
                      seq=1, input_id='seed', created_at='2026-05-20T00:00:00')
    store.add_evidence(conn, evidence_id='e1', quote='Data Center revenue was $51 billion in the quarter.', one_line='DC revenue $51bn', speaker=old_who, original_who=old_who,
                       original_day='2026-05-20', tier=old_tier, event_time='', seq=1, input_id='seed')
    store.add_source(conn, 'e1', 'seed', 'T4', '2026-05-20', '', 1)
    store.link(conn, 'e1', 'v1', 1)
    conn.commit()
    return conn


def piece(tier, who, day, quote='Data Center revenue will be $60 billion next quarter.'):
    return {'id': 'x1', 'links': ['v1'], 'tier': tier, 'speaker': who, 'original_who': who, 'original_day': day, 'event_time': '', 'one_line': quote[:60], 'quote': quote, 'location': ''}


def write_replace(conn, incoming, said_day):
    handover = type('H', (), {'candidates': [], 'evidence': [incoming], 'dropped': [], 'new_groups': []})()
    checked = matching.Checked({}, {('x1', 'v1'): ('replace', 'e1', said_day)}, [], {})
    written = writing.write(conn, UNIVERSE, 2, dict(ITEM, input_id='later', publication_day='2026-08-27'), handover, checked, {})
    conn.commit()
    return written


def test_a_third_party_view_never_retires_a_fact_and_is_stored_as_new(tmp_path):
    conn = ledger(tmp_path, old_tier='fact')
    written = write_replace(conn, piece('third_party_view', 'Bernstein', '2026-08-27'), '2026-08-27')
    assert conn.execute('select count(*) from replacements').fetchone()[0] == 0
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 2 and written.evidence_ids['x1'] == 'e2'
    assert any('replacement of e1 refused (third_party_view cannot replace fact)' in n for n in written.notes)
    assert sorted(r[0] for r in conn.execute("select evidence_id from evidence_links where view_id='v1'")) == ['e1', 'e2']


def test_a_party_statement_with_a_later_day_replaces_the_fact(tmp_path):
    conn = ledger(tmp_path, old_tier='fact')
    write_replace(conn, piece('party_statement', 'NVIDIA', '2026-08-27'), '2026-08-27')
    assert [tuple(r) for r in conn.execute('select old_evidence_id, new_evidence_id from replacements')] == [('e1', 'e2')]


def test_an_undated_piece_cannot_replace(tmp_path):
    conn = ledger(tmp_path, old_tier='party_statement')
    written = write_replace(conn, piece('party_statement', 'NVIDIA', 'Not stated'), 'Not stated')
    assert conn.execute('select count(*) from replacements').fetchone()[0] == 0
    assert any('no stated day' in n for n in written.notes)


def test_a_view_replaces_only_the_same_party_s_earlier_view(tmp_path):
    conn = ledger(tmp_path, old_tier='third_party_view', old_who='Morgan Stanley')
    write_replace(conn, piece('third_party_view', 'Morgan Stanley', '2026-08-27'), '2026-08-27')
    assert conn.execute('select count(*) from replacements').fetchone()[0] == 1
    conn2 = ledger(tmp_path / 'b', old_tier='third_party_view', old_who='Morgan Stanley') if (tmp_path / 'b').mkdir() is None else None
    written = write_replace(conn2, piece('third_party_view', 'Jefferies', '2026-08-27'), '2026-08-27')
    assert conn2.execute('select count(*) from replacements').fetchone()[0] == 0 and any("another party's third party view" in n for n in written.notes)


def test_measure_vocabulary_is_version_gated():
    v9 = extraction.schema_for('v9')['properties']['candidates']['items']['properties']['measure']['enum']
    v10 = extraction.schema_for('v10')['properties']['candidates']['items']['properties']['measure']['enum']
    assert 'market_size' not in v9 and 'project_cost' not in v9
    assert 'market_size' in v10 and 'project_cost' in v10 and set(v9) < set(v10)


def test_the_relation_question_carries_both_sides_defining_quotes(tmp_path):
    conn = ledger(tmp_path)
    assert 'Evidence: [NVIDIA 2026-05-20] Data Center revenue was $51 billion' in jev_matching.thesis_text(conn, 'v1')
    candidate = {'kind': 'asset', 'object': 'NVDA', 'looks_at': 'DC revenue', 'year': 'FY2027', 'due_day': '2027-02-28', 'question': '?', 'rungs': [], 'evidence_ids': ['x1']}
    state = jev_matching.candidate_state(candidate, [piece('fact', 'NVIDIA', '2026-08-27')])
    assert '[NVIDIA 2026-08-27] Data Center revenue will be $60 billion' in state
    assert 'two estimates or figures of that one quantity' in jev_matching.RELATIONS['same_quantity_or_event']


def test_a_rumour_is_replaced_by_an_official_or_its_own_source_never_by_another_party_s_view(tmp_path):
    # log row 47: a commentator's reaction replaced the WSJ-report rumour twice; 06-views: an official confirms or denies, the source revises
    conn = ledger(tmp_path, old_tier='rumour', old_who='The Wall Street Journal')
    written = write_replace(conn, piece('third_party_view', 'Futuriom', '2026-07-29'), '2026-07-29')
    assert conn.execute('select count(*) from replacements').fetchone()[0] == 0 and any("another party's" in n for n in written.notes)
    conn2 = ledger(tmp_path / 'b', old_tier='rumour', old_who='The Wall Street Journal') if (tmp_path / 'b').mkdir() is None else None
    write_replace(conn2, piece('rumour', 'The Wall Street Journal', '2026-07-29'), '2026-07-29')
    assert conn2.execute('select count(*) from replacements').fetchone()[0] == 1
    conn3 = ledger(tmp_path / 'c', old_tier='rumour', old_who='The Wall Street Journal') if (tmp_path / 'c').mkdir() is None else None
    write_replace(conn3, piece('party_statement', 'NVIDIA', '2026-07-29'), '2026-07-29')
    assert conn3.execute('select count(*) from replacements').fetchone()[0] == 1   # an official's denial or confirmation


def test_the_replace_criterion_is_about_one_statement_or_number():
    # 06-views line 197: replacement applies to a statement or number, not the whole report (log row 47)
    assert 'a later version of the same statement or number' in jev_matching.PIECES['supersedes']
    assert 'another statement on the same topic is not this' in jev_matching.PIECES['supersedes']
