"""The small send of D421's (c): the typed ruling out of an event (who decides, what they decide), alone, beside the working
request, which now carries D417, D420's proceeding rule and D418's narrowed sentence. Through the step's own runner, checks and
resend, both arms in the same minutes, three sends a thesis. The stop condition is the first trial's (REGISTERED.md).

  python3 clean-arch/step4-2026-11-10/probe-d421c-2026-11-10/run.py check
  python3 clean-arch/step4-2026-11-10/probe-d421c-2026-11-10/run.py send <new folder>
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
DEADLINE = ['u1/clean-3', 'u2/clean-2', 'u3/clean-3', 'u1/clean-6', 'u2/clean-5', 'u3/clean-7']       # a product ships by a date that is the due day
FRENCH = ['u1/clean-12', 'u2/clean-9', 'u3/clean-9']                                                  # a proceeding against the company itself
THESES_OF_ARM = {'typed': DEADLINE + FRENCH + ['u2/clean-3']}
THESES_OF_ARM['control'] = list(THESES_OF_ARM['typed'])


def texts_of(arm):
    return {'system': (HERE / f'{arm}-system.txt').read_text(), 'closing': (HERE / f'{arm}-closing.txt').read_text().strip(),
            'schema': json.loads((HERE / f'{arm}-schema.json').read_text())}


def check():
    working = stage_a.request_texts()
    control = texts_of('control')
    if control != working:
        raise SystemExit('the control arm is not the working request')
    for arm in ('typed',):
        texts = texts_of(arm)
        differs = [part for part in ('system', 'closing', 'schema') if texts[part] != control[part]]
        print(f"{arm}: differs from the control in {differs}; system {len(texts['system'])} characters, closing {len(texts['closing'])}; "
              f'{len(THESES_OF_ARM[arm])} theses')
    print(f"control: the working request; {len(THESES_OF_ARM['control'])} theses; sends in all: {3 * sum(len(names) for names in THESES_OF_ARM.values())}")


def main():
    if sys.argv[1:] == ['check']:
        check()
        return
    if len(sys.argv) != 3 or sys.argv[1] != 'send':
        raise SystemExit(__doc__)
    check()
    folder = Path(sys.argv[2])
    folder.mkdir(parents=True, exist_ok=False)
    all_cases = {case['case']: case for case in json.loads((STEP / 'stage_a' / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    results = {}

    def run_arm(arm):
        cases = [all_cases[name] for name in THESES_OF_ARM[arm]]
        written, limit, job_count = stage_a.run(cases, [1, 2, 3], folder / arm, CAP_USD_AN_ARM, research_list=research_list, texts=texts_of(arm))
        known, in_full, _ = stage_a.ledger_total(folder / arm / 'spend.jsonl')
        results[arm] = (len(written), job_count, known + in_full, limit.stopped, limit.stop_reason)

    threads = [threading.Thread(target=run_arm, args=(arm,)) for arm in THESES_OF_ARM]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    stopped = len(results) != len(THESES_OF_ARM)
    for arm, (written, job_count, spent, was_stopped, reason) in sorted(results.items()):
        print(f'{arm}: {written} of {job_count} sends have an outcome; spent ${spent:.4f}' + (f'; STOPPED: {reason}' if was_stopped else ''))
        stopped = stopped or was_stopped or written != job_count
    print(f'spent in all: ${sum(entry[2] for entry in results.values()):.4f}')
    if stopped:
        raise SystemExit('STOPPED: the small send is not complete and is not read as a result')


if __name__ == '__main__':
    main()
