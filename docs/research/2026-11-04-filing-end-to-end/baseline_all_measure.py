"""The all-seeds test's measure (baseline-design.md, round 8, the three conditions written before the send):
  1. v10 and v12 each agree in at least 6 of their 9 arm sends (3 draws x 3 reading sends; a reading send that kept nothing, a refused answer or
     a missing send counts as not agreeing);
  2. no question that received a starting figure is made worse: it fails when its drop is significant (control and arm labels permuted within
     each draw, where the 6 sends are exchangeable if the records have no effect; exact one-sided p < 0.05 on the control-minus-arm total), or
     when it drops by 2 or more of 9 and both readers find its wrong arm answers derive their rung from a starting-figure record (the adjudication
     file); a listed drop without an adjudication leaves the condition pending. Printed beside it: the chance, given each question's margins,
     that the significance rule fails it when the records do nothing (exact under that null: the draws are independent and, with inert records,
     a draw's six sends are exchangeable), and for all questions together the union bound (valid whatever the dependence between questions) and
     the product form (only if the questions were independent);
  Also printed for reading, not a condition: each question's rungs by draw, and every arm answer that chose a rung its draw's control did not or
  cited a starting-figure record (the ruler cannot see a move between two rungs that both overlap the gold range).
  3. every kept figure of the 22 questions has exactly one class from each reader and a final class (the classification file, keyed as the
     sheet), and none is misread (another period's or basis's figure labelled as the latest period or the question's basis), another quantity or not a
     figure.
A reader's decision is one value of the closed set; when the two readers agree the final decision is theirs, and when they differ it is either of
theirs with the reason written; anything else is refused.

usage: python3 baseline_all_measure.py sheet <reading.json> <sheet.json>
       python3 baseline_all_measure.py judge <reading.json> <requests.json> <answers.json> [<classified.json> [<adjudicated.json>]]
"""
import itertools
import json
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/scripts', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
from fractions import Fraction

ALPHA = Fraction(1, 20)                    # exact: a tail of exactly 0.05 is not below it
DRAWS = ('d1', 'd2', 'd3')
SENDS = 3
NEVER_JUDGED = ('v10', 'v12')
CLASSES = ('own', 'own, another period', 'misread', 'another quantity', 'not a figure')
WRONG = ('misread', 'another quantity', 'not a figure')
VERDICTS = ('the records drove the wrong answers', 'not the records')


def chosen_items(reading):
    """The items the document rule chooses for the reading's coverage start (the first test's readings predate the field: 2026-07-01)."""
    import sqlite3
    import baseline_all
    items = sqlite3.connect(f'file:{baseline_all.rf.ITEMS}?mode=ro', uri=True)
    items.row_factory = sqlite3.Row
    return [r['input_id'] for r in baseline_all.latest_report(items, reading.get('coverage_start', baseline_all.COVERAGE_START))]


def sheet_rows(reading):
    if sorted(reading['report']) != sorted(chosen_items(reading)) or len(set(reading['report'])) != len(reading['report']):
        raise SystemExit(f'INCOMPLETE: the reading\'s items {reading["report"]} are not the two the document rule chooses, each once')
    incomplete = [f'v{k}|{i}' for k in range(1, 23) for i in reading['report'] if len(reading['results'].get(f'v{k}', {}).get(i) or []) != SENDS]
    if incomplete:
        raise SystemExit(f'INCOMPLETE: {len(incomplete)} question-item pairs of the 22 seeds lack three replies: {incomplete[:4]}')
    failed = [f'{v}|{i}|{n}' for v, by_item in reading['results'].items() for i, sends in by_item.items() for n, r in enumerate(sends)
              if r is None or r.get('failure')]
    if failed:
        raise SystemExit(f'INCOMPLETE: {len(failed)} reading sends have no readable answer (a failed send is not an empty answer): {failed[:4]}')
    rows = []
    for view_id, by_item in reading['results'].items():
        for input_id in reading['report']:
            for n, r in enumerate(by_item[input_id]):
                for k, f in enumerate(r['figures']):
                    if f['kept']:
                        rows.append({'key': f'{view_id}|{input_id}|{n}|{k}', 'view_id': view_id, 'item': input_id.rsplit(':', 1)[-1], 'send': n,
                                     **{field: f[field] for field in ('quote', 'value', 'unit', 'period', 'basis', 'one_line')}})
    return rows


