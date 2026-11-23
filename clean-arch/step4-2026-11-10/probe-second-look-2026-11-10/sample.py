"""The sample of the second-look test (D422), from the fourth Stage A's readings ($0).

Four groups, by what the two reader families and the two third readers marked on each stored answer:
  agreed    a mark both first readers fail, or both third readers rule failed, or a fault outside the form both uphold: all
  disputed  no agreed fault, and a mark or a named fault on which the two third readers part: all
  held      no agreed or disputed fault, and a mark one first reader failed or a fault one named, which both third readers
            held or dismissed: all
  sound     no mark failed and no fault named by either first reader: 30 drawn with a fixed seed, ten events, ten figures,
            ten declines

The sample file names each send and nothing else; the groups are written to a key outside the probe's folder, since neither
the model nor the readers of the second answers are told them.

  python3 clean-arch/step4-2026-11-10/probe-second-look-2026-11-10/sample.py <key path>
"""
import collections
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-4'
MARKS = ['Q', 'O', 'R', 'D', 'X', 'F', 'Y', 'L', 'XR', 'N']
SEED = 20261110
SOUND_OF_A_KIND = 10


def lines_of(pattern, folder):
    rows = {}
    for answer_file in sorted(folder.glob(pattern)):
        for line in answer_file.read_text().splitlines():
            if line.strip().startswith('{'):
                row = json.loads(line)
                rows[row.get('item', row.get('id'))] = row
    return rows


def main():
    key_path = Path(sys.argv[1])
    if key_path.resolve().is_relative_to(HERE):
        raise SystemExit('the key must sit outside the probe\'s folder')
    item_to_send = {int(item): tuple(send) for item, send in json.loads((RUN / 'key-item-to-send.json').read_text()).items()}
    first = {family: lines_of(f'reader-{family}-packet-*.jsonl', RUN / 'readers-answers') for family in ('codex', 'claude')}
    third = {family: lines_of(f'rulings-{family}-*.jsonl', RUN / 'third-reader') for family in ('codex', 'claude')}
    outcomes = {(row['case'], row['pass']): row for pass_folder in sorted(RUN.glob('send-*'))
                for line in (pass_folder / 'outcomes.jsonl').read_text().splitlines() for row in [json.loads(line)]}
    groups = collections.defaultdict(list)
    for item, send in sorted(item_to_send.items(), key=lambda pair: pair[1]):
        agreed, disputed, held = [], [], []
        for mark in MARKS:
            values = [first[family][item].get(mark) for family in ('codex', 'claude')]
            if values == ['fails', 'fails']:
                agreed.append(mark)
            elif 'fails' in values:
                rulings = [third[family].get(f'{item}-{mark}', {}).get('ruling') for family in ('codex', 'claude')]
                (agreed if rulings == ['fails', 'fails'] else disputed if 'fails' in rulings else held).append(mark)
        for point in [point for point in third['codex'] if str(point).startswith(f'{item}-W')]:
            upheld = [bool(third[family].get(point, {}).get('upheld')) for family in ('codex', 'claude')]
            (agreed if all(upheld) else disputed if any(upheld) else held).append('W')
        group = 'agreed' if agreed else 'disputed' if disputed else 'held' if held else 'sound'
        groups[group].append((send, agreed or disputed or held))
    kind_of = lambda send: ('declined' if outcomes[send]['status'] == 'no ladder' else 'event' if outcomes[send]['answer']['ladder'].get('event') else 'figure')
    chooser = random.Random(SEED)
    sound = []
    for kind in ('event', 'figure', 'declined'):
        of_kind = sorted(send for send, _ in groups['sound'] if kind_of(send) == kind)
        sound.extend(chooser.sample(of_kind, SOUND_OF_A_KIND))
    key = {'agreed': [[list(send), marks] for send, marks in groups['agreed']], 'disputed': [[list(send), marks] for send, marks in groups['disputed']],
           'held': [[list(send), marks] for send, marks in groups['held']], 'sound': [[list(send), []] for send in sorted(sound)]}
    sample = sorted({tuple(send) for group in key.values() for send, _ in group})
    (HERE / 'sample.json').write_text(json.dumps([list(send) for send in sample], indent=1) + '\n')
    key_path.write_text(json.dumps(key, indent=1) + '\n')
    print(f"read: {len(item_to_send)} answers; with an agreed fault {len(groups['agreed'])}, a disputed one {len(groups['disputed'])}, "
          f"a first reader's mark the third readers held {len(groups['held'])}, none from either first reader {len(groups['sound'])}")
    print(f"sample: {len(sample)} sends (agreed {len(key['agreed'])}, disputed {len(key['disputed'])}, held {len(key['held'])}, sound {len(key['sound'])}: "
          f"{dict(collections.Counter(kind_of(tuple(send)) for send, _ in key['sound']))})")


if __name__ == '__main__':
    main()
