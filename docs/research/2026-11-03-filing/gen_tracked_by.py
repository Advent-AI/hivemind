"""Test 3, step 1: write each open question's "tracked by" line the way the question opener would in production, from the question alone
(no article is shown): the measures an analyst tracks to estimate the answer besides the question's own figure, naming parties by role
and kinds of figures, never a company, product or number. One call for all questions of one stored request. About a cent.

    python3 gen_tracked_by.py <d1 call id> tracked-by.json
"""
import json, re, sqlite3, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import config, model  # noqa: E402

SYSTEM = ("You are a senior hedge-fund analyst setting up research questions. For each question, write one line naming what you would "
          "track to estimate its answer besides the question's own reported or forecast figure: the other parties by role (suppliers, "
          "customers, competitors, regulators, financiers) and the kinds of figures they publish (their revenue from it, orders, backlog, "
          "capacity, shipments, prices, budgets, approvals). Do not name any company, product, person or number, and do not repeat the "
          "question. At most 25 words per line. Return a JSON object mapping each question id to its line.")


def main():
    call_id, out = int(sys.argv[1]), sys.argv[2]
    cfg = config.load(str(ROOT / 'poc/config/poc-v108.json'))
    db = sqlite3.connect(f'file:{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d1/archive.sqlite?mode=ro', uri=True)
    req = json.loads(db.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])
    qs = re.findall(r'^\s*- (v\d+) \(([^)]*)\): ([^\n]+)', req['messages'][1]['content'], re.M)
    listing = '\n'.join(f'{vid} ({obj}): {q}' for vid, obj, q in qs)
    body = {'model': req['model'], 'reasoning_effort': 'low', 'max_completion_tokens': 4000,
            'messages': [{'role': 'system', 'content': SYSTEM}, {'role': 'user', 'content': listing}],
            'response_format': {'type': 'json_object'}}
    lines = json.loads(model.openai_transport(cfg.provider, body, timeout=300)['choices'][0]['message']['content'])
    json.dump(lines, open(out, 'w'), ensure_ascii=False, indent=1)
    for vid, obj, q in qs:
        print(f'{vid} ({obj}) {q[:70]}\n     tracked by: {lines.get(vid, "-")}')


if __name__ == '__main__':
    main()
