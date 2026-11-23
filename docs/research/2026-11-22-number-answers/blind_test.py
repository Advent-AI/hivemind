"""The v13s blind conformance test (SMALL-DESIGN.md §5 with its [52] changes; D737, D738). $0 at the provider.

  python3 blind_test.py build <out folder>      # the six registered requests, each in its own folder (system.txt, user.txt, schema.json)
  python3 blind_test.py check <out folder>      # every writer's first answer through model.check_schema, from_answer and check
  python3 blind_test.py packets <out folder>    # one reader packet per answer: the whole request text and the answer, checker hidden

Writers put their first answer, unedited, at <out>/<case>/answers/<writer>.json (the writer label never reaches a reader).
"""
import hashlib
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO / 'src'))
import calc_small as cs  # noqa: E402
import paid_gate as pg  # noqa: E402
from hivemind import model  # noqa: E402

W = pg.W
CASES = {   # registered in SMALL-DESIGN.md §5: archive, calls, member keys
    'P': {'draw': 'old-1', 'calls': [('v4', 8810), ('v8', 8816)], 'arm': 'joint'},
    'P-v4': {'draw': 'old-1', 'calls': [('v4', 8810), ('v8', 8816)], 'arm': 'separate', 'member': 'v4'},
    'P-v8': {'draw': 'old-1', 'calls': [('v4', 8810), ('v8', 8816)], 'arm': 'separate', 'member': 'v8'},
    'S': {'draw': 'old-3', 'calls': [('v6', 9043)], 'arm': 'single',
          'what': W('four largest AI hyperscalers', 'data-center capex', 'combined', 'CY2026')},
    'O': {'draw': 'old-2', 'calls': [('v29', 8507)], 'arm': 'single', 'what': W('NVIDIA', 'equity investment commitments', 'company', 'end of FY2027'),
          'note': pg.O_NOTE},
    'E': {'draw': 'old-3', 'calls': [('v41', 9071)], 'arm': 'single', 'what': W('NVIDIA', 'revenue', 'Vera CPU', 'FY2028')},
}
REGISTERED_QUESTIONS = {
    ('old-1', 'v4'): "What will NVIDIA's total revenue be in FY2027?",
    ('old-1', 'v8'): 'How much Data Center segment revenue will NVIDIA report for FY2027?',
    ('old-3', 'v6'): 'How much will the four largest AI hyperscalers spend on data-center capital expenditures in calendar 2026?',
    ('old-2', 'v29'): "How much will NVIDIA's equity investment commitments reach at the publication of its FY2027 annual report?",
    ('old-3', 'v41'): 'What will NVIDIA report as Vera CPU revenue for FY2028?',
}
REGISTERED_EDGES = {('old-1', 'v4'): [431.2, 392.0, 352.8, 313.6], ('old-1', 'v8'): [400.0, 350.0, 300.0, 250.0],
                    ('old-3', 'v6'): [500.0, 600.0, 700.0, 800.0], ('old-2', 'v29'): [25.0, 50.0, 75.0, 100.0],
                    ('old-3', 'v41'): [50.0, 40.0, 30.0, 20.0]}


def heading(draw, call_id):
    a = sqlite3.connect(f'file:{pg.RUN / draw / "prod/archive.sqlite"}?mode=ro', uri=True)
    user = json.loads(a.execute('select request_json from model_calls where call_id=?', (call_id,)).fetchone()[0])['messages'][1]['content']
    m = re.match(r'Thesis (v\d+) \([^)]*\): ([^\n]*)', user)
    return m.group(1), m.group(2)


def edges(bands):
    out = []
    for lo, hi in bands:
        for e in (lo, hi):
            if e is not None and e not in out:
                out.append(e)
    return out


