"""Render one stored family's judging-v13 request (old-2 calls 8729 and 8737 on 2026-09-20) and check a conforming answer through the
v13 schema (model.check_schema) and calc_check. Harness-only, $0, no model call. Usage: python3 render_v13.py [out-prefix]"""
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'src'))
import calc_check as cc  # noqa: E402
import calc_small  # noqa: E402
import gate  # noqa: E402
from hivemind import model  # noqa: E402

S, N = {'type': 'string'}, {'type': 'number'}


def nullable(schema):
    return {'anyOf': [schema, {'type': 'null'}]}


def obj(props, desc=None):
    out = {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}
    if desc:
        out['description'] = desc
    return out


def v13_schema(member_ids, evidence_ids, theme_ids):
    what = obj({k: S for k in ('population', 'measure', 'scope', 'period')},
               'What the number measures: population, measure (the quantity, such as revenue or units; never its basis), scope, period.')
    figure = obj({
        'id': S, 'what': what,
        'basis': {'type': 'string', 'enum': sorted(cc.BASES - {'prior_forecast'}), 'description': 'reported: an actual; guidance: the company\'s '
                  'outlook; consensus: analysts\' average; third_party: one outside party; forecast: this family\'s forecast.'},
        'scenario': S,
        'kind': {'type': 'string', 'enum': ['computed', 'estimate', 'source'], 'description': 'source: stated in a shown passage; computed: one '
                 'operation on named figures; estimate: your judgement, stated as yours.'},
        'value': nullable(N), 'low': nullable(N), 'high': nullable(N),
        'bound': nullable({'type': 'string', 'enum': ['>', '>=', '<', '<=', 'approx', 'approx_below', 'approx_above']}),
        'unit': S,
        'evidence': nullable(S),
        'expression': nullable({'type': 'string', 'description': 'Source only: the complete numeric expression exactly as the passage writes '
                                'it, qualifiers included (for example "more than $2 billion", "$4.5 billion, plus or minus 3%", "more than triple").'}),
        'component': nullable({'type': 'string', 'enum': ['value', 'bound', 'midpoint', 'relative', 'low', 'high', 'multiplier']}),
        'inputs': nullable({'type': 'array', 'items': S}),
        'operation': nullable({'type': 'string', 'enum': sorted(cc.OPERATIONS)}),
        'signs': nullable({'type': 'array', 'items': N}),
        'relation': nullable({'type': 'string', 'enum': ['time_aggregation', 'accounting_parts', 'stated_in_addition', 'overlap_unknown'],
                              'description': 'Sum and roll_forward: periods of one quantity; declared parts of a whole; a source says they add; '
                              'unknown overlap (name the disputed figure).'}),
        'disputed': nullable(S),
        'bridge': nullable({'type': 'string', 'description': 'Only when no listed identity covers the operation (periods of one quantity, '
                            'declared parts, a balance and its flows, a stated share or multiplier, a total over a per-unit price): an '
                            'estimate stating the conversion and listing the operands it converts.'}),
        'basis_text': nullable(S), 'rests_on': nullable({'type': 'array', 'items': S}),
        'adjusts': nullable(obj({'figure': S, 'type': {'type': 'string', 'enum': ['discount', 'uplift', 'trim']}})),
        'converts': nullable({'type': 'array', 'items': S}),
    })
    push = obj({'evidence_id': {'type': 'string', 'enum': evidence_ids}, 'push': {'type': 'string', 'enum': ['toward_first', 'toward_last', 'none']}})
    theme_push = obj({'view_id': {'type': 'string', 'enum': theme_ids or ['none']},
                      'push': {'type': 'string', 'enum': ['toward_first', 'toward_last', 'none']}})
    answer = obj({
        'view_id': {'type': 'string', 'enum': member_ids},
        'shape': {'type': 'string', 'enum': ['forecast', 'unresolved']},
        'outcome': nullable(S), 'rung': nullable({'type': 'integer'}),
        'reference': nullable(obj({'figure': nullable(S), 'unavailable': nullable(S)}, 'An external figure, or a calculation from external '
                              'and reported figures, or unavailable with why.')),
        'reasons': S, 'why': nullable(S),
        'cites': {'type': 'array', 'items': {'type': 'string', 'enum': evidence_ids}},
        'pushes': {'type': 'array', 'items': push}, 'theme_pushes': {'type': 'array', 'items': theme_push},
    })
    return obj({'figures': {'type': 'array', 'items': figure}, 'answers': {'type': 'array', 'items': answer}})


