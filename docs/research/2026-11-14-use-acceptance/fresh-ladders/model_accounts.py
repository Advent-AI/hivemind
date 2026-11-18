"""The model's own account of listing, or not listing, a clause of the topic's outcome in not_judged (AGENTS §1; D546; ceiling $0.05).

Four stored conversations of the step that writes answer choices (the fresh week) are continued with the answer the model gave
as the assistant turn and one question. Two questions, each with an attempt that listed the clause and one that did not. The
question names the clause, so it can lead the reply: an account locates a reason, it does not show a fix. Asked once.

  python3 model_accounts.py
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402

LADDER = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1/ladder'
CAP_USD = 0.05
REPLY_TOKEN_CAP = 3000
CASES = [('c1/clean-5', 1, 'compared with the nearly $800 billion the article says they will spend this year', False),
         ('c1/clean-5', 3, 'compared with the nearly $800 billion the article says they will spend this year', True),
         ('c1/clean-3', 1, 'so that China data-center revenue can resume', False),
         ('c1/clean-3', 2, 'so that China data-center revenue can resume', True)]
QUESTION = ('One question about your answer. The topic\'s outcome field contains the words "{clause}". Your not_judged list {did} include '
            'them. Which sentence of the instructions decided whether those words belong in not_judged? Quote it. Then say what you took '
            '"the topic\'s wording" to mean in that sentence: which field or fields of the topic. Answer in at most 120 words.')


def main():
    output_path = HERE / 'accounts.json'
    if output_path.exists():
        raise SystemExit(f'{output_path} exists: the accounts are asked once')
    follow_ups = []
    for case, attempt, clause, listed in CASES:
        outcome = next(row for row in map(json.loads, (LADDER / f'send-{attempt}/outcomes.jsonl').read_text().splitlines()) if row['case'] == case)
        stored = outcome['requests'][0]
        archive = sqlite3.connect(f"file:{LADDER / f'send-{attempt}/archive.sqlite'}?mode=ro", uri=True)
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (stored['request_sha256'],)).fetchone()[0])
        answer = json.loads(stored['answer_text'])
        names = json.dumps(answer['ladder']['not_judged'], ensure_ascii=False)
        assert listed == any(word in names for word in ('800', 'revenue')), (case, attempt, names)          # the stored answer is the one the question describes
        follow_up = {'model': request['model'], 'reasoning_effort': request['reasoning_effort'], 'max_completion_tokens': REPLY_TOKEN_CAP,
                     'messages': request['messages'] + [{'role': 'assistant', 'content': stored['answer_text']},
                                                        {'role': 'user', 'content': QUESTION.format(clause=clause, did='does' if listed else 'does not')}]}
        follow_ups.append((case, attempt, listed, follow_up))
    limit = budget.Budget(CAP_USD)

    def ask(job):
        case, attempt, listed, follow_up = job
        response = limit.send('openai', follow_up)
        usage = response.get('usage') or {}
        return {'case': case, 'attempt': attempt, 'listed_the_clause': listed, 'question': follow_up['messages'][-1]['content'], 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(follow_ups)) as pool:
        replies = list(pool.map(ask, follow_ups))
    output_path.write_text(json.dumps({'replies': replies, 'spent_usd': round(limit.spent_usd, 5), 'cap_usd': CAP_USD}, ensure_ascii=False, indent=1) + '\n')
    for reply in replies:
        print('=' * 100)
        print(reply['case'], 'attempt', reply['attempt'], '| listed the clause:', reply['listed_the_clause'], '| tokens in', reply['input_tokens'], 'out', reply['output_tokens'])
        print(reply['reply'])
    print(f'spent ${limit.spent_usd:.4f} of ${CAP_USD:.2f} (from tokens at the published rates)')


if __name__ == '__main__':
    main()
