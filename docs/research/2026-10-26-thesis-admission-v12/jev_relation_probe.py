#!/usr/bin/env python3
"""Offline probe of the Jev candidate-relation criteria (D189 mechanism 1): re-send stored candidate calls whose list holds a thesis
of the same object and measure, unchanged (control) and with the analyst's criteria (arm), three samples each, and compare the
engine's outcome under each. Never touches a ledger or its archive; writes its own JSON and Markdown.

  --list   print the candidate pairs and stop ($0)
  --run    send the samples (Jev, about $0.0001 per call)

  python3 docs/research/2026-10-26-thesis-admission-v12/jev_relation_probe.py --ledger /abs/path/to/run --out /abs/path/out [--list|--run] [--samples 3] [--cap-usd 0.5] [--labels labels.json]
"""
import argparse
import collections
import json
import pathlib
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import jev, model  # noqa: E402
from hivemind.views import identity, jev_matching  # noqa: E402

PRICE = model.PRICES['jev-1.14.0'][0]
# The analyst's criteria: one question is one decision; a component with its own drivers is a distinct question; "part of" is not an answer
ANALYST = {
    'same_question': "one question: the same outcome settles both and an investor needs no separate answer; alternative wordings, another estimate or source, or another population or proxy of one aggregate (five companies named, the top five, the largest four) are the same question",
    'same_quantity_other_period': "the same defined quantity or event series for another period, such as the next fiscal or calendar year",
    'distinct_question_same_matter': "one matter, but the answers can move apart and an investor would want each: a component with its own drivers or its own settling figure (a region's revenue within a segment), a different quantity in the same deal (a guarantee beside a financing), a different event",
    'different': "different matters; sharing a company, industry or word is not enough",
    'cannot_tell': "the supplied material is insufficient or inconsistent"}
ANALYST_INSTRUCTION = ('What relationship holds between the CANDIDATE and the THESIS below? Ask what a senior analyst would hold: one question or two. '
                       'Use only the supplied text. Equal numbers and similar wording do not establish identity; a different population or estimate of one aggregate does not make two questions. THESIS:\n')
SAME = {'control': 'same_quantity_or_event', 'arm': 'same_question'}
OTHER = 'same_quantity_other_period'


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def outcome(answers, c, keys, open_at, same_key):
    """The engine's mapping (jev_matching.decide) with the given name of the 'same' option: merge into an open thesis unless the typed
    fields conflict; a period conflict or the other-period option is a succession; else new."""
    rel = {q[5:]: a for q, a in answers.items() if q.startswith('rel__')}
    same = sorted(((a['probabilities'].get(same_key, 0), v) for v, a in rel.items() if a['choice'] == same_key and a['probabilities'].get(same_key, 0) >= jev_matching.THRESHOLD), reverse=True)
    for _, v in same:
        key = keys.get(v)
        if key and identity.conflicts(key, c, merging=False):
            continue
        if key and identity.conflicts(key, c, merging=True):
            return 'succession', v
        if open_at(v):
            return 'merge', v
    other = sorted(((a['probabilities'].get(OTHER, 0), v) for v, a in rel.items() if a['choice'] == OTHER and a['probabilities'].get(OTHER, 0) >= jev_matching.THRESHOLD), reverse=True)
    for _, v in other:
        key = keys.get(v)
        if key and not identity.conflicts(key, c, merging=False):
            return 'succession', v
    return 'new', ''


def top(answers, v):
    a = answers.get(f'rel__{v}')
    if not a:
        return ''
    best = max(a['probabilities'].items(), key=lambda kv: kv[1])
    return f'{best[0]} {best[1]:.2f}'


