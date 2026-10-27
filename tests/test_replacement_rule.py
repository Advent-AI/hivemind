"""D167/D202: the writer owns the revision rule (06-views, the Replace row, read since D202 as "revises, both in force"): a `replace`
decision records a revision only when the incoming piece has a stated day, a tier at least the old piece's and, for views and rumours,
the same party; nothing is retired. The measure vocabulary is version-gated, and the relation question carries both sides' defining
quotes. Real ledgers on temporary paths."""
import os
import sys

from test_keyed_views import ITEM, UNIVERSE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import extraction  # noqa: E402
from hivemind.views import jev_matching, matching, store, writing  # noqa: E402


def ledger(tmp_path, old_tier='fact', old_who='NVIDIA', old_quote='Data Center revenue was $51 billion in the quarter.', old_line='DC revenue $51bn', old_speaker=None):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.ensure_writable_columns(conn)
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at='Data Center annual revenue', question='FY2027 Data Center revenue?',
                      due_day='2027-02-28', year='FY2027', rungs=[{'label': 'high', 'condition': '> $300bn', 'lo': 300, 'hi': None}, {'label': 'low', 'condition': '< $300bn', 'lo': None, 'hi': 300}],
                      seq=1, input_id='seed', created_at='2026-05-20T00:00:00')
    store.add_evidence(conn, evidence_id='e1', quote=old_quote, one_line=old_line, speaker=old_speaker or old_who, original_who=old_who,
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


def test_a_third_party_view_never_revises_a_fact_and_is_stored_as_new(tmp_path):
    conn = ledger(tmp_path, old_tier='fact')
    written = write_replace(conn, piece('third_party_view', 'Bernstein', '2026-08-27'), '2026-08-27')
    assert conn.execute('select count(*) from revisions').fetchone()[0] == 0
    assert conn.execute('select count(*) from evidence').fetchone()[0] == 2 and written.evidence_ids['x1'] == 'e2'
    assert any('revision of e1 refused (third_party_view cannot revise fact)' in n for n in written.notes)
    assert sorted(r[0] for r in conn.execute("select evidence_id from evidence_links where view_id='v1'")) == ['e1', 'e2']


def test_a_party_statement_with_a_later_day_revises_the_fact_and_both_stay_in_force(tmp_path):
    conn = ledger(tmp_path, old_tier='fact')
    write_replace(conn, piece('party_statement', 'NVIDIA', '2026-08-27'), '2026-08-27')
    assert [tuple(r) for r in conn.execute('select old_evidence_id, new_evidence_id from revisions')] == [('e1', 'e2')]
    assert conn.execute('select count(*) from replacements').fetchone()[0] == 0 and not store.is_replaced(conn, 'e1')
    in_force = {p['evidence_id']: p for p in store.evidence_in_force(conn, 'v1')}
    assert set(in_force) == {'e1', 'e2'} and in_force['e2']['revises']['evidence_id'] == 'e1' and in_force['e1']['revises'] is None


def test_an_undated_piece_cannot_revise(tmp_path):
    conn = ledger(tmp_path, old_tier='party_statement')
    written = write_replace(conn, piece('party_statement', 'NVIDIA', 'Not stated'), 'Not stated')
    assert conn.execute('select count(*) from revisions').fetchone()[0] == 0
    assert any('no stated day' in n for n in written.notes)


def test_a_view_revises_only_the_same_party_s_earlier_view(tmp_path):
    conn = ledger(tmp_path, old_tier='third_party_view', old_who='Morgan Stanley')
    write_replace(conn, piece('third_party_view', 'Morgan Stanley', '2026-08-27'), '2026-08-27')
    assert conn.execute('select count(*) from revisions').fetchone()[0] == 1
    conn2 = ledger(tmp_path / 'b', old_tier='third_party_view', old_who='Morgan Stanley') if (tmp_path / 'b').mkdir() is None else None
    written = write_replace(conn2, piece('third_party_view', 'Jefferies', '2026-08-27'), '2026-08-27')
    assert conn2.execute('select count(*) from revisions').fetchone()[0] == 0 and any("another party's third party view" in n for n in written.notes)


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


def test_a_rumour_is_revised_by_an_official_or_its_own_source_never_by_another_party_s_view(tmp_path):
    # log row 47: a commentator's reaction replaced the WSJ-report rumour twice; 06-views: an official confirms or denies, the source revises
    conn = ledger(tmp_path, old_tier='rumour', old_who='The Wall Street Journal')
    written = write_replace(conn, piece('third_party_view', 'Futuriom', '2026-07-29'), '2026-07-29')
    assert conn.execute('select count(*) from revisions').fetchone()[0] == 0 and any("another party's" in n for n in written.notes)
    conn2 = ledger(tmp_path / 'b', old_tier='rumour', old_who='The Wall Street Journal') if (tmp_path / 'b').mkdir() is None else None
    write_replace(conn2, piece('rumour', 'The Wall Street Journal', '2026-07-29'), '2026-07-29')
    assert conn2.execute('select count(*) from revisions').fetchone()[0] == 1
    conn3 = ledger(tmp_path / 'c', old_tier='rumour', old_who='The Wall Street Journal') if (tmp_path / 'c').mkdir() is None else None
    write_replace(conn3, piece('party_statement', 'NVIDIA', '2026-07-29'), '2026-07-29')
    assert conn3.execute('select count(*) from revisions').fetchone()[0] == 1 and len(store.evidence_in_force(conn3, 'v1')) == 2   # an official's denial or confirmation: recorded, nothing retired (D202)


def test_the_replace_criterion_is_about_one_statement_or_number():
    # 06-views line 197: replacement applies to a statement or number, not the whole report (log row 47)
    assert 'a later version of the same statement or number' in jev_matching.PIECES['supersedes']
    assert 'another statement on the same topic is not this' in jev_matching.PIECES['supersedes']


def test_a_denial_never_retires_the_report_it_denies_and_the_judge_sees_both(tmp_path):
    """D202, gold G09 (seq 77 of the v29 run): SemiAnalysis's Rubin Ultra cancellation report (rumour) under v1; NVIDIA's "our roadmap is
    intact" arrives with a `replace` decision. Both pieces stay in force; the judge's request lists both and names the revision."""
    from hivemind.views import judging
    conn = ledger(tmp_path, old_tier='rumour', old_who='SemiAnalysis', old_speaker='The Decoder, relaying a SemiAnalysis report',
                  old_quote='The more powerful version of the upcoming Rubin Ultra chip with four compute dies has also been canceled.',
                  old_line='The Decoder reported, citing SemiAnalysis, that Nvidia had canceled the four-die Rubin Ultra.')
    written = write_replace(conn, piece('party_statement', 'NVIDIA representative', '2026-07-06', quote='Our roadmap is intact.'), '2026-07-06')
    assert written.evidence_ids['x1'] == 'e2' and not store.is_replaced(conn, 'e1')
    assert [p['evidence_id'] for p in store.evidence_in_force(conn, 'v1')] == ['e1', 'e2']
    text = '\n'.join(judging._lines_english(conn, 'v1', store.view(conn, 'v1'), store.rungs_of(conn, 'v1'), store.evidence_in_force(conn, 'v1'), [], None))
    assert 'canceled the four-die Rubin Ultra' in text and 'Our roadmap is intact.' in text and 'the matcher read it as a later version of e1' in text and 'It replaces' not in text


def test_a_ledger_written_before_the_revisions_table_still_reads(tmp_path):
    """D202 new path × old checks: the served snapshots and the paused runs have no revisions table and are opened read-only."""
    import sqlite3
    conn = ledger(tmp_path)
    conn.execute('drop table revisions'); conn.commit(); conn.close()
    old = store.open_read_only(str(tmp_path / 'views.sqlite'))
    assert [p['evidence_id'] for p in store.evidence_in_force(old, 'v1')] == ['e1'] and store.evidence_in_force(old, 'v1')[0]['revises'] is None


def test_an_older_statement_arriving_late_is_stored_and_linked_as_new_not_dropped(tmp_path):
    """D202: before, a `replace` decision whose incoming piece was said before the target was logged in late_statements and linked
    nowhere (the v34 and v34b weeks each dropped SemiAnalysis's Kyber delay report this way; the three-month run dropped the SharonAI
    backstop figure). Now it is one more piece in force, with no revision relation, and the log row stays for the record."""
    conn = ledger(tmp_path, old_tier='party_statement', old_who='NVIDIA')          # e1 said 2026-05-20
    written = write_replace(conn, piece('third_party_view', 'SemiAnalysis', '2026-05-19', quote='Kyber NVL144 has been pushed back to 2028.'), '2026-05-19')
    assert written.evidence_ids['x1'] == 'e2'
    assert sorted(r[0] for r in conn.execute("select evidence_id from evidence_links where view_id='v1'")) == ['e1', 'e2']
    assert conn.execute('select count(*) from revisions').fetchone()[0] == 0
    assert conn.execute("select reason from late_statements").fetchone()[0].startswith('older than e1')
    assert any('older than e1' in n and 'stored as new' in n for n in written.notes)


def test_an_unknown_statement_day_is_stored_unknown_not_as_the_publication_day(tmp_path):
    """D203: a piece whose day the text does not state is stored with an empty original_day; the judge's request shows no day for it."""
    from hivemind.views import judging
    conn = ledger(tmp_path, old_tier='party_statement', old_who='NVIDIA')
    handover = type('H', (), {'candidates': [], 'evidence': [piece('party_statement', 'NVIDIA', '', quote='Data Center revenue will exceed $300 billion this year.')], 'dropped': [], 'new_groups': []})()
    checked = matching.Checked({}, {('x1', 'v1'): ('new', None, '')}, [], {})
    written = writing.write(conn, UNIVERSE, 2, dict(ITEM, input_id='later', publication_day='2026-08-27'), handover, checked, {})
    conn.commit()
    stored = store.evidence(conn, written.evidence_ids['x1'])
    assert stored['original_day'] == ''
    text = '\n'.join(judging._lines_english(conn, 'v1', store.view(conn, 'v1'), store.rungs_of(conn, 'v1'), store.evidence_in_force(conn, 'v1'), [], None))
    line = next(l for l in text.split('\n') if l.startswith('- e2 '))
    assert 'original source NVIDIA ; from later 2026-08-27' in line      # the statement day is blank; the outlet's day stays


def test_a_wrong_repeat_label_loses_no_content_and_the_judge_sees_both_with_the_label(tmp_path):
    """D204, repeats census #11: a Yahoo summary carrying the compute/networking split ($60bn/$15bn) was judged a repeat of a
    "hyperscalers ~50%" estimate and its text was discarded. Now the record is stored, linked, related; the judge reads both and the
    relation is labelled as the matcher's opinion."""
    from hivemind.views import judging
    conn = ledger(tmp_path, old_tier='third_party_view', old_who='24/7 Wall St.', old_quote='Hyperscalers account for about 50% of NVIDIA Data Center revenue.', old_line='hyperscalers about 50% of DC revenue')
    incoming = piece('fact', 'NVIDIA', '2026-07-23', quote='Data Center revenue of $75 billion included $60 billion of compute and $15 billion of networking; hyperscalers were roughly half.')
    handover = type('H', (), {'candidates': [], 'evidence': [incoming], 'dropped': [], 'new_groups': []})()
    checked = matching.Checked({}, {('x1', 'v1'): ('repeat', 'e1', '2026-07-23')}, [], {})
    written = writing.write(conn, UNIVERSE, 2, dict(ITEM, input_id='later', publication_day='2026-07-23'), handover, checked, {})
    conn.commit()
    assert written.evidence_ids['x1'] == 'e2' and store.evidence(conn, 'e2')['quote'].startswith('Data Center revenue of $75 billion')
    text = '\n'.join(judging._lines_english(conn, 'v1', store.view(conn, 'v1'), store.rungs_of(conn, 'v1'), store.evidence_in_force(conn, 'v1'), [], None))
    assert '$60 billion of compute' in text and 'the matcher read this as the same claim as e1' in text and 'counts one claim' in text

