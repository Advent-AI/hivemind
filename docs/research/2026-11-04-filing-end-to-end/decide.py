"""PRD 10 §6's decision for one test (amendment, prd-amendment-proposal.md §1): code decides by counts against the frozen gold; a reader who did not
write the change reads every case the counts list, to name its mechanism for the report, and decides nothing.

Counts on the totals. For two arms of an answers file (a control and a variant, three sends each per article), each measure of
`measure_filing.measure_send` is summed per arm, and the observed difference (variant − control) is set against the differences obtained when each
article's six answers are randomly reassigned between the two arms (the article and its request stay fixed; only the arm label moves). p is the
share of reassignments reaching the observed difference in the direction tested.
  development set: facts the gold uses reaching a question it uses them for, up (p < 5%); statements under v1 or v22, down (p < 5%);
                   the standard's not-kept spans present, not up (p < 5%); core matters present, not down (p < 5%);
  held-out set:    facts the gold uses reaching a question it uses them for, not down; not-kept spans present, not up; core present, not down.

Counts per question (both sets together). A gold item reaches a question when any statement expressing it is filed there: its best match, or any
statement quoting its own passage (`measure_filing.expressing`). For a fact the gold uses for question q, the variant drops it when it delivers it
to q in at least two fewer of its three sends than the control, and gains it in the reverse case; a full drop is every control send and no variant
send. A drop is the single home, not counted, when in at least two of the variant's sends that miss q the fact is filed under another question the
gold uses it for that is not broader than q (not q's ancestor in the seed tree: D207's one home, the narrowest); a gain mirrors it. A noise statement
(its gold span not kept by the standard, or kept and used by no question) is new on q when the variant files it under q in at least two sends and the
control in none (full: in every variant send), removed in the reverse case. A question fails when, net of the reverse cases, it reaches the limit of
any component: drops 3, full drops 2, noise 5, full noise 3 (BASE_LIMITS). The reassignments are computed first; while a variant identical to the
control would fail in more than 10% of them, the component that fails such variants most often is raised one step; only then is the observed table
compared. Calibration on the reassignments of the stored arm with each earlier variant (1,000 each): some question reaches drops 3 in 2.6%, full
drops 2 in 0.3% and 0.0%, noise 5 in 5.4% and 8.4%, full noise 3 in 1.1%; the base limits together in 8.5% and 11.6%. Smaller changes on one
question are listed for the reader and decide nothing.

usage: python3 decide.py <selection.json> <answers.json> <control arm> <variant arm> [--draws 4000] [--seed 20261105]
"""
import collections
import json
import random
import sqlite3
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import measure_filing as mf  # noqa: E402
from hivemind.views import store  # noqa: E402

DRAW = f'{ROOT}/poc/data/e2e-r9-frozen-v108-2026-11-03/d1'
REACH = 'M6 reaching a gold question'
PARKING = 'P parking: statements under v1 or v22'
NOISE = 'M4 not-kept present'
CORE = 'M3 core present'
CRITERIA = {                                           # set → [(measure, direction tested, required)]
    'dev': [(REACH, 'up', 'change'), (PARKING, 'down', 'change'), (NOISE, 'up', 'no change'), (CORE, 'down', 'no change')],
    'heldout': [(REACH, 'down', 'no change'), (NOISE, 'up', 'no change'), (CORE, 'down', 'no change')],
}
COMPONENTS = {                                         # per-question guard: component → (counted against, counted for)
    'drops': ('drop', 'gain'),                         # facts delivered in two or more fewer sends than the control
    'full drops': ('full drop', 'full gain'),          # facts every control send delivers and no variant send does
    'noise': ('new noise', 'removed noise'),           # noise statements in two or more variant sends and no control send
    'full noise': ('full new noise', 'full removed noise'),
}
BASE_LIMITS = {'drops': 3, 'full drops': 2, 'noise': 5, 'full noise': 3}
CHANCE_CEILING = 0.10


