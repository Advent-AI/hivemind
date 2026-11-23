"""D609's $0 trace, the identity part: the company's own figures on the carried fortnight against the 12 judged questions. Code decides
only identity (whose statement, whether it carries a figure, which store record, which repeat group, which day, which request showed it,
which question it is linked to); whether a statement bears on a question is read by hand, beside its source, afterwards.

Population: every Step 1 evidence item whose original party is the company and which carries at least one figure of any measure (no
measure list), each item separately. Reconciled to the store by (article, summary); unmatched items are listed, not called dropped.

For each judged question and each population member whose first source day is on or before the question's last judgement day:
  shown_last    the member's own record is in the last judging request;
  shown_earlier its own record is in an earlier request of that question only (its conclusion is carried forward);
  group_shown   another member of its repeat group was shown (the substance is compared by hand later, not assumed equal);
  linked_to     the questions its record is linked to;
  never         none of the above for this question.

  python3 trace_figures.py <run root> <output folder>
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

COMPANY = re.compile(r'^\s*(nvidia|nvda)\b', re.I)


def main(run_root, out):
    run_root, out = Path(run_root), Path(out)
    trace = sqlite3.connect(f"file:{run_root / 'c1/step1/trace.sqlite'}?mode=ro", uri=True)
    population = []
    for input_id, result in trace.execute("select input_id, result from trace where status='complete' order by sequence"):
        for evidence in json.loads(result).get('evidence', []):
            if COMPANY.match(evidence.get('original_party') or '') and evidence.get('figures'):
                population.append({'input_id': input_id, 'summary': evidence['summary'], 'figures': evidence['figures'],
                                   'passages': evidence.get('passages') or evidence.get('quotes') or evidence.get('quote')})
    store = sqlite3.connect(f"file:{run_root / 'c1/judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    by_text = collections.defaultdict(list)
    for evidence_id, input_id, one_line in store.execute('select evidence_id, created_from_input, one_line from evidence'):
        by_text[(input_id, one_line)].append(evidence_id)
    parent = {}

    def root(x):
        while parent.get(x, x) != x:
            x = parent[x]
        return x
    for old, new in store.execute('select old_evidence_id, new_evidence_id from same_claims'):
        parent[root(new)] = root(old)
    day_of = dict(store.execute('select evidence_id, min(publication_day) from evidence_sources group by evidence_id'))
    links = collections.defaultdict(set)
    for evidence_id, view_id in store.execute('select evidence_id, view_id from evidence_links'):
        links[evidence_id].add(view_id)
    members, unmatched = [], []
    for item in population:
        ids = by_text.get((item['input_id'], item['summary']))
        if not ids:
            unmatched.append(item)
            continue
        for evidence_id in ids:
            members.append(dict(item, evidence_id=evidence_id, group=root(evidence_id), day=day_of.get(evidence_id)))
    group_ids = collections.defaultdict(set)
    for member in members:
        group_ids[member['group']].add(member['evidence_id'])
    requests = collections.defaultdict(list)
    for request in json.loads((run_root / 'c1/judge/draw-c1/judge-requests.json').read_text()):
        requests[request['view']].append(request)
    questions = {view_id: (question, due) for view_id, question, due in store.execute('select view_id, question, due_day from views')}
    rows = []
    for view_id, its_requests in requests.items():
        its_requests.sort(key=lambda r: (r['day'], r['seq']))
        last = its_requests[-1]
        shown_last, shown_any = set(last['shown']), set().union(*(set(r['shown']) for r in its_requests))
        for member in members:
            if member['day'] is None or member['day'] > last['day']:
                continue
            others = group_ids[member['group']] - {member['evidence_id']}
            status = ('shown_last' if member['evidence_id'] in shown_last else 'shown_earlier' if member['evidence_id'] in shown_any
                      else 'group_shown' if others & shown_any else 'never')
            rows.append({'view': view_id, 'question': questions[view_id][0], 'last_day': last['day'], 'requests': len(its_requests),
                         'evidence_id': member['evidence_id'], 'group': member['group'], 'day': member['day'], 'status': status,
                         'linked_to': sorted(links.get(member['evidence_id'], ())), 'summary': member['summary'], 'figures': member['figures'],
                         'input_id': member['input_id'], 'group_shown_ids': sorted(others & shown_any)})
    out.mkdir(parents=True, exist_ok=True)
    (out / 'pairs.jsonl').write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
    (out / 'unmatched.jsonl').write_text('\n'.join(json.dumps(u, ensure_ascii=False) for u in unmatched) + '\n')
    print(f'population: {len(population)} company statements with a figure; matched to store records: {len(members)} members '
          f'in {len(group_ids)} repeat groups; unmatched items: {len(unmatched)}')
    print(f'judged questions with requests: {len(requests)}; fact-question pairs available by the last judgement: {len(rows)}')
    tally = collections.Counter((r['view'], r['status']) for r in rows)
    for view_id in sorted(requests, key=lambda v: int(v[1:]) if v[1:].isdigit() else v):
        counts = {s: tally[(view_id, s)] for s in ('shown_last', 'shown_earlier', 'group_shown', 'never')}
        print(f'  {view_id} (last {requests[view_id][-1]["day"]}, {len(requests[view_id])} requests): {counts} | {questions[view_id][0][:90]}')
    linked = collections.Counter(('linked elsewhere' if r['linked_to'] and r['view'] not in r['linked_to'] else
                                  'linked here' if r['view'] in r['linked_to'] else 'unlinked') for r in rows if r['status'] == 'never')
    print('never-shown pairs by link state:', dict(linked))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
