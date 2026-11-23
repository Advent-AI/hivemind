"""The D745 targeted $0 test (SMALL-DESIGN.md §5 [D745]): cases S, E and P-v8 built from the current request, a fresh Claude and Codex
writer each, readers with the shared rule text, and three controls built from stored third-run replies (K-unsupported: E with an
unsized 15% cut; K-unresolved-unjustified: P-v8 turned unresolved with a vague reason; K-unresolved-justified: S turned unresolved with
a reason naming the gap). Each control is checked by the code before use.

  python3 blind4.py build <out>      # the three requests and writer prompts
  python3 blind4.py check <out>      # every first answer through the schema, from_answer and check
  python3 blind4.py packets <out>    # reader packets: 6 replies + 3 controls, shuffled; key beside
  python3 blind4.py tally <out>      # the registered pass lines, after the readings (and adjudication where they disagree)
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
from blind_reread2 import READER_BRIEF as _BRIEF2  # noqa: E402
from blind_rules import format_material  # noqa: E402
from hivemind import model  # noqa: E402

CASES = ('S', 'E', 'P-v8')
_STEP2 = '2. For each member, name the evidence for the assumption that puts the forecast in its band, and say whether the passages support it.'
if _BRIEF2.count(_STEP2) != 1:
    raise SystemExit('the second re-read brief no longer holds its step 2')
READER_BRIEF = _BRIEF2.replace('second re-read, D744', 'targeted test, D745').replace(_STEP2, (
    '2. For each member answered as a forecast, name the evidence for the assumption that decides its band, and say whether the\n'
    '   passages support its size or a bound that justifies the rung. For each member answered unresolved, name the gap that remains\n'
    '   after the strongest relevant passages, and say whether the passages indeed cannot settle the rung.'))
BASE = HERE.parents[2] / 'poc/data/judging-v13s-blind3-2026-11-22'
PROMPT = """You are a writer in a blind test of a forecasting request. In the folder {folder} there are three files you may read:
- system.txt: the system message of the request;
- user.txt: the user message of the request;
- schema.json: the JSON schema your answer must satisfy (strict structured output: every property present, null where a field does not apply).
Read those three files and nothing else: no other file in any folder, no web, no tools beyond reading those three files.
Act as the model that receives this request: do the analysis the system and user messages ask for, and return your answer as one JSON object that satisfies schema.json exactly.
Return only the JSON object, with no text before or after it.
"""


def build(out):
    if out.exists():
        raise SystemExit(f'{out} exists')
    for name in CASES:
        it = bt.build_case(name, bt.CASES[name])
        folder = out / name
        (folder / 'answers').mkdir(parents=True)
        (folder / 'system.txt').write_text(it['system'])
        (folder / 'user.txt').write_text(it['user'])
        (folder / 'schema.json').write_text(json.dumps(it['schema'], indent=1, ensure_ascii=False))
        (folder / 'item.json').write_text(json.dumps(it, ensure_ascii=False))
        (folder / 'writer-prompt.txt').write_text(PROMPT.format(folder=folder))
        print(f'{name}: {it["arm"]}, members {it["members"]}, request {len(it["system"]) + len(it["user"])} chars')


def check(out):
    rows = []
    for name in CASES:
        it = json.loads((out / name / 'item.json').read_text())
        for w in bt.WRITERS:
            path = out / name / 'answers' / f'{w}.json'
            if not path.exists():
                raise SystemExit(f'INCOMPLETE: no first answer for {name}/{w}')
            raw = path.read_text()
            row = {'case': name, 'writer': w, 'sha256': hashlib.sha256(raw.encode()).hexdigest()}
            try:
                data = bt.first_json(raw)
            except json.JSONDecodeError:
                data = None
            if data is None:
                row.update(stage='not JSON', errors=[['format', 'not one JSON object as returned']])
            elif model.check_schema(data, it['schema']):
                row.update(stage='schema', errors=[['schema', e] for e in model.check_schema(data, it['schema'])])
            else:
                calc = cs.from_answer(data, it['family'])
                result = cs.check(it['family'], it['passages'], calc)
                row.update(stage='checked', errors=[list(e) for e in result['errors']], recorded=result['recorded'],
                           published=result['published'], decision=cs.publish_decision(it['family'], calc, result),
                           shapes={a['view_id']: a['shape'] for a in data['answers']})
            rows.append(row)
    (out / 'CHECKED.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    for r in rows:
        print(f'{r["case"]:5} {r["writer"]:7} {r["stage"]:8} {r.get("decision", "-"):9} {r.get("shapes")} '
              + '; '.join(f'{c}: {d}' for c, d in r['errors'])[:300])


def _fig(answer, fid):
    return next(f for f in answer['figures'] if f['id'] == fid)


def _unresolved(answer, why):
    a = copy.deepcopy(answer)
    for f in a['figures']:
        f['outcome_for'], f['reference_for'] = [], []
    a['answers'][0].update(shape='unresolved', rung=None, reference_unavailable=None, reasons=why, why=why)
    return a


def controls(out):
    made = {'K-unsupported': ('E', json.loads((BASE / 'E' / 'answers' / 'codex.json').read_text()))}
    made['K-unresolved-unjustified'] = ('P-v8', _unresolved(json.loads((BASE / 'P-v8' / 'answers' / 'claude.json').read_text()),
                                                            'The outlook for the second half is uncertain.'))
    # Built on the third run's S Codex reply: the S Claude reply is refused by the current code (S1, F11 "estimated").
    made['K-unresolved-justified'] = ('S', _unresolved(json.loads((BASE / 'S' / 'answers' / 'codex.json').read_text()), (
        'The question asks for the four companies\' data-center capital expenditure, and the rung turns on whether it reaches $700 billion. '
        'The passages give the four companies\' total capital expenditure (about $720-745 billion, e5014; tracked near $745 billion and '
        '$760 billion, e1856, e2458), AI-infrastructure spending of more than $730 billion (e1947), and data-center capex of nearly $800 '
        'billion for five companies (e5376). None of them gives the four companies\' data-center share: a total, a broader AI category '
        'and a five-company figure do not settle whether the four-company data-center figure is above or below $700 billion, since a '
        'share of about 94% of the total is the dividing line. So the rung cannot be settled from these passages.')))
    for name, (case, answer) in made.items():
        it = json.loads((out / case / 'item.json').read_text())
        if model.check_schema(answer, it['schema']):
            raise SystemExit(f'{name}: schema errors {model.check_schema(answer, it["schema"])[:2]}')
        codes = sorted({c for c, _ in cs.check(it['family'], it['passages'], cs.from_answer(answer, it['family']))['errors']})
        if codes:
            raise SystemExit(f'{name}: the code refuses it ({codes}); a reader control must be accepted by the code')
    return made


def packets(out):
    rows = json.loads((out / 'CHECKED.json').read_text())
    items = [{'case': r['case'], 'writer': r['writer'], 'answer': f'{r["case"]}/answers/{r["writer"]}.json'} for r in rows]
    folder = out / 'controls'
    folder.mkdir(exist_ok=False)
    for name, (case, answer) in controls(out).items():
        (folder / f'{name}.json').write_text(json.dumps(answer, ensure_ascii=False))
        items.append({'case': case, 'writer': name, 'answer': f'controls/{name}.json'})
    order = list(range(len(items)))
    random.Random(hashlib.sha256(b'D745 ' + (out / 'CHECKED.json').read_bytes()).hexdigest()).shuffle(order)
    packets_dir = out / 'reader-packets'
    packets_dir.mkdir(exist_ok=False)
    key = {}
    for n, i in enumerate(order, 1):
        item = items[i]
        it = json.loads((out / item['case'] / 'item.json').read_text())
        pid = f'U{n:02d}'
        key[pid] = item
        (packets_dir / f'{pid}.md').write_text('\n'.join([READER_BRIEF, format_material(out / item['case']), '',
                                                          '# The request as the writer saw it', '', it['user'], '', '# The answer', '',
                                                          (out / item['answer']).read_text(), '']))
    (out / 'reader-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {packets_dir}; key in reader-key.json (keep from readers)')


EXPECTED = {'K-unsupported': 'no', 'K-unresolved-unjustified': 'no', 'K-unresolved-justified': 'yes'}


def _reading(path):
    text = path.read_text()
    return json.loads(text[text.find('{'):text.rfind('}') + 1])


def _defect_key(defect):
    return (defect.get('type'), tuple(sorted(defect.get('figures') or [])))


def tally(out):
    """The registered D745 pass lines, scored as written: support settled by the two readers or, where they split, by both
    adjudicators; a defect settled when both readers mark it or both adjudicators uphold it."""
    key = json.loads((out / 'reader-key.json').read_text())
    checked = {(r['case'], r['writer']): r for r in json.loads((out / 'CHECKED.json').read_text())}
    rows, need, settled_defects, split_defects = {}, [], [], []
    for pid, item in sorted(key.items()):
        first = [_reading(out / 'reader-packets' / f'{pid}.{w}.json') for w in ('codex', 'claude')]
        adjudicated = [out / 'adjudication' / f'{pid}.{w}.json' for w in ('codex', 'claude')]
        adj = [_reading(p) for p in adjudicated] if all(p.exists() for p in adjudicated) else None
        answer = json.loads((out / item['answer']).read_text())
        shapes = {a['view_id']: a['shape'] for a in answer['answers']}
        marks = [{_defect_key(d) for d in r.get('defects', [])} for r in first]
        members = {}
        for view in shapes:
            votes = [r['members'].get(view, {}).get('supported') for r in first]
            if votes[0] == votes[1]:
                members[view] = (votes[0], votes)
            elif adj is None:
                members[view] = ('needs adjudication', votes)
            else:
                second = [a['members'].get(view, {}).get('supported') for a in adj]
                members[view] = (second[0] if second[0] == second[1] else 'split', votes + second)
        both = marks[0] & marks[1]
        either = (marks[0] | marks[1]) - both
        for d in both:
            settled_defects.append([pid, item['case'], item['writer'], d[0], list(d[1]), 'both readers'])
        if either and adj is None:
            need.append(pid)
        elif either:
            decisions = [{_defect_key(d): d.get('decision') for d in a.get('defects', [])} for a in adj]
            for d in sorted(either, key=str):
                pair = [decisions[0].get(d), decisions[1].get(d)]
                row = [pid, item['case'], item['writer'], d[0], list(d[1]), pair]
                if pair == ['uphold', 'uphold']:
                    settled_defects.append(row)
                elif pair != ['reject', 'reject']:       # a split, or a defect an adjudicator did not decide: read by hand
                    split_defects.append(row)
        if any(v[0] == 'needs adjudication' for v in members.values()) and pid not in need:
            need.append(pid)
        rows[pid] = {'case': item['case'], 'writer': item['writer'], 'shapes': shapes, 'members': members}
    if need:
        print('adjudication needed for:', ' '.join(sorted(need)))
        return
    lines, verdict = [], 'pass'
    for pid, r in rows.items():
        for view, (value, votes) in r['members'].items():
            shape = r['shapes'][view]
            if r['writer'] in EXPECTED:
                ok = value == EXPECTED[r['writer']]
                rule = f'control expects {EXPECTED[r["writer"]]}'
            elif r['case'] == 'P-v8':
                ok = shape == 'forecast' and value == 'yes'
                rule = 'a supported forecast'
            else:
                ok = value == 'yes'
                rule = 'a supported forecast or a justified unresolved answer'
            if value == 'split':
                verdict = 'inconclusive' if verdict == 'pass' else verdict
            elif not ok:
                verdict = 'fail'
            lines.append(f'{pid} {r["case"]:5} {r["writer"]:25} {view} {shape:10} settled={value:6} votes={votes} [{rule}] '
                         f'{"ok" if ok else "MISS"}')
    stops = [d for d in settled_defects if d[2] not in EXPECTED]
    refused = [k for k, v in checked.items() if v.get('decision') != 'publish']
    if stops or refused:
        verdict = 'fail'
    result = {'verdict': verdict, 'lines': lines, 'settled_defects': settled_defects, 'split_defects': split_defects,
              'refused': refused}
    (out / 'TALLY.json').write_text(json.dumps(result, indent=1, ensure_ascii=False))
    print('\n'.join(lines))
    print('settled defects:', settled_defects)
    print('split defects (disclosed):', split_defects)
    print('refused first replies:', refused)
    print('VERDICT:', verdict)


_STEP2_D745 = READER_BRIEF[READER_BRIEF.index('2. For each member answered as a forecast'):READER_BRIEF.index('Return JSON:')]
REREAD_BRIEF = READER_BRIEF.replace('targeted test, D745', 're-read under the comparison ruling, D747').replace(_STEP2_D745, (
    '2. For each member answered as a forecast, name the evidence for the assumption that decides its band, and say whether the\n'
    '   passages support its size or a bound that justifies the rung, or, where the passages do not give the asked quantity, whether\n'
    '   the answer explains a related figure as the definitions below require. For each member answered unresolved, name the gap that\n'
    '   remains after the strongest relevant passages, and say whether the passages indeed cannot settle the rung.\n\n'))
if 'D747' not in REREAD_BRIEF or 'An explained related figure satisfies this requirement' not in ' '.join(REREAD_BRIEF.split()):
    raise SystemExit('the D747 re-read brief does not hold the ruling')
BLIND3_REREAD2 = {'T10': ('S', 'claude'), 'T15': ('E', 'claude')}                 # SMALL-DESIGN.md §5 [D747]
REREAD_FROM_BLIND4 = ('U01', 'U02', 'U03', 'U04', 'U05', 'U06', 'U08')
REREAD_EXPECTED = {'blind4 U01': 'no', 'blind4 U02': 'no', 'blind4 U03': 'no', 'blind4 U05': 'no', 'blind3 T15': 'yes'}
REREAD_LABELS = {f'blind4 {p}' for p in REREAD_FROM_BLIND4} | {f'blind3 {p}' for p in BLIND3_REREAD2}
ORIGINAL_BLIND3 = {'K-unsupported': 'E'}      # U03 is the third run's E Codex reply unchanged: it is read under the request it was written for


def _display(path):
    """Every answer shown the same way (parsed and printed with one indent), so a control is not told apart by its layout."""
    return json.dumps(bt.first_json(Path(path).read_text()), indent=1, ensure_ascii=False)


def reread(out):
    """[D747] Nine stored answers re-read under the shared definitions with Alex's comparison ruling: seven from this run and the third
    run's T10 (its spending argument only) and T15 (the bracket both families accepted). Each packet carries the request its answer
    was written for; the constructed controls U01 and U04 are read under the request they were built for."""
    key4 = json.loads((out / 'reader-key.json').read_text())
    key3 = json.loads((BASE / 'reread2-key.json').read_text())
    items = [{'label': f'blind4 {pid}', 'case': key4[pid]['case'], 'writer': key4[pid]['writer'],
              'answer': str(out / key4[pid]['answer']),
              'case_dir': str(BASE / ORIGINAL_BLIND3[key4[pid]['writer']] if key4[pid]['writer'] in ORIGINAL_BLIND3
                              else out / key4[pid]['case'])} for pid in REREAD_FROM_BLIND4]
    for pid, (case, writer) in BLIND3_REREAD2.items():
        if (key3[pid]['case'], key3[pid]['writer']) != (case, writer):
            raise SystemExit(f'{pid} in the second re-read key is {key3[pid]}, not {case}/{writer}')
        items.append({'label': f'blind3 {pid}', 'case': case, 'writer': writer, 'answer': str(BASE / case / 'answers' / f'{writer}.json'),
                      'case_dir': str(BASE / case)})
    order = list(range(len(items)))
    random.Random(hashlib.sha256(b'D747 ' + json.dumps(items, sort_keys=True).encode()).hexdigest()).shuffle(order)
    folder = out / 'reread-packets'
    folder.mkdir(exist_ok=False)
    key = {}
    for n, i in enumerate(order, 1):
        item = items[i]
        case_dir = Path(item['case_dir'])
        pid = f'W{n:02d}'
        key[pid] = item
        (folder / f'{pid}.md').write_text('\n'.join([REREAD_BRIEF, format_material(case_dir), '', '# The request as the writer saw it', '',
                                                     (case_dir / 'user.txt').read_text(), '', '# The answer', '',
                                                     _display(item['answer']), '']))
        (folder / f'{pid}.codex-prompt.txt').write_text(
            f'Read the file {folder / f"{pid}.md"} and nothing else (no other file, no web). Follow the brief at its top: read the request '
            'and the answer it contains, and return only the JSON the brief asks for, with no text before or after it.\n')
    (out / 'reread-key.json').write_text(json.dumps(key, indent=1))
    print(f'{len(order)} packets in {folder}; key in reread-key.json (keep from readers)')


def reread_tally(out):
    """[D747] Registered lines: the five fixed readings as expected; every other answer settled (either way); the reasons behind every
    settled vote recorded by hand as compatible and applying Alex's rule (`reread-reasons.json`), else the vote does not settle; a
    settled defect on a writer's reply is a stop, except T10's marks (its quotation error is already settled, D744)."""
    key = json.loads((out / 'reread-key.json').read_text())
    if {item['label'] for item in key.values()} != REREAD_LABELS or len(key) != len(REREAD_LABELS):
        raise SystemExit(f'the key does not hold exactly the nine registered answers: {sorted(i["label"] for i in key.values())}')
    reasons_path = out / 'reread-reasons.json'
    reasons = json.loads(reasons_path.read_text()) if reasons_path.exists() else {}
    lines, need, verdict, defects = [], [], 'pass', []
    for pid, item in sorted(key.items()):
        first = [_reading(out / 'reread-packets' / f'{pid}.{w}.json') for w in ('codex', 'claude')]
        adjudicated = [out / 'reread-adjudication' / f'{pid}.{w}.json' for w in ('codex', 'claude')]
        adj = [_reading(p) for p in adjudicated] if all(p.exists() for p in adjudicated) else None
        answer = json.loads(Path(item['answer']).read_text())
        marks = [{_defect_key(d) for d in r.get('defects', [])} for r in first]
        either = (marks[0] | marks[1]) - (marks[0] & marks[1])
        for d in marks[0] & marks[1]:
            defects.append([pid, item['label'], d[0], list(d[1]), 'both readers'])
        for a in answer['answers']:
            view = a['view_id']
            votes = [r['members'].get(view, {}).get('supported') for r in first]
            if any(v not in ('yes', 'no') for v in votes):
                raise SystemExit(f'{pid} {view}: a first reading has no valid vote: {votes}')
            record = reasons.get(pid, {})
            first_ok = votes[0] == votes[1] and record.get('first') == 'compatible'
            if first_ok:
                value = votes[0]
            elif votes[0] == votes[1] and 'first' not in record:
                need.append(f'{pid} (reasons not yet recorded)')
                continue
            elif adj is None:
                need.append(pid)
                continue
            else:
                second = [x['members'].get(view, {}).get('supported') for x in adj]
                votes += second
                if second[0] != second[1]:
                    value = 'split'
                elif 'adjudicated' not in record:
                    need.append(f'{pid} (adjudicated reasons not yet recorded)')
                    continue
                else:
                    value = second[0] if record['adjudicated'] == 'compatible' else 'split'
            expected = REREAD_EXPECTED.get(item['label'])
            ok = value == expected if expected else value in ('yes', 'no')
            if not ok:
                verdict = 'fail' if expected and value != 'split' else ('inconclusive' if verdict == 'pass' else verdict)
            lines.append(f'{pid} {item["label"]:11} {item["case"]:5} {item["writer"]:25} {view} {a["shape"]:10} settled={value:6} '
                         f'votes={votes} [{"expects " + expected if expected else "must settle"}] {"ok" if ok else "MISS"}')
        if either and adj is None and pid not in need:
            need.append(pid)
        elif either and adj is not None:
            decisions = [{_defect_key(d): d.get('decision') for d in x.get('defects', [])} for x in adj]
            for d in sorted(either, key=str):
                pair = [decisions[0].get(d), decisions[1].get(d)]
                if pair != ['reject', 'reject']:
                    defects.append([pid, item['label'], d[0], list(d[1]), pair])
    if need:
        print('not final; needed:', ' | '.join(sorted(set(need))))
        return
    stops = [d for d in defects if (d[4] == 'both readers' or d[4] == ['uphold', 'uphold']) and not d[1].startswith('blind3 T10')
             and 'K-' not in key[d[0]]['writer']]
    if stops:
        verdict = 'fail'
    result = {'verdict': verdict, 'lines': lines, 'defects': defects, 'stops': stops}
    (out / 'REREAD-TALLY.json').write_text(json.dumps(result, indent=1, ensure_ascii=False))
    print('\n'.join(lines))
    print('defects (settled or split):', defects)
    print('stops:', stops)
    print('VERDICT:', verdict)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) == 3 else ''
    target = Path(sys.argv[2]).resolve() if len(sys.argv) == 3 else None
    {'build': build, 'check': check, 'packets': packets, 'tally': tally, 'reread': reread, 'reread-tally': reread_tally}.get(
        cmd, lambda _: (_ for _ in ()).throw(SystemExit(__doc__)))(target)
