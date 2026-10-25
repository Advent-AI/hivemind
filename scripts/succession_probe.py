"""Offline probe of a sixth relation option for the Jev candidate question (log row 48): 'the same defined quantity or event series
for another period'. Today the options cannot express a succession between two theses whose scopes are model-written in
different words (the code decides succession only for equal scopes): for a next-year figure Jev answers 'one matter, two
quantities', and the engine opens a new thesis. For every Jev candidate call of a ledger in which some listed thesis has the same
object and measure, the archived request is re-sent unchanged (fresh control) and with the option added (arm), three samples each.
Outcomes follow the engine: a same-quantity answer merges (key rules as in `jev_matching.decide`); in the arm, an other-period
answer on a thesis whose period ends before the candidate's begins, with no conflicting typed field and no successor at the time,
is a succession; then the code's succession rule (scopes equal, `identity.conflicts` for typed fields); else new. Scored against
the golds by majority. Never touches the ledger or its archive; writes its own JSON record.

Usage: python3 scripts/succession_probe.py --ledger poc/data/english-v23-jev-2026-10-25 --label v23-jev \
           --gold poc/eval/gold/week-benchmark-v23-2026-10-25.json --gold poc/eval/gold/august-benchmark-v23-2026-10-25.json \
           --out poc/reports/2026-10-25-succession-probe [--samples 3] [--cap-usd 0.40]
"""
import argparse, collections, json, pathlib, sqlite3, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import jev, model  # noqa: E402
from hivemind import universe as _universe  # noqa: E402
from hivemind.views import identity, jev_matching  # noqa: E402

PRICE = model.PRICES['jev-1.14.0'][0]
OTHER_PERIOD = ('same_quantity_other_period', 'the same defined quantity or event series for another period, such as the next fiscal or calendar year')


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def later(key, c):
    return bool(key.get('period_end') and c.get('period_start') and key['period_end'] < c['period_start'])


