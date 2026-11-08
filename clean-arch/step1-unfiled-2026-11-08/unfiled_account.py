"""The model's own account of each unfiled item (AGENTS §1): continue the stored DeepSeek conversation exactly as sent (system text with
the schema, the user item, the stored answer as the assistant turn) and ask one question per unfiled item, in free text. It locates a
reason; it does not prove a fix.

Usage: unfiled_account.py <trace.sqlite> <output.json> [--dry-run]"""
import concurrent.futures, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

QUESTION = ('In your answer you returned this statement with empty links, so it is unfiled and will not be stored: "{summary}". '
            'Which instruction in this request led you to leave it unfiled rather than link it to an open thesis or propose a new thesis? '
            'Quote the instruction. Then name the research question, if any, under which an experienced analyst covering the company would '
            'file this statement, and say whether that question is already open, would be a new thesis, or does not exist because the '
            'statement is not material. Answer in at most 150 words.')


def main():
    trace, out = sys.argv[1], Path(sys.argv[2])
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    jobs = []
    for seq, input_id, raw, result in conn.execute("select sequence, input_id, raw_response, result from trace where status='complete' order by sequence"):
        unfiled = json.loads(result).get('unfiled_evidence', [])
        if not unfiled:
            continue
        raw = json.loads(raw)
        sent = raw['sent_request']
        content = raw['choices'][0]['message']['content']
        for ev in unfiled:
            follow = {k: v for k, v in sent.items() if k != 'response_format'}
            follow['messages'] = sent['messages'] + [{'role': 'assistant', 'content': content},
                                                     {'role': 'user', 'content': QUESTION.format(summary=ev['summary'])}]
            follow['max_tokens'] = 4000
            follow.pop('max_completion_tokens', None)
            jobs.append((seq, input_id, ev['local_id'], ev['summary'], follow))
    chars = sum(len(json.dumps(j[4])) for j in jobs)
    print(f'{len(jobs)} questions; about {chars // 4} input tokens; about ${chars / 4 / 1e6 * model.PRICES["deepseek-flash"][0] + len(jobs) * 1500 / 1e6 * model.PRICES["deepseek-flash"][1]:.3f}')
    if '--dry-run' in sys.argv:
        return
    def ask(job):
        seq, input_id, local_id, summary, follow = job
        try:
            response = model.openai_transport('deepseek', follow)
        except Exception as error:
            return {'sequence': seq, 'input_id': input_id, 'local_id': local_id, 'summary': summary, 'error': f'{type(error).__name__}: {error}'}
        usage = response.get('usage') or {}
        return {'sequence': seq, 'input_id': input_id, 'local_id': local_id, 'summary': summary,
                'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask, jobs))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    ti = sum(r.get('input_tokens') or 0 for r in replies); to = sum(r.get('output_tokens') or 0 for r in replies)
    p = model.PRICES['deepseek-flash']
    print(f'{len(replies)} replies, {sum("error" in r for r in replies)} errors; tokens {ti} in, {to} out; ${ti / 1e6 * p[0] + to / 1e6 * p[1]:.3f} at published rates')


if __name__ == '__main__':
    main()
