"""The count of the Stage B baseline reading ($0), written before any reader's row exists (`BASELINE.md`).

It prints a result only when the reading is complete and no condition of the plan stops or voids it; otherwise it says
which, and prints no share. It takes nothing on trust that it can rebuild: the packets on disk must equal the packets the
builder makes from the stored runs and the trial's result, every answer file must hold exactly its packet's judgements,
and the session log must show a returned session for every packet.

  python3 clean-arch/step4-2026-11-10/stage_b/baseline_count.py <data folder> <key path>
"""
import collections
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_baseline  # noqa: E402
import stored_judgements  # noqa: E402

FAMILIES = ('codex', 'claude')
VERDICTS = ('SUPPORTED', 'UNSUPPORTED', 'INSUFFICIENT')
ALLOWED = {'reasoning_flaw': ('none', 'does_not_change_the_rung', 'changes_the_rung'), 'arithmetic': ('right', 'wrong', 'none'),
           'reference': ('holds', 'fails'), 'implied_outcome': ('holds', 'fails')}
FEWEST_DECIDED = 30
ESTIMATED_SECONDS_A_FAMILY = 9000        # the design's 51 seconds a judgement over the 168 read, 2.4 hours, taken as 2.5
MOST_ATTEMPTS = 2
MOST_SECONDS_A_SESSION = 3600


