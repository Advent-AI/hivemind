"""FRESH-A2-DESIGN.md v4's report and decision ($0; judges nothing itself).

  python3 fresh_score.py <cases.json> <population.json> <reading folder> <key path> <plants-expected path>

population.json: {"population_a": [...], "population_b": [...]} (b within a), written before any answer was read.
Prints, for each arm and each counting of unresolved points, the unchanged gate-1 report on population (a) (line 5's 35 of 44 and
28 of 44 are not applicable to this population), then the comparison on each population, then the decision. A trace review
(`<reading>/fresh/trace-review.json`, {"<topic>|<pass>|<mark>": class}) classes every send where A2 fails a mark, H and L aside, that
the control fails in none of its sends of the same topic; until it exists a lead is PROVISIONAL.
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent)]
import fresh_probe  # noqa: E402
import probe_score as ps  # noqa: E402

CLASSES = ('consistent with the change', 'pre-existing', 'uncertain')


def failing(loaded, counting):
    outcomes, readers, item_of, of_family, families, h_given, _ = loaded
    return {send: ps.failed_marks(send, outcome, (readers['reader 1'].get(send), readers['reader 2'].get(send)), of_family, families,
                                  h_given, item_of.get(send), counting)
            for send, outcome in outcomes.items() if not send[0].startswith('plant|')}


def comparison(failed, population):
    topic_of = lambda send: send[0].split('|', 1)[1].split(':', 1)[1]
    arm_of = lambda send: send[0].split('|', 1)[0]
    of = lambda arm: {send: marks for send, marks in failed.items() if arm_of(send) == arm and topic_of(send) in population}
    l_topics = {arm: sorted({topic_of(send) for send, marks in of(arm).items() if 'L' in marks}) for arm in ('control', 'changed')}
    n_sends = {arm: sum('N' in marks for marks in of(arm).values()) for arm in ('control', 'changed')}
    control_marks = collections.defaultdict(set)
    for send, marks in of('control').items():
        control_marks[topic_of(send)] |= marks
    to_review = sorted(f'{topic_of(send)}|{send[1]}|{mark}' for send, marks in of('changed').items()
                       for mark in marks - {'H', 'L'} if mark not in control_marks[topic_of(send)])
    h = {arm: sorted(f'{topic_of(send)} p{send[1]}' for send, marks in of(arm).items() if 'H' in marks) for arm in ('control', 'changed')}
    return {'n': len(population), 'L topics (control, A2)': (l_topics['control'], l_topics['changed']),
            'N sends (control, A2)': (n_sends['control'], n_sends['changed']), 'A2 failures to review': to_review, 'H sends (control, A2)': (h['control'], h['changed'])}


def verdict(numbers, review):
    control_l, a2_l = (len(topics) for topics in numbers['L topics (control, A2)'])
    if numbers['n'] < 5 or control_l < 2:
        return 'no verdict (not exercised)'
    if not (a2_l < control_l and a2_l <= 1) or numbers['N sends (control, A2)'][1] > numbers['N sends (control, A2)'][0]:
        return 'negative'
    if review is None:
        return 'lead (PROVISIONAL: the trace review is not done)' if numbers['A2 failures to review'] else 'lead'
    listed = set(numbers['A2 failures to review'])
    if not listed <= set(review) or any(review[key] not in CLASSES for key in listed):
        raise SystemExit('NOT SCORED: the trace review does not class every listed failure')
    if any(review[key] == 'consistent with the change' for key in listed):
        return 'negative'
    return 'lead, uncertain harms' if any(review[key] == 'uncertain' for key in listed) else 'lead'


def main(cases_path, population_path, reading, key_path, plants_path):
    population = json.loads(Path(population_path).read_text())
    fresh_probe.configure(cases_path, population_path)
    if not set(population['population_b']) <= set(population['population_a']):
        raise SystemExit('population (b) is not within (a)')
    loaded = ps.load_reading(reading, key_path, plants_path)
    outcomes, readers, item_of, of_family, families, _, plant_misses = loaded
    review_path = Path(reading) / 'fresh' / 'trace-review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else None
    decisions = {}
    for counting in ('holds', 'fails'):
        rulings = {send: ps.accounting.rulings_of_two(of_family[families[0]][send], of_family[families[-1]][send], counting)[0]
                   for send in of_family[families[0]]}
        for arm in ('control', 'changed'):
            chosen = {send: outcome for send, outcome in outcomes.items() if send[0].startswith(arm + '|')}
            report = ps.accounting.account(list(chosen.values()), readers['reader 1'], readers['reader 2'], rulings)
            print(f'===== gate-1 report, {"A2" if arm == "changed" else "control"}, unresolved counted {"for" if counting == "holds" else "against"} the answer '
                  f'(population a; line 5\'s 35 of 44 and 28 of 44 not applicable) =====')
            ps.collector.print_report(report, chosen, readers, rulings, item_of)
        failed = failing(loaded, counting)
        for name in ('population_a', 'population_b'):
            numbers = comparison(failed, set(population[name]))
            decisions[(name, counting)] = 'STOPPED: a planted control was missed' if plant_misses else verdict(numbers, review)
            print(f'== comparison, {name}, unresolved counted {"for" if counting == "holds" else "against"}: {decisions[(name, counting)]}')
            for key, value in numbers.items():
                print(f'   {key}: {value}')
    values = set(decisions.values())
    final = values.pop() if len(values) == 1 else ('no verdict' if any(value.startswith('no verdict') for value in decisions.values())
                                                     else 'inconclusive: the populations or countings disagree')
    print(f'DECISION: {final}')
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
