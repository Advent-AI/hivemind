"""Dry run of the Stage A reading ($0): hand-written ladders, right ones and ones with one planted fault each, as the judge would be
shown them, mixed in a fixed shuffled order. Writes the packet (no labels) and the key (which item carries which fault) beside
this script. On 2026-11-10 the script and the key were kept outside the repository until both readers had answered, then copied here."""
import copy, json, random
from pathlib import Path

REPO = Path('/Users/lchingen/hivemind')
CENSUS = json.loads((REPO / 'clean-arch/step4-2026-11-10/census/packet.json').read_text())
OUT = REPO / 'clean-arch/step4-2026-11-10/dryrun'
HERE = Path(__file__).resolve().parent
BULL = ['Strongly bullish', 'Bullish', 'Neutral', 'Bearish', 'Strongly bearish']


def thesis(run, tid):
    return next(t for t in CENSUS if t['run'] == run and t['id'] == tid)


def shown(obj, kind, question, year, due, rungs):
    return {'object': obj, 'kind': kind, 'question': question, 'year': year, 'due_day': due,
            'rungs': [{'position': n, 'label': l, 'condition': c} for n, (l, c) in enumerate(rungs, 1)]}


BASE = {}
# E1 company yes/no (u1 clean-3)
BASE['E1'] = dict(thesis=('u1', 'clean-3'), shown=shown('NVDA', 'asset', "Will NVIDIA's Vera Rubin platform have begun first shipments by 2026-12-31?", '2026', '2026-12-31', [
    ('Yes', 'First shipments of Vera Rubin are confirmed to have taken place on or before 2026-12-31.'),
    ('No', 'No first shipment of Vera Rubin is confirmed to have taken place on or before 2026-12-31.')]),
    extra=dict(not_judged=[], reference={'words': 'could begin shipping later this year', 'value': None}, favourable_end=None, due_day_basis='period_end'))
# E7 company yes/no with a part left out and listed (u1 clean-2)
BASE['E7'] = dict(thesis=('u1', 'clean-2'), shown=shown('NVDA', 'asset', "Will NVIDIA sign a guarantee or backstop for OpenAI's lease of the Ohio data center by 2027-12-31?", '2027', '2027-12-31', [
    ('Yes', "NVIDIA is confirmed to have signed a guarantee or backstop for OpenAI's lease of the Ohio data center on or before 2027-12-31."),
    ('No', 'No such guarantee or backstop is confirmed to have been signed on or before 2027-12-31.')]),
    extra=dict(not_judged=[{'part': 'the amount of the guarantee', 'why': 'no amount exists until a guarantee is signed; the outcome tracks the signing'}],
               reference={'words': 'negotiating to provide financial guarantees for OpenAI', 'value': None}, favourable_end=None, due_day_basis='stated'))
# E2 company five states (u2 clean-9)
E2_STATES = [
    ('Strongly bullish', 'The authority has closed the investigation with no finding against NVIDIA.'),
    ('Bullish', 'The authority has accepted commitments offered by NVIDIA and imposed no fine.'),
    ('Neutral', 'The authority has announced no decision.'),
    ('Bearish', 'The authority has imposed a fine and ordered no remedy.'),
    ('Strongly bearish', 'The authority has ordered remedies of its own, with or without a fine.')]
BASE['E2'] = dict(thesis=('u2', 'clean-9'), shown=shown('NVDA', 'asset', "What will France's competition authority have decided in its antitrust investigation into NVIDIA by 2027-01-31?", '2027', '2027-01-31', E2_STATES),
    extra=dict(not_judged=[], reference={'words': 'nearing a conclusion', 'value': None}, favourable_end=None, due_day_basis='period_end'))
# E3 theme five states (u3 clean-12)
E3_STATES = [
    ('Guidance eased', 'The Commerce Department has withdrawn or relaxed its May 2026 guidance.'),
    ('Guidance only', 'The May 2026 guidance stands and no binding rule has been proposed or issued.'),
    ('Rule proposed', 'A binding licensing rule for third-country shipments has been proposed and is not yet in force.'),
    ('Rule in force for named countries', 'A binding licensing requirement is in force for shipments to a named list of third countries.'),
    ('Rule in force for all third countries', 'A binding licensing requirement or ban is in force for shipments to every third country outside an exempt list.')]
