"""D248 applied to the identity layer (D258, 2026-11-02; e2e-loop review-2026-11-02.md §3.1): in one 14-day draw 10 of 23 questions an
article opened were ones Jev had called `part_of` an open question, and the code opened them because `part_of` fell through to 'new';
one near-identical policy question opened because the model typed it `event` against the seed's `policy_event`, and two more because
the model's event-type word for one licensing process varied (licence, approval, other).
R2-e: a candidate Jev calls part of an open question is filed under it (D248: the same outcome settles both; H1 a single deal under a
plan merges into it; H6 a small part opens no question); the typed fields still decide (a signing question never merges into an amount,
D248 item 1's recorded exception), and the collision judge may still keep a component apart under its own rule.
R2-f: `event` and `policy_event` are one measure family, and a policy process's step words are one process.
Real ledger on a temporary path; scripted Jev and model transports."""
import os
import sys

from test_collision_judge import CFG, JEV_ONLY, llm, run
from test_jev_matching import ITEM, candidate, scripted

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'src'))
from hivemind import model  # noqa: E402
from hivemind.views import identity, jev_matching, matching, store  # noqa: E402

YES_NO = [{'label': 'Yes', 'condition': 'It happened.', 'lo': None, 'hi': None}, {'label': 'No', 'condition': 'It did not.', 'lo': None, 'hi': None}]
LICENCE = dict(measure='policy_event', scope='China authorization of H200 imports', event_type='licence', basis='n/a', unit='n/a',
               period_start='2026-02-01', period_end='2027-01-31', year='2026', due_day='2027-01-31', rungs=YES_NO)


def policy_ledger(tmp_path):
    conn = store.open_db(str(tmp_path / 'views.sqlite'))
    store.ensure_writable_columns(conn)
    c = candidate('c0', **LICENCE, looks_at='H200 China authorization', question='Will Chinese authorities authorize any H200 imports by January 31, 2027?')
    store.create_view(conn, view_id='v1', object_id='NVDA', object_kind='asset', kind='asset', looks_at=c['looks_at'], question=c['question'],
                      due_day='2027-01-31', year='2026', rungs=YES_NO, seq=1, input_id='seed', created_at='2026-05-20T00:00:00')
    store.add_key(conn, 'v1', c, 1)
    conn.commit()
    return conn, c


def test_r2f_event_and_policy_event_are_one_family_and_a_policy_steps_words_are_one_process():
    key = dict(LICENCE, key_version=identity.KEY_VERSION, scope_source='model')
    assert not identity.conflicts(key, dict(LICENCE, measure='event', key_version=identity.KEY_VERSION, scope_source='watch', scope='H20/H200 China'), merging=False)
    assert not identity.conflicts(key, dict(LICENCE, event_type='approval', key_version=identity.KEY_VERSION, scope_source='model'), merging=False)
    assert not identity.conflicts(key, dict(LICENCE, event_type='other', key_version=identity.KEY_VERSION, scope_source='model'), merging=True)
    assert identity.conflicts(key, dict(LICENCE, measure='financing_amount', key_version=identity.KEY_VERSION, scope_source='model'), merging=False)
    launch = dict(measure='event', event_type='launch', basis='n/a', unit='n/a', scope='Rubin', scope_source='model', key_version=identity.KEY_VERSION,
                  period_start='2026-01-01', period_end='2026-12-31')
    assert identity.conflicts(launch, dict(launch, event_type='deployment'), merging=False)        # a deployment is still its own event type (R2-b)


def test_r2e_a_part_of_an_open_question_is_filed_under_it_unless_the_judge_keeps_it_apart(tmp_path):
    decision = run(tmp_path, JEV_ONLY, 'same_question')              # Jev alone says part_of 0.62: the part is evidence of the card, no new question
    assert (decision['outcome'], decision['target_view_id']) == ('merge', 'v1') and 'part_of' in decision['reason']
    decision = run(tmp_path / 'judged', CFG, 'distinct_question_same_matter')
    assert (decision['outcome'], decision['target_view_id']) == ('new', '')        # the judge may still hold two cards (its rule: own drivers, watched apart)


def test_r2e_a_signing_question_never_merges_into_an_amount_question(tmp_path):
    """D248 item 1's recorded exception: the Ohio lease guarantee's yes/no stays beside the financing total, whatever Jev calls it."""
    from test_jev_matching import ledger_with_view
    conn, _ = ledger_with_view(tmp_path)                                          # v1: Data Center revenue FY2027 (an amount)
    signing = candidate('c1', measure='event', event_type='deal', scope='OpenAI Ohio lease guarantee', basis='n/a', unit='n/a', rungs=YES_NO,
                        period_start='2026-01-01', period_end='2026-12-31', year='2026', due_day='2026-12-31', looks_at='Ohio guarantee signing',
                        question='Will NVIDIA sign the guarantee for the Ohio lease by December 31, 2026?')
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'a.sqlite')), JEV_ONLY, conn, ITEM, [signing], [], matching.Lists({'c1': ['v1']}, {}), [],
                                 transport=scripted({'rel__v1': ('part_of', 0.9)}))
    assert answer.data['candidates'][0]['outcome'] == 'new'


def test_r2f_the_same_licensing_decision_typed_as_an_event_or_another_step_word_merges_into_the_open_policy_question(tmp_path):
    conn, stored = policy_ledger(tmp_path)
    as_event = candidate('c1', **dict(LICENCE, measure='event', scope='H20/H200 China'), looks_at='H200 China approval',
                         question='Will Chinese authorities authorize Nvidia H200 purchases in China by 2027-01-31?')
    other_word = candidate('c2', **dict(LICENCE, event_type='approval', scope='China approval of H200 imports'), looks_at='H200 import approval',
                           question='Will China approve imports of Nvidia H200 chips by 2027-01-31?')
    answer = jev_matching.decide(model.Archive(str(tmp_path / 'a.sqlite')), JEV_ONLY, conn, ITEM, [as_event, other_word], [], matching.Lists({'c1': ['v1'], 'c2': ['v1']}, {}), [],
                                 transport=scripted({'rel__v1': ('same_quantity_or_event', 0.85)}))
    assert {d['id']: (d['outcome'], d['target_view_id']) for d in answer.data['candidates']} == {'c1': ('merge', 'v1'), 'c2': ('merge', 'v1')}
