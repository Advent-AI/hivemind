"""The model's own account of the favourable end it chose (AGENTS §1), for stored sends of theses whose sends gave both ends.

Each stored conversation is continued with the answer the model gave and one question. The question says that another send of
the same request gave the other end, so it can lead the reply: an account locates a reason, it does not show a fix. Asked once.

  python3 clean-arch/step4-2026-11-10/stage_a/direction_account.py
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402

DATA = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10'
OUTPUT = HERE / 'result-2' / 'direction-accounts.json'
CAP_USD = 0.05
REPLY_TOKEN_CAP = 3000
SENDS = [('run-2', 'acc/clean-1', 1), ('run-2', 'acc/clean-1', 2), ('run-2', 'acc/clean-7', 1), ('run-2', 'acc/clean-7', 2),
         ('run-2', 'u3/clean-8', 1), ('probe-reference', 'u3/clean-8', 1)]
QUESTION = ('One question about your answer. You set favourable_end to "{end}" with the reason: "{why}" Another answer to this '
            'same request set the other end, reasoning that {other}. (1) Which words of the request, the topic or the item led '
            'you to your end? Quote them. (2) Did you consider the other end, and what made you reject it? (3) Did the topic or '
            'the item take a side on which end is good for the company? Quote the words if so. (4) What would the request have '
            'had to say for you to give the same end every time? Answer in at most 170 words.')
OTHER = {'higher': 'a lower amount reduces the company\'s fixed obligations and its exposure if demand weakens',
         'lower': 'a higher amount secures the supply or the partners the company needs and supports demand for its products'}


def main():
    if OUTPUT.exists():
        raise SystemExit(f'{OUTPUT} exists: the accounts are asked once')
    follow_ups = []
    for run, case, pass_number in SENDS:
        folder = DATA / run / f'send-{pass_number}'
        row = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == case][0]
        accepted = [request for request in row['requests'] if request['result'] == 'ladder'][-1]
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        figure = row['answer']['ladder']['figure']
        question = QUESTION.format(end=figure['favourable_end'], why=figure['favourable_why'], other=OTHER[figure['favourable_end']])
        follow_up = {'model': stored['model'], 'reasoning_effort': stored['reasoning_effort'], 'max_completion_tokens': REPLY_TOKEN_CAP,
                     'messages': stored['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']}, {'role': 'user', 'content': question}]}
        follow_ups.append((run, case, pass_number, figure['favourable_end'], question, follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        run, case, pass_number, end, question, follow_up = job
        response = limit.send('openai', follow_up)
        usage = response.get('usage') or {}
        return {'run': run, 'case': case, 'pass': pass_number, 'end': end, 'question': question, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    OUTPUT.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(f"{reply['run']} {reply['case']} send {reply['pass']} | chose {reply['end']} | tokens in {reply['input_tokens']} out {reply['output_tokens']}")
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
