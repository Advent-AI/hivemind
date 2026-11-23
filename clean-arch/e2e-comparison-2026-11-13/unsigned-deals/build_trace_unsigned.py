"""The unsigned-deal probe, the request step ($0): c8's Step 1 requests for the reader-chosen fresh articles (`reader-marks.jsonl`), against
the library the acceptance run left after its last step (c8 exactly, from empty, 2026-09-05..07: `snapshot-acceptance-2026-09-07.json`),
written as a trace the reviewed probe (`../identity-probe/probe_identity.py`) sends unchanged. The request builder is the identity probe's
(`../identity-probe/build_fresh_trace.py`), which must first rebuild a stored request of the full run byte for byte, or it refuses.

  python3 build_trace_unsigned.py <output trace.sqlite>
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'identity-probe'))
import build_fresh_trace as builder  # noqa: E402

SNAPSHOT = HERE / 'snapshot-acceptance-2026-09-07.json'


def chosen():
    rows = [json.loads(line) for line in (HERE / 'reader-marks.jsonl').read_text().splitlines() if line.strip().startswith('{')]
    return [row for row in rows if row.get('chosen')]


def main():
    output = Path(sys.argv[1])
    if output.exists():
        raise SystemExit(f'{output} exists')
    settings, reference_sequence = builder.check_reference()
    theses = json.loads(SNAPSHOT.read_text())
    conn = sqlite3.connect(output)
    conn.execute('create table trace (sequence integer primary key, input_id text not null, before_state text not null, request text not null, '
                 'raw_response text, status text not null)')
    for sequence, row in enumerate(chosen(), 1):
        request = builder.build_request(settings, theses, builder.item_by_id(row['input_id']))
        conn.execute('insert into trace values (?, ?, ?, ?, ?, ?)', (sequence, row['input_id'], json.dumps(theses, ensure_ascii=False),
                     json.dumps(request), json.dumps({'sent_request': builder.live.deepseek_json_mode(request, 'high')}), 'complete'))
        print(sequence, row['story'], row['input_id'], row['expected'])
    conn.commit()
    conn.close()
    print(f'reference c3 sequence {reference_sequence} rebuilt byte for byte; {len(chosen())} fresh requests written to {output}')


if __name__ == '__main__':
    main()
