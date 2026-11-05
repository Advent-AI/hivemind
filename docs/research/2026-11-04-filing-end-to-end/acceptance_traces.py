"""What the acceptance reads besides its conditions (acceptance-design.md, "Read as well"), from finished runs only: for each candidate draw, the
coverage-start record (questions linked, records written, figures refused with their reasons); every judgement of v10 and v12 (day, rung, reasons);
the first judgement of each question that received starting figures, with the starting-figure records it cites; and, for each question, evidence
pieces in force and judgements at the window end in the candidate and the control draw of the same number.

usage: python3 acceptance_traces.py <candidate arm folder> <control arm folder> [question ...]
"""
import json
import sqlite3
import sys
from pathlib import Path

WINDOW_END = '2026-07-14'


def ledger(run):
    out = Path(run) / 'run.out'
    if out.exists() and 'RUN-ARM-DONE' not in out.read_text():
        raise SystemExit(f'{run} is not finished')
    conn = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def main():
    candidate, control = (sorted(p for p in Path(arm).iterdir() if p.is_dir() and p.name.startswith('d')) for arm in sys.argv[1:3])
    extra = sys.argv[3:]
    for run, twin in zip(candidate, control):
        conn, base = ledger(run), ledger(twin)
        row = conn.execute("select reason, sequence_no, publication_day from processing_steps where step='baseline'").fetchone()
        record = json.loads(row['reason'])
        records = [r['evidence_id'] for r in conn.execute('select evidence_id from evidence where created_seq=?', (row['sequence_no'],))]
        print(f'===== {run.name}: coverage-start record (seq {row["sequence_no"]}, day {row["publication_day"]}): linked {record["changed"]}, '
              f'{len(records)} records; refused {record["refused"]}')
        for view_id in ['v10', 'v12'] + extra:
            print(f'  -- {view_id} judgements (candidate):')
            for j in conn.execute('select publication_day, rung, reasons, cited_evidence_json from judgements where view_id=? and publication_day<=? order by judgement_id',
                                  (view_id, WINDOW_END)):
                cited = [e for e in json.loads(j['cited_evidence_json'] or '[]') if e in records]
                print(f'     {j["publication_day"]} rung {j["rung"]} cites starting records {cited}: {j["reasons"][:260]}')
        for view_id in record['changed']:
            first = conn.execute('select publication_day, rung, reasons, cited_evidence_json from judgements where view_id=? order by judgement_id limit 1', (view_id,)).fetchone()
            if first:
                cited = [e for e in json.loads(first['cited_evidence_json'] or '[]') if e in records]
                print(f'  first judgement {view_id} {first["publication_day"]} rung {first["rung"]} cites starting records {cited}: {first["reasons"][:200]}')
        print(f'  {"question":8} {"pieces cand/ctrl":17} {"judgements cand/ctrl":21}')
        for k in range(1, 23):
            view_id = f'v{k}'
            pieces = [db.execute('select count(*) from evidence_links where view_id=?', (view_id,)).fetchone()[0] for db in (conn, base)]
            judged = [db.execute('select count(*) from judgements where view_id=? and publication_day<=?', (view_id, WINDOW_END)).fetchone()[0] for db in (conn, base)]
            print(f'  {view_id:8} {pieces[0]:>4} / {pieces[1]:<10} {judged[0]:>4} / {judged[1]:<10}')


if __name__ == '__main__':
    main()
