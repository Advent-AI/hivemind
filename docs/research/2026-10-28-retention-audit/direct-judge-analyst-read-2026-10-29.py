"""Record the analyst's manual reading of every completed trial answer."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE / 'direct-judge-trial-2026-10-29'

# Manual source-versus-meaning and quote-coverage review, not a string scorer.
QUOTE_FAILURES = {
    (1, 'a'): 'Quote does not identify the metric as revenue.',
    (1, 'e'): 'Two separated source passages are joined with an ellipsis, not a verbatim quote.',
    (1, 'i'): 'Meaning attributes the forecast to NVIDIA management; quote says only management.',
    (2, 'e'): 'Quote covers the four companies but not the claimed possible NVIDIA chips.',
    (3, 'e'): 'Two separated passages are joined out of source order, not a verbatim quote.',
    (3, 'f'): 'Meaning also says Huang shared the letter, which the quote does not cover.',
    (3, 'h'): 'Meaning adds the adviser’s distinction about legitimate distillation, which the quote does not cover.',
}


def load(name):
    return json.loads((RUN / name).read_text())


def main():
    gold = load('gold.json')
    request = load('trial-request.json')
    user = json.loads(request['input'][1]['content'])
    articles = {a['input_id']: a['source'] for a in user['articles']}
    candidates = {c['id']: c for c in user['candidates']}
    rows = []
    for sample in range(1, 4):
        result = load(f'trial-{sample}.json')
        assert result['structurally_valid'] and result['response']['status'] == 'completed'
        for item in result['answer']['items']:
            ident = item['id']
            source = articles[candidates[ident]['input_id']]
            literal = item['quote'] in source
            reason = QUOTE_FAILURES.get((sample, ident), '')
            assert literal or reason
            rows.append({'sample': sample, 'id': ident, 'expected_label': gold[ident], 'actual_label': item['label'],
                         'label_correct': item['label'] == gold[ident],
                         'meaning_supported_by_source': 'yes',
                         'quote_verbatim': literal, 'quote_supports_complete_meaning': 'no' if reason else 'yes',
                         'quote_review_reason': reason, 'answer': item})
    assert len(rows) == 27 and set(QUOTE_FAILURES) <= {(r['sample'], r['id']) for r in rows}
    controls = [load(f'control-{i}.json') for i in range(1, 4)]
    assert all(not c['structurally_valid'] and c['response']['status'] == 'incomplete'
               and c['response']['incomplete_details']['reason'] == 'max_output_tokens' for c in controls)
    output = {'scope': 'Manual Codex reading of 27 responses to nine selected user-adjudicated development cases; no unseen test.',
              'control': 'All three controls incomplete at the output limit; no control scores.',
              'trial_label_correct': [sum(r['label_correct'] for r in rows if r['sample'] == i) for i in range(1, 4)],
              'trial_quote_complete': [sum(r['quote_supports_complete_meaning'] == 'yes' for r in rows if r['sample'] == i) for i in range(1, 4)],
              'rows': rows}
    with (RUN / 'analyst-read.json').open('x') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({k: v for k, v in output.items() if k != 'rows'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