BASE['E3'] = dict(thesis=('u3', 'clean-12'), shown=shown('chip-export-controls', 'theme', 'How far will US export restrictions on advanced AI-chip shipments to third countries have gone by 2027-01-31?', '2027', '2027-01-31', E3_STATES),
    extra=dict(not_judged=[{'part': "the resulting constraint on Nvidia's sales to those markets", 'why': 'the outcome tracks the rule; the effect on sales is read from later results'}],
               reference=None, favourable_end=None, due_day_basis='period_end'))
# E4 company figure, no reference (u1 clean-7)
BASE['E4'] = dict(thesis=('u1', 'clean-7'), shown=shown('NVDA', 'asset', 'What amount of supply and purchase commitments will NVIDIA report outstanding at its FY2027 year-end?', 'FY2027', '2027-02-28', [
    ('Strongly bullish', 'below 80,000,000,000 USD'), ('Bullish', 'from 80,000,000,000 USD to below 110,000,000,000 USD'),
    ('Neutral', 'from 110,000,000,000 USD to below 140,000,000,000 USD'), ('Bearish', 'from 140,000,000,000 USD to below 180,000,000,000 USD'),
    ('Strongly bearish', '180,000,000,000 USD or more')]),
    extra=dict(not_judged=[], reference=None, favourable_end='lower',
               favourable_why='A lower figure leaves less cash committed if AI demand disappoints, the risk the item raises.', due_day_basis='expected_publication'))
# E5 theme figure with a reference (u1 clean-4)
REF5 = 'Next year, Nvidia projects that this figure could reach $1 trillion.'
BASE['E5'] = dict(thesis=('u1', 'clean-4'), shown=shown('ai-capex', 'theme', 'What will the combined data-center capital expenditure of the big four AI hyperscalers be in calendar 2027?', '2027', '2028-02-15', [
    ('below 700,000,000,000 USD', 'below 700,000,000,000 USD'),
    ('from 700,000,000,000 USD to below 900,000,000,000 USD', 'from 700,000,000,000 USD to below 900,000,000,000 USD'),
    ('from 900,000,000,000 USD to below 1,100,000,000,000 USD', f'from 900,000,000,000 USD to below 1,100,000,000,000 USD (the reference when the question opened: "{REF5}")'),
    ('from 1,100,000,000,000 USD to below 1,300,000,000,000 USD', 'from 1,100,000,000,000 USD to below 1,300,000,000,000 USD'),
    ('1,300,000,000,000 USD or more', '1,300,000,000,000 USD or more')]),
    extra=dict(not_judged=[], reference={'words': REF5, 'value': 1000000000000}, favourable_end='n/a', due_day_basis='expected_publication'))
# E6 a refusal that is right (u2 clean-10)
BASE['E6'] = dict(thesis=('u2', 'clean-10'), shown={'no_ladder': "The topic's outcome names two things, new HBM capacity and whether record memory prices persist, and neither is the main one."}, extra={})


def variant(base, **changes):
    item = copy.deepcopy(BASE[base])
    for path, value in changes.items():
        target = item
        keys = path.split('__')
        for k in keys[:-1]:
            target = target[int(k) if k.isdigit() else k]
        target[int(keys[-1]) if keys[-1].isdigit() else keys[-1]] = value
    return item


WRONG = {}
w = variant('E1'); w['shown']['rungs'][0]['condition'], w['shown']['rungs'][1]['condition'] = w['shown']['rungs'][1]['condition'], w['shown']['rungs'][0]['condition']
WRONG['W1'] = (w, 'R', 'the Yes and No conditions are swapped')
w = variant('E2'); w['shown']['rungs'][0]['condition'], w['shown']['rungs'][4]['condition'] = w['shown']['rungs'][4]['condition'], w['shown']['rungs'][0]['condition']
WRONG['W2'] = (w, 'F', 'ordered remedies labelled Strongly bullish and closure Strongly bearish')
w = variant('E1'); w['shown'] = shown('NVDA', 'asset', "Will NVIDIA's Rubin Ultra platform have begun first shipments by 2027-12-31?", '2027', '2027-12-31', [
    ('Yes', 'First shipments of Rubin Ultra are confirmed to have taken place on or before 2027-12-31.'),
    ('No', 'No first shipment of Rubin Ultra is confirmed to have taken place on or before 2027-12-31.')])
