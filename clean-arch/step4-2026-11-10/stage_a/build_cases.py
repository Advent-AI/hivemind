"""The 44 cases of Stage A ($0, read-only): the 34 theses the three unseeded draws opened (the census packet) and the 10 theses the
fresh acceptance run opened, each with the fields Step 1 wrote and its opening article. A thesis id is local to its draw, so a case
is named by draw and thesis id: `u1/clean-3`, `acc/clean-2`. Writes cases.json beside this file.

Usage: python3 clean-arch/step4-2026-11-10/stage_a/build_cases.py"""
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


def main():
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
