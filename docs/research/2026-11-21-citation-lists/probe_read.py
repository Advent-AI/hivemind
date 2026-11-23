"""Reading packets and the one verdict of the paid acceptance probe (PROBE-DESIGN.md v5 §3, §4; D716).

  python3 probe_read.py packets <probe out folder>              # Part B and Part C packets for the hand reading (and a blind copy)
  python3 probe_read.py verdict <probe out folder> <readings>   # the ordered verdict from the answers and the final readings

Readings file (JSON): {"B": {"<key>|<draw>|<target>": {"class": ..., "valid_support": bool}}, "C": {"<key>": {"read": true,
"harms": [{"kind": "a|b|c|d", "status": "confirmed|unresolved"}]}}}. A Part B target id is the bad id for an evidence target and
"placement" for a placement target. Classes: intended, unsupported, misattributed, omitted (evidence); correct, absent, misattributed
(placement); ambiguous (either, counts neither way).
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / 'src'))
from hivemind import model                                              # noqa: E402
from hivemind.views import judging                                     # noqa: E402

HERE = Path(__file__).resolve().parent
PLAN, TARGETS, STORED_V7 = HERE / 'probe-plan.json', HERE / 'probe-targets.json', HERE / 'stored-v7-support.json'
MISATTRIBUTION_TOLERANCE = 2
CLASSES = {'intended', 'unsupported', 'misattributed', 'omitted', 'correct', 'absent', 'ambiguous'}


def load_answers(out):
    lines = [json.loads(line) for line in (Path(out) / 'answers.jsonl').read_text().splitlines() if line.strip()] if (Path(out) / 'answers.jsonl').exists() else []
    return {(l['part'], l['key'], l['form'], l['draw']): l for l in lines}


def target_ids(target):
    return target['bad'] if target['kind'] == 'evidence' else 'placement'


BLOCK_HEADERS = ('[Evidence in view under this thesis', '[Not shown:', '[Current conclusions of the theses it depends on]', '[Themes in force',
                 '[Previous conclusion', 'Answer per the JSON schema')


def entries(user):
    """Every listed entry a cited or pushed id can name, with its full text: evidence (`- eN [`), dependency and theme (`- vN (`) entries.
    An entry runs from its own start line to the next entry start or the next block header, whatever its lines look like (a quote may
    hold unindented lines or a line beginning with "[")."""
    starts = [(m.start(), m.group(1)) for m in re.finditer(r'^- ([ev]\d+) [\[(]', user, re.M)]
    stops = sorted([s for s, _ in starts] + [m.start() for h in BLOCK_HEADERS for m in re.finditer('^' + re.escape(h), user, re.M)] + [len(user)])
    found = {}
    for start, entry_id in starts:
        end = next(s for s in stops if s > start)
        found.setdefault(entry_id, user[start:end].rstrip('\n'))
    return found


def readable(data):
    """Content a reader can read: every field of the judge's answer, of the right type (the open v7 format's shape)."""
    return isinstance(data, dict) and not model.check_schema(data, judging.schema_for('judging-v7'))


def received(line):
    """An answer that can be read: answered, or refused by the format, with readable content either way."""
    return bool(line) and line['status'] in ('answered', 'format invalid') and readable(line.get('data'))


EVIDENCE_CLASSES = {'intended': {True}, 'unsupported': {False}, 'omitted': {False}, 'misattributed': {True, False}}
PLACEMENT_CLASSES = {'correct': {False}, 'absent': {False}, 'misattributed': {False}}
AMBIGUOUS = {'ambiguous': {False}}                                    # only for a target frozen as ambiguous; it never counts as support


def validate(readings, answers, plan, targets):
    """Refuses a readings file with a value outside the frozen sets, a reading of no planned or no readable answer, a class whose
    valid_support contradicts it (omitted or unsupported with support, intended without; a placement target has no support), or a Part C
    reading of a comparison that is not complete, or harms on a comparison not read."""
    kinds = {f'{r["key"]}|{d}|{target_ids(t)}': t for r in targets['requests'] for t in r['targets'] for d in (1, 2, 3)}
    for name, r in readings.get('B', {}).items():
        if name not in kinds:
            raise ValueError(f'Part B reading {name}: not a planned target')
        key, draw, _ = name.split('|')
        if not received(answers.get(('B', key, 'v12', int(draw)))):
            raise ValueError(f'Part B reading {name}: its answer is missing or unreadable')
        target = kinds[name]
        allowed = AMBIGUOUS if target.get('ambiguous') else (EVIDENCE_CLASSES if target['kind'] == 'evidence' else PLACEMENT_CLASSES)   # a frozen
        # ambiguous target is read as ambiguous and counts neither way; no other target may be called ambiguous
        if r.get('class') not in allowed or not isinstance(r.get('valid_support'), bool) or r['valid_support'] not in allowed[r['class']]:
            raise ValueError(f'Part B reading {name}: class {r.get("class")!r} with valid_support {r.get("valid_support")!r} is not allowed')
    matched = {f'{i["source"]}:{i["call_id"]}' for i in plan['matched']}
    for name, r in readings.get('C', {}).items():
        if name not in matched:
            raise ValueError(f'Part C reading {name}: not a planned comparison')
        if not isinstance(r.get('read'), bool) or any(h.get('kind') not in ('a', 'b', 'c', 'd') or h.get('status') not in ('confirmed', 'unresolved')
                                                     for h in r.get('harms', [])):
            raise ValueError(f'Part C reading {name} is malformed')
        if r.get('harms') and not r['read']:
            raise ValueError(f'Part C reading {name}: harms on a comparison not read')
        if not all(received(answers.get(('C', name, form, d))) for form in ('v12', 'v7') for d in (1, 2, 3)):
            raise ValueError(f'Part C reading {name}: the comparison is not complete')


def verdict(answers, readings, plan, targets, stored_v7, summary):
    """PROBE-DESIGN.md v5 §3: the first rule that applies."""
    validate(readings, answers, plan, targets)
    keys = lambda items: [f'{i["source"]}:{i["call_id"]}' for i in items]
    a1, a0 = keys(plan['acceptance'][:2])
    reasons = []
    for part, key in (('A1', a1), ('A0', a0)):
        line = answers.get((part, key, 'v12', 1))
        if line and (line['status'] == 'format invalid' or (line['status'] == 'transport error' and line.get('http_status') == 400)):
            return 'not ready (format)', [f'{part} rejected: {line.get("error", "")[:200]}']
    v12 = [l for l in answers.values() if l['form'] == 'v12' and l['part'] != 'A2']
    refused = [l for l in v12 if l['status'] == 'format invalid' or (l['status'] == 'answered' and l['check'])]
    if refused:
        reasons.append(f'{len(refused)} v12 answers refused')
    b_reads = readings.get('B', {})
    misattributed = {k.rsplit('|', 1)[0] for k, r in b_reads.items() if r['class'] == 'misattributed'}
    if len(misattributed) > MISATTRIBUTION_TOLERANCE:
        reasons.append(f'{len(misattributed)} Part B answers with a confirmed misattribution (tolerance {MISATTRIBUTION_TOLERANCE})')
    losses, unresolved = [], []
    for request in targets['requests']:
        for target in request['targets']:
            if target['kind'] != 'evidence' or not target.get('material'):
                continue
            draws = [b_reads.get(f'{request["key"]}|{d}|{target["bad"]}') for d in (1, 2, 3)]
            all_received = all(received(answers.get(('B', request['key'], 'v12', d))) for d in (1, 2, 3))
            if not all_received or any(r is None for r in draws):
                continue                                                   # a loss needs all three draws received and read
            if not any(r['valid_support'] for r in draws):
                (losses if stored_v7['targets'].get(request['key'], {}).get('supported') else unresolved).append(f'{request["key"]} {target["bad"]}')
    if losses:
        reasons.append('confirmed material loss in Part B: ' + ', '.join(losses))
    c_reads = readings.get('C', {})
    harms = [f'{k} ({h["kind"]})' for k, r in c_reads.items() for h in r.get('harms', []) if h['status'] == 'confirmed']
    if harms:
        reasons.append('confirmed material harm in Part C: ' + ', '.join(harms))
    if reasons:
        return 'not ready', reasons
    incomplete = []
    core = summary.get('core ledger', summary.get('ledger', {}))        # the ledger as the core run left it; A2 never changes the verdict
    if core.get('stopped'):
        incomplete.append(f'the ledger stopped: {core.get("stop_reason")}')
    for part, key in (('A1', a1), ('A0', a0)):
        line = answers.get((part, key, 'v12', 1))
        if not line or line['status'] != 'answered':
            incomplete.append(f'{part} has no result')
    for key in keys(plan['refused']):
        for d in (1, 2, 3):
            line = answers.get(('B', key, 'v12', d))
            if not received(line):
                incomplete.append(f'Part B {key} draw {d} missing or unreadable')
            for request in targets['requests']:
                if request['key'] == key:
                    for target in request['targets']:
                        if f'{key}|{d}|{target_ids(target)}' not in b_reads:
                            incomplete.append(f'Part B {key} draw {d} {target_ids(target)} not read')
    for key in keys(plan['matched']):
        complete = all(received(answers.get(('C', key, form, d))) for form in ('v12', 'v7') for d in (1, 2, 3))
        if not complete:
            incomplete.append(f'Part C {key} incomplete')
        elif not c_reads.get(key, {}).get('read'):
            incomplete.append(f'Part C {key} not read')
    if incomplete:
        return 'inconclusive (incomplete)', incomplete
    unresolved += [f'{k} ({h["kind"]})' for k, r in c_reads.items() for h in r.get('harms', []) if h['status'] == 'unresolved']
    if unresolved:
        return 'inconclusive (unresolved)', unresolved
    return 'pass', [f'{len(misattributed)} Part B answers with a confirmed misattribution']


def packets(out):
    out = Path(out)
    plan, targets, answers = json.loads(PLAN.read_text()), json.loads(TARGETS.read_text()), load_answers(out)
    by_key = {f'{i["source"]}:{i["call_id"]}': i for i in plan['refused'] + plan['matched']}
    show = lambda l: None if not l or not readable(l.get('data')) else {k: l['data'].get(k) for k in ('rung', 'reference', 'implied_outcome', 'reasons', 'cites', 'cites_views', 'pushes', 'theme_pushes', 'changed', 'why_changed')}
    b, blind = [], []
    for request in targets['requests']:
        item, listed = by_key[request['key']], entries(by_key[request['key']]['user'])
        for d in (1, 2, 3):
            line = answers.get(('B', request['key'], 'v12', d))
            text = json.dumps(show(line) or {}, ensure_ascii=False)
            for target in request['targets']:
                flags = [m for m in target.get('markers', []) if m.lower() not in text.lower()]
                data = (line or {}).get('data') if readable((line or {}).get('data')) else {}
                used = set(data.get('cites') or []) | set(data.get('cites_views') or []) | {x['evidence_id'] for x in data.get('pushes') or []} | {x['view_id'] for x in data.get('theme_pushes') or []}
                quotes = {e: listed.get(e, '(not listed)') for e in sorted(used | set(target.get('sources', []) + target.get('partial', []) + target.get('near_misses', [])))}
                entry = {'id': f'{request["key"]}|{d}|{target_ids(target)}', 'status': line['status'] if line else 'missing', 'answer': show(line),
                         'target': target, 'quotes': quotes, 'markers not found': flags, 'question': item['user'].split('\n', 1)[0]}
                b.append(entry)
                blind.append(entry)
    c = []
    for item in plan['matched']:
        key, listed = f'{item["source"]}:{item["call_id"]}', entries(item['user'])
        arms = {form: [show(answers.get(('C', key, form, d))) for d in (1, 2, 3)] for form in ('v12', 'v7')}
        cited = lambda a: (set((a or {}).get('cites') or []) | {p['evidence_id'] for p in (a or {}).get('pushes') or []}
                           | set((a or {}).get('cites_views') or []) | {p['view_id'] for p in (a or {}).get('theme_pushes') or []})
        counts = {form: {} for form in arms}
        for form, answers_ in arms.items():
            for a in answers_:
                for e in cited(a):
                    counts[form][e] = counts[form].get(e, 0) + 1
        differing = sorted(e for e in set(counts['v12']) | set(counts['v7']) if (counts['v12'].get(e, 0) >= 2) != (counts['v7'].get(e, 0) >= 2))
        everything = sorted(set(counts['v12']) | set(counts['v7']))
        c.append({'key': key, 'question': item['user'].split('\n', 1)[0], 'stored answer': json.loads(item['stored answer']) if item.get('stored answer') else None,
                  'v12': arms['v12'], 'v7': arms['v7'], 'rungs': {f: [a and a['rung'] for a in arms[f]] for f in arms},
                  'differing sources (>=2 of 3 in one arm only)': differing, 'quotes': {e: listed.get(e, '(not listed)') for e in everything}})
    (out / 'packet-B.json').write_text(json.dumps(b, ensure_ascii=False, indent=1))
    (out / 'packet-C.json').write_text(json.dumps(c, ensure_ascii=False, indent=1))
    print(f'Part B: {len(b)} target readings; Part C: {len(c)} comparisons')


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == 'packets':
        packets(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == 'verdict':
        out = Path(sys.argv[2])
        summary = json.loads((out / 'run-summary.json').read_text()) if (out / 'run-summary.json').exists() else {}
        result = verdict(load_answers(out), json.loads(Path(sys.argv[3]).read_text()), json.loads(PLAN.read_text()), json.loads(TARGETS.read_text()),
                         json.loads(STORED_V7.read_text()), summary)
        print(json.dumps({'verdict': result[0], 'reasons': result[1]}, indent=1))
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()
