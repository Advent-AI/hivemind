"""The model's own account of the ruling out it wrote, or left out, for the French investigation (AGENTS §1): four stored
sends of u1/clean-12 from the small send are continued with the answer the model gave and one question. The question does
not say which answer is wanted. An account locates a reason; it does not show a fix. Asked once.

  python3 clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/event_account.py
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

DATA = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'probe-d413-d414'
OUTPUT = HERE / 'result' / 'event-accounts.json'
CAP_USD = 0.05
SENDS = [('with-tie-rule', 1), ('with-tie-rule', 2), ('with-tie-rule', 3), ('without-tie-rule', 2)]
QUESTION = ('One question about your answer. Its event.ruled_out is: {ruled_out}. (1) Before the due day, what could happen to this '
            'investigation other than the authority publishing a decision or conclusion? Name each thing. (2) For each, say whether you '
            'counted it as the event having happened, as the event ruled out, or as neither, and why. (3) Which words of the request led '
            'you to write ruled_out as you did? Quote them. Answer in at most 170 words.')


def main():
    if OUTPUT.exists():
        raise SystemExit(f'{OUTPUT} exists: the accounts are asked once')
    follow_ups = []
    for arm, pass_number in SENDS:
        folder = DATA / arm / f'send-{pass_number}'
        row = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == 'u1/clean-12'][0]
        accepted = [request for request in row['requests'] if request['result'] == 'ladder'][-1]
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        ruled_out = row['answer']['ladder']['event']['ruled_out']
        question = QUESTION.format(ruled_out='null' if ruled_out is None else f'"{ruled_out}"')
        follow_up = {'model': stored['model'], 'reasoning_effort': stored['reasoning_effort'], 'max_completion_tokens': 3000,
                     'messages': stored['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']}, {'role': 'user', 'content': question}]}
        follow_ups.append((arm, pass_number, ruled_out, question, follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        arm, pass_number, ruled_out, question, follow_up = job
        response = limit.send('openai', follow_up)
        return {'arm': arm, 'pass': pass_number, 'ruled_out': ruled_out, 'question': question, 'reply': response['choices'][0]['message']['content']}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    OUTPUT.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(f"{reply['arm']} send {reply['pass']} | ruled_out: {reply['ruled_out']}")
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
