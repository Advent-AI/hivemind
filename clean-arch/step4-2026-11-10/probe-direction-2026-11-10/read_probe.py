"""Read the three-arm probe's first answers as REGISTERED.md says ($0). Written before any answer exists.

  python3 .../read_probe.py cells <probe folder>                 # every cell: the favourable end, a decline, or "not complete"
  python3 .../read_probe.py checks <probe folder>                # the old and reference arms' answers through the working checks
  python3 .../read_probe.py events <probe folder> <key path>     # the events' answers shuffled, without the arm; the key is written apart
"""
import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(STEP / 'ladder'), str(STEP / 'stage_a'), str(HERE)]
import ladder_step  # noqa: E402
import probe  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

COMPANY = 'NVDA'


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def answers_of(folder):
    """Every cell of the probe: the stored row, or None where no answer was stored."""
    stored = {(row['arm'], row['draw'], row['case']): row for line in (Path(folder) / 'answers.jsonl').read_text().splitlines() for row in [json.loads(line)]}
    return {(arm, draw, name): stored.get((arm, draw, name)) for arm, names in probe.THESES_OF_ARM.items() for draw in probe.DRAWS for name in names}


def parsed(row, arm):
    """(answer, None) or (None, why it is not complete)."""
    if row is None:
        return None, 'not complete: no answer stored'
    if row['error'] or not row['answer_text']:
        return None, f"not complete: {row['error'] or 'no text'}"
    try:
        answer = json.loads(row['answer_text'])
    except ValueError:
        return None, 'not complete: the answer cannot be read'
    problems = model.check_schema(answer, probe.texts_of(arm)['schema'])
    if problems:
        return None, f'not complete: does not fit its schema ({problems[0]})'
    return answer, None


def cell(answer, research_list):
    if answer['ladder'] is None:
        return 'declined'
    ladder = answer['ladder']
    if not ladder.get('figure'):
        return 'an event'
    return ladder['figure']['favourable_end'] if ladder['object'] == COMPANY or ladder['object'] not in research_list.themes else "a theme's figure"


def cells(folder, research_list):
    answers = answers_of(folder)
    incomplete = 0
    for name in probe.DIRECTION_THESES:
        print('-' * 110)
        print(name)
        for arm in probe.THESES_OF_ARM:
            values, notes = [], []
            for draw in probe.DRAWS:
                answer, why = parsed(answers[(arm, draw, name)], arm)
                if answer is None:
                    incomplete += 1
                    values.append('NOT COMPLETE')
                    notes.append(f'draw {draw}: {why}')
                    continue
                value = cell(answer, research_list)
                values.append(value)
                if value == 'declined':
                    notes.append(f"draw {draw} declined: {short(answer['no_ladder'], 150)}")
                elif value in ('higher', 'lower', 'unclear'):
                    notes.append(f"draw {draw} {value}: {short(answer['ladder']['figure']['favourable_why'], 170)}")
            print(f'  {arm:10} {values}')
            for note in notes:
                print(f'             {note}')
    print('=' * 110)
    print(f'cells of the direction theses: {len(probe.DIRECTION_THESES) * len(probe.THESES_OF_ARM) * len(probe.DRAWS)}; not complete: {incomplete}')


def checks(folder, research_list):
    cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    answers = answers_of(folder)
    for arm in ('old', 'reference'):
        refused, judged, reasons_seen, declined = 0, 0, collections.Counter(), 0
        for (cell_arm, draw, name), row in sorted(answers.items()):
            if cell_arm != arm:
                continue
            answer, why = parsed(row, arm)
            if answer is None:
                print(f'  {arm} draw {draw} {name}: {why}')
                continue
            judged += 1
            if answer['ladder'] is None:
                declined += 1
                continue
            exact = ladder_step.parse_exactly(row['answer_text'])
            reference = exact['ladder']['reference']
            if arm == 'old' and reference is not None:
                reference.setdefault('kind', 'expected')
                reference.setdefault('value_to', None)
            case = cases[name]
            reasons, _ = ladder_step.check_answer(exact, thesis=case['thesis'], article=case['item'], company=COMPANY, research_list=research_list,
                                                 repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                                 beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
            refused += bool(reasons)
            for reason in reasons:
                reasons_seen[short(reason, 70)] += 1
                print(f'  {arm} draw {draw} {name}: {short(reason, 200)}')
        print(f'{arm}: {judged} answers read; declined {declined}; a first answer a check would send back: {refused}; reasons: {dict(reasons_seen)}')
        print('-' * 110)


def events(folder, key_path, research_list):
    answers = answers_of(folder)
    listing = [(arm, draw, name) for (arm, draw, name) in answers if name in probe.EVENT_THESES]
    random.Random(20261111).shuffle(listing)
    key = {}
    for number, (arm, draw, name) in enumerate(listing, start=1):
        key[str(number)] = [arm, draw, name]
        answer, why = parsed(answers[(arm, draw, name)], arm)
        print('-' * 110)
        print(f'[{number}] {name}')
        if answer is None:
            print('   ', why)
            continue
        if answer['ladder'] is None:
            print('    DECLINED:', short(answer['no_ladder'], 300))
            continue
        ladder = answer['ladder']
        print(f"    object {ladder['object']} | due {ladder['due_day']} ({ladder['due_day_basis']})")
        print('    Q:', short(ladder['question'], 330))
        if ladder.get('event'):
            print('    YES:', short(ladder['event']['happened'], 330))
            print('    OUT:', short(ladder['event']['ruled_out'], 330))
        else:
            print('    A FIGURE, not an event:', ladder['figure']['unit'], ladder['figure']['year'])
        print('    not judged:', [short(entry, 90) for entry in ladder['not_judged']])
    Path(key_path).write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(listing)} event answers listed; the key from number to arm is at the path given')


def main():
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    if len(sys.argv) == 3 and sys.argv[1] == 'cells':
        cells(sys.argv[2], research_list)
    elif len(sys.argv) == 3 and sys.argv[1] == 'checks':
        checks(sys.argv[2], research_list)
    elif len(sys.argv) == 4 and sys.argv[1] == 'events':
        events(sys.argv[2], sys.argv[3], research_list)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
