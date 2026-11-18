"""D576's $0 census of line 2 (a part of the topic left unlisted, mark L) on one stored Stage A reading: for every send either first
reader marks L failing, the topic as the ladder step was given it (description, outcome, period), the send's own list of parts not
judged, both readers' marks and reasons, and the lists of the topic's other sends. Judges nothing; read-only.

  python3 line2_census.py <stage-a folder> <key path> <cases.json the run was given>
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'clean-arch/step4-2026-11-10/stage_a'))
import collect_readings as collector  # noqa: E402


def parts_of(outcome):
    answer = outcome.get('answer') or {}
    ladder = answer.get('ladder') if isinstance(answer, dict) else None
    return None if ladder is None else [p['part'] for p in ladder.get('not_judged') or []]


def main(run_folder, key_path, cases_path):
    _, _, outcomes, readers, _ = collector.read_rows(run_folder, key_path)
    theses = {case['case']: case['thesis'] for case in json.loads(Path(cases_path).read_text())}
    flagged = [send for send in sorted(outcomes)
               if any((readers[r].get(send) or {}).get('L') == 'fails' for r in ('reader 1', 'reader 2'))]
    if not flagged:
        raise SystemExit('no send has an L mark failing: nothing judged')
    print(f'sends read {len(outcomes)}; sends with L failing in at least one first reader {len(flagged)}')
    for send in flagged:
        outcome = outcomes[send]
        thesis = theses[outcome['case']]
        print(f'\n=== {send[0]} pass {send[1]} ({outcome["status"]})')
        print(f'  description: {thesis["description"]}')
        print(f'  outcome:     {thesis["outcome"]}')
        print(f'  period:      {thesis.get("period")}')
        print(f'  ladder question: {(outcome["answer"].get("ladder") or {}).get("question")}')
        print(f'  this send lists: {json.dumps(parts_of(outcome), ensure_ascii=False)}')
        for reader in ('reader 1', 'reader 2'):
            row = readers[reader].get(send) or {}
            print(f'  {reader}: L {row.get("L")} | {row.get("why", "")}')
        for other in sorted(s for s in outcomes if s[0] == send[0] and s != send):
            print(f'  pass {other[1]} lists: {json.dumps(parts_of(outcomes[other]), ensure_ascii=False)}')
    return 0


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
