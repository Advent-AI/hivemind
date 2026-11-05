"""Scores a probe_refile.py result against the frozen golds (see probe_refile.py). usage: python3 score_refile.py <refile.json> [--list]"""
import collections
import json
import sys

ROOT = '/Users/lchingen/hivemind'
sys.path[:0] = [f'{ROOT}/src', f'{ROOT}/docs/research/2026-11-04-filing-end-to-end']
import measure_filing as mf  # noqa: E402
import resend_filing as rf  # noqa: E402

items, pairs, cited_for, articles, by_passage = mf.load_gold()
seed = {e['question_id']: e['seed_view_id'] for e in json.load(open(f'{rf.GOLD}/gold-v1.json'))['entries'] if e.get('seed_view_id')}


def label(input_id, s):
    art = articles.get(input_id)
    if not art:
        return 'gold did not read', set()
    spans = [('kept', i['span'], i) for i in art['items']] + [('not kept', n['span'], n) for n in art['not_kept']]
    mine = rf.words(s['quote'] + ' ' + s['one_line'])
    top = max(spans, key=lambda x: len(mine & rf.words(x[1])), default=None)
    if not top or len(mine & rf.words(top[1])) < 3:
        return 'no gold span', set()
    if top[0] == 'not kept':
        return 'not kept by the standard', set()
    qs = cited_for.get(by_passage.get((input_id, top[1])), set())
    return ('used by the judgement gold' if qs else f'kept {top[2]["weight"]}, used by no question'), {seed[q] for q in qs if q in seed}


tally, fails = collections.Counter(), []
for conv in json.load(open(sys.argv[1])):
    for s in conv['rows']:
        lab, homes = label(conv['input_id'], s)
        start = 'homeless' if not s['before'] else 'revenue only'
        after = set(s['after'])
        if lab == 'used by the judgement gold':
            outcome = 'right home' if after & homes else ('none' if not after else 'another question')
            if outcome != 'right home':
                fails.append((start, sorted(homes), sorted(after), s['one_line'][:90]))
        else:
            outcome = 'none' if not after else 'linked'
        tally[(lab.split(',')[0] if lab.startswith('kept') else lab, start, outcome)] += 1
for k in sorted(tally):
    print(f'  {k[0]:28} {k[1]:13} → {k[2]:16} {tally[k]}')
if '--list' in sys.argv:
    for f in fails:
        print('  ', f)