QUALIFIERS = list(calc_small.QUALIFIERS)                 # one owner: the checker's closed list


def v13s_schema(member_ids, evidence_ids, theme_ids):
    """The small format (SMALL-DESIGN.md §3 [52], D737, D738): each rule the checks enforce stated beside its field."""
    members = {'type': 'array', 'items': {'type': 'string', 'enum': member_ids}}
    what = obj({'population': S,
                'measure': {'type': 'string', 'description': 'The quantity, such as revenue or capital expenditure; never its basis.'},
                'scope': S,
                'period': {'type': 'string', 'description': 'For example FY2027, FY2027 Q3, FY2027 H1, FY2027 Q1-Q3, CY2026, end of FY2027.'}},
               'What the number measures. Where the request lists keys (outcome keys, shared quantities), copy them exactly.')
    figure = obj({
        'id': {'type': 'string', 'description': 'Short and unique, such as F1; never a passage id.'},
        'what': what,
        'kind': {'type': 'string', 'enum': ['source', 'computed', 'estimate'], 'description': "source: a number written in a shown passage's "
                 'quote; computed: one operation on other figures; estimate: your judgement, with its assumption in basis_text.'},
        'basis': {'type': 'string', 'enum': ['reported', 'guidance', 'consensus', 'third_party', 'forecast'], 'description': "reported: an "
                  "actual; guidance: the company's outlook; consensus: analysts' average; third_party: one outside party; forecast: this "
                  "family's own forecast, on a computed or estimate figure only."},
        'value': nullable({'type': 'number', 'description': 'A point. Give value, or low and high, never both.'}),
        'low': nullable({'type': 'number', 'description': 'A range, low at most high, with value null.'}),
        'high': nullable({'type': 'number', 'description': 'A range, low at most high, with value null.'}),
        'unit': {'type': 'string', 'enum': ['USD bn', '%', 'x'], 'description': 'USD bn: money in billions of US dollars ($1.2 trillion = '
                 '1200; $500 million = 0.5). %: a percentage as its number (7.5% = 7.5). x: a multiple (double = 2).'},
        'evidence_id': nullable({'type': 'string', 'enum': evidence_ids, 'description': 'Source only: the passage whose quote holds the number.'}),
        'quote_number': nullable({'type': 'string', 'description': "Source only: a complete number exactly as the quote writes it, never a "
                                  "piece of a longer number, range or 'plus or minus' expression, with its currency and scale or its percent "
                                  "sign, and nothing else: '$4.5 billion', 'US$300 million', '$2.1bn', '40%', '-3%', "
                                  "'double', 'twice'. The value is the number as written (a minus only when the quote writes one). A written "
                                  "range in full ('$3–4 billion', 'between $3 billion and $4 billion', '$3 billion to $4 billion'), given as low and high; a change "
                                  "written 'from $3 billion to $5 billion' is two numbers, each copied alone. '$4.5 billion, "
                                  "plus or minus 3%' in full, given as low and high or its midpoint as value. Only US dollars."}),
        'qualifier': nullable({'type': 'string', 'enum': QUALIFIERS, 'description': "Source only: the qualifier the quote writes just before "
                               "the number (or 'or more' / 'or less' just after); none when there is none."}),
        'inputs': nullable({'type': 'array', 'items': S, 'description': "Computed only: ids of figures, never passages, in the operation's order."}),
        'operation': nullable({'type': 'string', 'enum': ['sum', 'difference', 'product', 'ratio', 'share', 'growth', 'apply_growth'],
                               'description': 'Computed only. sum(a, b, …) = a + b + … (one unit); difference(a, b) = a − b (one unit); '
                               'product(a, b, …) = a × b × … (USD bn × x, x × x or % × x; never USD bn × %); ratio(a, b) = a ÷ b (same units '
                               'give x; a ÷ x keeps a\'s unit); share(whole, percent) = whole × percent ÷ 100, the percent from 0 to 100; '
                               'growth(old, new) = the % change, in one unit; apply_growth(base, rate %) = base × (1 + rate ÷ 100). sum and '
                               'product take two or more inputs; the others exactly two. Never divide by a figure that can be zero. A range '
                               'input gives a range: compute both extremes, a figure used twice taking one value; you may declare the '
                               'midpoint as value. The figure equals the result within 0.5% (at least 0.1, or 0.05 for %). A sum never adds '
                               "a figure of the part's quantity to one of the whole's for the same period (the whole already includes the "
                               'part); a difference may take the part from the whole of the same period only to give the rest. A sum never adds '
                               'one quantity for the same period twice. When '
                               'a sum or difference combines periods of one quantity, write them FY2027, FY2027 Q3, FY2027 H1 or FY2027 '
                               "Q1-Q3 (or CY likewise), and they make up the output's period exactly (Q1 + Q2 = H1; FY − Q1-Q3 = Q4)."}),
        'basis_text': nullable({'type': 'string', 'description': 'Estimate only: the assumption, in words.'}),
        'rests_on': nullable({'type': 'array', 'items': S, 'description': 'Estimate only: the ids of the figures and passages it rests on.'}),
        'outcome_for': dict(members, description='The members whose forecast this figure is: your own forecast (a computed or estimate figure '
                            'with basis forecast, even when it agrees with consensus), exactly one for each member answered as a forecast, '
                            "none for an unresolved one. Its what is the member's outcome key, in USD bn."),
        'reference_for': dict(members, description="The members for which this figure is the market's reference. It and every figure beneath "
                              'it is a source or a computed figure, never an estimate or a forecast, and at least one of them is a quoted '
                              "consensus, guidance or outside figure. A past period's reported share or multiple carried to another period "
                              "(a quarter's mix applied to the year) makes it our comparison estimate, not the market's reference."),
    })
    push = obj({'evidence_id': {'type': 'string', 'enum': evidence_ids}, 'push': {'type': 'string', 'enum': ['toward_first', 'toward_last', 'none']}})
    theme_push = obj({'view_id': {'type': 'string', 'enum': theme_ids or ['none']},
                      'push': {'type': 'string', 'enum': ['toward_first', 'toward_last', 'none']}})
    answer = obj({
        'view_id': {'type': 'string', 'enum': member_ids},
        'shape': {'type': 'string', 'enum': ['forecast', 'unresolved'], 'description': 'forecast: a figure marked in outcome_for, a rung, and '
                  'a reference (a figure marked in reference_for, or reference_unavailable). unresolved: why; rung and reference_unavailable '
                  'null; no figure marked for it.'},
        'rung': nullable({'type': 'integer', 'description': 'Forecast only: the rung whose band holds the outcome as the code recomputes it '
                          '(a band includes its lower edge, not its upper); for a range outcome, a band it overlaps, with the reason in reasons.'}),
        'reference_unavailable': nullable({'type': 'string', 'description': 'Forecast only, when no figure is marked as its reference: why.'}),
        'reasons': S,
        'why': nullable({'type': 'string', 'description': 'Unresolved only: why the evidence cannot support a forecast.'}),
        'cites': {'type': 'array', 'items': {'type': 'string', 'enum': evidence_ids}},
        'pushes': {'type': 'array', 'items': push}, 'theme_pushes': {'type': 'array', 'items': theme_push},
    })
    return obj({'figures': {'type': 'array', 'items': figure, 'description': 'The family\'s calculation. Use one forecast figure for each '
                            'quantity and period, as a point or a range, wherever that quantity is needed (outside figures beneath it, or a '
                            'point a final range rests on, are fine). Guidance may inform a growth pace: record the pace you forecast as an estimate, say why '
                            'it applies, name the benchmark in rests_on, and use that estimate in the calculation. A rate computed from a shared '
                            'quantity\'s guidance or outside figure is never itself an input of the calculation. '
                            'To turn a total into a narrower quantity (data-center spending out of total capital expenditure), write the '
                            'deduction or share as its own figure, or give a supported bound; never relabel a total as the narrower quantity. '
                            'Figures name each other by id; no figure may depend on itself.'},
                'answers': {'type': 'array', 'items': answer}})


