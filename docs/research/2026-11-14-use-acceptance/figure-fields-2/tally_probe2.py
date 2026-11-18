"""The second figure-fields probe: the tally ($0; PROBE-DESIGN.md). Joins the blind readers' marks (packet one: both arms; packet two: the
candidate arm), the fresh pair's settling marks where they exist, and the records, and prints EVERY line of the design with a verdict:
met, NOT met, undecided (a difference between the families that could change it), not exercised, or not computed. It judges nothing
itself. `--lines` prints the list of lines and exits.

  python3 tally_probe2.py <records.jsonl> <cases.json> <key folder outside the repository>
"""
import collections
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FAMILIES = ('codex', 'claude')
CONTROL, CANDIDATE = 'c8', 'c22'
MOST = 2 / 3 - 1e-9
LINES = ['valid sends', 'named figures', 'a1-control', 'party, all figures', 'party missing', 'fixed period: where written', 'fixed period: wrong',
         'fixed period: year-unknown cases', 'fixed period: code check', 'openings', 'kept per send', 'linked per send', 'figures per send',
         'links by statement and question', "the statement's own party and date", 'measure and value', 'kind', 'format']
KEEP = {'k1-keep': re.compile(r'Hugging Face', re.I), 'k2-keep': re.compile(r'Blackwell|export', re.I)}


def lines_of(name):
    path = HERE / name
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip().startswith('{')]


