"""DESIGN.md's decision rule, applied to the probe's reading ($0; judges nothing itself).

Each send's marks are settled as the fortnight's reading settled them (faults_by_topic.py): the two first readers' value where
they agree, the two third readers' ruling where they differ, an unresolved point counted for the answer and then against it. H (the
added field, h-brief.md) is settled per listed part the same way, from `third-reader/h-rulings-<family>-*.jsonl` lines
{"id": "<item>-H-<position>", "ruling": ...}; `cannot_tell` settles nothing. A send fails H when a part settles as
`already_judged` or `settlement`.

  python3 probe_score.py <reading folder> <key path> <plants-expected path>

Refuses to score while any reader row is missing or not valid (H included).
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / 'clean-arch/step4-2026-11-10/stage_a')]
import accounting  # noqa: E402
import collect_readings as collector  # noqa: E402
import probe  # noqa: E402

H_VALUES = ('part', 'already_judged', 'settlement', 'cannot_tell')
HARM = ('already_judged', 'settlement')
OTHER_MARKS = [mark for mark in accounting.RULED_MARKS if mark != 'L'] + ['W', 'H', 'refusal', 'refused twice']
RULE_2_SKIPS = {'recovery': {'refusal'}, 'refusal control': {'refusal'}, 'disputed': set(OTHER_MARKS)}   # N and code refusals still count


def group_of():
    return {f'{source}:{name}': group for group, entries in probe.TOPICS.items() for source, name in entries}


def parts_listed(outcome):
    kind = accounting.kind_of(outcome)
    return 0 if kind in ('refusal', 'refused twice') else len(outcome['answer']['ladder']['not_judged'])


def h_problem(row, outcome):
    value = row.get('H')
    if not isinstance(value, list) or len(value) != parts_listed(outcome) or any(entry not in H_VALUES for entry in value):
        return f'H must hold one of {H_VALUES} for each of the {parts_listed(outcome)} parts listed'
    return None


def h_rulings(reading):
    """{point id: {family: ruling}}. Refuses a line that is not a ruling of one of H's four values, and a point one family rules twice."""
    given = {}
    for family in collector.FAMILIES.values():
        for answer_file in sorted((Path(reading) / 'third-reader').glob(f'h-rulings-{family}-*.jsonl')):
            for line in answer_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('```'):
                    continue
                try:
                    ruling = json.loads(line)
                    point, value = ruling['id'], ruling['ruling']
                except (ValueError, KeyError, TypeError):
                    raise SystemExit(f'NOT SCORED: {answer_file.name}: a line that is not an H ruling: {line[:80]}')
                if value not in H_VALUES:
                    raise SystemExit(f'NOT SCORED: {answer_file.name}: {point} is ruled {value!r}, not one of {H_VALUES}')
                if family in given.get(point, {}):
                    raise SystemExit(f'NOT SCORED: {point} is ruled twice by the {family} family')
                given.setdefault(point, {})[family] = value
    return given


def expected_sends():
    """Every send the reading must hold exactly once: each arm's 18 topics in three passes, and the three plants in pass 1."""
    from reading_prep import PLANTS
    arm_sends = {(f'{arm}|{source}:{name}', n) for arm in probe.ARMS for entries in probe.TOPICS.values() for source, name in entries
                 for n in probe.PASSES}
    return arm_sends | {(plant[0], 1) for plant in PLANTS}


def needs_ruling(first, second):
    """An H point goes to the third readers when the first readers differ or either cannot tell."""
    return first != second or 'cannot_tell' in (first, second)


def settled_h(values, ruled, unresolved_as):
    first = set(values)
    if len(first) == 1 and 'cannot_tell' not in first:
        return values[0]
    third = set(ruled.values())
    if len(ruled) == 2 and len(third) == 1 and 'cannot_tell' not in third:
        return ruled[next(iter(ruled))]
    return 'harm' if unresolved_as == 'fails' else 'part'


def failed_marks(send, outcome, rows, of_family, families, h_given, item, unresolved_as):
    """The marks this send fails under one treatment of unresolved points (L, the ruled marks, W, H, refusal, refused twice)."""
    kind = accounting.kind_of(outcome)
    if kind == 'refused twice':
        return {'refused twice'}
    failed = {'refusal'} if kind == 'refusal' else set()
    empty = {'marks': {}, 'W': {}}
    ruling, _ = accounting.rulings_of_two(of_family[families[0]].get(send, empty), of_family[families[-1]].get(send, empty), unresolved_as) \
        if send in of_family[families[0]] else (empty, [])
    for mark in accounting.marks_that_apply(kind):
        value = rows[0][mark] if rows[0][mark] == rows[1][mark] else ruling['marks'].get(mark, unresolved_as)
        if value == 'fails':
            failed.add(mark)
    for number, row in enumerate(rows, start=1):
        if row['W'].strip() and ruling['W'].get(f'reader {number}', unresolved_as == 'fails'):
            failed.add('W')
    for position in range(parts_listed(outcome)):
        value = settled_h([rows[0]['H'][position], rows[1]['H'][position]], h_given.get(f'{item}-H-{position}', {}), unresolved_as)
        if value in HARM + ('harm',):
            failed.add('H')
    return failed


