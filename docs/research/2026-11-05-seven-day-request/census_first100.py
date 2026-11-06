"""$0 census of a split run's first 100 rows (or a finished first-100 run): new questions with subject, kind and ladder; passages per new
question from the new-question call; drops by reason; matching outcomes; judged questions. Reads a snapshot of the run's ledger.
Usage: census_first100.py RUN_DIR [LAST_SEQ]"""
import json, re, sqlite3, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
UNIVERSE = json.loads((ROOT / 'poc/universe.json').read_text())
LISTED = {c['id'] for c in UNIVERSE['companies']} | {t['id'] for t in UNIVERSE['themes']}

def main(run, last_seq=None):
    status = json.loads((run / 'run-status.json').read_text()); start = status['starting_seq']
    db = run / 'snapshot/views.sqlite'
    conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True); conn.row_factory = sqlite3.Row
    manifest = json.loads((run / 'manifest.json').read_text()); first = {r['id'] for r in manifest['input_rows'][:100]}
    seqs = sorted({r['sequence_no'] for r in conn.execute("select input_id, sequence_no from processing_steps where step='dispatched' and sequence_no>?", (start,)) if r['input_id'] in first})
    last = last_seq or max(seqs)
    views = [dict(r) for r in conn.execute('select * from views where created_seq>? and created_seq<=? order by created_seq', (start, last))]
    out = {'run': str(run), 'items': 0, 'new_questions': [], 'drops': {}, 'outcomes': {}, 'a_passages': [], 'judged_new': 0}
    for v in views:
        rungs = conn.execute('select count(*), sum(lo is not null or hi is not null) from rungs where view_id=?', (v['view_id'],)).fetchone()
        a_ev = conn.execute('select count(*) from evidence_links l join evidence e using(evidence_id) where l.view_id=? and e.created_seq=?', (v['view_id'], v['created_seq'])).fetchone()[0]
        judged = conn.execute('select count(*) from judgements where view_id=?', (v['view_id'],)).fetchone()[0]
        key = conn.execute('select measure from view_keys where view_id=?', (v['view_id'],)).fetchone()
        out['new_questions'].append({'view_id': v['view_id'], 'seq': v['created_seq'], 'object': v['object_id'], 'listed_subject': v['object_id'] in LISTED,
                                     'kind': v['kind'], 'question': v['question'], 'rungs': rungs[0], 'numeric_rungs': bool(rungs[1]), 'opening_passages': a_ev,
                                     'judged': judged, 'key': key[0] if key else ''})
        out['judged_new'] += judged > 0
    for seq in seqs:
        if seq > last:
            continue
        folder = run / 'items' / str(seq)
        if not (folder / 'handover.json').exists():
            continue
        out['items'] += 1
        h = json.loads((folder / 'handover.json').read_text())
        for _, reason in h['dropped']:
            label = re.sub(r'year \S+ is', 'year X is', reason)
            out['drops'][label] = out['drops'].get(label, 0) + 1
    for row in conn.execute('select decisions_json, seq from match_records where seq>? and seq<=?', (start, last)):
        for d in json.loads(row['decisions_json']).get('candidates', []):
            out['outcomes'][d['outcome']] = out['outcomes'].get(d['outcome'], 0) + 1
    q = out['new_questions']
    numeric = [x for x in q if x['rungs'] == 0 and re.match(r'(What|How)', x['question']) or x['numeric_rungs']]
    print(f"items {out['items']}  new questions {len(q)}  unlisted subject {sum(not x['listed_subject'] for x in q)}  judged {out['judged_new']}")
    print(f"numeric questions with a ladder {sum(x['numeric_rungs'] for x in numeric)} of {len(numeric)}")
    pas = [x['opening_passages'] for x in q]
    print(f"opening passages per new question: mean {sum(pas)/max(1,len(pas)):.1f} max {max(pas or [0])}")
    print('drops', out['drops']); print('matching outcomes', out['outcomes'])
    for x in q:
        print(f"  {x['view_id']:5s} {x['seq']} {x['object'][:24]:24s} {x['kind']:5s} rungs {x['rungs']} {'num' if x['numeric_rungs'] else '   '} pass {x['opening_passages']:2d} judged {x['judged']} {x['key'] or '':11s} | {x['question'][:95]}")
    (run / 'census-first100.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n') if run.name.startswith('split-v2') else None
    return out

if __name__ == '__main__':
    main(Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else None)