def build_case(name, spec):
    draw = spec['draw']
    for view_id, call_id in spec['calls']:                     # the registered heading, question and ladder, or refuse
        tid, question = heading(draw, call_id)
        if tid != view_id or question != REGISTERED_QUESTIONS[(draw, view_id)]:
            raise SystemExit(f'{name}: call {call_id} heads {tid} "{question}", not the registered {view_id}')
        got = edges(pg.bands(draw, view_id))
        if got != REGISTERED_EDGES[(draw, view_id)]:                   # [54] in rung order, not sorted
            raise SystemExit(f'{name}: {view_id} ladder edges {got}, not the registered {REGISTERED_EDGES[(draw, view_id)]}')
    if spec['arm'] in ('joint', 'separate'):
        (tv, tc), (dv, dc) = spec['calls']
        family = pg.small_family(pg.pair_family(draw, (tv, tc), (dv, dc)), pg.PAIR_SCOPES)
        if spec['arm'] == 'joint':
            return pg.item(f'blind-{name}', 'joint', draw, spec['calls'], family, [tv, dv], 'v13s')
        return pg.item(f'blind-{name}', f'separate-{spec["member"]}', draw, spec['calls'], pg.only(family, spec['member']), [spec['member']], 'v13s')
    view_id, call_id = spec['calls'][0]
    family = {'members': {view_id: {'what': spec['what'], 'bands': pg.bands(draw, view_id)}}, 'relations': [], 'shared': [], 'compare_periods': []}
    family = pg.small_family(family, notes={view_id: spec['note']} if spec.get('note') else None)
    return pg.item(f'blind-{name}', 'single', draw, spec['calls'], family, [view_id], 'v13s')


def build(out):
    if out.exists():
        raise SystemExit(f'{out} exists')
    gate_quotes = {p['text'] for it in json.loads((HERE / 'paid-plan.json').read_text()) for p in it['passages'].values()}
    report = []
    for name, spec in CASES.items():
        it = build_case(name, spec)
        folder = out / name
        (folder / 'answers').mkdir(parents=True)
        (folder / 'system.txt').write_text(it['system'])
        (folder / 'user.txt').write_text(it['user'])
        (folder / 'schema.json').write_text(json.dumps(it['schema'], indent=1, ensure_ascii=False))
        (folder / 'item.json').write_text(json.dumps(it, ensure_ascii=False))
        fresh = sum(1 for p in it['passages'].values() if p['text'] not in gate_quotes)
        report.append(f'{name:5} {it["arm"]:13} members {it["members"]} passages {len(it["passages"])} ({fresh} quotes absent from the gate) '
                      f'request {len(it["system"]) + len(it["user"]) + len(json.dumps(it["schema"]))} chars')
    (out / 'BUILD.txt').write_text('\n'.join(report) + '\n')
    print('\n'.join(report))


WRITERS = ('claude', 'codex')
_FENCE = re.compile(r'^\s*```(?:json)?\s*\n(.*)\n\s*```\s*$', re.S)


def first_json(text):
    """[54] The writer's first output exactly as returned: one JSON object, optionally inside a single ```json fence; anything else
    (a preface, an array, two objects) is not an answer."""
    m = _FENCE.match(text)
    body = m.group(1) if m else text
    data = json.loads(body)
    return data if isinstance(data, dict) else None


def inventory(out):
    """[54] Every registered case has one first answer from each writer."""
    return [f'{name}/{w}' for name in CASES for w in WRITERS if not (out / name / 'answers' / f'{w}.json').exists()]


