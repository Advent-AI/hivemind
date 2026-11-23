"""The model's own account of its choices in the six-request probe (AGENTS §1; D404): each stored conversation is continued with
the answer the model gave as the assistant turn and one question about a fault read in it. The question names the fault, so it can
lead the reply: an account locates a reason, it does not show a fix.

  python3 clean-arch/step4-2026-11-10/probe-2026-11-10/model_account.py
"""
import concurrent.futures
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402

CAP_USD = 0.10
REPLY_TOKEN_CAP = 3000
QUESTIONS = {
    'u1/clean-4': (
        'One question about your answer. Its reference.words reads: "Nvidia projects that this figure could reach $1 trillion next '
        'year." The item\'s sentence reads: "Next year, Nvidia projects that this figure could reach $1 trillion." The request asks '
        'for the reference "in the item\'s own words". Which words of the request did you read as allowing the sentence to be '
        'reordered, and what in the request would have made you copy the item\'s sentence exactly as it stands? Quote the '
        'instruction you relied on. Answer in at most 120 words.'),
    'u1/clean-7': (
        'Three questions about your answer. (1) Its reference.words reads "The $119 billion cited in this item". Those words are in '
        'the topic; the item\'s own sentence is "Nvidia\'s $119B in supply commitments hinge on AI delivering measurable economic '
        'value". Which instruction led you to take the words from the topic? (2) The request describes the reference as what the '
        'market expects: a consensus, the company\'s guidance, the stated plan or deadline. The item gives $119B as the present '
        'amount. Which instruction led you to record it as the reference? (3) Your question says "compared with the $119 billion '
        'cited in this item". Whom did you take the reader of that question to be, and will that reader have the item? Quote the '
        'instructions you relied on. Answer in at most 180 words.'),
    'u3/clean-12': (
        'Two questions about your answer. (1) Its object is a theme, chip-export-controls, and you labelled its five states Strongly '
        'bearish, Bearish, Neutral, Bullish and Strongly bullish. The request says that for a theme each state carries a short name '
        'of the state. Which instruction led you to use those five labels? (2) Your question begins "By January 31, 2027, will the '
        'US Commerce Department ... have issued ...?", which is answered by a yes or a no, and you answered it with five states. '
        'Which instruction led you to that wording of the question? Quote the instructions you relied on. Answer in at most 150 '
        'words.'),
}


def main():
    output_path = HERE / 'accounts.json'
    if output_path.exists():
        raise SystemExit(f'{output_path} exists: the accounts are asked once')
    requests = {entry['case']: entry['request'] for entry in json.loads((HERE / 'requests-sent.json').read_text())}
    answers = {}
    for line in (HERE / 'answers.jsonl').read_text().splitlines():
        row = json.loads(line)
        answers[row['case']] = row['answer_text']
    limit = budget.Budget(CAP_USD)
    follow_ups = []
    for case, question in QUESTIONS.items():
        stored_request = requests[case]
        follow_up = {'model': stored_request['model'], 'reasoning_effort': stored_request['reasoning_effort'],
                     'max_completion_tokens': REPLY_TOKEN_CAP,
                     'messages': stored_request['messages'] + [{'role': 'assistant', 'content': answers[case]},
                                                               {'role': 'user', 'content': question}]}
        follow_ups.append((case, question, follow_up))

    def ask(job):
        case, question, follow_up = job
        response = limit.send('openai', follow_up)
        usage = response.get('usage') or {}
        return {'case': case, 'question': question, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    output_path.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(reply['case'], '| tokens in', reply['input_tokens'], 'out', reply['output_tokens'])
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