w['extra']['reference'] = None
WRONG['W3'] = (w, 'Q', 'the question is about another product and date than the thesis outcome')
WRONG['W4'] = (variant('E7', extra__not_judged=[]), 'L', 'the amount part of the thesis wording is left out and not listed')
w = variant('E1'); w['shown']['question'] = w['shown']['question'].replace('2026-12-31', '2026-09-30'); w['shown']['due_day'] = '2026-09-30'
for r in w['shown']['rungs']: r['condition'] = r['condition'].replace('2026-12-31', '2026-09-30')
w['extra']['due_day_basis'] = 'stated'
WRONG['W5'] = (w, 'D', 'the due day 2026-09-30 is supported by neither the thesis nor the article')
w = variant('E4'); w['shown']['object'] = 'ai-capex'; w['shown']['kind'] = 'theme'; w['shown']['year'] = '2027'
for r in w['shown']['rungs']: r['label'] = r['condition']
w['extra']['favourable_end'] = 'n/a'; w['extra'].pop('favourable_why', None)
WRONG['W6'] = (w, 'O', "the company's own commitments are filed under a theme")
w = variant('E5'); w['shown']['rungs'] = [{'position': n, 'label': c, 'condition': c} for n, c in enumerate([
    'below 450,000,000,000 USD', 'from 450,000,000,000 USD to below 600,000,000,000 USD', 'from 600,000,000,000 USD to below 700,000,000,000 USD',
    'from 700,000,000,000 USD to below 850,000,000,000 USD', '850,000,000,000 USD or more'], 1)]
w['extra']['reference'] = None
WRONG['W7'] = (w, 'X', "the article's stated expectation ($1 trillion) is left out and sits in the top rung")
WRONG['W8'] = (variant('E5', shown__year='2026'), 'Y', 'the year shown is 2026 for a calendar-2027 question')
w = variant('E4'); 
for r, c in zip(w['shown']['rungs'], ['below 1,000,000,000 USD', 'from 1,000,000,000 USD to below 2,000,000,000 USD', 'from 2,000,000,000 USD to below 5,000,000,000 USD',
                                       'from 5,000,000,000 USD to below 10,000,000,000 USD', '10,000,000,000 USD or more']):
    r['condition'] = c
WRONG['W9'] = (w, 'G', 'the article states $119 billion; every plausible outcome falls in the top rung')
w = variant('E1'); w['shown'] = {'no_ladder': 'Nothing in the topic can be checked on a date.'}; w['extra'] = {}
WRONG['W10'] = (w, 'N', 'a dated shipment question is refused as uncheckable')
w = variant('E3'); w['shown']['rungs'][3]['label'] = 'Rule proposed or in force for named countries'
w['shown']['rungs'][3]['condition'] = 'A binding licensing rule for third-country shipments has been proposed, or is in force for shipments to a named list of third countries.'
WRONG['W11'] = (w, 'R', 'two states overlap: a proposed rule satisfies rungs 3 and 4')

items = [(k, v, None, None) for k, v in BASE.items()] + [(k, v[0], v[1], v[2]) for k, v in WRONG.items()]
random.Random(20261110).shuffle(items)
packet, key = [], {}
for n, (source, item, mark, what) in enumerate(items, 1):
    t = thesis(*item['thesis'])
    packet.append({'item': n, 'thesis': t['thesis'], 'article': {k: t['article'][k] for k in ('publication_date', 'publisher', 'title', 'text')},
                   'ladder_as_the_judge_is_shown_it': item['shown'], 'other_fields': item['extra']})
    key[str(n)] = {'source': source, 'thesis': list(item['thesis']), 'planted_mark': mark, 'planted_fault': what}
OUT.mkdir(exist_ok=True)
(OUT / 'packet.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False))
(HERE / 'dryrun_key.json').write_text(json.dumps(key, indent=1))
print(len(packet), 'items;', sum(1 for v in key.values() if v['planted_mark']), 'with a planted fault;', (OUT / 'packet.json').stat().st_size, 'bytes')