def check(out):
    missing = inventory(out)
    if missing:
        raise SystemExit(f'INCOMPLETE: no first answer for {", ".join(missing)}')
    rows = []
    for name in CASES:
        it = json.loads((out / name / 'item.json').read_text())
        for w in WRITERS:
            raw = (out / name / 'answers' / f'{w}.json').read_text()
            row = {'case': name, 'writer': w, 'sha256': hashlib.sha256(raw.encode()).hexdigest()}
            try:
                data = first_json(raw)
            except json.JSONDecodeError:
                data = None
            if data is None:
                row.update(stage='not JSON', errors=[['format', 'not one JSON object as returned']])
            else:
                schema_errors = model.check_schema(data, it['schema'])
                if schema_errors:
                    row.update(stage='schema', errors=[['schema', e] for e in schema_errors])
                else:
                    try:
                        calc = cs.from_answer(data, it['family'])
                        result = cs.check(it['family'], it['passages'], calc)
                        row.update(stage='checked', errors=[list(e) for e in result['errors']], recorded=result['recorded'],
                                   published=result['published'], decision=cs.publish_decision(it['family'], calc, result))
                    except Exception as error:                     # [54] recorded per answer, classed apart from the writer's errors
                        row.update(stage='checker error', errors=[['checker', f'{type(error).__name__}: {error}'[:300]]])
            rows.append(row)
    (out / 'CHECKED.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    for r in rows:
        print(f'{r["case"]:5} {r["writer"]:10} {r["stage"]:8} {r.get("decision", "-"):9} ' + '; '.join(f'{c}: {d}' for c, d in r['errors'])[:300])


READER_BRIEF = """# Blind reading (judging-v13s blind test, SMALL-DESIGN.md §5)

You are given one forecasting request (the questions, their ladders, and every passage the writer was shown) and one answer to it,
written in a JSON format. You are not told who wrote the answer or whether any check accepted it. Read only what is given here.

For **every member** the answer forecasts, and for the answer as a whole, return JSON:

{"members": {"<view id>": {"supported": "yes|no", "ground": "<the passage ids or the stated assumption that put the forecast in its band>",
                           "why_not": "<if no: what is missing or wrong>"}},
 "defects": [{"type": "<one of: number misread | wrong arithmetic | part above or added into its whole | two forecasts of one quarter |
               own estimate passed off as the market's reference | broken structure>", "figures": ["<figure ids>"], "detail": "..."}]}

Definitions:
- supported: the forecast follows from the shown passages and the answer's stated assumptions; a reader could check it against them.
- number misread: a source figure's number, scale, sign or qualifier differs from what its passage writes.
- wrong arithmetic: a computed figure does not equal its operation on its inputs.
- part above or added into its whole: a segment is larger than the total it belongs to, or is added again into a total that already
  includes it (directly or through an intermediate figure or an estimate).
- two forecasts of one quarter: two different figures are used as the value of one quantity and period. A growth rate computed from
  guidance and used only as a stated benchmark for an estimate is not a second value, when one figure supplies the quarter in the
  calculation (a ruling). Look through any rate or multiple, including inside a stated assumption, for a second dollar value
  of the quarter.
- own estimate passed off as the market's reference: a figure marked as the market's reference is, or rests on, the writer's own
  estimate or forecast. A reference that applies a past period's reported share or multiple to another period (a quarter's mix
  applied to the year) is our comparison estimate, not the market's (a ruling).
- broken structure: a link that does not resolve, a figure that depends on itself, a missing or doubled answer, an outcome that is not
  the question's quantity, or a rung whose band does not hold the outcome. For a range outcome, the format allows "a band it overlaps,
  with the reason in reasons": such a rung is not broken structure; a band the range does not reach is. A total used for a narrower
  quantity (total capital expenditure for data-center spending) without a stated deduction or a supported bound is an outcome not of the question's quantity
  (a ruling).
Return an empty "defects" list when you find none. Return only JSON.
"""


def packets(out):
    if inventory(out):
        raise SystemExit('INCOMPLETE: packets need every first answer')
    rows = json.loads((out / 'CHECKED.json').read_text())
    if len(rows) != len(CASES) * len(WRITERS):
        raise SystemExit(f'INCOMPLETE: {len(rows)} checked answers, {len(CASES) * len(WRITERS)} registered')
    rng = random.Random(hashlib.sha256((out / 'CHECKED.json').read_bytes()).hexdigest())
    order = list(range(len(rows)))
    rng.shuffle(order)
    key = {}
    folder = out / 'reader-packets'
    folder.mkdir(exist_ok=False)
    for n, i in enumerate(order, 1):
        r = rows[i]
        it = json.loads((out / r['case'] / 'item.json').read_text())
        raw = (out / r['case'] / 'answers' / f'{r["writer"]}.json').read_text()
        pid = f'R{n:02d}'
        key[pid] = {'case': r['case'], 'writer': r['writer']}
        (folder / f'{pid}.md').write_text(READER_BRIEF + '\n# The request as the writer saw it\n\n' + it['user'] + '\n\n# The answer\n\n' + raw + '\n')
    (out / 'reader-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {folder}; key in reader-key.json (keep from readers)')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd in ('build', 'check', 'packets') and len(sys.argv) == 3:
        {'build': build, 'check': check, 'packets': packets}[cmd](Path(sys.argv[2]))
    else:
        raise SystemExit(__doc__)
