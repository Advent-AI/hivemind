"""The census matching packets of the full run (D452 gate 1; MATCHING-v2): each draw's opened questions under a neutral run name (r1..r6)
and neutral ids (t01..), so a reader cannot tell which system opened them; the key (neutral name and id → draw and original id) is
written to a path outside the repository. Checks ($0): every opened question of every draw appears exactly once in the packets and once in
the key; the key maps every packet row back to its original; an input with a duplicate id, or a draw named twice, is refused.

  python3 build_matching_packets.py <key path outside the repository> c1 c2 c3 p1 p2 p3
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                          # the sources (original labels): never shown to a reader
PACKETS = HERE.parent / 'full-matching'                         # the readers' folder: neutral packets only
MANIFEST = HERE.parents[1] / 'e2e-2026-11-09' / 'stage2-manifest.json'
SEED = 20261113


def build(draws, key_path):
    if len(set(draws)) != len(draws):
        raise SystemExit('a draw is named twice: refused')
    opened = {draw: json.loads((HERE / f'opened-{draw}.json').read_text()) for draw in draws}
    for draw, rows in opened.items():
        ids = [row['id'] for row in rows]
        if len(set(ids)) != len(ids) or any(row['run'] != draw for row in rows):
            raise SystemExit(f'{draw}: duplicate ids or rows of another run: refused')
    item_ids = json.loads(MANIFEST.read_text())['item_ids']
    for rows in opened.values():                                  # the clean extract gives a manifest position; production an input id
        for row in rows:
            if isinstance(row['article'], int):
                row['article'] = item_ids[row['article'] - 1]
    order = list(draws)
    random.Random(SEED).shuffle(order)
    key = {}
    for number, draw in enumerate(order, 1):
        run = f'r{number}'
        rows = []
        for index, row in enumerate(opened[draw], 1):
            neutral = f't{index:02d}'
            key[f'{run}/{neutral}'] = {'draw': draw, 'id': row['id']}
            rows.append({'run': run, 'id': neutral, 'article': row['article'], 'description': row['description'],
                         'outcome': row['outcome'], 'period': row['period']})
        (PACKETS / f'opened-{run}.json').write_text(json.dumps(rows, indent=1, ensure_ascii=False) + '\n')
    Path(key_path).write_text(json.dumps(key, indent=1) + '\n')
    # checks
    back = {(entry['draw'], entry['id']) for entry in key.values()}
    expected = {(draw, row['id']) for draw, rows in opened.items() for row in rows}
    packet_rows = [(run_file.stem.split('-')[1], row['id']) for run_file in sorted(PACKETS.glob('opened-r*.json'))
                   for row in json.loads(run_file.read_text())]
    if back != expected or len(key) != len(expected) or len(packet_rows) != len(expected) or \
            {f'{run}/{neutral}' for run, neutral in packet_rows} != set(key):
        raise SystemExit('check failed: the packets and the key do not hold every opened question exactly once')
    if any(not isinstance(json.loads(f.read_text())[0]['article'], str) for f in PACKETS.glob('opened-r*.json')):
        raise SystemExit('check failed: an article field is not an input id')
    print(f'{len(expected)} opened questions in {len(order)} neutral runs; key {key_path}; every one exactly once, every packet row keyed')


if __name__ == '__main__':
    build(sys.argv[2:], sys.argv[1])
