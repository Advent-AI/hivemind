"""The model's own account of an omitted statement (AGENTS §1): continue the stored DeepSeek conversation exactly as sent (system text
with the schema, the user item, the stored answer as the assistant turn) and ask the fixed question: which instruction led to leaving
the quoted source sentence out, and which two statements of the item it rejected. The question carries no verdict. It locates a
reason; it does not prove a fix.

Usage: omission_account.py <cases.json> <output.json> [--send]
cases.json: [{"label": "...", "trace": "<path, or segments joined with '+'>", "input_id": "...", "sentence": "..."}]"""
import concurrent.futures, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

QUESTION = ('The item contains this sentence: "{sentence}" Your answer does not include it. Which instruction in this request led you '
            'to leave it out? Quote the instruction. Then name the two statements of this item you rejected and the instruction behind '
            'each. Answer in at most 200 words.')


def stored(trace, input_id):
    for part in trace.split('+'):
        conn = sqlite3.connect(f'file:{part}?mode=ro', uri=True)
        row = conn.execute("select raw_response from trace where input_id=? and status='complete'", (input_id,)).fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
    raise SystemExit(f'{input_id} has no completed answer in {trace}')


def main():
    cases, out = json.loads(Path(sys.argv[1]).read_text()), Path(sys.argv[2])
    jobs = []
    for case in cases:
        raw = stored(case['trace'], case['input_id'])
        sent = raw['sent_request']
        follow = {k: v for k, v in sent.items() if k != 'response_format'}
        follow['messages'] = sent['messages'] + [
            {'role': 'assistant', 'content': raw['choices'][0]['message']['content']},
            {'role': 'user', 'content': QUESTION.format(sentence=case['sentence'])}]
        follow['max_tokens'] = 4000
        follow.pop('max_completion_tokens', None)
        jobs.append((case, follow))
    chars = sum(len(json.dumps(job[1])) for job in jobs)
    price = model.PRICES['deepseek-flash']
    print(f'{len(jobs)} questions; about {chars // 4} input tokens; about '
          f'${chars / 4 / 1e6 * price[0] + len(jobs) * 1500 / 1e6 * price[1]:.3f} at published rates')
    if '--send' not in sys.argv:
        return
    def ask(job):
        case, follow = job
        try:
            response = model.openai_transport('deepseek', follow)
        except Exception as error:   # recorded with its reason, never retried silently
            return {**case, 'error': f'{type(error).__name__}: {error}'}
        usage = response.get('usage') or {}
        return {**case, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask, jobs))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    tokens_in = sum(r.get('input_tokens') or 0 for r in replies)
    tokens_out = sum(r.get('output_tokens') or 0 for r in replies)
    print(f'{len(replies)} replies, {sum("error" in r for r in replies)} errors; ${tokens_in / 1e6 * price[0] + tokens_out / 1e6 * price[1]:.3f}')


if __name__ == '__main__':
    main()
