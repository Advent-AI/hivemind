"""Send the complete-evidence test (oracle-design.md, D361): each arm of oracle-requests.json three times, built by `model.build_request` with the
frozen judging configuration and refused unless its archive key equals the one recorded when the request was built and read. Every answer is
checked by `judging.check_answer` against the text that was sent (a refused answer is kept and counts as not judged) and scored by the frozen
scorer's rule (`score_judgement.py`): a numeric question agrees when the gold's implied range overlaps the band [lo, hi) of the chosen rung, read
from the draw's rungs table; the gold is read from gold-v1.json and refused unless its sha256 is the frozen one.

usage: python3 oracle_send.py <oracle-requests.json> <out.json> [--sends 3]
"""
import concurrent.futures
import hashlib
import json
import sqlite3
import sys
import time

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src']
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

RUN = f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
GOLD = f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold'


def main():
    requests_path, out = sys.argv[1], sys.argv[2]
    sends = int(sys.argv[sys.argv.index('--sends') + 1]) if '--sends' in sys.argv else 3
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    gold_bytes = open(f'{GOLD}/gold-v1.json', 'rb').read()
    frozen = open(f'{GOLD}/gold-v1.sha256').read().split()[0]
    if hashlib.sha256(gold_bytes).hexdigest() != frozen:
        raise SystemExit('gold-v1.json is not the frozen gold: refused')
    implied = {e['seed_view_id']: e['implied_outcome'] for e in json.loads(gold_bytes)['entries'] if e.get('seed_view_id') and e.get('implied_outcome')}
    conn = sqlite3.connect(f'file:{RUN}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    pinned = open(requests_path + '.sha256').read().split()[0]          # the version that was built, read and reviewed
    if hashlib.sha256(open(requests_path, 'rb').read()).hexdigest() != pinned:
        raise SystemExit(f'{requests_path} is not the pinned, reviewed version: nothing sent')
    requests = json.load(open(requests_path))
    bodies = {}
    for arm, r in requests.items():
        body = model.build_request(cfg.rejudging, r['system'], r['user'], schema, 'judgement', cfg.provider)
        if model.request_identity(body)[1] != r['request_sha256']:
            raise SystemExit(f'{arm}: the request differs from the one built and read; nothing sent')
        bodies[arm] = body
    print(f'gold sha256 {frozen[:16]}… (frozen); {len(bodies)} arms, {sends} sends each, judging {cfg.rejudging.prompt_version} on {cfg.rejudging.model}')

    def send(job):
        """One reply. Only a transport failure is re-sent (the same bytes); a reply that is not a readable answer is kept and counts as not judged."""
        arm, n = job
        for attempt in range(4):
            try:
                reply = model.openai_transport(cfg.provider, bodies[arm], timeout=300)
                break
            except Exception as error:
                if attempt == 3:
                    return arm, n, None, {}, f'transport: {type(error).__name__}: {str(error)[:200]}'
                print(f'  {arm} send {n}: {type(error).__name__}: {str(error)[:120]}; re-sent in {30 * (attempt + 1)} s', flush=True)
                time.sleep(30 * (attempt + 1))
        content = reply['choices'][0]['message']['content']
        try:
            return arm, n, json.loads(content), reply.get('usage') or {}, None
        except ValueError:
            return arm, n, content, reply.get('usage') or {}, 'reply is not JSON'

    jobs = [(arm, n) for arm in bodies for n in range(sends)]
    results = {arm: [None] * sends for arm in bodies}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for arm, n, data, usage, failure in pool.map(send, jobs):
            r = requests[arm]
            if failure:
                errors = [failure]
            else:
                try:
                    errors = judging.check_answer(conn, r['view_id'], data, request_text=r['user'])
                except Exception as error:                         # an answer missing a field is refused, not a crash
                    errors = [f'check failed: {type(error).__name__}: {error}']
            rung = conn.execute('select lo, hi, label from rungs where view_id=? and position=?', (r['view_id'], data['rung'])).fetchone() if not errors else None
            gold = implied[r['view_id']]
            agree = None if rung is None else ((rung['lo'] is None or gold['high'] >= rung['lo']) and (rung['hi'] is None or gold['low'] < rung['hi']))
            results[arm][n] = {'answer': data, 'check_errors': errors, 'rung': data.get('rung') if isinstance(data, dict) else None,
                               'band': None if rung is None else [rung['lo'], rung['hi']], 'agrees_with_gold': agree,
                               'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]}
            json.dump({'requests_file': requests_path, 'gold_sha256': frozen, 'results': results}, open(out + '.partial.json', 'w'), indent=1, ensure_ascii=False)
    price_in, price_out = model.PRICES[cfg.rejudging.model]
    cost = sum(x['tokens'][0] / 1e6 * price_in + x['tokens'][1] / 1e6 * price_out for arm in results for x in results[arm])
    for arm in results:
        view_id = requests[arm]['view_id']
        print(f'{arm:20} gold {implied[view_id]["low"]:,.4g}..{implied[view_id]["high"]:,.4g} | rungs {[x["rung"] for x in results[arm]]} '
              f'| agrees {sum(1 for x in results[arm] if x["agrees_with_gold"])}/{sends} | refused {sum(1 for x in results[arm] if x["check_errors"])}')
    print(f'cost ${cost:.4f} at the published rates ({price_in}/{price_out} per million tokens, input uncached)')
    json.dump({'requests_file': requests_path, 'gold_sha256': frozen, 'results': results}, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'saved {out}')


if __name__ == '__main__':
    main()