def main():
    if '--lines' in sys.argv:
        print('\n'.join(LINES))
        return
    records = [json.loads(line) for line in Path(sys.argv[1]).read_text().splitlines() if line.strip()]
    cases = {case['case']: case for case in json.loads(Path(sys.argv[2]).read_text())}
    key = {row['answer']: row for row in json.loads((Path(sys.argv[3]) / 'figure-fields-2-key.json').read_text())}
    label_of = {(row['case'], row['arm'], row['send']): label for label, row in key.items()}
    verdict = {name: 'not computed' for name in LINES}
    one = {family: {row['answer']: row for row in lines_of(f'{family}-reader-1.jsonl')} for family in FAMILIES}
    two = {family: {row['answer']: row for row in lines_of(f'{family}-reader-2.jsonl')} for family in FAMILIES}
    settle = {family: {row['answer']: row for row in lines_of(f'{family}-reader-1-settle.jsonl')} for family in FAMILIES}
    for family in FAMILIES:
        if set(key) - set(one[family]):
            raise SystemExit(f'{family} left {len(set(key) - set(one[family]))} answers of packet one unmarked: refused')
        candidate_labels = {label for label, row in key.items() if row['arm'] == CANDIDATE}
        if candidate_labels - set(two[family]):
            raise SystemExit(f'{family} left {len(candidate_labels - set(two[family]))} answers of packet two unmarked: refused')
    valid = collections.defaultdict(list)
    for record in records:
        if record['attempts'][-1].get('outcome') == 'valid':
            valid[(record['case'], record['arm'])].append(record)
    short = [f'{case} {arm}' for case in cases for arm in (CONTROL, CANDIDATE) if len(valid[(case, arm)]) < 2]
    verdict['valid sends'] = 'met' if not short else f'cases left out: {short}'
    print('valid sends per case and arm:', {f'{case} {arm}': len(rows) for (case, arm), rows in sorted(valid.items())})

    def figure_marks(source, family, label):
        return {(s.get('id'), f.get('n')): f for s in source[family].get(label, {}).get('statements') or [] for f in s.get('figures') or []}

    def settled_mark(label, position, field):
        """(mark, state): the mark both first readers give; else the one both fresh readers give; else None with 'open'."""
        first = [figure_marks(one, family, label).get(position, {}).get(field) for family in FAMILIES]
        if first[0] == first[1]:
            return first[0], 'agreed'
        fresh = [figure_marks(settle, family, label).get(position, {}).get(field) for family in FAMILIES]
        if fresh[0] is not None and fresh[0] == fresh[1]:
            return fresh[0], 'settled'
        return None, 'open'

    print('\nNAMED FIGURES (kept: valid sends in which each family finds it; right: its party, and its kind where the case says, by settled marks)')
    case_state = {}
    for case_name, case in cases.items():
        if not case.get('named_figures'):
            continue
        outcomes = []
        for number, named in enumerate(case['named_figures'], 1):
            kept = {arm: 0 for arm in (CONTROL, CANDIDATE)}
            right = wrong = open_marks = 0
            for arm in (CONTROL, CANDIDATE):
                for record in valid[(case_name, arm)]:
                    label = label_of[(case_name, arm, record['send'])]
                    found = [next((n for n in one[family][label].get('named') or [] if n.get('figure') == number), None) for family in FAMILIES]
                    if not all(f and f.get('statement') is not None for f in found):
                        continue
                    kept[arm] += 1
                    if arm != CANDIDATE:
                        continue
                    position = (found[0]['statement'], found[0].get('n'))
                    party, state = settled_mark(label, position, 'party')
                    kind, kind_state = settled_mark(label, position, 'kind')
                    stored = next((f for s in record.get('links') or [] if s.get('local_id') == position[0]
                                   for index, f in enumerate(s.get('figures') or [], 1) if index == position[1]), {})
                    party_ok = party == 'right' or (party == 'unknown_ok' and 'empty' in named['accepted'])
                    kind_ok = True
                    if named.get('kind_not'):
                        kind_ok = stored.get('kind') != named['kind_not']
                    if named.get('kind_is'):
                        kind_ok = stored.get('kind') == named['kind_is'] and kind != 'wrong'
                    if state == 'open' or kind_state == 'open':
                        open_marks += 1
                    elif party_ok and kind_ok:
                        right += 1
                    else:
                        wrong += 1
            exercised = kept[CONTROL] >= 2 or kept[CANDIDATE] >= 2
            retained = kept[CANDIDATE] >= kept[CONTROL] - 1 and not (kept[CONTROL] >= 2 and kept[CANDIDATE] < 2)
            if not exercised:
                state = 'not exercised'
            elif not retained:
                state = 'NOT retained'
            elif kept[CANDIDATE] and right / kept[CANDIDATE] >= MOST:
                state = 'right'
            elif kept[CANDIDATE] and (right + open_marks) / kept[CANDIDATE] >= MOST:
                state = 'undecided'
            else:
                state = 'NOT right'
            outcomes.append(state)
            print(f"  {case_name} figure {number} ({named['figure'][:56]}): kept c8 {kept[CONTROL]}, c22 {kept[CANDIDATE]}; right {right}, wrong {wrong}, open {open_marks} -> {state}")
        live = [o for o in outcomes if o != 'not exercised']
        case_state[case_name] = ('not exercised' if not live else 'fails' if any(o.startswith('NOT') for o in live)
                                 else 'undecided' if 'undecided' in live else 'passes')
        if case_name == 'a1-control':
            verdict['a1-control'] = 'met' if outcomes == ['right', 'right'] else ('undecided' if all(o in ('right', 'undecided') for o in outcomes) else f'NOT met {outcomes}')
    exercised_cases = [c for c, s in case_state.items() if s != 'not exercised']
    failing = [c for c in exercised_cases if case_state[c] == 'fails']
    undecided = [c for c in exercised_cases if case_state[c] == 'undecided']
    print('  cases:', case_state)
    if len(exercised_cases) < 6:
        verdict['named figures'] = f'not exercised (only {len(exercised_cases)} cases)'
    elif len(failing) > 1:
        verdict['named figures'] = f'NOT met (fail: {failing})'
    elif len(failing) + len(undecided) > 1:
        verdict['named figures'] = f'undecided (fail {failing}, undecided {undecided})'
    else:
        verdict['named figures'] = f'met ({len(exercised_cases)} exercised, fail {failing})'

    print('\nALL FIGURES, packet one, both arms settled alike')
    rates = {}
    for field in ('party', 'measure', 'value', 'kind'):
        for arm in (CONTROL, CANDIDATE):
            counts = collections.Counter()
            for label, row in key.items():
                if row['arm'] != arm:
                    continue
                positions = set(figure_marks(one, 'codex', label)) & set(figure_marks(one, 'claude', label))
                for position in positions:
                    mark, state = settled_mark(label, position, field)
                    counts[mark if state != 'open' else 'open'] += 1
            total = sum(counts.values())
            rates[(field, arm)] = (counts, total)
            print(f'  {field:8} {arm}: {dict(counts)} of {total}')

    def line(field, arm, limit, what='wrong'):
        counts, total = rates[(field, arm)]
        if not total:
            return 'not exercised'
        low, high = counts.get(what, 0) / total, (counts.get(what, 0) + counts.get('open', 0)) / total
        return ('met' if high <= limit else 'NOT met' if low > limit else 'undecided') + f' ({low:.1%} to {high:.1%})'

    verdict['party, all figures'] = line('party', CANDIDATE, 0.05)
    verdict['party missing'] = line('party', CANDIDATE, 0.10, 'missing')
    measure, value = line('measure', CANDIDATE, 0.05), line('value', CANDIDATE, 0.05)
    verdict['measure and value'] = 'met' if measure.startswith('met') and value.startswith('met') else f'measure {measure}; value {value}'
    counts_c8, total_c8 = rates[('kind', CONTROL)]
    counts_c22, total_c22 = rates[('kind', CANDIDATE)]
    if total_c8 and total_c22:
        low, high = counts_c22.get('wrong', 0) / total_c22, (counts_c22.get('wrong', 0) + counts_c22.get('open', 0)) / total_c22
        control_low = counts_c8.get('wrong', 0) / total_c8
        limit = min(0.05, control_low + 0.05)
        verdict['kind'] = ('met' if high <= limit else 'NOT met' if low > 0.05 else 'undecided') + f' (c22 {low:.1%} to {high:.1%}; c8 {control_low:.1%} to {(counts_c8.get("wrong", 0) + counts_c8.get("open", 0)) / total_c8:.1%})'

    print("\nTHE STATEMENT'S OWN PARTY AND DATE (the statement holding the named figures; marks both families agree on)")
    wrong_statements = {}
    for arm in (CONTROL, CANDIDATE):
        counts = collections.Counter()
        for label, row in key.items():
            if row['arm'] != arm or not cases[row['case']].get('named_figures'):
                continue
            located = [n.get('statement') for n in one['claude'][label].get('named') or [] if n.get('statement')]
            if not located:
                continue
            target = collections.Counter(located).most_common(1)[0][0]
            for field in ('statement_party', 'statement_date'):
                pair = [next((s.get(field) for s in one[family][label].get('statements') or [] if s.get('id') == target), None) for family in FAMILIES]
                counts[f'{field}: ' + (pair[0] if pair[0] == pair[1] else 'differ')] += 1
        wrong_statements[arm] = counts.get('statement_party: wrong', 0) + counts.get('statement_date: wrong', 0)
        print(f'  {arm}: {dict(sorted(counts.items()))}')
    verdict["the statement's own party and date"] = 'met' if wrong_statements[CANDIDATE] - wrong_statements[CONTROL] < 2 else f'NOT met ({wrong_statements})'

    print('\nFIXED PERIOD (packet two, the candidate arm; marks both families agree on)')
    agreed, differ = collections.Counter(), 0
    code_fail, disagreements, per_case_unknown = [], [], collections.defaultdict(lambda: collections.Counter())
    texts = {}
    for case_name, case in cases.items():
        trace = sqlite3.connect(f"file:{case['trace']}?mode=ro", uri=True)
        request = json.loads(trace.execute('select request from trace where sequence = ?', (case['sequence'],)).fetchone()[0])
        payload, _ = json.JSONDecoder().raw_decode(request['messages'][1]['content'])
        texts[case_name] = payload['source_item']['text']
    for label, row in key.items():
        if row['arm'] != CANDIDATE:
            continue
        record = next(r for r in valid[(row['case'], CANDIDATE)] if r['send'] == row['send'])
        stored = {(s.get('local_id'), index): f for s in record.get('links') or [] for index, f in enumerate(s.get('figures') or [], 1)}
        marks = {family: {(f.get('statement'), f.get('n')): f for f in two[family][label].get('figures') or []} for family in FAMILIES}
        for position, figure in stored.items():
            fixed = figure.get('fiscal_period')
            code_ok = None
            if fixed:
                year = fixed[2:6]
                short = year[2:]            # the year written near a fiscal marker: "fiscal 2027", "fiscal Q2 2027", "the second quarter of fiscal 2027", "FY27"
                marker = (rf'fiscal[^.\n]{{0,30}}?\b{year}\b|FY\s?({year}|{short})\b|\b{year}\b[^.\n]{{0,12}}fiscal' if fixed.startswith('FY')
                          else rf'\b{year}\b')
                code_ok = bool(re.search(marker, texts[row['case']], re.I))
                if not code_ok:
                    code_fail.append((row['case'], row['send'], figure.get('period'), fixed))
            a, b = marks['codex'].get(position), marks['claude'].get(position)
            if not a or not b:
                continue
            if cases[row['case']].get('year_unknown'):
                per_case_unknown[row['case']][(row['send'], 'written' if fixed else 'empty')] += 1
            if a.get('written') == b.get('written') and a.get('fixed') == b.get('fixed'):
                agreed[(a.get('written'), a.get('fixed'), a.get('deducible') if a.get('written') == 'no' else None)] += 1
                if fixed and code_ok is not None and (a.get('fixed') == 'right') != code_ok:
                    disagreements.append((row['case'], row['send'], figure.get('period'), fixed, f"readers {a.get('fixed')}, code {'written' if code_ok else 'not written'}"))
            else:
                differ += 1
    total = sum(agreed.values()) + differ
    written = sum(c for (w, _, _), c in agreed.items() if w == 'yes')
    right_written = sum(c for (w, f, _), c in agreed.items() if w == 'yes' and f == 'right')
    wrong = sum(c for (_, f, _), c in agreed.items() if f == 'wrong')
    print(f'  agreed {({str(k): v for k, v in agreed.items()})}; differ {differ}; of {total} figures')
    if written < 10:
        verdict['fixed period: where written'] = f'not exercised ({written} figures)'
    else:
        low, high = right_written / written, (right_written + differ) / written
        verdict['fixed period: where written'] = ('met' if low >= MOST else 'undecided' if high >= MOST else 'NOT met') + f' ({right_written} of {written} right)'
    if total:
        verdict['fixed period: wrong'] = ('met' if (wrong + differ) / total <= 0.05 else 'NOT met' if wrong / total > 0.05 else 'undecided') + f' ({wrong} wrong, {differ} differing, of {total})'
    unknown_written = unknown_total = 0
    state = []
    for case_name in [c for c in cases if cases[c].get('year_unknown')]:
        by_send = collections.defaultdict(lambda: [0, 0])
        for (send, what), count in per_case_unknown[case_name].items():
            by_send[send][0 if what == 'written' else 1] += count
        sends_with_two = sum(1 for w, e in by_send.values() if w + e >= 2)
        sends_written = sum(1 for w, e in by_send.values() if w)
        unknown_written += sum(w for w, e in by_send.values())
        unknown_total += sum(w + e for w, e in by_send.values())
        state.append((case_name, 'not exercised' if sends_with_two < 2 else 'fails' if len(by_send) and sends_written / len(by_send) >= MOST else 'ok', dict(by_send)))
    print('  year-unknown cases (per send: fixed periods written, left empty):', state)
    if not state or any(s == 'not exercised' for _, s, _ in state):
        verdict['fixed period: year-unknown cases'] = 'not exercised'
    elif any(s == 'fails' for _, s, _ in state) or (unknown_total and unknown_written / unknown_total > 0.05):
        verdict['fixed period: year-unknown cases'] = f'NOT met ({unknown_written} written of {unknown_total})'
    else:
        verdict['fixed period: year-unknown cases'] = f'met ({unknown_written} written of {unknown_total})'
    candidate_figures = sum(len(s.get('figures') or []) for (case, arm), rows in valid.items() if arm == CANDIDATE for r in rows for s in r.get('links') or [])
    verdict['fixed period: code check'] = ('met' if len(code_fail) / max(candidate_figures, 1) <= 0.05 else 'NOT met') + f' ({len(code_fail)} of {candidate_figures} figures carry a year the article does not write)'
    for row in code_fail:
        print('    code check fails:', row)
    for row in disagreements:
        print('    readers and code differ:', row)
    deducible = sum(c for (w, f, d), c in agreed.items() if w == 'no' and d == 'yes')
    print(f"  reported: left empty though the article writes the year {sum(c for (w, f, _), c in agreed.items() if w == 'yes' and f == 'empty_missing')}; "
          f'left empty where a reader could deduce it {deducible}')

    print('\nGUARDS BY CODE')
    opening_states, pooled = [], {CONTROL: [0, 0], CANDIDATE: [0, 0]}
    for case_name, pattern in KEEP.items():
        row = {arm: (sum(1 for r in valid[(case_name, arm)] if any(pattern.search(t.get('description', '')) for t in r.get('new_theses') or [])),
                     len(valid[(case_name, arm)])) for arm in (CONTROL, CANDIDATE)}
        control = row[CONTROL][0] / max(row[CONTROL][1], 1)
        if control < MOST:
            opening_states.append('absent')
        else:
            for arm in (CONTROL, CANDIDATE):
                pooled[arm][0] += row[arm][0]
                pooled[arm][1] += row[arm][1]
            opening_states.append('fails' if control - row[CANDIDATE][0] / max(row[CANDIDATE][1], 1) >= MOST else 'ok')
        print(f"  opening, {case_name}: c8 {row[CONTROL][0]}/{row[CONTROL][1]}, c22 {row[CANDIDATE][0]}/{row[CANDIDATE][1]}: {opening_states[-1]}")
    other = collections.defaultdict(lambda: collections.Counter())
    for (case_name, arm), rows in valid.items():
        for record in rows:
            for kind in {t.get('opens_as') for t in record.get('new_theses') or []}:
                other[(case_name, kind)][arm] += 1
    one_sided = [(k, dict(v)) for k, v in other.items() if (v[CONTROL] >= 2 and v[CANDIDATE] == 0) or (v[CANDIDATE] >= 2 and v[CONTROL] == 0)]
    print('  questions one arm opens in most sends and the other in none (by case and reason):', one_sided)
    if all(s == 'absent' for s in opening_states):
        verdict['openings'] = 'not exercised (control absent on every keep case)'
    elif 'fails' in opening_states or one_sided or (pooled[CONTROL][1] and pooled[CONTROL][0] / pooled[CONTROL][1] - pooled[CANDIDATE][0] / max(pooled[CANDIDATE][1], 1) >= 0.5):
        verdict['openings'] = 'NOT met'
    else:
        verdict['openings'] = 'no difference seen at three sends'
    totals = {arm: collections.Counter() for arm in (CONTROL, CANDIDATE)}
    links = collections.defaultdict(lambda: collections.Counter())
    for (case_name, arm), rows in valid.items():
        for record in rows:
            statements = record.get('links') or []
            totals[arm]['sends'] += 1
            totals[arm]['kept'] += len(statements)
            totals[arm]['linked'] += sum(1 for s in statements if any(l.get('target_type') == 'existing' for l in s.get('links') or []))
            totals[arm]['figures'] += sum(len(s.get('figures') or []) for s in statements)
            if not case_name.endswith('-keep'):
                for question in {l['target_id'] for s in statements if s.get('figures') for l in s.get('links') or [] if l.get('target_type') == 'existing'}:
                    links[(case_name, question)][arm] += 1
    for name, line_name in (('kept', 'kept per send'), ('linked', 'linked per send'), ('figures', 'figures per send')):
        a, b = totals[CONTROL][name] / totals[CONTROL]['sends'], totals[CANDIDATE][name] / totals[CANDIDATE]['sends']
        verdict[line_name] = ('met' if a == 0 or (b - a) / a >= -1 / 3 else 'NOT met') + f' (c8 {a:.2f}, c22 {b:.2f})'
    lopsided = [(k, dict(v)) for k, v in links.items() if (v[CONTROL] >= 2 and v[CANDIDATE] == 0) or (v[CANDIDATE] >= 2 and v[CONTROL] == 0)]
    print('  links by statement and question:', {f'{k[0]} -> {k[1]}': dict(v) for k, v in sorted(links.items())})
    verdict['links by statement and question'] = 'met' if not lopsided else f'to be read by both families: {lopsided}'
    invalid = {arm: sum(1 for r in records if r['arm'] == arm and r['attempts'][-1].get('outcome') != 'valid') for arm in (CONTROL, CANDIDATE)}
    verdict['format'] = ('met' if invalid[CANDIDATE] <= invalid[CONTROL] + 1 else 'NOT met') + f' ({invalid})'

    print('\nEVERY LINE OF THE DESIGN')
    for name in LINES:
        print(f'  {name}: {verdict[name]}')


if __name__ == '__main__':
    main()
