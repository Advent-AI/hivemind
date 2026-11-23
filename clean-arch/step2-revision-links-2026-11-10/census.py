#!/usr/bin/env python3
"""Every link the frozen judge's ledger holds only because a Step 2 revision relation carried it, in the three saved D392 clean draws,
with what a reader needs to judge it. No model call; the saved runs are opened read-only.

The experimental adapter (clean-arch/e2e-2026-11-09/adapter.py, Adapter.article) gives a record that revises an older one every
question link the older one holds. A link is "carried" here when the record's own Step 1 links and Step 3's later links do not include
that question. For each carried link the census gives: the record, the question, each relation that carried it with the older record,
whether another record of the same Step 3 group (the same statement, by Jev) is already under that question by its own link, how
often the judge was shown the record there and cited it, and whether the link was the only new link of that question on its day (so
the question was judged that day only because of it).

Usage: census.py <output json>"""
import collections, contextlib, glob, json, sqlite3, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT / 'clean-arch/e2e-2026-11-09'), str(ROOT / 'src')]
import adapter as e2e_adapter  # noqa: E402

DRAWS = ROOT / 'poc/data/clean-e2e-2026-11-09'


def source_items(trace):
    """input id -> the source item as Step 1 was shown it."""
    items = {}
    for part in trace.split('+'):
        with contextlib.closing(sqlite3.connect(f'file:{part}?mode=ro', uri=True)) as conn:
            for input_id, request, status in conn.execute('select input_id, request, status from trace order by sequence'):
                if status == 'complete':
                    items[input_id] = json.JSONDecoder().raw_decode(json.loads(request)['messages'][1]['content'])[0]['source_item']
    return items


