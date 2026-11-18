"""The record test on unread articles, the request step ($0): c8's Step 1 requests for the forty sampled unread articles
(`sample-unread.json`), each against the library the clean week draw left after its last step (2026-09-28: seven questions), written as a
trace the reviewed probe (`clean-arch/e2e-comparison-2026-11-13/identity-probe/probe_identity.py`) sends unchanged with its arms. The
request builder is the identity probe's (`build_fresh_trace.py`), which must first rebuild a stored request of the full run byte for
byte, or it refuses. The library is a labelled constructed state: every article is read against the same week-end library, not against
what a forward run would hold by then.

  python3 build_trace_record.py <output trace.sqlite>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, '/Users/lchingen/hivemind/clean-arch/e2e-comparison-2026-11-13/identity-probe')
import build_fresh_trace as builder  # noqa: E402

WEEK = Path('/Users/lchingen/hivemind/poc/data/clean-lean-week-2026-11-14/week-r2/c1/step1/trace.sqlite')


def main():
    output = Path(sys.argv[1])
    if output.exists():
        raise SystemExit(f'{output} exists')
    settings, reference_sequence = builder.check_reference()
    week = sqlite3.connect(f'file:{WEEK}?mode=ro', uri=True)
    theses = json.loads(week.execute("select after_state from trace where status='complete' order by sequence desc limit 1").fetchone()[0])
    (HERE / 'snapshot-week-end.json').write_text(json.dumps(theses, ensure_ascii=False, indent=1))
    sample = json.loads((HERE / 'sample-unread.json').read_text())['articles']
    conn = sqlite3.connect(output)
    conn.execute('create table trace (sequence integer primary key, input_id text not null, before_state text not null, request text not null, '
                 'raw_response text, status text not null)')
    cases = []
    for row in sample:
        request = builder.build_request(settings, theses, builder.item_by_id(row['input_id']))
        conn.execute('insert into trace values (?, ?, ?, ?, ?, ?)', (row['article'], row['input_id'], json.dumps(theses, ensure_ascii=False),
                     json.dumps(request), json.dumps({'sent_request': builder.live.deepseek_json_mode(request, 'high')}), 'complete'))
        cases.append({'case': f"a{row['article']:02d}-record", 'trace': str(output), 'sequence': row['article']})
    conn.commit()
    conn.close()
    (HERE / 'cases-record-2.json').write_text(json.dumps(cases, indent=1))
    print(f'reference sequence {reference_sequence} rebuilt byte for byte; {len(sample)} requests written against a library of {len(theses)} questions')


if __name__ == '__main__':
    main()