def rows_in(answer_file):
    """({judgement: row}, problems) of one file: a line that is not a row, and a judgement given twice, are problems."""
    rows, problems = {}, []
    for line_number, line in enumerate(answer_file.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
            number = int(row['judgement'])
        except (ValueError, KeyError, TypeError):
            problems.append(f'{answer_file.name} line {line_number}: not a row')
            continue
        if number in rows:
            problems.append(f'{answer_file.name}: judgement {number} given twice')
        rows[number] = row
    return rows, problems


def rung_problem(row, entry, null_allowed=False):
    """An UNSUPPORTED verdict names the rung the evidence points to: a rung of the ladder, other than the one shown. It may
    be null where the form's second test decides (an answer moved by a step the rules do not allow, and what remains leads
    to no rung): for a first reader, a flaw that changes the rung; for a third reader, whose form has no flaw field, always."""
    rung = row.get('rung_the_evidence_points_to')
    if rung is None and null_allowed:
        return None
    if type(rung) is not int or not 1 <= rung <= entry['rung_count']:
        return f'UNSUPPORTED with rung_the_evidence_points_to {rung!r}'
    if rung == entry['shown_rung']:
        return 'UNSUPPORTED naming the rung the answer chose'
    return None


def first_row_problem(row, entry):
    if row is None:
        return 'no row'
    if row.get('verdict') not in VERDICTS:
        return 'no valid verdict'
    for field, allowed in ALLOWED.items():
        if row.get(field) not in allowed:
            return f'{field} is {row.get(field)!r}'
    second_test = row['reasoning_flaw'] == 'changes_the_rung'
    if row['verdict'] == 'UNSUPPORTED' and rung_problem(row, entry, null_allowed=second_test):
        return rung_problem(row, entry, null_allowed=second_test)
    if row['reasoning_flaw'] == 'changes_the_rung' and row['verdict'] != 'UNSUPPORTED':
        return 'a flaw that changes the rung without the verdict UNSUPPORTED'
    named = row.get('E')
    if named != 'none' and not (isinstance(named, list) and named and all(item in entry['not_shown_ids'] for item in named)):
        return f'E is {named!r}, not "none" or ids of the evidence not shown'
    needs_reason = (row['verdict'] != 'SUPPORTED' or row['reasoning_flaw'] != 'none' or row['arithmetic'] == 'wrong'
                    or 'fails' in (row['reference'], row['implied_outcome']))
    if needs_reason and not (isinstance(row.get('why'), str) and row['why'].strip()):
        return 'no reason given'
    return None


def third_row_problem(row, entry):
    if row is None or row.get('verdict') not in VERDICTS:
        return 'no valid ruling'
    if row['verdict'] == 'UNSUPPORTED' and rung_problem(row, entry, null_allowed=True):
        return rung_problem(row, entry, null_allowed=True)
    if not (isinstance(row.get('why'), str) and row['why'].strip()):
        return 'no reason given'
    return None


def record_problems(folder, key):
    """What is wrong with the packets and the key as the record of what was read. The reading's packets and key are made
    again from the stored runs and the planted answers that passed the trial; the packet files on disk must be those files,
    text for text and no other, and the key must be that key. Sets each entry's `not_shown_ids`."""
    in_use_file = folder / 'planted-in-use.json'
    if not in_use_file.exists():
        return ['there is no planted-in-use.json: the trial of the planted answers has no result']
    in_use = {tuple(name) for name in json.loads(in_use_file.read_text())}
    views = {(view['draw'], view['view']): view for draw in stored_judgements.DRAWS for view in stored_judgements.views_of(draw)}
    texts, expected_key = build_baseline.rendered(build_baseline.reading_packets(views, in_use), views)
    problems = []
    kinds = collections.Counter(entry['kind'] for entry in expected_key.values())
    if len({kind for kind in kinds if kind.startswith('planted')}) != 3:
        problems.append(f"the planted answers in use cover {sorted(kind for kind in kinds if kind.startswith('planted'))}, not each of the form's three tests")
    stored = [(entry['draw'], entry['view'], entry['number_in_view']) for entry in expected_key.values() if entry['kind'] == 'stored']
    every = {(draw, view_id, index + 1) for (draw, view_id), view in views.items() for index in range(len(view['judgements']))}
    if sorted(stored) != sorted(every) or kinds['repeated'] != len(build_baseline.REPEATED):
        problems.append('the builder does not make every stored judgement once and the three repeats')
    if json.loads(json.dumps(expected_key)) != key:
        problems.append('the key is not the key of this reading: the stored judgements, the planted answers that passed the trial and the repeats, as the builder numbers them')
    on_disk = {packet_file.name: packet_file.read_text() for packet_file in (folder / 'readers').glob('*')}
    expected_files = {f'packet-{number}.json': text for number, text in enumerate(texts, start=1)}
    for name in sorted(set(on_disk) | set(expected_files)):
        if on_disk.get(name) != expected_files.get(name):
            problems.append(f'readers/{name} is not the packet the builder makes' if name in expected_files else f'readers/{name} is not a packet of this reading')
    for number, entry in key.items():
        entry['not_shown_ids'] = []
    if not problems:
        for text in texts:
            for row in json.loads(text):
                key[str(row['judgement'])]['not_shown_ids'] = [item['evidence_id'] for item in row['not_shown']]
    return problems


def session_problems(folder, packets):
    """(problems, seconds a family): the session log must show, for every packet and family, one or two attempts, the last
    of them returned and any earlier one stopped, each with its time. The log is the operator's record."""
    log_file = folder / 'sessions.json'
    log = json.loads(log_file.read_text()) if log_file.exists() else {}
    problems, seconds = [], {}
    for family in FAMILIES:
        logged = log.get(family, {})
        seconds[family] = 0.0
        for unknown in sorted(set(logged) - {str(packet) for packet in packets}):
            problems.append(f'{family}: the session log names packet {unknown}, which the reading does not have')
        for packet in packets:
            attempts = logged.get(str(packet))
            sound = (isinstance(attempts, list) and 1 <= len(attempts) <= MOST_ATTEMPTS
                     and all(isinstance(attempt, dict) and attempt.get('outcome') in ('returned', 'stopped')
                             and type(attempt.get('seconds')) in (int, float) and math.isfinite(attempt['seconds']) and attempt['seconds'] >= 0 for attempt in attempts))
            if not sound:
                problems.append(f'{family}: packet {packet} has no sound record of its sessions')
                continue
            seconds[family] += sum(attempt['seconds'] for attempt in attempts)
            if any(attempt['outcome'] == 'returned' and attempt['seconds'] > MOST_SECONDS_A_SESSION for attempt in attempts):
                problems.append(f'{family}: packet {packet} has a session that returned after more than {MOST_SECONDS_A_SESSION // 60} minutes; the plan stops it and runs it again')
            outcomes = [attempt['outcome'] for attempt in attempts]
            if outcomes[-1] != 'returned':
                problems.append(f'{family}: packet {packet} failed {len(attempts)} time(s) and was not read')
            elif outcomes[:-1] != ['stopped'] * (len(outcomes) - 1):
                problems.append(f'{family}: packet {packet} has two returned sessions; one reading a packet is the plan')
    return problems, seconds


def read(folder, key):
    """(first rows, third rows, seconds a family, problems that make the reading incomplete)."""
    first, third = {family: {} for family in FAMILIES}, {family: {} for family in FAMILIES}
    problems = record_problems(folder, key)
    packets = sorted({entry['packet'] for entry in key.values()})
    found, seconds = session_problems(folder, packets)
    problems += found
    if problems:
        return first, third, seconds, problems
    in_packet = collections.defaultdict(set)
    for number, entry in key.items():
        in_packet[entry['packet']].add(int(number))
    for family in FAMILIES:
        expected_files = {f'reader-{family}-packet-{packet}.jsonl': packet for packet in packets}
        for answer_file in sorted((folder / 'readers-answers').glob(f'reader-{family}-packet-*.jsonl')):
            if answer_file.name not in expected_files:
                problems.append(f'{family}: {answer_file.name} is not a packet of this reading')
                continue
            rows, found = rows_in(answer_file)
            problems += [f'{family}: {problem}' for problem in found]
            packet = expected_files[answer_file.name]
            if set(rows) != in_packet[packet]:
                problems.append(f'{family}: {answer_file.name} does not hold exactly the judgements of packet {packet}')
            first[family].update({number: row for number, row in rows.items() if number in in_packet[packet]})
        problems += [f'{family}: judgement {number}: {problem}' for number, entry in key.items() for problem in [first_row_problem(first[family].get(int(number)), entry)] if problem]
        for ruling_file in sorted((folder / 'third-reader').glob(f'rulings-{family}-*.jsonl')):
            rows, found = rows_in(ruling_file)
            problems += [f'{family} third reader: {problem}' for problem in found]
            problems += [f'{family} third reader: judgement {number} ruled in two files' for number in rows if number in third[family]]
            third[family].update(rows)
    if not problems:
        apart = differing(first, key)
        for family in FAMILIES:
            problems += [f'{family} third reader: judgement {number}: {problem}' for number in apart for problem in [third_row_problem(third[family].get(int(number)), key[number])] if problem]
            problems += [f'{family} third reader: a ruling for judgement {number}, on which the first readers do not differ' for number in third[family] if str(number) not in apart]
    if not problems:                               # the author's own read of every stored judgement any reader, first or third, calls UNSUPPORTED
        to_read = sorted(int(number) for number, entry in key.items() if entry['kind'] == 'stored'
                         and any(readers[family].get(int(number), {}).get('verdict') == 'UNSUPPORTED' for readers in (first, third) for family in FAMILIES))
        own_file = folder / 'own-read.jsonl'
        own, found = rows_in(own_file) if own_file.exists() else ({}, [])
        problems += [f'own read: {problem}' for problem in found]
        unread = [number for number in to_read if own.get(number, {}).get('verdict') not in VERDICTS or not (isinstance(own[number].get('why'), str) and own[number]['why'].strip())]
        if unread:
            problems.append(f"the author's own read (own-read.jsonl) lacks a verdict with its reason for the stored judgements a reader, first or third, calls UNSUPPORTED: {unread}")
    return first, third, seconds, problems


def differing(first, key):
    """The judgement numbers on which the two families' verdicts differ."""
    return [number for number in key if first['codex'][int(number)]['verdict'] != first['claude'][int(number)]['verdict']]


def three_ways(part, decided, unresolved, part_grows):
    """A share with the unresolved left out, counted SUPPORTED, counted UNSUPPORTED."""
    def share(numerator, denominator):
        return f'{numerator}/{denominator} ({100 * numerator / denominator:.0f}%)' if denominator else 'no denominator'
    whole = decided + unresolved
    return (f'unresolved left out {share(part, decided)}; counted SUPPORTED {share(part + (0 if part_grows == "against" else unresolved), whole)}; '
            f'counted UNSUPPORTED {share(part + (unresolved if part_grows == "against" else 0), whole)}')


def main():
    folder, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
    first, third, seconds, problems = read(folder, key)
    if problems:
        print(f'INCOMPLETE: {len(problems)} problems; no result is printed')
        for problem in problems[:40]:
            print('  ', problem)
        raise SystemExit(2)

    def verdict_of(number):
        pair = [first[family][int(number)]['verdict'] for family in FAMILIES]
        if pair[0] == pair[1]:
            return pair[0], 'both first readers'
        rulings = [third[family][int(number)]['verdict'] for family in FAMILIES]
        return (rulings[0], 'both third readers') if rulings[0] == rulings[1] else ('unresolved', 'the third readers part')

    stored = {number: entry for number, entry in key.items() if entry['kind'] == 'stored'}
    planted = {number: entry for number, entry in key.items() if entry['kind'].startswith('planted')}
    void = []
    print(f"== the reading: {len({entry['packet'] for entry in key.values()})} packets, {len(key)} judgements read by each family")
    print('== controls')
    for family in FAMILIES:
        caught = [number for number in planted if first[family][int(number)]['verdict'] == 'UNSUPPORTED']
        print(f'{family}: planted caught {len(caught)} of {len(planted)}')
        if (len(planted) - len(caught)) * 5 > len(planted):
            void.append(f'NOT MEASURED: {family} missed {len(planted) - len(caught)} of the {len(planted)} planted answers, more than one in five; the family is not used')
    for number, entry in planted.items():
        pair = {family: (first[family][int(number)]['verdict'], first[family][int(number)].get('rung_the_evidence_points_to')) for family in FAMILIES}
        print(f"   {entry['kind']} ({entry['draw']} {entry['view']} #{entry['number_in_view']}, stored rung {entry['stored_rung']}, shown {entry['shown_rung']}): {pair}")
        named_right = [family for family in FAMILIES if pair[family] == ('UNSUPPORTED', entry['stored_rung'])]
        if len(named_right) < len(FAMILIES):
            print(f"      (UNSUPPORTED with the stored rung named: {named_right or 'neither family'})")
        if all(value[0] != 'UNSUPPORTED' for value in pair.values()):
            void.append(f"STOPPED: the planted answer {entry['draw']} {entry['view']} #{entry['number_in_view']} was missed by both families")
    for number, entry in key.items():
        if entry['kind'] == 'repeated':
            twin = next(other for other, other_entry in stored.items() if (other_entry['draw'], other_entry['view'], other_entry['number_in_view']) == (entry['draw'], entry['view'], entry['number_in_view']))
            print(f"   repeated ({entry['draw']} {entry['view']} #{entry['number_in_view']}), as a stored judgement / as a control: " + '; '.join(f"{family} {first[family][int(twin)]['verdict']} / {first[family][int(number)]['verdict']}" for family in FAMILIES))
    for family in FAMILIES:
        print(f'{family}: sessions took {seconds[family] / 3600:.1f} hours in all (estimate {ESTIMATED_SECONDS_A_FAMILY / 3600:.1f})')
        if seconds[family] > 2 * ESTIMATED_SECONDS_A_FAMILY:
            void.append(f'NOT MEASURED: the {family} reading took {seconds[family] / 3600:.1f} hours, more than twice its estimate')
    apart = differing(first, stored)
    print(f'== the two families differ on {len(apart)} of {len(stored)} stored judgements')
    if len(apart) * 3 > len(stored):
        void.append(f'NOT MEASURED: the two families differ on {len(apart)} of {len(stored)} verdicts, more than a third')
    groups, how = collections.defaultdict(collections.Counter), collections.Counter()
    for number, entry in stored.items():
        verdict, source = verdict_of(number)
        how[source] += 1
        for group in ('all', f"draw {entry['draw']}", f"shape {entry['shape']}"):
            groups[group][verdict] += 1
    decided = groups['all']['SUPPORTED'] + groups['all']['UNSUPPORTED']
    if decided < FEWEST_DECIDED:
        void.append(f'NOT MEASURED: {decided} decided judgements, fewer than {FEWEST_DECIDED}')
    last, last_lines = collections.Counter(), []
    for number, entry in sorted(stored.items(), key=lambda pair: (pair[1]['draw'], pair[1]['view'])):
        if entry['last_of_view']:
            verdict, source = verdict_of(number)
            last[verdict] += 1
            last_lines.append(f"   {entry['draw']} {entry['view']:4s} {entry['shape']:6s} day {entry['day']} rung {entry['stored_rung']}: {verdict} ({source})")
    if last['SUPPORTED'] + last['UNSUPPORTED'] == 0:
        void.append('NOT MEASURED: no question has a decided last judgement')
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
        print(f"{'':19s}UNSUPPORTED among decided ({group}): {three_ways(counter['UNSUPPORTED'], counter['SUPPORTED'] + counter['UNSUPPORTED'], counter['unresolved'], 'against')}")
    print('== the last judgement of each question')
    print('\n'.join(last_lines))
    print(f"   SUPPORTED {last['SUPPORTED']}, UNSUPPORTED {last['UNSUPPORTED']}, INSUFFICIENT {last['INSUFFICIENT']}, unresolved {last['unresolved']}")
    print(f"   SUPPORTED among decided last judgements: {three_ways(last['SUPPORTED'], last['SUPPORTED'] + last['UNSUPPORTED'], last['unresolved'], 'for')}")
    print('== other marks on the stored judgements, by family (no line)')
    for family in FAMILIES:
        rows = [first[family][int(number)] for number in stored]
        print(f"{family}: verdicts {dict(collections.Counter(row['verdict'] for row in rows))}; reasoning_flaw {dict(collections.Counter(row['reasoning_flaw'] for row in rows))}; "
              f"arithmetic wrong {sum(1 for row in rows if row['arithmetic'] == 'wrong')}; reference fails {sum(1 for row in rows if row['reference'] == 'fails')}; "
              f"implied_outcome fails {sum(1 for row in rows if row['implied_outcome'] == 'fails')}; E named on {sum(1 for row in rows if row['E'] != 'none')}")


if __name__ == '__main__':
    main()
