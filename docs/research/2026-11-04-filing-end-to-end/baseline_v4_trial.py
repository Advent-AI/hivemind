"""The fourth version's trial on the May report (baseline-design.md, round 18), the conditions written before the send:
  v12  the capex line (1,757) kept in at least 5 of its 6 item reads, and the starting figure delivered in all 3 sends
       (baseline_read_measure.delivered, the two items of a send together);
  v10  delivered in all 3 sends;
  v19  keeps no figure; v20 keeps neither total Data Center revenue (75,246 or 75.2) nor Data Center networking revenue (14.8);
  v1, v3, v22  keep only figures whose period or one-line names the first quarter of FY2027 (baseline_read_measure.first_quarter_fy27), and v22
       keeps its latest-quarter total revenue (81,615 or 81.6) in at least 2 of 3 sends (the end check must not drop a starting figure).
A send without a readable answer leaves the trial incomplete: nothing is concluded.

usage: python3 baseline_v4_trial.py <reading.json>
"""
import json
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
import baseline_all_measure as bam  # noqa: E402
import baseline_read_measure as brm  # noqa: E402
from baseline_read import numbers  # noqa: E402

SENDS = 3
QUESTIONS = ('v12', 'v10', 'v19', 'v20', 'v1', 'v3', 'v22')
NOT_V20 = {75246.0, 75.2, 14.8}
LATEST_REVENUE = {81615.0, 81.6}


def main():
    reading = json.load(open(sys.argv[1]))
    if reading.get('task_version') != 4:
        raise SystemExit('the reading is not the fourth version')
    if sorted(reading['report']) != sorted(bam.chosen_items(reading)) or len(set(reading['report'])) != len(reading['report']):
        raise SystemExit(f'INCOMPLETE: the reading\'s items {reading["report"]} are not the two the document rule chooses, each once')
    expected = [(v, i, n) for v in QUESTIONS for i in reading['report'] for n in range(SENDS)]
    missing = [job for job in expected if not reading['results'].get(job[0], {}).get(job[1]) or job[2] >= len(reading['results'][job[0]][job[1]])
               or reading['results'][job[0]][job[1]][job[2]] is None or reading['results'][job[0]][job[1]][job[2]].get('failure')]
    if missing:
        raise SystemExit(f'INCOMPLETE: {len(missing)} of {len(expected)} sends have no readable answer: {missing[:4]}')
    item_kept = lambda v, i, n: [f for f in reading['results'][v][i][n]['figures'] if f['kept']]
    sends = lambda v, n: [f for i in reading['report'] for f in reading['results'][v][i][n]['figures']]
    kept = lambda v, n: [f for f in sends(v, n) if f['kept']]
    capex_reads = sum(any(1757.0 in numbers(f['value']) for f in item_kept('v12', i, n)) for i in reading['report'] for n in range(SENDS))
    delivered = {v: sum(brm.delivered(v, sends(v, n)) for n in range(SENDS)) for v in ('v10', 'v12')}
    v19 = [len(kept('v19', n)) for n in range(SENDS)]
    v20_wrong = [f for n in range(SENDS) for f in kept('v20', n) if set(numbers(f['value'])) & NOT_V20]
    other_period = [(v, f) for v in ('v1', 'v3', 'v22') for n in range(SENDS) for f in kept(v, n) if not brm.first_quarter_fy27(f['period'] + ' ' + f['one_line'])]
    v22_kept = sum(any(set(numbers(f['value'])) & LATEST_REVENUE and brm.first_quarter_fy27(f['period'] + ' ' + f['one_line']) for f in kept('v22', n))
                   for n in range(SENDS))
    verdict = {'v12 capex line in at least 5 of 6 reads': capex_reads >= 5, 'v12 delivered 3 of 3': delivered['v12'] == 3,
               'v10 delivered 3 of 3': delivered['v10'] == 3, 'v19 keeps nothing': not any(v19),
               'v20 keeps no total or networking revenue': not v20_wrong, 'v1, v3, v22 keep only latest-quarter figures': not other_period,
               'v22 keeps its starting figure in 2 of 3': v22_kept >= 2}
    print(f'v12 capex line kept in {capex_reads} of 6 item reads; delivered by send count {delivered}; v19 kept by send {v19}; v22 starting figure in {v22_kept} of 3')
    for v in QUESTIONS:
        for n in range(SENDS):
            for f in sends(v, n):
                print(f'   {v} send {n} kept {f["kept"]}: {f["value"]} | {f["period"][:40]} | {f["quote"][:90]!r}')
    for v, f in other_period:
        print(f'   other period kept for {v}: {f["value"]} | {f["period"]} | {f["one_line"][:100]}')
    print('\n' + '; '.join(f'{k}: {"yes" if ok else "NO"}' for k, ok in verdict.items()) + f' -> {"pass" if all(verdict.values()) else "FAIL"}')


if __name__ == '__main__':
    main()
