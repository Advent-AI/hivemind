"""Probe arms on stored K6b Step 1 requests (DeepSeek Flash, high effort, JSON mode with the schema in the system text), several draws
each, from a fixed before-state: the stored one, or an empty open-thesis list (a labelled synthetic bootstrap state).

The control arm ("k6b") must rebuild the stored request exactly (system text, user message, schema) before anything is sent. A candidate
replaces the system text, closing check or schema from `arms/<arm>-*`; the article and before-state are unchanged. Every answer goes
through the runner's checks; a nonconforming answer is recorded, never repaired.

Usage: probe_unfiled.py <cases.json> <output folder> --arms k6b,u1,u3,u1u3 --draws 3 [--send]
cases.json: [{"case": "d1-40", "trace": "<trace.sqlite>", "sequence": 40, "state": "stored" | "empty"}]"""
import argparse, concurrent.futures, json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1'), str(ROOT / 'clean-arch/takeover-2026-11-07')]
from hivemind import config, model  # noqa: E402
import runner  # noqa: E402
from probe import json_mode_call  # noqa: E402

SETTING = config.Setting('clean-step1', 'deepseek-flash', 'clean-step1', 'high', 32000)


def dump(obj):
    return json.dumps(obj, ensure_ascii=False)


def build(case, arm):
    conn = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
    request = json.loads(conn.execute('select request from trace where sequence=?', (case['sequence'],)).fetchone()[0])
    stored_user = request['messages'][1]['content']
    payload, end = json.JSONDecoder().raw_decode(stored_user)
    if case['state'] == 'empty':
        payload = dict(payload, open_theses=[])
    system = (HERE / 'arms' / f'{arm}-system.txt').read_text(encoding='utf-8')
    closing = (HERE / 'arms' / f'{arm}-closing.txt').read_text(encoding='utf-8')
    schema = json.loads((HERE / 'arms' / f'{arm}-schema.json').read_text(encoding='utf-8'))
    user = dump(payload) + '\n\n' + closing
    if arm == 'k6b' and case['state'] == 'stored':
        stored_schema = request['response_format']['json_schema']['schema']
        if (system, user, schema) != (request['messages'][0]['content'], stored_user, stored_schema):
            raise SystemExit(f"{case['case']}: the control does not rebuild the stored request")
    return system, user, schema, payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cases')
    parser.add_argument('output')
    parser.add_argument('--arms', required=True)
    parser.add_argument('--draws', type=int, default=3)
    parser.add_argument('--send', action='store_true')
    parser.add_argument('--max-output', type=int, default=SETTING.max_output_tokens, help='the output token cap sent with every request')
    args = parser.parse_args()
    setting = SETTING._replace(max_output_tokens=args.max_output) if hasattr(SETTING, '_replace') else __import__('dataclasses').replace(SETTING, max_output_tokens=args.max_output)
    cases = json.loads(Path(args.cases).read_text())
    jobs = []
    for case in cases:
        for arm in args.arms.split(','):
            system, user, schema, payload = build(case, arm)
            for draw in range(1, args.draws + 1):
                jobs.append((case, arm, draw, system, user, schema, payload))
    chars = sum(len(j[3]) + len(j[4]) + len(json.dumps(j[5])) for j in jobs)
    price_in, price_out = model.PRICES[SETTING.model]
    print(f'{len(jobs)} requests; the control rebuilds the stored request for every stored-state case; about {chars // 4} input tokens, '
          f'about ${chars / 4 / 1e6 * price_in + len(jobs) * 6000 / 1e6 * price_out:.2f} at published rates (6k output tokens each assumed)')
    if not args.send:
        return
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    def send(job):
        case, arm, draw, system, user, schema, payload = job
        record = {'case': case['case'], 'sequence': case['sequence'], 'state': case['state'], 'arm': arm, 'draw': draw}
        try:
            answer = json_mode_call(setting, system, user, schema, 'deepseek')
            record.update(input_tokens=answer.input_tokens, output_tokens=answer.output_tokens, cost_usd=answer.cost_usd, answer=answer.data)
            try:
                checked = runner.validate(answer.data, schema, {'text': payload['source_item']['text']}, payload['open_theses'])
                record.update(kept=checked['evidence'], unfiled=checked['unfiled_evidence'], new_theses=answer.data['new_theses'],
                              unresolved_links=checked['unresolved_links'], unlinked_new_theses=checked['unlinked_new_thesis_ids'])
            except runner.ContractError as error:
                record['contract_error'] = str(error)
        except Exception as error:   # recorded with its reason, never retried silently
            record['error'] = f'{type(error).__name__}: {error}'
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(send, jobs))
    (out / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    print(f"{len(records)} records; errors {sum('error' in r for r in records)}; contract errors {sum('contract_error' in r for r in records)}; "
          f"${sum(r.get('cost_usd', 0) for r in records):.2f}")


if __name__ == '__main__':
    main()
