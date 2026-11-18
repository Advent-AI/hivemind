"""A $0 census of the answer-choice step's refusals (D614): every refusal the frozen step wrote in the stored gate-1 readings (probe
readings: control sends only, by their sealed keys), with both first readers' N, the third readers' N where ruled, the model's stated
reason and the topic; grouped by topic, with how many of that topic's sends refused. Judges nothing.

  python3 refusal_census.py <output .jsonl>
"""
import collections
import glob
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRESH = HERE.parent / 'unlisted-parts' / 'fresh-a2'
sys.path[:0] = [str(FRESH), str(FRESH.parent), str(FRESH / 'postponement')]
import d_split_census as census  # noqa: E402
from audit_collect import BEFORE_THE_FROZEN_STEP, KEYS  # noqa: E402


def third(reading, number, mark):
    found = {}
    for family in census.FAMILIES:
        for ruling_file in glob.glob(f'{reading}/third-reader/rulings-{family}-*.jsonl'):
            for line in Path(ruling_file).read_text().splitlines():
                if line.strip().startswith('{'):
                    try:
                        ruling = json.loads(line)
                    except ValueError:
                        continue
                    if ruling.get('id') == f'{number}-{mark}':
                        found[family] = ruling.get('ruling')
    return found


def main(output):
    readings = sorted(os.path.dirname(f) for f in glob.glob(str(census.ROOT / 'poc/data/**/readers-answers'), recursive=True))
    rows = []
    for reading in readings:
        relative = str(Path(reading).relative_to(census.ROOT / 'poc/data'))
        if relative.startswith(BEFORE_THE_FROZEN_STEP):
            continue
        key_name = next((name for folder, name in KEYS.items() if relative.startswith(folder)), None)
        key = json.loads(Path(f'~/.hivemind-keys/{key_name}/key.json').expanduser().read_text()) if key_name else None
        items = census.items_of(reading)
        marks = {family: census.rows_of(reading, family) for family in census.FAMILIES}
        for number, item in sorted(items.items()):
            if key is not None and not key[str(number)][0].startswith('control|'):
                continue
            shown = item.get('ladder_as_the_judge_is_shown_it') or {}
            n_marks = tuple(marks[family].get(number, {}).get('N') for family in census.FAMILIES)
            if not any(m in ('holds', 'fails') for m in n_marks):
                continue                                    # N applies to refusals only
            rows.append({'reading': relative, 'item': number, 'topic': (item.get('thesis') or {}).get('description'),
                         'reason': (item.get('other_fields') or {}).get('reason') or shown.get('reason') or item.get('refusal_reason'),
                         'N': n_marks, 'N_third': third(reading, number, 'N'),
                         'why': {family: marks[family].get(number, {}).get('why', '') for family in census.FAMILIES}})
    Path(output).write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n')
    settled = lambda r: ('fails' if r['N'] == ('fails', 'fails') or (r['N'][0] != r['N'][1] and list(r['N_third'].values()) == ['fails'] * len(r['N_third']) and r['N_third'])
                         else 'holds' if r['N'] == ('holds', 'holds') or (r['N_third'] and set(r['N_third'].values()) == {'holds'}) else 'split')
    tally = collections.Counter(settled(r) for r in rows)
    print(f'refusals read on N: {len(rows)} over {len({r["topic"] for r in rows})} topics; settled {dict(tally)}')
    by_topic = collections.defaultdict(list)
    for r in rows:
        by_topic[r['topic']].append(settled(r))
    print('\ntopics with an unjustified (fails) or split refusal:')
    for topic, outcomes in by_topic.items():
        if set(outcomes) - {'holds'}:
            print(f'  {collections.Counter(outcomes)} | {(topic or "")[:150]}')


if __name__ == '__main__':
    main(sys.argv[1])
