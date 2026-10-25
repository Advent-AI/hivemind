"""Offline probe of the Jev evidence criterion `supersedes` (log row 47). Takes the archived Jev evidence calls of a ledger whose
decision was a replacement, plus a sample of calls that decided repeat or new, and re-sends each request twice: once unchanged
(the fresh control) and once with the `supersedes` description replaced by the full 06-views definition (rows Replace, 197, 306:
a later version of the same statement or number). Three samples per arm. Prints, per call, the outcome under the decision rule
of `views.jev_matching.decide` (repeat if a same_statement >= 0.5, else replace if a supersedes >= 0.5, else new) for the stored
answer, the control and the arm. Never touches the ledger or its archive; writes its own JSON record.

Usage: python3 scripts/supersedes_probe.py --ledger poc/data/english-v23-jev-2026-10-25 --out poc/reports/2026-10-25-supersedes-probe \
           [--controls 57] [--samples 3] [--cap-usd 0.15]
"""
import argparse, json, pathlib, random, sqlite3, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from hivemind import jev, model  # noqa: E402
from hivemind.views import jev_matching  # noqa: E402

PRICE = model.PRICES['jev-1.14.0'][0]
WORDINGS = {
    'v1': ("a later version of the same statement or number, changed: the same speaker revises that guidance, forecast or "
           "event-progress statement, an official confirms or denies that reported claim, or the original source revises that "
           "statement; another statement on the same topic is not this"),
    'v2': ("a later version of the same statement or number, changed: the same party revises that guidance, forecast or "
           "event-progress statement (a company and its executives are one party), an official confirms or denies that reported "
           "claim, or the original source revises that statement; another statement on the same topic is not this"),
}


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def outcomes(answers):
    """view -> (outcome, target) by the decision rule of jev_matching.decide."""
    by_view = {}
    for qid, a in answers.items():
        if not qid.startswith('piece__'):
            continue
        _, view, stored = qid.split('__')
        by_view.setdefault(view, []).append((a, stored))
    out = {}
    for view, scored in by_view.items():
        repeats = sorted(((a['probabilities']['same_statement'], x) for a, x in scored if a['choice'] == 'same_statement' and a['probabilities']['same_statement'] >= jev_matching.THRESHOLD), reverse=True)
        replaces = sorted(((a['probabilities']['supersedes'], x) for a, x in scored if a['choice'] == 'supersedes' and a['probabilities']['supersedes'] >= jev_matching.THRESHOLD), reverse=True)
        out[view] = ('repeat', repeats[0][1]) if repeats else ('replace', replaces[0][1]) if replaces else ('new', '')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ledger', required=True); ap.add_argument('--out', required=True)
    ap.add_argument('--controls', type=int, default=57); ap.add_argument('--samples', type=int, default=3)
    ap.add_argument('--cap-usd', type=float, default=0.15); ap.add_argument('--archive-name', default='archive.week.sqlite')
    ap.add_argument('--wording', default='v1', choices=sorted(WORDINGS))
    ap.add_argument('--after-call', type=int, default=0, help='only calls with a later call_id (an out-of-sample window)')
    ap.add_argument('--tag', default='', help='suffix of the output file')
    args = ap.parse_args()
    archive = ro(ROOT / args.ledger / args.archive_name)
    calls = []
    for r in archive.execute("select call_id, request_json, response_json from model_calls where model='jev-1.14.0' and purpose='match' and call_id > ? order by call_id", (args.after_call,)):
        request = json.loads(r['request_json'])
        if not any(q.startswith('piece__') for q in request['questions']):
            continue
        answers = json.loads(r['response_json'] or '{}').get('answers') or {}
        calls.append({'call_id': r['call_id'], 'request': request, 'stored': outcomes(answers)})
    replace_calls = [c for c in calls if any(o == 'replace' for o, _ in c['stored'].values())]
    others = [c for c in calls if c not in replace_calls]
    random.seed(20261025)
    sample = replace_calls + random.sample(others, min(args.controls, len(others)))
    spent, records = 0.0, []
    for c in sample:
        arm_request = json.loads(json.dumps(c['request']))
        for q in arm_request['questions'].values():
            if 'supersedes' in q.get('criteria', {}):
                q['criteria']['supersedes'] = WORDINGS[args.wording]
        rec = {'call_id': c['call_id'], 'state': c['request']['state'][:400], 'stored': c['stored'], 'control': [], 'arm': []}
        for _ in range(args.samples):
            for label, request in (('control', c['request']), ('arm', arm_request)):
                response = jev.transport(request)
                tokens = (response.get('usage') or {}).get('input_tokens') or 0
                spent += tokens / 1e6 * PRICE
                problems = jev.validate(response.get('answers'), request['questions'])
                rec[label].append({'outcomes': outcomes(response['answers']) if not problems else None, 'problems': problems,
                                   'answers': response.get('answers')})
        records.append(rec)
        if spent > args.cap_usd:
            print(f'cap reached at ${spent:.4f}')
            break
    out = ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / f'probe-{args.wording}{args.tag}.json').write_text(json.dumps({'wording': args.wording, 'new_supersedes': WORDINGS[args.wording], 'spent_usd': round(spent, 4), 'records': records}, indent=1, ensure_ascii=False))
    flips = {'replace→other (arm, all samples)': 0, 'replace kept (arm)': 0, 'control differs from stored': 0, 'other→replace (arm)': 0, 'repeat/new changed (arm)': 0}
    for rec in records:
        for view, (stored_outcome, _) in rec['stored'].items():
            arm = [s['outcomes'][view][0] for s in rec['arm'] if s['outcomes']]
            control = [s['outcomes'][view][0] for s in rec['control'] if s['outcomes']]
            if any(o != stored_outcome for o in control):
                flips['control differs from stored'] += 1
            if stored_outcome == 'replace':
                flips['replace→other (arm, all samples)' if arm and all(o != 'replace' for o in arm) else 'replace kept (arm)'] += 1
            else:
                if any(o == 'replace' for o in arm):
                    flips['other→replace (arm)'] += 1
                elif any(o != stored_outcome for o in arm):
                    flips['repeat/new changed (arm)'] += 1
    print(json.dumps({'calls': len(records), 'replace calls': len(replace_calls), 'spent_usd': round(spent, 4), **flips}, indent=1))


if __name__ == '__main__':
    main()
