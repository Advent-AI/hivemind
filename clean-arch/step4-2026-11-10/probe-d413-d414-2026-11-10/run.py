"""The small send of D413 and D414 before the third Stage A (D415): two arms through the step's own runner, checks and resend.

  with-tie-rule     the working request: D411, D414 and D413's tie rule for an amount the company owes
  without-tie-rule  the same request with D413's sentence taken out of the system text and of the closing check

Both arms carry D414 and run in the same minutes on the same 17 stored theses, three sends each. What is read and what stops
the line is in REGISTERED.md, written before the send.

  python3 clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/run.py check                 # $0: the two arms differ in D413's sentences alone
  python3 clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/run.py send <new folder>
  python3 clean-arch/step4-2026-11-10/probe-d413-d414-2026-11-10/run.py send-working <new folder>   # the second small send: the working request alone
"""
import json
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'clean-arch' / 'e2e-2026-11-09'), str(STEP / 'ladder'), str(STEP / 'stage_a')]
import stage_a  # noqa: E402
from hivemind import universe  # noqa: E402

CAP_USD_AN_ARM = 0.15
OBLIGATIONS = ['u1/clean-1', 'u1/clean-7', 'u2/clean-1', 'u2/clean-6', 'u3/clean-1', 'u3/clean-8', 'acc/clean-1', 'acc/clean-3', 'acc/clean-7']
NOT_A_YEARS_FIGURE = ['u1/clean-9', 'u2/clean-8', 'acc/clean-5']
OTHER_FIGURES = ['u1/clean-4', 'acc/clean-4', 'acc/clean-10']
EVENTS = ['u1/clean-3', 'u1/clean-12']
THESES = OBLIGATIONS + NOT_A_YEARS_FIGURE + OTHER_FIGURES + EVENTS
FRENCH_INVESTIGATION = ['u1/clean-12', 'u2/clean-9', 'u3/clean-9']
SECOND_SEND_THESES = THESES + ['u2/clean-9', 'u3/clean-9']        # the second small send adds the two sibling theses
TIE_RULE_SYSTEM = (" For an amount the company owes, guarantees or has committed to pay, when neither the topic nor the item settles which end is good for the "
                   "business, because they argue both ends or say nothing on it, it is lower; when the topic's own words say that more of it is good, it is higher. "
                   "A retailer's lease guarantees that the item says win store sites and also weigh on its credit are lower; an airline's aircraft purchase "
                   "commitments that the topic tracks as the fleet growth its plan needs are higher.")
TIE_RULE_CLOSING = (" For an amount the company owes, guarantees or has committed to pay, check that favourable_end is lower unless the topic or the item settles "
                    "the other end or the topic's own words say that more of it is good.")


def arms():
    working = stage_a.request_texts()
    if working['system'].count(TIE_RULE_SYSTEM) != 1 or working['closing'].count(TIE_RULE_CLOSING) != 1:
        raise SystemExit("the working request does not carry D413's two sentences exactly once each")
    without = dict(working, system=working['system'].replace(TIE_RULE_SYSTEM, ''), closing=working['closing'].replace(TIE_RULE_CLOSING, ''))
    return {'with-tie-rule': working, 'without-tie-rule': without}


def main():
    both = arms()
    print('characters, system and closing:', {name: (len(texts['system']), len(texts['closing'])) for name, texts in both.items()})
    if sys.argv[1:] == ['check']:
        return
    if len(sys.argv) != 3 or sys.argv[1] not in ('send', 'send-working'):
        raise SystemExit(__doc__)
    if sys.argv[1] == 'send-working':
        both = {'working': both['with-tie-rule']}
    names = SECOND_SEND_THESES if sys.argv[1] == 'send-working' else THESES
    folder = Path(sys.argv[2])
    folder.mkdir(parents=True, exist_ok=False)
    cases = [case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text()) if case['case'] in names]
    if len(cases) != len(names):
        raise SystemExit('a named thesis is not in cases.json')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    results = {}

    def run_arm(name):
        written, limit, job_count = stage_a.run(cases, [1, 2, 3], folder / name, CAP_USD_AN_ARM, research_list=research_list, texts=both[name])
        known, in_full, _ = stage_a.ledger_total(folder / name / 'spend.jsonl')
        results[name] = (len(written), job_count, known + in_full, limit.stopped, limit.stop_reason)

    threads = [threading.Thread(target=run_arm, args=(name,)) for name in both]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    stopped = False
    for name, (written, job_count, spent, was_stopped, reason) in sorted(results.items()):
        print(f'{name}: {written} of {job_count} sends have an outcome; spent ${spent:.4f}' + (f'; STOPPED: {reason}' if was_stopped else ''))
        stopped = stopped or was_stopped or written != job_count
    if stopped or len(results) != len(both):
        raise SystemExit('STOPPED: the small send is not complete and is not read as a result')


if __name__ == '__main__':
    main()
