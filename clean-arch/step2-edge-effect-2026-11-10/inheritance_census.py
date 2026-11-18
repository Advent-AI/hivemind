#!/usr/bin/env python3
"""How much of what the frozen judge read in the saved D392 clean draw 1 reached a question only because a Step 2 revision relation
carried it there? A count over the saved ledger, at no cost.

The adapter gives a record that revises an older one every question link the older one holds. A link is counted here as carried by a
relation when the record's own Step 1 links and Step 3's later links do not include that question. For each such link the count gives
the relations that carried it (one, or several), the two source readers' label for each relation (reports/step2-revision-census-2026-11-09,
a diagnostic reading, not a signed reference), the judge requests that showed the record under that question, and the judgements that
cited it there.

Usage: inheritance_census.py <new scratch folder> <output json>"""
import collections, contextlib, json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE)]
import edge_replay  # noqa: E402

LABELS = edge_replay.ROOT / 'reports/step2-revision-census-2026-11-09/comparison-after-challenge.json'


def main(scratch, output_path):
    adapter, _, _ = edge_replay.run_replay(Path(scratch).resolve(), edge_replay.STEP2)
    evidence_of = dict(adapter.evidence_of)
    adapter.conn.close()
    record_of = {evidence_id: record_id for record_id, evidence_id in evidence_of.items()}
    by_article, library = edge_replay.e2e_adapter.load_draw(edge_replay.TRACE, edge_replay.STEP2)
    records = {record['id']: record for article in by_article.values() for record in article}
    later_views = collections.defaultdict(set)
    for entry in library['later_log']:
        for record_id in entry['linked']:
            later_views[record_id].add(entry['thesis'])
    relations = [(revision['by'], revision['group']) for group in library['groups'].values() for revision in group['revises']]
    label_of = {(edge['incoming'], edge['group']): edge['after_challenge'] for edge in json.loads(LABELS.read_text())['saved_edges']}
    unlabelled = [relation for relation in relations if relation not in label_of]
    if unlabelled:
        raise SystemExit(f'relations with no reader label: {unlabelled}')

    saved = edge_replay.SAVED
    with contextlib.closing(sqlite3.connect(f"file:{saved / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        links = conn.execute('select id, evidence_id, view_id, seq from evidence_links order by id').fetchall()
        judgements = conn.execute('select view_id, publication_day, cited_evidence_json, pushes_json from judgements').fetchall()
    link_id = {(evidence_id, view_id): row_id for row_id, evidence_id, view_id, _ in links}
    shown_under = collections.Counter()
    requests = json.loads((saved / 'judge-requests.json').read_text())
    for request in requests:
        for evidence_id in request['shown']:
            shown_under[evidence_id, request['view']] += 1
    cited_under, pushed_under = collections.Counter(), collections.defaultdict(collections.Counter)
    for view_id, _, cited_json, pushes_json in judgements:
        for evidence_id in json.loads(cited_json or '[]'):
            cited_under[evidence_id, view_id] += 1
        for push in json.loads(pushes_json or '[]'):
            pushed_under[push['evidence_id'], view_id][push['push']] += 1

    carried = []
    for row_id, evidence_id, view_id, seq in links:
        record_id = record_of[evidence_id]
        if view_id in records[record_id]['thesis_ids'] or view_id in later_views[record_id]:
            continue
        carriers = []
        for by, group in relations:
            old = evidence_of.get(library['groups'][group]['original']['id'])
            if by == record_id and old and link_id.get((old, view_id), row_id) < row_id:
                carriers.append({'revised group': group, 'old evidence': old, 'readers': label_of[by, group]})
        if not carriers:
            raise SystemExit(f'link {evidence_id} -> {view_id} has no Step 1 link, no later link and no carrying relation')
        carried.append({'record': record_id, 'evidence': evidence_id, 'question': view_id, 'seq': seq, 'carried by': carriers,
                        'summary': records[record_id]['summary'], 'requests that showed it': shown_under[evidence_id, view_id],
                        'judgements that cited it': cited_under[evidence_id, view_id], 'pushes given': dict(pushed_under[evidence_id, view_id])})

    def kind(link):
        readers = {carrier['readers'] for carrier in link['carried by']}
        if readers == {'different'}:
            return 'only by relations the readers call different statements'
        if 'different' in readers:
            return 'by a relation called different and by another relation'
        return 'only by relations the readers call ' + ' or '.join(sorted(readers))

    by_kind = collections.defaultdict(lambda: collections.Counter())
    for link in carried:
        counts = by_kind[kind(link)]
        counts['links'] += 1
        counts['requests that showed it'] += link['requests that showed it']
        counts['judgements that cited it'] += link['judgements that cited it']
    requests_touched = sum(1 for request in requests if any((evidence_id, request['view']) in {(l['evidence'], l['question']) for l in carried}
                                                            for evidence_id in request['shown']))
    # The second way a relation reaches the judge: under the new record the request prints one line naming the piece it is read as a
    # later version of. Only the relation written last is printed (store.revision_of).
    group_of_original = {evidence_of[group['original']['id']]: group_id for group_id, group in library['groups'].items()
                         if group['original']['id'] in evidence_of}
    with contextlib.closing(sqlite3.connect(f"file:{saved / 'views.sqlite'}?mode=ro", uri=True)) as conn:
        revision_rows = conn.execute('select id, old_evidence_id, new_evidence_id from revisions order by id').fetchall()
    printed = {new: old for _, old, new in revision_rows}                      # the last row per new record wins
    shown_anywhere = collections.Counter(evidence_id for request in requests for evidence_id in request['shown'])
    notes = collections.defaultdict(collections.Counter)
    for new, old in printed.items():
        readers = label_of[record_of[new], group_of_original[old]]
        notes[readers]['records carrying the note'] += 1
        notes[readers]['requests that printed the note'] += shown_anywhere[new]
    summary = {'links in the ledger': len(links), 'links carried only by a revision relation': len(carried),
               'records with such a link': len({link['record'] for link in carried}),
               'questions with such a link': sorted({link['question'] for link in carried}),
               'judge requests in the run': len(requests), 'judge requests showing at least one such link': requests_touched,
               'relations in the library': len(relations), 'relations by reader label': dict(collections.Counter(label_of[r] for r in relations)),
               'by kind of carrying relation': {name: dict(counts) for name, counts in by_kind.items()},
               'relation rows written': len(revision_rows), 'records that print a later-version note': len(printed),
               'later-version notes by reader label of the printed relation': {name: dict(counts) for name, counts in notes.items()},
               'evidence showings in all requests': sum(shown_anywhere.values())}
    Path(output_path).write_text(json.dumps({'summary': summary, 'links': carried}, ensure_ascii=False, indent=1))
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    for link in carried:
        print(f"{link['evidence']:>5} {link['record']:>9} -> {link['question']:<4} shown {link['requests that showed it']:>2} cited {link['judgements that cited it']:>2} "
              f"{link['pushes given']} | " + '; '.join(f"{c['old evidence']} ({c['readers']})" for c in link['carried by']) + f" | {link['summary'][:110]}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
