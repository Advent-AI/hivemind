"""Stage A's accounting (DESIGN.md §8, "The accounting"; D400): from the outcomes of the 132 sends, two readers' rows and the
third reader's rulings, to the six lines. It reads only what it is given and judges nothing itself.

A send is one case in one pass. Its outcome is a ladder, a refusal by the model ("no ladder"), or "no ladder: refused" (refused
twice by code), which nobody reads. A reader's row is valid when it carries every field of the form with a value of the form's
set and a verdict, never `n/a`, on every mark that applies. A mark's value is the two readers' value where they agree and the
third reader's ruling where they differ. A fault a reader names under `W` goes to the third reader; upheld, the send is not right.
"""
import collections

LADDER_MARKS = ['Q', 'O', 'R', 'D', 'X', 'L', 'XR']            # apply to every written ladder
RULED_MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'L', 'XR', 'N']
ALL_MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'G', 'L', 'XR', 'N']
VERDICTS = ('holds', 'fails')
NOT_MEASURED = 'NOT MEASURED'


def kind_of(outcome):
    """What a send's outcome is to a reader: a figure, an event, a refusal, or nothing to read. Runs stored before D409 hold an
    event as yes/no or as five states, and are still read."""
    if outcome['status'] == 'no ladder: refused':
        return 'refused twice'
    if outcome['status'] == 'no ladder':
        return 'refusal'
    ladder = outcome['answer']['ladder']
    company = outcome['view']['kind'] == 'asset'
    if ladder.get('figure') is not None:
        return 'company figure' if company else 'theme figure'
    if ladder.get('event') is not None:
        return 'event'
    if ladder.get('states') is not None:
        return 'company states' if company else 'theme states'
    return 'yes/no'


def marks_that_apply(kind):
    """The marks on which a reader must give `holds` or `fails` for an outcome of this kind (G is not among them: it is reported)."""
    if kind == 'refusal':
        return ['N']
    marks = list(LADDER_MARKS)
    if kind in ('company figure', 'company states'):
        marks.append('F')
    if kind in ('company figure', 'theme figure'):
        marks.append('Y')
    return marks


def row_problem(row, outcome):
    """None when a reader's row is valid for this outcome, else what is wrong with it."""
    if row is None:
        return 'no row'
    kind = kind_of(outcome)
    applicable = marks_that_apply(kind)
    for mark in ALL_MARKS:
        if mark not in row:
            return f'{mark} is missing'
        value = row[mark]
        if mark == 'G':
            allowed = ('holds', 'fails', 'not_assessable') if kind in ('company figure', 'theme figure') else ('n/a',)
        elif mark in applicable:
            allowed = VERDICTS
        else:
            allowed = ('n/a',)
        if value not in allowed:
            return f'{mark} is {value!r}; for {kind} it is one of {allowed}'
    if not isinstance(row.get('W'), str):
        return 'W is missing or not a string'
    if not isinstance(row.get('why'), str):
        return 'why is missing or not a string'
    listed = 0 if kind == 'refusal' else len(outcome['answer']['ladder']['not_judged'])
    if not isinstance(row.get('B'), list) or len(row['B']) != listed or any(value not in ('bet', 'not_a_bet') for value in row['B']):
        return f'B must hold one of bet or not_a_bet for each of the {listed} parts listed'
    if (row['W'].strip() or any(row[mark] == 'fails' for mark in applicable)) and not row['why'].strip():
        return 'why is empty though a mark fails or W names a fault'
    return None


def rulings_of_two(ruling_of_one, ruling_of_other, unresolved_as):
    """One send's rulings from two third readers, one of each reader family. Where the two rule a mark alike, that is the
    mark's value. Where they differ the mark is unresolved: it takes `unresolved_as` ('holds' or 'fails'), so that every line can
    be read both ways, and it is listed. A fault named under `W` is upheld when both uphold it and not upheld when neither does;
    where they differ it is upheld only under 'fails'. A point one of the two did not rule on is left out, and the accounting
    then reports it as a missing ruling. Returns (the rulings as `account` takes them, the unresolved points)."""
    resolved, unresolved = {'marks': {}, 'W': {}}, []
    for mark in sorted(set(ruling_of_one.get('marks', {})) & set(ruling_of_other.get('marks', {}))):
        one, other = ruling_of_one['marks'][mark], ruling_of_other['marks'][mark]
        if one == other:
            resolved['marks'][mark] = one
        else:
            resolved['marks'][mark] = unresolved_as
            unresolved.append(mark)
    for reader in sorted(set(ruling_of_one.get('W', {})) & set(ruling_of_other.get('W', {}))):
        one, other = ruling_of_one['W'][reader], ruling_of_other['W'][reader]
        if one == other:
            resolved['W'][reader] = one
        else:
            resolved['W'][reader] = unresolved_as == 'fails'
            unresolved.append(f'W of {reader}')
    return resolved, unresolved


