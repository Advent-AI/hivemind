"""Per gold matter, its state in every draw of two arms (the funnel's five states: reaches, reaches as repeat, dropped at placement,
extracted but lost later, not extracted), and the matters whose state differs between the arms in at least two draws of three, with the
gold's weight and rule, so a regression class can be read matter by matter ($0, finished run folders). Same classification as e2e_funnel.

    python3 matter_states.py <arm A name>=<d1>,<d2>,<d3> <arm B name>=<d1>,<d2>,<d3>
"""
import collections
import json
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(ROOT / 'docs/research/2026-10-31-reference-context'), str(ROOT / 'src')]
import score_ref as sr  # noqa: E402

REACHED = ('reaches', 'reaches as repeat')


def states(run):
    views = sqlite3.connect(f'file:{run}/views.sqlite?mode=ro', uri=True); views.row_factory = sqlite3.Row
    archive = sqlite3.connect(f'file:{run}/archive.sqlite?mode=ro', uri=True)
    replaced = {r[0] for r in views.execute('select old_evidence_id from replacements')}
    repeats = {r[0] for r in views.execute('select new_evidence_id from same_claims')}
    out = {}
    for a in sr.articles:
        iid = a['input_id']
        r = archive.execute("select answer_json from model_calls where purpose='extract' and request_json like ? order by call_id desc limit 1", (f'%[Item] id {iid},%',)).fetchone()
        answer = json.loads(r[0]) if r and r[0] else {}
        by_id = {e['id']: e for e in answer.get('evidence', [])}
        h = views.execute('select handover_json from handovers where input_id=? order by id desc limit 1', (iid,)).fetchone()
        dropped_ids = {e for e, _ in json.loads(h['handover_json']).get('dropped', [])} if h else set()
        dropped = [by_id[e] for e in dropped_ids if e in by_id]
        stored = [dict(x) for x in views.execute('select evidence_id, quote, one_line from evidence where created_from_input=?', (iid,))]
        shown = [s for s in stored if s['evidence_id'] not in replaced]
        for n, it in enumerate(a['items']):
            if it['weight'] not in ('core', 'supporting'):
                continue
            if any(sr.sg.same_matter(it, s) for s in shown if s['evidence_id'] not in repeats):
                state = 'reaches'
            elif any(sr.sg.same_matter(it, s) for s in shown):
                state = 'reaches as repeat'
            elif any(sr.sg.same_matter(it, e) for e in dropped):
                state = 'dropped at placement'
            elif any(sr.sg.same_matter(it, e) for e in by_id.values()):
                state = 'extracted, lost later'
            else:
                state = 'not extracted'
            out[(iid, n)] = (state, it['weight'], a.get('title', '')[:50], it.get('span', '')[:120], (it.get('rule') or it.get('gold_rule') or '')[:80])
    return out


def main():
    arms = {}
    for arg in sys.argv[1:]:
        name, paths = arg.split('=', 1)
        arms[name] = [states(str(ROOT / p) if not p.startswith('/') else p) for p in paths.split(',')]
    (name_a, draws_a), (name_b, draws_b) = list(arms.items())[:2]
    keys = sorted(set().union(*[set(d) for d in draws_a + draws_b]))
    summary = collections.Counter()
    diffs = collections.defaultdict(list)
    for k in keys:
        sa = [d[k][0] for d in draws_a if k in d]; sb = [d[k][0] for d in draws_b if k in d]
        meta = next(d[k] for d in draws_a + draws_b if k in d)
        reach_a = sum(s in REACHED for s in sa); reach_b = sum(s in REACHED for s in sb)
        ext_a = sum(s != 'not extracted' for s in sa); ext_b = sum(s != 'not extracted' for s in sb)
        weight = meta[1]
        if reach_a >= 2 and reach_b <= 1:
            summary[(weight, f'reaches in {name_a}, not in {name_b}')] += 1
            diffs[(weight, f'reaches in {name_a}, not in {name_b}')].append((sa, sb, meta))
        elif reach_b >= 2 and reach_a <= 1:
            summary[(weight, f'reaches in {name_b}, not in {name_a}')] += 1
            diffs[(weight, f'reaches in {name_b}, not in {name_a}')].append((sa, sb, meta))
        if ext_a >= 2 and ext_b <= 1:
            summary[(weight, f'extracted in {name_a}, not in {name_b}')] += 1
            diffs[(weight, f'extracted in {name_a}, not in {name_b}')].append((sa, sb, meta))
        elif ext_b >= 2 and ext_a <= 1:
            summary[(weight, f'extracted in {name_b}, not in {name_a}')] += 1
            diffs[(weight, f'extracted in {name_b}, not in {name_a}')].append((sa, sb, meta))
    print(f'gold matters compared: {len(keys)}; a difference = the state holds in at least two draws of one arm and at most one of the other')
    for (weight, label), n in sorted(summary.items()):
        print(f'   {weight:10s} {label}: {n}')
    for (weight, label), rows in sorted(diffs.items()):
        print(f'\n## {weight} | {label} ({len(rows)})')
        for sa, sb, meta in rows:
            print(f"   {name_a} {[s[:9] for s in sa]} | {name_b} {[s[:9] for s in sb]} | {meta[2]} | {meta[3]}")


if __name__ == '__main__':
    main()
