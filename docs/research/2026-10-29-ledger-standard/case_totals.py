"""Totals over a case set, per draw: statements, gold core / supporting / optional kept, not-kept sentences kept, extras.
python3 case_totals.py CASES.json "LABEL:TAG,TAG,TAG" ..."""
import json, sys
import score_gold as sg
cases = json.load(open(sys.argv[1]))
gold = {a['input_id']: a for a in json.load(open('golden-v3/golden-v3-signed.json'))['articles']}
for spec in sys.argv[2:]:
    label, tags = spec.split(':'); rows = []
    for t in tags.split(','):
        ans = sg.answers(t); c = {'stmt': 0, 'core': 0, 'supp': 0, 'opt': 0, 'notkept': 0, 'extra': 0}
        for iid in cases:
            s = sg.kept(ans.get(iid), iid); a = gold[iid]
            if not s: continue
            c['stmt'] += len(s['evidence'])
            for it in a['items']:
                if any(sg.same(it['span'], e['quote']) for e in s['evidence']):
                    c[{'core': 'core', 'supporting': 'supp', 'optional': 'opt'}[it['weight']]] += 1
            for e in s['evidence']:
                if any(sg.same(it['span'], e['quote']) for it in a['items']): continue
                nk = [n for n in a['not_kept'] if sg.same(n['span'], e['quote'])]
                if nk and all(n['weight'] == 'not_kept' for n in nk): c['notkept'] += 1
                elif not nk: c['extra'] += 1
        rows.append(c)
    tot = {k: [r[k] for r in rows] for k in rows[0]}
    print(f'{label:8s}', tot)
