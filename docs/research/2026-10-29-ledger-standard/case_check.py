"""The cheapest proof before a whole-bench run (AGENTS section 1, step 4): on the decisive articles, for each version's
draws, how many draws kept each core or supporting gold entry, and how many not-kept sentences each draw kept, with the
named targets. python3 case_check.py CASES.json "LABEL:TAG,TAG,TAG" ..."""
import json, sys
import score_gold as sg
cases = json.load(open(sys.argv[1]))
versions = [(a.split(':')[0], a.split(':')[1].split(',')) for a in sys.argv[2:]]
gold = {a['input_id']: a for a in json.load(open('golden-v3/golden-v3-signed.json'))['articles']}
runs = {t: sg.answers(t) for _, tags in versions for t in tags}
SUPPRESS = ['structural shift', 'pivotal moment', 'not be worried', 'more like a hold', 'vicious competitor', 'outsources most of its manufacturing']
for iid in cases:
    a = gold[iid]
    print(f'## {a["title"][:80]}')
    for it in a['items']:
        if it['weight'] not in ('core', 'supporting'):
            continue
        row = []
        for label, tags in versions:
            n = 0
            for t in tags:
                s = sg.kept(runs[t].get(iid), iid)
                n += bool(s) and any(sg.same(it['span'], e['quote']) for e in s['evidence'])
            row.append(f'{label} {n}/{len(tags)}')
        if any(not r.endswith(f'{len(versions[0][1])}/{len(versions[0][1])}') for r in row):
            print(f'   {it["weight"][:4]} {" | ".join(row)} | {it["span"][:90]}')
    row = []
    for label, tags in versions:
        nk, sup = [], 0
        for t in tags:
            s = sg.kept(runs[t].get(iid), iid)
            k = [e for e in (s['evidence'] if s else []) if not any(sg.same(it['span'], e['quote']) for it in a['items'])
                 and any(sg.same(n['span'], e['quote']) and n['weight'] == 'not_kept' for n in a['not_kept'])]
            nk.append(len(k)); sup += sum(1 for e in k if any(x in e['quote'] for x in SUPPRESS))
        row.append(f'{label} not-kept kept {nk} (named targets {sup})')
    print('   ' + ' | '.join(row))
