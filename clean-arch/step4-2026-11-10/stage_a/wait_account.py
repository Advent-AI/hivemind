"""The model's own account of a wait written as the ruling out (AGENTS §1): the three sends of the third Stage A that both
readers fail on R are continued with the answer the model gave and one question. An account locates a reason; it does not
show a fix. Asked once.

  python3 clean-arch/step4-2026-11-10/stage_a/wait_account.py
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

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-3'
OUTPUT = HERE / 'result-3' / 'wait-accounts.json'
CAP_USD = 0.05
SENDS = [('u1/clean-3', 1), ('u1/clean-6', 1), ('u3/clean-7', 1)]
QUESTION = ('One question about your answer. Its event.ruled_out is: "{ruled_out}" (1) Suppose the due day arrives, the event has '
            'not happened, and no one has decided against it, abandoned it or withdrawn it. Under your answer, which of the three '
            'outcomes holds: happened, ruled out, or neither? (2) Under the request, which should hold in that case? Quote the words '
            'of the request you rely on. (3) If the two differ, what led you to write ruled_out as you did? Answer in at most 170 words.')


def main():
    if OUTPUT.exists():
        raise SystemExit(f'{OUTPUT} exists: the accounts are asked once')
    follow_ups = []
    for case, pass_number in SENDS:
        folder = RUN / f'send-{pass_number}'
        row = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == case][0]
        accepted = [request for request in row['requests'] if request['result'] == 'ladder'][-1]
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        ruled_out = row['answer']['ladder']['event']['ruled_out']
        follow_up = {'model': stored['model'], 'reasoning_effort': stored['reasoning_effort'], 'max_completion_tokens': 3000,
                     'messages': stored['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']},
                                                       {'role': 'user', 'content': QUESTION.format(ruled_out=ruled_out)}]}
        follow_ups.append((case, pass_number, ruled_out, follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        case, pass_number, ruled_out, follow_up = job
        response = limit.send('openai', follow_up)
        return {'case': case, 'pass': pass_number, 'ruled_out': ruled_out, 'reply': response['choices'][0]['message']['content']}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    OUTPUT.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(f"{reply['case']} send {reply['pass']} | ruled_out: {reply['ruled_out']}")
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