def null_distribution(per_draw):
    """The exact distribution of the control-minus-arm total when control and arm labels are permuted within each draw."""
    dist = {0: Fraction(1)}
    for control, arm in per_draw:
        pooled, n = control + arm, len(control)
        splits = list(itertools.combinations(range(len(pooled)), n))
        step = {}
        for chosen in splits:
            t = sum(pooled[i] for i in chosen) - sum(pooled[i] for i in range(len(pooled)) if i not in chosen)
            step[t] = step.get(t, 0) + Fraction(1, len(splits))
        merged = {}
        for a, pa in dist.items():
            for b, pb in step.items():
                merged[a + b] = merged.get(a + b, 0) + pa * pb
        dist = merged
    return dist


def tail(dist, t):
    return sum((p for value, p in dist.items() if value >= t), Fraction(0))


def false_failure(dist):
    """The chance that the significance rule fails the question when the records do nothing, given its margins."""
    significant = [t for t in dist if tail(dist, t) < ALPHA]
    return tail(dist, min(significant)) if significant else Fraction(0)


def decided(entry, field, allowed):
    """Two readers' decisions from the closed set and a final one: theirs when they agree; one of theirs, with a reason, when they differ."""
    first, second, final = entry.get('reader_1'), entry.get('reader_2'), entry.get(field)
    if first not in allowed or second not in allowed:
        return False
    return final == first if first == second else final in (first, second) and bool(str(entry.get('why') or '').strip())


def outcomes(results, key, sends):
    got = [bool(x['agrees_with_gold']) for x in results.get(key, [])]
    return got + [False] * (sends - len(got))


