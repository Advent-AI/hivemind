"""A neutral check of the conclusion "asked afterwards, the model files correctly" before the re-check is written (Alex: "单开始前再trace一次看看你是
不是结论正确"). For every answer of one arm of answers.json, the statements production would drop as homeless and the statements kept only under a
company-wide revenue question (v1 FY2027, v22 FY2028) are listed back to the model in the same conversation (the arm's request rebuilt as sent,
the answer's evidence list as the assistant turn, without its candidates), with one question that names no question id and quotes the arm's links instruction (the
reply schema replaces the extraction schema, where that instruction lives): give each statement's narrowest open question, or none. No question is suggested, so agreement with the gold cannot come from the probe.

Scored against the frozen golds: a statement whose matter the judgement gold uses has known homes (the seeds of those questions); a span the
extraction standard does not keep should get none; a kept matter no question uses is printed for reading.

usage: python3 probe_refile.py <arm> <out.json>
"""
import concurrent.futures
import copy
import json
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import measure_filing as mf  # noqa: E402
import resend_filing as rf  # noqa: E402
from hivemind import config, model  # noqa: E402

REVENUE_ROOTS = {'v1', 'v22'}
QUESTION = ('Re-read [Open questions] with the links field\'s instruction. For each statement listed below, give the id of the narrowest open question '
            'whose answer it makes more or less likely, or none when no open question is connected. Statements:\n')
REFILE_SCHEMA = {'type': 'object', 'additionalProperties': False, 'required': ['refile'], 'properties': {'refile': {'type': 'array', 'items': {
    'type': 'object', 'additionalProperties': False, 'required': ['id', 'links'], 'properties': {
        'id': {'type': 'string'}, 'links': {'type': 'array', 'items': {'type': 'string'}}}}}}}


def main():
    arm, out = sys.argv[1], sys.argv[2]
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    selection = json.load(open(f'{rf.HERE}/selection.json'))
    answers = json.load(open(f'{rf.HERE}/answers.json'))
    rules = json.load(open(f'{rf.HERE}/links-rules.json'))
    items_conn, archive, views = rf.ro(rf.ITEMS), rf.ro(f'{rf.DRAW}/archive.sqlite'), rf.ro(f'{rf.DRAW}/views.sqlite')
    jobs = []
    for input_id, per in answers.items():
        meta = selection['articles'][input_id]
        built = rf.rebuild(cfg, items_conn, archive, views, input_id, meta['call_id'], meta['request_sha256'])
        for n, result in enumerate(per[arm]):
            listed = result['homeless'] + [s for s in result['kept'] if set(s['links']) <= REVENUE_ROOTS]
            if listed:
                jobs.append((input_id, n, built, result, listed))

    def one(job):
        input_id, n, built, result, listed = job
        item, setting, system, user, schema, shown, parents = built
        variant = copy.deepcopy(schema)
        variant['properties']['evidence']['items']['properties']['links']['description'] = rules[arm]
        body = model.build_request(setting, system, user, variant, 'extraction', cfg.provider)
        assistant = json.dumps({'evidence': result['raw'], 'candidates': [], 'new_groups': []}, ensure_ascii=False)
        follow = (QUESTION.replace("with the links field's instruction", f'with the links field\'s instruction, which reads: "{rules[arm]}"')
                  + '\n'.join(f'- {s["id"]}: {s["one_line"]}' for s in listed))
        body['messages'] = body['messages'] + [{'role': 'assistant', 'content': assistant}, {'role': 'user', 'content': follow}]
        body['response_format'] = {'type': 'json_schema', 'json_schema': {'name': 'refile', 'strict': True, 'schema': REFILE_SCHEMA}}
        reply = model.openai_transport(cfg.provider, body)
        refile = {r['id']: [l for l in r['links'] if l in shown] for r in json.loads(reply['choices'][0]['message']['content'])['refile']}
        return input_id, n, [dict(s, before=s['links'], after=refile.get(s['id'], ['(not answered)'])) for s in listed], reply.get('usage') or {}

    results = []
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for input_id, n, rows, usage in pool.map(one, jobs):
            results.append({'input_id': input_id, 'send': n, 'rows': rows, 'tokens': [usage.get('prompt_tokens', 0), usage.get('completion_tokens', 0)]})
    json.dump(results, open(out, 'w'), ensure_ascii=False)
    print(f'{len(jobs)} conversations, {sum(len(r["rows"]) for r in results)} statements re-filed; saved {out}')


if __name__ == '__main__':
    main()
