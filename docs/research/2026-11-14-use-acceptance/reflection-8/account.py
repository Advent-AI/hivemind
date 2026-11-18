"""The model's own account of three stored astra declines (deep council round 2, AGENTS §1): each stored conversation is continued with one
neutral question, in prose (the answer schema dropped), at the request's own model and effort, with a 4,000-token output cap. The account
is a lead about the cause, checked against the request and the refusal before any draft (round 2's correction).

  python3 account.py <out file>
"""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import model  # noqa: E402

QUESTION = ("You declined to write a question. Quote exactly the instruction in your request that led you to decline. Then name the two "
            "other choices you considered and rejected, and say why you rejected each.")
CASES = [  # (label, archive, outcomes, case name)
    ('astra-frozen acc/clean-9 pass 1', 'poc/data/clean-ladder-stage-a-astra-2026-11-17/run-1/send-1', 'acc/clean-9'),
    ('astra-frozen acc/clean-8 pass 1', 'poc/data/clean-ladder-stage-a-astra-2026-11-17/run-1/send-1', 'acc/clean-8'),
    ('astra-edited pool-17 d1', 'poc/data/clean-second-side-probe-2026-11-17/run-1/edited-d1', 'edited-d1|pool-17'),
]
OUTPUT_CAP = 4000


def stored(folder, case_name):
    row = next(json.loads(line) for line in (ROOT / folder / 'outcomes.jsonl').read_text().splitlines() if json.loads(line)['case'] == case_name)
    if row['status'] != 'no ladder':
        raise SystemExit(f'{case_name}: the stored outcome is {row["status"]}, not a decline')
    first = row['requests'][0]
    con = sqlite3.connect(f"file:{ROOT / folder / 'archive.sqlite'}?mode=ro", uri=True)
    found = con.execute('select request_json from model_calls where request_sha256 = ?', (first['request_sha256'],)).fetchone()
    if not found:
        raise SystemExit(f'{case_name}: the stored request is not in the archive')
    return json.loads(found[0]), first['answer_text'], row['reason']


def continued(request, answer_text):
    out = {key: value for key, value in request.items() if key != 'response_format'}
    out['messages'] = request['messages'] + [{'role': 'assistant', 'content': answer_text}, {'role': 'user', 'content': QUESTION}]
    out['max_completion_tokens'] = OUTPUT_CAP
    return out


def main(out_path):
    results, spent = [], 0.0
    for label, folder, case_name in CASES:
        request, answer_text, reason = stored(folder, case_name)
        follow = continued(request, answer_text)
        response = model.openai_transport('openai', follow, max_attempts=1)
        usage = response.get('usage') or {}
        rate_in, rate_out = model.PRICES[follow['model']]
        cached = (usage.get('prompt_tokens_details') or {}).get('cached_tokens') or 0
        cost = ((usage.get('prompt_tokens', 0) - cached) * rate_in + cached * rate_in * model.CACHED_INPUT_SHARE
                + usage.get('completion_tokens', 0) * rate_out) / 1e6
        spent += cost
        results.append({'label': label, 'model': follow['model'], 'effort': follow.get('reasoning_effort'), 'stored_reason': reason,
                        'account': response['choices'][0]['message']['content'], 'usage': usage, 'cost_usd': round(cost, 4)})
        print(f'{label}: ${cost:.4f}', flush=True)
    Path(out_path).write_text(json.dumps(results, indent=1, ensure_ascii=False) + '\n')
    print(f'spent ${spent:.4f}')


if __name__ == '__main__':
    main(sys.argv[1])
