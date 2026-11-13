"""A figure's due day: the class counted on a stored run, and a candidate rule replayed on its answers ($0).

The candidate rule, for a figure whose day neither the thesis nor the article states (`due_day_basis` expected_publication):
the last day of the year the figure covers (the company's fiscal year, or the calendar year for a theme) plus a fixed number of
days. It is a candidate for Alex to decide, not a rule in force; the two lags are arguments.

For every thesis with a figure it prints the period the thesis names, the material that settles it, the three days the model
set, the day the rule would set, and how the rule's day stands against the model's own latest estimate (earlier than every
estimate the model gave: the material may not be out; much later: the question waits for nothing).

  python3 clean-arch/step4-2026-11-10/stage_a/due_day_rule_replay.py <run folder> [company lag in days] [theme lag in days]
"""
import collections
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(ROOT / 'src'), str(HERE)]
import accounting  # noqa: E402
from hivemind import universe  # noqa: E402

COMPANY = 'NVDA'


def period_end(row, research_list):
    """The last day of the year a figure covers."""
    year = row['answer']['ladder']['figure']['year']
    if row['view']['kind'] == 'asset':
        return datetime.date.fromisoformat(str(research_list.fiscal_period(COMPANY, year, bare_is_calendar=True)[1])[:10])
    return datetime.date(int(year), 12, 31)


def by_rule(row, research_list, lags):
    ladder = row['answer']['ladder']
    if ladder.get('figure') is None or ladder['due_day_basis'] != 'expected_publication':
        return ladder['due_day']
    return (period_end(row, research_list) + datetime.timedelta(days=lags[row['view']['kind']])).isoformat()


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def main():
    run_folder = Path(sys.argv[1])
    lags = {'asset': int(sys.argv[2]) if len(sys.argv) > 2 else 60, 'theme': int(sys.argv[3]) if len(sys.argv) > 3 else 90}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    rows = [json.loads(line) for pass_folder in sorted(run_folder.glob('send-*')) for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines()]
    sends_of = collections.defaultdict(list)
    for row in rows:
        sends_of[row['case']].append(row)
    all_ladders = {case: sends for case, sends in sends_of.items() if all(row['status'] == 'ladder' for row in sends)}
    same_now = sum(1 for sends in all_ladders.values() if len({row['answer']['ladder']['due_day'] for row in sends}) == 1)
    same_by_rule = sum(1 for sends in all_ladders.values() if len({by_rule(row, research_list, lags) for row in sends}) == 1)
    print(f"lags: {lags['asset']} days after the company's fiscal year-end, {lags['theme']} days after the calendar year-end")
    print(f'theses whose three sends are ladders: {len(all_ladders)}; the same due day in all three: {same_now} as sent, {same_by_rule} by the rule')
    print('still differing by the rule:', sorted(case for case, sends in all_ladders.items() if len({by_rule(row, research_list, lags) for row in sends}) > 1))
    earlier, later = [], []
    print()
    print('every thesis with a figure: the days the model set, the day by the rule, and the rule against the model\'s latest estimate')
    for case, sends in sorted(sends_of.items()):
        figures = [row for row in sends if row['status'] == 'ladder' and accounting.kind_of(row) in ('company figure', 'theme figure')]
        if not figures:
            continue
        thesis = cases[case]['thesis']
        set_days = [f"{row['answer']['ladder']['due_day']}{'*' if row['answer']['ladder']['due_day_basis'] != 'expected_publication' else ''}" for row in figures]
        rule_days = sorted({by_rule(row, research_list, lags) for row in figures})
        estimated = [datetime.date.fromisoformat(row['answer']['ladder']['due_day']) for row in figures if row['answer']['ladder']['due_day_basis'] == 'expected_publication']
        note = ''
        if estimated:
            gap = (datetime.date.fromisoformat(rule_days[-1]) - max(estimated)).days
            note = f'{gap:+d} days against the latest estimate'
            if gap < 0:
                earlier.append(case)
            if gap > 120:
                later.append(case)
        print(f"  {case:<12} {figures[0]['view']['kind']:<5} year {'/'.join(sorted({row['answer']['ladder']['figure']['year'] for row in figures})):<12} "
              f"model: {', '.join(set_days):<38} rule: {', '.join(rule_days):<12} {note}")
        print(f"               period: {short(thesis['period'], 150)}")
        print(f"               settled by: {short(thesis['settled_by'], 150)}")
    print()
    print('a "*" marks a day the answer calls stated; the rule leaves it as it is')
    print('the rule\'s day falls before an estimate the model gave:', earlier)
    print('the rule\'s day falls more than 120 days after the model\'s latest estimate:', later)


if __name__ == '__main__':
    main()
