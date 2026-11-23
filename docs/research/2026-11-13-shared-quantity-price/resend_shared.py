"""D191 point 4 / D368 item 1 on production's opening rule ("industry_aggregate" holds a price too): stored extraction requests of the full
run's production draws p1–p3 (poc-v118, unseeded), re-sent as production builds them, with one exact edit of the role's industry_aggregate
sentence in the arm `price`; the arm `stored` sends the request unchanged (a same-day control).

Faithful bytes (AGENTS §5): each request is rebuilt by `resend_filing.rebuild` (the code's own schema and setting, `model.build_request`),
which refuses an item whose rebuilt request does not carry the stored archive key. Every answer goes through what production runs on it
(`resend_filing.file_like_production`: `extraction.sift_with_groups`, the narrowest-question rule, the no-home drop). Spending goes through
the identity probe's tested ledger (reserve, settle at usage; missing or zero usage settles at the reservation; an overrun stops later sends).

  python3 resend_shared.py check <selection.json>                      (rebuilds every request, checks the edit; no send)
  python3 resend_shared.py send <selection.json> <answers.json> --sends 3 --max-usd 1
"""
import concurrent.futures
import json
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'docs/research/2026-11-04-filing-end-to-end'),
                str(ROOT / 'clean-arch/e2e-comparison-2026-11-13/identity-probe')]
from hivemind import config, extraction, model, universe  # noqa: E402
import resend_filing as rf  # noqa: E402
import probe_identity  # noqa: E402

FULL = ROOT / 'poc/data/clean-e2e-full-2026-11-13'
OLD = ('industry_aggregate: one aggregate quantity for one calendar year, such as the combined capital spending of named companies.')
NEW = ('industry_aggregate: one quantity or price outside any one company that several companies move on, for one calendar year, such as '
       'the combined capital spending of named companies or a raw material\'s contract price.')
ARMS = {'stored': [], 'price': [(OLD, NEW)]}


class OutputCapLedger(probe_identity.Ledger):
    """The identity probe's ledger, reading production's output cap (`max_completion_tokens`, the OpenAI request's name for it)."""

    def estimate(self, request):
        cap = request.get('max_tokens', request.get('max_completion_tokens'))
        if not isinstance(cap, int):
            raise SystemExit('a request without an output cap cannot be reserved')
        return ((2 * len(json.dumps(request).encode('utf-8')) + 4096) * self.price_in + cap * self.price_out) / 1e6


def stored_calls(draw):
    rf.DRAW = str(FULL / draw / 'prod')
    return rf.stored_calls()


def build_all(selection):
    cfg = config.load(str(ROOT / 'poc/config/poc-v118.json'))
    items_conn = rf.ro(rf.ITEMS)
    bodies, prepared = {}, {}
    for case in selection:
        draw, input_id = case['draw'], case['input_id']
        calls = stored_calls(draw)
        if input_id not in calls:
            raise SystemExit(f'{draw} {input_id}: no accepted extraction call in this draw')
        call_id, sha = calls[input_id]
        archive, views = rf.ro(f'{rf.DRAW}/archive.sqlite'), rf.ro(f'{rf.DRAW}/views.sqlite')
        item, setting, system, user, schema, shown, parents = rf.rebuild(cfg, items_conn, archive, views, input_id, call_id, sha)
        prepared[case['case']] = (item, shown, parents)
        for arm, edits in ARMS.items():
            sent_system = system
            for old_text, new_text in edits:
                if sent_system.count(old_text) != 1:
                    raise SystemExit(f"{case['case']} ({arm}): the sentence to replace occurs {sent_system.count(old_text)} times; nothing sent")
                sent_system = sent_system.replace(old_text, new_text)
            bodies[(case['case'], arm)] = model.build_request(setting, sent_system, user, schema, 'extraction', cfg.provider)
    return cfg, bodies, prepared


def main():
    command, selection = sys.argv[1], json.load(open(sys.argv[2]))
    cfg, bodies, prepared = build_all(selection)
    print(f'{len(prepared)} requests rebuilt byte-identical to the stored ones; {len(bodies)} arm requests built; the edit found once in each')
    if command == 'check':
        return
    out = Path(sys.argv[3])
    if out.exists():
        raise SystemExit(f'{out} exists')
    sends = int(sys.argv[sys.argv.index('--sends') + 1])
    ceiling = float(sys.argv[sys.argv.index('--max-usd') + 1])
    uni = universe.load(str(ROOT / 'poc/universe.json'))
    price_in, price_out = model.PRICES[next(iter(bodies.values()))['model']]
    ledger = OutputCapLedger(ceiling, price_in, price_out)

    def one(job):
        """Every attempt is its own reservation and settlement: the transport makes one attempt (max_attempts=1); a network failure or an
        unreadable answer is re-sent up to twice more, each again reserved; an answer that arrives but does not parse settles at its usage."""
        case, arm, number = job
        body = bodies[(case, arm)]
        attempts = []
        for attempt in range(3):
            reserved = ledger.reserve(body)
            if reserved is None:
                attempts.append(f'not sent: the ${ceiling} ceiling')
                return {'case': case, 'arm': arm, 'send': number, 'outcome': attempts[-1], 'attempts': attempts}
            try:
                reply = model.openai_transport(cfg.provider, body, timeout=300, max_attempts=1)
            except Exception as error:
                ledger.settle(reserved, None)
                attempts.append(f'transport: {type(error).__name__}: {str(error)[:100]}')
                continue
            cost = ledger.settle(reserved, reply.get('usage'))
            try:
                data = json.loads(reply['choices'][0]['message']['content'])
            except Exception as error:
                attempts.append(f'unreadable answer (${cost:.5f}): {type(error).__name__}')
                continue
            attempts.append(f'valid (${cost:.5f})')
            item, shown, parents = prepared[case]
            kept, homeless, dropped, _ = rf.file_like_production(data, item, shown, parents, uni)
            _evidence, candidates, _dropped, _ = extraction.sift_with_groups(data, item, item['text'] or '', set(shown), uni)
            return {'case': case, 'arm': arm, 'send': number, 'outcome': 'valid', 'attempts': attempts, 'answer_keys': list(data),
                    'raw_candidates': data.get('candidates') or [], 'kept_candidates': candidates, 'kept': len(kept),
                    'homeless': len(homeless), 'dropped': dropped}
        return {'case': case, 'arm': arm, 'send': number, 'outcome': 'failed after three attempts', 'attempts': attempts}
    jobs = [(case, arm, n) for case in prepared for arm in ARMS for n in range(1, sends + 1)]
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = list(pool.map(one, jobs))
    out.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in results) + '\n')
    print(f"{sum(r['outcome'] == 'valid' for r in results)} valid of {len(results)}; ledger ${ledger.spent:.4f} of ${ceiling}")


if __name__ == '__main__':
    main()
