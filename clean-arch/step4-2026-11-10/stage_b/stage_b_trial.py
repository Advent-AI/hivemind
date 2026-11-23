"""The trial of Stage B's planted answers ($0; `STAGE_B_READING.md`): which of the six both families call UNSUPPORTED, naming the
stored rung. It takes nothing on trust it can rebuild: the trial packets and key are made again by the builder and must equal the
files; the session record (`sessions-trial.json`) must show one returned session a packet and family, after at most one stopped;
every answer file must hold each judgement of its packet once, each row complete and in the form's contract. The planted
answers in use must cover each of the form's three tests, or the reading cannot start. `stage_b_count.py` calls `trial_result`
again and refuses a `planted-in-use.json` that is not its result.

  python3 clean-arch/step4-2026-11-10/stage_b/stage_b_trial.py <data folder> <trial key path>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import baseline_count as base  # noqa: E402
import build_baseline  # noqa: E402
import build_stage_b  # noqa: E402

FORM_FIELDS = {'judgement', 'verdict', 'rung_the_evidence_points_to', 'reasoning_flaw', 'arithmetic', 'reference', 'implied_outcome', 'E', 'why'}
TESTS = ('planted test 1', 'planted test 2', 'planted test 3')
BASELINE_ROW_PROBLEM = base.first_row_problem          # kept at import: stage_b_count.py puts row_problem in its place


def row_problem(row, entry):
    """The form's contract (`baseline_count.first_row_problem`), every field of the form present, a rung that is null or a rung of the
    ladder, and a reason that is text (empty where the form asks for none)."""
    if row is not None:
        if set(row) != FORM_FIELDS:
            return f'fields {sorted(row)}, not the form\'s {sorted(FORM_FIELDS)}'
        rung = row['rung_the_evidence_points_to']
        if rung is not None and not (type(rung) is int and 1 <= rung <= entry['rung_count']):
            return f'rung_the_evidence_points_to is {rung!r}'
        if not isinstance(row['why'], str):
            return f'why is {row["why"]!r}, not text'
    return BASELINE_ROW_PROBLEM(row, entry)


def trial_result(folder, trial_key):
    """(the planted answers in use as [draw, view, number], problems). The planted answers are in use only when there is no problem."""
    folder = Path(folder)
    views = build_stage_b.all_views()
    texts, expected_key = build_baseline.rendered(build_stage_b.validation_packets(views), views)
    problems = []
    if json.loads(json.dumps(expected_key)) != trial_key:
        problems.append('the trial key is not the key the builder makes')
    on_disk = {path.name: path.read_text() for path in (folder / 'validation').glob('*')}
    expected = {f'packet-{number}.json': text for number, text in enumerate(texts, start=1)}
    for name in sorted(set(on_disk) | set(expected)):
        if on_disk.get(name) != expected.get(name):
            problems.append(f'validation/{name} is not the trial packet the builder makes' if name in expected else f'validation/{name} is not a trial packet')
    log_file = folder / 'sessions-trial.json'
    log = json.loads(log_file.read_text()) if log_file.exists() else {}
    for family in base.FAMILIES:
        for number in range(1, len(texts) + 1):
            attempts = log.get(family, {}).get(str(number))
            sound = (isinstance(attempts, list) and 1 <= len(attempts) <= base.MOST_ATTEMPTS
                     and all(isinstance(attempt, dict) and isinstance(attempt.get('seconds'), (int, float)) and attempt['seconds'] >= 0 for attempt in attempts)
                     and [attempt.get('outcome') for attempt in attempts] == ['stopped'] * (len(attempts) - 1) + ['returned'])
            if not sound:
                problems.append(f'{family}: trial packet {number} has no sound record of a fresh session that returned (sessions-trial.json)')
    if problems:
        return [], problems
    for entry in trial_key.values():
        entry['not_shown_ids'] = []
    for text in texts:
        for row in json.loads(text):
            trial_key[str(row['judgement'])]['not_shown_ids'] = [item['evidence_id'] for item in row['not_shown']]
    rows = {family: {} for family in base.FAMILIES}
    for family in base.FAMILIES:
        for number in range(1, len(texts) + 1):
            path = folder / 'validation-answers' / f'reader-{family}-packet-{number}.jsonl'
            if not path.exists():
                problems.append(f'{family}: no answers for trial packet {number}')
                continue
            found, bad = base.rows_in(path)
            problems += [f'{family}: {problem}' for problem in bad]
            in_packet = {int(judgement) for judgement, entry in trial_key.items() if entry['packet'] == number}
            if set(found) != in_packet:
                problems.append(f'{family}: {path.name} does not hold exactly the judgements of trial packet {number}')
            rows[family].update({judgement: row for judgement, row in found.items() if judgement in in_packet})
        extra = [path.name for path in (folder / 'validation-answers').glob(f'reader-{family}-*')
                 if path.name not in {f'reader-{family}-packet-{number}.jsonl' for number in range(1, len(texts) + 1)} and path.suffix == '.jsonl']
        problems += [f'{family}: {name} is not a trial answer file' for name in extra]
        problems += [f'{family}: trial judgement {number}: {problem}' for number, entry in trial_key.items()
                     for problem in [row_problem(rows[family].get(int(number)), entry)] if problem]
    if problems:
        return [], problems
    in_use, covered = [], set()
    for number, entry in sorted(trial_key.items(), key=lambda pair: int(pair[0])):
        if entry['kind'].startswith('planted') and all((rows[family][int(number)]['verdict'], rows[family][int(number)]['rung_the_evidence_points_to'])
                                                       == ('UNSUPPORTED', entry['stored_rung']) for family in base.FAMILIES):
            in_use.append([entry['draw'], entry['view'], entry['number_in_view']])
            covered.add(entry['kind'])
    uncovered = [test for test in TESTS if test not in covered]
    if uncovered:
        problems.append(f'no planted answer under {uncovered} passed the trial: the reading cannot start until the planted answers are mended')
    return in_use, problems


def main():
    folder, trial_key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    in_use, problems = trial_result(folder, trial_key)
    rows = {family: {} for family in base.FAMILIES}
    for family in base.FAMILIES:
        for path in sorted((folder / 'validation-answers').glob(f'reader-{family}-packet-*.jsonl')):
            rows[family].update(base.rows_in(path)[0])
    for number, entry in sorted(trial_key.items(), key=lambda pair: int(pair[0])):
        pair = {family: (rows[family].get(int(number), {}).get('verdict'), rows[family].get(int(number), {}).get('rung_the_evidence_points_to')) for family in base.FAMILIES}
        print(f"{number:>2} {entry['kind']:15s} {entry['draw']} {entry['view']:4s} #{entry['number_in_view']:<2} stored rung {entry['stored_rung']}, shown {entry['shown_rung']}: {pair}")
        for family in base.FAMILIES:
            row = rows[family].get(int(number), {})
            if row.get('verdict') not in (None, 'SUPPORTED'):
                print(f"      {family}: {str(row.get('why', ''))[:400]}")
    if problems:
        print(f'NOT USABLE: {len(problems)} problems; planted-in-use.json is not written')
        for problem in problems[:30]:
            print('  ', problem)
        raise SystemExit(2)
    target = folder / 'planted-in-use.json'
    text = json.dumps(in_use) + '\n'
    if target.exists() and target.read_text() != text:
        raise SystemExit('planted-in-use.json exists with another result')
    target.write_text(text)
    print(f'{len(in_use)} of 6 planted answers pass the trial, covering each of the three tests; written to planted-in-use.json')


if __name__ == '__main__':
    main()
