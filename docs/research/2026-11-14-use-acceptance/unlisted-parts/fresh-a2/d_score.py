"""The D diagnostic's score (council round 106; $0): the four D-only readings against the frozen expectations and adopt rule.

  python3 d_score.py <key .json outside the repository>

Reads d-diagnostic/readings/{codex,claude}-{unchanged,clarified}.jsonl, maps packet items back to candidates by the key, and prints
each reading's marks by group, the constructed controls and the uncounted item apart, then the rule's result.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent / 'd-diagnostic'
FAMILIES, BRIEFS = ('codex', 'claude'), ('unchanged', 'clarified')
CLASS, FAIL, HOLD, KEPT, OVER, UNCOUNTED = range(1, 13), (13, 14, 15, 17, 18), range(19, 23), 23, 24, 16


def reading(family, brief, key):
    rows = [json.loads(line) for line in (HERE / 'readings' / f'{family}-{brief}.jsonl').read_text().splitlines() if line.strip().startswith('{')]
    marks = {key[str(row['item'])]: row['D'] for row in rows}
    if sorted(marks) != list(range(1, 25)) or any(mark not in ('holds', 'fails', 'n/a') for mark in marks.values()):
        raise SystemExit(f'{family}-{brief}: not one valid D for each of the 24 items')
    return marks, {key[str(row['item'])]: row.get('why', '') for row in rows}


def main(key_path):
    key = {item: int(candidate) for item, candidate in json.loads(Path(key_path).read_text()).items()}
    expected = {int(n): entry['D'] for n, entry in json.loads((HERE / 'expected.json').read_text())['expected'].items()}
    marks, reasons = {}, {}
    for family in FAMILIES:
        for brief in BRIEFS:
            marks[(family, brief)], reasons[(family, brief)] = reading(family, brief, key)
    print('reading            class holds (1-12)   fail controls failed   stated holds (19-22)   23 (stated kept)   24 (stated, code day)   16 (uncounted)')
    for (family, brief), found in marks.items():
        print(f'{family:6} {brief:10}  {sum(found[n] == "holds" for n in CLASS):>4} of 12          {sum(found[n] == "fails" for n in FAIL):>2} of 5'
              f'               {sum(found[n] == "holds" for n in HOLD):>2} of 4              {found[KEPT]:8}           {found[OVER]:8}              {found[UNCOUNTED]}')
    clarified = {family: marks[(family, 'clarified')] for family in FAMILIES}
    unchanged = {family: marks[(family, 'unchanged')] for family in FAMILIES}
    controls = list(FAIL) + list(HOLD) + [KEPT, OVER]
    moved = [(family, n, unchanged[family][n], clarified[family][n]) for family in FAMILIES for n in controls
             if unchanged[family][n] == expected[n] and clarified[family][n] != expected[n]]
    checks = {
        'Codex holds D on at least 10 of items 1-12 under the sentence': sum(clarified['codex'][n] == 'holds' for n in CLASS) >= 10,
        'both families fail D on at least 4 of items 13, 14, 15, 17, 18 under the sentence':
            all(sum(clarified[family][n] == 'fails' for n in FAIL) >= 4 for family in FAMILIES),
        'both families hold D on at least 3 of items 19-22 under the sentence':
            all(sum(clarified[family][n] == 'holds' for n in HOLD) >= 3 for family in FAMILIES),
        'both families hold item 23 and fail item 24 under the sentence':
            all(clarified[family][KEPT] == 'holds' and clarified[family][OVER] == 'fails' for family in FAMILIES),
        'no control moves away from its expected mark under the sentence': not moved,
    }
    print()
    for check, passed in checks.items():
        print(f'{"PASS" if passed else "FAIL"}  {check}')
    if moved:
        print('controls that moved:', moved)
    print('\nDECISION:', 'ADOPT the sentence' if all(checks.values()) else 'NOT ADOPTED')
    print('\nreasons given for D fails on class items 1-12:')
    for (family, brief), found in marks.items():
        for n in CLASS:
            if found[n] == 'fails':
                print(f'  {family} {brief} item {n}: {reasons[(family, brief)][n][:200]}')


if __name__ == '__main__':
    main(sys.argv[1])
