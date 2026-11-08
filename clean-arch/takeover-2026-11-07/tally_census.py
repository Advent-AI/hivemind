"""Unblind the reader answers and count, per arm, helpful matters covered, extras by class and wrong statements."""
import collections, json, sys
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[2] / 'poc/data/clean-step1-takeover-2026-11-07'
key = json.loads(Path(sys.argv[1]).read_text())
answers = [a for part in range(1, 5) for a in json.loads((FOLDER / f'census-answer-{part}.json').read_text())]
assert sorted(a['article'] for a in answers) == list(range(1, 50)), 'every article judged once'
coverage = collections.Counter()
extras = collections.Counter()
wrong = collections.Counter()
clean_only_misses, production_only_misses = [], []
for article in answers:
    clean_letter = 'A' if key[str(article['article'])] == 'clean=A' else 'B'
    production_letter = 'B' if clean_letter == 'A' else 'A'
    for matter in article['matters']:
        weight = 'helpful' if matter['weight'] in ('core', 'supporting') else 'optional'
        for arm, letter in (('clean', clean_letter), ('production', production_letter)):
            coverage[(arm, weight, matter['weight'], matter[letter])] += 1
        if weight == 'helpful' and matter[clean_letter] == 'no' and matter[production_letter] != 'no':
            clean_only_misses.append((article['article'], matter['weight'], matter['matter']))
        if weight == 'helpful' and matter[production_letter] == 'no' and matter[clean_letter] != 'no':
            production_only_misses.append((article['article'], matter['weight'], matter['matter']))
    for arm, letter in (('clean', clean_letter), ('production', production_letter)):
        for extra in article[f'{letter}_extras']:
            extras[(arm, extra['class'])] += 1
        wrong[arm] += len(article[f'{letter}_wrong'])
helpful = sum(v for (arm, weight, _, _), v in coverage.items() if arm == 'clean' and weight == 'helpful')
print(f'helpful matters (core+supporting) in the 49 articles: {helpful}')
for arm in ('clean', 'production'):
    row = {state: sum(v for (a, w, _, s), v in coverage.items() if a == arm and w == 'helpful' and s == state) for state in ('yes', 'partial', 'no')}
    core = {state: sum(v for (a, w, c, s), v in coverage.items() if a == arm and c == 'core' and s == state) for state in ('yes', 'partial', 'no')}
    print(f'{arm:11s} helpful covered {row}  core {core}  extras {sum(v for (a, _), v in extras.items() if a == arm)}  wrong {wrong[arm]}')
print('extras by class:', sorted(extras.items()))
print(f'\nhelpful matters production covers and clean misses: {len(clean_only_misses)}')
for row in clean_only_misses: print('  ', row)
print(f'\nhelpful matters clean covers and production misses: {len(production_only_misses)}')
for row in production_only_misses: print('  ', row)