def refused(failed):
    """Any refusal, the model's or code's: what rule 1 counts against a motivating topic."""
    return bool(failed & {'refusal', 'refused twice'})


def justified_refusal(failed):
    """The model declined and its reason was accepted (N did not settle as failing). A code refusal is not one."""
    return 'refusal' in failed and 'N' not in failed and 'refused twice' not in failed


def correct_written(failed):
    """A written answer with no mark settled as failing (every applicable mark, W and H included)."""
    return not failed


def decide(by_send, unresolved_as, plant_misses):
    """by_send: {(arm, topic, pass): failed marks}. Returns (decision, the numbers it rests on). The refusal-control and recovery rules
    apply only when the configured topics have those groups (DESIGN-A2.md v2)."""
    groups = group_of()
    of_group = lambda name: [topic for topic, group in groups.items() if group == name]
    motivating = of_group('motivating')
    control_l_topics = sum(any('L' in by_send.get(('control', topic, n), set()) for n in (1, 2, 3)) for topic in motivating)
    bad = [(topic, n) for topic in motivating for n in (1, 2, 3)
           if by_send.get(('changed', topic, n), {'refused twice'}) & {'L', 'refusal', 'refused twice'}]
    counts = collections.defaultdict(int)
    for (arm, topic, _), failed in by_send.items():
        for mark in failed & set(OTHER_MARKS):
            counts[(arm, groups[topic], mark)] += 1
    harm = [(group, mark, counts[('changed', group, mark)], counts[('control', group, mark)])
            for group in probe.TOPICS for mark in OTHER_MARKS if mark not in RULE_2_SKIPS.get(group, set())
            and counts[('changed', group, mark)] > counts[('control', group, mark)] + 1]
    sends = lambda arm, topic: [by_send.get((arm, topic, n), {'refused twice'}) for n in (1, 2, 3)]
    exercised = [topic for topic in of_group('refusal control') if sum(map(justified_refusal, sends('control', topic))) >= 2]
    lost = [topic for topic in exercised if sum(map(justified_refusal, sends('changed', topic))) < 2]
    correct = {arm: sum(correct_written(failed) for topic in of_group('recovery') for failed in sends(arm, topic)) for arm in probe.ARMS}
    per_recovery = {topic: {arm: sum(map(correct_written, sends(arm, topic))) for arm in probe.ARMS} for topic in of_group('recovery')}
    numbers = {'control: motivating topics failing L': control_l_topics, 'changed: motivating sends failing L or refused': len(bad),
               'changed: motivating topics failing L or refused': len({topic for topic, _ in bad}),
               'marks other than L where changed exceeds control + 1 (group, mark, changed, control)': harm, 'planted controls missed': plant_misses}
    if of_group('refusal control'):
        numbers.update({'refusal controls the control declines in 2 of 3 or more': exercised,
                        'of them, topics the changed request no longer declines in 2 of 3': lost,
                        'correct written recoveries (control, changed), of 12': (correct['control'], correct['changed']),
                        'correct written answers per recovery topic': per_recovery})
    if plant_misses:
        return 'STOPPED: a planted control was missed; the reading stops until the form is mended', numbers
    if control_l_topics < 3:
        return 'inconclusive', numbers
    recovery_room = 3 * len(of_group('recovery')) - correct['control']
    if of_group('refusal control') and (len(exercised) < 3 or recovery_room < 3):
        return 'inconclusive', numbers
    rule_1 = len({topic for topic, _ in bad}) <= 1 and len(bad) <= 1
    kept = not lost
    gain = not of_group('recovery') or correct['changed'] >= correct['control'] + 3
    return ('lead' if rule_1 and not harm and kept and gain else 'negative'), numbers


