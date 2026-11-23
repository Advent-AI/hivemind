"""The model's own account (AGENTS §1), for the price probe: the `price` arm's request on two memory articles is sent once more, and the
conversation continued with one neutral question about why it proposed no memory-price question. Sends through the probe's ledger.

  python3 model_account.py <output.json>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import resend_shared as rs  # noqa: E402
from hivemind import model  # noqa: E402

CASES = ['p2-target-f66e1689', 'p1-target-d0f3f832']
QUESTION = ('The item reports memory (DRAM/HBM) contract prices rising sharply. Your answer proposed no candidate question about a memory '
            'price. In plain terms, quote the instructions of this request that decided whether to propose one, say which reason (opens_as) '
            'such a question would have needed, and what made you not propose it. At most 150 words.')


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise SystemExit(f'{out} exists')
    selection = [c for c in json.load(open(HERE / 'selection.json')) if c['case'] in CASES]
    cfg, bodies, _prepared = rs.build_all(selection)
    price_in, price_out = model.PRICES[next(iter(bodies.values()))['model']]
    ledger = rs.OutputCapLedger(0.1, price_in, price_out)
    replies = []
    for case in CASES:
        body = bodies[(case, 'price')]
        reserved = ledger.reserve(body)
        first = model.openai_transport(cfg.provider, body, timeout=300, max_attempts=1)
        ledger.settle(reserved, first.get('usage'))
        answer = first['choices'][0]['message']['content']
        follow = dict(body, messages=body['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': QUESTION}])
        follow.pop('response_format', None)
        reserved = ledger.reserve(follow)
        second = model.openai_transport(cfg.provider, follow, timeout=300, max_attempts=1)
        ledger.settle(reserved, second.get('usage'))
        candidates = json.loads(answer).get('candidates') or []
        replies.append({'case': case, 'candidates_in_resent_answer': [c.get('question') for c in candidates],
                        'account': second['choices'][0]['message']['content']})
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    print(f'ledger ${ledger.spent:.4f}')


if __name__ == '__main__':
    main()
