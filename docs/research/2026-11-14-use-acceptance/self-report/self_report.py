"""The self-report diagnostic (council rounds 13 and 14, under D439): on the matched cases of `cases.json` (Stage B figure answers the
readers settled as resting on too little or unsupported, and answers both first readers passed on the same question paths), the
frozen judge is asked one fixed closed question about what sized the band it chose. Rebuild, identity check, follow-up, transport,
one attempt, pricing and records as `unsupported/judge_account.py` (D519), which this copies; only the cases and the question differ.

  python3 self_report.py <output folder>                    (dry: rebuilds, checks, prints, sends nothing)
  python3 self_report.py <output folder> --send --max-usd <ceiling>
"""

import concurrent.futures
import json
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import config, model  # noqa: E402
from hivemind.views import judging  # noqa: E402

QUESTION = ('In the answer you just gave, what places the amount in the band you chose? Begin your reply with a first line of exactly '
            '"LETTER: " and one letter, then one sentence naming the evidence ids or the assumption. A: a figure stated in the evidence shown '
            'places it in that band. B: a calculation that uses only figures stated in the evidence shown places it there. C: an assumption or '
            'estimate of your own, which the evidence shown does not state, decides the band, including a calculation in which such an '
            'assumption decides the band. D: nothing in the evidence shown sizes the amount. E: mixed, or you cannot tell.')
DATA = ROOT / 'poc/data'
CASES = [{'case': c['case'], 'kind': c['group'], 'source': f"Stage B, run {c['draw']}, question {c['view']}, {c['day']} ({c['verdict']})",
          'folder': DATA / f"clean-stage-b-2026-11-11/draw-{c['draw']}", 'where': ('judgement_id', c['judgement_id'])}
         for c in json.loads((Path(__file__).resolve().parent / 'cases.json').read_text())]


def store_of(folder):
    """The views store and the archive of one run folder (the Stage B draws keep theirs one level down)."""
    for candidate in (folder, *sorted(p for p in folder.iterdir() if p.is_dir())):
        if (candidate / 'views.sqlite').exists() and (candidate / 'archive.sqlite').exists():
            return candidate
    raise SystemExit(f'no views.sqlite with archive.sqlite under {folder}: refused')


