"""The effect of one missing fact on one stored judgement (EFFECT-TEST-DESIGN.md; D508, D509). After the reviewed method of
`docs/research/2026-11-04-filing-end-to-end/one_test.py`.

The stored last judging request of one question of the new system's fresh-week run is rebuilt by `model.build_request` with the frozen
judge's own setting and schema, and refused unless the rebuild has the stored archive key. The treatment is that request with one
stored statement inserted at the head of its evidence block, formatted by the production code (`judging._lines_english`), and the
block's item count raised by one; nothing else differs. Each condition is sent `--sends` times, at once, straight through the model
module's transport, one HTTP attempt at a time and at most two for a call; every attempt is written down before anything is parsed
(the raw reply, or the error), with its token usage and its cost at the published rates. An answer counts only when it passes the
judge's schema and the judge's own check of the answer against the request that was sent (`judging.check_answer`).

  python3 effect_test.py <run folder of the clean draw> <output folder> --view v7 --add e379 --from-view v3            (dry: builds, checks, prints, sends nothing)
  python3 effect_test.py <run folder of the clean draw> <output folder> --view v7 --add e379 --from-view v3 --send --max-usd 0.25
"""
import concurrent.futures
import json
import re
import sqlite3
import sys
import time
from pathlib import Path

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src']
from hivemind import config, model  # noqa: E402
from hivemind.views import judging, store  # noqa: E402


