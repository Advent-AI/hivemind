"""The H-only diagnostic (council round 33): every written question of both arms of the astra-with-A2 run, read blind for its listed
parts alone (`unlisted-parts/h-brief.md`), with four controls, by one fresh reader of each family. A separate diagnostic: it never
turns the voided gate reading into a pass.

  python3 h_reading.py prep <run folder> <key folder>       # writes <run folder>/h-reading/packet.json and the key outside the repo
  python3 h_reading.py score <run folder> <key folder> <codex rows> <claude rows>

The rule, fixed before the reading:
- VOID if either reader misses any entry of any control.
- Harmful listings are entries marked `already_judged` or `settlement`, counted agreed (both readers) and either (one reader).
- "within the bound" when A2's count is at most the frozen arm's + 1 in both countings; "exceeds the bound" when it is above it in
  both; otherwise "inconclusive".
"""
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import a2_probe  # noqa: E402
from a2_probe import build_reader_packets, refcontrol  # noqa: E402

H_VALUES, HARM = a2_probe.H_VALUES, a2_probe.H_HARM
SEED = 20261131
STORE = a2_probe.ROOT / 'poc' / 'data' / 'clean-dueday-probe-2026-11-16' / 'v2-d1' / 'outcomes.jsonl'


def stored(topic):
    row = next(json.loads(line) for line in STORE.read_text().splitlines() if json.loads(line)['case'].endswith('|' + topic))
    if row['status'] != 'ladder':
        raise SystemExit(f'the stored control question for {topic} is not a written question')
    return json.loads(json.dumps(row))


def controls():
    """{control: (row, case, expected H)}: the gate reading's planted listing control, a sound two-part question, a planted
    already-decided outcome on another event, and a planted settlement route on a figure."""
    cases = {f'{s}:{n}': c for s, n, c, _ in refcontrol.population()}
    out = {}
    row, case, marks = a2_probe.listing_control()
    out['control|listings'] = (row, case, marks['H'])
    sound = stored('week-10-06:c1/clean-5')
    out['control|sound-parts'] = (dict(sound, case='control|sound-parts'), cases['week-10-06:c1/clean-5'], ['part', 'part'])
    for topic, name, planted, expected in (
            ('fortnight:c1/clean-12', 'control|planted-outcome', 'The guarantee never becoming final by the check date.', 'already_judged'),
            ('fortnight:c1/clean-2', 'control|planted-route', "NVIDIA's FY2027 Form 10-K note in which the amount will be disclosed.", 'settlement')):
        row = stored(topic)
        listed = len(row['answer']['ladder']['not_judged'])
        row['answer']['ladder']['not_judged'] = row['answer']['ladder']['not_judged'] + [{'part': planted, 'why': 'listed for the reading'}]
        out[name] = (dict(row, case=name), cases[topic], [None] * listed + [expected])   # None: the stored entries are not judged here
    return out


def prep(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(a2_probe.ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    cases = {f'{s}:{n}': c for s, n, c, _ in refcontrol.population()}
    rows = {send: (row, cases[send.split('|', 1)[1]]) for send, row in a2_probe.readable(run_folder).items()
            if row['status'] == 'ladder' and row['answer']['ladder']['not_judged']}
    built = controls()
    rows.update({name: (row, case) for name, (row, case, _) in built.items()})
    order = sorted(rows)
    random.Random(SEED).shuffle(order)
    rl = refcontrol.research_list()
    items, key = [], {}
    for number, send in enumerate(order, start=1):
        key[str(number)] = send
        items.append({'item': number, **build_reader_packets.item_of(rows[send][0], rows[send][1], rl)})
    folder = run_folder / 'h-reading'
    folder.mkdir(exist_ok=False)
    (folder / 'packet.json').write_text(json.dumps(items, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'controls-expected.json').write_text(json.dumps({name: expected for name, (_, _, expected) in built.items()}, indent=1) + '\n')
    print(f'{len(items)} items ({len(built)} controls)')


def score(run_folder, key_folder, codex_rows, claude_rows):
    key = json.loads((Path(key_folder) / 'key.json').read_text())
    expected = json.loads((Path(key_folder) / 'controls-expected.json').read_text())
    packet = {item['item']: item for item in json.loads((Path(run_folder) / 'h-reading' / 'packet.json').read_text())}
    marks = {}
    for reader, path in (('codex', codex_rows), ('claude', claude_rows)):
        rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        if sorted(row.get('item') for row in rows) != list(range(1, len(key) + 1)):
            raise SystemExit(f'NOT SCORED: {reader} does not hold each of the {len(key)} items once')
        for row in rows:
            listed = len(packet[row['item']]['other_fields']['not_judged'])
            if not isinstance(row.get('H'), list) or len(row['H']) != listed or any(value not in H_VALUES for value in row['H']):
                raise SystemExit(f'NOT SCORED: {reader} item {row["item"]} has no valid H list of {listed}')
            send = key[str(row['item'])]
            if send in expected and any(want is not None and got != want for want, got in zip(expected[send], row['H'])):
                raise SystemExit(f'VOID: {reader} misses the {send}')
            marks.setdefault(send, {})[reader] = row['H']
    counts = {}
    for counting, rule in (('agreed', all), ('either', any)):
        counts[counting] = {arm: 0 for arm in a2_probe.ARMS}
        for send, by_reader in marks.items():
            if send in expected:
                continue
            arm = send.split('-d')[0]
            counts[counting][arm] += sum(rule(value in HARM for value in pair) for pair in zip(by_reader['codex'], by_reader['claude']))
    within = {counting: counts[counting]['a2'] <= counts[counting]['frozen'] + 1 for counting in counts}
    verdict = 'within the bound' if all(within.values()) else 'exceeds the bound' if not any(within.values()) else 'inconclusive'
    print(f'harmful listings {counts}')
    print(f'VERDICT: {verdict}')
    return verdict, counts


if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == 'prep':
        prep(*sys.argv[2:4])
    elif len(sys.argv) == 6 and sys.argv[1] == 'score':
        score(*sys.argv[2:6])
    else:
        sys.exit(__doc__)
