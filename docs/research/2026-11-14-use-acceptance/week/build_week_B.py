"""Lean step 2, reading B ($0): every question's last judgement by 2026-09-28 in the week's clean draw and production draw, as the judge request
was sent (its user text) and the answer. Planted wrong judgements are built from **earlier** judgements of the same runs (not last ones), so no
planted request repeats a request in the packet (the trial's flaw, TRIAL-RESULT.md); two rungs moved against the answer's own text, one
yes/no flipped, one reason that adds a fact the request does not hold. Eight real last judgements are offered to a separate reader as
supported-control candidates (`supported-candidates.json`). Shuffled with a fixed seed; the key goes outside the repository.

  python3 build_week_B.py <key folder outside the repository>
"""
import copy
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14')
# the clean draw is the relaunch after D488 (week-r2); production's completed draw is the first root's
ARCHIVES = {'c1': ROOT / 'week-r2/c1/judge/draw-c1/archive.sqlite', 'p1': ROOT / 'week/p1/prod/archive.sqlite'}
VIEW = re.compile(r'^\s*Thesis (v\d+) \(')


def judgements(draw):
    conn = sqlite3.connect(f'file:{ARCHIVES[draw]}?mode=ro', uri=True)
    rows = []
    for call_id, request_json, answer_json in conn.execute(
            "select call_id, request_json, answer_json from model_calls where purpose='judge' and answer_json is not null order by call_id"):
        user = json.loads(request_json)['messages'][-1]['content']
        found = VIEW.match(user)
        if found:
            rows.append({'draw': draw, 'view': found.group(1), 'call_id': call_id, 'request': user, 'answer': json.loads(answer_json)})
    last = {}
    for row in rows:
        last[row['view']] = row
    earlier = [row for row in rows if last[row['view']] is not row]
    return list(last.values()), earlier


def plant(item, kind):
    planted = copy.deepcopy(item)
    answer = planted['answer']
    rungs = re.findall(r'rung (\d) ', item['request'].split('\n', 2)[1]) or ['1', '2']
    top = max(int(r) for r in rungs)
    if kind == 'yes/no flipped':
        answer['rung'] = 2 if answer.get('rung') == 1 else 1
    else:                                   # the end of the ladder farthest from the answer's own rung, so the planted rung is never a neighbour
        answer['rung'] = top if (answer.get('rung') or 1) - 1 < top - (answer.get('rung') or 1) else 1
    if kind == 'fact added':
        answer['reasons'] = (answer.get('reasons') or '') + (' A further filing reported the opposite of what the cited items say, which moves '
                                                             'the answer to the other end of the ladder.')
    planted['planted'] = kind
    return planted


def is_yes_no(item):
    return bool(re.search(r'rung \d (Yes|No|Happened)\b', item['request'].split('\n', 2)[1]))


def main():
    key_folder = Path(sys.argv[1])
    key_folder.mkdir(parents=True, exist_ok=True)
    real, earlier = [], []
    for draw in ARCHIVES:
        last, before = judgements(draw)
        real += last
        earlier += before
    rng = random.Random(20261115)
    figures = [i for i in earlier if not is_yes_no(i)]
    yes_no = [i for i in earlier if is_yes_no(i)]
    bases = rng.sample(figures, 3) + (rng.sample(yes_no, 1) if yes_no else rng.sample(figures, 1))
    planted = [plant(bases[0], 'rung moved'), plant(bases[1], 'rung moved'), plant(bases[2], 'fact added'),
               plant(bases[3], 'yes/no flipped' if yes_no else 'rung moved')]
    requests = [r['request'] for r in real]
    if any(p['request'] in requests for p in planted):
        raise SystemExit('a planted request repeats a real one: refused')
    candidates = rng.sample(real, min(8, len(real)))
    (HERE / 'supported-candidates.json').write_text(json.dumps(
        [{'candidate': n, 'request': c['request'], 'answer': c['answer']} for n, c in enumerate(candidates, 1)], ensure_ascii=False, indent=1))
    rows = real + planted
    order = rng.sample(rows, len(rows))
    (HERE / 'packet-B.json').write_text(json.dumps([{'item': n, 'request': r['request'], 'answer': r['answer']} for n, r in enumerate(order, 1)],
                                                   ensure_ascii=False, indent=1))
    (key_folder / 'week-key-B.json').write_text(json.dumps(
        [{'item': n, 'draw': r['draw'], 'view': r['view'], 'call_id': r['call_id'], 'planted': r.get('planted'),
          'candidate': next((k for k, c in enumerate(candidates, 1) if c is r), None)} for n, r in enumerate(order, 1)], indent=1))
    print(f'real last judgements: c1 {sum(r["draw"] == "c1" for r in real)}, p1 {sum(r["draw"] == "p1" for r in real)}; planted 4 from '
          f'earlier judgements (no request repeated); packet {len(order)}; supported candidates {len(candidates)}')


if __name__ == '__main__':
    main()