def account(outcomes, rows_of_reader_1, rows_of_reader_2, rulings):
    """The report of Stage A.

    outcomes: one dict a send with `case`, `pass`, `status`, `answer`, `view` (as the runner writes them).
    rows_of_reader_1, rows_of_reader_2: {(case, pass): row}.
    rulings: {(case, pass): {'marks': {mark: 'holds'|'fails'}, 'W': {'reader 1'|'reader 2': True|False}}}, the third reader's;
    True means the named fault is upheld.
    """
    report = {'sends': len(outcomes), 'outcomes': collections.Counter(kind_of(outcome) for outcome in outcomes), 'invalid rows': [],
              'missing rulings': [], 'upheld W': [], 'W named': [], 'lines': {}, 'shares': {}}
    read = [outcome for outcome in outcomes if kind_of(outcome) != 'refused twice']
    values, right, sound_ladder = {}, {}, {}
    differing_pairs, applicable_pairs = 0, 0
    for outcome in outcomes:
        key = (outcome['case'], outcome['pass'])
        kind = kind_of(outcome)
        if kind == 'refused twice':
            right[key], sound_ladder[key] = False, False
            continue
        rows = (rows_of_reader_1.get(key), rows_of_reader_2.get(key))
        problems = [row_problem(row, outcome) for row in rows]
        for reader_number, problem in enumerate(problems, start=1):
            if problem:
                report['invalid rows'].append((key, f'reader {reader_number}', problem))
        if any(problems):
            continue
        ruling = rulings.get(key, {})
        send_values, complete = {}, True
        for mark in marks_that_apply(kind):
            applicable_pairs += 1
            if rows[0][mark] == rows[1][mark]:
                send_values[mark] = rows[0][mark]
            else:
                differing_pairs += 1
                ruled = ruling.get('marks', {}).get(mark)
                if ruled not in VERDICTS:
                    report['missing rulings'].append((key, mark))
                    complete = False
                else:
                    send_values[mark] = ruled
        upheld = False
        for reader_number, row in enumerate(rows, start=1):
            if row['W'].strip():
                report['W named'].append((key, f'reader {reader_number}', row['W'].strip()))
                decided = ruling.get('W', {}).get(f'reader {reader_number}')
                if decided not in (True, False):
                    report['missing rulings'].append((key, f'W of reader {reader_number}'))
                    complete = False
                elif decided:
                    upheld = True
                    report['upheld W'].append((key, f'reader {reader_number}', row['W'].strip()))
        if not complete:
            continue
        values[key] = send_values
        all_hold = all(value == 'holds' for value in send_values.values()) and not upheld
        right[key] = all_hold
        sound_ladder[key] = all_hold and kind != 'refusal'

    report['dispute share'] = 'no reading' if not read else (differing_pairs, applicable_pairs)
    reading_is_complete = not report['invalid rows'] and not report['missing rulings']
    too_disputed = bool(read) and applicable_pairs and differing_pairs * 3 > applicable_pairs
    measured = bool(read) and reading_is_complete and not too_disputed
    report['reading'] = ('no reading: every send was refused twice' if not read else
                         'incomplete: a row or a ruling is missing' if not reading_is_complete else
                         'too disputed: the readers differ on more than a third of the marks' if too_disputed else 'complete')

    ladders = [outcome for outcome in read if kind_of(outcome) != 'refusal']
    refusals = [outcome for outcome in read if kind_of(outcome) == 'refusal']

    def failing(mark, population):
        return [(outcome['case'], outcome['pass']) for outcome in population if values.get((outcome['case'], outcome['pass']), {}).get(mark) == 'fails']

    for number, mark in ((1, 'Q'), (2, 'L'), (3, 'R')):
        if not ladders or not measured:
            report['lines'][number] = NOT_MEASURED
        else:
            failed = failing(mark, ladders)
            report['lines'][number] = ('met' if not failed else 'missed', failed)
    if not refusals:
        report['lines'][4] = 'no refusal occurred'
    elif not measured:
        report['lines'][4] = NOT_MEASURED
    else:
        failed = failing('N', refusals)
        report['lines'][4] = ('met' if not failed else 'missed', failed)

    cases = sorted({outcome['case'] for outcome in outcomes})
    sends_of = {case: sorted((outcome for outcome in outcomes if outcome['case'] == case), key=lambda outcome: outcome['pass']) for case in cases}
    if read and not measured:
        report['lines'][5] = NOT_MEASURED
    else:
        right_cases = [case for case in cases if sum(right[(o['case'], o['pass'])] for o in sends_of[case]) >= 2]
        ladder_cases = [case for case in cases if sum(sound_ladder[(o['case'], o['pass'])] for o in sends_of[case]) >= 2]
        met = len(right_cases) >= 35 and len(ladder_cases) >= 28
        report['lines'][5] = ('met' if met else 'missed', {'right': len(right_cases), 'right by a ladder': len(ladder_cases), 'of': len(cases)})

    all_company_figures = [case for case in cases if len(sends_of[case]) == 3 and all(kind_of(o) == 'company figure' for o in sends_of[case])]
    all_ladders = [case for case in cases if len(sends_of[case]) == 3 and all(kind_of(o) not in ('refusal', 'refused twice') for o in sends_of[case])]
    shape_differs = [case for case in all_ladders if len({kind_of(o) for o in sends_of[case]}) > 1]
    if len(all_company_figures) < 3:
        direction = (NOT_MEASURED, {'theses whose three sends are company figures': len(all_company_figures), 'needed': 3})
    else:
        differing = [case for case in all_company_figures
                     if len({o['answer']['ladder']['figure']['favourable_end'] for o in sends_of[case]}) > 1]
        direction = ('met' if not differing else 'missed', {'theses': len(all_company_figures), 'direction differs': differing})
    if len(all_ladders) < 20:
        due_day = (NOT_MEASURED, {'theses whose three sends are ladders': len(all_ladders), 'needed': 20})
    else:
        same = [case for case in all_ladders if len({o['view']['due_day'] for o in sends_of[case]}) == 1]      # the day the question is due (D414)
        due_day = ('met' if len(same) * 10 >= len(all_ladders) * 9 else 'missed', {'theses': len(all_ladders), 'same due day': len(same)})
    report['lines'][6] = {'direction': direction, 'due day': due_day, 'shape differs across sends': shape_differs}

    if measured:
        populations = {mark: ladders for mark in LADDER_MARKS}
        populations['F'] = [o for o in ladders if kind_of(o) in ('company figure', 'company states')]
        populations['Y'] = [o for o in ladders if kind_of(o) in ('company figure', 'theme figure')]
        populations['N'] = refusals
        for mark, population in populations.items():
            holding = sum(1 for o in population if values[(o['case'], o['pass'])][mark] == 'holds')
            report['shares'][mark] = 'none to count' if not population else (holding, len(population))
    figures = [o for o in ladders if kind_of(o) in ('company figure', 'theme figure')]
    for reader_number, rows in ((1, rows_of_reader_1), (2, rows_of_reader_2)):
        counts = collections.Counter()
        for outcome in figures:
            row = rows.get((outcome['case'], outcome['pass']))
            counts['not read' if row is None or row_problem(row, outcome) else row['G']] += 1
        report['shares'][f'G, reader {reader_number}'] = dict(counts) if figures else 'no figure'
        parts = collections.Counter()
        for outcome in ladders:
            row = rows.get((outcome['case'], outcome['pass']))
            listed = len(outcome['answer']['ladder']['not_judged'])
            if row is None or row_problem(row, outcome):
                parts['not read'] += listed
            else:
                parts.update(row['B'])
        report['shares'][f'B, reader {reader_number}'] = dict(parts) if parts else 'nothing listed'
    return report
