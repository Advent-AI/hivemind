"""D470's census, step 2: the model's own account, asked neutrally, of eight theses Step 1 opened in a shape the ladder step had to decline
(seven counted breaches and the disputed c3/clean-3). Each stored Step 1 conversation is continued exactly (the stored request's messages,
the stored answer, then one user turn restating the response schema and asking the question); the question names the thesis as written and
asks what it tracks, which instructions were applied and what other wording was considered, without saying what is wrong with it. Sends go
through the identity probe's tested ledger (`../identity-probe/probe_identity.py`: a reservation per send, usage that is missing or prices
at zero settles at the reservation, an overrun stops later sends) under one ceiling. A reply is a lead, read against the answer and request.

  python3 shape_accounts.py <output.json> [c1/clean-11,...]
"""
import concurrent.futures
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(HERE.parent / 'identity-probe')]
from hivemind import model  # noqa: E402
import probe_identity  # noqa: E402

DATA = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
TRACES = {'c1': DATA / 'c1/step1/trace.sqlite', 'c2': DATA / 'c2/step1-redo/trace.sqlite', 'c3': DATA / 'c3/step1/trace.sqlite'}
CASES = [('c1', 'clean-10'), ('c1', 'clean-11'), ('c1', 'clean-13'), ('c1', 'clean-15'), ('c1', 'clean-2'), ('c2', 'clean-6'),
         ('c3', 'clean-9'), ('c3', 'clean-3')]
CEILING_USD = 0.40
MAX_TOKENS = 12000        # a short reply after reasoning; the ledger reserves the whole cap, so the stored 64,000 would block parallel sends
QUESTION = ('Your answer proposed a new thesis: "{description}" Its tracked outcome: "{outcome}" Its period: "{period}" In plain terms, what '
            'does this thesis track — which figure or event, over which period — and what will settle it? Quote the instructions of this '
            'request you applied in writing its outcome and its period, and name any other wording you considered for the outcome or the '
            'period and why you did not use it. Answer in at most 170 words.')


def opening(draw, thesis_id):
    """The sequence, stored request, stored answer and the thesis as opened, for the step whose after-state first holds thesis_id."""
    conn = sqlite3.connect(f'file:{TRACES[draw]}?mode=ro', uri=True)
    for sequence, request, raw, before, after in conn.execute(
            "select sequence, request, raw_response, before_state, after_state from trace where status='complete' order by sequence"):
        if thesis_id in {t['id'] for t in json.loads(after)} and thesis_id not in {t['id'] for t in json.loads(before)}:
            thesis = next(t for t in json.loads(after) if t['id'] == thesis_id)
            conn.close()
            return sequence, json.loads(request), json.loads(raw)['choices'][0]['message']['content'], thesis
    raise SystemExit(f'{draw} {thesis_id}: no step opened it')


def follow_up(draw, thesis_id):
    sequence, request, answer, thesis = opening(draw, thesis_id)
    schema = request.get('response_format')
    turn = ('For reference, this is the response schema you answered with, field descriptions included:\n' + json.dumps(schema, ensure_ascii=False)
            + '\n\n' + QUESTION.format(**{k: thesis[k] for k in ('description', 'outcome', 'period')}))
    follow = dict(request, messages=request['messages'] + [{'role': 'assistant', 'content': answer}, {'role': 'user', 'content': turn}])
    follow.pop('response_format', None)
    follow['max_tokens'] = MAX_TOKENS
    return sequence, thesis, follow


def main():
    out = Path(sys.argv[1])
    if out.exists():
        raise SystemExit(f'{out} exists')
    only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    built = [(draw, thesis_id, *follow_up(draw, thesis_id)) for draw, thesis_id in CASES if only is None or f'{draw}/{thesis_id}' in only]
    price_in, price_out = model.PRICES[built[0][4]['model']]
    ledger = probe_identity.Ledger(CEILING_USD, price_in, price_out)

    def ask(item):
        draw, thesis_id, sequence, thesis, request = item
        reserved = ledger.reserve(request)
        if reserved is None:
            return {'draw': draw, 'thesis': thesis_id, 'outcome': f'not sent: the ${CEILING_USD} ceiling would be passed'}
        try:
            response = model.openai_transport('deepseek', request)
        except Exception as error:
            ledger.settle(reserved, None)
            return {'draw': draw, 'thesis': thesis_id, 'outcome': f'error: {type(error).__name__}: {error}'}
        cost = ledger.settle(reserved, response.get('usage'))
        return {'draw': draw, 'thesis': thesis_id, 'sequence': sequence, 'description': thesis['description'], 'outcome': thesis['outcome'],
                'period': thesis['period'], 'reply': response['choices'][0]['message']['content'], 'cost_usd': round(cost, 6)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask, built))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1) + '\n')
    print(f'{sum("reply" in r for r in replies)} replies of {len(replies)}; ledger spent ${ledger.spent:.4f} of ${CEILING_USD}')


if __name__ == '__main__':
    main()
