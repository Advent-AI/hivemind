"""The model's own account of chosen links (AGENTS §1): continue the stored DeepSeek conversation exactly as sent (system text with
the schema, the user item, the stored answer as the assistant turn) and ask one question per link, in free text. The question is the
same for every link and carries no verdict. It locates a reason; it does not prove a fix.

Usage: link_account.py <trace.sqlite> <links.json> <output.json> [--dry-run]
links.json: [{"label": "...", "sequence": 9, "item": "e3", "thesis": "clean-1"}]"""
import concurrent.futures, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

QUESTION = ('In your answer you linked this statement: "{summary}" to the thesis "{question}". Which instruction in this request led '
            'you to link it to that thesis? Quote the instruction. Then say whether this statement would change an experienced '
            "analyst's view of that thesis's answer, and how; if it would not, say what made you link it anyway. Answer in at most 150 "
            'words.')


def main():
    trace, links, out = sys.argv[1], json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    rows = {seq: (raw, result, after) for seq, raw, result, after in
            conn.execute("select sequence, raw_response, result, after_state from trace where status='complete'")}
    jobs = []
    for link in links:
        raw, result, after = rows[link['sequence']]
        raw, answer = json.loads(raw), json.loads(result)
        questions = {t['id']: t['description'] for t in json.loads(after)}
        item = next(ev for ev in answer['evidence'] if ev['local_id'] == link['item'])
        sent = raw['sent_request']
        follow = {k: v for k, v in sent.items() if k != 'response_format'}
        follow['messages'] = sent['messages'] + [
            {'role': 'assistant', 'content': raw['choices'][0]['message']['content']},
            {'role': 'user', 'content': QUESTION.format(summary=item['summary'], question=questions[link['thesis']])}]
        follow['max_tokens'] = 4000
        follow.pop('max_completion_tokens', None)
        jobs.append((link, follow))
    chars = sum(len(json.dumps(j[1])) for j in jobs)
    price = model.PRICES['deepseek-flash']
    print(f'{len(jobs)} questions; about {chars // 4} input tokens; about '
          f'${chars / 4 / 1e6 * price[0] + len(jobs) * 1500 / 1e6 * price[1]:.3f} at published rates')
    if '--dry-run' in sys.argv:
        return
    def ask(job):
        link, follow = job
        try:
            response = model.openai_transport('deepseek', follow)
        except Exception as error:   # recorded with its reason, never retried silently
            return {**link, 'error': f'{type(error).__name__}: {error}'}
        usage = response.get('usage') or {}
        return {**link, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask, jobs))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    tokens_in = sum(r.get('input_tokens') or 0 for r in replies)
    tokens_out = sum(r.get('output_tokens') or 0 for r in replies)
    print(f'{len(replies)} replies, {sum("error" in r for r in replies)} errors; tokens {tokens_in} in, {tokens_out} out; '
          f'${tokens_in / 1e6 * price[0] + tokens_out / 1e6 * price[1]:.3f} at published rates')


if __name__ == '__main__':
    main()
