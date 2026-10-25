"""Score each ledger's evidence decisions (repeat / replace / new, and the target) against the evidence gold, which names
acceptable targets by text because evidence ids differ between ledgers; a row may list `options`, other states it also
accepts (a same-day correction may be a repeat or a replace), and `uncertain` rows are set aside. Read-only.

Usage: python3 scripts/score_evidence_gold.py --gold poc/eval/gold/evidence-decisions-seed-2026-10-25.json \
           --ledger control=poc/data/english-groups4-2026-10-25 --ledger jev=poc/data/english-jev2-2026-10-25
"""
import argparse, collections, json, pathlib, sqlite3

ROOT = pathlib.Path(__file__).resolve().parents[1]


def ro(path):
    conn = sqlite3.connect(f'file:{path}?mode=ro', uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def decisions(conn):
    """(input short name, evidence handover id, view id) -> (outcome, target one-line) from the last first-pass record of each input."""
    out = {}
    for r in conn.execute('select input_id, call_no, decisions_json from match_records order by id'):
        if r['call_no'] not in (1, 2):
            continue
        short = r['input_id'] if r['input_id'].startswith('truenorth:') else r['input_id'].split(':')[-1]
        for x in json.loads(r['decisions_json'] or '{}').get('evidence', []):
            target = x.get('target_evidence_id') or ''
            text = ''
            if target:
                row = conn.execute('select one_line from evidence where evidence_id=?', (target,)).fetchone()
                text = row['one_line'] if row else ''
            out[f"{short}|{x['id']}|{x['view_id']}"] = (x['outcome'], text)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gold', required=True)
    ap.add_argument('--ledger', action='append', required=True, help='label=path, repeatable')
    args = ap.parse_args()
    gold = json.loads((ROOT / args.gold).read_text())['decisions']
    judged = {k: v for k, v in gold.items() if not v.get('uncertain')}
    print(f"gold: {len(gold)} decisions, {len(judged)} judged, {len(gold) - len(judged)} uncertain; by class "
          f"{dict(collections.Counter(v['gold'] for v in judged.values()))}")
    for spec in args.ledger:
        label, path = spec.split('=', 1)
        got = decisions(ro(ROOT / path / 'views.sqlite'))
        right = wrong_kind = wrong_target = missing = 0
        per_class = collections.defaultdict(lambda: [0, 0])
        errors = []
        for key, g in judged.items():
            if key not in got:
                missing += 1
                continue
            outcome, text = got[key]
            per_class[g['gold']][1] += 1
            if outcome != g['gold'] and outcome not in g.get('options', []):      # options: other states the gold also accepts
                wrong_kind += 1
                errors.append(f"- {key}: gold {g['gold']} → {label} {outcome} ({text[:70]})")
            elif outcome in ('repeat', 'replace') and not any(t in text for t in g.get('targets', [])):
                wrong_target += 1
                errors.append(f"- {key}: {outcome} right, target not acceptable: {text[:80]}")
            else:
                right += 1
                per_class[g['gold']][0] += 1
        total = right + wrong_kind + wrong_target
        print(f"\n{label}: {right}/{total} right ({wrong_kind} wrong kind, {wrong_target} wrong target, {missing} not decided in this ledger)")
        for cls in ('repeat', 'replace', 'new'):
            r_, n_ = per_class[cls]
            print(f"  {cls}: {r_}/{n_}")
        print('\n'.join(errors))


if __name__ == '__main__':
    main()
