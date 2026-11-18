"""The 44 cases of Stage A ($0, read-only): the 34 theses the three unseeded draws opened (the census packet) and the 10 theses the
fresh acceptance run opened, each with the fields Step 1 wrote and its opening article. A thesis id is local to its draw, so a case
is named by draw and thesis id: `u1/clean-3`, `acc/clean-2`. Writes cases.json beside this file.

Usage: python3 clean-arch/step4-2026-11-10/stage_a/build_cases.py
       python3 clean-arch/step4-2026-11-10/stage_a/build_cases.py --fresh <label> --draws <folder> --parts <trace>[,<segment>] --output <file>

The fresh path (WIRING-DESIGN.md §A, D448) writes one draw's opened theses as cases to the named file, named `<label>/<thesis id>`; the
count is the number of theses the trace opened (counted from its states, not a constant), each case is unique and has its opening
article. The default path is unchanged and still requires the 44."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEP = HERE.parent
ROOT = STEP.parents[1]
sys.path.insert(0, str(STEP / 'census'))
import build_packet  # noqa: E402

ACCEPTANCE = ROOT / 'poc/data/clean-acceptance-2026-11-09'
THESIS_FIELDS = ('description', 'outcome', 'period', 'opens_as', 'settled_by')
ITEM_FIELDS = ('publication_date', 'publisher', 'title', 'text')


def opened_count(draws, parts):
    """The theses a trace opened, counted from its before and after states alone (independent of build_packet)."""
    import sqlite3
    seen = set()
    for part in parts:
        conn = sqlite3.connect(f'file:{Path(draws) / part}?mode=ro', uri=True)
        try:
            for before, after in conn.execute("select before_state, after_state from trace where status='complete' order by sequence"):
                before_ids = {t['id'] for t in json.loads(before)}
                seen |= {t['id'] for t in json.loads(after) if t['id'] not in before_ids}
        finally:
            conn.close()
    return len(seen)


def fresh(label, draws, parts, output):
    expected = opened_count(draws, parts)
    entries = build_packet.theses_of(label, parts, draws=draws, expected=expected)
    cases = [{'case': f"{label}/{entry['id']}",
              'thesis': {'id': entry['id'], **{field: entry['thesis'][field] for field in THESIS_FIELDS}},
              'item': {field: entry['article'][field] for field in ITEM_FIELDS}} for entry in entries]
    names = [case['case'] for case in cases]
    if len(set(names)) != len(names) or any(not case['item'].get('text') or not case['item'].get('publication_date') for case in cases):
        raise SystemExit(f'{label}: case names not unique, or a case without its opening article')
    Path(output).write_text(json.dumps(cases, indent=1, ensure_ascii=False) + '\n')
    print(f'{label}: {len(cases)} cases written to {output} (the trace opened {expected})')


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fresh')
    parser.add_argument('--draws')
    parser.add_argument('--parts')
    parser.add_argument('--output')
    arguments = parser.parse_args()
    if arguments.fresh:
        if not (arguments.draws and arguments.parts and arguments.output):
            raise SystemExit('--fresh needs --draws, --parts and --output')
        if Path(arguments.output).exists():
            raise SystemExit(f'{arguments.output} exists: refused')
        return fresh(arguments.fresh, arguments.draws, arguments.parts.split(','), arguments.output)
    stored = json.loads((STEP / 'census' / 'packet.json').read_text())
    acceptance = build_packet.theses_of('acc', ['step1/trace.sqlite'], draws=ACCEPTANCE, expected=10)
    cases = []
    for entry in stored + acceptance:
        cases.append({'case': f"{entry['run']}/{entry['id']}",
                      'thesis': {'id': entry['id'], **{field: entry['thesis'][field] for field in THESIS_FIELDS}},
                      'item': {field: entry['article'][field] for field in ITEM_FIELDS}})
    names = [case['case'] for case in cases]
    if len(cases) != 44 or len(set(names)) != 44:
        raise SystemExit(f'{len(cases)} cases, {len(set(names))} different names: expected 44 and 44')
    (HERE / 'cases.json').write_text(json.dumps(cases, indent=1, ensure_ascii=False) + '\n')
    by_draw = {}
    for name in names:
        by_draw[name.split('/')[0]] = by_draw.get(name.split('/')[0], 0) + 1
    print('cases:', len(cases), by_draw, '| the same thesis id in more than one draw:', len(names) - len({name.split('/')[1] for name in names}))


if __name__ == '__main__':
    main()
