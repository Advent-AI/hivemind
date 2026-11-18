"""The D diagnostic's candidate items (council rounds 104 and 105; $0). Copied whole from stored gate-1 packets, a fixed seed, every
topic at most once across the whole sample, in these groups (drawn in this order, so a topic drawn into an earlier group is not
available to a later one):

  class-split     a binding obligation's yearly figure, day set by code (basis expected_publication), Codex failed D, Claude passed
  class-agreed    the same class where both first readers passed D
  fail-control    both first readers failed D (any kind)
  hold-stated     basis stated, both first readers passed D
  stated-kept     CONSTRUCTED from an unused class topic: the article gains one sentence stating the annual report's filing day, and
                  the choices show that day with basis stated (D should hold)
  stated-over     CONSTRUCTED likewise, but the choices keep code's day with basis expected_publication (D should fail: the day
                  contradicts a date the article gives)

  python3 d_sample.py <output candidates .json>
"""
import copy
import json
import random
import sys
from pathlib import Path

import d_split_census as census

SEED = 20261117
WANTED = {'class-split': 8, 'class-agreed': 4, 'fail-control': 6, 'hold-stated': 4}
STATED_DAY, STATED_SENTENCE = '2027-02-24', 'NVIDIA said it will file its fiscal 2027 annual report on Form 10-K on February 24, 2027.'


def group_of(item, rows, number):
    shown, other = item.get('ladder_as_the_judge_is_shown_it') or {}, item.get('other_fields') or {}
    marks = tuple(rows[family].get(number, {}).get('D') for family in census.FAMILIES)
    obligation = (item.get('thesis') or {}).get('opens_as') == 'binding_obligation'
    if census.in_class(item) and obligation and marks == ('fails', 'holds'):
        return 'class-split'
    if census.in_class(item) and obligation and marks == ('holds', 'holds'):
        return 'class-agreed'
    if shown and marks == ('fails', 'fails'):
        return 'fail-control'
    if shown and other.get('due_day_basis') == 'stated' and marks == ('holds', 'holds'):
        return 'hold-stated'
    return None


def constructed(entry, group):
    """A class item given a stated filing day in its article; the choices show that day (stated-kept) or keep code's (stated-over)."""
    item = copy.deepcopy(entry['item'])
    item['article']['text'] = item['article']['text'].rstrip() + '\n' + STATED_SENTENCE
    if group == 'stated-kept':
        item['ladder_as_the_judge_is_shown_it']['due_day'] = STATED_DAY
        item['other_fields']['due_day_basis'] = 'stated'
    return {'group': group, 'source': entry['source'], 'constructed': f'article + "{STATED_SENTENCE}"' +
            (f'; due day {STATED_DAY}, basis stated' if group == 'stated-kept' else '; code-set due day and basis kept'),
            'first_readers': None, 'item': item}


def main(output):
    readings = sorted(str(Path(found).parent) for found in census.ROOT.glob('poc/data/**/readers-answers'))
    pools = {group: {} for group in WANTED}
    for reading in readings:
        items = census.items_of(reading)
        rows = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            group = group_of(item, rows, number)
            topic = (item.get('thesis') or {}).get('description')
            if group and topic not in pools[group]:
                pools[group][topic] = {'group': group, 'source': [str(Path(reading).relative_to(census.ROOT)), number],
                                       'first_readers': {family: {'D': rows[family][number].get('D'), 'why': rows[family][number].get('why')}
                                                         for family in census.FAMILIES},
                                       'item': {key: value for key, value in item.items() if key != 'item'}}
    chosen, used = [], set()
    for group, count in WANTED.items():
        candidates = sorted((entry for topic, entry in pools[group].items() if topic not in used), key=lambda entry: tuple(entry['source']))
        drawn = random.Random(SEED).sample(candidates, min(count, len(candidates)))
        used |= {entry['item']['thesis']['description'] for entry in drawn}
        chosen += drawn
        print(f'{group}: {len(candidates)} distinct unused topics, {len(drawn)} drawn')
    spare = sorted((entry for pool in ('class-split', 'class-agreed') for topic, entry in pools[pool].items() if topic not in used),
                   key=lambda entry: tuple(entry['source']))
    for group, entry in zip(('stated-kept', 'stated-over'), random.Random(SEED).sample(spare, 2)):
        chosen.append(constructed(entry, group))
        used.add(entry['item']['thesis']['description'])
        print(f'{group}: constructed from {entry["source"]}')
    if len(used) != len(chosen):
        raise SystemExit('a topic repeats in the sample')
    Path(output).write_text(json.dumps(chosen, ensure_ascii=False, indent=1) + '\n')
    print(f'{len(chosen)} candidates, {len(used)} distinct topics -> {output}')


if __name__ == '__main__':
    main(sys.argv[1])
