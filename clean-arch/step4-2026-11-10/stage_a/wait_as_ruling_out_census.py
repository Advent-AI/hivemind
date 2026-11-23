"""The class "a wait written as the ruling out", counted on every stored event answer since events have three outcomes ($0).

A crude screen picks the ruling-out sentences to read by hand: a sentence that speaks of the day passing or of the event not
having happened and names no decision, abandonment or statement. The screen only chooses what is printed; the count that
matters is the hand reading of what it prints, and a sample of what it does not print is shown so that the screen itself can
be checked. Nothing is sent.

  python3 clean-arch/step4-2026-11-10/stage_a/wait_as_ruling_out_census.py
"""
import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DATA = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10'
WAIT = re.compile(r'has passed|have passed|passes without|passed without|ends without|ended without|has not begun|have not begun|had not begun|'
                  r'has not occurred|have not occurred|not occurred by|no first shipment|no longer possible|deadline has passed|without the event', re.I)
DECISION = re.compile(r'abandon|cancel|withdraw|decid|den(y|ies|ied)|reject|block|prohibit|bar(s|red)?\b|postpon|delay|state[sd]?\b|announc|confirm|rul(e|es|ed|ing)\b', re.I)


def short(text, length):
    text = ' '.join(str(text).split())
    return text if len(text) <= length else text[:length - 1] + '…'


def stored_events():
    """(where, case, send, ruled_out) for every stored event answer of the three-outcome form."""
    for folder in ('run-2', 'probe-reference', 'probe-d413-d414/with-tie-rule', 'probe-d413-d414/without-tie-rule', 'probe-d413-d414-second/working', 'run-3'):
        for pass_folder in sorted((DATA / folder).glob('send-*')):
            for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines():
                row = json.loads(line)
                if row['status'] == 'ladder' and row['answer']['ladder'].get('event'):
                    yield folder, row['case'], row['pass'], row['answer']['ladder']['event']['ruled_out']
    for line in (DATA / 'probe-direction' / 'answers.jsonl').read_text().splitlines():
        row = json.loads(line)
        ladder = json.loads(row['answer_text']).get('ladder') if row['answer_text'] else None
        if ladder and ladder.get('event'):
            yield f"probe-direction/{row['arm']}", row['case'], row['draw'], ladder['event']['ruled_out']


def main():
    by_case = collections.defaultdict(list)
    for where, case, send, ruled_out in stored_events():
        by_case[case].append((where, send, ruled_out))
    total = sum(len(rows) for rows in by_case.values())
    print(f'stored event answers of the three-outcome form: {total}, in {len(by_case)} theses')
    screened = 0
    for case, rows in sorted(by_case.items()):
        picked = [(where, send, text) for where, send, text in rows if text is not None and WAIT.search(text)]
        no_decision = [entry for entry in picked if not DECISION.search(entry[2])]
        nulls = sum(1 for _, _, text in rows if text is None)
        print('-' * 110)
        print(f'{case}: {len(rows)} answers; no ruling out: {nulls}; picked by the screen: {len(picked)}, of them with no decision word: {len(no_decision)}')
        for where, send, text in picked:
            screened += 1
            print(f"   [{'no decision word' if (where, send, text) in no_decision else 'has a decision word'}] {where} send {send}: {short(text, 240)}")
    print('=' * 110)
    print(f'picked by the screen for reading: {screened} of {total}')
    not_picked = [(case, where, send, text) for case, rows in sorted(by_case.items()) for where, send, text in rows if text is not None and not WAIT.search(text)]
    print(f'a sample of the {len(not_picked)} sentences the screen did not pick (every twelfth), to check the screen:')
    for case, where, send, text in not_picked[::12]:
        print(f'   {case} {where} send {send}: {short(text, 200)}')


if __name__ == '__main__':
    main()
