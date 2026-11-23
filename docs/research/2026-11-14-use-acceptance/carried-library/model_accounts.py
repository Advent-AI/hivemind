"""The model's own account of six choices in the small comparison (AGENTS §1): continue the stored first-step conversation of
one read with the stored answer as the assistant turn and one question. The reply locates the instruction the model
followed; it does not show a fix. Cost: one short completion per case on DeepSeek Flash, priced from tokens at the published
rates (`hivemind.model.PRICES`).

  python3 model_accounts.py <the run's reads folder> <output.json>
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

TAIL = (' Quote the instruction or instructions of this request that led you there, and name the statements of the request you '
        'weighed against them. Then say what an experienced analyst covering the company would have done with this article. Answer '
        'in at most 170 words.')
CASES = [
    ('235-carried', 'Your answer filed the $25 billion of equity-investment commitments, the $99 billion equity-investment balance and '
                    'the net equity purchases under the open thesis clean-1, and opened no new thesis. Why did you not open a thesis on '
                    'NVIDIA\'s outstanding equity-investment commitments at its next annual report?'),
    ('119-carried', 'Your answer kept the Groq lawsuit, the reported DOJ probe and the FTC chair\'s statement, filed them under no thesis, '
                    'and opened a thesis only on Groq 3 LPX shipments. Why did you not open a thesis on whether U.S. regulators act '
                    'against NVIDIA\'s Groq transaction?'),
    ('012-empty', 'Your answer kept Micron\'s results and its outlook of only a moderate rise in memory selling prices, filed them under no '
                  'thesis, and opened no thesis. Why did you not open a thesis on memory (HBM/DRAM) contract prices?'),
    ('035-empty', 'Your answer kept the third-quarter guidance that assumes no China data-center revenue and the H20 licence charge, filed '
                  'them under no thesis, and opened no thesis. Why did you not open a thesis on whether NVIDIA can resume data-center '
                  'sales in China?'),
    ('173-carried', 'Your answer filed the statement that five clients each accounted for at least 10% of NVIDIA\'s accounts receivable '
                    'under the open thesis clean-1 (credit support and guarantees). Why that thesis?'),
    ('206-carried', 'Your answer filed the CFO\'s outlook of 70% sales growth in 2028, limited by supply, under the open thesis clean-2 '
                    '(purchase and supply commitments). Why that thesis?'),
]


def follow_up(reads, folder, question):
    conn = sqlite3.connect(f"file:{Path(reads) / folder / 'trace.sqlite'}?mode=ro", uri=True)
    request, raw = conn.execute("select request, raw_response from trace where status = 'complete'").fetchone()
    request, raw = json.loads(request), json.loads(raw)
    sent = raw.get('sent_request') or request                       # the bytes the provider received, when an adaptation changed them
    follow = dict(sent, messages=sent['messages'] + [{'role': 'assistant', 'content': raw['choices'][0]['message']['content']},
                                                     {'role': 'user', 'content': question + TAIL}])
    follow.pop('response_format', None)
    return follow


def main(reads, output):
    output = Path(output)
    if output.exists():
        raise SystemExit(f'{output} exists')
    price_in, price_out = model.PRICES['deepseek-flash']

    def ask(case):
        folder, question = case
        response = model.openai_transport('deepseek', follow_up(reads, folder, question))
        usage = response.get('usage') or {}
        return {'read': folder, 'question': question, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        replies = list(pool.map(ask, CASES))
    output.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    tokens_in = sum(r['input_tokens'] or 0 for r in replies)
    tokens_out = sum(r['output_tokens'] or 0 for r in replies)
    print(f'{len(replies)} replies; tokens {tokens_in} in, {tokens_out} out; about ${(tokens_in * price_in + tokens_out * price_out) / 1e6:.4f} at the published rates')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
