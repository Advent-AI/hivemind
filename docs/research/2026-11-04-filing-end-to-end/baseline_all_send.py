"""Send the all-seeds judging test (baseline-design.md, round 8): each request of the pinned requests file as many times as it says (a control
three times, an arm once), rebuilt by `model.build_request` with the frozen judging configuration and refused unless its archive key equals the
one recorded when it was built and read. Each answer is checked as production checked it when the request was made: `judging.check_answer`
against the text that was sent, with the changed rule read against the previous conclusion that text carried (the ledger's current state is the
stored answer to a control request, not its previous conclusion). A refused answer counts as not judged. Each answer is scored by the frozen
scorer's rule (`score_judgement.py`; the gold read from gold-v1.json and refused unless its sha256 is the frozen one): a numeric question agrees
when the gold's implied range overlaps the band [lo, hi) of the chosen rung, a yes/no question when the chosen rung's label is "Yes" exactly when
the gold says yes; rungs read from the request's draw.

usage: python3 baseline_all_send.py --verify                      (scores the three draws' stored last judgements with this rule and compares
                                                                    each question with score_judgement.py; sends nothing)
       python3 baseline_all_send.py <requests.json> <out.json>
"""
import concurrent.futures
import hashlib
import json
import re
import sqlite3
import subprocess
import sys
import time

ROOT = '/Users/lchingen/hivemind'
HERE = f'{ROOT}/docs/research/2026-11-04-filing-end-to-end'
sys.path[:0] = [f'{ROOT}/src', HERE]
from baseline_all import DRAWS  # noqa: E402
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

GOLD = f'{ROOT}/docs/research/2026-11-01-e2e-loop/judgement-gold'
WINDOW_END = '2026-07-14'
PREVIOUS = re.compile(r'^\[Previous conclusion, for comparison only\] rung (\d+);', re.M)
CHANGED_RULE = re.compile(r'^rung moved from \d+ to \d+ but changed is false$|^first judgement must say changed$')


def gold():
    """{seed view id: (implied outcome, unit)} from the frozen gold, refused unless its sha256 is the frozen one."""
    gold_bytes = open(f'{GOLD}/gold-v1.json', 'rb').read()
    frozen = open(f'{GOLD}/gold-v1.sha256').read().split()[0]
    if hashlib.sha256(gold_bytes).hexdigest() != frozen:
        raise SystemExit('gold-v1.json is not the frozen gold: refused')
    units = {q['id']: q['unit'] for q in json.load(open(f'{GOLD}/questions-v1.json'))['questions']}
    out = {}
    for entry in json.loads(gold_bytes)['entries']:
        if entry.get('no_view') or not entry.get('seed_view_id'):
            continue
        resolved = entry.get('resolution') or entry
        if resolved.get('implied_outcome'):
            out[entry['seed_view_id']] = (resolved['implied_outcome'], units[entry['question_id']])
    return frozen, out


def agrees(rung, implied, unit):
    if unit == 'yes/no':
        return (rung['label'].lower() == 'yes') == bool(implied['yes_no'])
    return (rung['lo'] is None or implied['high'] >= rung['lo']) and (rung['hi'] is None or implied['low'] < rung['hi'])


def answer_errors(conn, view_id, data, user):
    errors = [e for e in judging.check_answer(conn, view_id, data, request_text=user) if not CHANGED_RULE.match(e)]
    previous = PREVIOUS.search(user)
    if previous is None and not data['changed']:
        errors.append('first judgement must say changed')
    if previous is not None and int(previous.group(1)) != data['rung'] and not data['changed']:
        errors.append(f'rung moved from {previous.group(1)} to {data["rung"]} but changed is false')
    return errors


def verify():
    """This rule on the stored last judgements of the three draws, question by question, against score_judgement.py's printed outcomes."""
    _, implied = gold()
    differ = 0
    for draw, run in DRAWS.items():
        conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
        conn.row_factory = sqlite3.Row
        printed = subprocess.run([sys.executable, f'{GOLD}/score_judgement.py', run], capture_output=True, text=True, check=True).stdout
        scorer = {f'v{int(m.group(1))}': m.group(2) for m in re.finditer(r'^q(\d\d) (agree|DISAGREE|no judgement)', printed, re.M) if int(m.group(1)) <= 22}
        mine = {}
        for view_id, (outcome, unit) in implied.items():
            j = conn.execute('select rung from judgements where view_id=? and publication_day<=? order by judgement_id desc limit 1', (view_id, WINDOW_END)).fetchone()
            if j is None:
                mine[view_id] = 'no judgement'
                continue
            rung = conn.execute('select lo, hi, label from rungs where view_id=? and position=?', (view_id, j['rung'])).fetchone()
            mine[view_id] = 'agree' if agrees(rung, outcome, unit) else 'DISAGREE'
        wrong = {v: (mine[v], scorer.get(v)) for v in mine if mine[v] != scorer.get(v)}
        differ += len(wrong) + (set(scorer) != set(mine))
        print(f'{draw}: {len(mine)} questions, agree {sum(x == "agree" for x in mine.values())}, disagree {sum(x == "DISAGREE" for x in mine.values())}, '
              f'no judgement {sum(x == "no judgement" for x in mine.values())}; differs from score_judgement.py on {wrong or "none"}')
    sys.exit(1 if differ else 0)