def outcome(answers, c, keys, objects, open_at, has_successor, arm):
    rel = {q[5:]: a for q, a in answers.items() if q.startswith('rel__')}
    same = sorted(((a['probabilities']['same_quantity_or_event'], v) for v, a in rel.items()
                   if a['choice'] == 'same_quantity_or_event' and a['probabilities']['same_quantity_or_event'] >= jev_matching.THRESHOLD), reverse=True)
    for _, v in same:
        key = keys.get(v)
        if key and identity.conflicts(key, c, merging=False):
            continue
        if key and identity.conflicts(key, c, merging=True):
            if later(key, c) and not has_successor(v):
                return 'succession', v
            continue
        if open_at(v):
            return 'merge', v
    if arm:
        other = sorted(((a['probabilities'].get(OTHER_PERIOD[0], 0), v) for v, a in rel.items()
                        if a['choice'] == OTHER_PERIOD[0] and a['probabilities'][OTHER_PERIOD[0]] >= jev_matching.THRESHOLD), reverse=True)
        for _, v in other:
            key = keys.get(v)
            if key and objects.get(v) == c['object'] and not identity.conflicts(key, c, merging=False) and later(key, c) and not has_successor(v):
                return 'succession', v
    for v in rel:                                            # the code's rule, with the shared typed-field check (fix of row 48)
        key = keys.get(v)
        if not key or objects.get(v) != c['object'] or identity.conflicts(key, c, merging=False):
            continue
        if _universe.scope_key(key.get('scope', '')) == _universe.scope_key(c.get('scope', '')) and later(key, c) and not has_successor(v):
            return 'succession', v
    return 'new', ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True); ap.add_argument('--label', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--gold', action='append', required=True); ap.add_argument('--samples', type=int, default=3)
    ap.add_argument('--cap-usd', type=float, default=0.40)
    args = ap.parse_args()
    conn = ro(ROOT / args.ledger / 'views.sqlite')
    archive = ro(ROOT / args.ledger / 'archive.sqlite')
    golds = {}
    for g in args.gold:
        golds.update({k: v for k, v in json.loads((ROOT / g).read_text())['candidates'].get(args.label, {}).items() if not k.startswith('_')})
    keys = {r['view_id']: dict(r) for r in conn.execute('select * from view_keys')}
    objects = {r['view_id']: r['object_id'] for r in conn.execute('select view_id, object_id from views')}
    looks = {r['view_id']: r['looks_at'] for r in conn.execute('select view_id, looks_at from views')}
    succ_seq = {r['succeeds']: r['seq'] for r in conn.execute('select succeeds, seq from successions')}
    by_state = {}
    for r in archive.execute("select call_id, request_json, response_json from model_calls where model='jev-1.14.0' and purpose='match'"):
        request = json.loads(r['request_json'])
        if any(q.startswith('rel__') for q in request['questions']):
            by_state[request['state']] = (r['call_id'], request, json.loads(r['response_json'] or '{}').get('answers') or {})
    last = {}
    for r in conn.execute('select input_id, call_no, seq from match_records where call_no in (1,2) order by id'):
        last[r['input_id']] = r['seq']
    work = []
    for inp, seq in last.items():
        handover = json.loads(conn.execute('select handover_json from handovers where input_id=?', (inp,)).fetchone()['handover_json'])
        for c in handover['candidates']:
            found = by_state.get(jev_matching.candidate_state(c, handover['evidence']))
            if not found:
                continue
            listed = [q[5:] for q in found[1]['questions'] if q.startswith('rel__')]
            if any(objects.get(v) == c['object'] and keys.get(v, {}).get('measure') == c.get('measure') for v in listed):
                work.append((f"{inp}|{c['id']}", seq, c, found))
    spent, records = 0.0, []
    for key_id, seq, c, (call_id, request, stored) in work:
        open_at = lambda v, seq=seq: keys.get(v, {}).get('seq', 10 ** 9) < seq
        has_successor = lambda v, seq=seq: succ_seq.get(v, 10 ** 9) < seq
        arm_request = json.loads(json.dumps(request))
        for q, body in arm_request['questions'].items():
            if q.startswith('rel__'):
                body['criteria'] = dict(body['criteria'], **{OTHER_PERIOD[0]: OTHER_PERIOD[1]})
        rec = {'key': key_id, 'call_id': call_id, 'gold': golds.get(key_id), 'stored': outcome(stored, c, keys, objects, open_at, has_successor, False), 'control': [], 'arm': []}
        for _ in range(args.samples):
            for label, req, arm in (('control', request, False), ('arm', arm_request, True)):
                response = jev.transport(req)
                spent += ((response.get('usage') or {}).get('input_tokens') or 0) / 1e6 * PRICE
                problems = jev.validate(response.get('answers'), req['questions'])
                rec[label].append(None if problems else outcome(response['answers'], c, keys, objects, open_at, has_successor, arm))
        records.append(rec)
        if spent > args.cap_usd:
            print(f'cap reached at ${spent:.4f}')
            break
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / f'probe-{args.label}.json').write_text(json.dumps({'option': OTHER_PERIOD, 'spent_usd': round(spent, 4), 'records': records}, indent=1, ensure_ascii=False))

    def majority(samples):
        got = [tuple(s) for s in samples if s]
        return collections.Counter(got).most_common(1)[0][0] if got else ('error', '')

    def right(g, o):
        if g is None:
            return None
        if g['gold'] == 'either':
            return None
        if o[0] != g['gold']:
            return False
        return g['gold'] == 'new' or g.get('target_text', '') in looks.get(o[1], '')
    score = {'control': collections.Counter(), 'arm': collections.Counter()}
    for rec in records:
        for label in ('control', 'arm'):
            o = majority(rec[label])
            verdict = right(rec['gold'], o)
            if verdict is not None:
                score[label][('right' if verdict else 'wrong', rec['gold']['gold'])] += 1
        c_o, a_o = majority(rec['control']), majority(rec['arm'])
        mark = '' if rec['gold'] is None else f" gold {rec['gold']['gold']}"
        if c_o != a_o or (rec['gold'] and rec['gold']['gold'] == 'succession'):
            print(f"{rec['key'][-46:]}{mark}: stored {rec['stored'][0]} | control {c_o[0]} {c_o[1]} | arm {a_o[0]} {a_o[1]} | arm samples {[s[0] if s else 'err' for s in rec['arm']]}")
    print(json.dumps({'candidates probed': len(records), 'spent_usd': round(spent, 4),
                      'control': {f'{k[0]} {k[1]}': v for k, v in sorted(score['control'].items())},
                      'arm': {f'{k[0]} {k[1]}': v for k, v in sorted(score['arm'].items())}}, indent=1))


if __name__ == '__main__':
    main()
