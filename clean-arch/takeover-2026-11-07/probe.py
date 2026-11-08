"""Re-send stored Step 1 requests under a control and a candidate prompt, several draws each, from the stored before-state.

The control is the stored request as sent in a stored run (its identity is checked before any send). The candidate replaces the system
text and sends the stored payload (the leading JSON of the stored user message, without any closing check the stored run appended)
followed by its own closing check; the article, open theses and schema are unchanged.
Each (arm, draw) has its own archive so a repeated draw is a fresh sample, never a cached answer."""
import argparse
import concurrent.futures
import hashlib
import json
import sqlite3
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch/step1')]
from hivemind import config, model  # noqa: E402
import runner  # noqa: E402

RUN_FOLDERS = ['clean-step1-2026-07-08-09-continuing', 'clean-step1-2026-07-08-09-segment-2']
SETTING = config.Setting('clean-step1', 'gpt-6-luna', 'clean-step1', 'low', 12000)


def stored_requests(traces, manifest):
    ids = json.loads(Path(manifest).read_text())['item_ids']
    by_id = {}
    for trace in traces:
        conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
        for input_id, request in conn.execute("select input_id, request from trace where status='complete'"):
            by_id[input_id] = json.loads(request)
    return {number: by_id[input_id] for number, input_id in enumerate(ids, 1) if input_id in by_id}


def arm_config(arm, candidate_dir, prd_schema):
    """An arm's schema and model setting: `<arm>-schema.json` and `<arm>-settings.json` beside the prompts when present."""
    base = arm.split('@')[0]
    schema_path = next((candidate_dir / f'{name}-schema.json' for name in (arm, base) if (candidate_dir / f'{name}-schema.json').exists()), None)
    settings_path = candidate_dir / f'{arm}-settings.json'
    schema = json.loads(schema_path.read_text()) if schema_path else prd_schema
    setting = SETTING
    if settings_path.exists():
        s = json.loads(settings_path.read_text())
        setting = config.Setting('clean-step1', s.get('model', SETTING.model), 'clean-step1', s.get('reasoning_effort', SETTING.reasoning_effort), s.get('max_output_tokens', SETTING.max_output_tokens))
        if s.get('provider', 'openai') != 'openai' or s.get('json_mode'):
            setting = (setting, s.get('provider', 'openai'))
    return schema, setting


