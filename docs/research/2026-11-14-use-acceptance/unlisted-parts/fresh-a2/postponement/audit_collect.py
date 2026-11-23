"""D606's $0 audit of the postponed-event class, step 1: every event answer the frozen answer-choice step wrote in the stored gate-1
readings (probe readings: control sends only, by their sealed keys; plants and changed arms left out), collected once per distinct
answer (topic, question, due day and Ruled-out rung), with its whole Ruled-out rung (the model's decision and the sentence code adds),
its decider, the source item's day and every first reader's and third reader's R across the readings that showed it. Judges nothing.

  python3 audit_collect.py <output .jsonl>
"""
import collections
import glob
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent), str(HERE.parents[1])]
import d_split_census as census  # noqa: E402
import postponement_census as pc  # noqa: E402

KEYS = {'clean-unlisted-probe-2026-11-16': 'unlisted-probe', 'clean-unlisted-probe-a2-2026-11-16': 'unlisted-probe-a2',
        'clean-unlisted-probe-a3-2026-11-16': 'unlisted-probe-a3', 'clean-fresh-a2-2026-11-16': 'fresh-a2'}
BEFORE_THE_FROZEN_STEP = ('clean-ladder-stage-a-2026-11-10/run-2', 'clean-ladder-stage-a-2026-11-10/run-3')


def main(output):
    readings = sorted(os.path.dirname(f) for f in glob.glob(str(census.ROOT / 'poc/data/**/readers-answers'), recursive=True))
    answers, shown = {}, collections.Counter()
    for reading in readings:
        relative = str(Path(reading).relative_to(census.ROOT / 'poc/data'))
        if relative.startswith(BEFORE_THE_FROZEN_STEP):
            continue
        key_name = next((name for folder, name in KEYS.items() if relative.startswith(folder)), None)
        key = json.loads(Path(f'~/.hivemind-keys/{key_name}/key.json').expanduser().read_text()) if key_name else None
        items = census.items_of(reading)
        rows = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            if key is not None and not key[str(number)][0].startswith('control|'):
                continue
            ladder = item.get('ladder_as_the_judge_is_shown_it') or {}
            ruled_out = [rung for rung in ladder.get('rungs') or [] if rung.get('label') == 'Ruled out']
            if not ruled_out:
                continue
            shown[relative] += 1
            identity = json.dumps([(item.get('thesis') or {}).get('description'), ladder.get('question'), ladder.get('due_day'),
                                   ruled_out[0]['condition']], ensure_ascii=False)
            entry = answers.setdefault(identity, {
                'topic': (item.get('thesis') or {}).get('description'), 'question': ladder.get('question'), 'due_day': ladder.get('due_day'),
                'rungs': ladder.get('rungs'), 'ruled_out_by': (item.get('other_fields') or {}).get('ruled_out_by'),
                'decision': pc.first_sentence(ruled_out[0]['condition']), 'article_title': (item.get('article') or {}).get('title'),
                'article_day': (item.get('article') or {}).get('publication_date'), 'article_text': (item.get('article') or {}).get('text'),
                'seen': []})
            entry['seen'].append({'reading': relative, 'item': number, 'send': key[str(number)] if key else None,
                                  'R': {family: rows[family].get(number, {}).get('R') for family in census.FAMILIES},
                                  'R_why': {family: rows[family].get(number, {}).get('why', '') for family in census.FAMILIES},
                                  'third': pc.rulings_of(reading, number)})
    Path(output).write_text('\n'.join(json.dumps(entry, ensure_ascii=False) for entry in answers.values()) + '\n')
    print(f'frozen-step event answers shown: {sum(shown.values())} over {len(shown)} readings; distinct answers: {len(answers)}; '
          f'distinct topics: {len({a["topic"] for a in answers.values()})} -> {output}')
    for reading, count in sorted(shown.items()):
        print(f'   {count:4} {reading}')


if __name__ == '__main__':
    main(sys.argv[1])
