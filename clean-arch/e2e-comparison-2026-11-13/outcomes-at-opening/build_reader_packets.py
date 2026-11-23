"""D478's two blind readings ($0), built from the probe's records:

1. ladderable (both arms, arm-blind): every new thesis on the target and should-not-open cases, with only its question, outcome and period
   (c19's two new fields removed), shuffled with a fixed seed;
2. quality (c19 only): every c19 new thesis with its question, outcome, period, settles_on and outcomes.

The key (item number → case, arm, send, thesis) is written outside the repository, to the path given, so no reader can list it.

  python3 build_reader_packets.py <records.jsonl> <key folder outside the repository>
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LADDERABLE_CASES = {'c1-memh100', 'c2-memrack', 'c1-intel', 'c1-firmus', 'c3-chinaok', 'c2-asic', 'c1-survey', 'c3-surveyb', 'c1-federal'}
SHOWN = ('description', 'outcome', 'period')


def main():
    records = [json.loads(line) for line in open(sys.argv[1]) if line.strip()]
    key_folder = Path(sys.argv[2])
    key_folder.mkdir(parents=True, exist_ok=True)
    ladderable, quality = [], []
    for record in records:
        for index, thesis in enumerate(record.get('new_theses') or []):
            source = {'case': record['case'], 'arm': record['arm'], 'send': record['send'], 'thesis': index}
            if record['case'] in LADDERABLE_CASES:
                ladderable.append((source, {k: thesis.get(k) for k in SHOWN}))
            if record['arm'] == 'c19':
                quality.append((source, {k: thesis.get(k) for k in SHOWN + ('settles_on', 'outcomes')}))
    for name, rows in (('ladderable', ladderable), ('quality', quality)):
        order = random.Random(f'20261113:{name}').sample(rows, len(rows))
        packet = [dict(item=number, **shown) for number, (_source, shown) in enumerate(order, 1)]
        key = [dict(item=number, **source) for number, (source, _shown) in enumerate(order, 1)]
        (HERE / f'packet-{name}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=1) + '\n')
        (key_folder / f'key-{name}.json').write_text(json.dumps(key, indent=1) + '\n')
        print(f'{name}: {len(packet)} theses')


if __name__ == '__main__':
    main()
