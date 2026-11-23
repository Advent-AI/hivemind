"""The registered reading of every eligible pair of the census, written before any census answer is read (council R round 13): each
of the 105 pairs of `neither-census.json` gets one class.

  R  the required link, with its direction and sign: the known positive only (round 14), Data Center revenue reading total revenue
     (D537's clear case; the READS criterion's own first example, a product line read against the company's total). Missing it is a
     miss; the opposite direction or the opposite sign is a wrong link.
  W  any link is wrong: neither answer bounds or drives the other (the criterion's "neither" class) and the material each was shown
     names no connection: a financing or commitment amount against a revenue, growth or margin question (supply commitments, and credit
     support against revenue, excepted below), and two financing amounts of different kinds.
  O  open: defensible either way under the criterion as written (overlapping scopes; growth against the amount it is computed from;
     another period of the same quantity; supply commitments against revenue or margin; gross margin against revenue). Reported, not
     scored.

The seq-148 pairs were seen before this registration (the July test's answers): disclosed with every score.

  python3 expected_links.py > expected-links.md
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REQUIRED = {('v9', 'v14'): 'Data Center revenue read against total revenue: D537\'s clear case, the known positive'}
FINANCING = {'v1', 'v2', 'v15', 'v29', 'v32', 'v36'}
BASE_EFFECT_READ = {'v8', 'v9', 'v14', 'v16'}      # FY2027 revenue amounts; v17 is FY2028 total revenue growth
NO_BRIDGE = ('321:v16', '1238:v9')                # FY2027 CPU against FY2028 growth; FY2027 Data Center against FY2028 total (round 18)
REVENUE = {'v8', 'v9', 'v14', 'v16', 'v17', 'v21', 'v35'}
MARGIN = {'v28', 'v33'}
CREDIT = {'v1', 'v2'}
OPEN_FINANCING = {frozenset({'v1', 'v2'}): 'AI-cloud credit support sits inside all customer and cloud-provider credit support; either may read the other',
                  frozenset({'v15', 'v32'}): 'a licence payment commitment may sit inside supply commitments',
                  frozenset({'v29', 'v36'}): 'a convertible-bond investment may or may not count as an equity investment commitment',
                  frozenset({'v2', 'v15'}): 'the shown repurchase of unsold GPU capacity may sit inside supply commitments (round 15)'}


def classify(a, b):
    """(class, direction or None, reason) for the unordered pair a, b, from the scopes and the evidence each was shown with (round 14:
    only the known positive is required; a W pair is one whose shown material names no connection)."""
    for (reader, read), reason in REQUIRED.items():
        if {a, b} == {reader, read}:
            return 'R', f'{reader} reads {read}', reason
    pair = frozenset({a, b})
    if pair in OPEN_FINANCING:
        return 'O', None, OPEN_FINANCING[pair]
    if 'v15' in pair and pair & (REVENUE | MARGIN):
        return 'O', None, 'supply commitments, shown as "tying its fortunes to hyperscaler order books", against revenue or margin'
    if pair & CREDIT and pair & (REVENUE | MARGIN):
        return 'O', None, 'the credit-support evidence shown says NVIDIA earns product revenue and a share of cloud revenue on the supported capacity and may buy back unsold capacity (revenue mix and cost paths into margin, round 15)'
    if pair <= FINANCING:
        return 'W', None, 'two financing amounts of different kinds; the shown material names no connection'
    if pair & FINANCING and pair & (REVENUE | MARGIN):
        return 'W', None, 'a financing amount against a revenue, growth or margin question; the shown material names no connection'
    return 'O', None, 'part and whole far apart, overlapping scopes, growth against its amount, another period, or margin against revenue'


def main():
    census = json.loads((HERE / 'neither-census.json').read_text())
    rows, counts = [], {'R': 0, 'W': 0, 'O': 0}
    for opening in census['openings with a pair shown']:
        for pair in opening['pairs']:
            if not pair.get('eligible'):
                continue
            rows.append((opening['seq'], pair['thesis']))
    import sqlite3
    stored = sqlite3.connect('file:' + str(HERE.parents[2] / 'poc/data/comparison-2026-11-17/run/old-2/prod/views.sqlite') + '?mode=ro', uri=True)
    new_at = {seq: stored.execute('select view_id from views where created_seq=? and view_id in (select view_id from view_keys)', (seq,)).fetchone()[0]
              for seq, _ in rows}
    out = {}
    print('# Registered reading of the census pairs (written before any census answer; `expected_links.py`)\n')
    print('| seq | new | shown | class | required direction | reason |')
    print('|---|---|---|---|---|---|')
    for seq, thesis in rows:
        kind, direction, reason = classify(new_at[seq], thesis)
        counts[kind] += 1
        out[f'{seq}:{thesis}'] = {'new': new_at[seq], 'shown': thesis, 'class': kind, 'direction': direction}
        print(f'| {seq} | {new_at[seq]} | {thesis} | {kind} | {direction or ""} | {reason} |')
    print(f'\nPairs: {len(rows)}; R {counts["R"]}, W {counts["W"]}, O {counts["O"]}. The seq-148 pairs were seen before this registration.')
    (HERE / 'expected-links.json').write_text(json.dumps(out, indent=1))
    # version 2's registration (WORDING-V2.md §3, written before its probe's answers): the census's classes plus F, the base-effect
    # sign council R round 17 named: a growth rate reading an earlier period's revenue amount with the sign together
    v2 = json.loads(json.dumps(out))
    for key, entry in v2.items():
        if entry['new'] == 'v17' and entry['shown'] in BASE_EFFECT_READ:
            entry.update({'class': 'F', 'direction': None, 'forbidden': ('v17 reads ' + entry['shown'], 'together')})
    for key in NO_BRIDGE:            # round 18: the shown text gives no bridge across the periods, so any accepted link fails
        v2[key].update({'class': 'W', 'direction': None, 'forbidden': None})
    (HERE / 'expected-links-v2.json').write_text(json.dumps(v2, indent=1))
    print(f"\nVersion 2 adds F (forbidden: v17 reads an FY2027 revenue amount with the sign together): {sorted(k for k, e in v2.items() if e['class'] == 'F')}; "
          f"and W for any link across periods with no bridge in the shown text: {list(NO_BRIDGE)}; 1238:v14 stays O and is reported.")


if __name__ == '__main__':
    main()
