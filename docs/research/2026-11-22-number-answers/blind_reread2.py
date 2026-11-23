"""The D744 second blinded re-read of a v13s blind run (SMALL-DESIGN.md §5 [D744]): the same first replies, read with the same rule text
adjudicators get (blind_rules: system text, every schema description, the definitions), plus five controls built from fresh copies:
K-midpoint and K-misread (P's Claude reply, its "plus or minus 2%" guidance as the midpoint 108 or as 108.5), K-overlap and K-disjoint
(E's Claude reply with a growth range giving $36-43B, rung 3 with its reason or rung 4, text made consistent), and K-unsupported (E's
Claude reply with a 140% growth estimate its own reasons argue against). Each control is checked by the code before it is used.

Usage: python3 blind_reread2.py <blind run folder>
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
import calc_small as cs  # noqa: E402
from blind_rules import DEFINITIONS, format_material  # noqa: E402

READER_BRIEF = """# Blind reading (judging-v13s blind test, second re-read, D744)

You are given one forecasting request (the questions, their ladders, and every passage the writer was shown), the system text and the
format rules the writer was given, and one answer written in that format. You are not told who wrote the answer or whether any check
accepted it. Read only what is given here.

Judge in two steps:
1. Check each source figure against its passage's quote and each computed figure against its inputs, using the format rules below.
   What the format rules permit is not a defect.
2. For each member, name the evidence for the assumption that puts the forecast in its band, and say whether the passages support it.

Return JSON:
{"members": {"<view id>": {"supported": "yes|no", "ground": "<the passage ids or the stated assumption that put the forecast in its band>",
                           "why_not": "<if no: what is missing or wrong>"}},
 "defects": [{"type": "<one of: number misread | wrong arithmetic | part above or added into its whole | two forecasts of one quarter |
               own estimate passed off as the market's reference | broken structure>", "figures": ["<figure ids>"], "detail": "..."}]}

""" + DEFINITIONS + """
Return an empty "defects" list when you find none. Return only JSON.
"""


def _fig(answer, fid):
    return next(f for f in answer['figures'] if f['id'] == fid)


def _replace(text, old, new):
    if text.count(old) != 1:
        raise SystemExit(f'control text: "{old[:60]}" occurs {text.count(old)} times')
    return text.replace(old, new)


def controls(out):
    made = {}
    p = json.loads((out / 'P' / 'answers' / 'claude.json').read_text())
    guide = next(f for f in p['figures'] if f.get('quote_number') == '$108.0 billion, plus or minus 2%')
    for name, value in (('K-midpoint', 108.0), ('K-misread', 108.5)):
        a = copy.deepcopy(p)
        _fig(a, guide['id']).update(value=value, low=None, high=None)
        made[name] = ('P', a, guide['id'])
    e = json.loads((out / 'E' / 'answers' / 'claude.json').read_text())
    old_reason = 'I forecast 85% growth (F7) on the $20 billion base, giving $37 billion (F8): rung 3 (Neutral), just below the rung-2 line.'
    for name, rung, reason in (
            ('K-overlap', 3, 'I forecast 80% to 115% growth (F7) on the $20 billion base, giving $36 billion to $43 billion (F8). Its midpoint, '
             'near $39.5 billion, and most of the range lie in rung 3 (Neutral), so I choose rung 3; the top of the range reaches rung 2.'),
            ('K-disjoint', 4, 'I forecast 80% to 115% growth (F7) on the $20 billion base, giving $36 billion to $43 billion (F8): rung 4.')):
        a = copy.deepcopy(e)
        f7, f8 = _fig(a, 'F7'), _fig(a, 'F8')
        f7.update(value=None, low=80.0, high=115.0, basis_text=_replace(f7['basis_text'], 'gives 85%.', 'gives 80% to 115%.'))
        f8.update(value=None, low=36.0, high=43.0)
        a['answers'][0].update(rung=rung, reasons=_replace(a['answers'][0]['reasons'], old_reason, reason))
        made[name] = ('E', a, 'F8')
    a = copy.deepcopy(e)
    _fig(a, 'F7').update(value=140.0, basis_text='My estimate of FY2028 Vera CPU revenue growth: 140%, because AI demand is strong.',
                         rests_on=['F2'])
    _fig(a, 'F8').update(value=48.0)
    a['answers'][0].update(rung=2, reasons=_replace(a['answers'][0]['reasons'], old_reason,
                                                    'I forecast 140% growth (F7) on the $20 billion base, giving $48 billion (F8): rung 2 (Bullish).'))
    made['K-unsupported'] = ('E', a, 'F7')
    expected = {'K-midpoint': [], 'K-misread': ['S1'], 'K-overlap': [], 'K-disjoint': ['S6'], 'K-unsupported': []}
    for name, (case, answer, _) in made.items():
        it = json.loads((out / case / 'item.json').read_text())
        codes = sorted({c for c, _ in cs.check(it['family'], it['passages'], cs.from_answer(answer, it['family']))['errors']})
        if codes != expected[name]:
            raise SystemExit(f'{name}: the code gives {codes}, expected {expected[name]}; the control is not what it claims')
    return made


def build(out):
    rows = json.loads((out / 'CHECKED.json').read_text())
    items = [{'case': r['case'], 'writer': r['writer'], 'answer': f'{r["case"]}/answers/{r["writer"]}.json'} for r in rows]
    folder = out / 'reread2-controls'
    folder.mkdir(exist_ok=False)
    for name, (case, answer, figure) in controls(out).items():
        (folder / f'{name}.json').write_text(json.dumps(answer, ensure_ascii=False))
        items.append({'case': case, 'writer': name, 'answer': f'reread2-controls/{name}.json', 'figure': figure})
    seed = hashlib.sha256(b'D744 second re-read ' + (out / 'CHECKED.json').read_bytes()).hexdigest()
    order = list(range(len(items)))
    random.Random(seed).shuffle(order)
    packets = out / 'reread2-packets'
    packets.mkdir(exist_ok=False)
    key = {}
    for n, i in enumerate(order, 1):
        item = items[i]
        it = json.loads((out / item['case'] / 'item.json').read_text())
        pid = f'T{n:02d}'
        key[pid] = item
        text = '\n'.join([READER_BRIEF, format_material(out / item['case']), '', '# The request as the writer saw it', '', it['user'], '',
                          '# The answer', '', (out / item['answer']).read_text(), ''])
        (packets / f'{pid}.md').write_text(text)
    (out / 'reread2-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {packets}; key in reread2-key.json (keep from readers)')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    build(Path(sys.argv[1]).resolve())