def seed_ancestors():
    """question id → the questions broader than it in the seed tree (its parents, transitively; seeds' edges are written at seq 0, D253)."""
    views = sqlite3.connect(f'file:{DRAW}/views.sqlite?mode=ro', uri=True)
    views.row_factory = sqlite3.Row
    seed_ids = [row[0] for row in views.execute("select view_id from views where view_id glob 'v[0-9]*'")]
    parents = {view_id: store.direct_parents(views, view_id, 0) for view_id in seed_ids}

    def climb(view_id, seen):
        for parent in parents.get(view_id, ()):
            if parent not in seen:
                seen.add(parent)
                climb(parent, seen)
        return seen
    return collections.defaultdict(set, {view_id: climb(view_id, set()) for view_id in seed_ids})


def reassignment_test(per_article, draws, seed):
    """observed difference, and p in each direction, for every measure: (observed, p_up, p_down) by measure name."""
    measure_names = sorted(set().union(*[counter for control_sends, variant_sends in per_article for counter in control_sends + variant_sends]))
    observed = {name: sum(c[name] for _, variant_sends in per_article for c in variant_sends)
                - sum(c[name] for control_sends, _ in per_article for c in control_sends) for name in measure_names}
    generator = random.Random(seed)
    reached_up = collections.Counter()
    reached_down = collections.Counter()
    for _ in range(draws):
        difference = collections.Counter()
        for control_sends, variant_sends in per_article:
            pooled = control_sends + variant_sends
            order = list(range(len(pooled)))
            generator.shuffle(order)
            for position, index in enumerate(order):
                sign = -1 if position < len(control_sends) else 1
                for name, value in pooled[index].items():
                    difference[name] += sign * value
        for name in measure_names:
            reached_up[name] += difference[name] >= observed[name]
            reached_down[name] += difference[name] <= observed[name]
    return {name: (observed[name], reached_up[name] / draws, reached_down[name] / draws) for name in measure_names}


def send_facts(input_id, result, gold, seeds_of_item):
    """For one send: (item, question) → (delivered to that question, where the fact went), and the set of (gold span, question) noise links."""
    items, pairs, cited_for, articles, by_passage = gold
    deliveries = {}
    for item_id, questions in seeds_of_item.items():
        if items[item_id]['input_id'] != input_id:
            continue
        carriers = mf.expressing(result['kept'], items[item_id])
        reached = set().union(*[set(c['links']) for c in carriers]) if carriers else set()
        went = reached or {'homeless' if mf.expressing(result['homeless'], items[item_id]) else 'not written'}
        for question in questions:
            deliveries[(item_id, question)] = (question in reached, went)
    noise = {}
    article = articles.get(input_id)
    if article:
        spans = [('kept' if x.get('weight', 'kept') != 'not_kept' else 'not kept', x['span']) for x in article['items'] + article['not_kept']]
        for statement in result['kept']:
            text = statement['quote'] + ' ' + statement['one_line']
            scored = [(mf.same_fact(text, span)[1], weight, span) for weight, span in spans if mf.same_fact(text, span)[0]]
            if not scored:
                continue
            _, weight, span = max(scored)
            if weight == 'not kept' or not cited_for.get(by_passage.get((input_id, span)), set()):
                for link in statement['links']:
                    if link.startswith('v'):
                        noise[(span, link)] = statement['quote']
    return deliveries, noise