def v13s_header(family, shown):
    """[52] The family header's rule lines, rendered from the family's data."""
    lines = []
    for r in family.get('relations', []):
        if r['type'] == 'part_of' and {r['part'], r['whole']} <= shown:
            periods = ', '.join(p for p in family.get('compare_periods', []) if p != family['members'][r['part']]['what']['period'])
            lines.append(f'Relations: {r["part"]} is part of {r["whole"]}. For each of {periods} and for the outcomes, the part\'s figure may '
                         'not exceed the whole\'s: for every value of anything both rest on, and otherwise the part\'s low end may not exceed '
                         'the whole\'s high end.')
    if not lines:
        lines.append('Relations: none.')
    for ps in family.get('part_scopes', []):
        lines.append(f'Scopes: {ps["population"]} {ps["measure"]} {ps["part"]} is part of {ps["population"]} {ps["measure"]} {ps["whole"]}. A sum '
                     'never adds the part into the whole for the same period; a difference may take the part from the whole of the same '
                     'period only to give the rest.')
    shared = '; '.join(f'{w["population"]}, {w["measure"]}, {w["scope"]}, {w["period"]}' for w in family.get('shared', [])) or 'none'
    lines.append(f'Shared quantities, one forecast figure each; on every arithmetic path from an outcome, through rates and multiples too, '
                 f'the first figure of that quantity reached is its forecast: {shared}.')
    keys = '; '.join(f'{v} = {m["what"]["population"]} | {m["what"]["measure"]} | {m["what"]["scope"]} | {m["what"]["period"]}'
                     + (f' ({m["key_note"]})' if m.get('key_note') else '') for v, m in family.get('members', {}).items() if v in shown)
    lines.append(f'Outcome keys (population | measure | scope | period), in USD bn, to be used exactly: {keys}.')
    return '\n'.join(lines) + '\n'


