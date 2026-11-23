"""The source check's readings joined to the key, by the rule frozen in SOURCE-CHECK-DESIGN.md ($0). It judges nothing.

  python3 tally_source_check.py <key folder holding key-source-check.json>
"""
import collections
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_source_check  # noqa: E402

FAMILIES = ('codex', 'claude')
CASE_ONE = {'none_shown', 'weak'}


def rows_of(path):
    if not path.exists():
        return {}
    text, decoder, out, position = path.read_text(), json.JSONDecoder(), {}, 0
    while True:
        start = text.find('{"case"', position)
        if start == -1:
            return out
        try:
            row, position = decoder.raw_decode(text, start)
            out[row['case']] = row
        except json.JSONDecodeError:
            position = start + 1


def main(key_folder):
    key = json.loads((Path(key_folder) / 'key-source-check.json').read_text())
    rows = {f: {c: r for n in (1, 2, 3, 4) for c, r in rows_of(HERE / f'{f}-source-check-{n}.jsonl').items()} for f in FAMILIES}
    for f in FAMILIES:
        missing = sorted(set(key) - set(rows[f]), key=lambda c: int(c[1:]))
        print(f'{f}: {len(rows[f])} of {len(key)} cases; missing {missing}')
    expected = {judgement: marks for _, judgement, marks in build_source_check.CONTROLS}
    print('\nCONTROLS (every recorded expected mark):')
    control_missed = False
    for case, entry in sorted(key.items(), key=lambda kv: int(kv[0][1:])):
        if entry['group'] != 'control':
            continue
        marks = expected[entry['judgement']]
        for f in FAMILIES:
            got = {m: rows[f].get(case, {}).get(m) for m in marks}
            ok = all(got[m] == v for m, v in marks.items())
            control_missed |= not ok
            print(f"   {case} ({entry['draw']} #{entry['judgement']}) {f}: {'as expected' if ok else 'MISSED'} | expected {marks} | got {got}")
    study = {c: e for c, e in key.items() if e['group'] in ('rejected', 'accepted')}
    differ = 0
    case_one_both = collections.Counter()
    print('\nSTUDY CASES (both families; earlier verdict):')
    for case, entry in sorted(study.items(), key=lambda kv: (kv[1]['group'], kv[1]['draw'], kv[1]['view'], kv[1]['day'])):
        marks = [rows[f].get(case, {}) for f in FAMILIES]
        member = [m.get('bears') in CASE_ONE if m.get('bears') not in (None, 'cannot_tell') else None for m in marks]
        if member[0] is None or member[1] is None or member[0] != member[1]:
            differ += 1
        if member == [True, True]:
            case_one_both[entry['group']] += 1
        print(f"   {entry['group']:<8} {entry['draw']} {entry['view']} {entry['day']} {entry['verdict']:<12} | "
              + ' || '.join(f"{f}: bears {m.get('bears')}, supports {m.get('supports_band')}, step {m.get('step_decides')}, accept {m.get('accept')}"
                            for f, m in zip(FAMILIES, marks)))
    n_rejected = sum(1 for e in study.values() if e['group'] == 'rejected')
    n_accepted = sum(1 for e in study.values() if e['group'] == 'accepted')
    share_rejected = case_one_both['rejected'] / n_rejected
    share_accepted = case_one_both['accepted'] / n_accepted
    print(f"\ncase (1) by both families: rejected {case_one_both['rejected']} of {n_rejected} ({share_rejected:.0%}), "
          f"accepted {case_one_both['accepted']} of {n_accepted} ({share_accepted:.0%}); difference {100 * (share_rejected - share_accepted):.0f} points")
    print(f'families differ on case (1) membership (a cannot_tell or a missing row counts as a difference): {differ} of {len(study)}')
    if control_missed:
        verdict = 'UNCLEAR (a control mark missed)'
    elif differ >= 6:
        verdict = 'NOT APPLICABLE CONSISTENTLY'
    elif case_one_both['rejected'] - case_one_both['accepted'] < 4 or share_rejected - share_accepted < 0.30:
        verdict = 'DOES NOT TRACK REJECTION'
    else:
        verdict = 'LEAD (exploratory)'
    print('by the frozen rule:', verdict)
    print('\nper path:')
    for path in sorted({(e['draw'], e['view']) for e in study.values()}):
        cases = [c for c, e in study.items() if (e['draw'], e['view']) == path]
        for group in ('rejected', 'accepted'):
            mine = [c for c in cases if study[c]['group'] == group]
            both = sum(all(rows[f].get(c, {}).get('bears') in CASE_ONE for f in FAMILIES) for c in mine)
            print(f'   {path} {group}: case (1) by both {both} of {len(mine)}')


if __name__ == '__main__':
    main(sys.argv[1])
