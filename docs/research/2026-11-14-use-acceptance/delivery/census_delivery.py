"""Do the kept financial figures reach the judgements? The census ($0; DELIVERY-CHECK-DESIGN.md, D505). Read-only on a finished run.

For the new system's stored fresh-week draw it joins three stored things: the financial table's lines (each line's statements, from
`record-3/table-rows-week.json`), the run's evidence records with their links to questions and their same-claim joins
(`judge/draw-c1/views.sqlite`), and what every judgement request was shown (`judge-requests.json`). A table line is *shown* to a
question when one of its own statements was in a judgement request of that question. A statement Step 2 joined to one of them as the
same claim, shown to the question, is only a *lead*: a statement can carry several figures and the joined one may not state this
one, so whether the figure itself was in a request is read in the request (DELIVERY-CHECK-DESIGN.md, step 3). It writes
`delivery-census.json` (per line: its statements' evidence ids with their articles' place in the run, the questions it was linked
to, shown to, and has a same-claim lead for) and prints the counts. It judges nothing about what a question needs.

  python3 census_delivery.py <run folder of the clean draw>
"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TABLE = HERE.parent / 'record-3' / 'table-rows-week.json'


def main():
    run = Path(sys.argv[1])
    views = sqlite3.connect(f"file:{run / 'judge/draw-c1/views.sqlite'}?mode=ro", uri=True)
    trace = sqlite3.connect(f"file:{run / 'step1/trace.sqlite'}?mode=ro", uri=True)
    input_of = {sequence: input_id for sequence, input_id in trace.execute('select sequence, input_id from trace')}
    summary_of = {}
    for sequence, result in trace.execute('select sequence, result from trace'):
        for item in json.loads(result).get('evidence') or []:
            summary_of[(sequence, item['local_id'])] = ' '.join(item['summary'].split())
    evidence_of = {}
    for evidence_id, one_line, input_id in views.execute('select evidence_id, one_line, created_from_input from evidence'):
        evidence_of[(input_id, ' '.join(one_line.split()))] = evidence_id
    # same-claim groups (Step 2's joins), as connected sets
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for old, new in views.execute('select old_evidence_id, new_evidence_id from same_claims'):
        parent[find(old)] = find(new)
    linked = collections.defaultdict(set)
    for evidence_id, view_id in views.execute('select evidence_id, view_id from evidence_links'):
        linked[evidence_id].add(view_id)
    shown = collections.defaultdict(set)      # view -> evidence ids shown in any of its judgement requests
    last_shown = {}
    for request in json.loads((run / 'judge/draw-c1/judge-requests.json').read_text()):
        shown[request['view']].update(request['shown'])
        last_shown[request['view']] = set(request['shown'])
    shown_groups = {view: {find(e) for e in ids} for view, ids in shown.items()}
    questions = {view_id: question for view_id, question in views.execute('select view_id, question from views')}
    table = json.loads(TABLE.read_text())
    census, unmatched = {}, []
    for line_id, members in table.items():
        ids = []
        for member in members:
            evidence_id = evidence_of.get((input_of[member['article']], summary_of[(member['article'], member['statement'])]))
            if evidence_id is None:
                unmatched.append((line_id, member['article'], member['statement']))
            else:
                ids.append(evidence_id)
        census[line_id] = {'evidence': ids, 'articles': sorted({member['article'] for member in members}),
                           'linked_to': sorted({view for e in ids for view in linked.get(e, ())}),
                           'shown_to': sorted(view for view in questions if any(e in shown[view] for e in ids)),
                           'same_claim_lead_for': sorted(view for view in questions if not any(e in shown[view] for e in ids)
                                                         and any(find(e) in shown_groups[view] for e in ids))}
    (HERE / 'delivery-census.json').write_text(json.dumps({'questions': questions, 'lines': census, 'statements_dropped_before_judging': unmatched}, ensure_ascii=False, indent=1))
    statements = {e for entry in census.values() for e in entry['evidence']}
    print(f'{len(table)} table lines; {len(statements)} financial statements matched to stored evidence; {len(unmatched)} table statements with no stored evidence record: {unmatched[:6]}')
    print(f"lines with a statement linked to any question: {sum(1 for e in census.values() if e['linked_to'])}; lines with a statement shown to any judgement: "
          f"{sum(1 for e in census.values() if e['shown_to'])}; lines shown to none: {sum(1 for e in census.values() if not e['shown_to'])}")
    for view in sorted(questions):
        own = [line for line, e in census.items() if view in e['shown_to']]
        leads = [line for line, e in census.items() if view in e['same_claim_lead_for']]
        print(f"  {view}: shown {len(shown[view])} statements over its judgements (last request {len(last_shown[view])}); table lines whose own statement was shown {len(own)}: {own}; "
              f"same-claim leads only {len(leads)}")
        print(f"      {questions[view][:170]}")


if __name__ == '__main__':
    main()
