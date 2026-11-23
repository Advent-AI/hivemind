"""Print a run's answers thesis by thesis, the three sends side by side, for reading by hand ($0).

  python3 clean-arch/step4-2026-11-10/stage_a/print_traces.py <run folder> [first thesis number] [last thesis number]
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def compact_number(match):
    """12,000,000,000 as 12B, for a line a person reads; the exact numbers stay in the outcomes file."""
    value = float(match.group(0).replace(',', ''))
    for size, letter in ((1e12, 'T'), (1e9, 'B'), (1e6, 'M')):
        if abs(value) >= size:
            return f'{value / size:g}{letter}'
    return f'{value:g}'


def compact_range(condition):
    text = re.sub(r'\d[\d,]*(?:\.\d+)?', compact_number, condition.split(' (')[0])
    return text.replace('from ', '').replace(' to below ', '–').replace('below ', '<').replace(' or more', '+')


def main():
    run_folder = Path(sys.argv[1])
    cases = json.loads((HERE / 'cases.json').read_text())
    first, last = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (1, len(cases))
    rows = {(row['case'], row['pass']): row for pass_folder in sorted(run_folder.glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}
    for number, case in enumerate(cases, start=1):
        if not first <= number <= last:
            continue
        thesis = case['thesis']
        print('=' * 100)
        print(f"[{number}] {case['case']} | article {case['item']['publication_date']} | {thesis['opens_as']} | OUTCOME: {short(thesis['outcome'], 230)}")
        for pass_number in (1, 2, 3):
            row = rows.get((case['case'], pass_number))
            if row is None:
                print(f' p{pass_number}: no outcome')
                continue
            sent_back = [short('; '.join(request.get('reasons', [])), 70) for request in row['requests'] if request.get('reasons')]
            resent = f' | resent for: {sent_back[0]}' if sent_back else ''
            if row['status'] == 'no ladder':
                print(f" p{pass_number}: DECLINED: {short(row['reason'], 210)}{resent}")
                continue
            if row['status'] != 'ladder':
                print(f' p{pass_number}: REFUSED TWICE: {sent_back}')
                continue
            ladder, view = row['answer']['ladder'], row['view']
            reference = ladder['reference']
            reference_text = 'no ref' if reference is None else f"ref {'no value' if reference['value'] is None else compact_number(re.match(r'.*', str(reference['value'])))}: {short(row['passage'], 90)}"
            listed = [short(part['part'], 55) for part in ladder['not_judged']]
            print(f" p{pass_number}: {view['object_id']} due {view['due_day']} [{ladder['due_day_basis'][:6]}] | Q: {short(view['question'], 215)}")
            if ladder.get('event') is not None:
                print(f"     YES: {short(ladder['event']['happened'], 170)}")
                ruled_out = ladder['event']['ruled_out']
                if isinstance(ruled_out, dict):                  # D416: who decides, what they decide
                    ruled_out = f"[by {ruled_out['by_whom']}] {ruled_out['decision']}"
                print(f"     OUT: {short(ruled_out, 230) if ruled_out else 'none (two rungs)'}")
            else:
                figure = ladder['figure']
                ranges = ' | '.join(compact_range(rung['condition']) for rung in view['rungs'])
                why = '' if figure['favourable_end'] == 'n/a' else f" ({short(figure['favourable_why'], 80)})"
                print(f"     {figure['unit']} {figure['year']} fav {figure['favourable_end']}{why}: {ranges}")
            print(f'     {reference_text} | not judged {len(listed)}: {listed[:3]}{resent}')


if __name__ == '__main__':
    main()
