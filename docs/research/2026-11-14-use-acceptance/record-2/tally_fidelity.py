"""The record test on unread articles, the fidelity tally ($0; RECORD-TEST-2-DESIGN.md, check 2). Joins the two reader families' marks on the
forty sampled lines to the key and prints, per record and per field, the lines both mark right, both mark not right, and those they mark
differently, with every line that is not right for both. A count, not a line. It judges nothing itself.

  python3 tally_fidelity.py <key folder outside the repository>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELDS = ('source', 'measure', 'value', 'kind', 'period')


def objects(path):
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), [], 0
    while True:
        start = text.find('{"row"', position)
        if start == -1:
            return out
        row, position = decoder.raw_decode(text, start)
        out.append(row)


def main():
    key_folder = Path(sys.argv[1])
    key = json.loads((key_folder / 'record-2-key-fidelity.json').read_text())
    arms = json.loads((key_folder / 'record-2-key-views.json').read_text())
    record_of = {arms[arm]['label']: arm for arm in ('c8', 'c22')}
    packet = {row['row']: row for row in json.loads((HERE / 'fidelity-packet-whole.json').read_text())['rows']}
    marks = {'claude': {row['row']: row for row in objects(HERE / 'claude-fidelity.jsonl')},
             'codex': {row['row']: row for part in (1, 2, 3, 4) for row in objects(HERE / f'codex-fidelity-part{part}.jsonl')}}
    for family, found in marks.items():
        missing = sorted(set(key) - set(found))
        if missing:
            raise SystemExit(f'{family} reader left rows unmarked: {missing}: refused')
    good = {'right', 'unknown_ok'}
    for label in ('A', 'B'):
        rows = sorted(row for row, line_id in key.items() if line_id.startswith(label))
        print(f'RECORD {label} ({record_of[label]}): {len(rows)} sampled lines')
        for field in FIELDS:
            both_right = [r for r in rows if all(marks[f][r].get(field) in good for f in marks)]
            both_not = [r for r in rows if all(marks[f][r].get(field) not in good for f in marks)]
            differ = [r for r in rows if r not in both_right and r not in both_not]
            detail = collections.Counter(marks[f][r].get(field) for f in marks for r in both_not)
            print(f'  {field}: right for both {len(both_right)}; not right for both {len(both_not)} {dict(detail) if both_not else ""}; marked differently {len(differ)}')
        for row in rows:
            flagged = {f: {field: marks[f][row].get(field) for field in FIELDS if marks[f][row].get(field) not in good} for f in marks}
            if any(flagged.values()):
                line = packet[row]
                print(f"    {row} [{key[row]}] art {line['article']}: {line['measure'][:38]} | {line['period'][:20]} = {line['value'][:24]} | {line['kind']} | {line['source'][:32]}")
                for family in marks:
                    if flagged[family]:
                        print(f"        {family}: {flagged[family]} — {str(marks[family][row].get('note'))[:210]}")


if __name__ == '__main__':
    main()
