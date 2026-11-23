"""The v13s small format's Part A cases (SMALL-DESIGN.md §5 [52], D738): A1 correct forms pass, A2 defects are refused by their named
rule (or recorded, where D738 says so), A3 Luna's observed mistakes are impossible under the schema or refused by their stated rule.
Each case runs the real path: the v13s schema (model.check_schema), calc_small.from_answer, calc_small.check. $0.
Usage: python3 small_cases.py   (prints one line per case; exit 1 on any failure)."""
import copy
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'src'))
if os.environ.get('CALC_SMALL_DIR'):                     # small_mutants.py: a mutated calc_small.py on a scratch copy
    sys.path.insert(0, os.environ['CALC_SMALL_DIR'])
import calc_small as cs  # noqa: E402
import render_v13 as rv  # noqa: E402
from hivemind import model  # noqa: E402

FIELDS = ['id', 'what', 'kind', 'basis', 'value', 'low', 'high', 'unit', 'evidence_id', 'quote_number', 'qualifier', 'inputs', 'operation',
          'basis_text', 'rests_on', 'outcome_for', 'reference_for']
PASSAGES = {
    'e1': 'First-quarter revenue was $81.6 billion, up 85% from a year ago.',
    'e2': 'Second-quarter revenue was $96.2 billion.',
    'e3': 'Revenue is expected to be $108.0 billion, plus or minus 2%.',
    'e4': 'Data Center revenue was $75.3 billion in the first quarter.',
    'e5': 'Data Center revenue was $89.0 billion in the second quarter, 92.5% of total revenue.',
    'e6': 'Analysts expect full-year revenue of $411 billion.',
    'e7': 'Data center revenue will be well over $300 billion next year.',
    'e8': 'and 65% growth in Q4.',
    'e9': 'Fourth-quarter revenue a year ago was $68.1 billion.',
    'e10': 'the company not only still expects $20 billion in sales, but roughly twice that number next year.',
    'e11': 'A plant costing $300 million or more is planned.',
    'e12': 'Margins moved -3% in the period.',
    'e13': 'Combined spending reached $1.2 trillion.',
    'e14': 'The bonds total US$10 billion; sales were $96.2bn; the range is between $105.84 billion and $110.16 billion.',
    'e15': 'The program costs €5 billion.',
    'e16': 'Spending will not be over $300 billion.',
    'e17': 'Unit prices rose 12% and volumes doubled.',
    'e18': 'Spending is tracked at $745 billion.',
    'e19': 'Another estimate puts spending at $760 billion.',
    'e20': 'The share is between 72% and 73% of the total.',
    'e21': 'The fund may invest as much as $10 billion.',
    'e22': 'Gross margin was 40% and the segment took 25% of it.',
    'e23': 'Analysts believe the market will grow fivefold between this year and 2030, from $35 billion to $170 billion.',
    'e24': 'Capex guidance ranges from $195 billion to $205 billion.',
    'e25': 'Analysts expect the segment to take 92% of revenue this year.',
    'e26': 'Tech giants will spend an estimated $750 billion this year.',
}
PASSAGES = {k: {'text': v, 'speaker': 'an outlet'} for k, v in PASSAGES.items()}
EVIDENCE = sorted(PASSAGES)


def W(scope, period, measure='revenue', population='NVIDIA'):
    return {'population': population, 'measure': measure, 'scope': scope, 'period': period}


PAIR = {'members': {'v4': {'what': W('company', 'FY2027'), 'unit': 'USD bn',
                           'bands': [[431.2, None], [392.0, 431.2], [352.8, 392.0], [313.6, 352.8], [None, 313.6]]},
                    'v8': {'what': W('Data Center', 'FY2027'), 'unit': 'USD bn',
                           'bands': [[400.0, None], [350.0, 400.0], [300.0, 350.0], [250.0, 300.0], [None, 250.0]]}},
        'relations': [{'type': 'part_of', 'part': 'v8', 'whole': 'v4'}],
        'shared': [W('company', 'FY2027 Q3'), W('company', 'FY2027 Q4')],
        'compare_periods': ['FY2027 Q3', 'FY2027 Q4', 'FY2027'],
        'part_scopes': [{'population': 'NVIDIA', 'measure': 'revenue', 'part': 'Data Center', 'whole': 'company'}]}


def F(id, what, kind, basis, unit, **kw):
    f = {k: None for k in FIELDS}
    f.update(id=id, what=what, kind=kind, basis=basis, unit=unit, outcome_for=[], reference_for=[])
    f.update(kw)
    return f


def A(view, shape='forecast', rung=None, reference_unavailable=None, why=None):
    return {'view_id': view, 'shape': shape, 'rung': rung, 'reference_unavailable': reference_unavailable, 'reasons': 'case',
            'why': why, 'cites': [], 'pushes': [], 'theme_pushes': []}


def base_pair():
    """A correct joint answer: company quarters, one shared Q3/Q4 forecast, Data Center quarters through share, a consensus reference."""
    figs = [
        F('F1', W('company', 'FY2027 Q1'), 'source', 'reported', 'USD bn', value=81.6, evidence_id='e1', quote_number='$81.6 billion', qualifier='none'),
        F('F2', W('company', 'FY2027 Q2'), 'source', 'reported', 'USD bn', value=96.2, evidence_id='e2', quote_number='$96.2 billion', qualifier='none'),
        F('F3', W('company', 'FY2027 Q3'), 'source', 'guidance', 'USD bn', value=108.0, evidence_id='e3',
          quote_number='$108.0 billion, plus or minus 2%', qualifier='none'),
        F('F4', W('company', 'FY2027 Q3'), 'estimate', 'forecast', 'USD bn', value=110.0, basis_text='a small beat on guidance', rests_on=['F3']),
        F('F5', W('company', 'FY2027 Q4'), 'estimate', 'forecast', 'USD bn', value=115.0, basis_text='growth continues', rests_on=['F4']),
        F('F6', W('company', 'FY2027'), 'computed', 'forecast', 'USD bn', value=402.8, inputs=['F1', 'F2', 'F4', 'F5'], operation='sum',
          outcome_for=['v4']),
        F('F7', W('Data Center', 'FY2027 Q1'), 'source', 'reported', 'USD bn', value=75.3, evidence_id='e4', quote_number='$75.3 billion', qualifier='none'),
        F('F8', W('Data Center', 'FY2027 Q2'), 'source', 'reported', 'USD bn', value=89.0, evidence_id='e5', quote_number='$89.0 billion', qualifier='none'),
        F('F9', W('Data Center', 'FY2027 Q2', measure='share of revenue'), 'source', 'reported', '%', value=92.5, evidence_id='e5',
          quote_number='92.5%', qualifier='none'),
        F('F10', W('Data Center', 'FY2027 Q3'), 'computed', 'forecast', 'USD bn', value=101.75, inputs=['F4', 'F9'], operation='share'),
        F('F11', W('Data Center', 'FY2027 Q4'), 'computed', 'forecast', 'USD bn', value=106.375, inputs=['F5', 'F9'], operation='share'),
        F('F12', W('Data Center', 'FY2027'), 'computed', 'forecast', 'USD bn', value=372.425, inputs=['F7', 'F8', 'F10', 'F11'], operation='sum',
          outcome_for=['v8']),
        F('F13', W('company', 'FY2027'), 'source', 'consensus', 'USD bn', value=411.0, evidence_id='e6', quote_number='$411 billion',
          qualifier='none', reference_for=['v4']),
    ]
    return {'figures': figs, 'answers': [A('v4', rung=2), A('v8', rung=2, reference_unavailable='no market figure for this segment')]}


