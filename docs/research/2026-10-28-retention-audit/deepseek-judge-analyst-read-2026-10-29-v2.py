"""Record the manual reading of completed replies from the model comparison."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE / 'deepseek-judge-trial-2026-10-29'

QUOTE_ISSUES = {
    ('gpt', 2, 'a'): 'Quote omits the revenue metric.',
    ('gpt', 2, 'e'): 'Separated source passages are joined into a fabricated verbatim quote.',
    ('gpt', 2, 'f'): 'Quote does not cover Huang sharing the letter.',
    ('gpt', 2, 'i'): 'Quote changes whitespace before punctuation; it is not an exact source substring.',
    ('gpt', 3, 'e'): 'Separated source passages are joined into a fabricated verbatim quote.',
    ('gpt', 3, 'i'): 'Quote changes whitespace before punctuation; it is not an exact source substring.',
    ('deepseek', 3, 'a'): 'Quote omits the revenue metric.',
    ('deepseek', 3, 'b'): 'Quote omits the $319 valuation and 25x multiple added to the meaning.',
    ('deepseek', 3, 'c'): 'Quote omits SK hynix and does not support the HBM inference.',
    ('deepseek', 3, 'e'): 'Quote omits the mansion, charges and destination added to the meaning.',
    ('deepseek', 3, 'f'): 'Quote omits the named companies and the count.',
    ('deepseek', 3, 'g'): 'Quote omits the official and the claimed sanction power.',
    ('deepseek', 3, 'h'): 'Quote omits the adviser and the additional distinction about distillation.',
    ('deepseek', 3, 'i'): 'Quote omits the management attribution.',
}
MEANING_ISSUES = {
    ('deepseek', 3, 'c'): 'HBM is not mentioned in the article; the extension is not explicitly supported by the source.',
    ('deepseek', 3, 'e'): 'The source says the servers were shipped to Malaysia; the answer says they were planned to be shipped.',
    ('deepseek', 3, 'h'): 'The adviser objected to covert industrial distillation aimed at stealing proprietary US technology; the answer drops that qualifying condition.',
}


def main():
    gold = json.loads((RUN / 'gold.json').read_text())
    request = json.loads((RUN / 'gpt-request.json').read_text())
    user = json.loads(request['input'][1]['content'])
    sources = {a['input_id']: a['source'] for a in user['articles']}
    cases = {x['id']: x['input_id'] for x in user['candidates']}
    all_rows, samples = [], []
    for provider in ('gpt', 'deepseek'):
        for sample in (1, 2, 3):
            raw = json.loads((RUN / f'{provider}-{sample}.json').read_text())
            if not raw['structurally_valid']:
                samples.append({'provider': provider, 'sample': sample, 'status': 'incomplete_or_invalid',
                                'reason': raw.get('response', {}).get('incomplete_details') or raw.get('error')})
                continue
            rows = []
            for item in raw['answer']['items']:
                ident = item['id']
                key = (provider, sample, ident)
                literal = item['quote'] in sources[cases[ident]]
                quote_issue = QUOTE_ISSUES.get(key, '')
                assert literal or quote_issue
                if ident == 'b':
                    label_result = 'unscored_user_weight_unspecified'
                elif key == ('deepseek', 3, 'e'):
                    label_result = 'unresolved_changed_the_candidate_fact'
                else:
                    label_result = 'correct' if item['label'] == gold[ident] else 'incorrect'
                rows.append({'provider': provider, 'sample': sample, 'id': ident,
                             'expected_label': gold[ident], 'label_result': label_result,
                             'meaning_review': 'not_fully_source_supported' if key in MEANING_ISSUES else 'source_supported',
                             'meaning_issue': MEANING_ISSUES.get(key, ''), 'quote_verbatim': literal,
                             'quote_supports_complete_meaning': not bool(quote_issue), 'quote_issue': quote_issue,
                             'answer': item})
            assert len(rows) == 9 and len({r['id'] for r in rows}) == 9
            assert sum(r['label_result'] in ('correct', 'incorrect', 'unresolved_changed_the_candidate_fact') for r in rows) == 8
            samples.append({'provider': provider, 'sample': sample, 'status': 'manually_reviewed',
                            'correct': sum(r['label_result'] == 'correct' for r in rows),
                            'incorrect': sum(r['label_result'] == 'incorrect' for r in rows),
                            'unresolved': sum(r['label_result'].startswith('unresolved') for r in rows),
                            'denominator': 8, 'complete_supporting_quotes': sum(r['quote_supports_complete_meaning'] for r in rows),
                            'quote_denominator': 9})
            all_rows.extend(rows)
    assert len(samples) == 6 and len(all_rows) == 27
    assert {(s['provider'], s['sample'], s.get('correct')) for s in samples if s['status'] == 'manually_reviewed'} == {('gpt', 2, 6), ('gpt', 3, 4), ('deepseek', 3, 5)}
    output = {'scope': 'Manual Codex review; eight user-scored development cases, EPS unscored, nine citation cases; not unseen or whole-pipeline acceptance.',
              'samples': samples, 'rows': all_rows}
    with (RUN / 'analyst-read-v2.json').open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps(samples, ensure_ascii=False))


if __name__ == '__main__':
    main()