def load_reading(reading, key_path, plants_path):
    """Every check main() made before scoring; returns what the scoring reads. Refuses an incomplete or invalid reading."""
    found = [(outcome['case'], outcome['pass']) for outcome in collector.outcomes_of(reading)]
    if len(found) != len(set(found)) or set(found) != expected_sends():
        raise SystemExit(f'NOT SCORED: the reading does not hold each expected send exactly once: missing '
                         f'{sorted(expected_sends() - set(found))[:5]}, unknown {sorted(set(found) - expected_sends())[:5]}, '
                         f'repeated {len(found) - len(set(found))}')
    import reading_prep
    if json.loads(Path(plants_path).read_text()) != reading_prep.plants()[2]:
        raise SystemExit('NOT SCORED: the plants file is not the planted controls reading_prep.py builds')
    key, item_of, outcomes, readers, problems = collector.read_rows(reading, key_path)
    for reader in collector.FAMILIES:
        for send, outcome in outcomes.items():
            row = readers[reader].get(send)
            if accounting.kind_of(outcome) != 'refused twice' and row is not None and accounting.row_problem(row, outcome) is None:
                problem = h_problem(row, outcome)
                if problem:
                    problems[reader]['rows'].append((item_of[send], send, problem))
    bad_rows = {reader: found['rows'] for reader, found in problems.items() if found['rows'] or found['unreadable lines']}
    if bad_rows:
        raise SystemExit(f'NOT SCORED: rows missing or not valid: {bad_rows}')
    families = collector.third_reader_families(reading)
    disputed = collector.disputes_of(outcomes, readers)
    h_points = [send for send, outcome in outcomes.items() if not send[0].startswith('plant|') and accounting.kind_of(outcome) != 'refused twice'
                and any(needs_ruling(readers['reader 1'][send]['H'][n], readers['reader 2'][send]['H'][n]) for n in range(parts_listed(outcome)))]
    both = sorted(collector.FAMILIES.values())
    if disputed and families != both:
        raise SystemExit(f'NOT SCORED: {len(disputed)} differences need both third-reader families; found {families}')
    h_families = sorted(family for family in both if any((Path(reading) / 'third-reader').glob(f'h-rulings-{family}-*.jsonl')))
    if h_points and h_families != both:
        raise SystemExit(f'NOT SCORED: {len(h_points)} sends with H points need both third-reader families; found {h_families}')
    read = {family: collector.read_rulings(reading, item_of, outcomes, readers, family) for family in families}
    missing = {family: found[1] for family, found in read.items() if found[1]}
    if missing:
        raise SystemExit(f'NOT SCORED: third-reader rulings missing: {missing}')
    of_family = {family: found[0] for family, found in read.items()}
    h_given = h_rulings(reading)
    h_missing = [f'{item_of[send]}-H-{position}' for send, outcome in outcomes.items()
                 if not send[0].startswith('plant|') and accounting.kind_of(outcome) != 'refused twice'
                 for position in range(parts_listed(outcome))
                 if needs_ruling(readers['reader 1'][send]['H'][position], readers['reader 2'][send]['H'][position])
                 and len(h_given.get(f'{item_of[send]}-H-{position}', {})) < 2]
    if h_missing:
        raise SystemExit(f'NOT SCORED: H rulings missing for {h_missing}')
    expected = json.loads(Path(plants_path).read_text())
    plant_misses = [(plant, reader, readers[reader][(plant, 1)]['H'][entry['position']], entry['expected'])
                    for plant, entry in expected.items() for reader in collector.FAMILIES
                    if readers[reader][(plant, 1)]['H'][entry['position']] != entry['expected']]
    return outcomes, readers, item_of, of_family, families, h_given, plant_misses


def main(reading, key_path, plants_path):
    outcomes, readers, item_of, of_family, families, h_given, plant_misses = load_reading(reading, key_path, plants_path)
    decisions = {}
    for unresolved_as, label in (('holds', 'unresolved counted for the answer'), ('fails', 'unresolved counted against it')):
        by_send = {}
        for send, outcome in outcomes.items():
            if send[0].startswith('plant|'):
                continue
            arm, topic = send[0].split('|', 1)
            rows = (readers['reader 1'].get(send), readers['reader 2'].get(send))
            by_send[(arm, topic, send[1])] = failed_marks(send, outcome, rows, of_family, families, h_given, item_of.get(send), unresolved_as)
        decisions[label], numbers = decide(by_send, unresolved_as, plant_misses)
        print(f'== {label}: {decisions[label]}')
        for name, value in numbers.items():
            print(f'   {name}: {value}')
        for topic, group in group_of().items():
            line = ' | '.join(f"{arm} p{n}: {','.join(sorted(by_send.get((arm, topic, n), {'missing'}))) or 'ok'}" for arm in ('control', 'changed') for n in (1, 2, 3))
            print(f'   {group:16} {topic:24} {line}')
    recovery = [topic for topic, group in group_of().items() if group == 'recovery']
    if recovery:   # G is reported beside, as gate 1's accounting reports it (accounting.marks_that_apply leaves it out)
        g_fails = {topic: {arm: sum(all((readers[r].get((f'{arm}|{topic}', n)) or {}).get('G') == 'fails' for r in collector.FAMILIES)
                                    for n in probe.PASSES) for arm in probe.ARMS} for topic in recovery}
        print(f'   recovery topics, sends whose ranges both first readers mark G fails (control, changed): {g_fails}')
    verdicts = set(decisions.values())
    print(f'DECISION: {verdicts.pop() if len(verdicts) == 1 else "not settled: the two countings differ"}')
    return 0


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if arguments[:1] == ['--arm']:
        probe.configure(arguments[1])
        arguments = arguments[2:]
    sys.exit(main(*arguments))
