"""The model's own account of a probe's thesis decisions (AGENTS §1): rebuild the probe request as `probe.json_mode_call` sends it,
put the recorded answer back as the assistant turn (re-serialised from the parsed answer: the probe keeps no raw text, so key order
and spacing may differ), and ask one fixed question. It locates a reason; it does not prove a fix.

Usage: thesis_account.py <records.json>... --asks <asks.json> --output <output.json> [--send]
asks.json: [{"case": "fresh-47", "arm": "c10a", "draw": 1, "thesis": "NT1"} | {..., "statement": "<words of a kept summary>"}]"""
import argparse, concurrent.futures, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import probe_unfiled  # noqa: E402
from probe_unfiled import model  # noqa: E402

OPENED = ('In your answer you proposed the new thesis "{subject}". Which instruction in this request led you to open it? Quote it. '
          'How did you judge whether the matter is already signed or undertaken, and whether its scale is large enough for a separate '
          'thesis: what did you compare it with? Which two statements of the request argued against opening it, and why did you set '
          'them aside? At most 200 words.')
NOT_OPENED = ('In your answer you proposed no thesis for the statement "{subject}". Which instruction in this request led you not to '
              'open one? Quote it. How did you judge whether the matter is already signed or undertaken, and whether its scale is large '
              'enough for a separate thesis: what did you compare it with? Which two statements of the request argued for opening it, '
              'and why did you set them aside? At most 200 words.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('records', nargs='+'); parser.add_argument('--asks', required=True); parser.add_argument('--output', required=True)
    parser.add_argument('--send', action='store_true')
    args = parser.parse_args()
    records = [r for path in args.records for r in json.loads(Path(path).read_text()) if 'answer' in r]
    cases = {c['case']: c for c in json.loads((HERE / 'cases-c9.json').read_text())}
    jobs = []
    for ask in json.loads(Path(args.asks).read_text()):
        record = next(r for r in records if (r['case'], r['arm'], r['draw']) == (ask['case'], ask['arm'], ask['draw']))
        system, user, schema, _ = probe_unfiled.build(cases[ask['case']], ask['arm'])
        if 'thesis' in ask:
            subject = next(t['description'] for t in record['answer']['new_theses'] if t['local_id'] == ask['thesis'])
            question = OPENED.format(subject=subject)
        else:
            subject = next(e['summary'] for e in record['answer']['evidence'] if ask['statement'] in e['summary'])
            question = NOT_OPENED.format(subject=subject)
        request = {'model': probe_unfiled.SETTING.model, 'max_tokens': 8000, 'reasoning_effort': probe_unfiled.SETTING.reasoning_effort,
                   'messages': [{'role': 'system', 'content': system + '\n\nReturn only one JSON object that conforms to this JSON Schema:\n' + json.dumps(schema)},
                                {'role': 'user', 'content': user},
                                {'role': 'assistant', 'content': json.dumps(record['answer'], ensure_ascii=False)},
                                {'role': 'user', 'content': question}]}
        jobs.append((ask, request))
    price_in, price_out = model.PRICES[probe_unfiled.SETTING.model]
    chars = sum(len(json.dumps(j[1])) for j in jobs)
    print(f'{len(jobs)} questions; about {chars // 4} input tokens; about ${chars / 4 / 1e6 * price_in + len(jobs) * 3000 / 1e6 * price_out:.3f}')
    if not args.send:
        return
    def ask_one(job):
        ask, request = job
        try:
            response = model.openai_transport('deepseek', request)
        except Exception as error:   # recorded with its reason, never retried silently
            return {**ask, 'error': f'{type(error).__name__}: {error}'}
        usage = response.get('usage') or {}
        return {**ask, 'reply': response['choices'][0]['message']['content'], 'input_tokens': usage.get('prompt_tokens'),
                'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask_one, jobs))
    Path(args.output).write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    tokens_in = sum(r.get('input_tokens') or 0 for r in replies); tokens_out = sum(r.get('output_tokens') or 0 for r in replies)
    print(f'{len(replies)} replies, {sum("error" in r for r in replies)} errors; ${tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out:.3f}')


if __name__ == '__main__':
    main()
