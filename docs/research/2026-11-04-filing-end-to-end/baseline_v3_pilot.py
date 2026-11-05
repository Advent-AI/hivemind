"""The third version's trial on the questions that motivated it (baseline-design.md, round 14), the four conditions written before the send:
  v19  keeps no figure in any of its 3 sends (the report states no standalone Vera CPU revenue, no line it is computed from, no other name for it);
  v20  keeps neither total Data Center revenue (75,246 or 75.2) nor Data Center networking revenue (14.8) in any send; every other kept figure is
       listed to be read;
  v10  delivers its two lines (first-quarter operating income and revenue) in at least 2 of 3 sends, by the second version's decision
       (baseline_read_measure.delivered), the two items of a send together;
  v12  delivers its first-quarter purchases of property and equipment in at least 2 of 3 sends, the same way.

A send without a readable answer (transport failure, a reply that is not JSON) leaves the trial incomplete: nothing is concluded.

usage: python3 baseline_v3_pilot.py <reading.json>
"""
import json
import sys

sys.path[:0] = ['/Users/lchingen/hivemind/src', '/Users/lchingen/hivemind/docs/research/2026-11-04-filing-end-to-end']
import baseline_read_measure as brm  # noqa: E402
from baseline_read import numbers  # noqa: E402

SENDS = 3
NOT_V20 = {75246.0, 75.2, 14.8}           # total Data Center revenue as printed in either item, and Data Center networking revenue


def v_missing(reading, view_id, input_id, n):
    sends = reading['results'].get(view_id, {}).get(input_id, [])
    return n >= len(sends) or sends[n] is None or bool(sends[n].get('failure'))


def main():
    reading = json.load(open(sys.argv[1]))
    if reading.get('task_version') != 3:
        raise SystemExit('the reading is not the third version')
    expected = [(v, i, n) for v in ('v19', 'v20', 'v10', 'v12') for i in reading['report'] for n in range(SENDS)]
    missing = [job for job in expected if v_missing(reading, *job)]
    if missing:
        raise SystemExit(f'INCOMPLETE: {len(missing)} of {len(expected)} sends have no readable answer (a failed send is not an empty answer): {missing[:4]}')
    sends = lambda view_id, n: [f for input_id in reading['report'] for f in reading['results'][view_id][input_id][n]['figures']]
    kept = lambda view_id, n: [f for f in sends(view_id, n) if f['kept']]
    v19 = [len(kept('v19', n)) for n in range(SENDS)]
    v20_wrong = [f for n in range(SENDS) for f in kept('v20', n) if set(numbers(f['value'])) & NOT_V20]
    v20_other = [f for n in range(SENDS) for f in kept('v20', n) if not set(numbers(f['value'])) & NOT_V20]
    delivered = {v: sum(brm.delivered(v, sends(v, n)) for n in range(SENDS)) for v in ('v10', 'v12')}
    verdict = {'v19 keeps nothing': not any(v19), 'v20 keeps no total or networking revenue': not v20_wrong,
               'v10 delivered in 2 of 3': delivered['v10'] >= 2, 'v12 delivered in 2 of 3': delivered['v12'] >= 2}
    print(f'v19 kept figures by send: {v19}')
    for f in v19 and [f for n in range(SENDS) for f in kept('v19', n)]:
        print(f'   v19 kept: {f["value"]} | {f["period"]} | {f["quote"][:120]!r}')
    print(f'v20 kept total or networking revenue: {len(v20_wrong)}; other kept figures to read: {len(v20_other)}')
    for f in v20_wrong + v20_other:
        print(f'   v20 kept: {f["value"]} | {f["period"]} | {f["quote"][:120]!r}')
    print(f'delivered by send count: {delivered}')
    for view_id in ('v19', 'v20', 'v10', 'v12'):
        refused = [f for n in range(SENDS) for f in sends(view_id, n) if not f['kept']]
        for f in refused:
            print(f'   {view_id} refused (in report {f["in_report"]}, labelled {f["labelled"]}, value in quote {f["value_in_quote"]}): '
                  f'{f["quote"][:100]!r} value {f["value"]!r}')
    print('\n' + '; '.join(f'{k}: {"yes" if v else "NO"}' for k, v in verdict.items()) + f' -> {"pass" if all(verdict.values()) else "FAIL"}')


if __name__ == '__main__':
    main()