def parts(user):
    head, rest = user.split('\n\n[Evidence in view', 1)
    evidence = '[Evidence in view' + rest.split('\n\n[', 1)[0]
    tail = '\n\n[' + rest.split('\n\n[', 1)[1] if '\n\n[' in rest else ''
    blocks = {b.split(']', 1)[0]: '[' + b for b in tail.split('\n\n[')[1:]}
    return head, evidence, blocks


def render(archive_path, calls, family, shown=None, fmt='v13'):
    """The v13 user message for a family from its members' stored requests: the members in `shown` (default: all) get a header; the
    evidence in view is the union over every call, each passage once; the themes once; each member's exact figure keys. fmt 'v13s'
    gives the small format's header lines (v13's bytes are unchanged)."""
    archive = sqlite3.connect(f'file:{archive_path}?mode=ro', uri=True)
    heads, lines, seen, themes, earlier = [], [], set(), '', []
    shown = set(shown) if shown is not None else {v for v, _ in calls}
    for view_id, call_id in calls:
        user = json.loads(archive.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])['messages'][1]['content']
        head, evidence, blocks = parts(user)
        if view_id in shown:
            heads.append(head)
        for item in evidence.split('\n- ')[1:]:
            eid = item.split(' ', 1)[0]
            if eid not in seen:
                seen.add(eid)
                lines.append('- ' + item)
        themes = themes or next((v for k, v in blocks.items() if k.startswith('Themes')), '')
        prev = next((v for k, v in blocks.items() if k.startswith('Previous')), '').split('\n\nAnswer per the JSON schema')[0]   # [46g.1] v7's output line goes
        earlier.append(f'- {view_id}: ' + prev.replace('[Previous conclusion, for comparison only]', 'our earlier forecast, not a source:').strip())
    rel = '; '.join(f'{r["part"]} is part of {r["whole"]}' if r['type'] == 'part_of' else f'{r["later"]} rests on {r["earlier"]}\'s base'
                    for r in family['relations'] if {r.get('part'), r.get('whole'), r.get('later'), r.get('earlier')} - {None} <= shown) or 'none'
    shared = '; '.join(f'{w["population"]}, {w["measure"]}, {w["scope"]}, {w["period"]}' for w in family['shared']) or 'none'
    keys = '; '.join(f'{v} = {m["what"]["population"]} | {m["what"]["measure"]} | {m["what"]["scope"]} | {m["what"]["period"]}'
                     for v, m in family.get('members', {}).items() if v in shown)
    if fmt == 'v13s':
        header = v13s_header(family, shown)
    else:
        header = (f'Relations: {rel}.\nShared quantities, one forecast each per scenario: {shared}.\n'
                  + (f'Outcome keys (population | measure | scope | period), to be used exactly: {keys}.\n' if keys else ''))
    user = ('[Family] members:\n' + '\n\n'.join(heads) + '\n\n' + header + '\n'
            f'[Evidence in view for the family, {len(lines)} items]\n' + '\n'.join(lines) + '\n\n' + themes
            + '\n\nAnswer per the JSON schema: one calculation for the family and one answer per member.')   # D728: no earlier forecast
    return user, sorted(seen), [t.split(' ', 1)[0] for t in themes.split('\n- ')[1:]]


