"""D575's $0 census of Stage B's control line within its fixed population: for each of the 16 control theses, the readers'
verdicts (from result/control-count.txt), the thesis as Steps 1 to 3 opened it (stage_a/cases.json) and the question the ladder
step wrote (the draw's clean_ladders row), so the step that set each blocker can be read side by side. Read-only."""
import json, re, sqlite3, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / 'clean-arch/step4-2026-11-10/stage_b'))
import stored_judgements  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
COUNT = ROOT / 'clean-arch/step4-2026-11-10/stage_b/result/control-count.txt'
CASES = ROOT / 'clean-arch/step4-2026-11-10/stage_a/cases.json'
RUN = ROOT / 'poc/data/clean-stage-b-2026-11-11'
LINE = re.compile(r'^(\[Ohio, listed apart\] )?(u\d)/(clean-\d+)\s+(q\d+) same question (\w+), same due (\w+) .*?material (shown|not shown|unresolved) '
                  r'\(items shown (\d+), not shown (\d+).*?eligible (True|False) .*?agrees with reader B (True|False)')


def main():
    cases = {c['case']: c['thesis'] for c in json.loads(CASES.read_text())}
    rows = [m for m in (LINE.match(line) for line in COUNT.read_text().splitlines()) if m]
    if len(rows) != 16:
        raise SystemExit(f'expected 16 control lines, read {len(rows)}')
    tally = {}
    for m in rows:
        ohio, draw, thesis, ruler, same_q, same_due, material, shown, not_shown, eligible, agrees = m.groups()
        conn = sqlite3.connect(f'file:{RUN}/draw-{draw}/views.sqlite?mode=ro', uri=True)
        stored_judgements.refuse_split_store(conn, 'control_census')
        ladder_question = json.loads(conn.execute('select checked_answer from clean_ladders where thesis_id=?', (thesis,)).fetchone()[0])['ladder']['question']
        opened = cases[f'{draw}/{thesis}']['description']
        if ohio:
            state = 'Ohio (listed apart)'
        elif eligible == 'True' and material == 'shown':
            state = 'counted'
        elif eligible == 'True':
            state = f'eligible, material {material}'
        else:
            state = f'not eligible (question {same_q}, due {same_due})'
        tally[state] = tally.get(state, 0) + 1
        print(f'{draw}/{thesis} {ruler} | {state} | material {material} ({shown} shown, {not_shown} not) | agrees {agrees}')
        print(f'   opened: {opened}')
        print(f'   ladder: {ladder_question}')
    print('== tally:', json.dumps(tally, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
