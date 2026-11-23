"""D464's reading aid ($0): print every record of the identity probe by case, arm and send — the attempt outcomes, each retained new thesis
(question, outcome, period, reason, closest open thesis, why a separate bet), and for a merge article whether any kept evidence links to the
open thesis the reader named. It decides nothing; Claude marks each send against the frozen lines (PROBE-DESIGN-v2.md).

  python3 list_answers.py <probe output folder> > answers.txt
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out = Path(sys.argv[1])
    records = [json.loads(line) for line in (out / 'records.jsonl').read_text().splitlines() if line.strip()]
    selection = {s['case']: s for s in json.loads((HERE / 'v2/selection-v3.json').read_text())}
    by_case = defaultdict(list)
    for record in records:
        by_case[record['case']].append(record)
    for case in sorted(by_case, key=lambda c: (not c.startswith('fresh'), c)):
        info = selection.get(case)
        head = f"{info['category']} {info['role']} story={info['story']} expected={info['expected']}" if info else 'stored guard'
        print(f'\n######## {case} | {head}')
        if info:
            print(f"   title: {info['title'][:120]}")
            if info.get('question_if_new'):
                print(f"   reader's question: {info['question_if_new'][:160]}")
        target = info['expected'].split('link to ')[1] if info and info['expected'].startswith('link to') else None
        for record in sorted(by_case[case], key=lambda r: (r['arm'], r['send'])):
            outcomes = '; '.join(a.get('outcome') or a.get('error', '?') for a in record['attempts'])
            print(f"  [{record['arm']} send {record['send']}] {outcomes}")
            for thesis in record.get('new_theses') or []:
                print(f"     NEW ({thesis.get('opens_as')}; closest {thesis.get('closest_open_thesis')}): {thesis.get('description', '')[:170]}")
                print(f"         period: {str(thesis.get('period'))[:110]} | why separate: {str(thesis.get('why_a_separate_bet'))[:120]}")
            if target is not None and 'links' in record:
                linked = sum(1 for e in record['links'] if any(l.get('target_id') == target for l in e.get('links', [])))
                print(f"     evidence linked to {target}: {linked} of {len(record['links'])} kept")
    print(f'\n{len(records)} records')


if __name__ == '__main__':
    main()
