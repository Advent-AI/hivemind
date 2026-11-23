"""The count of Stage B's reading ($0; `STAGE_B_READING.md`; D428), with the baseline count's refusals: it prints a result only for a
complete reading that no condition stops or voids, and takes nothing on trust that it can rebuild (the packets and key are made
again from the run folders and the trial's result, and must equal the files). Its reports mirror the baseline count's
(`baseline_count.py`), and its lines are D428's. Line 3, the control theses, is counted apart (`control_theses.py`).

  python3 clean-arch/step4-2026-11-10/stage_b/stage_b_count.py <reading folder> <key path> <trial key path>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import baseline_count as base  # noqa: E402
import build_baseline  # noqa: E402
import build_stage_b  # noqa: E402
import stage_b_trial  # noqa: E402
import stored_judgements  # noqa: E402

BASELINE_FIGURE = {'unresolved left out': 4 / 52, 'counted SUPPORTED': 4 / 53, 'counted UNSUPPORTED': 5 / 53}   # stage_b/RESULT.md
MARGIN, YES_NO_MOST, LAST_MOST = 0.05, 0.05, 0.10                                                       # D428
SECONDS_A_JUDGEMENT = 51                                                                                 # the design's estimate
DRAWS = ('u1', 'u2', 'u3')
TRIAL_KEY = {}                                                                                           # set by main


def record_problems(folder, key):
    """The record of what was read: the trial's result is derived again from its answers and must be planted-in-use.json; the
    packets and key are made again from the run folders and that result and must equal the files."""
    in_use_file = folder / 'planted-in-use.json'
    if not in_use_file.exists():
        return ['there is no planted-in-use.json: the trial of the planted answers has no result']
    derived, problems = stage_b_trial.trial_result(folder, TRIAL_KEY)
    if problems:
        return [f'the trial: {problem}' for problem in problems]
    if json.loads(in_use_file.read_text()) != derived:
        return ['planted-in-use.json is not the trial\'s result']
    views = build_stage_b.all_views()
    texts, expected_key = build_baseline.rendered(build_stage_b.stage_b_packets(views, {tuple(entry) for entry in derived}), views)
    kinds = collections.Counter(entry['kind'] for entry in expected_key.values())
    if {kind for kind in kinds if kind.startswith('planted')} != set(stage_b_trial.TESTS):
        problems.append("the planted answers in use do not cover each of the form's three tests")
    stored = sorted((entry['draw'], entry['view'], entry['number_in_view']) for entry in expected_key.values() if entry['kind'] == 'stored')
    every = sorted((draw, view_id, index + 1) for (draw, view_id), view in views.items() for index in range(len(view['judgements'])))
    if stored != every or kinds['repeated'] != build_stage_b.REPEATS:
        problems.append('the builder does not make every stored judgement once and the three repeats')
    if json.loads(json.dumps(expected_key)) != key:
        problems.append('the key is not the key of this reading as the builder makes it')
    on_disk = {path.name: path.read_text() for path in (folder / 'readers').glob('*')}
    expected = {f'packet-{number}.json': text for number, text in enumerate(texts, start=1)}
    for name in sorted(set(on_disk) | set(expected)):
        if on_disk.get(name) != expected.get(name):
            problems.append(f'readers/{name} is not the packet the builder makes' if name in expected else f'readers/{name} is not a packet of this reading')
    for entry in key.values():
        entry['not_shown_ids'] = []
    if not problems:
        for text in texts:
            for row in json.loads(text):
                key[str(row['judgement'])]['not_shown_ids'] = [item['evidence_id'] for item in row['not_shown']]
    return problems


def three(counter, part):
    """{reading: (numerator, denominator)} for the share of `part` among decided, the unresolved three ways."""
    decided = counter['SUPPORTED'] + counter['UNSUPPORTED']
    unresolved = counter['unresolved']
    against = part == 'UNSUPPORTED'
    return {'unresolved left out': (counter[part], decided),
            'counted SUPPORTED': (counter[part] + (0 if against else unresolved), decided + unresolved),
            'counted UNSUPPORTED': (counter[part] + (unresolved if against else 0), decided + unresolved)}


def line_shape(entry):
    """D428 compares figures with figures and events with events; an event of two or three rungs counts as yes/no."""
    return 'figure' if entry['shape'] == 'figure' else 'yes/no'


def main():
    global TRIAL_KEY
    for run_folder in stored_judgements.stage_b_folders().values():          # before any read: a split store is refused (DESIGN.md v4)
        stored_judgements.refuse_split_store(stored_judgements.read_only(run_folder / 'views.sqlite'), 'stage_b_count')
    folder, key, TRIAL_KEY = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), json.loads(Path(sys.argv[3]).read_text())
    base.record_problems = record_problems                  # the baseline's reader of rows, sessions and rulings, over Stage B's record
    base.first_row_problem = stage_b_trial.row_problem       # the form's contract, with every field of the form present
    first, third, seconds, problems = base.read(folder, key)
    if problems:
        print(f'INCOMPLETE: {len(problems)} problems; no result is printed')
        for problem in problems[:40]:
            print('  ', problem)
        raise SystemExit(2)

    def verdict_of(number):
        pair = [first[family][int(number)]['verdict'] for family in base.FAMILIES]
        if pair[0] == pair[1]:
            return pair[0], 'both first readers'
        rulings = [third[family][int(number)]['verdict'] for family in base.FAMILIES]
        return (rulings[0], 'both third readers') if rulings[0] == rulings[1] else ('unresolved', 'the third readers part')

    stored = {number: entry for number, entry in key.items() if entry['kind'] == 'stored'}
    planted = {number: entry for number, entry in key.items() if entry['kind'].startswith('planted')}
    void = []
    print(f"== the reading: {len({entry['packet'] for entry in key.values()})} packets, {len(key)} judgements read by each family")
    print('== controls')
    if not planted:
        void.append('NOT MEASURED: no planted answer passed the trial, so the readers are untested')
    for family in base.FAMILIES:
        caught = [number for number in planted if first[family][int(number)]['verdict'] == 'UNSUPPORTED']
        print(f'{family}: planted caught {len(caught)} of {len(planted)}')
        if (len(planted) - len(caught)) * 5 > len(planted):
            void.append(f'NOT MEASURED: {family} missed {len(planted) - len(caught)} of the {len(planted)} planted answers, more than one in five; the family is not used')
    for number, entry in planted.items():
        pair = {family: (first[family][int(number)]['verdict'], first[family][int(number)].get('rung_the_evidence_points_to')) for family in base.FAMILIES}
        print(f"   {entry['kind']} ({entry['draw']} {entry['view']} #{entry['number_in_view']}, stored rung {entry['stored_rung']}, shown {entry['shown_rung']}): {pair}")
        named_right = [family for family in base.FAMILIES if pair[family] == ('UNSUPPORTED', entry['stored_rung'])]
        if len(named_right) < len(base.FAMILIES):
            print(f"      (UNSUPPORTED with the stored rung named: {named_right or 'neither family'})")
        if all(value[0] != 'UNSUPPORTED' for value in pair.values()):
            void.append(f"STOPPED: the planted answer {entry['draw']} {entry['view']} #{entry['number_in_view']} was missed by both families")
    for number, entry in key.items():
        if entry['kind'] == 'repeated':
            twin = next(other for other, other_entry in stored.items() if (other_entry['draw'], other_entry['view'], other_entry['number_in_view']) == (entry['draw'], entry['view'], entry['number_in_view']))
            print(f"   repeated ({entry['draw']} {entry['view']} #{entry['number_in_view']}), as a stored judgement / as a control: " + '; '.join(f"{family} {first[family][int(twin)]['verdict']} / {first[family][int(number)]['verdict']}" for family in base.FAMILIES))
    estimate = SECONDS_A_JUDGEMENT * len(key)
    for family in base.FAMILIES:
        print(f'{family}: sessions took {seconds[family] / 3600:.1f} hours in all (estimate {estimate / 3600:.1f})')
        if seconds[family] > 2 * estimate:
            void.append(f'NOT MEASURED: the {family} reading took {seconds[family] / 3600:.1f} hours, more than twice its estimate')
    apart = base.differing(first, stored)
    print(f'== the two families differ on {len(apart)} of {len(stored)} stored judgements')
    if len(apart) * 3 > len(stored):
        void.append(f'NOT MEASURED: the two families differ on {len(apart)} of {len(stored)} verdicts, more than a third')
    groups, how, last, last_lines = collections.defaultdict(collections.Counter), collections.Counter(), collections.Counter(), []
    for number, entry in sorted(stored.items(), key=lambda pair: (pair[1]['draw'], int(pair[1]['view'][1:]), pair[1]['number_in_view'])):
        verdict, source = verdict_of(number)
        how[source] += 1
        for group in ('all', f"draw {entry['draw']}", f"shape {entry['shape']}", f"line {line_shape(entry)}"):
            groups[group][verdict] += 1
        if entry['last_of_view']:
            last[verdict] += 1
            last_lines.append(f"   {entry['draw']} {entry['view']:4s} {entry['shape']:6s} day {entry['day']} rung {entry['stored_rung']}: {verdict} ({source})")
    decided = groups['all']['SUPPORTED'] + groups['all']['UNSUPPORTED']
    if decided < base.FEWEST_DECIDED:
        void.append(f'NOT MEASURED: {decided} decided judgements, fewer than {base.FEWEST_DECIDED}')
    for name, counter in (('the figure line', groups['line figure']), ('the yes/no line', groups['line yes/no']), ('the last-judgement line', last)):
        if counter['SUPPORTED'] + counter['UNSUPPORTED'] == 0:
            void.append(f'NOT MEASURED: {name} has no decided judgement (a zero denominator)')
    record = json.loads((stored_judgements.STAGE_B / 'run.json').read_text())
    laddered = judged = 0
    per_draw = []
    for draw, run_folder in stored_judgements.stage_b_folders().items():
        connection = stored_judgements.read_only(run_folder / 'views.sqlite')
        draw_laddered = connection.execute("select count(*) from clean_ladders where status = 'ladder'").fetchone()[0]
        draw_judged = connection.execute('select count(distinct view_id) from judgements').fetchone()[0]
        per_draw.append(f'{draw} {draw_judged} of {draw_laddered}')
        laddered, judged = laddered + draw_laddered, judged + draw_judged
    if laddered == 0:
        void.append('NOT MEASURED: line 2 has no laddered thesis (a zero denominator)')
    if void:
        print('== RESULT')
        for line in void:
            print(line)
        print('No share is printed.')
        raise SystemExit(3)
    print('== verdicts decided by:', dict(how))
    for group in sorted(groups):
        counter = groups[group]
        print(f"{group:14s} {sum(counter.values()):3d}: SUPPORTED {counter['SUPPORTED']}, UNSUPPORTED {counter['UNSUPPORTED']}, INSUFFICIENT {counter['INSUFFICIENT']}, unresolved {counter['unresolved']}")
        print(f"{'':19s}UNSUPPORTED among decided ({group}): {base.three_ways(counter['UNSUPPORTED'], counter['SUPPORTED'] + counter['UNSUPPORTED'], counter['unresolved'], 'against')}")
    print('== the last judgement of each question')
    print('\n'.join(last_lines))
    print('== the lines (D428)')
    print(f"line 1, no draw incomplete: {'met' if all(record.get(draw, {}).get('state') == 'complete' for draw in DRAWS) else 'MISSED'}")
    print(f"line 2, nine in ten laddered theses judged: {judged} of {laddered} ({', '.join(per_draw)}): {'met' if judged * 10 >= laddered * 9 else 'MISSED'}")
    for name, counter, limit_of in (('figure', groups['line figure'], lambda reading: BASELINE_FIGURE[reading] + MARGIN),
                                    ('yes/no', groups['line yes/no'], lambda reading: YES_NO_MOST),
                                    ('last judgements', last, lambda reading: LAST_MOST)):
        print(f"{name}: SUPPORTED {counter['SUPPORTED']}, UNSUPPORTED {counter['UNSUPPORTED']}, INSUFFICIENT {counter['INSUFFICIENT']} (beside), unresolved {counter['unresolved']}")
        for reading, (numerator, denominator) in three(counter, 'UNSUPPORTED').items():
            share = numerator / denominator
            print(f"   {reading}: UNSUPPORTED {numerator}/{denominator} ({100 * share:.1f}%) against at most {100 * limit_of(reading):.1f}%: "
                  f"{'met' if share <= limit_of(reading) + 1e-12 else 'MISSED'}")
    print('line 3 (the control theses) is counted by control_theses.py')
    print('== other marks on the stored judgements, by family (no line)')
    for family in base.FAMILIES:
        rows = [first[family][int(number)] for number in stored]
        print(f"{family}: verdicts {dict(collections.Counter(row['verdict'] for row in rows))}; reasoning_flaw {dict(collections.Counter(row['reasoning_flaw'] for row in rows))}; "
              f"arithmetic wrong {sum(1 for row in rows if row['arithmetic'] == 'wrong')}; reference fails {sum(1 for row in rows if row['reference'] == 'fails')}; "
              f"implied_outcome fails {sum(1 for row in rows if row['implied_outcome'] == 'fails')}; E named on {sum(1 for row in rows if row['E'] != 'none')}")


if __name__ == '__main__':
    main()
