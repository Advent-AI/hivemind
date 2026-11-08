"""The model's own account of a choice (AGENTS §1): continue a stored Step 1 conversation with the stored answer as the assistant turn
and one question, then record the free-text reply. The question names the thesis, so it can lead the answer; it locates the reason,
it does not show a fix.

Usage: model_account.py <trace.sqlite> <output.json> <sequence> [<sequence> ...]"""
import concurrent.futures, json, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

QUESTION = ('For the new thesis you proposed, "{thesis}": which instruction in this request led you to open it as a new thesis rather '
            'than link its evidence to an open thesis or leave the statement out? Quote the instruction. Then say whether this matter, by '
            'its own scale, can change the company\'s revenue, profit, cash or credit risk, and what an experienced analyst covering the '
            'company would have done with this article. Answer in at most 150 words.')


def main():
    trace, out, sequences = sys.argv[1], Path(sys.argv[2]), [int(x) for x in sys.argv[3:]]
    conn = sqlite3.connect(f'file:{trace}?mode=ro', uri=True)
    jobs = []
    for sequence in sequences:
        request, result = conn.execute('select request, result from trace where sequence=?', (sequence,)).fetchone()
        request, result = json.loads(request), json.loads(result)
        answer = {k: result[k] for k in ('new_theses', 'evidence')}
        for ev in answer['evidence']:
            for key in ('verified_source_passages', 'source_passages_repaired'):
                ev.pop(key, None)
        for thesis in result['new_theses']:
            follow = dict(request, messages=request['messages'] + [
                {'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)},
                {'role': 'user', 'content': QUESTION.format(thesis=thesis['description'])}])
            follow.pop('response_format', None)
            jobs.append((sequence, thesis['description'], follow))
    def ask(job):
        sequence, thesis, follow = job
        response = model.openai_transport('openai', follow)
        usage = response.get('usage') or {}
        return {'sequence': sequence, 'thesis': thesis, 'reply': response['choices'][0]['message']['content'],
                'input_tokens': usage.get('prompt_tokens'), 'output_tokens': usage.get('completion_tokens')}
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        replies = list(pool.map(ask, jobs))
    out.write_text(json.dumps(replies, ensure_ascii=False, indent=1))
    tokens_in = sum(r['input_tokens'] or 0 for r in replies); tokens_out = sum(r['output_tokens'] or 0 for r in replies)
    print(f'{len(replies)} replies; tokens {tokens_in} in, {tokens_out} out; ${tokens_in / 1e6 * 0.10 + tokens_out / 1e6 * 0.50:.4f} at published rates')


if __name__ == '__main__':
    main()
