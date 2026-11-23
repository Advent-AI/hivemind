"""Round 73's $0 reading: the topics the A2 clause would touch, each with its description, outcome, period and full article, for two
blind readers who decide under D397, D417, D436 and D437 whether it is one bet (with second sides), separate bets, a main part that
itself breaks a decline case, or unresolved. The packet names no arm, no stored answer and no earlier verdict.

  python3 build_packet.py
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = ROOT / 'poc/data'
CASE_FILES = {'fortnight': [DATA / 'clean-carried-run-2026-11-16/c1/cases/cases.json'],
              'week-10-06': [DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json'],
              'july': [DATA / f'clean-e2e-full-2026-11-13/c{n}/cases/cases.json' for n in (1, 2, 3)]}
TOPICS = [('fortnight', 'c1/clean-13'), ('july', 'c3/clean-7'),                                  # the two arm-A refusals
          ('july', 'c1/clean-15'), ('july', 'c2/clean-6'), ('july', 'c3/clean-3'), ('july', 'c1/clean-13'),
          ('week-10-06', 'c1/clean-12'), ('week-10-06', 'c1/clean-4'),                           # refusals both readers agreed
          ('july', 'c2/clean-10'), ('week-10-06', 'c1/clean-13'), ('july', 'c1/clean-11'), ('july', 'c1/clean-2')]   # split refusals
SEED = 20261116


def main():
    found = []
    for source, name in TOPICS:
        case = next(c for path in CASE_FILES[source] for c in json.loads(path.read_text()) if c['case'] == name)
        thesis, item = case['thesis'], case['item']
        found.append({'description': thesis['description'], 'outcome': thesis['outcome'], 'period': thesis.get('period'),
                      'article': {'publication_date': item['publication_date'], 'title': item['title'], 'text': item['text']},
                      'key': f'{source}:{name}'})
    random.Random(SEED).shuffle(found)
    key = {}
    for number, entry in enumerate(found, start=1):
        key[str(number)] = entry.pop('key')
        entry['topic'] = number
    (HERE / 'packet.json').write_text(json.dumps(found, ensure_ascii=False, indent=1) + '\n')
    keys = Path.home() / '.hivemind-keys' / 'unlisted-probe'
    keys.mkdir(parents=True, exist_ok=True)
    (keys / 'd436-key.json').write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(found)} topics; key outside the repository')


if __name__ == '__main__':
    main()
