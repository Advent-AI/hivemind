"""Round 79's account of A2's listing choices: two of A2's stored sends whose lists hold entries the readers settled as not parts
(fortnight clean-6 pass 1: a delay and a termination; clean-13 pass 2: two settlement sources) are continued as their stored
conversations, rebuilt by the production builder and checked against the sent sha256, with one neutral question. An account is a lead.
Asked once; $0.02 ceiling.

  python3 listing_account.py <A2 probe data folder>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe  # noqa: E402
from probe import model, stage_a, universe  # noqa: E402

CAP_USD = 0.02
SENDS = [('fortnight', 'c1/clean-6', 1), ('fortnight', 'c1/clean-13', 2)]
QUESTION = ('One question about your answer. For each entry of your not_judged list, say in one line which instruction in the request '
            'led you to list it, and whether one of your answer choices already decides it. Answer in at most 150 words.')


def main(folder):
    probe.configure('a2')
    folder = Path(folder)
    output_path = HERE / 'listing-accounts.json'
    if output_path.exists():
        raise SystemExit(f'{output_path.name} exists: the accounts are asked once')
    research_list = universe.load(str(probe.ROOT / 'poc' / 'universe.json'))
    topics = {(source, name): case for _, source, name, case in probe.load_topics()}
    limit = stage_a.budget.Budget(CAP_USD)
    replies = []
    for source, name, pass_number in SENDS:
        label = f'changed|{source}:{name}'
        outcome = next(row for row in map(json.loads, (folder / 'changed' / f'send-{pass_number}' / 'outcomes.jsonl').read_text().splitlines())
                       if row['case'] == label)
        request = probe.built(topics[(source, name)], probe.arm_texts(), research_list)
        if model.request_identity(request)[1] != outcome['requests'][-1]['request_sha256']:
            raise SystemExit(f'{label} pass {pass_number}: the rebuilt request is not the one sent')
        follow_up = {key: value for key, value in request.items() if key not in ('response_format', 'max_completion_tokens')}
        follow_up['max_completion_tokens'] = 3000
        follow_up['messages'] = request['messages'] + [{'role': 'assistant', 'content': outcome['requests'][-1]['answer_text']},
                                                       {'role': 'user', 'content': QUESTION}]
        response = limit.send('openai', follow_up)
        replies.append({'case': label, 'pass': pass_number, 'listed': [p['part'] for p in outcome['answer']['ladder']['not_judged']],
                        'reply': response['choices'][0]['message']['content']})
    output_path.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 80, '\n', reply['case'], 'pass', reply['pass'], '\n listed:', reply['listed'], '\n', reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
