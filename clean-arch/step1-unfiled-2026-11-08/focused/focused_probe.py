"""Probe of a focused call for D388 (Alex, 2026-11-09: test a separate step; c8 unchanged). Code routes by identity only: each statement
c8 kept and linked to a binding_obligation thesis (open before the article, or opened in the same answer). One call per article reads
the article, every open and new thesis, and the routed statements, and decides per statement whether a signing thesis opens. Every
answer goes through the code contract below; a nonconforming answer is recorded, never repaired.

Usage: focused_probe.py <output folder> --plan <plan.json> [--send]
plan.json: [{"case": "dev-4", "trace": "<trace.sqlite>", "sequence": 4, "draws": 3}]"""
import argparse, concurrent.futures, json, re, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/takeover-2026-11-07')]
from hivemind import config, model  # noqa: E402
from probe import json_mode_call  # noqa: E402

SETTING = config.Setting('clean-step1', 'deepseek-flash', 'clean-step1', 'high', 32000)
SYSTEM = (HERE / 'system.txt').read_text(encoding='utf-8')
CLOSING = (HERE / 'closing.txt').read_text(encoding='utf-8')
SCHEMA = json.loads((HERE / 'schema.json').read_text(encoding='utf-8'))
COMPANY = {'name': 'NVIDIA', 'most_recent_annual_profit': 'net income of $120.067 billion for fiscal year 2026 (ended January 2026)',
           'five_percent_of_that_profit': 'about $6.0 billion',
           'source': "NVIDIA's fourth-quarter fiscal 2026 results release, 8-K exhibit 99.1, filed 2026-02-26 "
                     '(corpus item edgar:NVDA:0001045810-26-000019:q4fy26pr.htm)'}


def stored_case(trace, sequence):
    """The stored c8 request payload and answer for one article, and the opening reason of every thesis opened before it."""
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    kinds = {}
    for (result,) in conn.execute("select result from trace where status='complete' and sequence<? order by sequence", (sequence,)):
        answer = json.loads(result)
        ids = answer.get('new_thesis_ids') or {}
        kinds.update({ids[t['local_id']]: t.get('opens_as') for t in answer['new_theses'] if t['local_id'] in ids})
    request, result = conn.execute('select request, result from trace where sequence=?', (sequence,)).fetchone()
    payload = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]
    return payload, json.loads(result), kinds


def route(answer, kinds):
    """Identity only: the statements linked to a binding_obligation thesis, with those thesis IDs."""
    new_kinds = {t['local_id']: t.get('opens_as') for t in answer['new_theses']}
    routed = []
    for item in answer['evidence']:
        targets = [link['target_id'] for link in item['links']
                   if (kinds if link['target_type'] == 'existing' else new_kinds).get(link['target_id']) == 'binding_obligation']
        if targets:
            routed.append((item, targets))
    return routed


def build(payload, answer, routed):
    source = payload['source_item']
    theses = ([{'id': t['id'], 'description': t['description']} for t in payload['open_theses']]
              + [{'id': t['local_id'], 'description': t['description'], 'new_in_this_item': True} for t in answer['new_theses']])
    statements = [{'local_id': item['local_id'], 'summary': item['summary'], 'source_passages': item['source_passages'],
                   'linked_to': targets} for item, targets in routed]
    body = {'company': COMPANY, 'source_item': {key: source.get(key) for key in ('title', 'published_at', 'text')}, 'theses': theses,
            'statements': statements}
    return json.dumps(body, ensure_ascii=False) + '\n\n' + CLOSING, {t['id'] for t in theses}


