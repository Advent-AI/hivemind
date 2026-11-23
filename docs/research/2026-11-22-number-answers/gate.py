"""The $0 gate of judging-v13 (DESIGN.md v5 §6, registered in D725 and council round 46e). Harness-only; reads stored stores
read-only and the frozen gold packet; writes nothing but its report. Usage: python3 gate.py [report.txt]; exit 1 on any miss."""
import copy
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import calc_check as cc  # noqa: E402

REPO = HERE.parents[2]
RUN = REPO / 'poc/data/comparison-2026-11-17/run'
PACKET = REPO / 'docs/research/2026-11-01-e2e-loop/judgement-gold/packet-v1.json'


def store_passages(draw, ids):
    conn = sqlite3.connect(f'file:{RUN / draw / "prod/views.sqlite"}?mode=ro', uri=True)
    rows = conn.execute(f'select evidence_id, quote, speaker from evidence where evidence_id in ({",".join("?" * len(ids))})', ids).fetchall()
    assert len(rows) == len(ids), (draw, ids, rows)
    return {e: {'text': q, 'speaker': s} for e, q, s in rows}


def packet_passages(ids):
    items = {it['id']: it for it in json.loads(PACKET.read_text())['items']}
    return {i: {'text': items[i]['passage'], 'speaker': items[i]['who']} for i in ids}


def W(population, measure, scope, period):
    return {'population': population, 'measure': measure, 'scope': scope, 'period': period}


def src(fid, evidence, expression, value, unit, basis, what, component='value', bound=None):
    fig = {'id': fid, 'kind': 'source', 'evidence': evidence, 'expression': expression, 'component': component, 'value': value,
           'unit': unit, 'basis': basis, 'what': what}
    if bound:
        fig['bound'] = bound
    return fig


def comp(fid, op, inputs, value, unit, what, basis='forecast', **extra):
    fig = {'id': fid, 'kind': 'computed', 'operation': op, 'inputs': inputs, 'unit': unit, 'basis': basis, 'what': what}
    fig.update({'low': value[0], 'high': value[1]} if isinstance(value, tuple) else {'value': value})
    fig.update(extra)
    return fig


def est(fid, value, unit, what, basis_text, rests_on=(), basis='forecast', **extra):
    fig = {'id': fid, 'kind': 'estimate', 'unit': unit, 'basis': basis, 'what': what, 'basis_text': basis_text, 'rests_on': list(rests_on)}
    fig.update({'low': value[0], 'high': value[1]} if isinstance(value, tuple) else {'value': value})
    fig.update(extra)
    return fig


def ans(view_id, outcome, rung, reference):
    return {'view_id': view_id, 'shape': 'forecast', 'outcome': outcome, 'rung': rung, 'reference': reference, 'reasons': 'r', 'cites': [],
            'pushes': [], 'theme_pushes': [], 'changed': True, 'why_changed': 'w'}


# ---------- R1: old-2 calls 8729 (v14) and 8737 (v9), 2026-09-20 ----------
BANDS_OLD2_REV = [[450, None], [400, 450], [350, 400], [300, 350], [None, 300]]
CO, DC = 'company', 'Data Center'
R1_FAMILY = {'members': {'v14': {'what': W('NVIDIA', 'revenue', CO, 'FY2027'), 'bands': BANDS_OLD2_REV},
                         'v9': {'what': W('NVIDIA', 'revenue', DC, 'FY2027'), 'bands': BANDS_OLD2_REV}},
             'relations': [{'type': 'part_of', 'part': 'v9', 'whole': 'v14'}],
             'shared': [W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), W('NVIDIA', 'revenue', CO, 'FY2027 Q4')],
             'compare_periods': ['FY2027 Q3', 'FY2027 Q4', 'FY2027'],
             'prior_answers': {'v9': {'day': '2026-09-19', 'values': [414.0, 385.0, 390.0]}}}   # call 8621: reference $414B, outcome $385–390B
R1_PASSAGES = store_passages('old-2', ['e238', 'e2497', 'e2499', 'e4762', 'e3943', 'e5056', 'e4995', 'e3219', 'e976'])


def r1_common():
    return [
        src('q1', 'e238', '$81.6 billion', 81.6, 'USD bn', 'reported', W('NVIDIA', 'revenue', CO, 'FY2027 Q1')),
        src('q2', 'e2497', '$96.2 billion', 96.2, 'USD bn', 'reported', W('NVIDIA', 'revenue', CO, 'FY2027 Q2')),
        src('g3', 'e2499', '$108.0 billion, plus or minus 2%', 108.0, 'USD bn', 'guidance', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), 'midpoint'),
        src('g3w', 'e2499', '$108.0 billion, plus or minus 2%', 2.0, '%', 'guidance', W('NVIDIA', 'guidance width', CO, 'FY2027 Q3'), 'relative'),
        comp('g3r', 'range_from_relative', ['g3', 'g3w'], (105.84, 110.16), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), basis='guidance'),
        src('beat', 'e4762', '3.1%', 3.1, '%', 'third_party', W('NVIDIA', 'beat over the guidance high end', CO, 'last four quarters')),
        est('q3f', 113.5, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), 'the guide high end 110.16 plus the 3.1% average beat', ['g3r', 'beat']),
        src('g12', 'e3943', '12%', 12.0, '%', 'third_party', W('NVIDIA', 'sequential growth', CO, 'FY2027 Q3')),
        est('carry', 12.0, '%', W('NVIDIA', 'assumption', CO, 'FY2027 Q4'), "Q3's guided 12% sequential growth continues into Q4", ['g12'],
            converts=['q3f']),
        comp('q4f', 'apply_growth', ['q3f', 'g12'], 127.1, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q4'), bridge='carry'),
        comp('fy14', 'sum', ['q1', 'q2', 'q3f', 'q4f'], 418.4, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), relation='time_aggregation'),
        src('c411', 'e5056', 'around $411 billion', 411.0, 'USD bn', 'consensus', W('NVIDIA', 'revenue', CO, 'FY2027'), 'bound', 'approx'),
        src('dch1', 'e4995', '$164 billion', 164.0, 'USD bn', 'reported', W('NVIDIA', 'revenue', DC, 'FY2027 H1')),
        src('mix', 'e3219', '92.5%', 92.5, '%', 'reported', W('NVIDIA', 'Data Center share', CO, 'FY2027 Q2')),
    ]


