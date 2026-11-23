"""The complementary Astra screen (council round 15): the same launcher, checks and verdict as `astra_probe.py`, on the 14 topics the
first screen's seeded draw left out, with fresh sol and astra arms, three interleaved draws each, read blind together.

  python3 astra_rest.py check                          # $0: the complement, requests, controls, spend; writes check-passed-rest.json
  python3 astra_rest.py send <new run folder>
  python3 astra_rest.py reading <run folder> <key folder>
  python3 astra_rest.py score <run folder> <key folder>
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import astra_probe as base  # noqa: E402
import refcontrol  # noqa: E402

FIRST_SIZE, FIRST_SEED = 12, 20261123                # the first screen's draw (D632), fixed here, not read from the launcher
FIRST_RUN = base.ROOT / 'poc' / 'data' / 'clean-astra-screen-2026-11-16' / 'sol-d1' / 'outcomes.jsonl'


def first_sample():
    """The first screen's 12 topics, drawn again by its own seed and size, and checked against the topics its run sent."""
    population = refcontrol.population()
    names = sorted(f'{source}:{name}' for source, name, _, _ in population)
    chosen = set(random.Random(FIRST_SEED).sample(names, FIRST_SIZE))
    if FIRST_RUN.exists():
        sent = {json.loads(line)['case'].split('|', 1)[1] for line in FIRST_RUN.read_text().splitlines()}
        if sent != chosen:
            raise SystemExit('the first screen sent other topics than its seed draws: the complement is not defined')
    return [entry for entry in population if f'{entry[0]}:{entry[1]}' in chosen]


def complement():
    """The 26 topics less the first screen's 12: (source, name, case, stored)."""
    first = {f'{source}:{name}' for source, name, _, _ in first_sample()}
    rest = [entry for entry in refcontrol.population() if f'{entry[0]}:{entry[1]}' not in first]
    if len(first) != FIRST_SIZE or len(rest) != 14:
        raise SystemExit(f'the complement is not 14 of 26: first {len(first)}, rest {len(rest)}')
    return rest


base.sample = complement
base.SAMPLE_SIZE = 14
base.CAPS = {'sol': 1.20, 'astra': 5.00}       # $6.20 in all; about $7.45 remains of D439's $40
base.SHUFFLE_SEED = 20261124
base.RECORD = HERE / 'check-passed-rest.json'
base.CODE_FILES = base.CODE_FILES + [Path(__file__)]

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'check':
        base.check()
    elif command == 'send':
        base.send(sys.argv[2])
    elif command == 'reading':
        base.reading(*sys.argv[2:4])
    elif command == 'score':
        base.score(*sys.argv[2:4])
    else:
        sys.exit(__doc__)
