"""Summary of test 1 (test1-answers.json): per request and arm, three sends: links per linked statement, share with two or more links,
statements with no link, and the decisive statements (Broadcom figures to v16, NVIDIA share figures to v6, guard statements unlinked)."""
import json, re, sqlite3, collections
A = json.load(open('test1-answers.json'))
CALLS = ['d1:213', 'd1:370', 'd1:713', 'd1:760', 'd1:429', 'd1:100']
ARMS = ['stored', 'nofallback', 'v1', 'v2']
BROADCOM = re.compile(r'broadcom', re.I); BCNUM = re.compile(r'10\.8|16(\.0)? billion|\$16|ai semiconductor|custom (ai )?(accelerator|asic|chip)|asic', re.I)
SHARE = re.compile(r'(\d{2})%.{0,60}(market|share)|(market|share).{0,60}(\d{2})%', re.I)
VAL = re.compile(r'p/e|price target|target price|forward earnings|multiple|valuation|cheap', re.I)
tot = collections.defaultdict(lambda: collections.Counter())
for call in CALLS:
    print(f'\n## {call}')
    for arm in ARMS:
        row = []
        for n in range(3):
            a = A.get(f'{call}|{arm}|{n}', {}); ev = a.get('evidence', [])
            linked = [e for e in ev if e.get('links')]
            nl = [len([l for l in e['links'] if l.startswith('v')]) for e in linked]
            bc = [e for e in ev if BROADCOM.search(e.get('quote', '') + e.get('one_line', '')) and BCNUM.search(e.get('quote', '') + e.get('one_line', ''))]
            sh = [e for e in ev if SHARE.search(e.get('one_line', '')) and re.search(r'nvidia', e.get('one_line', ''), re.I) and not BROADCOM.search(e.get('one_line', ''))]
            vl = [e for e in ev if VAL.search(e.get('one_line', ''))]
            row.append(f"{len(ev)}st/{len(ev)-len(linked)}empty/avg{(sum(nl)/len(nl) if nl else 0):.2f}/2+:{sum(1 for x in nl if x >= 2)}"
                       f" | bc->v16 {sum('v16' in (e.get('links') or []) for e in bc)}/{len(bc)} bc->v1 {sum('v1' in (e.get('links') or []) for e in bc)}"
                       f" | share->v6 {sum('v6' in (e.get('links') or []) for e in sh)}/{len(sh)} share->v1/v2 {sum(bool({'v1','v2'} & set(e.get('links') or [])) for e in sh)}"
                       f" | valuation linked {sum(1 for e in vl if e.get('links'))}/{len(vl)}")
            tot[arm]['statements'] += len(ev); tot[arm]['linked'] += len(linked); tot[arm]['links'] += sum(nl); tot[arm]['two_plus'] += sum(1 for x in nl if x >= 2)
            if call in ('d1:429', 'd1:100', 'd1:760'): tot[arm]['guard_two_plus'] += sum(1 for x in nl if x >= 2)
        print(f'  {arm:<10} ' + '\n             '.join(row))
print('\n## totals over six requests, three sends each')
for arm in ARMS:
    t = tot[arm]
    print(f"  {arm:<10} statements {t['statements']}, linked {t['linked']}, links per linked {t['links']/max(1,t['linked']):.2f}, two or more links {t['two_plus']}, in guard articles {t['guard_two_plus']}")
