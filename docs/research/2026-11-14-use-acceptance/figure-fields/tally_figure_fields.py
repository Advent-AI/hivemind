"""The figure-fields probe: the tally ($0; PROBE-DESIGN.md). Joins the two blind reader families' marks on both packets to the key and
prints every count the frozen lines read; openings, kept, linked and figure counts come from the records by code. It judges nothing
itself. Marks are counted where the two families agree; every mark they give differently is counted apart and listed.

  python3 tally_figure_fields.py <records.jsonl> <cases.json> <key folder outside the repository>
"""
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
ARMS = ('c8', 'c21')
MOST = 2 / 3 - 1e-9
KEEP = {'k1-keep': re.compile(r'Rubin', re.I), 'k2-keep': re.compile(r'hyperscal|capital expenditure|capex|spend', re.I),
        'k3-keep': re.compile(r'RTX|Ministry of Industry|MIIT', re.I)}
EMPTY_ALLOWED = {('t3-target', 1), ('t4-target', 1)}        # named figures whose party may be empty (the article names no one)


def lines(name):
    return [json.loads(line) for line in (HERE / name).read_text().splitlines() if line.strip().startswith('{')]


def main():
    records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
    cases = {case['case']: case for case in json.loads(Path(sys.argv[2]).read_text())}
    key = {row['answer']: row for row in json.loads((Path(sys.argv[3]) / 'figure-fields-key.json').read_text())}
    label_of = {(row['case'], row['arm'], row['send']): label for label, row in key.items()}
    one = {family: {row['answer']: row for row in lines(f'{family}-reader-1.jsonl')} for family in FAMILIES}
    two = {family: {row['answer']: row for row in lines(f'{family}-reader-2.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        missing = sorted(set(key) - set(one[family]))
        if missing:
            raise SystemExit(f'{family} left {len(missing)} answers of packet one unmarked ({missing[:5]}): refused')
        expected = {label for label, row in key.items() if row['arm'] == 'c21'}
        if expected - set(two[family]):
            raise SystemExit(f'{family} left {len(expected - set(two[family]))} answers of packet two unmarked: refused')
    valid = collections.defaultdict(list)
    for record in records:
        if record['attempts'][-1].get('outcome') == 'valid':
            valid[(record['case'], record['arm'])].append(record)
    print('valid sends:', {f'{case} {arm}': len(rows) for (case, arm), rows in sorted(valid.items())})

    def figure_marks(family, label):
        out = {}
        for statement in one[family][label].get('statements') or []:
            for figure in statement.get('figures') or []:
                out[(statement.get('id'), figure.get('n'))] = figure
        return out

    print('\nPARTY, the named figures (kept in how many valid sends; party right in how many of those)')
    case_state = {arm: {} for arm in ARMS}
    for case_name, case in cases.items():
        if not case.get('named_figures'):
            continue
        states = {arm: [] for arm in ARMS}
        for number, named in enumerate(case['named_figures'], 1):
            row = {}
            for arm in ARMS:
                per_family = {}
                for family in FAMILIES:
                    kept = right = 0
                    for record in valid[(case_name, arm)]:
                        label = label_of[(case_name, arm, record['send'])]
                        found = next((n for n in one[family][label].get('named') or [] if n.get('figure') == number), None)
                        if found and found.get('statement') is not None:
                            kept += 1
                            mark = (figure_marks(family, label).get((found['statement'], found.get('n'))) or {}).get('party')
                            right += mark == 'right' or (mark == 'unknown_ok' and (case_name, number) in EMPTY_ALLOWED)
                    per_family[family] = (kept, right)
                row[arm] = per_family
            total = {arm: len(valid[(case_name, arm)]) for arm in ARMS}
            exercised = all(row['c8'][family][0] >= 2 for family in FAMILIES)
            kept_ok = all(row['c21'][family][0] >= 2 and row['c21'][family][0] >= row['c8'][family][0] - 1 for family in FAMILIES)
            right_ok = {arm: all(row[arm][family][0] and row[arm][family][1] / row[arm][family][0] >= MOST for family in FAMILIES) for arm in ARMS}
            print(f"  {case_name} figure {number} ({named['figure'][:52]}): c8 {row['c8']} of {total['c8']}; c21 {row['c21']} of {total['c21']}"
                  f" | {'exercised' if exercised else 'not exercised (c8 keeps it in fewer than two)'}; c21 kept {'ok' if kept_ok else 'NOT ok'}; "
                  f"right: c8 {'yes' if right_ok['c8'] else 'no'}, c21 {'yes' if right_ok['c21'] else 'no'}")
            if exercised:
                states['c21'].append(kept_ok and right_ok['c21'])
                states['c8'].append(right_ok['c8'])
        for arm in ARMS:
            case_state[arm][case_name] = 'not exercised' if not states[arm] else ('passes' if all(states[arm]) else 'fails')
    for arm in ARMS:
        print(f'  target cases, {arm}: {case_state[arm]}')
    exercised_cases = [c for c, s in case_state['c21'].items() if s != 'not exercised']
    passing = [c for c in exercised_cases if case_state['c21'][c] == 'passes']
    room = [c for c, s in case_state['c8'].items() if s == 'fails']
    print(f'  -> exercised {len(exercised_cases)}, c21 passes {len(passing)} (line: at least four of each); room (c8 fails) on {len(room)} (needs three)')

    print('\nALL FIGURES, packet one (marks both families agree on; differing marks counted apart)')
    for field in ('party', 'measure', 'value', 'kind'):
        for arm in ARMS:
            agreed, differ = collections.Counter(), 0
            for label, row in key.items():
                if row['arm'] != arm:
                    continue
                marks = {family: figure_marks(family, label) for family in FAMILIES}
                for position in set(marks['codex']) & set(marks['claude']):
                    a, b = marks['codex'][position].get(field), marks['claude'][position].get(field)
                    if a == b:
                        agreed[a] += 1
                    else:
                        differ += 1
            total = sum(agreed.values()) + differ
            print(f"  {field:8} {arm}: agreed {dict(agreed)}; differ {differ}; of {total} figures both families marked"
                  + (f" | wrong by both {agreed.get('wrong', 0) / total:.1%}, wrong by either at most {(agreed.get('wrong', 0) + differ) / total:.1%}" if total else ''))
    print('  the statement\'s own party and date, target and control cases:')
    for field in ('statement_party', 'statement_date'):
        for arm in ARMS:
            agreed, differ = collections.Counter(), 0
            for label, row in key.items():
                if row['arm'] != arm or row['case'].endswith('-keep'):
                    continue
                by_family = {family: {s.get('id'): s.get(field) for s in one[family][label].get('statements') or []} for family in FAMILIES}
                for statement in set(by_family['codex']) & set(by_family['claude']):
                    if by_family['codex'][statement] == by_family['claude'][statement]:
                        agreed[by_family['codex'][statement]] += 1
                    else:
                        differ += 1
            print(f'    {field} {arm}: agreed {dict(agreed)}; differ {differ}')
    print('  links of statements with figures, target and control cases (reader marks):')
    for arm in ARMS:
        counts = {family: collections.Counter() for family in FAMILIES}
        for label, row in key.items():
            if row['arm'] != arm or row['case'].endswith('-keep'):
                continue
            for family in FAMILIES:
                for statement in one[family][label].get('statements') or []:
                    for link in statement.get('links') or []:
                        counts[family][link.get('mark')] += 1
                    if statement.get('should_link'):
                        counts[family]['should have been linked'] += 1
        print(f'    {arm}: ' + '; '.join(f'{family} {dict(counts[family])}' for family in FAMILIES))

    print('\nFIXED PERIOD, packet two (c21 only)')
    agreed, differ = collections.Counter(), 0
    for label in two['codex']:
        marks = {family: {(f.get('statement'), f.get('n')): f for f in two[family].get(label, {}).get('figures') or []} for family in FAMILIES}
        for position in set(marks['codex']) & set(marks['claude']):
            a, b = marks['codex'][position], marks['claude'][position]
            if a.get('established') == b.get('established') and a.get('fixed') == b.get('fixed'):
                agreed[(a.get('established'), a.get('fixed'))] += 1
            else:
                differ += 1
    established = sum(count for (is_established, _), count in agreed.items() if is_established == 'yes')
    not_established = sum(count for (is_established, _), count in agreed.items() if is_established == 'no')
    total = sum(agreed.values()) + differ
    wrong = sum(count for (_, fixed), count in agreed.items() if fixed == 'wrong')
    print(f'  agreed marks {({f"{e}/{f}": c for (e, f), c in agreed.items()})}; differ {differ}; of {total} figures')
    if established:
        print(f"  established ({established}; needs ten): right {agreed.get(('yes', 'right'), 0)} = {agreed.get(('yes', 'right'), 0) / established:.0%} (line: two thirds)")
    if not_established:
        print(f"  not established ({not_established}; needs five): left empty {agreed.get(('no', 'right'), 0)} = {agreed.get(('no', 'right'), 0) / not_established:.0%} (line: two thirds)")
    print(f'  wrong by both {wrong} = {wrong / total:.1%} of all figures (line: one in twenty); wrong by either at most {(wrong + differ) / total:.1%}')

    print('\nGUARDS BY CODE')
    for case_name, pattern in KEEP.items():
        row = {arm: (sum(1 for r in valid[(case_name, arm)] if any(pattern.search(t.get('description', '')) for t in r.get('new_theses') or [])),
                     len(valid[(case_name, arm)])) for arm in ARMS}
        control = row['c8'][0] / max(row['c8'][1], 1)
        state = 'control absent' if control < MOST else ('FAILS' if control - row['c21'][0] / max(row['c21'][1], 1) >= MOST else 'no difference seen at three sends')
        print(f"  opening, {case_name}: c8 {row['c8'][0]}/{row['c8'][1]}, c21 {row['c21'][0]}/{row['c21'][1]}: {state}")
    totals = {arm: collections.Counter() for arm in ARMS}
    for (case_name, arm), rows in valid.items():
        for record in rows:
            statements = record.get('links') or []
            totals[arm]['sends'] += 1
            totals[arm]['kept'] += len(statements)
            totals[arm]['linked'] += sum(1 for s in statements if any(l.get('target_type') == 'existing' for l in s.get('links') or []))
            totals[arm]['figures'] += sum(len(s.get('figures') or []) for s in statements)
    for name in ('kept', 'linked', 'figures'):
        a, b = totals['c8'][name] / totals['c8']['sends'], totals['c21'][name] / totals['c21']['sends']
        print(f"  {name} per send: c8 {a:.2f}, c21 {b:.2f} ({(b - a) / a:+.0%}; fails below -33%)")
    invalid = {arm: sum(1 for r in records if r['arm'] == arm and r['attempts'][-1].get('outcome') != 'valid') for arm in ARMS}
    print(f'  invalid sends: {invalid}')


if __name__ == '__main__':
    main()
