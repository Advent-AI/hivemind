"""D578's two accounts: each refusal of the changed request is continued as its stored conversation (the request rebuilt by the
production builder and checked against the stored request's sha256, the model's own answer text as the assistant turn) with one
neutral question. An account is a lead that can rationalize the answer, not proof of a cause. Asked once; $0.02 ceiling.

  python3 refusal_account.py <probe data folder>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe  # noqa: E402
from probe import model, stage_a, universe  # noqa: E402

CAP_USD = 0.02
REPLY_TOKEN_CAP = 3000
REFUSALS = [('fortnight', 'c1/clean-13', 1), ('july', 'c3/clean-7', 3)]
QUESTION = ('One question about your answer. You returned no_ladder. Which instruction in the request, and which words of the topic '
            'or the item, led you to decline? Quote them. If you cannot identify them, say so. Answer in at most 120 words.')


def main(folder):
    folder = Path(folder)
    output_path = HERE / 'refusal-accounts.json'
    if output_path.exists():
        raise SystemExit(f'{output_path.name} exists: the accounts are asked once')
    research_list = universe.load(str(probe.ROOT / 'poc' / 'universe.json'))
    topics = {(source, name): case for _, source, name, case in probe.load_topics()}
    jobs = []
    for source, name, pass_number in REFUSALS:
        label = f'changed|{source}:{name}'
        outcome = next(row for row in map(json.loads, (folder / 'changed' / f'send-{pass_number}' / 'outcomes.jsonl').read_text().splitlines())
                       if row['case'] == label)
        if outcome['status'] != 'no ladder' or len(outcome['requests']) != 1:
            raise SystemExit(f'{label} pass {pass_number}: not a single-request refusal')
        request = probe.built(topics[(source, name)], probe.arm_texts(), research_list)
        if model.request_identity(request)[1] != outcome['requests'][0]['request_sha256']:
            raise SystemExit(f'{label} pass {pass_number}: the rebuilt request is not the one sent')
        follow_up = {key: value for key, value in request.items() if key not in ('response_format', 'max_completion_tokens')}
        follow_up['max_completion_tokens'] = REPLY_TOKEN_CAP
        follow_up['messages'] = request['messages'] + [{'role': 'assistant', 'content': outcome['requests'][0]['answer_text']},
                                                       {'role': 'user', 'content': QUESTION}]
        jobs.append((label, pass_number, follow_up))
    limit = stage_a.budget.Budget(CAP_USD)
    replies = []
    for label, pass_number, follow_up in jobs:
        response = limit.send('openai', follow_up)
        usage = response.get('usage') or {}
        replies.append({'case': label, 'pass': pass_number, 'question': QUESTION, 'reply': response['choices'][0]['message']['content'],
                        'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')})
    output_path.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 80)
        print(reply['case'], 'pass', reply['pass'], '| tokens in', reply['input_tokens'], 'out', reply['output_tokens'])
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
