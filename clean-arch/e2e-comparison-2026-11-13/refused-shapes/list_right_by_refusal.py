"""D470's census, step 1 ($0): the theses of the full run's Stage A that are right (two of three sends) but not right by a written ladder,
computed with the collector's own inputs and the accounting rule (`stage_a/accounting.py`: right = every applicable mark holds and no
upheld W; a sound ladder = right and not a refusal), every unresolved point counted for the answer (the favourable treatment).

  python3 list_right_by_refusal.py
"""
import collections
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STAGE_A = ROOT / 'clean-arch/step4-2026-11-10/stage_a'
sys.path.insert(0, str(STAGE_A))
import accounting  # noqa: E402
import collect_readings  # noqa: E402

RUN = ROOT / 'poc/data/clean-e2e-full-2026-11-13/stage-a'
KEY = ROOT / 'poc/data/clean-e2e-full-2026-11-13/stage-a-key.json'


def main():
    _, item_of, outcomes, readers, _ = collect_readings.read_rows(RUN, KEY)
    families = collect_readings.third_reader_families(RUN)
    of_family = {family: collect_readings.read_rulings(RUN, item_of, outcomes, readers, family)[0] for family in families}
    rulings = {send: accounting.rulings_of_two(of_family[families[0]][send], of_family[families[1]][send], 'holds')[0]
               for send in of_family[families[0]]}
    rows1, rows2 = readers['reader 1'], readers['reader 2']
    right, sound = {}, {}
    for outcome in outcomes.values():
        key = (outcome['case'], outcome['pass'])
        kind = accounting.kind_of(outcome)
        if kind == 'refused twice':
            right[key] = sound[key] = False
            continue
        r1, r2 = rows1.get(key), rows2.get(key)
        values = {}
        for mark in accounting.marks_that_apply(kind):
            values[mark] = r1[mark] if r1[mark] == r2[mark] else rulings.get(key, {}).get('marks', {}).get(mark)
        upheld = any(row['W'].strip() and rulings.get(key, {}).get('W', {}).get(f'reader {n}') for n, row in ((1, r1), (2, r2)))
        right[key] = all(v == 'holds' for v in values.values()) and not upheld
        sound[key] = right[key] and kind != 'refusal'
    by_case = collections.defaultdict(list)
    for outcome in outcomes.values():
        by_case[outcome['case']].append(outcome)
    right_cases = [c for c, sends in by_case.items() if sum(right[(o['case'], o['pass'])] for o in sends) >= 2]
    ladder_cases = [c for c, sends in by_case.items() if sum(sound[(o['case'], o['pass'])] for o in sends) >= 2]
    print(f'right {len(right_cases)}; right by a ladder {len(ladder_cases)}; of {len(by_case)} (the collector printed 32 / 22 / 40)')
    for case in sorted(set(right_cases) - set(ladder_cases)):
        kinds = [accounting.kind_of(o) for o in sorted(by_case[case], key=lambda o: o['pass'])]
        reasons = [o.get('reason') for o in sorted(by_case[case], key=lambda o: o['pass']) if o.get('reason')]
        print(f'  {case:14s} sends: {kinds} | {reasons[0][:150] if reasons else ""}')


if __name__ == '__main__':
    main()
