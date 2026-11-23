"""The census of unsupported judgements, step 1 ($0; D518): every stored judgement of the two earlier readings (the Stage B baseline and
Stage B itself) that both first readers did not pass as SUPPORTED, with each reader's verdict and reason, the third readers' rulings,
the settled verdict by those readings' own rule, and the author's stored own read. It reads the readers' stored files with the earlier
count script's own row reader and re-derives nothing else; it judges nothing.

  python3 inventory_earlier_readings.py <folder holding stage-b-baseline-key.json and stage-b-reading-key.json>
"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'clean-arch/step4-2026-11-10/stage_b'))
import baseline_count  # noqa: E402

FAMILIES = ('codex', 'claude')
READINGS = {'baseline': (ROOT / 'poc/data/clean-stage-b-baseline-2026-11-10', 'stage-b-baseline-key.json'),
            'stage-b': (ROOT / 'poc/data/clean-stage-b-reading-2026-11-12', 'stage-b-reading-key.json')}


def main():
    key_folder = Path(sys.argv[1])
    inventory = []
    for reading, (folder, key_name) in READINGS.items():
        key = json.loads((key_folder / key_name).read_text())
        first, third = {family: {} for family in FAMILIES}, {family: {} for family in FAMILIES}
        for family in FAMILIES:
            for answer_file in sorted((folder / 'readers-answers').glob(f'reader-{family}-packet-*.jsonl')):
                first[family].update(baseline_count.rows_in(answer_file)[0])
            for ruling_file in sorted((folder / 'third-reader').glob(f'rulings-{family}-*.jsonl')):
                third[family].update(baseline_count.rows_in(ruling_file)[0])
        own = baseline_count.rows_in(folder / 'own-read.jsonl')[0] if (folder / 'own-read.jsonl').exists() else {}
        stored = {int(number): entry for number, entry in key.items() if entry['kind'] == 'stored'}
        totals = collections.Counter()
        for number, entry in sorted(stored.items(), key=lambda pair: (pair[1]['draw'], pair[1]['view'], pair[1]['number_in_view'])):
            pair = [first[family][number]['verdict'] for family in FAMILIES]
            if pair[0] == pair[1]:
                settled = pair[0]
            else:
                rulings = [third[family][number]['verdict'] for family in FAMILIES]
                settled = rulings[0] if rulings[0] == rulings[1] else 'unresolved'
            totals[settled] += 1
            if pair == ['SUPPORTED', 'SUPPORTED']:
                continue
            inventory.append({'reading': reading, 'judgement': number, 'draw': entry['draw'], 'view': entry['view'], 'number_in_view': entry['number_in_view'],
                              'shape': entry.get('shape'), 'entry': {k: v for k, v in entry.items() if k not in ('packet',)},
                              'first': {family: {k: first[family][number].get(k) for k in ('verdict', 'rung_the_evidence_points_to', 'reasoning_flaw', 'why')} for family in FAMILIES},
                              'third': {family: {k: third[family][number].get(k) for k in ('verdict', 'why')} for family in FAMILIES if number in third[family]},
                              'settled': settled, 'own': own.get(number)})
        print(f"{reading}: {len(stored)} stored judgements; settled {dict(totals)}; not passed by both first readers: {sum(1 for row in inventory if row['reading'] == reading)}")
    (HERE / 'inventory-earlier-readings.json').write_text(json.dumps(inventory, indent=1, ensure_ascii=False) + '\n')
    by_path = collections.defaultdict(list)
    for row in inventory:
        by_path[(row['reading'], row['draw'], row['view'], row['shape'])].append(row)
    for (reading, draw, view, shape), rows in by_path.items():
        print(f"\n{reading} {draw} {view} ({shape}): {len(rows)} judgements not passed by both: " + ', '.join(f"#{r['number_in_view']} {r['settled']}" for r in rows))
        sample = rows[0]
        print('   key entry fields:', {k: str(v)[:80] for k, v in sample['entry'].items() if k not in ('kind', 'draw', 'view', 'number_in_view', 'shape')})
        for row in rows[:2]:
            for family in FAMILIES:
                print(f"   #{row['number_in_view']} {family}: {row['first'][family]['verdict']} | {str(row['first'][family]['why'])[:260]}")
            if row['own']:
                print(f"   #{row['number_in_view']} own read: {row['own'].get('verdict')} | {str(row['own'].get('why'))[:200]}")


if __name__ == '__main__':
    main()