def json_mode_call(setting, system, user, schema, provider):
    """JSON mode with the schema stated in the system text (DeepSeek refuses a strict schema; for OpenAI it isolates the request form):
    the answer is checked against the schema by code; a nonconforming answer fails the item, it is never repaired."""
    cap = 'max_completion_tokens' if provider == 'openai' else 'max_tokens'
    request = {'model': setting.model, cap: setting.max_output_tokens, 'response_format': {'type': 'json_object'},
               'messages': [{'role': 'system', 'content': system + '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(schema)},
                            {'role': 'user', 'content': user}]}
    if setting.reasoning_effort:
        request['reasoning_effort'] = setting.reasoning_effort
    response = model.openai_transport(provider, request)
    data = json.loads(response['choices'][0]['message']['content'])
    errors = model.check_schema(data, schema)
    if errors:
        raise model.SchemaError('; '.join(errors[:5]))
    usage = response.get('usage') or {}
    price_in, price_out = model.PRICES.get(setting.model, (0.0, 0.0))
    tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
    return SimpleNamespace(data=data, cached=False, input_tokens=tokens_in, output_tokens=tokens_out, cost_usd=round(tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out, 6))


def arm_texts(arm, stored, candidate_dir):
    if arm.startswith('control'):
        return stored['messages'][0]['content'], stored['messages'][1]['content']
    base = arm.split('@')[0]
    payload, end = json.JSONDecoder().raw_decode(stored['messages'][1]['content'])
    return ((candidate_dir / f'{base}-system.txt').read_text(encoding='utf-8'),
            stored['messages'][1]['content'][:end] + '\n\n' + (candidate_dir / f'{base}-closing.txt').read_text(encoding='utf-8'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--articles', required=True, help='comma-separated article numbers of the 49-article run')
    parser.add_argument('--arms', default='control,k1')
    parser.add_argument('--draws', type=int, default=3)
    parser.add_argument('--output', required=True, help='a new folder')
    parser.add_argument('--send', action='store_true', help='without it, only build and check the requests')
    parser.add_argument('--stored', default=','.join(str(ROOT / 'poc/data' / f / 'trace.sqlite') for f in RUN_FOLDERS),
                        help='comma-separated trace files whose requests are the control and whose payloads the candidates reuse')
    parser.add_argument('--manifest', default=str(ROOT / 'poc/data/clean-step1-2026-07-08-09/manifest.json'), help='numbers articles in its order')
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    candidate_dir = Path(__file__).resolve().parent
    _, schema = runner.draft(ROOT / 'clean-arch/PRD.md')
    requests = stored_requests(args.stored.split(','), args.manifest)
    articles = [int(x) for x in args.articles.split(',')]
    jobs = []
    for number in articles:
        stored = requests[number]
        if stored['response_format']['json_schema']['schema'] != schema:
            raise SystemExit(f'article {number}: stored schema differs from the PRD schema')
        rebuilt = model.build_request(SETTING, stored['messages'][0]['content'], stored['messages'][1]['content'], schema, 'clean_step1', 'openai')
        if rebuilt != stored:
            raise SystemExit(f'article {number}: rebuilt control request differs from the stored request')
        for arm in args.arms.split(','):
            system, user = arm_texts(arm, stored, candidate_dir)
            arm_schema, arm_setting = arm_config(arm, candidate_dir, schema)
            for draw in range(1, args.draws + 1):
                jobs.append((number, arm, draw, system, user, arm_schema, arm_setting))
    print(f'{len(jobs)} requests built; control requests match the stored bytes for {len(articles)} articles')
    if not args.send:
        return
    archives = {}
    def send(job):
        number, arm, draw, system, user, arm_schema, arm_setting = job
        archive = archives[(arm, draw)]
        cfg = SimpleNamespace(provider='openai', version=f'takeover-probe-{arm}', checksum=hashlib.sha256((system + user[-8000:]).encode()).hexdigest()[:16])
        payload = json.JSONDecoder().raw_decode(requests[number]['messages'][1]['content'])[0]
        item = {'text': payload['source_item']['text']}
        record = {'article': number, 'arm': arm, 'draw': draw}
        try:
            if isinstance(arm_setting, tuple):
                answer = json_mode_call(arm_setting[0], system, user, arm_schema, arm_setting[1])
            else:
                answer = model.call(archive, cfg, arm_setting, system, user, arm_schema, 'clean_step1', 'takeover_probe')
            record.update(cached=answer.cached, input_tokens=answer.input_tokens, output_tokens=answer.output_tokens, cost_usd=answer.cost_usd, answer=answer.data)
            try:
                checked = runner.validate(answer.data, arm_schema, item, payload['open_theses'])
                record['unfiled'] = [{'summary': ev['summary'], 'passages': ev['source_passages']} for ev in checked['unfiled_evidence']]
                record['kept_evidence'] = checked['evidence']
                record['unverified_passages'] = sum(p is None for ev in checked['evidence'] for p in ev['verified_source_passages'])
                record['unresolved_links'] = checked['unresolved_links']
                record['unlinked_new_theses'] = checked['unlinked_new_thesis_ids']
            except runner.ContractError as error:
                record['contract_error'] = str(error)
        except Exception as error:  # a failed send is recorded with its reason, never retried silently
            record['error'] = f'{type(error).__name__}: {error}'
        return record
    for arm in args.arms.split(','):
        for draw in range(1, args.draws + 1):
            archives[(arm, draw)] = model.Archive(str(out / f'archive-{arm}-d{draw}.sqlite'))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    (out / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=1))
    failed = [r for r in results if 'error' in r or 'contract_error' in r]
    print(f'sent {len(results)}; failed {len(failed)}; cost ${sum(r.get("cost_usd") or 0 for r in results):.4f}')
    for r in failed:
        print('  failed', r['article'], r['arm'], r['draw'], r.get('error') or r.get('contract_error'))
    for arm in args.arms.split(','):
        rows = [r for r in results if r['arm'] == arm and 'answer' in r]
        print(f'  {arm}: evidence {sum(len(r["answer"]["evidence"]) for r in rows)} over {len(rows)} answers; new theses {sum(len(r["answer"]["new_theses"]) for r in rows)}; '
              f'unverified passages {sum(r.get("unverified_passages", 0) for r in rows)}; output tokens {sum(r["output_tokens"] for r in rows)}')


if __name__ == '__main__':
    main()
