"""D198: a judgement reads the evidence in view, not everything in force: what arrived within its last READINGS judgements and
what one of its last BASIS judgements cited. The rest stays in force in the ledger and is counted, not shown. Gated on the
judging prompt version (v5). Real ledger on a temporary path."""
import os
import sys

from test_theme_block import ASSET_RUNGS, DAY, ledger

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import config  # noqa: E402
from hivemind.views import judging, store  # noqa: E402

V5 = config.load(os.path.join(ROOT, 'poc', 'config', 'poc-v30.json'))
ANSWER = {'rung': 3, 'reasons': 'r', 'cites': [], 'cites_views': [], 'pushes': [], 'changed': True, 'why_changed': 'first', 'theme_pushes': []}


def piece(conn, evidence_id, view_id, seq, tier='third_party_view'):
    store.add_evidence(conn, evidence_id=evidence_id, quote=f'quote {evidence_id}', one_line=f'line {evidence_id}', speaker='analyst', original_who='',
                       original_day='2026-07-10', tier=tier, event_time='', seq=seq, input_id=f'gnews:{evidence_id}')
    store.add_source(conn, evidence_id, f'gnews:{evidence_id}', 'T7', '2026-07-10', 'p1', seq)
    store.link(conn, evidence_id, view_id, seq)
    conn.commit()


def judged_citing(conn, view_id, seq, cites):
    import types
    answer = types.SimpleNamespace(data=dict(ANSWER, cites=cites), call_id=0, request_sha256='x', cached=False, cost_usd=0.0)
    judging._record(conn, V5, view_id, seq, DAY, answer)


def test_a_young_thesis_reads_everything_in_force(tmp_path):
    conn = ledger(tmp_path)                          # v1 holds e1 (linked at seq 1)
    piece(conn, 'e3', 'v1', 2)
    shown, hidden = judging.evidence_in_view(conn, 'v1', 'judging-v5')
    assert [p['evidence_id'] for p in shown] == ['e1', 'e3'] and hidden == 0
    for seq in range(3, 3 + judging.READINGS - 1):
        judged_citing(conn, 'v1', seq, [])
    shown, hidden = judging.evidence_in_view(conn, 'v1', 'judging-v5')
    assert len(shown) == 2 and hidden == 0            # fewer than READINGS judgements: still everything


def test_after_its_readings_an_uncited_piece_leaves_view_and_is_counted(tmp_path):
    conn = ledger(tmp_path)
    piece(conn, 'e3', 'v1', 2)                        # e1 and e3 arrive before five judgements that never cite e3
    for seq in range(3, 3 + judging.READINGS):
        judged_citing(conn, 'v1', seq, ['e1'])        # e1 is the basis
    piece(conn, 'e4', 'v1', 20)                       # a fresh arrival
    shown, hidden = judging.evidence_in_view(conn, 'v1', 'judging-v5')
    assert [p['evidence_id'] for p in shown] == ['e1', 'e4'] and hidden == 1
    assert [p['evidence_id'] for p in judging.evidence_in_view(conn, 'v1', 'judging-v4')[0]] == ['e1', 'e3', 'e4']   # v4 reads in force


def test_the_basis_decays_and_a_replacement_arrives_with_its_predecessor(tmp_path):
    conn = ledger(tmp_path)
    piece(conn, 'e3', 'v1', 2)
    judged_citing(conn, 'v1', 3, ['e3'])              # cited once, long ago
    for seq in range(4, 4 + judging.BASIS):
        judged_citing(conn, 'v1', seq, ['e1'])        # ten later judgements cite only e1
    assert [p['evidence_id'] for p in judging.evidence_in_view(conn, 'v1', 'judging-v5')[0]] == ['e1']
    piece(conn, 'e5', 'v1', 30)                       # e5 replaces e1 (a later account by the same party)
    store.replace(conn, 'e1', 'e5', '2026-07-30', 30)
    conn.commit()
    shown, hidden = judging.evidence_in_view(conn, 'v1', 'judging-v5')
    assert [p['evidence_id'] for p in shown] == ['e5'] and shown[0]['replaced']['evidence_id'] == 'e1' and hidden == 1


def test_the_request_states_the_count_and_the_check_holds_the_answer_to_what_was_shown(tmp_path):
    conn = ledger(tmp_path)
    piece(conn, 'e3', 'v1', 2)
    for seq in range(3, 3 + judging.READINGS):
        judged_citing(conn, 'v1', seq, ['e1'])
    _, request_text = judging.build_prompt(conn, 'v1', 'judging-v5')
    assert '[Evidence in view under this thesis, 1 items]' in request_text
    assert '[Not shown: 1 more pieces in force, read in earlier judgements; the previous conclusion carries them]' in request_text
    assert judging.evidence_shown_in(request_text) == {'e1'}
    assert judging.check_answer(conn, 'v1', dict(ANSWER, cites=['e1'], pushes=[{'evidence_id': 'e1', 'push': 'none'}]), 'judging-v5', request_text) == []
    assert judging.check_answer(conn, 'v1', dict(ANSWER, cites=['e3']), 'judging-v5', request_text) == ['e3 is not among the evidence shown to v1']
    assert judging.check_answer(conn, 'v1', dict(ANSWER, pushes=[{'evidence_id': 'e3', 'push': 'none'}]), 'judging-v5', request_text) == ['push on e3 which was not shown to v1']
    assert judging.check_answer(conn, 'v1', dict(ANSWER, cites=['e3']), 'judging-v5') == ['e3 is not among the evidence shown to v1']   # computed from the ledger when the text is not given
    assert judging.check_answer(conn, 'v1', dict(ANSWER, cites=['e3']), 'judging-v4') == []                                            # v4: in force
