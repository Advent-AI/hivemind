"""The trial of the planted answers ($0): which of the six both families call UNSUPPORTED, naming the stored rung.

Reads the two trial packets' rows and their key, prints each family's row on every judgement of the trial, and writes
`planted-in-use.json` in the data folder: the planted answers the reading may use.

  python3 clean-arch/step4-2026-11-10/stage_b/plant_trial.py <data folder> <trial key path>
"""
import json
import sys
from pathlib import Path

FAMILIES = ('codex', 'claude')


def main():
    folder, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    rows = {family: {} for family in FAMILIES}
    for family in FAMILIES:
        for answer_file in sorted((folder / 'validation-answers').glob(f'reader-{family}-packet-*.jsonl')):
            for line in answer_file.read_text().splitlines():
                if line.strip().startswith('{'):
                    row = json.loads(line)
                    rows[family][int(row['judgement'])] = row
        missing = [number for number in key if int(number) not in rows[family]]
        if missing:
            raise SystemExit(f'{family}: no row for trial judgements {missing}')
    in_use = []
    for number, entry in key.items():
        pair = {family: (rows[family][int(number)]['verdict'], rows[family][int(number)].get('rung_the_evidence_points_to')) for family in FAMILIES}
        line = f"{number:>2} {entry['kind']:15s} {entry['draw']} {entry['view']:4s} #{entry['number_in_view']:<2} stored rung {entry['stored_rung']}, shown {entry['shown_rung']}: {pair}"
        if entry['kind'].startswith('planted'):
            passed = all(value == ('UNSUPPORTED', entry['stored_rung']) for value in pair.values())
            line += '  -> in use' if passed else '  -> NOT USED'
            if passed:
                in_use.append([entry['draw'], entry['view'], entry['number_in_view']])
        print(line)
        for family in FAMILIES:
            if rows[family][int(number)]['verdict'] != 'SUPPORTED':
                print(f"      {family}: {str(rows[family][int(number)].get('why', ''))[:300]}")
    (folder / 'planted-in-use.json').write_text(json.dumps(in_use) + '\n')
    print(f'{len(in_use)} of {sum(1 for entry in key.values() if entry["kind"].startswith("planted"))} planted answers pass the trial; written to planted-in-use.json')


if __name__ == '__main__':
    main()
