"""One readable trace file per article item of a split-v2 first-100 run: the article, what A proposed (closest question, what separates
it, passages), record preparation, the handover (candidates, evidence with links, drops), the matching decisions with their reasons, the
questions written and every judgement of the questions this run opened. Reads the run's snapshot; writes traces/<run>/<seq>.json."""
import json, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src')]
from hivemind import testdb

INPUT = ROOT / 'poc/data/parallel-thesis-evidence-input-2026-11-05/items.sqlite'

def main(run_name):
    run = ROOT / 'poc/data' / run_name; out = Path(__file__).parent / 'traces' / run_name; out.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(f"file:{run / 'snapshot/views.sqlite'}?mode=ro", uri=True); conn.row_factory = sqlite3.Row
    items = testdb.open_db(str(INPUT)); status = json.loads((run / 'run-status.json').read_text()); start = status['starting_seq']
    index = []
    for folder in sorted((run / 'items').glob('*'), key=lambda p: int(p.name)):
        if not (folder / 'handover.json').exists():
            continue
        seq = int(folder.name)
        user = json.loads((folder / 'b-request.json').read_text())['messages'][-1]['content']
        iid = user.split('[Item] id ')[1].split(',')[0]
        item = testdb.item_of(items.execute('select * from items where input_id=?', (iid,)).fetchone())
        a = json.loads((folder / 'a-answer.json').read_text()); b = json.loads((folder / 'b-answer.json').read_text())
        meta = json.loads((folder / 'meta-answer.json').read_text()) if (folder / 'meta-answer.json').exists() else None
        handover = json.loads((folder / 'handover.json').read_text())
        decisions = [d for (j,) in conn.execute('select decisions_json from match_records where seq=? order by id', (seq,)) for d in [json.loads(j)]]
        new_views = [dict(r) for r in conn.execute('select view_id, object_id, kind, question, due_day, year from views where created_seq=?', (seq,))]
        for v in new_views:
            v['rungs'] = [dict(r) for r in conn.execute('select position, label, condition, lo, hi from rungs where view_id=? order by position', (v['view_id'],))]
            v['judgements'] = [dict(r) for r in conn.execute('select publication_day, rung, reasons, cited_evidence_json, implied_outcome from judgements where view_id=? order by judgement_id', (v['view_id'],))]
        shown = json.loads((folder / 'shown.json').read_text())
        trace = {'seq': seq, 'input_id': iid, 'day': item['publication_day'], 'title': item['title'], 'publisher': item['publisher'], 'category': item['category'],
                 'subjects_tagged_upstream': [o.get('value') for o in item.get('object_identifiers') or []], 'questions_shown': len(shown),
                 'a_answer': a, 'record_preparation': meta, 'b_answer': b, 'handover': handover, 'matching_decisions': decisions,
                 'questions_written': new_views, 'article': item['text']}
        (out / f'{seq}.json').write_text(json.dumps(trace, ensure_ascii=False, indent=1))
        index.append({'seq': seq, 'title': item['title'][:120], 'a_questions': [q['question'] for q in a['questions']], 'b_evidence': len(b['evidence']),
                      'dropped': [d[1] for d in handover['dropped']], 'written': [v['view_id'] + ' ' + v['question'] for v in new_views]})
    ledger = [dict(r) for r in conn.execute('select view_id, created_seq, object_id, kind, question from views order by created_seq, view_id')]
    links = [dict(r) for r in conn.execute('select l.view_id, e.evidence_id, e.created_seq, e.tier, e.quote, e.one_line from evidence_links l join evidence e using(evidence_id) where e.created_seq>? order by e.created_seq', (start,))]
    judgements = [dict(r) for r in conn.execute('select view_id, publication_day, rung, reasons, cited_evidence_json, implied_outcome from judgements where seq>? order by judgement_id', (start,))]
    (out / '_index.json').write_text(json.dumps(index, ensure_ascii=False, indent=1))
    (out / '_ledger.json').write_text(json.dumps({'questions': ledger, 'evidence_links_written_this_run': links, 'judgements_this_run': judgements}, ensure_ascii=False, indent=1))
    print(run_name, len(index), 'items')

if __name__ == '__main__':
    for name in sys.argv[1:]:
        main(name)
