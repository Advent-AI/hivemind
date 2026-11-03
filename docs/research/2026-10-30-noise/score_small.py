"""Score the noise small sample against its frozen key (key-small.json; the sha256 is checked first). Code counts structure only; every
guard a version loses is listed with that version's statements on the page, to be read.

    python3 score_small.py N1 v53 v57 v58
    python3 score_small.py - N1:v53 N1:v57 F1:v53F --subset probed,empty     # runs named run:version; only those key articles
    python3 score_small.py Z v59 v60 --key key-v60                             # another frozen key
"""
import collections
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / '2026-10-29-ledger-standard'
sys.path[:0] = [str(LEDGER), str(LEDGER / 'final-2026-10-30')]
import score_gold as sg  # noqa: E402
import final_scores as fs  # noqa: E402

args = sys.argv[1:]
subset = None
key_name = 'key-small'
if '--key' in args:
    key_name = args[args.index('--key') + 1]
    args = args[:args.index('--key')] + args[args.index('--key') + 2:]
if '--subset' in args:
    subset = args[args.index('--subset') + 1].split(',')
    args = args[:args.index('--subset')]
prefix, versions = args[0], args[1:]
tags = {v: (v.replace(':', '-') if prefix == '-' else f'{prefix}-{v}') for v in versions}
body = (HERE / f'{key_name}.json').read_text()
expected = (HERE / f'{key_name}.sha256').read_text().split()[0]
assert hashlib.sha256(body.encode()).hexdigest() == expected, f'{key_name}.json changed after it was frozen'
key = json.loads(body)
if subset:
    keep = [i for i in key['articles'] if ('probed' in subset and i in key['probed_articles']) or ('empty' in subset and i in key['empty_pages'])]
    key['articles'] = keep
    key['decisive_not_kept'] = [d for d in key['decisive_not_kept'] if d['input_id'] in keep]
    key['guard_items'] = [g for g in key['guard_items'] if g['input_id'] in keep]
gold = {a['input_id']: a for a in json.loads(Path(fs.GOLDS['dev']).read_text())['articles']}
print('key sha256', expected[:12], '| gold sha256', sg.sha(fs.GOLDS['dev'])[:12], '| articles', len(key['articles']))

sifted = {v: [{iid: sg.kept(run.get(iid), iid) for iid in key['articles']} for run in (sg.answers(f'{tags[v]}-d{d}') for d in (1, 2, 3))]
          for v in versions}


def kept_draws(version, iid, test):
    return sum(bool(s.get(iid)) and any(test(e) for e in s[iid]['evidence']) for s in sifted[version])


rows = collections.OrderedDict()
for v in versions:
    draws = sifted[v]
    unusable = [sum(s.get(i) is None for i in key['articles']) for s in draws]
    decisive = [kept_draws(v, d['input_id'], lambda e, d=d: sg.same(d['span'], e['quote'])) for d in key['decisive_not_kept']]
    guards = [(g, kept_draws(v, g['input_id'], lambda e, g=g: sg.same_matter(next(i for i in gold[g['input_id']]['items'] if i['span'] == g['span']), e)))
              for g in key['guard_items']]
    per_draw = collections.defaultdict(list)
    for s in draws:
        c = collections.Counter()
        for iid in key['articles']:
            a, r = gold[iid], s.get(iid)
            if not r:
                continue
            c['statements'] += len(r['evidence'])
            c['dropped by code'] += sum(1 for d in r['dropped'] if str(d[0]).startswith('e'))
            c['candidates'] += len(r['candidates'])
            for e in r['evidence']:
                if any(sg.same_matter(i, e) for i in a['items']):
                    c['gold ' + next(i['weight'] for i in a['items'] if sg.same_matter(i, e))] += 1
                elif any(sg.same(n['span'], e['quote']) for n in a['not_kept'] if n['weight'] == 'not_kept'):
                    c['gold not-kept'] += 1
                elif any(sg.same(n['span'], e['quote']) for n in a['not_kept']):
                    c['gold optional'] += 1
                else:
                    c['outside gold'] += 1
            if iid in key['empty_pages']:
                c['empty-page statements'] += len(r['evidence'])
        for k, val in c.items():
            per_draw[k].append(val)
    rows[v] = {'unusable answers per draw': unusable,
               'decisive not-kept: draws kept (of 3 x %d)' % len(decisive): sum(decisive),
               'decisive not-kept kept in >=2 draws': sum(x >= 2 for x in decisive),
               'core guards kept every draw (of %d)' % sum(g['weight'] == 'core' for g, _ in guards): sum(n == 3 for g, n in guards if g['weight'] == 'core'),
               'supporting guards kept >=2 draws (of %d)' % sum(g['weight'] == 'supporting' for g, _ in guards): sum(n >= 2 for g, n in guards if g['weight'] == 'supporting'),
               'guard kept-draws total (of %d)' % (3 * len(guards)): sum(n for _, n in guards),
               **{k + ' per draw': per_draw[k] for k in ('statements', 'gold core', 'gold supporting', 'gold optional', 'gold not-kept', 'outside gold',
                                                         'empty-page statements', 'dropped by code', 'candidates')}}
    rows[v]['_guards'] = guards

names = [k for k in rows[versions[0]] if not k.startswith('_')]
width = max(len(n) for n in names)
print(f"{'':{width}}  " + '  '.join(f'{v:>14}' for v in versions))
for n in names:
    print(f'{n:{width}}  ' + '  '.join(f'{str(rows[v][n]):>14}' for v in versions))

control = versions[0]
base = {g['span']: n for g, n in rows[control]['_guards']}
for v in versions[1:]:
    lost = [(g, base[g['span']], n) for g, n in rows[v]['_guards'] if base[g['span']] >= 2 and n <= base[g['span']] - 2 or (g['weight'] == 'core' and base[g['span']] == 3 and n < 3)]
    print(f'\n## {v}: guards {control} kept that {v} lost (core: any draw lost from 3/3; supporting: two draws fewer) — read each')
    for g, b, n in lost:
        print(f"- [{g['weight']}] {g['input_id'][:30]} {control} {b}/3 -> {v} {n}/3 | {g['span'][:170]}")
