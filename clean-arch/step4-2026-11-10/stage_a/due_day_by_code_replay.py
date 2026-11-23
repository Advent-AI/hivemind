"""D414 on a stored run, at no cost: every stored ladder put through the step's checks and view writer as they now stand.

It prints what the due-day rule does to answers written before it existed: which answers the new refusal (a figure expected
before its year ends) sends back, anything else that is now refused, and how many theses have one due day in their three sends
when the day is the one code sets. A stored reference of the earlier shape is given the kind `expected` and no upper end, so
that the same checks read it. Nothing is sent; a refused answer would be sent back once in the working path, which a replay
cannot show.

  python3 clean-arch/step4-2026-11-10/stage_a/due_day_by_code_replay.py <run folder>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(STEP / 'ladder')]
import ladder_step  # noqa: E402
from hivemind import extraction, universe  # noqa: E402

COMPANY = 'NVDA'


def main():
    run_folder = Path(sys.argv[1])
    cases = {case['case']: case for case in json.loads((HERE / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    rows = [json.loads(line) for pass_folder in sorted(run_folder.glob('send-*')) for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines()]
    sends_of = collections.defaultdict(list)
    judged, refused_new, other_reasons, days = 0, [], collections.Counter(), {}
    for row in rows:
        sends_of[row['case']].append(row)
        if row['status'] != 'ladder':
            continue
        judged += 1
        accepted = [request for request in row['requests'] if request['result'] == 'ladder'][-1]
        answer = ladder_step.parse_exactly(accepted['answer_text'])
        reference = answer['ladder']['reference']
        if reference is not None:
            reference.setdefault('kind', 'expected')
            reference.setdefault('value_to', None)
        case = cases[row['case']]
        reasons, passage = ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=COMPANY, research_list=research_list,
                                                    repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                                    beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
        for reason in reasons:
            if 'before that: a figure is published after the period it covers ends' in reason:
                refused_new.append((row['case'], row['pass'], answer['ladder']['figure']['year'], answer['ladder']['due_day']))
            else:
                other_reasons[(row['case'], row['pass'], reason[:110])] += 1
        if not reasons:
            view = ladder_step.write_view(answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'], company=COMPANY,
                                          research_list=research_list)
            days[(row['case'], row['pass'])] = (answer['ladder']['due_day'], view['due_day'], answer['ladder']['due_day_basis'], answer['ladder'].get('figure') is not None)
    print(f'stored ladders put through the checks as they stand: {judged}')
    print(f'sent back by the new refusal, a figure expected before its year ends: {len(refused_new)}')
    for case, pass_number, year, day in sorted(refused_new):
        print(f'  {case} send {pass_number}: year {year}, expected {day}')
    print(f'sent back for any other reason: {len(other_reasons)}')
    for (case, pass_number, reason), _ in sorted(other_reasons.items()):
        print(f'  {case} send {pass_number}: {reason}')
    all_ladders = [case for case, sends in sends_of.items() if all(row['status'] == 'ladder' for row in sends)]
    still_whole = [case for case in all_ladders if all((case, row['pass']) in days for row in sends_of[case])]
    as_sent = sum(1 for case in all_ladders if len({row['answer']['ladder']['due_day'] for row in sends_of[case]}) == 1)
    by_code = [case for case in still_whole if len({days[(case, row['pass'])][1] for row in sends_of[case]}) == 1]
    print(f'theses whose three sends are ladders: {len(all_ladders)}; one due day in all three as sent: {as_sent}')
    print(f'of them, theses whose three stored answers the checks still accept: {len(still_whole)}; one due day in all three by code: {len(by_code)}')
    print('  still differing:', sorted(set(still_whole) - set(by_code)))
    moved = collections.Counter()
    for (case, pass_number), (written, due, basis, is_figure) in days.items():
        if written != due:
            moved[(case, due)] += 1
    print(f'answers whose due day code replaces: {sum(moved.values())}, in {len({case for case, _ in moved})} theses')
    if judged == 0:
        raise SystemExit('no ladder was read: nothing was judged')


if __name__ == '__main__':
    main()
