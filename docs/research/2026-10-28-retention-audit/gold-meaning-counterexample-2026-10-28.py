"""Reproduce the frozen gold's 82%/41% semantic scoring error on archived controls."""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
OLD = HERE.parent / '2026-10-28-extraction-quality'
ITEM_ID = 'gnews:71df54965281684cc500960f'

def case_correct(summaries):
    """Case-specific check only, not a general semantic scoring rule."""
    text = ' '.join(summaries).lower()
    return 'revenue' in text and '82%' in text and '41%' in text

def main():
    old_gold = json.loads((OLD / 'gold-extraction.json').read_text())
    article = next(a for a in old_gold['articles'] if a['input_id'] == ITEM_ID)
    fact = next(s for s in article['statements'] if s['id'] == 'a11-2')
    assert fact['weight'] == 'colour' and '82%' in fact['span'] and '41%' in fact['span']
    new = json.loads((HERE / 'source-reference.json').read_text())
    newer = next(a for a in new['articles'] if a['input_id'] == ITEM_ID)
    newfact = next(s for s in newer['claims'] if s['id'] == 'a64-2')
    assert newfact['core'] and 'revenue growth' in newfact['source_text'].lower()
    assert any(s['id'] == 'a64-3' for s in newer['claims']) and 'FY2028 EPS' in article['rejected_note']
    scores = json.loads((OLD / 'results/send-control.json').read_text())
    cases = []
    for sample in (1, 2, 3):
        conn = sqlite3.connect('file:' + str(OLD / f'results/archive-control-s{sample}.sqlite') + '?mode=ro', uri=True)
        hits = []
        for request, answer in conn.execute("select request_json,answer_json from model_calls where purpose='extract'"):
            user = json.loads(request)['messages'][1]['content']
            if '[Item] id ' + ITEM_ID + ',' in user:
                hits.append(json.loads(answer))
        assert len(hits) == 1
        evidence = [e for e in hits[0]['evidence'] if '82%' in e['one_line'] or '41%' in e['one_line']]
        summaries = [e['one_line'] for e in evidence]
        assert len(evidence) == 2 and not case_correct(summaries)
        assert case_correct(['Wall Street analysts forecast revenue growth of 82% in 2026 and 41% in 2027.'])
        row = next(r for r in scores if r['input_id'] == ITEM_ID and r['sample'] == sample)
        cell = row['cells']['a11-2']
        if sample in (2, 3):
            assert cell['cell'] == 'kept_right' and len(cell['pieces']) == 1
        cases.append({'sample': sample, 'old_score': cell, 'extracted_records': evidence,
                      'source_contains_metric': 'revenue growth', 'full_meaning_preserved': False})
    output = {'source_id': ITEM_ID, 'old_gold': 'a11-2: colour', 'new_reference_conflict': 'a64-2: core',
              'excluded_old_gold_but_added_new_reference': 'a64-3: FY2028 EPS',
              'old_control_cases': cases, 'case_specific_positive_control_passed': True,
              'scope': 'one known semantic counterexample; no general prevalence estimated'}
    with (HERE / 'gold-meaning-counterexample-2026-10-28.json').open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2); f.write('\n')
    print('3 archived controls: 82% and 41% extracted in separate records; revenue metric absent in all 3; old scorer called 2 kept_right')

if __name__ == '__main__':
    main()