def draw_census(draw):
    judged = Path(sorted(glob.glob(str(DRAWS / f'stage2-clean-d{draw}/judged*')))[-1])     # draw 3's completed run is judged-2
    trace = f"{DRAWS}/stage2-clean-d{draw}/trace.sqlite+{DRAWS}/stage2-clean-d{draw}-segment-2/trace.sqlite"
    by_article, library = e2e_adapter.load_draw(trace, DRAWS / f'stage2-clean-d{draw}-segment-2/step2')
    records = {record['id']: record for article in by_article.values() for record in article}
    opened = {thesis_id: thesis for theses in e2e_adapter.trace_articles(trace)[1].values() for thesis_id, thesis in theses.items()}
    items = source_items(trace)
    later = collections.defaultdict(set)
    for entry in library['later_log']:
        for record_id in entry['linked']:
            later[record_id].add(entry['thesis'])
    with contextlib.closing(sqlite3.connect(f'file:{judged}/views.sqlite?mode=ro', uri=True)) as conn:
        conn.row_factory = sqlite3.Row
        evidence = {row['evidence_id']: dict(row) for row in conn.execute('select * from evidence')}
        links = [dict(row) for row in conn.execute('select * from evidence_links order by id')]
        revisions = [dict(row) for row in conn.execute('select * from revisions order by id')]
        views = {row['view_id']: dict(row) for row in conn.execute('select * from views')}
        rungs = collections.defaultdict(list)
        for row in conn.execute('select view_id, label, condition from rungs order by view_id, position'):
            rungs[row['view_id']].append(f"{row['label']}: {row['condition']}")
        judgements = [dict(row) for row in conn.execute('select view_id, seq, publication_day, rung, cited_evidence_json, pushes_json from judgements')]
        day_of_seq = {row['seq']: row['publication_day'] for row in conn.execute('select seq, publication_day from evidence_sources')}
    by_key = collections.defaultdict(list)
    for record in records.values():
        by_key[record['input_id'], record['summary']].append(record['id'])
    record_of = {}
    for evidence_id, row in evidence.items():
        candidates = by_key[row['created_from_input'], row['one_line']]
        if len(candidates) != 1:
            raise SystemExit(f'draw {draw}: {evidence_id} does not map to one Step 1 record')
        record_of[evidence_id] = candidates[0]
    evidence_of = {record_id: evidence_id for evidence_id, record_id in record_of.items()}
    link_id = {(link['evidence_id'], link['view_id']): link['id'] for link in links}
    requests = json.loads((judged / 'judge-requests.json').read_text())
    shown = collections.Counter((e, request['view']) for request in requests for e in request['shown'])
    cited, pushes = collections.Counter(), collections.defaultdict(collections.Counter)
    for judgement in judgements:
        for e in json.loads(judgement['cited_evidence_json'] or '[]'):
            cited[e, judgement['view_id']] += 1
        for push in json.loads(judgement['pushes_json'] or '[]'):
            pushes[push['evidence_id'], judgement['view_id']][push['push']] += 1
    new_links_of_round = collections.Counter((link['view_id'], day_of_seq[link['seq']]) for link in links)

    def describe(record_id):
        record = records[record_id]
        return {'record': record_id, 'evidence': evidence_of.get(record_id), 'article': record['input_id'], 'publication_date': record['publication_date'],
                'statement_date': record.get('statement_date'), 'original_party': record.get('original_party'),
                'reporting_speaker': record.get('reporting_speaker'), 'tier': record['tier'], 'summary': record['summary'],
                'passages': record.get('verified_passages') or record.get('passages'),
                'own_step1_questions': [v for v in record['thesis_ids'] if v in views], 'later_linked_questions': sorted(later[record_id]),
                # every thesis Step 1 filed the record under: the seeded test judges only the 22 seed questions and drops a link to a
                # thesis the clean system opened itself, so a record can be filed by Step 1 and still have no judged question
                'step1_theses': [{'id': t, 'question': opened[t]['description'] if t in opened else views[t]['question']} for t in record['thesis_ids']]}

    carried = []
    for link in links:
        record_id = record_of[link['evidence_id']]
        view_id = link['view_id']
        if view_id in records[record_id]['thesis_ids'] or view_id in later[record_id]:
            continue
        carriers = [describe(record_of[row['old_evidence_id']]) for row in revisions
                    if row['new_evidence_id'] == link['evidence_id'] and link_id.get((row['old_evidence_id'], view_id), link['id']) < link['id']]
        if not carriers:
            raise SystemExit(f"draw {draw}: link {link['evidence_id']} -> {view_id} has no Step 1 link, no later link and no carrying relation")
        group = library['groups'][library['placement'][record_id]]
        same_statement = [copy['id'] for copy in [group['original']] + group['members']
                          if copy['id'] != record_id and view_id in (records[copy['id']]['thesis_ids'] + sorted(later[copy['id']]))
                          and copy['id'] in evidence_of]
        day = day_of_seq[link['seq']]
        carried_that_round = sum(1 for other in links if other['view_id'] == view_id and day_of_seq[other['seq']] == day
                                 and view_id not in records[record_of[other['evidence_id']]]['thesis_ids']
                                 and view_id not in later[record_of[other['evidence_id']]])
        carried.append({'draw': draw, 'question': view_id, 'question_text': views[view_id]['question'], 'ladder': rungs[view_id],
                        'new': describe(record_id), 'carried_by': carriers, 'day': day,
                        'same_statement_already_under_the_question_by_its_own_link': same_statement,
                        'shown_to_the_judge': shown[link['evidence_id'], view_id], 'cited': cited[link['evidence_id'], view_id],
                        'pushes': dict(pushes[link['evidence_id'], view_id]),
                        'question_judged_that_day_only_for_carried_links': new_links_of_round[view_id, day] == carried_that_round})
    totals = {'draw': draw, 'ledger': judged.name, 'links': len(links), 'relations': len(revisions), 'carried links': len(carried),
              'records with a carried link': len({c['new']['record'] for c in carried}),
              'carried links of a record Step 1 filed under no thesis at all': sum(not c['new']['step1_theses'] for c in carried),
              'carried links of a record Step 1 filed only under a thesis the seeded test does not judge': sum(bool(c['new']['step1_theses']) and not c['new']['own_step1_questions'] for c in carried),
              'evidence showings': sum(len(request['shown']) for request in requests),
              'showings of carried links': sum(c['shown_to_the_judge'] for c in carried),
              'carried links whose statement is already under the question': sum(bool(c['same_statement_already_under_the_question_by_its_own_link']) for c in carried),
              'rounds judged only for carried links': len({(c['question'], c['day']) for c in carried if c['question_judged_that_day_only_for_carried_links']})}
    articles = {input_id: items[input_id] for c in carried for input_id in [c['new']['article']] + [o['article'] for o in c['carried_by']]}
    return totals, carried, articles


if __name__ == '__main__':
    output = {'draws': [], 'carried': [], 'articles': {}}
    for draw in (1, 2, 3):
        totals, carried, articles = draw_census(draw)
        output['draws'].append(totals)
        output['carried'].extend(carried)
        output['articles'].update(articles)
        print(json.dumps(totals))
    Path(sys.argv[1]).write_text(json.dumps(output, ensure_ascii=False, indent=1))
    for c in output['carried']:
        print(f"\nd{c['draw']} {c['new']['evidence']:>5} {c['new']['record']:>9} -> {c['question']} [{c['question_text'][:70]}] day {c['day']} shown {c['shown_to_the_judge']} cited {c['cited']} "
              f"{c['pushes']} already-there {c['same_statement_already_under_the_question_by_its_own_link']} only-reason-judged {c['question_judged_that_day_only_for_carried_links']}")
        print(f"     NEW ({c['new']['original_party']}; Step 1 theses {[t['id'] for t in c['new']['step1_theses']]}): {c['new']['summary'][:260]}")
        for old in c['carried_by']:
            print(f"     OLD {old['evidence']} {old['record']} ({old['original_party']}): {old['summary'][:260]}")
