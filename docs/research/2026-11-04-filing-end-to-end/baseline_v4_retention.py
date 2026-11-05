"""The May registered reading's added condition (baseline-design.md, round 18, after review-v4-codex-r1): the fourth version's end check must not
drop a starting figure the earlier versions kept. Each of v1, v2, v3, v11 and v22 keeps, in at least 2 of 3 sends (the two items together), a kept
figure whose value is its first-quarter FY2027 figure as printed and whose period or one-line names that quarter; v10 and v12 are delivered in at
least 2 of 3 sends by the second version's decision (their condition 1 is then judged). The reading must hold the 22 seeds, both items, three replies.

usage: python3 baseline_v4_retention.py <reading.json>
"""
import json
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
import baseline_all_measure as bam  # noqa: E402
import baseline_read_measure as brm  # noqa: E402
from baseline_read import numbers  # noqa: E402

SENDS = 3
LATEST = {'v1': {81615.0, 81.6}, 'v2': {75246.0, 75.2}, 'v3': {75.0, 74.9}, 'v11': {1.87, 2.39}, 'v22': {81615.0, 81.6}}


def main():
    reading = json.load(open(sys.argv[1]))
    if reading.get('task_version') != 4 or reading.get('report_day') != '2026-05-20':
        raise SystemExit('the reading is not the fourth version on the May 20 report')
    bam.sheet_rows(reading)                            # refuses an incomplete reading or a failed send
    sends = lambda v, n: [f for i in reading['report'] for f in reading['results'][v][i][n]['figures']]
    kept_latest = {v: sum(any(f['kept'] and set(numbers(f['value'])) & values and brm.first_quarter_fy27(f['period'] + ' ' + f['one_line'])
                              for f in sends(v, n)) for n in range(SENDS)) for v, values in LATEST.items()}
    delivered = {v: sum(brm.delivered(v, sends(v, n)) for n in range(SENDS)) for v in ('v10', 'v12')}
    ok = all(c >= 2 for c in kept_latest.values()) and all(c >= 2 for c in delivered.values())
    print(f'starting figure kept by send count {kept_latest}; v10, v12 delivered {delivered} -> {"pass" if ok else "FAIL"} (each needs 2 of 3)')


if __name__ == '__main__':
    main()
