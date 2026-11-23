"""The model's own account of two things the four-arm small send showed (AGENTS §1): in the object arm, the company's own sales
filed under the theme; in the typed arm, a decision to go on waiting written as the ruling out, and no ruling out at all.
Each stored conversation is continued with the answer the model gave and one question. An account locates a reason; it does
not show a fix. Asked once.

  python3 clean-arch/step4-2026-11-10/probe-d416-d418-2026-11-10/accounts.py
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

DATA = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'probe-d416-d418'
OUTPUT = HERE / 'result' / 'accounts.json'
CAP_USD = 0.05
OBJECT_QUESTION = ('One question about your answer. Its object is the theme chip-export-controls, and its question asks whether the '
                   'company\'s own sales take place. (1) Which words of the request led you to that object? Quote them. (2) The request '
                   'also says a question about the company\'s revenue or product progress is about the company "even when policy or '
                   'macroeconomics drives it". How did you weigh the two? (3) What does the topic\'s outcome name as the thing tracked: '
                   'the government\'s decision, or the company\'s sales? Answer in at most 150 words.')
CONTINUE_QUESTION = ('One question about your answer. Its ruled_out names the authority and the decision "{decision}" (1) Under the '
                     'request, is an investigation that is still going on the day the event ruled out, or the event still awaited? Quote '
                     'the words you rely on. (2) What led you to write this decision? (3) What else, if anything, could rule the event '
                     'out before the due day? Answer in at most 150 words.')
NULL_QUESTION = ('One question about your answer. Its event.ruled_out is null. (1) Before the due day, could the authority formally '
                 'abandon or withdraw the investigation without issuing the decision or conclusion your question asks about? (2) If it '
                 'did, which of your outcomes would hold on the due day, and why? (3) Which words of the request led you to null? '
                 'Answer in at most 150 words.')
SENDS = [('object', 'u3/clean-5', 1, OBJECT_QUESTION), ('object', 'u3/clean-5', 3, OBJECT_QUESTION),
         ('typed', 'u2/clean-9', 1, CONTINUE_QUESTION), ('typed', 'u2/clean-9', 2, NULL_QUESTION), ('typed', 'u3/clean-9', 1, NULL_QUESTION)]


def main():
    if OUTPUT.exists():
        raise SystemExit(f'{OUTPUT} exists: the accounts are asked once')
    follow_ups = []
    for arm, case, pass_number, question in SENDS:
        folder = DATA / arm / f'send-{pass_number}'
        row = [row for line in (folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)] if row['case'] == case][0]
        accepted = [request for request in row['requests'] if request['result'] == 'ladder'][-1]
        connection = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        stored = json.loads(connection.execute('select request_json from model_calls where request_sha256 = ?', (accepted['request_sha256'],)).fetchone()[0])
        connection.close()
        ruled_out = row['answer']['ladder']['event']['ruled_out']
        if question is CONTINUE_QUESTION:
            question = question.format(decision=ruled_out['decision'])
        follow_up = {'model': stored['model'], 'reasoning_effort': stored['reasoning_effort'], 'max_completion_tokens': 3000,
                     'messages': stored['messages'] + [{'role': 'assistant', 'content': accepted['answer_text']}, {'role': 'user', 'content': question}]}
        follow_ups.append((arm, case, pass_number, question, follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        arm, case, pass_number, question, follow_up = job
        response = limit.send('openai', follow_up)
        return {'arm': arm, 'case': case, 'pass': pass_number, 'question': question, 'reply': response['choices'][0]['message']['content']}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    OUTPUT.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(f"{reply['arm']} {reply['case']} send {reply['pass']}")
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
