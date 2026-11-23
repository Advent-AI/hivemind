"""Read the small send of D416, D417 and D418 as REGISTERED.md says ($0). Written before any answer exists.

  python3 clean-arch/step4-2026-11-10/probe-d416-d418-2026-11-10/read.py <probe folder>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import run  # noqa: E402


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def rows_of(folder, arm):
    return {(row['case'], row['pass']): row for pass_folder in sorted((Path(folder) / arm).glob('send-*'))
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}


def one_send(row):
    if row is None:
        return 'NOT COMPLETE: no outcome stored'
    back = [reason for request in row['requests'] for reason in request.get('reasons', [])]
    note = f" | sent back first for: {'; '.join(short(reason, 110) for reason in back)}" if back else ''
    if row['status'] == 'no ladder':
        return f"declined: {short(row['reason'], 190)}{note}"
    if row['status'] != 'ladder':
        return f'REFUSED TWICE{note}'
    ladder, view = row['answer']['ladder'], row['view']
    if ladder.get('figure'):
        return f"{view['object_id']} figure {ladder['figure']['year']} | due {view['due_day']} | Q: {short(ladder['question'], 150)}{note}"
    ruled_out = ladder['event']['ruled_out']
    if isinstance(ruled_out, dict):
        ruled_out = f"BY {ruled_out['by_whom']} | {ruled_out['decision']}"
    return f"{view['object_id']} event | due {view['due_day']} | OUT: {short(ruled_out, 250)}{note}"


def main():
    folder = Path(sys.argv[1])
    stored = {arm: rows_of(folder, arm) for arm in run.THESES_OF_ARM}
    for arm in ('typed', 'survey', 'object'):
        print('#' * 110)
        print(f'arm {arm} beside the control')
        for name in run.THESES_OF_ARM[arm]:
            print('-' * 110)
            print(name)
            for which in ('control', arm):
                for pass_number in (1, 2, 3):
                    print(f'  {which:8} send {pass_number}: {one_send(stored[which].get((name, pass_number)))}')
    print('#' * 110)
    for arm, rows in stored.items():
        statuses = collections.Counter(row['status'] for row in rows.values())
        back = collections.Counter(short(reason, 60) for row in rows.values() for request in row['requests'] for reason in request.get('reasons', []))
        print(f'{arm}: {len(rows)} of {len(run.THESES_OF_ARM[arm]) * 3} sends stored; {dict(statuses)}; first answers sent back, by reason: {dict(back)}')
    for arm in ('control', 'object'):
        objects = {name: [row['view']['object_id'] if row and row['status'] == 'ladder' else ('-' if row is None else row['status'])
                          for row in (stored[arm].get((name, pass_number)) for pass_number in (1, 2, 3))] for name in run.THESES_OF_ARM['object']}
        print(f'{arm}, the object of each send: {objects}')
    for arm in ('control', 'survey'):
        kinds = {name: ['ladder' if row and row['status'] == 'ladder' else ('-' if row is None else row['status'])
                        for row in (stored[arm].get((name, pass_number)) for pass_number in (1, 2, 3))] for name in run.THESES_OF_ARM['survey']}
        print(f'{arm}, a ladder or not: {kinds}')


if __name__ == '__main__':
    main()