def judge(reading, requests, answers, classified, adjudicated):
    sheet_rows(reading)                       # refuses a reading with a failed send
    results = answers['results']
    keys = {k for k, r in requests.items() if r['sends']}
    missing = keys - set(results)
    if missing:
        print(f'WARNING: {len(missing)} requests have no answers; they count as not agreeing: {sorted(missing)[:5]}')
    questions = sorted({r['view_id'] for r in requests.values()} | set(NEVER_JUDGED), key=lambda v: int(v[1:]))
    no_figure = sorted({v for v in reading['results']} - set(questions), key=lambda v: int(v[1:]))
    print(f'questions with no kept figure in any reading send (both arms the same request, not sent): {no_figure}\n')
    print(f'{"question":8} {"control by draw":16} {"arm by draw":16} {"control":8} {"arm":6} {"p":7} {"null fail":9} sends citing a record')
    delivered, listed, significant, null_fails, rungs, to_read = {}, [], [], [], [], []
    for view_id in questions:
        per_draw, cited = [], 0
        for draw in DRAWS:
            control = outcomes(results, f'{draw} {view_id} control', SENDS) if view_id not in NEVER_JUDGED else []
            control_rungs = [x['rung'] for x in results.get(f'{draw} {view_id} control', [])]
            arm, arm_rungs = [], []
            for n in range(SENDS):
                key = f'{draw} {view_id} arm {n}'
                arm += outcomes(results, key, 1)
                cited += sum(1 for x in results.get(key, []) if x['cites_records'])
                for x in results.get(key, []):
                    arm_rungs.append(x['rung'])
                    if (view_id not in NEVER_JUDGED and x['rung'] not in control_rungs) or x['cites_records']:
                        to_read.append(f'{key}: rung {x["rung"]} (control rungs {control_rungs}), cites records {x["cites_records"]}, agrees {x["agrees_with_gold"]}')
            rungs.append(f'{view_id} {draw}: control {control_rungs} arm {arm_rungs}')
            per_draw.append((control, arm))
        arm_total = sum(sum(a) for _, a in per_draw)
        by_draw_a = ' '.join(f'{sum(a)}/{len(a)}' for _, a in per_draw)
        if view_id in NEVER_JUDGED:
            delivered[view_id] = arm_total >= 6
            print(f'{view_id:8} {"never judged":16} {by_draw_a:16} {"-":8} {arm_total}/9{"":2} {"":7} {"":9} {cited}  -> '
                  f'{"delivered" if delivered[view_id] else "NOT delivered"} (needs 6/9)')
            continue
        control_total = sum(sum(c) for c, _ in per_draw)
        dist = null_distribution(per_draw)
        p = tail(dist, control_total - arm_total)
        chance = false_failure(dist)
        null_fails.append(chance)
        flag = ''
        if p < ALPHA:
            significant.append(view_id)
            flag = 'SIGNIFICANT DROP'
        elif control_total - arm_total >= 2:
            listed.append(view_id)
            flag = 'drop of 2+: read the reasons'
        print(f'{view_id:8} {" ".join(f"{sum(c)}/{len(c)}" for c, _ in per_draw):16} {by_draw_a:16} {control_total}/9{"":4} {arm_total}/9{"":2} '
              f'{float(p):<7.3f} {float(chance):<9.3f} {cited}  {flag}')
    product = Fraction(1)
    for chance in null_fails:
        product *= 1 - chance
    print(f'\nchance that the significance rule fails some question when the records do nothing: at most {float(min(sum(null_fails, Fraction(0)), Fraction(1))):.3f} '
          f'(union bound, any dependence); {float(1 - product):.3f} if the questions were independent')
    print('\nrungs chosen, by question and draw (the ruler cannot see a move between two rungs that both overlap the gold range):\n  ' + '\n  '.join(rungs))
    print(f'\narm answers to read beside the control (a rung the control did not choose in that draw, or a starting-figure record cited): {len(to_read)}\n  '
          + '\n  '.join(to_read))
    print(f'\ncondition 1 (v10, v12 each at least 6/9): {"pass" if all(delivered.values()) else "FAIL"} {delivered}')
    verdicts = {}
    for entry in adjudicated or []:
        if entry['view_id'] in verdicts or not decided(entry, 'verdict', VERDICTS):
            raise SystemExit(f'adjudication of {entry["view_id"]}: duplicated, or not two readers\' decisions from {VERDICTS} with a final one that '
                             f'is theirs (a reason written when they differ)')
        verdicts[entry['view_id']] = entry['verdict']
    harmed = [v for v in listed if verdicts.get(v) == VERDICTS[0]]
    pending = [v for v in listed if v not in verdicts]
    if significant or harmed:
        state = f'FAIL (significant {significant}, records drove the wrong answers {harmed})'
    elif pending:
        state = f'PENDING: the reasons of {pending} are to be read by two readers'
    else:
        state = 'pass'
    print(f'condition 2 (no question made worse): {state}; listed drops {listed}, adjudicated {verdicts}')
    if classified is None:
        print('condition 3: the classification file is not given; not judged')
        return
    expected = {row['key'] for row in sheet_rows(reading)}
    given = [c['key'] for c in classified]
    problems = [c['key'] for c in classified if not decided(c, 'class', CLASSES)]
    if set(given) != expected or len(given) != len(set(given)) or problems:
        raise SystemExit(f'classification incomplete: {len(expected - set(given))} kept figures missing, {len(set(given) - expected)} unknown keys, '
                         f'{len(given) - len(set(given))} duplicates, {len(problems)} not two readers\' classes from the closed set with a final one '
                         f'that is theirs (a reason written when they differ)')
    wrong = [c['key'] for c in classified if c['class'] in WRONG]
    counts = {k: sum(1 for c in classified if c['class'] == k) for k in CLASSES}
    print(f'condition 3 (nothing misread, of another quantity or not a figure): {"pass" if not wrong else "FAIL " + str(wrong)}; '
          f'{len(classified)} kept figures: {counts}; readers disagreed on {sum(1 for c in classified if c["reader_1"] != c["reader_2"])}')


def main():
    if sys.argv[1] == 'sheet':
        rows = sheet_rows(json.load(open(sys.argv[2])))
        json.dump(rows, open(sys.argv[3], 'w'), indent=1, ensure_ascii=False)
        print(f'{len(rows)} kept figures over {len({r["view_id"] for r in rows})} questions written to {sys.argv[3]}')
        return
    reading, requests, answers = (json.load(open(p)) for p in sys.argv[2:5])
    optional = [json.load(open(p)) for p in sys.argv[5:7]]
    judge(reading, requests, answers, *(optional + [None] * (2 - len(optional))))


if __name__ == '__main__':
    main()