def collect(conn, archive):
    keys = {r['view_id']: dict(r) for r in conn.execute('select * from view_keys')}
    views = {r['view_id']: dict(r) for r in conn.execute('select view_id, object_id, looks_at, question from views')}
    by_state = {}
    for r in archive.execute("select call_id, request_json, response_json from model_calls where model='jev-1.14.0' and purpose='match' order by call_id"):
        request = json.loads(r['request_json'])
        if any(q.startswith('rel__') for q in request['questions']):
            by_state[request['state']] = (r['call_id'], request, (json.loads(r['response_json'] or '{}').get('answers') or {}))
    work = []
    for h in conn.execute('select input_id, seq, handover_json from handovers order by seq'):
        handover = json.loads(h['handover_json'])
        for c in handover['candidates']:
            found = by_state.get(jev_matching.candidate_state(c, handover['evidence']))
            if not found:
                continue
            listed = [q[5:] for q in found[1]['questions'] if q.startswith('rel__')]
            peers = [v for v in listed if views.get(v, {}).get('object_id') == c['object'] and keys.get(v, {}).get('measure') == c.get('measure')]
            if peers:
                work.append({'key': f"{h['input_id']}|{c['id']}", 'seq': h['seq'], 'candidate': c, 'call_id': found[0], 'request': found[1], 'stored': found[2], 'peers': peers})
    return keys, views, work


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--samples', type=int, default=3)
    ap.add_argument('--cap-usd', type=float, default=0.5)
    ap.add_argument('--labels', default=None, help='JSON {key: {"expect": "merge|new|succession", "target": "vN", "note": "..."}}')
    args = ap.parse_args()
    ledger = pathlib.Path(args.ledger)
    conn, archive = ro(ledger / 'views.sqlite'), ro(ledger / 'archive.sqlite')
    keys, views, work = collect(conn, archive)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    if args.list or not args.run:
        print(f'{len(work)} candidate calls with a same-object, same-measure thesis on the list')
        for w in work:
            c = w['candidate']
            print(f"\n{w['key']}  (call {w['call_id']})\n   CANDIDATE {c['object']} {c.get('measure')} [{c.get('scope', '')}] {c['year']}: {c['question'][:110]}")
            for v in w['peers']:
                print(f"   peer {v} [{keys[v]['scope']}] {views[v]['question'][:100]}  stored: {top(w['stored'], v)}")
        return
    labels = json.loads(pathlib.Path(args.labels).read_text()) if args.labels else {}
    spent, records = 0.0, []
    for w in work:
        c, request = w['candidate'], w['request']
        open_at = lambda v, seq=w['seq']: keys.get(v, {}).get('seq', 10 ** 9) < seq
        arm_request = json.loads(json.dumps(request))
        for q, body in arm_request['questions'].items():
            if q.startswith('rel__'):
                body['criteria'] = dict(ANALYST)
                body['instructions'] = ANALYST_INSTRUCTION + body['instructions'].split('THESIS:\n', 1)[1]
        rec = {'key': w['key'], 'call_id': w['call_id'], 'peers': w['peers'], 'label': labels.get(w['key']),
               'stored': outcome(w['stored'], c, keys, open_at, SAME['control']), 'control': [], 'arm': [], 'arm_top': []}
        for _ in range(args.samples):
            for label, req, same_key in (('control', request, SAME['control']), ('arm', arm_request, SAME['arm'])):
                response = jev.transport(req)
                spent += ((response.get('usage') or {}).get('input_tokens') or 0) / 1e6 * PRICE
                problems = jev.validate(response.get('answers'), req['questions'])
                rec[label].append(None if problems else outcome(response['answers'], c, keys, open_at, same_key))
                if label == 'arm' and not problems:
                    rec['arm_top'].append({v: top(response['answers'], v) for v in w['peers']})
        records.append(rec)
        print(f"{w['key'][-40:]}: stored {rec['stored'][0]} control {[o[0] if o else None for o in rec['control']]} arm {[o[0] if o else None for o in rec['arm']]}")
        if spent > args.cap_usd:
            print(f'cap reached at ${spent:.4f}')
            break
    (out / 'records.json').write_text(json.dumps(records, ensure_ascii=False, indent=1))

    def majority(samples):
        counted = collections.Counter((o[0], o[1]) for o in samples if o)
        return counted.most_common(1)[0][0] if counted else ('none', '')
    lines = [f'# Jev relation criteria probe on `{ledger.name}` ({len(records)} candidates, {args.samples} samples per arm, ${spent:.4f})', '',
             '| candidate | peers | label | stored | control (majority) | arm (majority) | arm top answers |', '|---|---|---|---|---|---|---|']
    agree = collections.Counter()
    for r in records:
        ctrl, arm = majority(r['control']), majority(r['arm'])
        lab = (r['label'] or {}).get('expect', '')
        want = (r['label'] or {}).get('target', '')
        if lab:                                              # outcome must agree; the target too when the label names one
            agree['control'] += ctrl[0] == lab and (not want or ctrl[1] == want)
            agree['arm'] += arm[0] == lab and (not want or arm[1] == want)
            agree['n'] += 1
        tops = '; '.join(f'{v}: {t}' for v, t in (r['arm_top'][0] if r['arm_top'] else {}).items())
        lines.append(f"| {r['key'][-44:]} | {', '.join(r['peers'])} | {lab} {(r['label'] or {}).get('target', '')} | {r['stored'][0]} {r['stored'][1]} | {ctrl[0]} {ctrl[1]} | {arm[0]} {arm[1]} | {tops} |")
    if agree['n']:
        lines += ['', f"Against the labels ({agree['n']}): control right {agree['control']}, arm right {agree['arm']}."]
    (out / 'probe.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines[-3:]))


if __name__ == '__main__':
    main()