def check(data, routed_ids, thesis_ids):
    """The code contract: one decision per routed statement; opens exactly when every condition holds; each opened statement under
    exactly one new signing thesis, nothing else under one, and no empty or repeated new thesis."""
    errors = []
    decided = [d['statement'] for d in data['decisions']]
    if sorted(decided) != sorted(routed_ids):
        errors.append(f'decisions {sorted(decided)} != routed {sorted(routed_ids)}')
    opened = {d['statement'] for d in data['decisions'] if d['opens']}
    for d in data['decisions']:
        holds = (d['signed_status'] == 'not_yet_signed' and d['large_enough'] and d['separate_bet'] and d['settleable']
                 and d['already_asked_by'] is None)
        if d['opens'] != holds:
            errors.append(f"{d['statement']}: opens is {d['opens']} but the conditions give {holds}")
        if d['already_asked_by'] is not None and d['already_asked_by'] not in thesis_ids:
            errors.append(f"{d['statement']}: unknown thesis {d['already_asked_by']}")
    listed = [s for t in data['new_signing_theses'] for s in t['statements']]
    if sorted(listed) != sorted(opened):
        errors.append(f'statements under new theses {sorted(listed)} != opened {sorted(opened)}')
    local_ids = [t['local_id'] for t in data['new_signing_theses']]
    if len(set(local_ids)) != len(local_ids) or any(not t['statements'] for t in data['new_signing_theses']):
        errors.append('a repeated or empty new signing thesis')
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output'); parser.add_argument('--plan', required=True); parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    jobs, skipped = [], []
    for case in json.loads(Path(args.plan).read_text()):
        payload, answer, kinds = stored_case(case['trace'], case['sequence'])
        routed = route(answer, kinds)
        if not routed:
            skipped.append(case['case'])
            continue
        user, thesis_ids = build(payload, answer, routed)
        for draw in range(1, case['draws'] + 1):
            jobs.append((case, draw, user, [item['local_id'] for item, _ in routed], thesis_ids))
    chars = sum(len(SYSTEM) + len(json.dumps(SCHEMA)) + len(j[2]) for j in jobs)
    price_in, price_out = model.PRICES[SETTING.model]
    print(f'{len(jobs)} requests over {len({j[0]["case"] for j in jobs})} articles; about {chars // 4} input tokens; about '
          f'${chars / 4 / 1e6 * price_in + len(jobs) * 3000 / 1e6 * price_out:.2f} at published rates (3k output tokens each assumed); skipped with no routed statement: {skipped}')
    if not args.send:
        return
    out = Path(args.output); out.mkdir(parents=True, exist_ok=False)
    def send(job):
        case, draw, user, routed_ids, thesis_ids = job
        record = {'case': case['case'], 'sequence': case['sequence'], 'trace': case['trace'], 'draw': draw, 'routed': routed_ids}
        request = {'model': SETTING.model, 'max_tokens': SETTING.max_output_tokens, 'response_format': {'type': 'json_object'},
                   'reasoning_effort': SETTING.reasoning_effort,
                   'messages': [{'role': 'system', 'content': SYSTEM + '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(SCHEMA)},
                                {'role': 'user', 'content': user}]}
        response = None
        for attempt in (1, 2):   # a transport error is re-sent once; both attempts are recorded
            try:
                response = model.openai_transport('deepseek', request)
                break
            except Exception as error:
                record.setdefault('transport_errors', []).append(f'attempt {attempt}: {type(error).__name__}: {error}')
        if response is None:
            record['error'] = record['transport_errors'][-1]
            return record
        usage = response.get('usage') or {}
        tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
        record.update(input_tokens=tokens_in, output_tokens=tokens_out,
                      cost_usd=round(tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out, 6),
                      raw=response['choices'][0]['message']['content'])
        try:
            data = json.loads(record['raw'])
        except json.JSONDecodeError as error:
            record['contract_errors'] = [f'not JSON: {error}']
            return record
        record['answer'] = data
        schema_errors = model.check_schema(data, SCHEMA)
        record['contract_errors'] = schema_errors[:5] if schema_errors else check(data, routed_ids, thesis_ids)
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(send, jobs))
    (out / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    print(f"{len(records)} records; errors {sum('error' in r for r in records)}; contract errors {sum(bool(r.get('contract_errors')) for r in records)}; "
          f"${sum(r.get('cost_usd', 0) for r in records):.2f}")


if __name__ == '__main__':
    main()
