"""D485 trial, reading B ($0): every view's last judgement by 2026-07-14 in clean draw c1 and production draw p1, as the judge request was
sent (its user text, which carries the question, the ladder and every piece of evidence shown with its passages, speaker and date) and the
answer (rung, reasons, cites). Four planted wrong judgements are copies of real ones with the answer altered (two rungs moved against the
answer's own text, one yes/no flipped, one reason that adds a fact the request does not hold); controls known to be supported are chosen
afterwards by a separate reader from `supported-candidates.json`. Items are shuffled with a fixed seed; the key goes outside the repository.

  python3 build_B.py <key folder outside the repository>
"""
import copy
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = Path('/Users/lchingen/hivemind/poc/data/clean-e2e-full-2026-11-13')
ARCHIVES = {'c1': FULL / 'c1/judge/draw-c1/archive.sqlite', 'p1': FULL / 'p1/prod/archive.sqlite'}
VIEW = re.compile(r'^\s*Thesis (v\d+) \(')


def last_judgements(draw):
    conn = sqlite3.connect(f'file:{ARCHIVES[draw]}?mode=ro', uri=True)
    last = {}
    for call_id, request_json, answer_json in conn.execute(
            "select call_id, request_json, answer_json from model_calls where purpose='judge' and answer_json is not null order by call_id"):
        user = json.loads(request_json)['messages'][-1]['content']
        found = VIEW.match(user)
        if found:
            last[found.group(1)] = {'draw': draw, 'view': found.group(1), 'call_id': call_id, 'request': user, 'answer': json.loads(answer_json)}
    return list(last.values())


def plant(item, kind):
    planted = copy.deepcopy(item)
    answer = planted['answer']
    rungs = re.findall(r'rung (\d) ', item['request'].split('\n', 2)[1]) or ['1', '2']
    if kind == 'rung moved':
        top = max(int(r) for r in rungs)
        answer['rung'] = 1 if answer.get('rung') != 1 else top
    elif kind == 'yes/no flipped':
        answer['rung'] = 2 if answer.get('rung') == 1 else 1
    elif kind == 'fact added':
        answer['reasons'] = (answer.get('reasons') or '') + (' A further filing reported the opposite of what the cited items say, which '
                                                             'moves the answer to the other end of the ladder.')
        top = max(int(r) for r in rungs)
        answer['rung'] = 1 if answer.get('rung') != 1 else top
    planted['planted'] = kind
    return planted


def main():
    key_folder = Path(sys.argv[1])
    key_folder.mkdir(parents=True, exist_ok=True)
    real = last_judgements('c1') + last_judgements('p1')
    rng = random.Random(20261114)
    yes_no = [i for i in real if 'rung 1 Yes' in i['request'] or ': Yes' in i['request'].split('\n', 2)[1]]
    figures = [i for i in real if i not in yes_no]
    bases = rng.sample(figures, 3) + rng.sample(yes_no, 1) if yes_no else rng.sample(real, 4)
    planted = [plant(bases[0], 'rung moved'), plant(bases[1], 'rung moved'), plant(bases[2], 'fact added'),
               plant(bases[3], 'yes/no flipped' if yes_no else 'rung moved')]
    candidates = rng.sample([i for i in real if i not in bases], 8)
    (HERE / 'supported-candidates.json').write_text(json.dumps(
        [{'candidate': n, 'request': c['request'], 'answer': c['answer']} for n, c in enumerate(candidates, 1)], ensure_ascii=False, indent=1))
    rows = real + planted
    order = rng.sample(rows, len(rows))
    packet = [{'item': n, 'request': r['request'], 'answer': r['answer']} for n, r in enumerate(order, 1)]
    key = [{'item': n, 'draw': r['draw'], 'view': r['view'], 'call_id': r['call_id'], 'planted': r.get('planted'),
            'candidate': next((k for k, c in enumerate(candidates, 1) if c is r), None)} for n, r in enumerate(order, 1)]
    (HERE / 'packet-B.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1))
    (key_folder / 'key-B.json').write_text(json.dumps(key, indent=1))
    sizes = [len(p['request']) for p in packet]
    print(f'real last judgements: c1 {sum(r["draw"] == "c1" for r in real)}, p1 {sum(r["draw"] == "p1" for r in real)}; planted 4; '
          f'packet {len(packet)} items, request characters {sum(sizes)} (largest {max(sizes)}); supported candidates 8')


if __name__ == '__main__':
    main()