def single(what, bands=((None, None),)):
    return {'members': {'s': {'what': what, 'unit': 'USD bn', 'bands': [list(b) for b in bands]}}, 'relations': [], 'shared': [],
            'compare_periods': [], 'part_scopes': []}


def one(figs, rung=1, family=None, reference_unavailable='none shown'):
    fam = family or single(figs[-1]['what'], ((None, None),))
    return {'figures': figs, 'answers': [A('s', rung=rung, reference_unavailable=reference_unavailable)]}, fam


def run(answer, family, passages=PASSAGES):
    members = sorted(family['members'])
    schema = rv.v13s_schema(members, EVIDENCE, [])
    schema_errors = model.check_schema(answer, schema)
    if schema_errors:
        return {'schema': schema_errors}
    calc = cs.from_answer(answer, family)
    return cs.check(family, passages, calc)


def fig(answer, fid):
    return next(f for f in answer['figures'] if f['id'] == fid)


CASES = []


MESSAGES = {}


def case(group, name, expect, recorded=None, message=None):
    def wrap(build):
        CASES.append((group, name, expect, recorded, build))
        if message:
            MESSAGES[name] = message                     # the intended refusal's own words, where another rule could also refuse
        return build
    return wrap


# ---------- A1: correct forms pass ----------
@case('A1', 'the base joint answer', 'pass')
def _():
    return base_pair(), PAIR


@case('A1', '$108.0B ± 2% as a range (low and high)', 'pass')
def _():
    a = base_pair()
    fig(a, 'F3').update(value=None, low=105.84, high=110.16)
    return a, PAIR


@case('A1', 'Q1 + Q2 = H1, then H1 + Q3 + Q4 = FY', 'pass')
def _():
    a = base_pair()
    a['figures'].append(F('H1', W('company', 'FY2027 H1'), 'computed', 'reported', 'USD bn', value=177.8, inputs=['F1', 'F2'], operation='sum'))
    fig(a, 'F6').update(inputs=['H1', 'F4', 'F5'])
    return a, PAIR


@case('A1', 'FY − Q1-Q3 = Q4 (a residual)', 'pass')
def _():
    a = base_pair()
    a['figures'] += [F('N9', W('company', 'FY2027 Q1-Q3'), 'computed', 'forecast', 'USD bn', value=287.8, inputs=['F1', 'F2', 'F4'], operation='sum'),
                     F('C4', W('company', 'FY2027 Q4'), 'computed', 'consensus', 'USD bn', value=123.2, inputs=['F13', 'N9'], operation='difference')]
    return a, PAIR


@case('A1', 'a year-over-year rate on last year\'s quarter (recorded, not refused)', 'pass', recorded='carried across periods')
def _():
    figs = [F('B', W('company', 'FY2026 Q4'), 'source', 'reported', 'USD bn', value=68.1, evidence_id='e9', quote_number='$68.1 billion', qualifier='none'),
            F('G', W('company', 'FY2027 Q4', measure='revenue growth'), 'source', 'third_party', '%', value=65.0, evidence_id='e8', quote_number='65%', qualifier='none'),
            F('O', W('company', 'FY2027 Q4'), 'computed', 'forecast', 'USD bn', value=112.365, inputs=['B', 'G'], operation='apply_growth', outcome_for=['s'])]
    return one(figs)


@case('A1', 'a whole times a mix through share', 'pass')
def _():
    a = base_pair()
    return a, PAIR


