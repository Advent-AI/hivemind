"""D742 replay on the saved refused reply (P-v4, Claude writer, re-run): the reply as written, two guidance resets (council 56 and 56b),
and the stated-estimate form council 56c asks for. $0. Usage: python3 s4_replay.py"""
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / 'src'))
import calc_small as cs  # noqa: E402
from hivemind import model  # noqa: E402

CASE = HERE.parents[2] / 'poc/data/judging-v13s-blind2-2026-11-22/P-v4'
item = json.loads((CASE / 'item.json').read_text())
saved = json.loads((CASE / 'answers/claude.json').read_text())
BLANK = {k: None for k in saved['figures'][0]}


def fig(answer, fid):
    return next(f for f in answer['figures'] if f['id'] == fid)


def new(**kw):
    f = dict(BLANK, outcome_for=[], reference_for=[])
    f.update(kw)
    return f


def total(a, q4):
    fig(a, 'F10').update(value=q4)
    fy = round(177.82 + 112.5 + q4, 2)
    fig(a, 'F11').update(value=fy)
    fig(a, 'F14').update(value=round((fy / 215.9 - 1) * 100, 2))
    return a


def reset_twice():                       # council 56: Q4 = Q2 x (108/96.2)^2, Q3 = 112.5 in the sum
    a = copy.deepcopy(saved)
    a['figures'].append(new(id='FX', what={'population': 'NVIDIA', 'measure': 'revenue sequential multiple', 'scope': 'company',
                                           'period': 'FY2027 Q3'}, kind='computed', basis='guidance', unit='x', value=1.1227,
                            inputs=['F4', 'F2'], operation='ratio'))
    fig(a, 'F10').update(inputs=['F2', 'FX', 'FX'], operation='product')
    return total(a, 121.25)


def reset_by_gap():                      # council 56b: base = F8 x (1 + growth(F8, F4)) = 108, then grown 12%
    a = copy.deepcopy(saved)
    a['figures'] += [new(id='FR', what={'population': 'NVIDIA', 'measure': 'revenue gap to guidance', 'scope': 'company', 'period': 'FY2027 Q3'},
                         kind='computed', basis='guidance', unit='%', value=-4.0, inputs=['F8', 'F4'], operation='growth'),
                     new(id='FB', what={'population': 'NVIDIA', 'measure': 'revenue base', 'scope': 'company', 'period': 'FY2027 Q3'},
                         kind='computed', basis='guidance', unit='USD bn', value=108.0, inputs=['F8', 'FR'], operation='apply_growth'),
                     new(id='FP', what={'population': 'NVIDIA', 'measure': 'revenue sequential growth', 'scope': 'company', 'period': 'FY2027 Q4'},
                         kind='estimate', basis='forecast', unit='%', value=12.0, basis_text='the guided pace', rests_on=['F9'])]
    fig(a, 'F10').update(inputs=['FB', 'FP'])
    return total(a, 120.96)


def stated_estimate():                   # council 56c: the chosen pace recorded as an estimate resting on the guided rate
    a = copy.deepcopy(saved)
    a['figures'].append(new(id='FE', what={'population': 'NVIDIA', 'measure': 'revenue sequential growth', 'scope': 'company',
                                           'period': 'FY2027 Q4'}, kind='estimate', basis='forecast', unit='%', value=12.27,
                            basis_text='Q4 keeps the guided Q2-to-Q3 pace: hyperscale demand reaccelerates as Rubin supply builds',
                            rests_on=['F9']))
    fig(a, 'F10').update(inputs=['F8', 'FE'])
    return total(a, 126.3)


for name, build, expect in [('the saved reply as written', lambda: copy.deepcopy(saved), 'S4'),
                            ('council 56 reset: the guided multiple applied twice to Q2', reset_twice, 'S4'),
                            ('council 56b reset: the forecast pulled back to guidance, then grown', reset_by_gap, 'S4'),
                            ('council 56c form: the chosen pace as a stated estimate', stated_estimate, 'pass')]:
    a = build()
    schema_errors = model.check_schema(a, item['schema'])
    calc = cs.from_answer(a, item['family'])
    result = cs.check(item['family'], item['passages'], calc)
    codes = sorted({c for c, _ in result['errors']}) or ['pass']
    got = ','.join(codes) if not schema_errors else 'schema'
    print(f'{"PASS" if got == expect else "FAIL"}  {name}: expected {expect}, got {got}; published {result["published"]}; '
          f'{[e[1] for e in result["errors"]][:1]}')
