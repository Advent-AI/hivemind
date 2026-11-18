"""Ruled-out rungs that may catch a postponement (D590; line 3; $0).

Every event answer in every stored gate-1 reading packet is listed with its Ruled-out rung's first sentence (the step's named decision;
code's own sentence follows "This rung holds when"). A screen picks the sentences bounded by a date or speaking of a delay. The screen
only chooses what is printed for reading: each picked answer is printed whole (question, topic, rungs) with both first readers' R and
both third readers' R rulings, and every one is read by hand. The screen is validated on a known positive (the fresh week's control
clean-17 pass 3), on known negatives (a sample of answers both families passed on R with no date in the sentence) and on a sample it did
not pick.

  python3 postponement_census.py <output .jsonl>
"""
import collections
import glob
import json
import os
import random
import re
import sys
from pathlib import Path

import d_split_census as census

MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December'
BOUNDED = re.compile(rf'\b(by|before|until|no later than|prior to)\s+(the end of\s+)?(\d{{4}}-\d{{2}}-\d{{2}}|({MONTHS})\b|(end|year-end|the due day|fiscal)|\d{{4}}\b)', re.I)
DELAY = re.compile(r'postpon|delay|defer|push(es|ed)? back|later than', re.I)
KNOWN_POSITIVE = ('poc/data/clean-fresh-a2-2026-11-16/choices/reading', 30)


def first_sentence(rung_condition):
    return rung_condition.split(' This rung holds when')[0].strip()


def rulings_of(reading, number):
    found = {}
    for family in census.FAMILIES:
        for ruling_file in glob.glob(f'{reading}/third-reader/rulings-{family}-*.jsonl'):
            for line in Path(ruling_file).read_text().splitlines():
                if line.strip().startswith('{'):
                    try:
                        ruling = json.loads(line)
                    except ValueError:
                        continue
                    if ruling.get('id') == f'{number}-R':
                        found[family] = ruling.get('ruling')
    return found


def main(output):
    readings = sorted(os.path.dirname(found) for found in glob.glob(str(census.ROOT / 'poc/data/**/readers-answers'), recursive=True))
    events, picked = [], []
    for reading in readings:
        items = census.items_of(reading)
        rows = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            rungs = (item.get('ladder_as_the_judge_is_shown_it') or {}).get('rungs') or []
            ruled_out = [rung for rung in rungs if rung.get('label') == 'Ruled out']
            if not ruled_out:
                continue
            sentence = first_sentence(ruled_out[0]['condition'])
            entry = {'reading': str(Path(reading).relative_to(census.ROOT)), 'item': number,
                     'topic': (item.get('thesis') or {}).get('description'), 'question': item['ladder_as_the_judge_is_shown_it'].get('question'),
                     'due_day': item['ladder_as_the_judge_is_shown_it'].get('due_day'), 'ruled_out_by': (item.get('other_fields') or {}).get('ruled_out_by'),
                     'sentence': sentence, 'R': {family: rows[family].get(number, {}).get('R') for family in census.FAMILIES},
                     'R_why': {family: rows[family].get(number, {}).get('why', '') for family in census.FAMILIES},
                     'R_rulings': rulings_of(reading, number),
                     'screen': bool(BOUNDED.search(sentence) or DELAY.search(sentence))}
            events.append(entry)
            if entry['screen']:
                picked.append(entry)
    Path(output).write_text('\n'.join(json.dumps(entry, ensure_ascii=False) for entry in picked) + '\n')
    positive = [entry for entry in events if (entry['reading'], entry['item']) == KNOWN_POSITIVE]
    if not positive or not positive[0]['screen']:
        raise SystemExit('SCREEN FAILED: the known positive (fresh control clean-17 pass 3) is not picked')
    topics = {entry['topic'] for entry in picked}
    print(f'event answers read: {len(events)} over {len({entry["topic"] for entry in events})} topics; picked by the screen: {len(picked)} '
          f'answers over {len(topics)} topics -> {output}')
    print('known positive picked: yes')
    print('picked answers by first readers\' R:', dict(collections.Counter(tuple(entry['R'].values()) for entry in picked)))
    unpicked = [entry for entry in events if not entry['screen']]
    negatives = [entry for entry in unpicked if tuple(entry['R'].values()) == ('holds', 'holds')]
    print(f'\nknown negatives (both families R holds, not picked): {len(negatives)}; a sample of 5:')
    for entry in random.Random(20261119).sample(negatives, min(5, len(negatives))):
        print('  -', entry['sentence'][:200])
    print('\nan unpicked sample of 10 (any R), for reading:')
    for entry in random.Random(20261120).sample(unpicked, min(10, len(unpicked))):
        print(f'  - R {tuple(entry["R"].values())} | {entry["sentence"][:200]}')


if __name__ == '__main__':
    main(sys.argv[1])