def strict(calc, schema):
    """Fill every optional field with null, as strict structured output returns it."""
    fprops = schema['properties']['figures']['items']['properties']
    aprops = schema['properties']['answers']['items']['properties']
    figs = [{k: f.get(k) for k in fprops} for f in calc['figures']]
    for f in figs:
        f['scenario'] = f['scenario'] or 'base'
        if f['what'] is None:
            f['what'] = {'population': '', 'measure': '', 'scope': '', 'period': ''}
    answers = []
    for a in calc['answers']:
        a2 = {k: a.get(k) for k in aprops}
        if a2['reference'] is not None:
            a2['reference'] = {'figure': a['reference'].get('figure'), 'unavailable': a['reference'].get('unavailable')}
        a2['why'] = a.get('why')
        answers.append(a2)
    return {'figures': figs, 'answers': answers}


def without_nulls(calc):
    clean = lambda d: {k: v for k, v in d.items() if v is not None}
    answers = []
    for a in calc['answers']:
        a2 = clean(a)
        if 'reference' in a2:
            a2['reference'] = clean(a2['reference'])
        answers.append(a2)
    return {'figures': [clean(f) for f in calc['figures']], 'answers': answers}


def main():
    archive = REPO / 'poc/data/comparison-2026-11-17/run/old-2/prod/archive.sqlite'
    system = (HERE / 'judging-v13-draft.txt').read_text()
    user, evidence_ids, theme_ids = render(archive, [('v14', 8729), ('v9', 8737)], gate.R1_FAMILY)
    schema = v13_schema(['v14', 'v9'], evidence_ids, theme_ids)
    calc = gate.r1('c')
    answer = strict(calc, schema)
    schema_errors = model.check_schema(answer, schema)
    for a in answer['answers']:
        a['cites'] = [e for e in a['cites'] if e in evidence_ids]
    result = cc.check(gate.R1_FAMILY, gate.R1_PASSAGES, without_nulls(answer))
    missing = sorted({f['evidence'] for f in calc['figures'] if f.get('evidence')} - set(evidence_ids))
    report = [f'system {len(system)} characters; user {len(user)} characters; schema {len(json.dumps(schema))} characters',
              f'evidence items {len(evidence_ids)}; themes {len(theme_ids)}',
              f'source passages the answer cites that the rendered request does not show: {missing or "none"}',
              f'schema errors: {schema_errors or "none"}', f'calc_check errors: {result["errors"] or "none"}',
              f'recorded: {json.dumps(result["recorded"])}']
    print('\n'.join(report))
    family_sb = {'members': {}, 'relations': [{'type': 'same_base', 'later': 'v35', 'earlier': 'v14'}],
                 'shared': [{'population': 'NVIDIA', 'measure': 'revenue', 'scope': 'company', 'period': 'FY2027'}]}
    user_sb, _, _ = render(archive, [('v14', 8729), ('v35', 8732)], family_sb)
    line = next(l for l in user_sb.split('\n') if l.startswith('Relations:'))
    report.append(f'same-base family (calls 8729, 8732): {line}')
    print(report[-1])
    if "v35 rests on v14's base" not in line:
        return 1
    if len(sys.argv) > 1:
        prefix = Path(sys.argv[1])
        prefix.with_suffix('.request.json').write_text(json.dumps({'system': system, 'user': user, 'schema': schema}, indent=1))
        prefix.with_suffix('.answer.json').write_text(json.dumps(answer, indent=1))
        prefix.with_suffix('.txt').write_text('\n'.join(report) + '\n')
    return 0 if not schema_errors and not result['errors'] and not missing else 1


if __name__ == '__main__':
    raise SystemExit(main())
