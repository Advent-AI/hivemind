"""D505's gap on the fortnight, the code part ($0; D564): the company's own financial figures the first step kept, grouped where
Step 2 joined repeats, and for each judged question whether each group reached its last judgement's request. Code decides only
identity: whose figure (the statement's own party), which typed measure, which group, which ids the request showed, which day.
Whether a figure bears on a question is the readers'.

  python3 figures_census.py <run root> <key folder>     # writes packet-figures-<n>.json and the key
"""
import collections
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMPANY = re.compile(r'^\s*(nvidia|nvda)\b', re.I)
MEASURE = re.compile(r'revenue|sales|margin|eps|earnings|net income|profit|cash flow|repurchase|buyback|dividend|guidance|outlook', re.I)
SEED = 20261116


def main(run_root, keys):
    run_root, keys = Path(run_root), Path(keys)
    trace = sqlite3.connect(f"file:{run_root / 'c1/step1/trace.sqlite'}?mode=ro", uri=True)
    records = []
    for input_id, result in trace.execute("select input_id, result from trace where status='complete' order by sequence"):
        for evidence in json.loads(result).get('evidence', []):
            figures = [f for f in evidence.get('figures') or [] if MEASURE.search(str(f.get('measure') or ''))]
            if COMPANY.match(evidence.get('original_party') or '') and figures:
                records.append((input_id, evidence['summary'], figures))
    store = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    by_text = collections.defaultdict(list)
    for evidence_id, input_id, one_line in store.execute('select e.evidence_id, e.created_from_input, e.one_line from evidence e'):
        by_text[(input_id, one_line)].append(evidence_id)
    parent = {}
    def root(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x
    for old, new in store.execute('select old_evidence_id, new_evidence_id from same_claims'):
        parent[root(new)] = root(old)
    day_of = dict(store.execute('select evidence_id, min(publication_day) from evidence_sources group by evidence_id'))
    groups = collections.defaultdict(list)
    unmatched = 0
    for input_id, summary, figures in records:
        ids = by_text.get((input_id, summary))
        if not ids:
            unmatched += 1
            continue
        for evidence_id in ids:
            groups[root(evidence_id)].append((evidence_id, summary, figures))
    print(f'company figure statements kept: {len(records)} ({unmatched} not found in the store by article and summary); groups: {len(groups)}')
    judged = []
    for view_id, question, due in store.execute('select view_id, question, due_day from views order by created_seq'):
        last = store.execute('select publication_day, request_sha256, cited_evidence_json from judgements where view_id=? order by seq desc, judgement_id desc limit 1', (view_id,)).fetchone()
        if last:
            judged.append((view_id, question, last))
    requests = json.loads((run_root / 'c1/judge/draw-c1/judge-requests.json').read_text())
    shown_last = {}
    for request in requests:
        shown_last[request['view']] = (request['day'], set(request['shown']))
    archive = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/archive.sqlite'}?mode=ro", uri=True)
    packet, key = [], {}
    rng = random.Random(SEED)
    for view_id, question, (day, sha, cited) in judged:
        request = json.loads(archive.execute('select request_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])['messages'][-1]['content']
        answer = json.loads(archive.execute('select answer_json from model_calls where request_sha256 = ?', (sha,)).fetchone()[0])
        shown = shown_last[view_id][1]
        candidates = []
        for group, members in groups.items():
            ids = {m[0] for m in members}
            first_day = min(day_of.get(i, '9999') for i in ids)
            if ids & shown or first_day > day:
                continue
            evidence_id, summary, figures = sorted(members, key=lambda m: day_of.get(m[0], '9999'))[0]
            candidates.append({'day': day_of.get(evidence_id), 'statement': summary, 'figures': figures, 'reports': len(ids), 'group': group})
        rng.shuffle(candidates)
        delivered = sum(1 for group, members in groups.items() if {m[0] for m in members} & shown)
        entry = {'question_ref': f'Q{len(packet) + 1}', 'request': request, 'answer': {k: answer.get(k) for k in ('rung', 'implied_outcome', 'reasons')},
                 'candidates': [dict({k: v for k, v in c.items() if k != 'group'}, ref=f'F{n}') for n, c in enumerate(candidates, 1)]}
        key[entry['question_ref']] = {'view': view_id, 'day': day, 'groups': {f'F{n}': c['group'] for n, c in enumerate(candidates, 1)}, 'delivered_groups': delivered}
        packet.append(entry)
        print(f'{view_id} (judged {day}): company figure groups delivered {delivered}; available and not delivered {len(candidates)} | {question[:80]}')
    order = rng.sample(packet, len(packet))
    halves = [order[: len(order) // 2], order[len(order) // 2:]]
    for n, half in enumerate(halves, 1):
        (HERE / f'packet-figures-{n}.json').write_text(json.dumps(half, indent=1, ensure_ascii=False) + '\n')
        print(f'packet {n}: {len(half)} questions, {sum(len(e["candidates"]) for e in half)} candidates, {len((HERE / f"packet-figures-{n}.json").read_text()):,} characters')
    (keys / 'key-figures.json').write_text(json.dumps(key, indent=1) + '\n')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
