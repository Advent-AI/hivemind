"""The model's own account of three declines the fourth Stage A's readers call unjustified (AGENTS §1): "two figures, none the
main one" on theses that every earlier run answered with a ladder. Each stored conversation is continued with the answer the
model gave and one question. An account locates a reason; it does not show a fix. Asked once.

  python3 clean-arch/step4-2026-11-10/stage_a/decline_account.py
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

RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-4'
OUTPUT = HERE / 'result-4' / 'decline-accounts.json'
CAP_USD = 0.05
SENDS = [('u3/clean-11', 1), ('u3/clean-11', 3), ('acc/clean-9', 2)]
QUESTION = ('One question about your answer. You returned no_ladder because the topic names two figures and neither is the main '
            'one. (1) Quote the words of the topic\'s outcome that name each of the two figures. (2) The request says to judge "the '
            'one the topic\'s outcome names as what is tracked" and to list every other part in not_judged. Does the outcome\'s '
            'wording put one of the two first, or the other in brackets or as "the portion of it"? (3) Which words of the request '
            'led you to decline rather than to judge one and list the other? Answer in at most 150 words.')


def main():
    if OUTPUT.exists():
        raise SystemExit(f'{OUTPUT} exists: the accounts are asked once')
    follow_ups = []
    for case, pass_number in SENDS:
        folder = RUN / f'send-{pass_number}'
        row = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == case][0]
        accepted = row['requests'][-1]
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        follow_up = {'model': stored['model'], 'reasoning_effort': stored['reasoning_effort'], 'max_completion_tokens': 3000,
                     'messages': stored['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']}, {'role': 'user', 'content': QUESTION}]}
        follow_ups.append((case, pass_number, row['reason'], follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        case, pass_number, reason, follow_up = job
        response = limit.send('openai', follow_up)
        return {'case': case, 'pass': pass_number, 'reason_given': reason, 'reply': response['choices'][0]['message']['content']}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    OUTPUT.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(f"{reply['case']} send {reply['pass']} | declined: {reply['reason_given'][:160]}")
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