def per_question(article_sends, assignment, seeds_of_item, ancestors):
    """Counted drops, gains, single-home moves and noise changes per question for one split of each article's six sends into control and variant."""
    table = collections.defaultdict(lambda: collections.Counter())
    cases = []
    for input_id, sends in article_sends.items():
        control_indexes, variant_indexes = assignment[input_id]
        for key in sends[0][0]:
            item_id, question = key
            control_hits = sum(sends[i][0][key][0] for i in control_indexes)
            variant_hits = sum(sends[i][0][key][0] for i in variant_indexes)
            for side, losing_indexes, change in (('drop', variant_indexes, control_hits - variant_hits), ('gain', control_indexes, variant_hits - control_hits)):
                if change < 2:
                    continue
                other_homes = (seeds_of_item[item_id] - {question}) - ancestors[question]
                moved = sum(1 for i in losing_indexes if not sends[i][0][key][0] and sends[i][0][key][1] & other_homes)
                kind = f'single-home {side}' if moved >= 2 else side
                table[question][kind] += 1
                if kind == side and change == len(control_indexes):          # every send of one arm delivers it, no send of the other
                    table[question][f'full {side}'] += 1
                cases.append({'kind': kind, 'item': item_id, 'question': question, 'input_id': input_id, 'control': control_hits, 'variant': variant_hits,
                              'control_went_to': [sorted(sends[i][0][key][1]) for i in control_indexes],
                              'variant_went_to': [sorted(sends[i][0][key][1]) for i in variant_indexes]})
        noise_keys = set().union(*[sends[i][1].keys() for i in range(len(sends))])
        for span, question in noise_keys:
            in_control = sum(1 for i in control_indexes if (span, question) in sends[i][1])
            in_variant = sum(1 for i in variant_indexes if (span, question) in sends[i][1])
            if in_variant == len(variant_indexes) and in_control == 0:
                table[question]['full new noise'] += 1
            elif in_control == len(control_indexes) and in_variant == 0:
                table[question]['full removed noise'] += 1
            if in_variant >= 2 and in_control == 0:
                table[question]['new noise'] += 1
                quote = next(sends[i][1][(span, question)] for i in variant_indexes if (span, question) in sends[i][1])
                cases.append({'kind': 'new noise', 'question': question, 'input_id': input_id, 'span': span[:240], 'quote': quote[:240], 'variant_sends': in_variant})
            elif in_control >= 2 and in_variant == 0:
                table[question]['removed noise'] += 1
    return table, cases


def net(counts, component):
    plus, minus = COMPONENTS[component]
    return counts[plus] - counts[minus]


def failing(table, limits):
    return sorted(q for q, counts in table.items() if any(net(counts, component) >= limits[component] for component in COMPONENTS))


