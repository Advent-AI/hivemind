"""Unblind probe scores: per arm, helpful matters covered (of matter-answer pairs), extras by class and wrong statements.

Usage: tally_probe.py <probe folder> <label key file>"""
import collections, json, sys
from pathlib import Path

probe, key = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text())
scores = [a for part in range(1, 5) for a in json.loads((probe / f'score-answer-{part}.json').read_text())]
packets = {p['article']: p for part in range(1, 5) for p in json.loads((probe / f'score-packet-{part}.json').read_text())}
assert sorted(s['article'] for s in scores) == sorted(packets), 'every article scored once'
totals = collections.defaultdict(collections.Counter)
per_article = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for score in scores:
    number = score['article']
    weights = {m['id']: m['weight'] for m in packets[number]['matters']}
    weights.update({m['id']: m['weight'] for m in score.get('added_matters', [])})
    assert set(score['answers']) == set(packets[number]['answers']), f'article {number}: every answer scored'
    for label, judged in score['answers'].items():
        arm = key[f'{number}:{label}'].split(':')[0]
        for matter_id, weight in weights.items():
            state = judged['coverage'].get(matter_id, 'missing')
            group = 'helpful' if weight in ('core', 'supporting') else 'optional'
            totals[arm][(group, state)] += 1
            if weight == 'core':
                totals[arm][('core', state)] += 1
            if group == 'helpful':
                per_article[number][arm][state] += 1
        for extra in judged['extras']:
            totals[arm][('extra', extra['class'])] += 1
            per_article[number][arm]['extra'] += 1
        totals[arm][('wrong', 'any')] += len(judged['wrong'])
        totals[arm][('answers', 'n')] += 1
for arm, counter in totals.items():
    helpful = {s: counter[('helpful', s)] for s in ('yes', 'partial', 'no', 'missing')}
    core = {s: counter[('core', s)] for s in ('yes', 'partial', 'no')}
    extras = {k[1]: v for k, v in counter.items() if k[0] == 'extra'}
    print(f'{arm:8s} answers {counter[("answers", "n")]}  helpful {helpful}  core {core}  extras {sum(extras.values())} {extras}  wrong {counter[("wrong", "any")]}')
print('\nper article (helpful yes / partial / no, extras), summed over three draws:')
for number in sorted(per_article):
    row = per_article[number]
    print(number, {arm: (c['yes'], c['partial'], c['no'], c['extra']) for arm, c in sorted(row.items())})
