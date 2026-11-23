"""The two-week run's reading packets, as PLAN.md froze them ($0). Blind where the reading allows; keys outside the repository.

  python3 build_readings.py openings <run root> <key folder>     # reading 1: week 2's openings, with lost-question and lost-fact controls
  python3 build_readings.py answers <run root> <key folder>      # reading 2: every question's last judgement, planted wrong answers, control candidates

Reading 3 (source to answer) is built from the readers' answers to reading 1 and is not here.
"""
import copy
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WEEK1_ARTICLES = 235
SEED = 20261116
VIEW = re.compile(r'^\s*Thesis (v\d+) \(')


def trace_rows(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    try:
        items = {item['input_id']: item for item in json.loads(conn.execute('select source_items from run').fetchone()[0])}
        rows = [dict(zip(('sequence', 'input_id', 'before', 'after', 'result', 'status'), row)) for row in
                conn.execute('select sequence, input_id, before_state, after_state, result, status from trace order by sequence')]
    finally:
        conn.close()
    return items, rows


def openings(run_root, keys):
    run_root, keys = Path(run_root), Path(keys)
    items, rows = trace_rows(run_root / 'c1/step1/trace.sqlite')
    topics, articles, opened_rows = {}, [], []
    for row in rows:
        if row['status'] != 'complete':
            continue
        before, after = json.loads(row['before']), json.loads(row['after'])
        for topic in after:
            topics.setdefault(topic['id'], {key: topic[key] for key in ('id', 'description', 'outcome', 'period')})
        opened = [t['id'] for t in after if t['id'] not in {b['id'] for b in before}]
        if row['sequence'] > WEEK1_ARTICLES and opened:
            opened_rows.append(row['sequence'])
    week2 = [row for row in rows if row['sequence'] > WEEK1_ARTICLES and row['status'] == 'complete']
    others = [row['sequence'] for row in week2 if row['sequence'] not in opened_rows]
    sample = sorted(random.Random(SEED).sample(others, min(20, len(others))))
    chosen = sorted(opened_rows + sample)
    by_sequence = {row['sequence']: row for row in rows}
    for number, sequence in enumerate(chosen, 1):
        row = by_sequence[sequence]
        before, after, result = json.loads(row['before']), json.loads(row['after']), json.loads(row['result'])
        held = [t['id'] for t in before]
        new = [t['id'] for t in after if t['id'] not in held]
        allocated = result.get('new_thesis_ids') or {}
        statements = []
        for index, evidence in enumerate(result.get('evidence', []), 1):
            homes = [allocated.get(link.get('target_id'), link.get('target_id')) for link in evidence.get('links') or []]
            statements.append({'ref': f'S{index}', 'statement': evidence['summary'], 'filed_under': homes or ['nowhere']})
        item = items[row['input_id']]
        articles.append({'article': number, 'day': item['publication_day'], 'publisher': item['publisher'], 'title': item['title'], 'text': item['text'],
                         'library_held': held, 'opened': [{'ref': f'T{index}', **topics[t]} for index, t in enumerate(new, 1)], 'statements': statements})
    packet = {'questions': topics, 'articles': articles}
    (HERE / 'packet-openings.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    (keys / 'key-openings.json').write_text(json.dumps({str(n): s for n, s in enumerate(chosen, 1)} | {'opened_rows': opened_rows, 'sample': sample}, indent=1) + '\n')
    week1_opened = sum(1 for row in rows if row['sequence'] <= WEEK1_ARTICLES and row['status'] == 'complete'
                       and len(json.loads(row['after'])) > len(json.loads(row['before'])))
    print(f'openings packet: {len(articles)} articles ({len(opened_rows)} that opened a topic, {len(sample)} sampled others); '
          f'{len(topics)} questions over the fortnight; week 1 articles that opened a topic: {week1_opened} of {WEEK1_ARTICLES}')


def plant(item, kind):
    planted = copy.deepcopy(item)
    answer = planted['answer']
    rungs = re.findall(r'rung (\d) ', item['request'].split('\n', 2)[1]) or ['1', '2']
    top = max(int(r) for r in rungs)
    if kind == 'yes/no flipped':
        answer['rung'] = 2 if answer.get('rung') == 1 else 1
    else:
        answer['rung'] = top if (answer.get('rung') or 1) - 1 < top - (answer.get('rung') or 1) else 1
    if kind == 'fact added':
        answer['reasons'] = (answer.get('reasons') or '') + (' A further filing reported the opposite of what the cited items say, which moves '
                                                             'the answer to the other end of the ladder.')
    planted['planted'] = kind
    return planted


def is_yes_no(item):
    return bool(re.search(r'rung \d (Yes|No|Happened)\b', item['request'].split('\n', 2)[1]))


def answers(run_root, keys):
    run_root, keys = Path(run_root), Path(keys)
    conn = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    rows = []
    for call_id, request_json, answer_json in conn.execute(
            "select call_id, request_json, answer_json from model_calls where purpose='judge' and answer_json is not null order by call_id"):
        user = json.loads(request_json)['messages'][-1]['content']
        found = VIEW.match(user)
        if found:
            rows.append({'view': found.group(1), 'call_id': call_id, 'request': user, 'answer': json.loads(answer_json)})
    conn.close()
    last = {}
    for row in rows:
        last[row['view']] = row
    real = list(last.values())
    earlier = [row for row in rows if last[row['view']] is not row]
    rng = random.Random(SEED)
    figures = [i for i in earlier if not is_yes_no(i)]
    yes_no = [i for i in earlier if is_yes_no(i)]
    bases = rng.sample(figures, 3) + (rng.sample(yes_no, 1) if yes_no else rng.sample(figures, 1))
    planted = [plant(bases[0], 'rung moved'), plant(bases[1], 'rung moved'), plant(bases[2], 'fact added'),
               plant(bases[3], 'yes/no flipped' if yes_no else 'rung moved')]
    if any(p['request'] in [r['request'] for r in real] for p in planted):
        raise SystemExit('a planted request repeats a real one: refused')
    candidates = rng.sample(real, min(8, len(real)))
    (HERE / 'supported-candidates.json').write_text(json.dumps(
        [{'candidate': n, 'request': c['request'], 'answer': c['answer']} for n, c in enumerate(candidates, 1)], ensure_ascii=False, indent=1) + '\n')
    order = rng.sample(real + planted, len(real) + len(planted))
    (HERE / 'packet-answers.json').write_text(json.dumps([{'item': n, 'request': r['request'], 'answer': r['answer']} for n, r in enumerate(order, 1)],
                                                         ensure_ascii=False, indent=1) + '\n')
    (keys / 'key-answers.json').write_text(json.dumps(
        [{'item': n, 'view': r['view'], 'call_id': r['call_id'], 'planted': r.get('planted'),
          'candidate': next((k for k, c in enumerate(candidates, 1) if c is r), None)} for n, r in enumerate(order, 1)], indent=1) + '\n')
    print(f'answers packet: {len(real)} last judgements, 4 planted from earlier judgements; {len(order)} items; {len(candidates)} control candidates')


if __name__ == '__main__':
    command, run_root, keys = sys.argv[1:4]
    Path(keys).mkdir(parents=True, exist_ok=True)
    {'openings': openings, 'answers': answers}[command](run_root, keys)
