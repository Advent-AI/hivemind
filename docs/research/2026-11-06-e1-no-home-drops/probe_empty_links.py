"""E1, the extraction model's own account of an empty filing (AGENTS §1), about $0.002 a send. The stored production extraction conversation
(poc-v108 control draw) is continued as stored: system, user, the stored answer as the assistant's turn, then one question quoting the links
field's own description from that request's schema. Each case is sent twice; one answer is one draw."""
import json, sqlite3, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, '/Users/lchingen/hivemind/src')
from hivemind import config, model  # noqa: E402

BENCH = Path('/Users/lchingen/hivemind-no-preseed-evidence-review/docs/research/2026-11-06-architecture-benchmark')
HERE = Path(__file__).resolve().parent
CASES = [  # (packet case, set, draw, statement id, questions to ask about)
    (9, 'window', 'd1', 'e4', 'v11'), (18, 'window', 'd2', 'e6', 'v11'), (39, 'test', 'd1', 'e5', 'v13 and v4'),
    (2, 'window', 'd2', 'e3', 'v13 and v4'), (5, 'window', 'd2', 'e11', 'v16'), (27, 'window', 'd3', 'e4', 'v1'),
    (54, 'test', 'd2', 'e1', 'v2'), (29, 'window', 'd2', 'e2', 'v18'), (23, 'window', 'd1', 'e3', 'v18'), (17, 'window', 'd2', 'e9', 'v16')]
SENDS = 2


def build(case):
    number, set_name, draw, statement_id, others = case
    folder = BENCH / ('runs/control-v108-' if set_name == 'window' else 'runs/test-control-') / '..' / (('control-v108-' if set_name == 'window' else 'test-control-') + draw)
    packet = json.load(open(HERE / 'packet.json'))[number]
    traces = {m['matter']: m for m in json.load(open(BENCH / f"results/traces-{'window' if set_name == 'window' else 'test'}-control.json"))}
    call_id = traces[packet['matter']]['draws'][draw]['raw']['extract'][0]['call_id']
    archive = sqlite3.connect(f'file:{folder.resolve()}/archive.sqlite?mode=ro', uri=True)
    request_json, answer_json = archive.execute('select request_json, answer_json from model_calls where call_id = ?', (call_id,)).fetchone()
    request, answer = json.loads(request_json), json.loads(answer_json)
    statement = next(e for e in answer['evidence'] if e['id'] == statement_id)
    assert statement['links'] == [] and packet['article']['id'] in request['messages'][-1]['content']
    rule = request['response_format']['json_schema']['schema']['properties']['evidence']['items']['properties']['links']['description']
    question = (f'You wrote the statement {statement_id}, "{statement["one_line"]}", with empty links, so it was filed under no question. '
                f'The links field\'s instruction was: "{rule}" '
                f'Which words of that instruction, or of the question list, led you to leave its links empty? Did you consider {others}, and why '
                f'did you not file it there? Quote the words, and answer in a few short paragraphs.')
    probe = {k: v for k, v in request.items() if k not in ('response_format', 'messages')}
    probe['messages'] = list(request['messages']) + [{'role': 'assistant', 'content': answer_json}, {'role': 'user', 'content': question}]
    return number, statement, others, probe


def main():
    cfg = config.load('/Users/lchingen/hivemind/poc/config/poc-v108.json')
    built = [build(case) for case in CASES]
    jobs = [(b, n) for b in built for n in range(SENDS)]
    with ThreadPoolExecutor(8) as pool:
        answers = list(pool.map(lambda job: model.openai_transport(cfg.provider, job[0][3]), jobs))
    lines, tokens_in, tokens_out = ['# E1: the extraction model\'s account of empty links (poc-v108 control draws)', ''], 0, 0
    for (b, n), response in zip(jobs, answers):
        number, statement, others, _ = b
        usage = response.get('usage', {})
        tokens_in += usage.get('prompt_tokens', 0); tokens_out += usage.get('completion_tokens', 0)
        if n == 0:
            lines += [f'## Case #{number}: "{statement["one_line"]}" (asked about {others})', '']
        lines += [f'### send {n + 1}', '', response['choices'][0]['message']['content'].strip(), '']
    price_in, price_out = model.PRICES[cfg.model] if hasattr(cfg, 'model') else model.PRICES['gpt-6-luna']
    lines += [f'Tokens: {tokens_in} in, {tokens_out} out; at most ${tokens_in / 1e6 * price_in + tokens_out / 1e6 * price_out:.3f} at the published rates, uncached.']
    (HERE / 'model-account.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(lines[-1])


if __name__ == '__main__':
    main()
