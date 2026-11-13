"""The model's own account of one second-round answer (AGENTS §1): why it wrote a judged question for a topic the first request
had it decline four times of four."""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
sys.path[:0] = [str(REPOSITORY / 'src'), str(REPOSITORY / 'clean-arch' / 'e2e-2026-11-09')]
import budget  # noqa: E402

QUESTION = ('One question about your answer. The topic\'s outcome names two things: whether meaningful new HBM capacity comes online, '
            'and whether record-high prices persist. The request says to return no_ladder when "the topic has no main figure or event, '
            'naming none, or naming several with none of them the main one", and never to combine two things. You wrote a judged '
            'question. Which sentences of the request led you to write one here rather than return no_ladder? Quote each, and say '
            'which weighed most. Then say what, in the request, would have made you decline. Answer in at most 180 words.')


def main():
    output_path = HERE / 'account-round2-clean-10.json'
    if output_path.exists():
        raise SystemExit(f'{output_path} exists')
    connection = sqlite3.connect(f"file:{HERE / 'archive-round2.sqlite'}?mode=ro", uri=True)
    for request_json, answer_json in connection.execute('select request_json, answer_json from model_calls order by rowid'):
        request = json.loads(request_json)
        if json.loads(request['messages'][1]['content'].rsplit('\n\n', 1)[0])['thesis']['id'] == 'clean-10':
            break
    answer_text = next(json.loads(line)['answer_text'] for line in (HERE / 'answers-round2.jsonl').read_text().splitlines()
                       if json.loads(line)['case'] == 'u2/clean-10')
    follow_up = {'model': request['model'], 'reasoning_effort': request['reasoning_effort'], 'max_completion_tokens': 3000,
                 'messages': request['messages'] + [{'role': 'assistant', 'content': answer_text}, {'role': 'user', 'content': QUESTION}]}
    limit = budget.Budget(0.05)
    response = limit.send('openai', follow_up)
    reply = response['choices'][0]['message']['content']
    output_path.write_text(json.dumps({'question': QUESTION, 'reply': reply, 'usage': response.get('usage')}, ensure_ascii=False, indent=1) + '\n')
    print(reply)
    print(f'spent ${limit.spent_usd:.4f}')


if __name__ == '__main__':
    main()
