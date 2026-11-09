"""Probe of the candidate c12 against c8 (DESIGN.md §6) on stored clean Step 1 requests, from their stored before-states, so the arms
differ only in the request. The c8 arm is the stored request exactly as it was sent: the stored request must be c8 (its system text is
c8-system.txt and its user message ends with c8-closing.txt) and the stored sent request must be the live transport's form of it. The
c12 arm is the same stored request with only the system text and the closing check replaced by c12's, put in the transport's form the
same way. Every answer goes through the runner's checks. A gold fact counts as written when a kept item quotes its passage
(stage1_probe.quotes_gold) and as delivered to the theses that item links.

Usage: q12_probe.py <cases.json> <output folder> [--draws 3] [--send]
cases.json: [{"case": "...", "trace": "<path, or segments joined with '+'>", "input_id": "...", "gold": ["i131", ...]}]"""
import argparse, concurrent.futures, json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
from hivemind import model  # noqa: E402
import runner  # noqa: E402
from live import deepseek_json_mode  # noqa: E402
from stage1_probe import dump, quotes_gold  # noqa: E402

ARMS = ROOT / 'clean-arch/step1-unfiled-2026-11-08/arms'
PACKET = ROOT / 'docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json'


def arm_texts(arm):
    return ((ARMS / f'{arm}-system.txt').read_text(encoding='utf-8'), (ARMS / f'{arm}-closing.txt').read_text(encoding='utf-8'),
            json.loads((ARMS / f'{arm}-schema.json').read_text(encoding='utf-8')))


def stored_row(trace, input_id):
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        row = conn.execute("select request, raw_response, before_state from trace where input_id=? and status='complete'", (input_id,)).fetchone()
        conn.close()
        if row:
            return row
    raise SystemExit(f'{input_id} has no completed row in {trace}')


def build_jobs(cases, draws):
    c8_system, c8_closing, c8_schema = arm_texts('c8')
    c12_system, c12_closing, c12_schema = arm_texts('c12')
    jobs = []
    for case in cases:
        request_text, raw, before = stored_row(case['trace'], case['input_id'])
        stored, sent = json.loads(request_text), json.loads(raw)['sent_request']
        if json.dumps(sent) != json.dumps(deepseek_json_mode(stored, sent.get('reasoning_effort'))):   # bytes as sent, key order included
            raise SystemExit(f"{case['case']}: the sent request is not, byte for byte, the live transport's form of the stored request")
        stored_user = stored['messages'][1]['content']
        payload, end = json.JSONDecoder().raw_decode(stored_user)
        if stored['messages'][0]['content'] != c8_system or stored_user != dump(payload) + '\n\n' + c8_closing:
            raise SystemExit(f"{case['case']}: the stored request is not c8")
        if stored['response_format']['json_schema']['schema'] != c8_schema:
            raise SystemExit(f"{case['case']}: the stored schema is not c8's")
        if payload['open_theses'] != [{k: t[k] for k in ('id', 'description', 'outcome', 'period')} for t in json.loads(before)]:
            raise SystemExit(f"{case['case']}: the stored payload does not show the stored before-state")
        candidate = json.loads(json.dumps(stored))
        candidate['messages'][0]['content'] = c12_system
        candidate['messages'][1]['content'] = dump(payload) + '\n\n' + c12_closing
        candidate['response_format']['json_schema']['schema'] = c12_schema
        candidate_sent = deepseek_json_mode(candidate, sent.get('reasoning_effort'))
        item = {'text': payload['source_item']['text']}
        for draw in range(1, draws + 1):
            jobs.append((case, 'c8', draw, sent, item, payload['open_theses'], c8_schema))
            jobs.append((case, 'c12', draw, candidate_sent, item, payload['open_theses'], c12_schema))
    return jobs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cases'); parser.add_argument('output')
    parser.add_argument('--draws', type=int, default=3, choices=[1, 2, 3]); parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    cases = json.loads(Path(args.cases).read_text())
    jobs = build_jobs(cases, args.draws)
    price_in, price_out = model.PRICES['deepseek-flash']
    chars = sum(len(json.dumps(j[3])) for j in jobs)
    print(f'{len(jobs)} requests over {len(cases)} cases; about {chars // 4} input tokens; about '
          f'${chars / 4 / 1e6 * price_in + len(jobs) * 6000 / 1e6 * price_out:.2f} at published rates with 6k output tokens each '
          f'(an estimate: input tokens are estimated and up to three transport attempts are possible)')
    if not args.send:
        return
    gold = {i['id']: i for i in json.loads(PACKET.read_text())['items']}
    out = Path(args.output); out.mkdir(parents=True, exist_ok=False)
    def send(job):
        case, arm, draw, request, item, shown, schema = job
        record = {'case': case['case'], 'arm': arm, 'draw': draw}
        try:
            response = model.openai_transport('deepseek', request)
        except Exception as error:   # recorded with its reason, never retried silently
            record['error'] = f'{type(error).__name__}: {error}'
            return record
        usage = response.get('usage') or {}
        record.update(input_tokens=usage.get('prompt_tokens'), cached_tokens=usage.get('prompt_cache_hit_tokens'),
                      output_tokens=usage.get('completion_tokens'))
        try:
            record['raw'] = response['choices'][0]['message']['content']
            answer = json.loads(record['raw'])
            checked = runner.validate(answer, schema, item, shown)
        except Exception as error:
            record['contract_error'] = f'{type(error).__name__}: {error}'
            return record
        record['kept'] = [{'summary': e['summary'], 'links': [l['target_id'] for l in e['links'] if l['target_type'] == 'existing'],
                           'passages': e.get('verified_source_passages') or e['source_passages']} for e in checked['evidence']]
        record['new_theses'] = answer['new_theses']
        record['written'] = {g: any(quotes_gold(e, gold[g]['passage']) for e in checked['evidence']) for g in case['gold']}
        record['delivered'] = {g: sorted({l['target_id'] for e in checked['evidence'] if quotes_gold(e, gold[g]['passage'])
                                          for l in e['links'] if l['target_type'] == 'existing'}) for g in case['gold']}
        return record
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        records = list(pool.map(send, jobs))
    (out / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    tokens = [sum(r.get(k) or 0 for r in records) for k in ('input_tokens', 'cached_tokens', 'output_tokens')]
    cost = ((tokens[0] - tokens[1]) * price_in + tokens[1] * price_in * model.CACHED_INPUT_SHARE + tokens[2] * price_out) / 1e6
    print(f"{len(records)} records; errors {sum('error' in r for r in records)}; contract errors {sum('contract_error' in r for r in records)}; "
          f'${cost:.2f} at published rates')


if __name__ == '__main__':
    main()