def r1(variant):
    figs = r1_common()
    if variant in ('a', 'b'):
        figs.append(comp('dcq3', 'share', ['g3', 'mix'], 99.9, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q3')))
    else:
        figs.append(comp('dcq3', 'share', ['q3f', 'mix'], 105.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q3')))
    if variant == 'a':
        figs.append(est('dcq4', 146.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'),
                        'hyperscale reacceleration, the Rubin ramp, a discounted SemiAnalysis uplift', ['e976']))
        dcfy = 409.9
    elif variant == 'b':
        figs.append(est('dcq4', 115.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'), 'held below the company quarter', ['e976']))
        dcfy = 378.9
    else:
        figs.append(comp('dcq4', 'share', ['q4f', 'mix'], 117.6, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4')))
        dcfy = 386.6
    figs.append(comp('dcfy', 'sum', ['dch1', 'dcq3', 'dcq4'], dcfy, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), relation='time_aggregation'))
    if variant == 'a':                                    # as stored: the previous conclusion's $414B called the market reference
        figs.append({'id': 'prior414', 'kind': 'prior', 'basis': 'prior_forecast', 'value': 414.0, 'unit': 'USD bn',
                     'what': W('NVIDIA', 'revenue', DC, 'FY2027'), 'pointer': {'view': 'v9', 'day': '2026-09-19'}})   # its reference field, $414B since 09-14 (call 7939)
        v9_ref = {'figure': 'prior414'}
    else:
        figs.append(comp('dcref', 'share', ['c411', 'mix'], 380.2, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), basis='consensus', bound='approx'))
        v9_ref = {'figure': 'dcref'}
    v9_rung = 2 if dcfy >= 400 else 3
    return {'figures': figs, 'answers': [ans('v14', 'fy14', 2, {'figure': 'c411'}), ans('v9', 'dcfy', v9_rung, v9_ref)]}


# ---------- R2: old-2 call 8734 (v29 equity commitments) ----------
R2_FAMILY = {'members': {'v29': {'what': W('NVIDIA', 'equity investment commitments', CO, 'end of FY2027'),
                                 'bands': [[None, 25], [25, 50], [50, 75], [75, 100], [100, None]]}},
             'relations': [], 'shared': [], 'compare_periods': []}
R2_PASSAGES = store_passages('old-2', ['e2620', 'e2889', 'e1732'])


def r2():
    eic = 'equity investment commitments'
    return {'figures': [
        src('bal', 'e2620', '$25 billion', 25.0, 'USD bn', 'reported', W('NVIDIA', eic, CO, 'as of 2026-07-26')),
        src('add18', 'e2889', '$18 billion', 18.0, 'USD bn', 'reported', W('NVIDIA', eic, CO, 'rest of FY2027')),
        est('mtk', 3.5, 'USD bn', W('NVIDIA', eic, CO, 'rest of FY2027'), 'the MediaTek investment announced after the balance date'),
        est('talks', 6.5, 'USD bn', W('NVIDIA', eic, CO, 'rest of FY2027'), 'the Anthropic and Thinking Machines talks, risk-adjusted (amount inferred from the stated $53B total)'),
        src('ref70', 'e1732', '$70 billion', 70.0, 'USD bn', 'third_party', W('NVIDIA', 'equity investments to ecosystem partners', CO, 'period not specified')),
        comp('end', 'roll_forward', ['bal', 'add18', 'mtk', 'talks'], 53.0, 'USD bn', W('NVIDIA', eic, CO, 'end of FY2027'),
             relation='overlap_unknown', disputed='add18'),
    ], 'answers': [ans('v29', 'end', 3, {'figure': 'ref70'})]}                     # as stored: Bank of America's $70B


# ---------- R3: old-2 call 8595 (v6, four hyperscalers' 2027 data-center capex) ----------
FOUR = 'four largest AI hyperscalers'
R3_FAMILY = {'members': {'v6': {'what': W(FOUR, 'data-center capex', 'combined', 'CY2027'),
                                'bands': [[None, 800], [800, 900], [900, 1100], [1100, 1200], [1200, None]]}},
             'relations': [], 'shared': [], 'compare_periods': []}
R3_PASSAGES = store_passages('old-2', ['e1786', 'e2535', 'e1926'])


def r3(variant):
    if variant == 'a':                                    # the qualifiers stripped, as the stored arithmetic used them
        a = src('a730', 'e1786', '$730 billion', 730.0, 'USD bn', 'reported', W(FOUR, 'AI infrastructure spending', 'combined', 'CY2026'))
        b = src('b800', 'e2535', '$800 billion', 800.0, 'USD bn', 'guidance', W('top five hyperscalers', 'capex', 'combined', 'CY2026'))
        bound = {}
    else:
        a = src('a730', 'e1786', 'more than $730 billion', 730.0, 'USD bn', 'reported', W(FOUR, 'AI infrastructure spending', 'combined', 'CY2026'),
                'bound', '>')
        b = src('b800', 'e2535', 'nearly $800 billion', 800.0, 'USD bn', 'guidance', W('top five hyperscalers', 'capex', 'combined', 'CY2026'),
                'bound', 'approx_below')
        bound = {'bound': '>'}                            # more than $730B over nearly $800B, times $1.3T: a lower bound
    c = src('c1300', 'e2535', '$1.3 trillion', 1300.0, 'USD bn', 'guidance', W('top five hyperscalers', 'capex', 'combined', 'CY2027'))
    figs = [a, b, c]
    ratio_extra, prod_extra = dict(bound), dict(bound)
    if variant == 'c':
        figs.append(est('br1', 0.9125, 'x', W(FOUR, 'assumption', 'combined', 'CY2026'),
                        "four companies' AI infrastructure spending stands for their share of five companies' capex", converts=['a730', 'b800']))
        figs.append(est('br2', 0.9125, 'x', W(FOUR, 'assumption', 'combined', 'CY2027'),
                        'the 2026 share carries to 2027 and to data-center capex', converts=['c1300']))
        ratio_extra['bridge'], prod_extra['bridge'] = 'br1', 'br2'
    figs.append(comp('share45', 'ratio', ['a730', 'b800'], 0.9125, 'x', W(FOUR, 'share of top-five capex', 'combined', 'CY2026'), **ratio_extra))
    figs.append(comp('cap27', 'product', ['share45', 'c1300'], 1186.25, 'USD bn', W(FOUR, 'data-center capex', 'combined', 'CY2027'), **prod_extra))
    figs.append(src('ref108', 'e1926', '$1.08 trillion', 1080.0, 'USD bn', 'third_party', W('hyperscalers', 'spending', 'combined', 'CY2027')))
    return {'figures': figs, 'answers': [ans('v6', 'cap27', 4, {'figure': 'ref108'})]}   # as stored: the $1.08T consensus


# ---------- R4: old-3 call 9166 (v41, FY2028 Vera CPU) ----------
R4_FAMILY = {'members': {'v41': {'what': W('NVIDIA', 'revenue', 'Vera CPU', 'FY2028'),
                                 'bands': [[50, None], [40, 50], [30, 40], [20, 30], [None, 20]]}},
             'relations': [], 'shared': [], 'compare_periods': []}
R4_PASSAGES = store_passages('old-3', ['e3660'])


def r4():
    return {'figures': [
        src('c20', 'e3660', '$20 billion', 20.0, 'USD bn', 'guidance', W('NVIDIA', 'revenue', 'CPU', 'FY2027')),
        src('m2', 'e3660', 'more than double', 2.0, 'x', 'guidance', W('NVIDIA', 'revenue multiple', 'CPU', 'FY2028'), 'multiplier', '>'),
        comp('cpu28', 'product', ['c20', 'm2'], 40.0, 'USD bn', W('NVIDIA', 'revenue', 'CPU', 'FY2028'), basis='guidance', bound='>'),
        est('vera28', (38.0, 39.0), 'USD bn', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2028'),
            "management's CPU outlook read as Vera's, trimmed for no shipment volume in hand and AMD's benchmarks", ['cpu28'],
            adjusts={'figure': 'cpu28', 'type': 'trim'}),
    ], 'answers': [ans('v41', 'vera28', 3, {'figure': 'cpu28'})]}


# ---------- G1–G4: the frozen gold's reasoning (q01, q02, q19, q22) ----------
G_PASSAGES = packet_passages(['i037', 'i090', 'i280', 'i281', 'i295', 'i106', 'i219', 'i216', 'i288', 'i129', 'i096', 'i218', 'i256', 'i173'])
SEED = {'v1': [[500, None], [400, 500], [350, 400], [300, 350], [None, 300]],
        'v2': [[440, None], [360, 440], [310, 360], [260, 310], [None, 260]],
        'v19': [[20, None], [12, 20], [6, 12], [2, 6], [None, 2]],
        'v22': [[650, None], [550, 650], [480, 550], [420, 480], [None, 420]]}


def q01_figs():
    return [
        src('gq1', 'i280', '$81.6 billion', 81.6, 'USD bn', 'reported', W('NVIDIA', 'revenue', CO, 'FY2027 Q1')),
        src('gq2', 'i281', '$91 billion, plus or minus 2%', 91.0, 'USD bn', 'guidance', W('NVIDIA', 'revenue', CO, 'FY2027 Q2'), 'midpoint'),
        comp('gh1', 'sum', ['gq1', 'gq2'], 172.6, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 H1'), relation='time_aggregation'),
        est('gh2', (228.0, 262.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 H2'),
            'accelerating growth, compute 20% above consensus, the Rubin ramp at twice the GB300 price, the Vera target: no fixed increment',
            ['i295', 'i106', 'i219', 'i216', 'i288']),
        comp('gfy', 'sum', ['gh1', 'gh2'], (400.0, 435.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), relation='time_aggregation'),
        src('gc392', 'i037', '$392 billion', 392.0, 'USD bn', 'consensus', W('NVIDIA', 'revenue', CO, 'FY2027')),
    ]


V1 = {'what': W('NVIDIA', 'revenue', CO, 'FY2027'), 'bands': SEED['v1']}


def g1():
    return ({'members': {'v1': V1}, 'relations': [], 'shared': [], 'compare_periods': []},
            {'figures': q01_figs(), 'answers': [ans('v1', 'gfy', 2, {'figure': 'gc392'})]})


def g2():
    """q01 and q02 with paired scenarios [46g.3]: low and high paths for the company total and the segment, each final range an estimate."""
    figs = [f for f in q01_figs() if f['id'] in ('gq1', 'gq2', 'gh1', 'gc392')] + [
        est('gh2lo', 228.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 H2'), 'the low end of the second-half drivers',
            ['i295', 'i106', 'i219', 'i216', 'i288'], scenario='low'),
        est('gh2hi', 262.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 H2'), 'the high end of the second-half drivers',
            ['i295', 'i106', 'i219', 'i216', 'i288'], scenario='high'),
        comp('gfylo', 'sum', ['gh1', 'gh2lo'], 400.6, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), relation='time_aggregation', scenario='low'),
        comp('gfyhi', 'sum', ['gh1', 'gh2hi'], 434.6, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), relation='time_aggregation', scenario='high'),
        est('gfy', (400.0, 435.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), 'the two paths, rounded', ['gfylo', 'gfyhi'], scenario='range'),
        src('gmix', 'i129', '92%', 92.0, '%', 'reported', W('NVIDIA', 'Data Center share', CO, 'FY2027 Q1')),
        comp('gref2', 'share', ['gc392', 'gmix'], 360.6, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), basis='consensus'),
        est('gshlo', 92.0, '%', W('NVIDIA', 'Data Center share', CO, 'FY2027'), 'the Q1 mix, held', ['gmix'], scenario='low'),
        est('gshhi', 93.0, '%', W('NVIDIA', 'Data Center share', CO, 'FY2027'), 'the Q1 mix, a point higher', ['gmix'], scenario='high'),
        comp('gdclo', 'share', ['gfylo', 'gshlo'], 368.55, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), scenario='low'),
        comp('gdchi', 'share', ['gfyhi', 'gshhi'], 404.18, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), scenario='high'),
        est('gdc', (370.0, 400.0), 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), 'the two paths, with the compute tracking',
            ['gdclo', 'gdchi', 'i106'], scenario='range'),
    ]
    family = {'members': {'v1': V1, 'v2': {'what': W('NVIDIA', 'revenue', DC, 'FY2027'), 'bands': SEED['v2']}},
              'relations': [{'type': 'part_of', 'part': 'v2', 'whole': 'v1'}],
              'shared': [W('NVIDIA', 'revenue', CO, 'FY2027')], 'compare_periods': ['FY2027']}
    return family, {'figures': figs, 'answers': [ans('v1', 'gfy', 2, {'figure': 'gc392'}), ans('v2', 'gdc', 2, {'figure': 'gref2'})]}


def g3():
    figs = [
        src('gt20', 'i288', '$20 billion', 20.0, 'USD bn', 'guidance', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2027')),
        src('gasp', 'i218', '$5,000', 5000.0, 'USD', 'third_party', W('NVIDIA', 'price per unit', 'Vera CPU', 'in volume')),
        comp('gunits', 'ratio', ['gt20', 'gasp'], 4000000.0, 'units', W('NVIDIA', 'units', 'Vera CPU', 'FY2027')),
        est('gvera', (8.0, 18.0), 'USD bn', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2027'),
            'launches this fall, about two selling quarters; four million units; a host-CPU choice of Xeon', ['gunits', 'i096'],
            adjusts={'figure': 'gt20', 'type': 'discount'}),
    ]
    family = {'members': {'v19': {'what': W('NVIDIA', 'revenue', 'Vera CPU', 'FY2027'), 'bands': SEED['v19']}},
              'relations': [], 'shared': [], 'compare_periods': []}
    return family, {'figures': figs, 'answers': [ans('v19', 'gvera', 2, {'figure': 'gt20'})]}


def g4():
    figs = q01_figs() + [
        src('g41', 'i090', '41%', 41.0, '%', 'consensus', W('NVIDIA', 'revenue growth', CO, 'FY2028')),
        comp('gfy28c', 'apply_growth', ['gfy', 'g41'], (565.0, 615.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028')),
        est('gfy28', (560.0, 640.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), 'the big four capex step to over $1 trillion; Rubin pricing; Vera',
            ['gfy28c', 'i256', 'i173'], scenario='range'),
        src('gc554', 'i037', '$554 billion', 554.0, 'USD bn', 'consensus', W('NVIDIA', 'revenue', CO, 'FY2028')),
    ]
    family = {'members': {'v1': V1, 'v22': {'what': W('NVIDIA', 'revenue', CO, 'FY2028'), 'bands': SEED['v22']}},
              'relations': [{'type': 'same_base', 'later': 'v22', 'earlier': 'v1'}], 'shared': [], 'compare_periods': []}
    return family, {'figures': figs, 'answers': [ans('v1', 'gfy', 2, {'figure': 'gc392'}), ans('v22', 'gfy28', 2, {'figure': 'gc554'})]}


# ---------- the registered items ----------
def codes(result):
    return {code for code, _ in result['errors']}


MANIFEST = {}


def run():
    rows = []

    def item(name, family, passages, calc, ok, why):
        MANIFEST[name] = {'family': family, 'calc': calc}
        try:
            result = cc.check(family, passages, calc)
        except Exception as error:                    # a crash is a miss with its reason, never a silent stop of the gate
            rows.append((name, False, f'CRASH {type(error).__name__}: {error}', {'errors': [], 'recorded': []}))
            return
        verdict, note = ok(result)
        rows.append((name, verdict, note, result))

    item('R1a', R1_FAMILY, R1_PASSAGES, r1('a'),
         lambda r: ('C3' in codes(r) and any('FY2027 Q4' in d for c, d in r['errors'] if c == 'C3'), 'C3 on Q4'), '')
    item('R1b', R1_FAMILY, R1_PASSAGES, r1('b'),
         lambda r: ('C4' in codes(r) and 'C3' not in codes(r) and any('FY2027 Q3' in d and 'g3' in d for c, d in r['errors'] if c == 'C4'),
                    'C4 on the Q3 bypass, no C3'), '')
    item('R1c', R1_FAMILY, R1_PASSAGES, r1('c'), lambda r: (not r['errors'], 'passes'), '')
    item('R2', R2_FAMILY, R2_PASSAGES, r2(),
         lambda r: (not r['errors'] and any(x['type'] == 'overlap' and x['figure'] == 'end' and abs(x['alternate'][0] - 35) < 0.01
                                            and 50 in x['definite'] for x in r['recorded']),
                    'overlap recorded; ~35 definitely crosses 50'), '')
    item('R3a', R3_FAMILY, R3_PASSAGES, r3('a'),
         lambda r: (any(c == 'C1' and 'a730' in d for c, d in r['errors']) and any(c == 'C1' and 'b800' in d for c, d in r['errors']),
                    'C1 on both stripped qualifiers'), '')
    item('R3b', R3_FAMILY, R3_PASSAGES, r3('b'),
         lambda r: ('C1' not in codes(r) and 'C8' in codes(r), 'passes C1, C8 without bridges'), '')
    item('R3c', R3_FAMILY, R3_PASSAGES, r3('c'),
         lambda r: (not r['errors'] and sum(x['type'] == 'bridge' for x in r['recorded']) == 2, 'bridges recorded, undetermined'), '')
    item('R4', R4_FAMILY, R4_PASSAGES, r4(),
         lambda r: (not r['errors'] and any(x['type'] == 'adjustment' and x['figure'] == 'vera28' and 40 in x['definite']
                                            for x in r['recorded']), 'trim definitely crosses 40'), '')
    for name, maker in (('G1', g1), ('G2', g2), ('G3', g3), ('G4', g4)):
        family, calc = maker()
        item(name, family, G_PASSAGES, calc, lambda r: (not r['errors'], 'passes, estimates visible'), '')
    f1, c1 = g1()
    p1 = copy.deepcopy(c1)
    p1['figures'][0]['value'] = 81.9
    item('P1', f1, G_PASSAGES, p1, lambda r: (codes(r) == {'C1'} and any('gq1' in d for _, d in r['errors']), 'C1 only, on gq1'), '')
    p2 = copy.deepcopy(c1)
    gfy = next(f for f in p2['figures'] if f['id'] == 'gfy')
    gfy['low'], gfy['high'] = 450.0, 480.0
    item('P2', f1, G_PASSAGES, p2, lambda r: (codes(r) == {'C2'} and any('gfy' in d for _, d in r['errors']), 'C2 only, on gfy'), '')
    p3a = copy.deepcopy(c1)
    p3a['figures'].append({'id': 'pri', 'kind': 'prior', 'basis': 'prior_forecast', 'value': 425.0, 'unit': 'USD bn',
                           'what': W('NVIDIA', 'revenue', CO, 'FY2027'), 'pointer': {'view': 'v1', 'day': '2026-07-13'}})
    p3a['answers'][0]['reference'] = {'figure': 'pri'}
    f1p = dict(f1, prior_answers={'v1': {'day': '2026-07-13', 'values': [425.0]}})       # the earlier answer it points to, as shown
    item('P3a', f1p, G_PASSAGES, p3a, lambda r: (codes(r) == {'C5'}, 'C5 only'), '')
    f2, c2 = g2()
    g2x = copy.deepcopy(c2)
    lo = next(f for f in g2x['figures'] if f['id'] == 'gdclo'); hi = next(f for f in g2x['figures'] if f['id'] == 'gdchi')
    lo['inputs'], lo['value'] = ['gfyhi', 'gshlo'], 399.83                  # crossed: low share on the high total
    hi['inputs'], hi['value'] = ['gfylo', 'gshhi'], 372.56
    item('G2x', f2, G_PASSAGES, g2x, lambda r: (any(c == 'C4' and 'another scenario' in d for c, d in r['errors']), 'C4: scenarios crossed'), '')
    r1x = r1('b')
    r1x['figures'].append(est('altq3', 108.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), 'the guide as an alternate forecast', ['g3'],
                              scenario='alt'))
    next(f for f in r1x['figures'] if f['id'] == 'dcq3')['inputs'] = ['altq3', 'mix']
    item('R1bx', R1_FAMILY, R1_PASSAGES, r1x, lambda r: (any(c == 'C4' and 'another scenario' in d for c, d in r['errors']),
                                                         'C4: the base reads an alternate scenario'), '')
    r1x2 = r1('b')                                    # routed through an intermediate segment figure
    r1x2['figures'].append(est('altq3', 108.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), 'the guide as an alternate forecast', ['g3'],
                               scenario='alt'))
    r1x2['figures'].append(comp('altdc', 'share', ['altq3', 'mix'], 99.9, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q3 interim'), scenario='alt'))
    next(f for f in r1x2['figures'] if f['id'] == 'dcq3').update(operation='product', inputs=['altdc', 'one'], value=99.9)
    r1x2['figures'].append({'id': 'one', 'kind': 'estimate', 'unit': 'x', 'basis': 'forecast', 'what': W('NVIDIA', 'factor', DC, 'FY2027 Q3'),
                            'basis_text': 'unchanged', 'rests_on': [], 'value': 1.0})
    item('R1bx2', R1_FAMILY, R1_PASSAGES, r1x2, lambda r: (any(c == 'C4' and 'another scenario' in d for c, d in r['errors']),
                                                           'C4: borrowed through an intermediate'), '')
    r1x4 = r1('b')                                    # an alternate forecast computed from sources only (no estimate on its path)
    r1x4['figures'].append(comp('altq3', 'sum', ['g3'], 108.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), relation='stated_in_addition',
                                scenario='alt'))
    next(f for f in r1x4['figures'] if f['id'] == 'dcq3')['inputs'] = ['altq3', 'mix']
    item('R1bx4', R1_FAMILY, R1_PASSAGES, r1x4, lambda r: (any(c == 'C4' and 'another scenario' in d for c, d in r['errors']),
                                                           'C4: the base reads a source-only alternate forecast'), '')
    r1x3 = r1('b')                                    # a point labelled range, read by the base
    r1x3['figures'].append(est('altq3', 108.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q3'), 'the guide as a point', ['g3'], scenario='range'))
    next(f for f in r1x3['figures'] if f['id'] == 'dcq3')['inputs'] = ['altq3', 'mix']
    item('R1bx3', R1_FAMILY, R1_PASSAGES, r1x3, lambda r: (any(c == 'C4' and 'range summary' in d for c, d in r['errors']),
                                                           'C4: a point labelled range'), '')
    p3e2 = copy.deepcopy(p3a)                         # the earlier forecast relabelled as an estimate
    pri = next(f for f in p3e2['figures'] if f['id'] == 'pri')
    pri.update(kind='estimate', basis_text='our earlier figure', rests_on=[])
    p3e2['answers'][0]['outcome'] = 'pri'
    p3e2['answers'][0]['reference'] = {'figure': 'gc392'}
    item('P3e2', f1p, G_PASSAGES, p3e2, lambda r: (any(c == 'C10' for c, d in r['errors']), 'C10: an earlier forecast relabelled'), '')
    r1sc = r1('a')                                    # [46j.1] the company in base, Data Center in alt: the stored contradiction relabelled
    for f in r1sc['figures']:
        if f['id'] in ('dcq3', 'dcq4', 'dcfy'):
            f['scenario'] = 'alt'
    r1sc['figures'] = [f for f in r1sc['figures'] if f['id'] != 'prior414']
    r1sc['answers'][1]['reference'] = {'unavailable': 'none supplied'}
    item('R1sc', R1_FAMILY, R1_PASSAGES, r1sc, lambda r: (any(c == 'C4' and 'cover' in d for c, d in r['errors']),
                                                         'C4: part and whole in different scenarios'), '')
    g2x2 = copy.deepcopy(c2)                          # [46j.1] crossing the non-shared share estimates
    next(f for f in g2x2['figures'] if f['id'] == 'gdclo').update(inputs=['gfylo', 'gshhi'], value=372.56)
    next(f for f in g2x2['figures'] if f['id'] == 'gdchi').update(inputs=['gfyhi', 'gshlo'], value=399.83)
    item('G2x2', f2, G_PASSAGES, g2x2, lambda r: (any(c == 'C4' and 'another scenario' in d for c, d in r['errors']),
                                                   'C4: share estimates crossed'), '')
    f24 = {'members': {'v1': V1, 'v22': {'what': W('NVIDIA', 'revenue', CO, 'FY2028'), 'bands': SEED['v22']}},
           'relations': [{'type': 'same_base', 'later': 'v22', 'earlier': 'v1'}], 'shared': [W('NVIDIA', 'revenue', CO, 'FY2027')],
           'compare_periods': []}
    c24 = copy.deepcopy(c2)                           # [46j.2] q22 on q01's published range, per scenario
    c24['figures'] = [f for f in c24['figures'] if f['id'] not in ('gmix', 'gref2', 'gshlo', 'gshhi', 'gdclo', 'gdchi', 'gdc')] + [
        src('g41', 'i090', '41%', 41.0, '%', 'consensus', W('NVIDIA', 'revenue growth', CO, 'FY2028')),
        comp('g28lo', 'apply_growth', ['gfylo', 'g41'], 564.85, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), scenario='low'),
        comp('g28hi', 'apply_growth', ['gfyhi', 'g41'], 612.79, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), scenario='high'),
        est('g28', (560.0, 640.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), 'the two paths, widened for capex, Rubin pricing and Vera',
            ['g28lo', 'g28hi', 'i256', 'i173'], scenario='range'),
        src('gc554', 'i037', '$554 billion', 554.0, 'USD bn', 'consensus', W('NVIDIA', 'revenue', CO, 'FY2028'))]
    c24['answers'] = [ans('v1', 'gfy', 2, {'figure': 'gc392'}), ans('v22', 'g28', 2, {'figure': 'gc554'})]
    item('G24', f24, G_PASSAGES, c24, lambda r: (not r['errors'], "passes: q22 per scenario on q01's range"), '')
    def safe_changed(*args):                          # a crash in change detection is a miss with its reason
        try:
            return cc.changed(*args)
        except Exception as error:
            return None, f'CRASH {type(error).__name__}: {error}'
    prev = {'rung': 2, 'outcome': 417.5, 'sources': []}
    calc_c = r1('c')
    figs_c = {f['id']: f for f in calc_c['figures']}
    prev['sources'] = cc.member_sources(calc_c['answers'][0], figs_c)
    ch1 = safe_changed(dict(prev, outcome=418.4), calc_c['answers'][0], figs_c)
    ch2 = safe_changed(dict(prev, rung=3, outcome=387.0), calc_c['answers'][0], figs_c)
    sib = copy.deepcopy(calc_c)                       # [46k.3] a sibling-only source change leaves v14 unchanged
    sib_figs = {f['id']: f for f in sib['figures']}
    sib_figs['dch1'].update(expression='$164 billion', value=164.0)
    sib_figs['mix']['evidence'] = 'e3219'
    ch3 = safe_changed(dict(prev, outcome=418.4), sib['answers'][0], dict(sib_figs, mix=dict(sib_figs['mix'], expression='92.5% (restated)')))
    c5 = r2()                                         # [46aa] declared $52.75B, recomputed and published $53.00B, against a published $52.70B
    next(f for f in c5['figures'] if f['id'] == 'end')['value'] = 52.75
    f5 = {f['id']: f for f in c5['figures']}
    r5 = cc.check(R2_FAMILY, R2_PASSAGES, c5)
    own5 = cc.member_sources(c5['answers'][0], f5)
    ch5 = safe_changed({'rung': 3, 'outcome': 52.70, 'sources': own5}, c5['answers'][0], f5)
    rows.append(('CH5', not r5['errors'] and r5['published']['v29'][:2] == [53.0, 53.0] and ch5[0] is True and '53.0' in ch5[1],
                 f'published {r5["published"]["v29"]}; {ch5[1]}', r5))
    c6 = r4()                                         # [46ab] published below $39B before, above $39B now, same rung and sources
    v6 = next(f for f in c6['figures'] if f['id'] == 'vera28'); v6.update(value=39.0, bound='>'); v6.pop('low'); v6.pop('high')
    c6['figures'].append(comp('vout', 'sum', ['vera28'], 39.0, 'USD bn', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2028'), bound='>'))
    c6['answers'][0].update(outcome='vout', rung=3)
    f6 = {f['id']: f for f in c6['figures']}
    r6 = cc.check(R4_FAMILY, R4_PASSAGES, c6)
    own6 = cc.member_sources(c6['answers'][0], f6)
    ch6 = safe_changed({'rung': 3, 'outcome': [None, 39.0, '<'], 'sources': own6}, c6['answers'][0], f6)
    ch6b = safe_changed({'rung': 3, 'outcome': r6['published']['v41'], 'sources': own6}, c6['answers'][0], f6)
    rows.append(('CH6', not r6['errors'] and ch6[0] is True and ch6b[0] is False, f'below to above 39: {ch6[1]}; same published: {ch6b[1]}', r6))
    c7 = r1('c')                                      # [46ac.1] the guidance width dropped, the $108B midpoint kept (same passage and expression)
    c7['figures'] = [f for f in c7['figures'] if f['id'] not in ('g3w', 'g3r')]
    next(f for f in c7['figures'] if f['id'] == 'q3f')['rests_on'] = ['g3', 'beat']
    f7 = {f['id']: f for f in c7['figures']}
    r7 = cc.check(R1_FAMILY, R1_PASSAGES, c7)
    ch7 = safe_changed({'rung': 2, 'outcome': 418.42, 'sources': prev['sources']}, c7['answers'][0], f7)
    rows.append(('CH7', not r7['errors'] and ch7[0] is True and 'relative' in ch7[1], f'{ch7[1]}', r7))
    c8 = r4()                                         # [46ac.2] a numeric answer becomes unresolved
    c8['answers'][0] = {'view_id': 'v41', 'shape': 'unresolved', 'why': 'no Vera volume stated', 'cites': [], 'pushes': [], 'theme_pushes': []}
    r8 = cc.check(R4_FAMILY, R4_PASSAGES, c8)
    ch8 = safe_changed({'rung': 3, 'outcome': [38.0, 39.0, None], 'sources': []}, c8['answers'][0], {f['id']: f for f in c8['figures']})
    rows.append(('CH8', not r8['errors'] and ch8 == (True, 'now unresolved'), f'{ch8[1]}', r8))
    rows.append(('CH1', ch1[0] is False, f'unchanged: {ch1[1]}', {'errors': [], 'recorded': []}))
    rows.append(('CH2', ch2[0] is True and 'rung 3 to 2' in ch2[1], f'changed: {ch2[1]}', {'errors': [], 'recorded': []}))
    rows.append(('CH3', ch3[0] is False, f'sibling-only change: {ch3[1]}', {'errors': [], 'recorded': []}))
    f1g, c1g = g1()                                   # [46l.2] a wider range with the same midpoint
    figs_g = {f['id']: f for f in c1g['figures']}
    own_g = cc.member_sources(c1g['answers'][0], figs_g)
    ch4 = safe_changed({'rung': 2, 'outcome': (390.0, 445.0), 'sources': own_g}, c1g['answers'][0], figs_g)
    rows.append(('CH4', ch4[0] is True and 'outcome' in ch4[1], f'wider range, same midpoint: {ch4[1]}', {'errors': [], 'recorded': []}))
    g24m = copy.deepcopy(c24)                         # [46k.1] the high path replaced by a standalone estimate
    g24m['figures'] = [f for f in g24m['figures'] if f['id'] != 'g28hi'] + [
        est('g28hi', 612.79, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), 'a standalone view', ['i256'], scenario='high')]
    item('G24m', f24, G_PASSAGES, g24m, lambda r: (any(c == 'C9' and 'g28hi' in d for c, d in r['errors']), 'C9: the high path skips q01'), '')
    g24d = copy.deepcopy(c24)                         # [46l.1] the high calculation deleted
    g24d['figures'] = [f for f in g24d['figures'] if f['id'] != 'g28hi']
    next(f for f in g24d['figures'] if f['id'] == 'g28')['rests_on'] = ['g28lo', 'i256', 'i173']
    item('G24d', f24, G_PASSAGES, g24d, lambda r: (any(c == 'C9' and 'covers' in d for c, d in r['errors']), 'C9: the high path missing'), '')
    g24c = copy.deepcopy(c24)                         # [46l.1] the high path computed from FY2028 consensus, q01's high only cited
    g24c['figures'] = [f for f in g24c['figures'] if f['id'] != 'g28hi'] + [
        est('g28hi', 612.79, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), 'consensus, adjusted', ['gc554', 'gfyhi'], scenario='high')]
    item('G24c', f24, G_PASSAGES, g24c, lambda r: (any(c == 'C9' and 'g28hi' in d for c, d in r['errors']), 'C9: q01 only cited, not computed'), '')
    g24c3 = copy.deepcopy(c24)                        # [46m.1] q01's high forecast in an unused third operand
    next(f for f in g24c3['figures'] if f['id'] == 'g28hi').update(inputs=['gc554', 'g41', 'gfyhi'], value=781.14)
    item('G24c3', f24, G_PASSAGES, g24c3, lambda r: (any(c == 'C7' and 'operands' in d for c, d in r['errors']), 'C7: an operand the arithmetic ignores'), '')
    g24s1 = copy.deepcopy(c24)                        # [46n] a sum whose short signs list drops q01's path
    g24s1['figures'] = [f for f in g24s1['figures'] if f['id'] != 'g28hi'] + [
        comp('g28hi', 'sum', ['gc554', 'gfyhi'], 554.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), scenario='high', signs=[1])]
    item('G24s1', f24, G_PASSAGES, g24s1, lambda r: (any(c == 'C7' and 'signs' in d for c, d in r['errors']), 'C7: a short signs list'), '')
    g24s0 = copy.deepcopy(c24)                        # [46n] a zero sign
    g24s0['figures'] = [f for f in g24s0['figures'] if f['id'] != 'g28hi'] + [
        comp('g28hi', 'sum', ['gc554', 'gfyhi'], 554.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), scenario='high', signs=[1, 0])]
    item('G24s0', f24, G_PASSAGES, g24s0, lambda r: (any(c == 'C7' and 'signs' in d for c, d in r['errors']), 'C7: a zero sign'), '')
    g24a1 = copy.deepcopy(c24)                        # [46n] one operand for apply_growth: refused, not a crash
    next(f for f in g24a1['figures'] if f['id'] == 'g28hi')['inputs'] = ['gfyhi']
    item('G24a1', f24, G_PASSAGES, g24a1, lambda r: (any(c == 'C7' and 'operands' in d for c, d in r['errors']), 'C7: one operand, no crash'), '')
    g24x = copy.deepcopy(c24)                         # [46o.1] q01's base added and subtracted: it cancels out
    g24x['figures'] = [f for f in g24x['figures'] if f['id'] != 'g28hi'] + [
        comp('g28hi', 'sum', ['gc554', 'gfyhi', 'gfyhi'], 554.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'), scenario='high', signs=[1, 1, -1])]
    item('G24x', f24, G_PASSAGES, g24x, lambda r: (any(c == 'C9' and 'does not change' in d for c, d in r['errors']), 'C9: a base that cancels'), '')
    g24nv = copy.deepcopy(c24)                        # [46o.2] a computed figure with no number
    hi_fig = next(f for f in g24nv['figures'] if f['id'] == 'g28hi')
    hi_fig.pop('value', None)
    item('G24nv', f24, G_PASSAGES, g24nv, lambda r: (any(c == 'C7' and 'value or a complete range' in d for c, d in r['errors']), 'C7: no number, no crash'), '')
    f4x, c4x = g4()                                   # [46p] a same-period cancellation on a range base: $554B + x - x
    c4x['figures'].append(comp('g28cancel', 'sum', ['gc554', 'gfy28c', 'gfy28c'], 554.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'),
                               relation='stated_in_addition', signs=[1, 1, -1]))
    next(f for f in c4x['figures'] if f['id'] == 'gfy28')['rests_on'] = ['g28cancel', 'i256']
    item('G4x', f4x, G_PASSAGES, c4x, lambda r: (any(c == 'C9' and 'g28cancel' in d and 'does not change' in d for c, d in r['errors'])
                                                 and 'C8' not in codes(r), 'C9: a range base that cancels, no C8 mask'), '')
    for name, bad in (('R1rneg', -2), ('R1r6', 6), ('R1rnone', None)):     # [46q] a rung outside the ladder
        rr = r1('c')
        if bad is None:
            rr['answers'][1].pop('rung')
        else:
            rr['answers'][1]['rung'] = bad
        item(name, R1_FAMILY, R1_PASSAGES, rr, lambda r: (any(c == 'C6' and 'is not one of' in d for c, d in r['errors']), 'C6: no such rung'), '')
    for name, rung_b, expect_c6 in (('R4b2', 2, True), ('R4b3', 3, False)):   # [46r] "less than $40B" on rung 2 and on rung 3
        rb = r4()
        next(f for f in rb['figures'] if f['id'] == 'vera28').update(value=40.0, bound='<')
        next(f for f in rb['figures'] if f['id'] == 'vera28').pop('low'); next(f for f in rb['figures'] if f['id'] == 'vera28').pop('high')
        rb['answers'][0]['rung'] = rung_b
        item(name, R4_FAMILY, R4_PASSAGES, rb,
             (lambda r: (any(c == 'C6' for c, _ in r['errors']), 'C6: below 40 is not on the 40-50 rung')) if expect_c6 else
             (lambda r: (not any(c == 'C6' for c, _ in r['errors']) and any(x['type'] == 'adjustment' and x['definite'] == [40]
                                                                          for x in r['recorded']),
                         'below 40 sits on the 30-40 rung; the trim from above 40 definitely crosses 40')), '')
    rq = r1('c')                                      # [46s, 46z.2] Data Center Q4 strictly above the company Q4, exactly 127.12 recomputed
    rq['figures'] = [f for f in rq['figures'] if f['id'] not in ('dcq4', 'dcfy')] + [
        est('dcq4', 127.12, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'), 'above the company quarter', ['e976'], bound='>'),
        comp('dcfy', 'sum', ['dch1', 'dcq3', 'dcq4'], 396.1, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), relation='time_aggregation', bound='>')]
    item('R1qb', R1_FAMILY, R1_PASSAGES, rq, lambda r: (any(c == 'C3' and 'FY2027 Q4' in d for c, d in r['errors']), 'C3: strictly above an exact whole'), '')
    rq2 = r1('c')                                     # [46t.2] Data Center Q4 above 130 and company Q4 at least 127.1 can both hold
    rq2['figures'] = [f for f in rq2['figures'] if f['id'] not in ('q4f', 'fy14', 'dcq4', 'dcfy', 'carry')] + [
        est('q4f', 127.1, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027 Q4'), 'at least the guided pace', ['q3f', 'g12'], bound='>='),
        comp('fy14', 'sum', ['q1', 'q2', 'q3f', 'q4f'], 418.4, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), relation='time_aggregation', bound='>='),
        est('dcq4', 130.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'), 'above the guided company pace times the mix', ['q4f'], bound='>'),
        comp('dcfy', 'sum', ['dch1', 'dcq3', 'dcq4'], 399.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), relation='time_aggregation', bound='>')]
    item('R1qc', R1_FAMILY, R1_PASSAGES, rq2, lambda r: (not r['errors'], 'passes: >130 within >=127.1 can hold'), '')
    rb_one = r4()                                     # [46t.1] the bounded outcome passed through a one-input sum keeps its bound
    vf = next(f for f in rb_one['figures'] if f['id'] == 'vera28'); vf.update(value=40.0, bound='<'); vf.pop('low'); vf.pop('high')
    rb_one['figures'].append(comp('vout', 'sum', ['vera28'], 40.0, 'USD bn', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2028'), bound='<'))
    rb_one['answers'][0].update(outcome='vout', rung=3)
    item('R4one', R4_FAMILY, R4_PASSAGES, rb_one, lambda r: (not r['errors'] and any(x['type'] == 'adjustment' and x['definite'] == [40]
                                                                                     for x in r['recorded']), 'the bound survives recomputation'), '')
    r2b = r2()                                        # [46u.1] a retained lower bound: the alternate stays a lower bound
    next(f for f in r2b['figures'] if f['id'] == 'talks')['bound'] = '>'
    next(f for f in r2b['figures'] if f['id'] == 'end')['bound'] = '>'
    item('R2b1', R2_FAMILY, R2_PASSAGES, r2b, lambda r: (not r['errors'] and any(x['type'] == 'overlap' and 50 in x['possible']
                                                                                 and 50 not in x['definite'] for x in r['recorded']),
                                                         'the $50B crossing only possible: >$35B may exceed $50B'), '')
    for name, declared, expect in (('R2b2a', '<', True), ('R2b2b', '>', False)):   # [46u.2] subtracting a lower bound gives an upper bound
        rd = r2()
        rd['figures'] = [f for f in rd['figures'] if f['id'] not in ('talks', 'end')] + [
            est('draw', 6.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'), 'commitments funded, at least', bound='>'),
            comp('end', 'roll_forward', ['bal', 'add18', 'mtk', 'draw'], 40.0, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'end of FY2027'),
                 relation='overlap_unknown', disputed='add18', signs=[1, 1, 1, -1], bound=declared)]
        rd['answers'][0]['rung'] = 2
        item(name, R2_FAMILY, R2_PASSAGES, rd,
             (lambda r: (not r['errors'], 'passes: 46.5 minus more than 6.5 is below 40')) if expect else
             (lambda r: (any(c == 'C2' and 'end' in d for c, d in r['errors']), 'C2: the minus sign flips the bound')), '')
    r2m = r2()                                        # [46v] a retained upper bound beside a retained lower bound
    next(f for f in r2m['figures'] if f['id'] == 'mtk')['bound'] = '<'
    next(f for f in r2m['figures'] if f['id'] == 'talks')['bound'] = '>'
    next(f for f in r2m['figures'] if f['id'] == 'end')['bound'] = 'approx'
    item('R2m', R2_FAMILY, R2_PASSAGES, r2m, lambda r: (any(c == 'C2' and 'opposite sides' in d for c, d in r['errors'])
                                                        and not any(50 in x.get('definite', []) for x in r['recorded']),
                                                        'C2: opposing bounds, and no definite crossing recorded'), '')
    rrev = r2()                                       # [46w] a bounded commitment booked and fully reversed: exact, not unbounded
    rrev['figures'] = [f for f in rrev['figures'] if f['id'] not in ('talks', 'end')] + [
        est('cm', 6.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'), 'a commitment later reversed', bound='>'),
        comp('end', 'roll_forward', ['bal', 'add18', 'mtk', 'cm', 'cm'], 46.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'end of FY2027'),
             relation='overlap_unknown', disputed='add18', signs=[1, 1, 1, 1, -1])]
    rrev['answers'][0]['rung'] = 2
    item('R2rev', R2_FAMILY, R2_PASSAGES, rrev, lambda r: (not r['errors'] and any(x['type'] == 'overlap' and x['alternate'] == [28.5, 28.5]
                                                                                   for x in r['recorded']), 'passes: x - x nets out; alternate 28.5'), '')
    f4y, c4y = g4()                                   # two distinct figures with one derivation: a - b cancels, netting cannot see it
    c4y['figures'].append(comp('gfy28d', 'apply_growth', ['gfy', 'g41'], (565.0, 615.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028')))
    c4y['figures'].append(comp('g28cancel', 'sum', ['gc554', 'gfy28c', 'gfy28d'], 554.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2028'),
                               relation='stated_in_addition', signs=[1, 1, -1]))
    next(f for f in c4y['figures'] if f['id'] == 'gfy28')['rests_on'] = ['g28cancel', 'i256']
    item('G4x2', f4y, G_PASSAGES, c4y, lambda r: (any(c == 'C9' and 'g28cancel' in d and 'does not change' in d for c, d in r['errors']),
                                                   'C9: two copies of one derivation cancel'), '')
    for name, rev in (('R2rev2', comp('rev', 'difference', ['cm', 'cm'], 0.0, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'))),
                      ('R2rev3', comp('rev', 'sum', ['cm', 'cm'], 0.0, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'),
                                      relation='stated_in_addition', signs=[1, -1]))):          # [46x.2] the reversal as its own subtotal
        rr2 = r2()
        rr2['figures'] = [f for f in rr2['figures'] if f['id'] not in ('talks', 'end')] + [
            est('cm', 6.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'), 'a commitment later reversed', bound='>'), rev,
            comp('end', 'roll_forward', ['bal', 'add18', 'mtk', 'rev'], 46.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'end of FY2027'),
                 relation='overlap_unknown', disputed='add18')]
        rr2['answers'][0]['rung'] = 2
        item(name, R2_FAMILY, R2_PASSAGES, rr2, lambda r: (not r['errors'] and any(x['type'] == 'overlap' and x['alternate'] == [28.5, 28.5]
                                                                                   for x in r['recorded']), 'passes: a separate x - x is exactly zero'), '')
    ramb = r1('c')                                    # [46x.1] two Data Center Q4 forecasts: a starting estimate and an adjusted one
    ramb['figures'] = [f for f in ramb['figures'] if f['id'] not in ('dcq4', 'dcfy')] + [
        comp('dcq4', 'share', ['q4f', 'mix'], 117.6, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4')),
        est('dcq4b', 146.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'), 'reacceleration on top', ['dcq4', 'e976'], adjusts={'figure': 'dcq4', 'type': 'uplift'}),
        comp('dcfy', 'sum', ['dch1', 'dcq3', 'dcq4b'], 415.0, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), relation='time_aggregation')]
    ramb['answers'][1]['rung'] = 2
    item('R1amb', R1_FAMILY, R1_PASSAGES, ramb, lambda r: (any(c == 'C3' and 'FY2027 Q4' in d for c, d in r['errors']), 'C3: refused, deterministically'), '')
    f4b, c4b = g4()                                   # [46y.1] q01's published forecast rests on its subtotal; q22 uses the published one
    sub = next(f for f in c4b['figures'] if f['id'] == 'gfy')
    sub['id'] = 'gfysub'
    c4b['figures'].append(est('gfy', (400.0, 435.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), 'the subtotal, held', ['gfysub']))
    item('G4b', f4b, G_PASSAGES, c4b, lambda r: (not any(c == 'C9' for c, _ in r['errors']), 'no C9: q22 on the published forecast'), '')
    rz = r2()                                         # [46y.2] x - x declared slightly off zero
    rz['figures'] = [f for f in rz['figures'] if f['id'] not in ('talks', 'end')] + [
        est('cm', 6.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'), 'a commitment later reversed', bound='>'),
        comp('rev', 'difference', ['cm', 'cm'], -0.09, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027')),
        est('t35', 3.5, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'rest of FY2027'), 'talks, risk-adjusted'),
        comp('end', 'roll_forward', ['bal', 'add18', 'mtk', 't35', 'rev'], 49.91, 'USD bn', W('NVIDIA', 'equity investment commitments', CO, 'end of FY2027'),
             relation='overlap_unknown', disputed='add18')]
    rz['answers'][0]['rung'] = 2
    item('R2z', R2_FAMILY, R2_PASSAGES, rz, lambda r: (any(c == 'C2' and 'rev' in d and 'exactly' in d for c, d in r['errors']), 'C2: zero is exact'), '')
    rz2 = copy.deepcopy(rz)
    next(f for f in rz2['figures'] if f['id'] == 'rev')['value'] = 0.0
    item('R2z2', R2_FAMILY, R2_PASSAGES, rz2, lambda r: (any(c == 'C6' for c, _ in r['errors']), 'C6: placed by the recomputed $50B, not the declared $49.91B'), '')
    f4b2, c4b2 = g4()                                 # [46z.1] q01 publishes an adjusted forecast; q22 still uses the old subtotal
    sub2 = next(f for f in c4b2['figures'] if f['id'] == 'gfy')
    sub2['id'] = 'gfysub'
    c4b2['figures'].append(est('gfy', (430.0, 460.0), 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), 'the subtotal, adjusted up', ['gfysub'],
                               adjusts={'figure': 'gfysub', 'type': 'uplift'}))
    next(f for f in c4b2['figures'] if f['id'] == 'gfy28c')['inputs'] = ['gfysub', 'g41']
    c4b2['answers'][0]['rung'] = 2
    item('G4b2', f4b2, G_PASSAGES, c4b2, lambda r: (any(c == 'C9' for c, _ in r['errors']), "C9: q22 on q01's superseded subtotal"), '')
    rz3 = copy.deepcopy(rz2)                          # [46z.2] the declared $49.91B on the $50–75B rung: published at the recomputed $50B
    rz3['answers'][0]['rung'] = 3
    MANIFEST['R2z3'] = {'family': R2_FAMILY, 'calc': rz3}
    res3 = cc.check(R2_FAMILY, R2_PASSAGES, rz3)
    rows.append(('R2z3', not res3['errors'] and res3['published']['v29'][:2] == [50.0, 50.0], f'published {res3["published"]["v29"]}', res3))
    rc = r1('c')                                      # [46z.2] both quarters declared 127.1; recomputed Data Center 127.25 above company 127.12
    rc['figures'] = [f for f in rc['figures'] if f['id'] not in ('dcq4', 'dcfy')] + [
        est('g21', 21.2, '%', W('NVIDIA', 'Data Center sequential growth', DC, 'FY2027 Q4'), 'reacceleration'),
        est('dcbr', 1.0, 'x', W('NVIDIA', 'assumption', DC, 'FY2027 Q4'), 'Q3 carried into Q4 at the stated growth', converts=['dcq3']),
        comp('dcq4', 'apply_growth', ['dcq3', 'g21'], 127.1, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027 Q4'), bridge='dcbr'),
        comp('dcfy', 'sum', ['dch1', 'dcq3', 'dcq4'], 396.1, 'USD bn', W('NVIDIA', 'revenue', DC, 'FY2027'), relation='time_aggregation')]
    item('R1canon', R1_FAMILY, R1_PASSAGES, rc, lambda r: (any(c == 'C3' and 'FY2027 Q4' in d for c, d in r['errors']), 'C3 on the recomputed values'), '')
    f4c, c4c = g4()                                   # [46m.2] the single-scenario calculation removed, q01 only cited
    c4c['figures'] = [f for f in c4c['figures'] if f['id'] != 'gfy28c']
    next(f for f in c4c['figures'] if f['id'] == 'gfy28')['rests_on'] = ['gfy', 'i256', 'i173']
    item('G4c', f4c, G_PASSAGES, c4c, lambda r: (any(c == 'C9' and 'no calculation' in d for c, d in r['errors']), 'C9: a citation for a calculation'), '')
    p3e = copy.deepcopy(p3a)
    p3e['answers'][0]['outcome'] = 'pri'
    p3e['answers'][0]['reference'] = {'figure': 'gc392'}
    item('P3e', f1p, G_PASSAGES, p3e, lambda r: (any(c == 'C10' and 'current outcome' in d for c, d in r['errors']), 'C10: a prior as the outcome'), '')
    p3d = copy.deepcopy(p3a)
    p3d['answers'][0]['reference'] = {'figure': 'pri', 'unavailable': 'no consensus supplied'}
    item('P3d', f1p, G_PASSAGES, p3d, lambda r: (any(c == 'C5' and 'exactly one' in d for c, d in r['errors']), 'C5: both a figure and unavailable'), '')
    p3c = copy.deepcopy(p3a)
    next(f for f in p3c['figures'] if f['id'] == 'pri')['value'] = 431.0
    item('P3c', f1p, G_PASSAGES, p3c, lambda r: ('C10' in codes(r), 'C10: a prior figure the earlier answer does not state'), '')
    p3b = copy.deepcopy(c1)
    p3b['figures'].append(est('wrap', 425.0, 'USD bn', W('NVIDIA', 'revenue', CO, 'FY2027'), 'our earlier forecast, close to the Street', ['gc392']))
    p3b['answers'][0]['reference'] = {'figure': 'wrap'}
    item('P3b', f1, G_PASSAGES, p3b, lambda r: (codes(r) == {'C5'}, 'C5 only'), '')

    f3, c3 = g3()
    p4 = copy.deepcopy(c3)
    next(f for f in p4['figures'] if f['id'] == 'gasp')['what']['scope'] = 'Rubin GPU'      # a price of another product
    item('P4', f3, G_PASSAGES, p4, lambda r: (codes(r) == {'C8'} and any('gunits' in d for _, d in r['errors']),
                                               'C8 only, on gunits: the per-unit identity needs one scope'), '')

    g3inv = copy.deepcopy(c3)
    g3inv['figures'].append(comp('gback', 'product', ['gunits', 'gasp'], 20.0, 'USD bn', W('NVIDIA', 'revenue', 'Vera CPU', 'FY2027')))
    item('G3inv', f3, G_PASSAGES, g3inv, lambda r: (not r['errors'], 'the per-unit inverse gives $20B'), '')
    f4, c4 = g4()
    g4m = copy.deepcopy(c4)
    next(f for f in g4m['figures'] if f['id'] == 'gfy28c')['inputs'] = ['gc392', 'g41']
    next(f for f in g4m['figures'] if f['id'] == 'gfy28c').update(low=552.72, high=552.72)
    item('G4m', f4, G_PASSAGES, g4m, lambda r: ('C9' in codes(r), "C9: FY2028 rests on consensus, not q01's forecast"), '')
    r4m = r4()
    next(f for f in r4m['figures'] if f['id'] == 'cpu28')['bound'] = '<'
    item('R4m', R4_FAMILY, R4_PASSAGES, r4m, lambda r: (any(c == 'C2' and 'cpu28' in d for c, d in r['errors']), 'C2: the bound direction reversed'), '')

    # T1–T9: the C1 forms on real passages
    t_pass = {**R1_PASSAGES, **R3_PASSAGES, **R4_PASSAGES}
    tests = [
        ('T1', src('t', 'e2499', '$108.0 billion, plus or minus 2%', 108.0, 'USD bn', 'guidance', W('x', 'x', 'x', 'x'), 'midpoint'), True),
        ('T2', src('t', 'e1786', 'more than $730 billion', 730.0, 'USD bn', 'reported', W('x', 'x', 'x', 'x'), 'bound', '>'), True),
        ('T3a', src('t', 'e2535', 'nearly $800 billion', 800.0, 'USD bn', 'guidance', W('x', 'x', 'x', 'x'), 'bound', 'approx_below'), True),
        ('T3b', src('t', 'e2535', '$1.3 trillion', 1300.0, 'USD bn', 'guidance', W('x', 'x', 'x', 'x')), True),
        ('T4', src('t', 'e3660', 'more than double', 2.0, 'x', 'guidance', W('x', 'x', 'x', 'x'), 'multiplier', '>'), True),
        ('T5a', src('t', 'e1786', '$730 billion', 730.0, 'USD bn', 'reported', W('x', 'x', 'x', 'x')), False),
        ('T5b', src('t', 'e2535', '$800 billion', 800.0, 'USD bn', 'guidance', W('x', 'x', 'x', 'x')), False),
        ('T6', src('t', 'e3660', 'double', 2.0, 'x', 'guidance', W('x', 'x', 'x', 'x'), 'multiplier'), False),
        ('T7', src('t', 'e2499', '$108.0 billion, plus or minus 2%', 108.5, 'USD bn', 'guidance', W('x', 'x', 'x', 'x'), 'midpoint'), False),
        ('T8', src('t', 'e1786', 'more than $730 billion', 730.0, 'USD bn', 'reported', W('x', 'x', 'x', 'x'), 'value'), False),
        ('T9', src('t', 'e2535', '$800 billion', 800.0, 'USD bn', 'guidance', W('x', 'x', 'x', 'x'), 'bound', 'approx_below'), False),
    ]
    for name, fig, accept in tests:
        errs = cc._source_errors(fig, t_pass)
        ok = (not errs) == accept and (name != 'T9' or any('not a complete numeric expression' in d for _, d in errs))
        rows.append((name, ok, 'accepted' if accept else 'refused', {'errors': errs, 'recorded': []}))

    # U1–U2: the paths
    u1 = r1('c')
    u1['answers'][1] = {'view_id': 'v9', 'shape': 'unresolved', 'why': 'the segment mix after Q2 is not stated', 'cites': [], 'changed': True,
                        'why_changed': 'w'}
    res = cc.check(R1_FAMILY, R1_PASSAGES, u1)
    decision = cc.publish_decision(R1_FAMILY, u1, res)
    rows.append(('U1', decision == 'held' and not res['errors'], f'decision {decision}', res))
    res_bad = cc.check(f1, G_PASSAGES, p2)
    outcome = cc.family_outcome([cc.publish_decision(f1, p2, res_bad), cc.publish_decision(f1, p2, res_bad)])
    rows.append(('U2', outcome == 'unresolved', f'two refusals give {outcome}', res_bad))
    return rows


def main():
    rows = run()
    lines = ['judging-v13 $0 gate (DESIGN.md v5 §6)', '']
    for name, ok, note, result in rows:
        lines.append(f'{"PASS" if ok else "MISS"}  {name:5}  {note}')
        for code, detail in result['errors']:
            lines.append(f'        {code}: {detail}')
        for rec in result['recorded']:
            lines.append(f'        recorded: {json.dumps(rec)}')
    misses = [r[0] for r in rows if not r[1]]
    lines += ['', f'{len(rows)} items, {len(rows) - len(misses)} pass, misses: {misses or "none"}',
              'GATE PASS' if not misses else 'GATE FAIL']
    text = '\n'.join(lines)
    print(text)
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(text + '\n')
        Path(sys.argv[1]).with_suffix('.fixtures.json').write_text(json.dumps(MANIFEST, indent=1, sort_keys=True))
    return 0 if not misses else 1


if __name__ == '__main__':
    raise SystemExit(main())
