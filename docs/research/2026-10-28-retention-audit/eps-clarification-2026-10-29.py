"""Preserve prior references and apply Alex's later EPS clarification."""
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE / 'gold-user-2026-10-29-v2' / 'reference.json'
OUT = HERE / 'gold-user-2026-10-29-v3'
CLARIFICATION = '2028 EPS 预测可以留下来啊，我的意思是因为太久远了，现在才2026.。。'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def main():
    old = json.loads(OLD.read_text())
    assert old['ready_for_scoring'] is False
    assert next(x for x in old['decisions'] if x['question'] == '2')['decision'] == 'exclude'
    candidate = copy.deepcopy(old)
    candidate['prior_reference_sha256'] = sha(OLD)
    candidate['user_clarifications'] = [{'question': '2', 'verbatim': CLARIFICATION,
                                          'interpretation': 'May be retained as a relatively distant forecast; no core/colour weight or destination was specified.'}]
    decision = next(x for x in candidate['decisions'] if x['question'] == '2')
    decision.update({'decision': 'may_retain', 'weight': 'not_adjudicated',
                     'time_note': 'FY2028 estimate is relatively distant at the 2026 article date.',
                     'clarification': CLARIFICATION})
    week = next(x for x in candidate['weekly_overrides'] if x['case'] == 'week:a64-3')
    week.update({'decision': 'may_retain', 'weight': 'not_adjudicated', 'target_status': 'not_adjudicated'})
    candidate['scoring_reason'] = 'The EPS forecast may be retained; its weight and target, other cases and scorer remain unvalidated.'
    assert candidate['base'] == old['base'] and candidate['user_answers_verbatim'] == old['user_answers_verbatim']
    assert candidate['ready_for_scoring'] is False and 'articles' not in candidate
    assert [(d['question'], d) for d in candidate['decisions'] if d['question'] != '2'] == [(d['question'], d) for d in old['decisions'] if d['question'] != '2']

    old_recount = json.loads((HERE / 'user-judge-recheck-2026-10-29-v2.json').read_text())
    history = copy.deepcopy(old_recount)
    eps = next(c for c in history['cases'] if c['user_question'] == '2')
    eps['expected_weight'] = 'not_adjudicated_may_retain'
    eps['note'] = CLARIFICATION
    for cell in eps['samples']:
        cell['correct_relevance_and_weight'] = None
    history['correct_per_sample'] = [sum(c['samples'][i]['correct_relevance_and_weight'] is True for c in history['cases']) for i in range(6)]
    history['denominator_per_sample'] = 7
    history['scope'] = 'Retrospective: seven scored user decisions; Singapore and EPS excluded from scoring for distinct uncertainties.'
    assert history['correct_per_sample'] == [2, 2, 2, 2, 2, 3]
    assert all(sum(c['samples'][i]['correct_relevance_and_weight'] is not None for c in history['cases']) == 7 for i in range(6))

    prior_trial = json.loads((HERE / 'direct-judge-trial-2026-10-29' / 'analyst-read.json').read_text())
    trial = copy.deepcopy(prior_trial)
    for row in trial['rows']:
        if row['id'] == 'b':
            row['expected_label'] = 'not_adjudicated_may_retain'
            row['label_correct'] = None
    trial['scope'] = 'Retrospective: EPS unscored after user clarification; eight labelled development cases, citation assessed on all nine.'
    trial['trial_label_correct'] = [sum(r['label_correct'] is True for r in trial['rows'] if r['sample'] == i) for i in range(1, 4)]
    trial['trial_label_denominator'] = 8
    assert trial['trial_label_correct'] == [5, 7, 7]
    assert trial['trial_quote_complete'] == prior_trial['trial_quote_complete'] == [6, 8, 6]
    assert all(sum(r['label_correct'] is not None for r in trial['rows'] if r['sample'] == i) == 8 for i in range(1, 4))
    assert all(r['actual_label'] == 'colour' for r in trial['rows'] if r['id'] == 'b')

    old_week = json.loads((HERE / 'week-fact-review-2026-10-29-v2.json').read_text())
    reference = json.loads((HERE / 'source-reference.json').read_text())
    article = next(a for a in reference['articles'] if a['article_no'] == 64)
    claim = next(c for c in article['claims'] if c['id'] == 'a64-3')
    ledger = json.loads((HERE / 'ledger.json').read_text())['v38'][63]
    record = next(r for r in ledger['records'] if r['id'] == 'e3')
    assert claim['source_text'] in ledger['source'] and record['quote'] in ledger['source'] and record['final_status'] == 'dropped'
    weekly = copy.deepcopy(old_week)
    row = {'id': 'a64-3', 'article_no': 64, 'input_id': article['input_id'], 'publication_day': ledger['day'],
           'source_text': claim['source_text'], 'additional_source_text': [], 'meaning': claim['meaning'],
           'previous_model_core': claim['core'], 'reviewed_meaning': claim['meaning'], 'extraction_content': 'complete',
           'analyst_note': 'User: may retain as a relatively distant forecast; exact weight and target not adjudicated.',
           'records': [{k: record[k] for k in ('id', 'quote', 'one_line', 'speaker', 'original_who', 'original_day', 'tier',
                                                'event_time', 'status', 'drop_reason', 'final_status', 'stored_id', 'stored_links')}],
           'complete_content_written': False, 'destination_correct': 'not assessed', 'old_coverage_complete': True}
    pos = next(i for i, x in enumerate(weekly['rows']) if x['id'] == 'a64-2') + 1
    weekly['rows'].insert(pos, row)
    weekly['scope'] = '33 provisional claims including an eligible longer-dated forecast, not an accepted benchmark.'
    weekly['exclusion'] = None
    weekly['counts'] = {'complete': 26, 'partial': 5, 'absent': 2}
    assert len(weekly['rows']) == 33 and sum(r['complete_content_written'] for r in weekly['rows']) == 12
    assert {k: sum(r['extraction_content'] == k for r in weekly['rows']) for k in weekly['counts']} == weekly['counts']
    assert not OUT.exists()
    OUT.mkdir()
    for name, value in [('reference.json', candidate), ('old-judge-recount.json', history),
                        ('direct-judge-recount.json', trial), ('week-fact-review.json', weekly)]:
        put(OUT / name, value)
    put(OUT / 'checks.json', {'old_reference_sha256': sha(OLD), 'preserved_old_answers': True,
                               'eps_scored': False, 'old_judge_counts': history['correct_per_sample'],
                               'direct_judge_counts': trial['trial_label_correct'], 'reference_scoreable': False})
    with (OUT / 'READY').open('x') as f:
        f.write('correction recorded; reference is not ready for scoring\n')
    print('EPS eligible, weight unresolved; historical controls 2/7, direct trial 5/8, 7/8, 7/8; old data preserved')


if __name__ == '__main__':
    main()
