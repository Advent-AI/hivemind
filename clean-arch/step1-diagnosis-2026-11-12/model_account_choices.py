"""The model's own account of a choice Step 1 made, or a thesis it did not open (AGENTS §1): continue a stored c8 conversation with
the stored answer as the assistant turn and one question, and record the free-text reply. Each question names what the answer did
and what it did not do, so it can lead the reply; the reply locates the instruction the model followed, it does not show a fix.

  python3 clean-arch/step1-diagnosis-2026-11-12/model_account_choices.py <output.json>

Cost: one short completion per case on DeepSeek Flash, priced from tokens at the published rates in hivemind.model.PRICES.
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

DRAWS = ROOT / 'poc/data/clean-unseeded-2026-11-10'
TAIL = (' Quote the instruction or instructions of this request that led you there, and name the statements of the request you weighed '
        'against them. Then say what an experienced analyst covering the company would have done with this article. Answer in at most '
        '170 words.')
YEAR = ('Your answer opened one thesis on the big four hyperscalers\' combined data-center capital expenditure for calendar {opened}, and '
        'used the article\'s figure for calendar {other} only as its base or benchmark. Why did you not open calendar {other}\'s combined '
        'spending as a thesis of its own?')
OHIO = ('Your answer linked the report that NVIDIA has been negotiating to guarantee OpenAI\'s lease of a large Ohio data center to the open '
        'thesis on the amount of credit support NVIDIA has extended. Why did you not open a thesis on whether NVIDIA signs that guarantee '
        'by a check date?')
MEMORY = ('Your answer opened a thesis on AI memory contract prices "through calendar 2026-2027". Why did you track the two years together '
          'rather than one calendar year\'s contract price, or next year\'s price against this year\'s?')
CASES = [('d1', 42, YEAR.format(opened=2027, other=2026)), ('d2', 42, YEAR.format(opened=2026, other=2027)),
         ('d3', 42, YEAR.format(opened=2027, other=2026)), ('d2', 8, OHIO), ('d3', 8, OHIO), ('d1', 56, MEMORY)]


def follow_up(draw, sequence, question):
    conn = sqlite3.connect(f"file:{DRAWS / f'draw-{draw}' / 'trace.sqlite'}?mode=ro", uri=True)
    request, raw = conn.execute("select request, raw_response from trace where sequence = ? and status = 'complete'", (sequence,)).fetchone()
    request, raw = json.loads(request), json.loads(raw)
    stored_answer = raw['choices'][0]['message']['content']            # the answer exactly as the model gave it
    follow = dict(request, messages=request['messages'] + [{'role': 'assistant', 'content': stored_answer},
                                                           {'role': 'user', 'content': question + TAIL}])
    follow.pop('response_format', None)
    return follow


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise SystemExit(f'{out} exists')

    def ask(case):
        draw, sequence, question = case
        response = model.openai_transport('deepseek', follow_up(draw, sequence, question))   # the provider the stored runs used (settings.json)
        usage = response.get('usage') or {}
        return {'draw': draw, 'sequence': sequence, 'question': question, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        replies = list(pool.map(ask, CASES))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    tokens_in = sum(reply['input_tokens'] or 0 for reply in replies)
    tokens_out = sum(reply['output_tokens'] or 0 for reply in replies)
    print(f'{len(replies)} replies; tokens {tokens_in} in, {tokens_out} out')


if __name__ == '__main__':
    main()
