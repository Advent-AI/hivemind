"""D260 (Alex, 2026-11-02: 门槛没有标准，按照你作为 hedge fund analyst 的认识来定): from judging-v6 a judgement is a forecast against a
reference. The answer names the reference (what the market expects) and the implied outcome (the figure or date the evidence
implies); the schema requires both from v6, code refuses an empty one, the ledger stores both beside the rung, and a ledger written
before v6 gains the columns when opened for writing. Real ledger on a temporary path."""
import os
import sys
import types

from test_theme_block import ASSET_RUNGS, DAY, ledger

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

V90 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v90.json'))
ANSWER = {'rung': 2, 'reference': 'Consensus FY2027 revenue of $392 billion sits in rung 3.', 'implied_outcome': 'Q1 $81.6bn and Q2 guide $91bn give a run-rate above $400bn.',
          'reasons': 'the implied outcome crosses the $400bn boundary', 'cites': ['e1'], 'cites_views': [], 'pushes': [{'evidence_id': 'e1', 'push': 'toward_first'}],
          'changed': True, 'why_changed': 'first', 'theme_pushes': []}


def test_v6_requires_the_reference_and_the_implied_outcome_and_v5_does_not():
    assert V90.rejudging.prompt_version == 'judging-v6'
    v6 = judging.schema_for('judging-v6')
    assert v6['required'][:3] == ['rung', 'reference', 'implied_outcome'] and v6['properties']['reference'] == {'type': 'string'}
    v5 = judging.schema_for('judging-v5')
    assert 'reference' not in v5['required'] and 'implied_outcome' not in v5['properties']
    system, _ = judging.build_prompt(ledger_for_prompt(), 'v1', 'judging-v6')
    assert 'Judge against a reference' in system and 'implied_outcome' in system


def ledger_for_prompt():
    import tempfile
    from pathlib import Path
    return ledger(Path(tempfile.mkdtemp()))


def test_an_empty_reference_is_refused_under_v6_and_both_fields_are_stored_beside_the_rung(tmp_path):
    conn = ledger(tmp_path)
    _, request_text = judging.build_prompt(conn, 'v1', 'judging-v6')
    assert judging.check_answer(conn, 'v1', ANSWER, 'judging-v6', request_text) == []
    assert judging.check_answer(conn, 'v1', dict(ANSWER, reference='  '), 'judging-v6', request_text) == [
        'reference is empty: state what the market expects and the figure or date the evidence implies']
    assert judging.check_answer(conn, 'v1', dict(ANSWER, reference='  '), 'judging-v5', request_text) == []      # v5 answers carry no stance fields
    answer = types.SimpleNamespace(data=ANSWER, call_id=0, request_sha256='x', cached=False, cost_usd=0.0)
    judging._record(conn, V90, 'v1', 2, DAY, answer)
    row = conn.execute("select rung, reference, implied_outcome from judgements where view_id='v1'").fetchone()
    assert (row['rung'], row['reference'], row['implied_outcome']) == (2, ANSWER['reference'], ANSWER['implied_outcome'])


def test_a_ledger_written_before_v6_gains_the_stance_columns_when_opened_for_writing(tmp_path):
    legacy = store.open_db(str(tmp_path / 'legacy.sqlite'))
    legacy.execute('drop table judgements')
    legacy.execute('create table judgements (judgement_id integer primary key autoincrement, view_id text, seq integer, input_id text, rung integer, reasons text, '
                   'cited_evidence_json text, cited_views_json text, pushes_json text, changed integer, why_changed text, config_checksum text, call_id integer, '
                   'request_sha256 text, publication_day text, theme_pushes_json text)')
    legacy.commit(); legacy.close()
    reopened = store.open_db(str(tmp_path / 'legacy.sqlite'))
    columns = [r[1] for r in reopened.execute('pragma table_info(judgements)')]
    assert 'reference' in columns and 'implied_outcome' in columns
    store.create_view(reopened, view_id='v1', object_id='NVDA', object_kind='company', kind='asset', looks_at='x', question='x?', due_day='2027-02-24', year='FY2027',
                      rungs=ASSET_RUNGS, seq=1, input_id='i', created_at='2026-02-25T22:00:00Z')
    v5_answer = types.SimpleNamespace(data={k: v for k, v in ANSWER.items() if k not in judging.STANCE_FIELDS}, call_id=0, request_sha256='x', cached=False, cost_usd=0.0)
    judging._record(reopened, V90, 'v1', 2, DAY, v5_answer)
    assert tuple(reopened.execute("select reference, implied_outcome from judgements where view_id='v1'").fetchone()) == (None, None)
