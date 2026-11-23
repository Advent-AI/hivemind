"""Tally of the pair marks: Claude's own read (written first) beside the blind readers' ($0; D536).

  python3 tally_pairs.py
"""
import collections
import json
from pathlib import Path

HERE = Path(__file__).parent


def load(path):
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip().startswith('{')]
    return {(row['new'], row['other']): row for row in rows}


def main():
    pairs = json.loads((HERE / 'pairs.json').read_text())['pairs']
    order = [(pair['new'], pair['other']) for pair in pairs]
    recorded = {(pair['new'], pair['other']): pair for pair in pairs}
    readers = {'own': {(row['new'], row['other']): row for row in json.loads((HERE / 'own-read-before-readers.json').read_text())}}
    for name in ('codex', 'claude'):
        if (HERE / f'{name}-reader.jsonl').exists():
            readers[name] = load(HERE / f'{name}-reader.jsonl')
    for name, marks in readers.items():
        missing = [key for key in order if key not in marks]
        print(f"{name}: {len(marks)} marks, missing {len(missing)}; " + str(dict(collections.Counter(row['mark'] for row in marks.values()))))
    names = list(readers)
    blind = [name for name in names if name != 'own']
    print()
    for key in order:
        marks = [readers[name].get(key, {}).get('mark', '-') for name in names]
        if set(marks) != {'none'}:
            strength = [readers[name].get(key, {}).get('strength', '') or '' for name in names]
            engine = recorded[key]
            print(f"{key[0]:>3} <- {key[1]:<3} | " + ' | '.join(f"{name} {mark}{'/' + s if s else ''}" for name, mark, s in zip(names, marks, strength))
                  + f" | engine: {engine['matching_engine_relation']} {engine['matching_engine_probability']}" + (' (same article)' if engine['how_permitted'].startswith('opened') else ''))
    wants = lambda mark: mark in ('relies', 'mutual')
    both = [key for key in order if blind and all(wants(readers[name].get(key, {}).get('mark')) for name in blind)]
    either = [key for key in order if any(wants(readers[name].get(key, {}).get('mark')) for name in blind)]
    print(f"\nthe new question would want the other's conclusion: both blind readers {len(both)} {both}; at least one {len(either)}; own read {[key for key in order if wants(readers['own'][key]['mark'])]}")
    backwards = [key for key in order if blind and all(readers[name].get(key, {}).get('mark') in ('reverse', 'mutual') for name in blind)]
    print(f"the other question would want the new one's conclusion (both blind readers): {len(backwards)} {backwards}")
    same = [key for key in order if blind and all(readers[name].get(key, {}).get('mark') == 'same' for name in blind)]
    print(f"the same question twice or another period of it (both blind readers): {len(same)} {same}")
    agree = sum(1 for key in order if len({readers[name].get(key, {}).get('mark') for name in blind}) == 1) if len(blind) == 2 else None
    print(f"the two blind readers give the same mark on {agree} of {len(order)} pairs")
    (HERE / 'tally.json').write_text(json.dumps({'both_blind_readers_want': both, 'at_least_one_wants': either, 'both_say_reverse_or_mutual': backwards, 'both_say_same': same, 'same_mark': agree, 'pairs': len(order)}, indent=1) + '\n')


if __name__ == '__main__':
    main()
