"""The third readers' H packet (DESIGN.md, "Reading"; h-third-reader-brief.md): every listed part of an arm's answer on which the two
first readers differ on H, or either cannot tell. Each point carries the item as the first readers saw it, the part, and the two
marks as "a" and "b", drawn per point from a fixed seed so a third reader cannot rule by family. Plants are not ruled (a missed
plant stops the reading instead).

  python3 h_disputes.py <reading folder> <key path>

Writes <reading folder>/third-reader/h-packet-1.json; refuses an existing one. Prints the number of points.
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / 'clean-arch/step4-2026-11-10/stage_a'), str(ROOT / 'src')]
import build_reader_packets  # noqa: E402
import probe_score  # noqa: E402
from hivemind import universe  # noqa: E402

SIDES_SEED = 20261116


def points(reading, key_path):
    _, item_of, outcomes, readers, _ = probe_score.collector.read_rows(reading, key_path)
    cases = {case['case']: case for case in json.loads((Path(reading) / 'cases.json').read_text())}
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    found = []
    for send, outcome in sorted(outcomes.items(), key=lambda pair: item_of.get(pair[0], 0)):
        if send[0].startswith('plant|') or probe_score.accounting.kind_of(outcome) == 'refused twice':
            continue
        for position in range(probe_score.parts_listed(outcome)):
            marks = [readers['reader 1'][send]['H'][position], readers['reader 2'][send]['H'][position]]
            if not probe_score.needs_ruling(*marks):
                continue
            point = f'{item_of[send]}-H-{position}'
            if random.Random(f'{SIDES_SEED}-{point}').random() < 0.5:
                marks.reverse()
            item = build_reader_packets.item_of(outcome, cases[send[0]], research_list)
            found.append({'id': point, 'item': item, 'part': outcome['answer']['ladder']['not_judged'][position],
                          'marks': {'a': marks[0], 'b': marks[1]}})
    return found


def main(reading, key_path):
    target = Path(reading) / 'third-reader' / 'h-packet-1.json'
    if target.exists():
        raise SystemExit(f'{target} exists: refused')
    found = points(reading, key_path)
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(found, indent=1, ensure_ascii=False) + '\n')
    print(f'{len(found)} H points to rule: {target}')
    return len(found)


if __name__ == '__main__':
    main(*sys.argv[1:])