def main():
    selection_path, answers_path, control, variant = sys.argv[1:5]
    draws = int(sys.argv[sys.argv.index('--draws') + 1]) if '--draws' in sys.argv else 4000
    seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 20261105
    selection, answers = json.load(open(selection_path)), json.load(open(answers_path))
    gold = mf.load_gold()
    items, pairs, cited_for, articles, by_passage = gold
    both_arms = {input_id: per for input_id, per in answers.items() if control in per and variant in per}
    counters = {input_id: ([mf.measure_send(input_id, r, selection['sets'], gold)[0] for r in per[control]],
                           [mf.measure_send(input_id, r, selection['sets'], gold)[0] for r in per[variant]]) for input_id, per in both_arms.items()}
    verdict = {'control': control, 'variant': variant, 'draws': draws, 'seed': seed, 'counts': {}}
    print(f'{control} (control) against {variant}, {draws} reassignments of each article\'s six answers (seed {seed})')
    for set_name, criteria in CRITERIA.items():
        per_article = [counters[i] for i in selection['sets'][set_name] if i in counters]
        if not per_article:                            # a check over an empty population is unexercised, not passed (AGENTS §4)
            print(f'\n{set_name}: no article answered by both arms: UNEXERCISED')
            verdict['counts'][set_name] = 'unexercised'
            continue
        tested = reassignment_test(per_article, draws, seed)
        print(f'\n{set_name}: {len(per_article)} articles')
        print(f'  {"measure":44} {"control":>8} {"variant":>8} {"diff":>6} {"p up":>7} {"p down":>7}  per send (control | variant)')
        for name in sorted(tested):
            if name.startswith(('Q ', 'N ')):
                continue
            observed, p_up, p_down = tested[name]
            sends_control = [sum(pa[0][n][name] for pa in per_article) for n in range(3)]
            sends_variant = [sum(pa[1][n][name] for pa in per_article) for n in range(3)]
            print(f'  {name[:44]:44} {sum(sends_control):>8} {sum(sends_variant):>8} {observed:>6} {p_up:>7.4f} {p_down:>7.4f}  {sends_control} | {sends_variant}')
        results = []
        for name, direction, required in criteria:
            observed, p_up, p_down = tested.get(name, (0, 1.0, 1.0))
            p = p_up if direction == 'up' else p_down
            moved = p < 0.05 and (observed > 0 if direction == 'up' else observed < 0)
            passed = moved if required == 'change' else not moved
            results.append({'measure': name, 'direction': direction, 'required': required, 'observed': observed, 'p': p, 'passed': passed})
            print(f'  -> {name}: {direction} {"required" if required == "change" else "must not happen"}; diff {observed}, p {p:.4f}: {"pass" if passed else "FAIL"}')
        verdict['counts'][set_name] = results
    # Per question, both sets together.
    seeds_of_item = collections.defaultdict(set)
    for qid, seed_id, item_id in pairs:
        seeds_of_item[item_id].add(seed_id)
    ancestors = seed_ancestors()
    union = [i for i in both_arms if i in set(selection['sets']['dev']) | set(selection['sets']['heldout'])]
    article_sends = {i: [send_facts(i, r, gold, seeds_of_item) for r in both_arms[i][control] + both_arms[i][variant]] for i in union}
    generator = random.Random(seed + 1)
    null_tables = []                                   # the per-question tables of the reassignments, computed before the observed one
    for _ in range(draws):
        split = {}
        for i in union:
            order = list(range(6))
            generator.shuffle(order)
            split[i] = (tuple(order[:3]), tuple(order[3:]))
        null_tables.append(per_question(article_sends, split, seeds_of_item, ancestors)[0])

    def chance(limits, components=COMPONENTS):
        return sum(1 for t in null_tables if any(net(c, k) >= limits[k] for c in t.values() for k in components)) / draws
    limits = dict(BASE_LIMITS)
    while chance(limits) > CHANCE_CEILING:            # raise the component that fails identical variants most often, one step
        noisiest = max(COMPONENTS, key=lambda k: chance(limits, [k]))
        limits[noisiest] += 1
    actual = {i: ((0, 1, 2), (3, 4, 5)) for i in union}
    table, cases = per_question(article_sends, actual, seeds_of_item, ancestors)
    failed = failing(table, limits)
    print(f'\nper question, both sets ({len(union)} articles); limits {limits} (base {BASE_LIMITS}); a variant identical to the control fails in '
          f'{chance(limits):.1%} of {draws} reassignments ({", ".join(f"{k} {chance(limits, [k]):.1%}" for k in COMPONENTS)})')
    print(f'  {"question":9} {"drops":>6} {"gains":>6} {"full -":>7} {"full +":>7} {"1-home out":>11} {"1-home in":>10} {"new noise":>10} {"removed":>8} {"full new":>9}')
    for question in sorted(table, key=lambda q: int(q[1:]) if q[1:].isdigit() else 999):
        c = table[question]
        print(f'  {question:9} {c["drop"]:>6} {c["gain"]:>6} {c["full drop"]:>7} {c["full gain"]:>7} {c["single-home drop"]:>11} {c["single-home gain"]:>10} '
              f'{c["new noise"]:>10} {c["removed noise"]:>8} {c["full new noise"]:>9}' + ('   FAIL' if question in failed else ''))
    print(f'  failing: {failed or "none"}')
    failing_questions = failed
    counted = [r for results in verdict['counts'].values() if results != 'unexercised' for r in results]
    unexercised = [name for name, results in verdict['counts'].items() if results == 'unexercised']
    verdict.update(per_question={q: dict(c) for q, c in table.items()}, per_question_failing=failing_questions, per_question_limits=limits,
                   per_question_chance_failure=chance(limits), cases_to_read=cases)
    verdict['passed'] = None if unexercised else all(r['passed'] for r in counted) and not failing_questions
    print(f"\nverdict: {'UNEXERCISED on ' + ', '.join(unexercised) if unexercised else ('PASS' if verdict['passed'] else 'FAIL')}"
          f"{'' if verdict['passed'] or unexercised else ' (' + ', '.join([r['measure'] for r in counted if not r['passed']] + [f'question {q}' for q in failing_questions]) + ')'}"
          f"; {len(cases)} cases listed for the reader in {answers_path.replace('.json', f'-reading-{variant}.json')}")
    json.dump(verdict, open(answers_path.replace('.json', f'-reading-{variant}.json'), 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
