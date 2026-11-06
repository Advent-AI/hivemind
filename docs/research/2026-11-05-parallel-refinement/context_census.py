"""Compare saved diagnostic snapshots with the actual replay day-start selection; no model calls or scoring."""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import b_arm
from hivemind import extraction
from hivemind.views import store


def main():
    if len(sys.argv) > 2:
        raise SystemExit('usage: context_census.py [absolute-new-output-file]')
    cfg, universe, cases = b_arm.base_requests()
    database = ROOT / 'poc/data/parallel-thesis-evidence-input-2026-11-05/views.sqlite'
    conn = sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    rows = []
    for case in cases:
        item = case['item']
        objects = [o['value'] for o in item.get('object_identifiers') or [] if universe.has(o['value'])]
        day_seq = store.day_start_seq(conn, item['publication_day'])
        actual = extraction.shown_views(conn, cfg, item, objects)
        experiment = case['shown']
        by_id = {v['view_id']: v for v in experiment}
        actual_ids, trial_ids = {v['view_id'] for v in actual}, set(by_id)
        extra, missing = trial_ids - actual_ids, actual_ids - trial_ids
        same_day = [qid for qid in extra if by_id[qid]['created_seq'] > day_seq]
        other = [qid for qid in extra if by_id[qid]['created_seq'] <= day_seq]
        rows.append({'input_id': item['input_id'], 'day': item['publication_day'], 'seq': case['seq'],
                     'objects': objects, 'day_start_seq': day_seq, 'trial_count': len(trial_ids),
                     'day_start_count': len(actual_ids), 'extra': sorted(extra), 'missing': sorted(missing),
                     'extra_same_day': sorted(same_day), 'extra_other_scope': sorted(other)})
    origins = {'total': conn.execute('select count(*) from views').fetchone()[0],
               'seq_zero': conn.execute('select count(*) from views where created_seq=0').fetchone()[0],
               'seed_prefix': conn.execute("select count(*) from views where lower(substr(created_from_input,1,5))='seed:'").fetchone()[0]}
    conn.close()
    if len(rows) != 10 or len({r['input_id'] for r in rows}) != 10:
        raise ValueError('unexpected or empty diagnostic population')
    control = next(r for r in rows if r['input_id'] == 'gnews:085b1e1a1543437edb9756d6')
    if control['trial_count'] != 8 or control['day_start_count'] != 7 or control['extra'] != ['v8'] or control['missing']:
        raise ValueError('known positive control changed')
    result = {'description': 'Same saved historical ledger; diagnostic immediately-before-item snapshot versus actual day-start and object filter. Entries are article-question pairs.',
              'source_ledger_origins': origins, 'articles': len(rows), 'different': sum(bool(r['extra'] or r['missing']) for r in rows),
              'extra_total': sum(len(r['extra']) for r in rows), 'extra_same_day_total': sum(len(r['extra_same_day']) for r in rows),
              'extra_other_scope_total': sum(len(r['extra_other_scope']) for r in rows),
              'missing_total': sum(len(r['missing']) for r in rows), 'rows': rows}
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if len(sys.argv) == 2:
        path = Path(sys.argv[1])
        if not path.is_absolute() or path.exists():
            raise ValueError('output must be an absolute new file')
        path.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
