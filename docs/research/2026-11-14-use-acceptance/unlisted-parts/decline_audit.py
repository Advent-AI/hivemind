"""D579's $0 audit, part 1: every refusal ("no ladder") the step wrote in the stored readings outside Alex's 44, with its reason, the
two first readers' N marks, and the topic's description, outcome and period, so each can be read against line 6's decline cases.

  python3 decline_audit.py
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'))
import collect_readings as collector  # noqa: E402

DATA = ROOT / 'poc/data'
KEYS = Path(os.path.expanduser('~/.hivemind-keys'))
READINGS = {   # name: (stage-a folder, key, cases files)
    'july': (DATA / 'clean-e2e-full-2026-11-13/stage-a', DATA / 'clean-e2e-full-2026-11-13/stage-a-key.json',
             [DATA / f'clean-e2e-full-2026-11-13/c{n}/cases/cases.json' for n in (1, 2, 3)]),
    'fortnight': (DATA / 'clean-carried-run-2026-11-16/stage-a', KEYS / 'carried-run/stage-a-key.json',
                  [DATA / 'clean-carried-run-2026-11-16/c1/cases/cases.json']),
    'week-10-06': (DATA / 'clean-second-week-2026-11-15/week-continued/stage-a', KEYS / 'second-week-2026-11-15/key.json',
                   [DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json']),
}


def main():
    total = 0
    for name, (folder, key, case_files) in READINGS.items():
        theses = {case['case']: case['thesis'] for path in case_files for case in json.loads(path.read_text())}
        _, _, outcomes, readers, _ = collector.read_rows(folder, key)
        topics = sorted({send[0] for send in outcomes})
        refusals = [(send, outcome) for send, outcome in sorted(outcomes.items()) if outcome['status'] == 'no ladder']
        print(f'##### {name}: {len(topics)} topics, {len(outcomes)} sends, {len(refusals)} refusals by the model')
        for send, outcome in refusals:
            marks = [(readers[r].get(send) or {}).get('N') for r in collector.FAMILIES]
            thesis = theses[send[0]]
            print(f'== {send[0]} pass {send[1]} | N {marks}\n   reason: {outcome["reason"]}\n   description: {thesis["description"]}'
                  f'\n   outcome: {thesis["outcome"]}\n   period: {thesis.get("period")}')
        total += len(refusals)
    print(f'refusals in all: {total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
