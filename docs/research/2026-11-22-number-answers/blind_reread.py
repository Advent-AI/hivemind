"""The D743 blinded re-read of a v13s blind run (SMALL-DESIGN.md §5 [D743]): the same first replies under the corrected readers' brief,
plus two controls built from a copy of E's Claude reply (a range outcome crossing the $40B edge: C-overlap names a band it overlaps
with the reason given, C-disjoint names a band it does not reach), in a fresh shuffle. The key is written beside, never in a packet.

Usage: python3 blind_reread.py <blind run folder>
"""
import copy
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / 'src'))
import blind_test as bt  # noqa: E402
import calc_small as cs  # noqa: E402

LOW, HIGH = 80.0, 115.0                     # growth estimate range: 20 x 1.80 = 36 to 20 x 2.15 = 43


def controls(out):
    """C-overlap and C-disjoint from E's Claude reply; the code accepts the first and refuses the second (S6)."""
    base = json.loads((out / 'E' / 'answers' / 'claude.json').read_text())
    est = next(f for f in base['figures'] if f['kind'] == 'estimate' and f['unit'] == '%')
    outcome = next(f for f in base['figures'] if f['outcome_for'])
    made = {}
    for name, rung, sentence in [('C-overlap', 3, 'The growth estimate is a range, so the outcome runs from about $36 billion to $43 billion. '
                                  'Its midpoint, near $39.5 billion, and most of the range lie in rung 3, so I choose rung 3; only the top '
                                  'of the range reaches rung 2.'),
                                 ('C-disjoint', 4, 'The growth estimate is a range, so the outcome runs from about $36 billion to $43 '
                                  'billion. I choose rung 4.')]:
        a = copy.deepcopy(base)
        e = next(f for f in a['figures'] if f['id'] == est['id'])
        e.update(value=None, low=LOW, high=HIGH)
        o = next(f for f in a['figures'] if f['id'] == outcome['id'])
        o.update(value=None, low=36.0, high=43.0)
        a['answers'][0]['rung'] = rung
        a['answers'][0]['reasons'] = sentence + ' ' + a['answers'][0]['reasons']
        made[name] = a
    it = json.loads((out / 'E' / 'item.json').read_text())
    for name, a in made.items():
        result = cs.check(it['family'], it['passages'], cs.from_answer(a, it['family']))
        codes = sorted({c for c, _ in result['errors']})
        want = [] if name == 'C-overlap' else ['S6']
        if codes != want:
            raise SystemExit(f'{name}: the code gives {codes}, expected {want}; the control is not what it claims')
    return made


def build(out):
    rows = json.loads((out / 'CHECKED.json').read_text())
    items = [(r['case'], r['writer'], (out / r['case'] / 'answers' / f'{r["writer"]}.json').read_text()) for r in rows]
    for name, a in controls(out).items():
        items.append(('E', name, json.dumps(a, ensure_ascii=False)))
    seed = hashlib.sha256(b'D743 re-read ' + (out / 'CHECKED.json').read_bytes()).hexdigest()
    order = list(range(len(items)))
    random.Random(seed).shuffle(order)
    folder = out / 'reread-packets'
    folder.mkdir(exist_ok=False)
    key = {}
    for n, i in enumerate(order, 1):
        case, writer, raw = items[i]
        it = json.loads((out / case / 'item.json').read_text())
        pid = f'Q{n:02d}'
        key[pid] = {'case': case, 'writer': writer}
        (folder / f'{pid}.md').write_text(bt.READER_BRIEF + '\n# The request as the writer saw it\n\n' + it['user'] + '\n\n# The answer\n\n'
                                          + raw + '\n')
    (out / 'reread-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {folder}; key in reread-key.json (keep from readers)')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    build(Path(sys.argv[1]).resolve())
