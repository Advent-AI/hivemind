"""Probe-6 diagnostics (AGENTS §1): (1) re-send the two requests whose c2 answers were not valid JSON and record finish_reason, token
usage and content length; (2) ask the model's own account for the d2-6 new theses. Usage: probe6_diagnose.py <records.json> <out.json>"""
import concurrent.futures, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_unfiled  # noqa: E402
from hivemind import model  # noqa: E402


def request(system, user, schema, extra=None, max_tokens=None):
    body = {'model': probe_unfiled.SETTING.model, 'max_tokens': max_tokens or probe_unfiled.SETTING.max_output_tokens,
            'response_format': {'type': 'json_object'}, 'reasoning_effort': probe_unfiled.SETTING.reasoning_effort,
            'messages': [{'role': 'system', 'content': system + '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(schema)},
                         {'role': 'user', 'content': user}]}
    if extra:
        body.pop('response_format')
        body['max_tokens'] = 4000
        body['messages'] += extra
    return body


def main():
    records = json.loads(Path(sys.argv[1]).read_text())
    cases = {c['case']: c for c in json.loads((HERE / 'cases.json').read_text())}
    jobs = []
    for name in ('empty-62', 'empty-85'):
        system, user, schema, _ = probe_unfiled.build(cases[name], 'c2')
        jobs.append(({'kind': 'resend', 'case': name}, request(system, user, schema)))
    system, user, schema, _ = probe_unfiled.build(cases['d2-6'], 'c2')
    for r in records:
        if r['case'] == 'd2-6' and r['arm'] == 'c2' and r.get('new_theses'):
            thesis = r['new_theses'][0]['description']
            question = (f'You proposed the new thesis "{thesis}". Which instruction in this request led you to open it rather than leave the '
                        'statement unfiled? Quote it, and name the two statements in the request you set aside. At most 150 words.')
            extra = [{'role': 'assistant', 'content': json.dumps(r['answer'], ensure_ascii=False)}, {'role': 'user', 'content': question}]
            jobs.append(({'kind': 'account', 'case': 'd2-6', 'draw': r['draw']}, request(system, user, schema, extra)))
    def send(job):
        meta, body = job
        try:
            response = model.openai_transport('deepseek', body)
        except Exception as error:
            return dict(meta, error=f'{type(error).__name__}: {error}')
        choice = response['choices'][0]
        content = choice['message'].get('content') or ''
        usage = response.get('usage') or {}
        out = dict(meta, finish_reason=choice.get('finish_reason'), usage=usage, content_chars=len(content))
        if meta['kind'] == 'resend':
            try:
                json.loads(content)
                out['valid_json'] = True
            except ValueError as error:
                out['valid_json'] = False
                out['json_error'] = str(error)
        else:
            out['reply'] = content
        return out
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(send, jobs))
    Path(sys.argv[2]).write_text(json.dumps(results, ensure_ascii=False, indent=1))
    for r in results:
        print(json.dumps({k: v for k, v in r.items() if k != 'reply'}, ensure_ascii=False))
        if 'reply' in r:
            print('  ', r['reply'])


if __name__ == '__main__':
    main()