def main():
    if sys.argv[1] == '--verify':
        return verify()
    requests_path, out = sys.argv[1], sys.argv[2]
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    schema = judging.schema_for(cfg.rejudging.prompt_version)
    frozen, implied = gold()
    pinned = open(requests_path + '.sha256').read().split()[0]
    if hashlib.sha256(open(requests_path, 'rb').read()).hexdigest() != pinned:
        raise SystemExit(f'{requests_path} is not the pinned, reviewed version: nothing sent')
    requests = {k: r for k, r in json.load(open(requests_path)).items() if r['sends']}
    bodies = {}
    for key, r in requests.items():
        body = model.build_request(cfg.rejudging, r['system'], r['user'], schema, 'judgement', cfg.provider)
        if model.request_identity(body)[1] != r['request_sha256']:
            raise SystemExit(f'{key}: the request differs from the one built and read; nothing sent')
        bodies[key] = body
    conns = {}
    for run in {r['run'] for r in requests.values()}:
        conns[run] = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True, check_same_thread=False)
        conns[run].row_factory = sqlite3.Row
    print(f'gold sha256 {frozen[:16]}… (frozen); {len(bodies)} requests, {sum(r["sends"] for r in requests.values())} sends, judging '
          f'{cfg.rejudging.prompt_version} on {cfg.rejudging.model}', flush=True)

    def send(job):
        """One reply. Only a transport failure is re-sent (the same bytes); a reply that is not a readable answer is kept and counts as not judged."""
        key, n = job
        for attempt in range(4):
            try:
                reply = model.openai_transport(cfg.provider, bodies[key], timeout=300)
                break
            except Exception as error:
                if attempt == 3:
                    return key, n, None, {}, f'transport: {type(error).__name__}: {str(error)[:200]}'
                print(f'  {key} send {n}: {type(error).__name__}; re-sent in {30 * (attempt + 1)} s', flush=True)
                time.sleep(30 * (attempt + 1))
        content = reply['choices'][0]['message']['content']
        try:
            return key, n, json.loads(content), reply.get('usage') or {}, None
        except ValueError:
            return key, n, content, reply.get('usage') or {}, 'reply is not JSON'

    jobs = [(key, n) for key, r in requests.items() for n in range(r['sends'])]
    results = {key: [None] * r['sends'] for key, r in requests.items()}
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for key, n, data, usage, failure in pool.map(send, jobs):
            r = requests[key]
            conn = conns[r['run']]
            if failure:
                errors = [failure]
            else:
                try:
                    errors = answer_errors(conn, r['view_id'], data, r['user'])
                except Exception as error:                         # an answer missing a field is refused, not a crash
                    errors = [f'check failed: {type(error).__name__}: {error}']
            rung = conn.execute('select lo, hi, label from rungs where view_id=? and position=?', (r['view_id'], data['rung'])).fetchone() if not errors else None
            outcome, unit = implied[r['view_id']]
            agree = None if rung is None else agrees(rung, outcome, unit)
            results[key][n] = {'answer': data, 'check_errors': errors, 'rung': data.get('rung') if isinstance(data, dict) else None,
                               'label': None if rung is None else rung['label'], 'agrees_with_gold': agree,
                               'cites_records': sorted(set(data.get('cites', [])) & {p['evidence_id'] for p in r['pieces']}) if isinstance(data, dict) else [],
                               'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]}
            json.dump({'requests_file': requests_path, 'gold_sha256': frozen, 'results': results}, open(out + '.partial.json', 'w'), indent=1, ensure_ascii=False)
    price_in, price_out = model.PRICES[cfg.rejudging.model]
    cost = sum(x['tokens'][0] / 1e6 * price_in + x['tokens'][1] / 1e6 * price_out for key in results for x in results[key])
    for key in results:
        print(f'{key:22} rungs {[x["rung"] for x in results[key]]} | agrees {sum(1 for x in results[key] if x["agrees_with_gold"])}/{len(results[key])} '
              f'| refused {sum(1 for x in results[key] if x["check_errors"])}')
    print(f'cost ${cost:.4f} at the published rates ({price_in}/{price_out} per million tokens, input uncached)')
    json.dump({'requests_file': requests_path, 'gold_sha256': frozen, 'results': results}, open(out, 'w'), indent=1, ensure_ascii=False)
    print(f'saved {out}')


if __name__ == '__main__':
    main()
