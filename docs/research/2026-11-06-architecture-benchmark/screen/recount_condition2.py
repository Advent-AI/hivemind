"""Condition 2 of the screen recomputed from the blind reader's verdicts on every not-kept match (notkept-check-reader.out): a send's not-kept count
is the matches the reader says the record keeps as its statement. "unsure" is counted both ways and both results are printed. The same correction
applies to every version and to S_n.

    python3 recount_condition2.py <occurrences.json (the key file kept outside the repository)>"""
import itertools
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    occurrences = json.load(open(sys.argv[1]))['occurrences']
    text = (HERE / 'notkept-check-reader.out').read_text()
    verdicts = {r['id']: r['recorded'] for r in json.loads(text[text.index('['):text.rindex(']') + 1])}
    missing = sorted({pid for _, _, _, pid in occurrences} - set(verdicts))
    if missing:
        raise SystemExit(f'not decidable: the reader gave no verdict for {len(missing)} pairs')
    names = sorted({name for name, _, _, _ in occurrences} | {f'{a}{k}' for a, n in (('C', 6), ('R', 3), ('P', 3)) for k in range(1, n + 1)})
    for unsure_counts in (True, False):
        counts = {n: 0 for n in names}
        for name, _, _, pid in occurrences:
            v = verdicts[pid]
            counts[name] += v == 'yes' or (unsure_counts and v == 'unsure')
        mean = lambda ns: sum(counts[n] for n in ns) / len(ns)
        current = [f'C{k}' for k in range(1, 7)]
        s_n = max(abs(mean(list(a)) - mean([c for c in current if c not in a])) for a in itertools.combinations(current, 3))
        bound = mean(['P1', 'P2', 'P3']) + s_n
        r, c46 = mean(['R1', 'R2', 'R3']), mean(['C4', 'C5', 'C6'])
        label = 'unsure counted as kept' if unsure_counts else 'unsure not counted'
        print(f'[{label}] per send: ' + ', '.join(f'{n} {counts[n]}' for n in names))
        print(f'  C1–C3 {mean(["C1", "C2", "C3"]):.2f}; C4–C6 {c46:.2f}; R {r:.2f}; P {mean(["P1", "P2", "P3"]):.2f}; S_n {s_n:.2f}; bound {bound:.2f}')
        print(f'  condition 2: {"PASS" if r <= bound else "FAIL"}; self-check {"holds" if c46 <= bound else "NOT DECIDABLE"}')
    print('verdicts:', {v: sum(1 for x in verdicts.values() if x == v) for v in set(verdicts.values())})


if __name__ == '__main__':
    main()
