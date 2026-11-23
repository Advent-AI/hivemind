"""Print probe answers for reading (no scoring): per case and answer, the new theses, the kept items with their links and condition, and
the unfiled items.

Usage: print_answers.py <records.json> <case> [arm,...]"""
import json, sys

records = json.loads(open(sys.argv[1]).read())
case = sys.argv[2]
arms = sys.argv[3].split(',') if len(sys.argv) > 3 else None
for r in records:
    if r['case'] != case or (arms and r['arm'] not in arms):
        continue
    print(f"--- {r['arm']} d{r['draw']}" + (f"  ERROR {r.get('error') or r.get('contract_error')}" if 'kept' not in r else ''))
    if 'kept' not in r:
        continue
    for t in r['new_theses']:
        print(f"  NEW [{t['local_id']}] {t['description'][:150]}")
    for ev in r['kept']:
        c = ev.get('condition')
        cond = f"  COND[{c['kind']}: {c['measure']} | {c['period']} | {c['value']}]" if c else ''
        cond += ''.join(f"  FIG[{f['kind']}: {f['measure']} | {f['period']} | {f['value']}]" for f in ev.get('figures') or [])
        print(f"  KEPT -> {[l['target_id'] for l in ev['links']]}{cond} | {ev['summary'][:120]}")
    for ev in r['unfiled']:
        print(f"  DROP | {ev['summary'][:120]}")
    for issue in r.get('answer', {}).get('_none', []):
        pass
