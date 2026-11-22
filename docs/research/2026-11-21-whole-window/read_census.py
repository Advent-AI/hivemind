"""Score the census draws against the registered reading (`expected-links.json`, written before any census answer was read).

  python3 read_census.py <census-1 folder> <census-2 folder> <census-3 folder> > census-pairs.md
  python3 read_census.py --v2 <probe-v2-1> <probe-v2-2> <probe-v2-3> > probe-v2-pairs.md   # version 2 (WORDING-V2.md), its own
                                                # registration (`expected-links-v2.json`: the census's classes plus F)

The scorer refuses unless it is given exactly three distinct draws (1, 2, 3), each with a `draw.json` that says it was a paid draw and was counted
(complete, both July seq-148 answers reused, equal to old-2, no link row, the ledger never stopped or overran: `window_test.census`),
and unless every registered pair has a READS answer in every draw.

Per pair and draw: the READS answer (choice and probabilities), the SIGN answer when asked, and the decision the product takes (a link
needs a reading direction at 0.5 or more and a sign of together or opposite at 0.5 or more). Verdicts:
  R pair (the known positive): right only when the registered direction is linked with the sign together (a higher total makes a
    higher Data Center figure more likely); missed when no link is written; wrong for the opposite direction or the opposite sign;
  W pair: wrong if linked, right if not;
  F pair (version 2 only): wrong when linked in the forbidden direction with the forbidden sign; otherwise reported;
  O pair: reported only.
A margin (the winning READS probability minus the next) below 0.10 on a linked or a required pair is flagged as fragile.
The gate (DESIGN.md §3; WORDING-V2.md §3): no wrong link (W, or F for version 2) in any draw, and the known positive right in every
draw.
"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
THRESHOLD = 0.5
READS = {'candidate_reads_thesis', 'thesis_reads_candidate'}
SIGNS = {'together', 'opposite'}
REQUIRED_SIGN = 'together'


class Refused(SystemExit):
    pass


def decisions(views_path):
    """{(seq, thesis): {'reads': choice, 'p': probabilities, 'sign': choice or None, 'sp': probabilities or None}}"""
    conn = sqlite3.connect(f'file:{views_path}?mode=ro', uri=True)
    out = {}
    for seq, record_json in conn.execute("select seq, record_json from link_selections where status='proposed' order by id"):
        for pair in json.loads(record_json).get('pairs', []):
            if 'thesis' not in pair:
                continue
            entry = out.setdefault((seq, pair['thesis']), {'reads': None, 'p': None, 'sign': None, 'sp': None})
            if 'reads' in pair:
                entry['reads'], entry['p'] = pair['reads'], pair['probabilities']
            if 'sign' in pair:
                entry['sign'], entry['sp'] = pair['sign'], pair['probabilities']
    return out


def linked(entry, new, thesis):
    """(direction '<reader> reads <read>', sign) the product writes, or (None, None)."""
    if entry['reads'] not in READS or entry['p'][entry['reads']] < THRESHOLD:
        return None, None
    if entry['sign'] not in SIGNS or entry['sp'][entry['sign']] < THRESHOLD:
        return None, None
    direction = f'{new} reads {thesis}' if entry['reads'] == 'candidate_reads_thesis' else f'{thesis} reads {new}'
    return direction, entry['sign']


def margin(entry):
    values = sorted(entry['p'].values(), reverse=True)
    return round(values[0] - values[1], 2)


def score(draws, expected):
    """draws: [(name, decisions)]. Returns (rows, summary); refuses when a registered pair has no READS answer in a draw."""
    rows, wrong, missed, right, fragile, positive = [], [], [], [], [], []
    for key, reg in expected.items():
        seq, thesis = int(key.split(':')[0]), key.split(':')[1]
        cells = []
        for name, answers in draws:
            entry = answers.get((seq, thesis))
            if entry is None or entry['p'] is None:
                raise Refused(f'{name}: no READS answer for the registered pair {key}')
            direction, sign = linked(entry, reg['new'], thesis)
            m = margin(entry)
            short = {'candidate_reads_thesis': 'new→', 'thesis_reads_candidate': '←new', 'neither': 'none'}[entry['reads']]
            cell = f"{short} {entry['p'][entry['reads']]:.2f} (m {m:.2f})" + (f"; {entry['sign']} {entry['sp'][entry['sign']]:.2f}" if entry['sign'] else '')
            if reg['class'] == 'R':
                if direction is None:
                    verdict = 'missed'
                elif direction == reg['direction'] and sign == REQUIRED_SIGN:
                    verdict = 'right'
                else:
                    verdict = 'WRONG'
                positive.append(verdict == 'right')
            elif reg['class'] == 'W':
                verdict = 'WRONG' if direction else 'right'
            elif reg['class'] == 'F':
                verdict = 'WRONG' if (direction, sign) == tuple(reg['forbidden']) else (f'linked: {direction} ({sign})' if direction else 'no link')
            else:
                verdict = f'linked: {direction} ({sign})' if direction else 'no link'
            if verdict == 'WRONG':
                wrong.append((name, key, direction, sign))
            elif verdict == 'missed':
                missed.append((name, key))
            elif verdict == 'right' and reg['class'] == 'R':
                right.append((name, key))
            if (direction or reg['class'] == 'R') and m < 0.10:
                fragile.append((name, key, m))
            cells.append(f'{cell} → {verdict}')
        rows.append((seq, reg, thesis, cells))
    gate = not wrong and bool(positive) and all(positive)
    return rows, {'right': right, 'missed': missed, 'wrong': wrong, 'fragile': fragile, 'gate': gate}


def counted_draws(folders, wording=None):
    if len(folders) != 3:
        raise Refused(f'three census draws are required, got {len(folders)}')
    seen = []
    for folder in folders:
        record_path = Path(folder) / 'draw.json'
        if not record_path.exists():
            raise Refused(f'{folder}: no draw.json (not a census draw)')
        record = json.loads(record_path.read_text())
        if record.get('transport') != 'paid':
            raise Refused(f'{folder}: not a paid draw (transport {record.get("transport")!r})')
        if record.get('wording') != wording:
            raise Refused(f'{folder}: wording {record.get("wording")!r}, expected {wording!r}')
        if not record.get('counted'):
            raise Refused(f'{folder}: the draw was not counted: {record.get("problems")}')
        seen.append(record['draw'])
    if sorted(seen) != ['1', '2', '3']:
        raise Refused(f'the draws must be 1, 2 and 3, got {seen}')
    return [(Path(f).name, decisions(Path(f) / 'views.sqlite')) for f in folders]


def main(folders):
    wording = None
    if folders and folders[0] == '--v2':
        wording, folders = 'v2', folders[1:]
    expected = json.loads((HERE / ('expected-links-v2.json' if wording == 'v2' else 'expected-links.json')).read_text())
    draws = counted_draws(folders, wording)
    rows, summary = score(draws, expected)
    print('# Census of the link decisions over the window, scored against the registered reading\n')
    print('| seq | new | shown | class | registered | ' + ' | '.join(name for name, _ in draws) + ' |')
    print('|---|---|---|---|---|' + '---|' * len(draws))
    for seq, reg, thesis, cells in rows:
        print(f"| {seq} | {reg['new']} | {thesis} | {reg['class']} | {reg['direction'] or ''} | " + ' | '.join(cells) + ' |')
    print('\nDraws: 3 (' + ('version 2: every link job asked fresh, the seq-148 jobs included).' if wording == 'v2' else
                             'the seq-148 jobs of each answered by its paired July sample).'))
    print(f"Known positive right: {len(summary['right'])}; missed: {len(summary['missed'])} {summary['missed']}")
    print(f"Wrong links: {len(summary['wrong'])} {summary['wrong']}")
    print(f"Fragile (margin below 0.10 on a linked or required pair): {len(summary['fragile'])} {summary['fragile']}")
    print(f"\nGate (no wrong link in any draw; the known positive right in every draw): {'PASS' if summary['gate'] else 'FAIL'}")


if __name__ == '__main__':
    main(sys.argv[1:])
