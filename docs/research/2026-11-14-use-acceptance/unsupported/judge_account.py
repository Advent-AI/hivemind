"""The frozen judge's own account of four stored answers (D519, under D439; AGENTS §1, "the model's own account").

For each case the stored judging request is rebuilt by `model.build_request` with the frozen judge's own setting and schema and refused
unless the rebuild has the stored archive key. The conversation is then continued: the stored answer is given back as the judge's turn
(its stored JSON, serialised again: the original bytes and the model's hidden reasoning are not stored), and one neutral question is
asked. The follow-up keeps the model, the reasoning effort and the output allowance, and drops only the answer form. One HTTP attempt a
call; every reply is written down before anything is read from it; cost at the published rates. Nothing is written to any run.

  python3 judge_account.py <output folder>                    (dry: rebuilds, checks, prints, sends nothing)
  python3 judge_account.py <output folder> --send --max-usd 0.10
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

QUESTION = 'Which instruction and which supplied evidence led to your selected band? Identify the calculation and any assumptions you used.'
DATA = ROOT / 'poc/data'
CASES = [
    {'case': 'N-credit-support', 'kind': 'N', 'source': 'baseline, run d1, question v9, first answer (2026-07-01)',
     'folder': DATA / 'clean-unseeded-2026-11-10/draw-d1/judged', 'where': ('judgement_id', 2)},
    {'case': 'N-memory-capacity', 'kind': 'N', 'source': 'Stage B, run u3, question v10, first answer (2026-07-10)',
     'folder': DATA / 'clean-stage-b-2026-11-11/draw-u3', 'where': ('judgement_id', 39)},
    {'case': 'B-one-fifth-discount', 'kind': 'B', 'source': 'trial, old system run p1, question v1, last answer (call 801)',
     'folder': DATA / 'clean-e2e-full-2026-11-13/p1/prod', 'where': ('call_id', 801)},
    {'case': 'B-fourth-quarter-growth', 'kind': 'B', 'source': 'fresh week, old system run p1, question v4, last answer (call 715)',
     'folder': DATA / 'clean-lean-week-2026-11-14/week/p1/prod', 'where': ('call_id', 715)},
]


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
        worst += characters / 2.5 / 1e6 * price_in + setting.max_output_tokens / 1e6 * price_out
        question = views.execute('select question from views where view_id = ?', (view_id,)).fetchone()[0]
        prepared.append({'case': case['case'], 'kind': case['kind'], 'source': case['source'], 'view': view_id, 'day': day, 'judgement_id': judgement_id,
                         'call_id': call_id, 'stored_request_sha256': sha, 'stored_band': rung, 'question': question,
                         'stored_answer': answer, 'follow_up': follow})
        print(f"{case['case']}: {case['source']}\n   {view_id} on {day}, band {rung}; the rebuild has the stored key {sha[:16]}; follow-up {characters} characters\n   question: {question[:170]}\n"
              f"   stored implied outcome: {str(answer.get('implied_outcome'))[:300]}")
    print(f"\nmodel {setting.model}, effort {setting.reasoning_effort}, output allowance {setting.max_output_tokens}; {len(prepared)} calls, one HTTP attempt each; "
          f"cost if every call used its whole output allowance: ${worst:.3f}\nthe question: {QUESTION}")
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
            record.update(error=repr(error)[:400], seconds=round(time.time() - started, 1), usd_at_published_rates=0.0)
            (output / f"reply-{item['case']}.json").write_text(json.dumps(record, indent=1))
            return record
        (output / f"reply-{item['case']}.json").write_text(json.dumps(reply, ensure_ascii=False, indent=1))
        usage = reply.get('usage') or {}
        tokens_in, tokens_out = int(usage.get('prompt_tokens') or 0), int(usage.get('completion_tokens') or 0)
        cached = min(tokens_in, int((usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0))
        cost = (tokens_in - cached) / 1e6 * price_in + cached / 1e6 * price_in * model.CACHED_INPUT_SHARE + tokens_out / 1e6 * price_out
        try:
            account = reply['choices'][0]['message']['content']
        except (KeyError, IndexError, TypeError) as error:
            account, record['error'] = None, f'malformed reply: {error!r}'
        record.update(account=account, input_tokens=tokens_in, cached_tokens=cached, output_tokens=tokens_out,
                      usd_at_published_rates=round(cost, 6), seconds=round(time.time() - started, 1))
        return record

    with concurrent.futures.ThreadPoolExecutor(len(prepared)) as pool:
        records = [future.result() for future in [pool.submit(send, item) for item in prepared]]
    (output / 'accounts.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))
    spent = sum(record.get('usd_at_published_rates') or 0 for record in records)
    (output / 'spend.json').write_text(json.dumps({'calls': len(records), 'usd_at_published_rates': round(spent, 6), 'ceiling_usd': max_usd,
                                                   'rates_per_million': {'input': price_in, 'output': price_out, 'cached_input_share': model.CACHED_INPUT_SHARE}}, indent=1))
    print(f"sent {len(records)} calls; accounts returned {sum(1 for r in records if r.get('account'))}; ${spent:.4f} at the published rates")


if __name__ == '__main__':
    main()