@case('A1', '"over $300 billion" (from "well over $300 billion") with qualifier over', 'pass', recorded='qualified source')
def _():
    figs = [F('S', W('Data Center', 'FY2028'), 'source', 'third_party', 'USD bn', value=300.0, evidence_id='e7', quote_number='$300 billion', qualifier='over'),
            F('O', W('Data Center', 'FY2028'), 'estimate', 'forecast', 'USD bn', value=320.0, basis_text='above the outside figure', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A1', '"-3%" as written', 'pass')
def _():
    figs = [F('S', W('company', 'FY2027', measure='margin change'), 'source', 'reported', '%', value=-3.0, evidence_id='e12', quote_number='-3%', qualifier='none'),
            F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=10.0, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A1', '"$300 million or more" with qualifier "or more"', 'pass')
def _():
    figs = [F('S', W('plant', 'FY2027', measure='cost'), 'source', 'reported', 'USD bn', value=0.3, evidence_id='e11', quote_number='$300 million', qualifier='or more'),
            F('O', W('plant', 'FY2027', measure='cost'), 'estimate', 'forecast', 'USD bn', value=0.35, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A1', '"an estimated $750 billion" with qualifier "estimated" [D745]', 'pass')
def _():
    figs = [F('S', W('tech giants', 'CY2026', measure='data-center spending'), 'source', 'third_party', 'USD bn', value=750.0, evidence_id='e26',
              quote_number='$750 billion', qualifier='estimated'),
            F('O', W('tech giants', 'CY2026', measure='data-center spending'), 'estimate', 'forecast', 'USD bn', value=740.0, basis_text='x',
              rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A2', '"an estimated $750 billion" recorded with qualifier "none" (S1) [D745]', 'S1')
def _():
    figs = [F('S', W('tech giants', 'CY2026', measure='data-center spending'), 'source', 'third_party', 'USD bn', value=750.0, evidence_id='e26',
              quote_number='$750 billion', qualifier='none'),
            F('O', W('tech giants', 'CY2026', measure='data-center spending'), 'estimate', 'forecast', 'USD bn', value=740.0, basis_text='x',
              rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A1', '$1.2 trillion as 1200 USD bn', 'pass')
def _():
    figs = [F('S', W('four companies', 'CY2026', measure='capex'), 'source', 'reported', 'USD bn', value=1200.0, evidence_id='e13', quote_number='$1.2 trillion', qualifier='none'),
            F('O', W('four companies', 'CY2026', measure='capex'), 'estimate', 'forecast', 'USD bn', value=1250.0, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs, family=single(W('four companies', 'CY2026', measure='capex'), ((1000.0, 1500.0),)))


@case('A1', 'a range outcome overlapping its rung', 'pass')
def _():
    figs = [F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', low=380.0, high=400.0, basis_text='a range', outcome_for=['s'])]
    return one(figs, rung=2, family=single(W('company', 'FY2027'), ((400.0, None), (350.0, 400.0))))


@case('A1', 'one figure marked for two members', 'pass')
def _():
    fam = {'members': {'a': {'what': W('company', 'FY2027'), 'unit': 'USD bn', 'bands': [[None, None]]},
                       'b': {'what': W('company', 'FY2027'), 'unit': 'USD bn', 'bands': [[None, None]]}},
           'relations': [], 'shared': [], 'compare_periods': [], 'part_scopes': []}
    figs = [F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=400.0, basis_text='x', outcome_for=['a', 'b'])]
    return {'figures': figs, 'answers': [A('a', rung=1, reference_unavailable='none'), A('b', rung=1, reference_unavailable='none')]}, fam


@case('A2', '[D741] consensus total × a past quarter\'s reported share marked as the market reference (S5)', 'S5')
def _():
    a = base_pair()
    a['figures'].append(F('R8', W('Data Center', 'FY2027'), 'computed', 'consensus', 'USD bn', value=380.175, inputs=['F13', 'F9'], operation='share',
                          reference_for=['v8']))
    a['answers'][1]['reference_unavailable'] = None
    return a, PAIR


@case('A1', '[D741] consensus total × an outside full-year share as the market reference', 'pass')
def _():
    a = base_pair()
    a['figures'] += [F('SH', W('Data Center', 'FY2027', measure='share of revenue'), 'source', 'consensus', '%', value=92.0, evidence_id='e25',
                       quote_number='92%', qualifier='none'),
                     F('R8', W('Data Center', 'FY2027'), 'computed', 'consensus', 'USD bn', value=378.12, inputs=['F13', 'SH'], operation='share',
                       reference_for=['v8'])]
    a['answers'][1]['reference_unavailable'] = None
    return a, PAIR


@case('A1', '[D740] "from $35 billion to $170 billion": each amount copied alone', 'pass')
def _():
    figs = [F('S1', W('market', 'CY2026'), 'source', 'third_party', 'USD bn', value=35.0, evidence_id='e23', quote_number='$35 billion', qualifier='none'),
            F('S2', W('market', 'CY2030'), 'source', 'third_party', 'USD bn', value=170.0, evidence_id='e23', quote_number='$170 billion', qualifier='none'),
            F('O', W('market', 'CY2026'), 'estimate', 'forecast', 'USD bn', value=36.0, basis_text='near the outside figure', rests_on=['S1', 'S2'],
              outcome_for=['s'])]
    return one(figs)


@case('A2', '[D740] "from $35 billion to $170 billion" copied as one range (S1)', 'S1')
def _():
    figs = [F('S1', W('market', 'CY2026'), 'source', 'third_party', 'USD bn', low=35.0, high=170.0, evidence_id='e23',
              quote_number='$35 billion to $170 billion', qualifier='none'),
            F('O', W('market', 'CY2026'), 'estimate', 'forecast', 'USD bn', value=36.0, basis_text='x', rests_on=['S1'], outcome_for=['s'])]
    return one(figs)


@case('A1', '[D740] "ranges from $195 billion to $205 billion" is one range', 'pass')
def _():
    figs = [F('S1', W('company', 'CY2026', measure='capex'), 'source', 'guidance', 'USD bn', low=195.0, high=205.0, evidence_id='e24',
              quote_number='$195 billion to $205 billion', qualifier='none'),
            F('O', W('company', 'CY2026', measure='capex'), 'estimate', 'forecast', 'USD bn', value=200.0, basis_text='the midpoint', rests_on=['S1'],
              outcome_for=['s'])]
    return one(figs)


@case('A1', 'an unresolved member', 'pass')
def _():
    a = base_pair()
    a['figures'] = [f for f in a['figures'] if f['id'] not in ('F7', 'F8', 'F10', 'F11', 'F12')]
    a['answers'][1] = A('v8', shape='unresolved', why='no segment figure is shown')
    return a, PAIR


@case('A1', 'a conversion between quantities (recorded, not refused)', 'pass', recorded='conversion between quantities')
def _():
    figs = [F('S1', W('four companies', 'CY2026', measure='capex'), 'source', 'third_party', 'USD bn', value=745.0, evidence_id='e18',
              quote_number='$745 billion', qualifier='none'),
            F('M', W('four companies', 'CY2026', measure='data-center share'), 'estimate', 'forecast', 'x', value=0.8, basis_text='most capex is data centers'),
            F('O', W('four companies', 'CY2026', measure='data-center capex'), 'computed', 'forecast', 'USD bn', value=596.0, inputs=['S1', 'M'],
              operation='product', outcome_for=['s'])]
    return one(figs)


@case('A1', '"not only still expects $20 billion" as a source, "roughly twice" as a multiple', 'pass')
def _():
    figs = [F('B', W('company', 'FY2027', measure='CPU sales'), 'source', 'guidance', 'USD bn', value=20.0, evidence_id='e10', quote_number='$20 billion', qualifier='none'),
            F('X', W('company', 'FY2028', measure='CPU sales multiple'), 'source', 'guidance', 'x', value=2.0, evidence_id='e10', quote_number='twice', qualifier='roughly'),
            F('O', W('company', 'FY2028', measure='CPU sales'), 'computed', 'forecast', 'USD bn', value=40.0, inputs=['B', 'X'], operation='product', outcome_for=['s'])]
    return one(figs)


@case('A1', '12% × 2x = 24%', 'pass')
def _():
    figs = [F('P', W('unit', 'FY2027', measure='price change'), 'source', 'reported', '%', value=12.0, evidence_id='e17', quote_number='12%', qualifier='none'),
            F('X', W('unit', 'FY2027', measure='factor'), 'estimate', 'forecast', 'x', value=2.0, basis_text='two steps'),
            F('Q', W('unit', 'FY2027', measure='price change'), 'computed', 'forecast', '%', value=24.0, inputs=['P', 'X'], operation='product'),
            F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=10.0, basis_text='x', rests_on=['Q'], outcome_for=['s'])]
    return one(figs)


@case('A1', 'US$10 billion, $96.2bn, a written range', 'pass')
def _():
    figs = [F('A1', W('bonds', 'FY2027', measure='size'), 'source', 'reported', 'USD bn', value=10.0, evidence_id='e14', quote_number='US$10 billion', qualifier='none'),
            F('A2', W('company', 'FY2027 Q2'), 'source', 'reported', 'USD bn', value=96.2, evidence_id='e14', quote_number='$96.2bn', qualifier='none'),
            F('A3', W('company', 'FY2027 Q3'), 'source', 'guidance', 'USD bn', low=105.84, high=110.16, evidence_id='e14',
              quote_number='between $105.84 billion and $110.16 billion', qualifier='none'),
            F('O', W('company', 'FY2027 Q3'), 'computed', 'forecast', 'USD bn', value=108.0, inputs=['A3', 'A3'], operation='sum'),
            ]
    figs[-1].update(inputs=['A3'], operation='sum')
    figs[-1].update(kind='estimate', inputs=None, operation=None, basis_text='the midpoint', rests_on=['A3'], outcome_for=['s'])
    return one(figs)


@case('A1', 'a point Data Center forecast beside a company range (lowest against highest)', 'pass')
def _():
    a = base_pair()
    fig(a, 'F4').update(value=None, low=105.84, high=110.16)
    fig(a, 'F10').update(kind='estimate', basis_text='segment stays near its mix', inputs=None, operation=None, value=100.0, rests_on=['F4'])
    fig(a, 'F6').update(value=None, low=398.64, high=402.96)
    fig(a, 'F12').update(value=370.675)
    return a, PAIR


@case('A1', 'a final range estimate resting on a computed point of the same quantity', 'pass', recorded='one quantity, several figures')
def _():
    a = base_pair()
    fig(a, 'F12').update(outcome_for=[])                 # the computed point keeps basis forecast: the final range is the value adopted
    a['figures'].append(F('R', W('Data Center', 'FY2027'), 'estimate', 'forecast', 'USD bn', low=360.0, high=385.0, basis_text='a range around it',
                          rests_on=['F12'], outcome_for=['v8']))
    return a, PAIR


@case('A1', 'two outside estimates averaged into one starting point', 'pass')
def _():
    figs = [F('S1', W('four companies', 'CY2026', measure='capex'), 'source', 'third_party', 'USD bn', value=745.0, evidence_id='e18', quote_number='$745 billion', qualifier='none'),
            F('S2', W('four companies', 'CY2026', measure='capex'), 'source', 'third_party', 'USD bn', value=760.0, evidence_id='e19', quote_number='$760 billion', qualifier='none'),
            F('T', W('four companies', 'CY2026', measure='capex, two sources'), 'computed', 'third_party', 'USD bn', value=1505.0, inputs=['S1', 'S2'], operation='sum'),
            F('H', W('four companies', 'CY2026', measure='capex'), 'computed', 'forecast', 'USD bn', value=752.5, inputs=['T', 'D'], operation='ratio'),
            F('D', W('four companies', 'CY2026', measure='divisor'), 'estimate', 'forecast', 'x', value=2.0, basis_text='two sources'),
            F('O', W('four companies', 'CY2026', measure='capex'), 'estimate', 'forecast', 'USD bn', value=752.5, basis_text='the average', rests_on=['H'], outcome_for=['s'])]
    figs[3]['basis'] = 'third_party'
    return one(figs)


@case('A1', 'the remainder: company − Data Center = the rest', 'pass')
def _():
    a = base_pair()
    a['figures'].append(F('REST', W('other', 'FY2027'), 'computed', 'forecast', 'USD bn', value=30.375, inputs=['F6', 'F12'], operation='difference'))
    return a, PAIR


@case('A1', 'a guidance-implied growth rate as the stated benchmark of a Q4 estimate (D741 ruling 1) [D742]', 'pass')
def _():
    a = base_pair()
    a['figures'].append(F('G', W('company', 'FY2027 Q3', measure='revenue sequential growth'), 'computed', 'guidance', '%', value=12.27, inputs=['F2', 'F3'], operation='growth'))
    fig(a, 'F5').update(basis_text='Q4 grows about 13%, a little above the guided Q2-to-Q3 pace', rests_on=['F4', 'G'], value=124.3)
    fig(a, 'F6').update(value=412.1)
    fig(a, 'F11').update(value=114.9775)
    fig(a, 'F12').update(value=381.0275)
    return a, PAIR


# ---------- A2: defects are refused by their named rule ----------
def defect(name, rule, mutate, family=PAIR, base=base_pair, recorded=None):
    @case('A2', name, rule, recorded)
    def _():
        a = base()
        mutate(a)
        return a, family


defect('108.5 for "$108.0 billion" (S1)', 'S1', lambda a: fig(a, 'F3').update(value=108.5))
defect('a qualifier the quote does not write (S1)', 'S1', lambda a: fig(a, 'F1').update(qualifier='about'))
defect('a number not written in the quote (S1)', 'S1', lambda a: fig(a, 'F1').update(quote_number='$81.62 billion', value=81.62))
defect('"± 2%" read as a positive point 110.16 (S1)', 'S1', lambda a: fig(a, 'F3').update(value=110.16))
defect('a plain wrong sum (S2)', 'S2', lambda a: fig(a, 'F6').update(value=410.0))
defect('money × % through product (S2)', 'S2', lambda a: fig(a, 'F10').update(operation='product'))
defect('a three-input difference (S7)', 'S7', lambda a: fig(a, 'F6').update(operation='difference'))
defect('a part forecast above the whole for Q3 (S3)', 'S3', lambda a: (fig(a, 'F9').update(value=92.5), fig(a, 'F10').update(
    kind='estimate', basis_text='segment', inputs=None, operation=None, value=112.0, rests_on=['F4']), fig(a, 'F12').update(value=382.675)))
defect('a part outcome above the whole outcome (S3)', 'S3', lambda a: (fig(a, 'F12').update(
    kind='estimate', basis_text='segment', inputs=None, operation=None, value=405.0, rests_on=['F10']), a['answers'][1].update(rung=1)))
defect('Data Center added into company in one sum (S8)', 'S8', lambda a: a['figures'].append(F(
    'BAD', W('company', 'FY2027'), 'computed', 'forecast', 'USD bn', value=775.225, inputs=['F6', 'F12'], operation='sum')))
defect('Q2 + Q3 labelled H1 (S8)', 'S8', lambda a: a['figures'].append(F(
    'BAD', W('company', 'FY2027 H1'), 'computed', 'forecast', 'USD bn', value=206.2, inputs=['F2', 'F4'], operation='sum')))
defect('FY − Q1 labelled Q4 (S8)', 'S8', lambda a: a['figures'].append(F(
    'BAD', W('company', 'FY2027 Q4'), 'computed', 'consensus', 'USD bn', value=329.4, inputs=['F13', 'F1'], operation='difference')))
defect('two forecasts of one shared quarter, both used (S4)', 'S4', lambda a: (a['figures'].append(F(
    'BAD', W('company', 'FY2027 Q3'), 'estimate', 'forecast', 'USD bn', value=112.0, basis_text='another view')),
    fig(a, 'F10').update(inputs=['BAD', 'F9'], value=103.6), fig(a, 'F12').update(value=374.275)))
defect('an unused second forecast of a quarter is not counted (passes)', 'pass', lambda a: a['figures'].append(F(
    'ALT', W('company', 'FY2027 Q3'), 'estimate', 'forecast', 'USD bn', value=112.0, basis_text='an alternative not used')))
defect('Q3 guidance used directly beside the Q3 forecast (S4)', 'S4', lambda a: fig(a, 'F10').update(inputs=['F3', 'F9'], value=99.9))
defect('a guidance-implied rate computed straight into Q4, not through an estimate (S4, stated) [D742]', 'S4', lambda a: (a['figures'].append(
    F('G', W('company', 'FY2027 Q3', measure='revenue sequential growth'), 'computed', 'guidance', '%', value=12.27, inputs=['F2', 'F3'], operation='growth')),
    fig(a, 'F5').update(kind='computed', basis_text=None, rests_on=None, inputs=['F4', 'G'], operation='apply_growth', value=123.49),
    fig(a, 'F6').update(value=411.29), fig(a, 'F11').update(value=114.23), fig(a, 'F12').update(value=380.28)))
defect('Q4 built on the guided Q3 through the guided multiple applied twice to Q2 (S4) [D742]', 'S4', lambda a: (a['figures'].append(
    F('X', W('company', 'FY2027 Q3', measure='revenue sequential multiple'), 'computed', 'guidance', 'x', value=1.1227, inputs=['F3', 'F2'], operation='ratio')),
    fig(a, 'F5').update(kind='computed', basis_text=None, rests_on=None, inputs=['F2', 'X', 'X'], operation='product', value=121.25),
    fig(a, 'F6').update(value=409.05), fig(a, 'F11').update(value=112.16), fig(a, 'F12').update(value=378.21)))
defect('Q4 grown from a run-rate rebuilt from Q2 at the guided rate (S4) [D742]', 'S4', lambda a: (a['figures'].extend([
    F('G', W('company', 'FY2027 Q3', measure='revenue sequential growth'), 'computed', 'guidance', '%', value=12.27, inputs=['F2', 'F3'], operation='growth'),
    F('T', W('company', 'FY2027 Q3', measure='revenue run-rate'), 'computed', 'guidance', 'USD bn', value=108.0, inputs=['F2', 'G'], operation='apply_growth')]),
    fig(a, 'F5').update(kind='computed', basis_text=None, rests_on=None, inputs=['T', 'G'], operation='apply_growth', value=121.25),
    fig(a, 'F6').update(value=409.05), fig(a, 'F11').update(value=112.16), fig(a, 'F12').update(value=378.21)))
defect('the forecast reset to guidance by its own growth to guidance, then grown (S4) [D742]', 'S4', lambda a: (a['figures'].extend([
    F('R', W('company', 'FY2027 Q3', measure='revenue gap to guidance'), 'computed', 'guidance', '%', value=-1.82, inputs=['F4', 'F3'], operation='growth'),
    F('B', W('company', 'FY2027 Q3', measure='revenue base'), 'computed', 'guidance', 'USD bn', value=108.0, inputs=['F4', 'R'], operation='apply_growth'),
    F('P', W('company', 'FY2027 Q4', measure='revenue sequential growth'), 'source', 'reported', '%', value=12.0, evidence_id='e17',
      quote_number='12%', qualifier='none')]),
    fig(a, 'F5').update(kind='computed', basis_text=None, rests_on=None, inputs=['B', 'P'], operation='apply_growth', value=120.96),
    fig(a, 'F6').update(value=408.76), fig(a, 'F11').update(value=111.888), fig(a, 'F12').update(value=377.938)))
defect('two Data Center Q4 forecasts, both used (S4)', 'S4', lambda a: (a['figures'].append(F(
    'BAD', W('Data Center', 'FY2027 Q4'), 'estimate', 'forecast', 'USD bn', value=104.0, basis_text='another view')),
    fig(a, 'F12').update(outcome_for=[]), a['figures'].append(F('X', W('Data Center', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=372.0,
                                                                basis_text='near the sum', rests_on=['F12', 'BAD'], outcome_for=['v8']))))
defect('an estimate marked as the reference (S5)', 'S5', lambda a: (a['figures'].append(F(
    'R8', W('Data Center', 'FY2027'), 'estimate', 'reported', 'USD bn', value=380.0, basis_text='looks like consensus', rests_on=['F13'],
    reference_for=['v8'])), a['answers'][1].update(reference_unavailable=None)))
defect('a computed reference with basis forecast (S5)', 'S5', lambda a: (a['figures'].append(F(
    'SH', W('Data Center', 'FY2027', measure='share of revenue'), 'source', 'consensus', '%', value=92.0, evidence_id='e25', quote_number='92%',
    qualifier='none')), a['figures'].append(F(
    'R8', W('Data Center', 'FY2027 consensus view'), 'computed', 'forecast', 'USD bn', value=378.12, inputs=['F13', 'SH'], operation='share',
    reference_for=['v8'])), a['answers'][1].update(reference_unavailable=None)))      # an outside full-year share: only the forecast basis refuses it
defect('a reference resting on an estimate (S5)', 'S5', lambda a: (a['figures'].append(F(
    'R8', W('Data Center', 'FY2027'), 'computed', 'consensus', 'USD bn', value=373.45, inputs=['F13', 'M'], operation='share',
    reference_for=['v8'])), a['figures'].append(F('M', W('Data Center', 'FY2027', measure='mix'), 'estimate', 'forecast', '%', value=90.86,
                                                    basis_text='mix')), a['answers'][1].update(reference_unavailable=None)))
defect('a reported-only reference (S5)', 'S5', lambda a: (fig(a, 'F1').update(reference_for=['v8']), a['answers'][1].update(reference_unavailable=None)))
defect('both a reference figure and a reason (S5)', 'S5', lambda a: a['answers'][0].update(reference_unavailable='also none'))
defect('neither a reference figure nor a reason (S5)', 'S5', lambda a: a['answers'][1].update(reference_unavailable=None))
defect('no outcome marker (S6)', 'S6', lambda a: fig(a, 'F12').update(outcome_for=[]))
defect('two outcome markers (S6)', 'S6', lambda a: fig(a, 'F11').update(outcome_for=['v8']))
defect('a marker on an unresolved member (S7)', 'S7', lambda a: a['answers'][1].update(shape='unresolved', why='none', rung=None,
                                                                                     reference_unavailable=None))
defect('an outcome key mismatch (S6)', 'S6', lambda a: fig(a, 'F12').update(what=W('Data Center', 'FY2027', population='NVIDIA Corp')))
defect('a source as the outcome (S6)', 'S6', lambda a: (fig(a, 'F12').update(outcome_for=[]), a['figures'].append(F(
    'SRC', W('Data Center', 'FY2027'), 'source', 'third_party', 'USD bn', value=300.0, evidence_id='e7', quote_number='$300 billion',
    qualifier='over', outcome_for=['v8'])), a['answers'][1].update(rung=3)))
defect('a share above 100% (S2)', 'S2', lambda a: (fig(a, 'F9').update(kind='estimate', basis='forecast', evidence_id=None, quote_number=None,
    qualifier=None, value=110.0, basis_text='mix'), fig(a, 'F10').update(value=121.0), fig(a, 'F11').update(value=126.5),
    fig(a, 'F12').update(value=411.8)))
defect('a rung outside the ladder (S6)', 'S6', lambda a: a['answers'][0].update(rung=9))
defect('a rung whose band misses the outcome (S6)', 'S6', lambda a: a['answers'][0].update(rung=1))
defect('a declared value within tolerance whose recomputed value crosses the edge (S6)', 'S6', lambda a: (
    fig(a, 'F5').update(value=104.3), fig(a, 'F6').update(value=391.9), a['answers'][0].update(rung=3),
    fig(a, 'F11').update(value=96.4775), fig(a, 'F12').update(value=362.5275)))
defect('value with low (S7)', 'S7', lambda a: fig(a, 'F1').update(low=80.0))
defect('a cycle through rests_on (S7)', 'S7', lambda a: fig(a, 'F4').update(rests_on=['F5']))
defect('a passage id in inputs (S7)', 'S7', lambda a: fig(a, 'F6').update(inputs=['F1', 'e2', 'F4', 'F5']))
defect('a source with basis forecast (S7)', 'S7', lambda a: fig(a, 'F3').update(basis='forecast'))
defect('duplicate member answers (S7)', 'S7', lambda a: a['answers'].append(A('v4', rung=2)))
defect('a figure id equal to a passage id (S7)', 'S7', lambda a: a['figures'].append(F(
    'e1', W('company', 'FY2027 Q1'), 'estimate', 'reported', 'USD bn', value=81.6, basis_text='copy')))
defect('an estimate resting on both part and whole (recorded, not refused)', 'pass', lambda a: a['figures'].append(F(
    'BOTH', W('company', 'FY2027', measure='combined'), 'estimate', 'forecast', 'USD bn', value=775.0, basis_text='both', rests_on=['F6', 'F12'])),
    recorded='part and whole in one estimate')
defect('Data Center × 1x added to company (recorded as a conversion, not refused: D738)', 'pass', lambda a: a['figures'] + [
    a['figures'].append(F('ONE', W('company', 'FY2027', measure='factor'), 'estimate', 'forecast', 'x', value=1.0, basis_text='one')),
    a['figures'].append(F('ADJ', W('company', 'FY2027', measure='revenue adjustment'), 'computed', 'forecast', 'USD bn', value=372.425,
                          inputs=['F12', 'ONE'], operation='product'))], recorded='conversion between quantities')


@case('A2', 'division by a range that contains zero (S2)', 'S2', message='can be zero')
def _():
    figs = [F('Z', W('a', 'FY2027', measure='z'), 'estimate', 'forecast', 'x', low=-1.0, high=1.0, basis_text='z'),
            F('N', W('a', 'FY2027', measure='n'), 'estimate', 'forecast', 'USD bn', value=10.0, basis_text='n'),
            F('O', W('a', 'FY2027'), 'computed', 'forecast', 'USD bn', value=0.0, inputs=['N', 'Z'], operation='ratio', outcome_for=['s'])]
    return one(figs)                                     # 0.0 is the midpoint of the vertices: only the zero-divisor rule refuses it


@case('A2', '[-3, -2] × [2, 4] declared other than [-12, -4] (S2)', 'S2')
def _():
    figs = [F('P', W('a', 'FY2027', measure='p'), 'estimate', 'forecast', 'x', low=-3.0, high=-2.0, basis_text='p'),
            F('Q', W('a', 'FY2027', measure='q'), 'estimate', 'forecast', 'x', low=2.0, high=4.0, basis_text='q'),
            F('R', W('a', 'FY2027', measure='r'), 'computed', 'forecast', 'x', low=-8.0, high=-6.0, inputs=['P', 'Q'], operation='product'),
            F('O', W('a', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=1.0, basis_text='o', rests_on=['R'], outcome_for=['s'])]
    return one(figs)


@case('A2', 'a figure used twice takes one value: ratio(F, F) over a range is 1, not a spread (passes)', 'pass')
def _():
    figs = [F('P', W('a', 'FY2027', measure='p'), 'estimate', 'forecast', 'USD bn', low=50.0, high=150.0, basis_text='p'),
            F('R', W('a', 'FY2027', measure='r'), 'computed', 'forecast', 'x', value=1.0, inputs=['P', 'P'], operation='ratio'),
            F('O', W('a', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=1.0, basis_text='o', rests_on=['R'], outcome_for=['s'])]
    return one(figs)


@case('A2', 'a euro amount as a source (S1)', 'S1')
def _():
    figs = [F('S', W('program', 'FY2027', measure='cost'), 'source', 'reported', 'USD bn', value=5.0, evidence_id='e15', quote_number='€5 billion', qualifier='none'),
            F('O', W('program', 'FY2027', measure='cost'), 'estimate', 'forecast', 'USD bn', value=5.0, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A2', 'trillions written as 1.2 USD bn (S1)', 'S1')
def _():
    figs = [F('S', W('four companies', 'CY2026', measure='capex'), 'source', 'reported', 'USD bn', value=1.2, evidence_id='e13', quote_number='$1.2 trillion', qualifier='none'),
            F('O', W('four companies', 'CY2026', measure='capex'), 'estimate', 'forecast', 'USD bn', value=1.25, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A2', '"-3%" taken as 3 (S1)', 'S1')
def _():
    figs = [F('S', W('company', 'FY2027', measure='margin change'), 'source', 'reported', '%', value=3.0, evidence_id='e12', quote_number='3%', qualifier='none'),
            F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=10.0, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A2', 'a qualifier dropped: "over $300 billion" as none (S1)', 'S1')
def _():
    figs = [F('S', W('Data Center', 'FY2028'), 'source', 'third_party', 'USD bn', value=300.0, evidence_id='e7', quote_number='$300 billion', qualifier='none'),
            F('O', W('Data Center', 'FY2028'), 'estimate', 'forecast', 'USD bn', value=320.0, basis_text='x', rests_on=['S'], outcome_for=['s'])]
    return one(figs)


@case('A2', 'an outcome at the band\'s upper edge (S6)', 'S6')
def _():
    figs = [F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=400.0, basis_text='x', outcome_for=['s'])]
    return one(figs, rung=2, family=single(W('company', 'FY2027'), ((400.0, None), (350.0, 400.0))))


# ---------- [54] round 54's counterexamples, each beside its correct form ----------
defect('"5%" copied out of "85%" (S1)', 'S1', lambda a: a['figures'].append(F(
    'G', W('company', 'FY2027 Q1', measure='growth'), 'source', 'reported', '%', value=5.0, evidence_id='e1', quote_number='5%', qualifier='none')))
defect('"$108.0 billion" copied alone from "$108.0 billion, plus or minus 2%" (S1)', 'S1',
       lambda a: fig(a, 'F3').update(quote_number='$108.0 billion'))
defect('"2%" copied out of "plus or minus 2%" (S1)', 'S1', lambda a: a['figures'].append(F(
    'T', W('company', 'FY2027 Q3', measure='tolerance'), 'source', 'guidance', '%', value=2.0, evidence_id='e3', quote_number='2%', qualifier='none')))
defect('one end copied out of a written range (S1)', 'S1', lambda a: a['figures'].append(F(
    'L', W('company', 'FY2027 Q3'), 'source', 'guidance', 'USD bn', value=105.84, evidence_id='e14', quote_number='$105.84 billion', qualifier='none')))
defect('rests_on on a reported figure (S7)', 'S7', lambda a: fig(a, 'F1').update(rests_on=['e6']))
defect('inputs on an estimate (S7)', 'S7', lambda a: fig(a, 'F4').update(inputs=['F3']))
defect('a number that is not finite (S7)', 'S7', lambda a: fig(a, 'F4').update(value=1e300 * 1e300))
defect('the remainder taken across periods: company Q3 − Data Center Q2 (S8)', 'S8', lambda a: a['figures'].append(F(
    'REST', W('other', 'FY2027 Q3'), 'computed', 'forecast', 'USD bn', value=21.0, inputs=['F4', 'F8'], operation='difference')))
defect('one period added twice: Q1 + Q2 + Q2 labelled H1 (S8)', 'S8', lambda a: a['figures'].append(F(
    'H1', W('company', 'FY2027 H1'), 'computed', 'reported', 'USD bn', value=274.0, inputs=['F1', 'F2', 'F2'], operation='sum')))
defect('one period added twice in plain words (S8)', 'S8', lambda a: (a['figures'].append(F(
    'Pa', W('company', 'second quarter'), 'estimate', 'reported', 'USD bn', value=96.2, basis_text='copy')), a['figures'].append(F(
    'Pb', W('company', 'first half'), 'computed', 'reported', 'USD bn', value=192.4, inputs=['Pa', 'Pa'], operation='sum'))))
defect('a part above its whole at one end of a linked range: part = 215 − whole (S3)', 'S3', lambda a: (
    fig(a, 'F4').update(value=None, low=105.84, high=110.16),
    a['figures'].append(F('K', W('combined', 'FY2027 Q3'), 'estimate', 'forecast', 'USD bn', value=215.0, basis_text='a combined figure')),
    fig(a, 'F10').update(inputs=['K', 'F4'], operation='difference', value=None, low=104.84, high=109.16),
    fig(a, 'F6').update(value=None, low=398.64, high=402.96), fig(a, 'F12').update(value=None, low=375.515, high=379.835)))
defect('a part above its whole while an unused alternative sits beside it (S3)', 'S3', lambda a: (
    fig(a, 'F10').update(kind='estimate', basis_text='segment', inputs=None, operation=None, value=120.0, rests_on=['F4']),
    fig(a, 'F12').update(value=390.675), a['figures'].append(F('ALT', W('Data Center', 'FY2027 Q3'), 'estimate', 'reported', 'USD bn',
                                                                value=105.0, basis_text='not used'))))


@case('A1', 'one uncertain quarter on two paths takes one value: FY = Q1 + Q2 + Q3 + (consensus − Q1-Q3) is exactly 411', 'pass')
def _():
    return one(_linked(411.0))


@case('A2', 'the same calculation declared as a spread 406.68–415.32 (S2)', 'S2')
def _():
    figs = _linked(None)
    figs[-1].update(value=None, low=406.68, high=415.32)
    return one(figs)


def _linked(value):
    return [F('Q1', W('company', 'FY2027 Q1'), 'source', 'reported', 'USD bn', value=81.6, evidence_id='e1', quote_number='$81.6 billion', qualifier='none'),
            F('Q2', W('company', 'FY2027 Q2'), 'source', 'reported', 'USD bn', value=96.2, evidence_id='e2', quote_number='$96.2 billion', qualifier='none'),
            F('Q3', W('company', 'FY2027 Q3'), 'source', 'guidance', 'USD bn', low=105.84, high=110.16, evidence_id='e3',
              quote_number='$108.0 billion, plus or minus 2%', qualifier='none'),
            F('C', W('company', 'FY2027'), 'source', 'consensus', 'USD bn', value=411.0, evidence_id='e6', quote_number='$411 billion', qualifier='none'),
            F('N9', W('company', 'FY2027 Q1-Q3'), 'computed', 'guidance', 'USD bn', low=283.64, high=287.96, inputs=['Q1', 'Q2', 'Q3'], operation='sum'),
            F('Q4', W('company', 'FY2027 Q4'), 'computed', 'consensus', 'USD bn', low=123.04, high=127.36, inputs=['C', 'N9'], operation='difference'),
            F('FY', W('company', 'FY2027'), 'computed', 'forecast', 'USD bn', value=value, inputs=['Q1', 'Q2', 'Q3', 'Q4'], operation='sum',
              outcome_for=['s'])]


@case('A1', 'a range straddling zero times itself is 0 to 9', 'pass')
def _():
    return one(_square(0.0, 9.0))


@case('A2', 'a range straddling zero times itself declared 4 to 9 (S2)', 'S2')
def _():
    return one(_square(4.0, 9.0))


def _square(lo, hi):
    return [F('P', W('a', 'FY2027', measure='p'), 'estimate', 'forecast', 'x', low=-2.0, high=3.0, basis_text='p'),
            F('R', W('a', 'FY2027', measure='r'), 'computed', 'forecast', 'x', low=lo, high=hi, inputs=['P', 'P'], operation='product'),
            F('O', W('a', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=1.0, basis_text='o', rests_on=['R'], outcome_for=['s'])]


@case('A1', 'a part added to the whole for different periods: company H1 + Data Center Q3 (recorded, not refused)', 'pass',
      recorded='part and whole added for different periods')
def _():
    a = base_pair()
    a['figures'] += [F('H1', W('company', 'FY2027 H1'), 'computed', 'reported', 'USD bn', value=177.8, inputs=['F1', 'F2'], operation='sum'),
                     F('FL', W('company and Data Center', 'FY2027 Q1-Q3', measure='revenue floor'), 'computed', 'forecast', 'USD bn',
                       value=279.55, inputs=['H1', 'F10'], operation='sum')]
    return a, PAIR


@case('A1', 'a share of a percentage: 25% of 40% = 10%', 'pass')
def _():
    figs = [F('M', W('company', 'FY2027', measure='gross margin'), 'source', 'reported', '%', value=40.0, evidence_id='e22', quote_number='40%', qualifier='none'),
            F('S', W('segment', 'FY2027', measure='share of margin'), 'source', 'reported', '%', value=25.0, evidence_id='e22', quote_number='25%', qualifier='none'),
            F('X', W('segment', 'FY2027', measure='margin points'), 'computed', 'forecast', '%', value=10.0, inputs=['M', 'S'], operation='share'),
            F('O', W('company', 'FY2027'), 'estimate', 'forecast', 'USD bn', value=1.0, basis_text='o', rests_on=['X'], outcome_for=['s'])]
    return one(figs)


@case('A1', '"between 72% and 73%" and "as much as $10 billion"', 'pass')
def _():
    figs = [F('B', W('segment', 'FY2027', measure='share'), 'source', 'reported', '%', low=72.0, high=73.0, evidence_id='e20',
              quote_number='between 72% and 73%', qualifier='none'),
            F('C', W('fund', 'FY2027', measure='investment'), 'source', 'reported', 'USD bn', value=10.0, evidence_id='e21',
              quote_number='$10 billion', qualifier='as much as'),
            F('O', W('fund', 'FY2027', measure='investment'), 'estimate', 'forecast', 'USD bn', value=8.0, basis_text='below the cap',
              rests_on=['B', 'C'], outcome_for=['s'])]
    return one(figs)


# ---------- A3: Luna's observed mistakes, encoded in v13s ----------
def luna(name, expect, mutate, base=base_pair, family=PAIR):
    @case('A3', name, expect)
    def _():
        a = base()
        mutate(a)
        return a, family


luna('a prose outcome (an outcome marker must name a member)', 'schema', lambda a: fig(a, 'F6').update(outcome_for=['$398.1 billion']))
luna('a prose evidence id', 'schema', lambda a: fig(a, 'F1').update(evidence_id='NVIDIA reported FY2026 revenue of $215.9 billion.'))
luna('a prose reference (a reference marker must name a member)', 'schema', lambda a: fig(a, 'F13').update(reference_for=['Analyst consensus of $411 billion']))
luna('a unit spelled "USD billions"', 'schema', lambda a: fig(a, 'F1').update(unit='USD billions'))
luna('value with a range (both given)', 'S7', lambda a: fig(a, 'F3').update(low=105.84, high=110.16))
luna('a four-input difference', 'S7', lambda a: fig(a, 'F6').update(operation='difference'))
luna('money × % through product', 'S2', lambda a: (fig(a, 'F10').update(operation='product', value=10175.0),
                                                  fig(a, 'F12').update(value=10445.675)))      # arithmetic consistent: only the unit rule refuses it
luna('"FY2027 first half" summed from quarters', 'S8', lambda a: a['figures'].append(F(
    'H1', W('company', 'FY2027 first half'), 'computed', 'reported', 'USD bn', value=177.8, inputs=['F1', 'F2'], operation='sum')))
luna('a passage id in inputs', 'S7', lambda a: fig(a, 'F6').update(inputs=['e1', 'F2', 'F4', 'F5']))
luna('prose in inputs', 'S7', lambda a: fig(a, 'F6').update(inputs=['Q1 revenue', 'F2', 'F4', 'F5']))
luna('an outcome in "USD trillion"', 'schema', lambda a: fig(a, 'F6').update(unit='USD trillion'))
luna('"65% growth in Q4" copied as the number', 'S1', lambda a: a['figures'].append(F(
    'G', W('company', 'FY2027 Q4', measure='growth'), 'source', 'third_party', '%', value=65.0, evidence_id='e8', quote_number='65% growth in Q4',
    qualifier='none')))


def main():
    failures = 0
    for group, name, expect, recorded, build in CASES:
        answer, family = build()
        result = run(copy.deepcopy(answer), family)
        if 'schema' in result:
            got = 'schema'
            detail = result['schema'][:1]
        else:
            codes = sorted({c for c, _ in result['errors']})
            got = 'pass' if not codes else ','.join(codes)
            detail = result['errors'][:2]
        ok = got == expect                               # [54] exactly the registered rule(s): no other refusal may stand in for it
        if ok and name in MESSAGES and not any(MESSAGES[name] in d for _, d in result.get('errors', [])):
            ok, detail = False, [f'the refusal does not say "{MESSAGES[name]}"'] + list(result.get('errors', []))[:2]
        if ok and recorded:
            ok = any(r['type'] == recorded for r in result.get('recorded', []))
            if not ok:
                detail = [f'missing recorded {recorded}: {[r["type"] for r in result.get("recorded", [])]}']
        failures += not ok
        print(f'{"PASS" if ok else "FAIL"}  {group}  {name}  [expected {expect}{" + recorded " + recorded if recorded else ""}; got {got}]'
              + ('' if ok else f'  {json.dumps(detail, ensure_ascii=False)[:400]}'))
    print(f'{len(CASES) - failures} of {len(CASES)} cases as registered')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