def main():
    output = Path(sys.argv[1])
    max_usd = float(sys.argv[sys.argv.index('--max-usd') + 1]) if '--max-usd' in sys.argv else 0.0
    cfg = config.load(str(ROOT / 'poc/config/poc-v108.json'))
    setting, schema = cfg.rejudging, judging.schema_for(cfg.rejudging.prompt_version)
    price_in, price_out = model.PRICES[setting.model]
    prepared, worst = [], 0.0
    for case in CASES:
        folder = store_of(case['folder'])
        views = sqlite3.connect(f"file:{folder / 'views.sqlite'}?mode=ro", uri=True)
        archive = sqlite3.connect(f"file:{folder / 'archive.sqlite'}?mode=ro", uri=True)
        column, value = case['where']
        row = views.execute(f'select view_id, seq, publication_day, rung, request_sha256, call_id, judgement_id from judgements where {column} = ?', (value,)).fetchall()
        if len(row) != 1:
            raise SystemExit(f"{case['case']}: {len(row)} judgements with {column} {value}: refused")
        view_id, seq, day, rung, sha, call_id, judgement_id = row[0]
        stored = archive.execute('select request_json, answer_json from model_calls where request_sha256 = ?', (sha,)).fetchall()
        if len(stored) != 1:
            raise SystemExit(f"{case['case']}: {len(stored)} archived calls with the judgement's request key: refused")
        request, answer = json.loads(stored[0][0]), json.loads(stored[0][1])
        system = next(m['content'] for m in request['messages'] if m['role'] == 'system')
        user = next(m['content'] for m in request['messages'] if m['role'] == 'user')
        rebuilt = model.build_request(setting, system, user, schema, 'judgement', cfg.provider)
        if model.request_identity(rebuilt)[1] != sha:
            raise SystemExit(f"{case['case']}: the rebuilt request is not the stored one: refused")
        if system != (ROOT / 'src/hivemind/prompts/judging-v7.txt').read_text().strip() and system.strip() != (ROOT / 'src/hivemind/prompts/judging-v7.txt').read_text().strip():
            raise SystemExit(f"{case['case']}: the stored system text is not the frozen judge's instructions: refused")
        if answer.get('rung') != rung:
            raise SystemExit(f"{case['case']}: the archived answer's band {answer.get('rung')} is not the stored judgement's {rung}: refused")
        follow = dict(rebuilt, messages=rebuilt['messages'] + [{'role': 'assistant', 'content': json.dumps(answer, ensure_ascii=False)},
                                                               {'role': 'user', 'content': QUESTION}])
        follow.pop('response_format')
        characters = sum(len(m['content']) for m in follow['messages'])
        stored_input_tokens = archive.execute('select input_tokens from model_calls where request_sha256 = ?', (sha,)).fetchone()[0]
        added = follow['messages'][len(rebuilt['messages']):]
        added_tokens = sum(len(m['content'].encode('utf-8')) + 50 for m in added)   # a token holds at least one byte; 50 for each message's framing
        bound = (stored_input_tokens + added_tokens) / 1e6 * price_in + setting.max_output_tokens / 1e6 * price_out
        worst += bound
        question = views.execute('select question from views where view_id = ?', (view_id,)).fetchone()[0]
        prepared.append({'case': case['case'], 'kind': case['kind'], 'source': case['source'], 'view': view_id, 'day': day, 'judgement_id': judgement_id,
                         'call_id': call_id, 'stored_request_sha256': sha, 'stored_band': rung, 'question': question,
                         'stored_answer': answer, 'follow_up': follow, 'bound_usd': round(bound, 6)})
        print(f"{case['case']}: {case['source']}\n   {view_id} on {day}, band {rung}; the rebuild has the stored key {sha[:16]}; follow-up {characters} characters")
    print(f"\nmodel {setting.model}, effort {setting.reasoning_effort}, output allowance {setting.max_output_tokens}; {len(prepared)} calls, one HTTP attempt each; "
          f"bound (the original call's recorded input tokens, the added messages at one token a byte plus 50 each, the whole output allowance, no cache discount): ${worst:.3f}\nthe question: {QUESTION}")
    if '--send' not in sys.argv:
        print('dry: nothing sent')
        return
    if worst > max_usd:
        raise SystemExit(f'the worst case ${worst:.3f} is above the ceiling ${max_usd}: refused')
    if output.exists():
        raise SystemExit(f'{output} exists: refusing to write over it')
    output.mkdir(parents=True)
    (output / 'requests.json').write_text(json.dumps(prepared, ensure_ascii=False, indent=1))

    def send(item):
        started = time.time()
        record = {key: item[key] for key in ('case', 'kind', 'source', 'view', 'day', 'call_id', 'stored_request_sha256', 'stored_band', 'question')}
        try:
            reply = model.openai_transport(cfg.provider, item['follow_up'], max_attempts=1)
        except Exception as error:  # a transport failure is a recorded attempt, not a lost one
            record.update(error=repr(error)[:400], seconds=round(time.time() - started, 1), usd_at_published_rates=item['bound_usd'], cost_basis='bound: no usage returned')
            (output / f"reply-{item['case']}.json").write_text(json.dumps(record, indent=1))
            return record
        (output / f"reply-{item['case']}.json").write_text(json.dumps(reply, ensure_ascii=False, indent=1))
        usage = reply.get('usage') or {}
        tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
        cached = min(tokens_in, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
        complete = all(isinstance(usage.get(name), int) for name in ('prompt_tokens', 'completion_tokens'))
        if complete and tokens_out > setting.max_output_tokens:
            record['bound_breach'] = f'{tokens_out} output tokens above the allowance'
        cost = item['bound_usd'] if not complete else (tokens_in - cached) / 1e6 * price_in + cached / 1e6 * price_in * model.CACHED_INPUT_SHARE + tokens_out / 1e6 * price_out
        try:
            account = reply['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError) as error:
            account, record['error'] = None, f'malformed reply: {error!r}'
        record.update(account=account, input_tokens=tokens_in, cached_tokens=cached, output_tokens=tokens_out,
                      usd_at_published_rates=round(cost, 6), seconds=round(time.time() - started, 1))
        return record

    records = []
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        for start in range(0, len(prepared), 8):
            batch = prepared[start:start + 8]
            records += [future.result() for future in [pool.submit(send, item) for item in batch]]
            spent_so_far = sum(record.get('usd_at_published_rates') or 0 for record in records)
            if any(record.get('bound_breach') for record in records) or any((r.get('usd_at_published_rates') or 0) > item['bound_usd'] + 1e-9
                                                                            for r, item in zip(records, prepared)):
                print('a call cost more than its bound: stopped before the next batch')
                break
            if spent_so_far + sum(item['bound_usd'] for item in prepared[start + 8:]) > max_usd:
                print(f'spent ${spent_so_far:.4f}; the remaining bounds would pass the ceiling: stopped before the next batch')
                break
    (output / 'accounts.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    spent = sum(record.get('usd_at_published_rates') or 0 for record in records)
    (output / 'spend.json').write_text(json.dumps({'calls': len(records), 'usd_at_published_rates': round(spent, 6), 'ceiling_usd': max_usd,
                                                   'rates_per_million': {'input': price_in, 'output': price_out, 'cached_input_share': model.CACHED_INPUT_SHARE}}, indent=1))
    print(f"sent {len(records)} calls; accounts returned {sum(1 for r in records if r.get('account'))}; ${spent:.4f} at the published rates")


if __name__ == '__main__':
    main()
