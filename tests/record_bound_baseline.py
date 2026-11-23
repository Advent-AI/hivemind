"""Records today's outcome of every call in `bound_cases.calls` on the four store states, before the bound resolver is built (proof
2c: "today's recorded output where the rule keeps it"). Run once, with today's code; the file it writes is the baseline the test reads.

  python3 tests/record_bound_baseline.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.join(os.path.dirname(HERE), 'src')]
import bound_cases  # noqa: E402

OUTPUT = os.path.join(HERE, 'fixtures', 'bound-baseline-2026-11-16.json')


def main():
    if os.path.exists(OUTPUT):
        raise SystemExit(f'{OUTPUT} exists: the baseline is recorded once, before the change')
    baseline = {}
    with tempfile.TemporaryDirectory() as folder:
        for state in bound_cases.STATES:
            conn = bound_cases.open_state(state, folder)
            for name, kind, call in bound_cases.calls(conn, state):
                baseline[f'{state}|{name}|{kind}'] = bound_cases.outcome(call)
            conn.close()
    with open(OUTPUT, 'w') as handle:
        json.dump(baseline, handle, indent=1, sort_keys=True)
        handle.write('\n')
    print(f'{len(baseline)} outcomes recorded -> {OUTPUT}')


if __name__ == '__main__':
    main()