def option(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    run, output = Path(sys.argv[1]), Path(sys.argv[2])
    view_id, add_id, from_view = option('--view'), option('--add'), option('--from-view')
    sends, max_usd = int(option('--sends', '3')), float(option('--max-usd', '0'))
    cfg = config.load(f'{ROOT}/poc/config/poc-v108.json')
    setting, schema = cfg.rejudging, judging.schema_for(cfg.rejudging.prompt_version)
    views = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f"file:{run / 'judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    sha, stored_rung = views.execute('select request_sha256, rung from judgements where view_id = ? order by seq desc limit 1', (view_id,)).fetchone()
    stored = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])
    system = next(m['content'] for m in stored['messages'] if m['role'] == 'system')
    user = next(m['content'] for m in stored['messages'] if m['role'] == 'user')
    control = model.build_request(setting, system, user, schema, 'judgement', cfg.provider)
    if model.request_identity(control)[1] != sha:
        raise SystemExit('the rebuilt request is not the stored one: refusing')
    if re.search(rf'^- {add_id} \[', user, re.M):
        raise SystemExit(f'{add_id} is already in the stored request of {view_id}: nothing to test')
    piece = next((p for p in store.evidence_in_force(views, from_view) if p['evidence_id'] == add_id), None)
    if piece is None:
        raise SystemExit(f'{add_id} is not in force under {from_view}: refusing')
    built = judging._lines_english(views, view_id, store.view(views, view_id), store.rungs_of(views, view_id), [piece], [], None)
    start = next(i for i, line in enumerate(built) if line.startswith('[Evidence in view under this thesis')) + 1
    block = []
    for line in built[start:]:
        if line.startswith('\n['):
            break
        block.append(line)
    block_text = '\n'.join(block)
    other_sha = views.execute('select request_sha256 from judgements where view_id = ? order by seq desc limit 1', (from_view,)).fetchone()[0]
    other_user = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (other_sha,)).fetchone()[0])['messages'][1]['content']
    if block_text not in other_user:
        raise SystemExit(f"the block built for {add_id} is not the text the judge saw under {from_view}: refusing")
    header = re.search(r'\[Evidence in view under this thesis, (\d+) items\]', user)
    with_fact = user.replace(header.group(0), f'[Evidence in view under this thesis, {int(header.group(1)) + 1} items]\n{block_text}', 1)
    removed = with_fact.replace(block_text + '\n', '', 1).replace(f'{int(header.group(1)) + 1} items]', f'{header.group(1)} items]', 1)
    if removed != user:
        raise SystemExit('taking the inserted block and the count back out does not give the stored text: refusing')
    treatment = model.build_request(setting, system, with_fact, schema, 'judgement', cfg.provider)
    price_in, price_out = model.PRICES[setting.model]
    attempts_allowed = 2
    worst = attempts_allowed * 2 * sends * ((len(system) + len(with_fact)) / 2.5 / 1e6 * price_in + setting.max_output_tokens / 1e6 * price_out)
    print(f'question {view_id}: stored answer {stored_rung}; the control rebuild has the stored key {sha[:16]}; items {header.group(1)} -> {int(header.group(1)) + 1}')
    print(f'inserted block ({len(block_text)} characters; the same text the judge saw under {from_view}):\n{block_text}')
    print(f'model {setting.model}, effort {setting.reasoning_effort}; {2 * sends} calls, at most {attempts_allowed} HTTP attempts each; '
          f'cost if every attempt were charged its whole output allowance: ${worst:.3f}')
    if '--send' not in sys.argv:
        print('dry: nothing sent')
        return
    if worst > max_usd:
        raise SystemExit(f'the worst case ${worst:.3f} is above the ceiling ${max_usd}: refusing')
    if output.exists():
        raise SystemExit(f'{output} exists: refusing to write over it')
    output.mkdir(parents=True)
    (output / 'requests.json').write_text(json.dumps({'control': control, 'with_fact': treatment, 'stored_key': sha, 'added': add_id, 'block': block_text}, ensure_ascii=False, indent=1))
    jobs = [(condition, number, request, with_fact if condition == 'with_fact' else user)
            for condition, request in (('control', control), ('with_fact', treatment)) for number in range(1, sends + 1)]

    def send(job):
        """One call: up to two HTTP attempts, each written to disk before anything is parsed."""
        condition, number, request, request_text = job
        record = {'condition': condition, 'send': number, 'attempts': [], 'answer': None, 'valid': False, 'errors': []}
        for attempt in range(1, attempts_allowed + 1):
            started = time.time()
            try:
                reply = model.openai_transport(cfg.provider, request, max_attempts=1)
            except Exception as error:  # a transport failure is a recorded attempt, not a lost one
                record['attempts'].append({'attempt': attempt, 'error': repr(error)[:400], 'seconds': round(time.time() - started, 1)})
                (output / f'attempt-{condition}-{number}-{attempt}.json').write_text(json.dumps(record['attempts'][-1], indent=1))
                continue
            (output / f'attempt-{condition}-{number}-{attempt}.json').write_text(json.dumps(reply, ensure_ascii=False, indent=1))
            usage = reply.get('usage') or {}
            tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
            cached = min(tokens_in, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
            cost = (tokens_in - cached) / 1e6 * price_in + cached / 1e6 * price_in * model.CACHED_INPUT_SHARE + tokens_out / 1e6 * price_out
            record['attempts'].append({'attempt': attempt, 'input_tokens': tokens_in, 'cached_tokens': cached, 'output_tokens': tokens_out,
                                       'usd_at_published_rates': round(cost, 6), 'seconds': round(time.time() - started, 1)})
            try:
                data = json.loads(reply['choices'][0]['message']['content'])
            except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
                record['errors'].append(f'attempt {attempt}: malformed reply: {error!r}'[:300])
                continue
            errors = model.check_schema(data, schema)
            if not errors:
                check = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
                check.row_factory = sqlite3.Row
                errors = judging.check_answer(check, view_id, data, request_text)
            record['answer'], record['errors'], record['valid'] = data, record['errors'] + [f'attempt {attempt}: {e}' for e in errors], not errors
            break
        return record

    with concurrent.futures.ThreadPoolExecutor(len(jobs)) as pool:
        answers = [future.result() for future in [pool.submit(send, job) for job in jobs]]
    spent = sum(a.get('usd_at_published_rates', 0.0) for record in answers for a in record['attempts'])
    (output / 'answers.json').write_text(json.dumps(answers, ensure_ascii=False, indent=1))
    (output / 'spend.json').write_text(json.dumps({'calls': len(answers), 'http_attempts': sum(len(r['attempts']) for r in answers),
                                                   'usd_at_published_rates': round(spent, 6), 'ceiling_usd': max_usd}, indent=1))
    for record in sorted(answers, key=lambda r: (r['condition'], r['send'])):
        answer = record['answer'] or {}
        print(f"{record['condition']} {record['send']}: valid {record['valid']}; answer {answer.get('rung')}; cites {answer.get('cites')}; attempts {len(record['attempts'])}; "
              f"errors {record['errors']}; ${sum(a.get('usd_at_published_rates', 0.0) for a in record['attempts']):.4f}")
    print(f"{len(answers)} calls, {sum(len(r['attempts']) for r in answers)} HTTP attempts, ${spent:.4f} at the published rates (ceiling ${max_usd})")


if __name__ == '__main__':
    main()
