"""The split probe's verdict ($0; it judges nothing itself): DESIGN.md v4 §3's counts, then §0b item 4's reading rule with §0c item 3's
two countings.

Counts, from the two arms' outcomes:
- T, per topic: a send succeeds when it splits and both years write a ladder; the topic passes with at least 2 of 3; both must pass.
- C1, C2 and C3, per topic: it fails when any split send names the split case, or when the frozen step's 3 sends agree on their kind
  (ladder or not) and at least 2 of the split arm's 3 have another.
- M is reported.

The reading (reading_split.py's folder, the Stage A form plus `BY` and `LQ`, split-brief.md): each mark is settled from the two first
readers where they agree, else from the two third readers where they agree, else counted for the answer and then against it.
`BY` and `LQ` points go to the third readers when the first readers differ or either cannot tell, in
`third-reader/split-rulings-<family>-*.jsonl` lines {"id": "<item>-BY", "ruling": "yes"|"no"|"cannot_tell"}.
- Vetoes: on a yearly item of T or M, a hard-line mark (Q, O, R, L, N) failing, `BY` yes or `LQ` yes; on a split-arm C1 item, `BY`
  or `LQ` yes, or a hard-line mark failing that no frozen-arm item of the same topic fails.
- A plant not marked `yes` in its field by a first reader voids the reading; so does any missing or invalid row or ruling.

The verdict: negative when a count fails, whatever the reading (the counts do not depend on readers); void when the reading is void;
otherwise lead when no veto holds under either counting, negative when one holds under both, inconclusive when it holds under one.
Yearly items exist only in the split arm and carry `split`, so readers can tell those items' arm; the arm names are hidden, and C1
items of both arms are read alike.

  python3 score_split.py <probe data folder> <key folder>
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE), str(ROOT / 'clean-arch/step4-2026-11-10/stage_a')]
import probe_split  # noqa: E402   (first: it puts the ladder step's folder on the path)
import accounting  # noqa: E402
import build_reader_packets  # noqa: E402
from hivemind import universe  # noqa: E402
import collect_readings as collector  # noqa: E402
import ladder_split  # noqa: E402
import reading_split  # noqa: E402

FIELDS = ('BY', 'LQ')
FIELD_VALUES = ('yes', 'no', 'cannot_tell')
HARD = ('Q', 'O', 'R', 'L', 'N')
CONTROLS = ('C1', 'C2', 'C3')


def names_case(row):
    """Whether any answer the split arm's topic call got names the split case (a refused one included)."""
    for request in row['requests']:
        try:
            no_ladder = json.loads(request.get('answer_text') or 'null').get('no_ladder')
        except (ValueError, AttributeError):
            continue
        if isinstance(no_ladder, dict) and no_ladder.get('case') == ladder_split.SPLIT_CASE:
            return True
    return False


def kind(row):
    return {'ladder': 'ladder', 'split': 'split'}.get(row['status'], 'no ladder')


def counts(probe_folder):
    groups = reading_split.group_of()
    expected = {(topic, n) for topic in groups for n in probe_split.PASSES}
    sends = {}
    for arm in probe_split.ARMS:
        rows = reading_split.rows_of(Path(probe_folder) / arm)
        keys = [(row['case'].split('|', 1)[1], row['pass']) for row in rows]
        if len(keys) != len(set(keys)) or set(keys) != expected or any(not row['case'].startswith(f'{arm}|') for row in rows):
            raise SystemExit(f'NOT SCORED: the {arm} arm does not hold every topic and pass exactly once ({len(keys)} rows, '
                             f'{len(set(keys))} distinct, {len(expected)} expected)')
        sends[arm] = dict(zip(keys, rows))
    out = {'T': {}, 'controls': {}, 'M': {}}
    for topic, group in groups.items():
        split_rows = [sends['split'][(topic, n)] for n in probe_split.PASSES]
        if group == 'T':
            succeeded = [row['pass'] for row in split_rows if row['status'] == 'split' and len(row['children']) == 2
                         and all(child['status'] == 'ladder' for child in row['children'].values())]
            out['T'][topic] = {'sends succeeding': succeeded, 'passes': len(succeeded) >= 2}
        elif group in CONTROLS:
            frozen_kinds = [kind(sends['frozen'][(topic, n)]) for n in probe_split.PASSES]
            split_kinds = [kind(row) for row in split_rows]
            named = [row['pass'] for row in split_rows if names_case(row)]
            changed = len(set(frozen_kinds)) == 1 and sum(k != frozen_kinds[0] for k in split_kinds) >= 2
            out['controls'][topic] = {'group': group, 'frozen kinds': frozen_kinds, 'split kinds': split_kinds, 'sends naming the case': named,
                                      'kind changed': changed, 'kind rule exercised': len(set(frozen_kinds)) == 1, 'passes': not named and not changed}
        else:
            out['M'][topic] = [{'status': row['status'], 'years': {y: c['status'] for y, c in (row.get('children') or {}).items()}} for row in split_rows]
    out['pass'] = all(entry['passes'] for entry in out['T'].values()) and all(entry['passes'] for entry in out['controls'].values())
    return out


def field_rulings(reading):
    given = {}
    for family in collector.FAMILIES.values():
        for answer_file in sorted((Path(reading) / 'third-reader').glob(f'split-rulings-{family}-*.jsonl')):
            for line in answer_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith('```'):
                    continue
                try:
                    ruling = json.loads(line)
                    point, value = ruling['id'], ruling['ruling']
                except (ValueError, KeyError, TypeError):
                    raise SystemExit(f'VOID: {answer_file.name}: a line that is not a ruling: {line[:80]}')
                if value not in FIELD_VALUES or family in given.get(point, {}):
                    raise SystemExit(f'VOID: {answer_file.name}: {point} is ruled {value!r} or ruled twice by {family}')
                given.setdefault(point, {})[family] = value
    return given


def needs_ruling(first, second):
    return first != second or 'cannot_tell' in (first, second)


def field_points(outcomes, readers, item_of):
    return [(send, field) for send in outcomes if not send[0].startswith('plant|') for field in FIELDS
            if needs_ruling(readers['reader 1'][send][field], readers['reader 2'][send][field])]


def load_reading(probe_folder, reading, key_path, plants_path):
    """Everything the verdict reads; raises SystemExit('VOID: …') for an incomplete or invalid reading or a missed plant. The reading
    must hold exactly the items its sends give (reading_split.reading_rows), each once, and the key exactly those items."""
    derived_rows, derived_cases = reading_split.reading_rows(probe_folder)
    derived = sorted((row['case'], row['pass']) for row in derived_rows)
    held = sorted((row['case'], row['pass']) for row in collector.outcomes_of(reading))
    key = json.loads(Path(key_path).read_text())
    keyed = sorted(tuple(send) for send in key.values())
    if held != derived or keyed != derived:
        raise SystemExit(f'VOID: the reading holds {len(held)} items and the key {len(keyed)}, not exactly the {len(derived)} its sends give')
    same = lambda value: json.loads(json.dumps(value, ensure_ascii=False))
    rebuilt = {(row['case'], row['pass']): same(row) for row in derived_rows}
    if any(rebuilt[(row['case'], row['pass'])] != same(row) for row in collector.outcomes_of(reading)):
        raise SystemExit('VOID: an item of the reading differs in content from the send it was built from')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    shown_list = [item for packet in sorted((Path(reading) / 'readers').glob('packet-*.json')) for item in json.loads(packet.read_text())]
    if len(shown_list) != len({item['item'] for item in shown_list}) or len(shown_list) != len(key):
        raise SystemExit(f'VOID: the packets hold {len(shown_list)} items, {len({item["item"] for item in shown_list})} distinct, '
                         f'not each of the {len(key)} keyed items once')
    shown = {item['item']: item for item in shown_list}
    expected_items = {int(number): same({'item': int(number), **build_reader_packets.item_of(rebuilt[tuple(send)], derived_cases[send[0]], research_list),
                                         'split': rebuilt[tuple(send)]['split']}) for number, send in key.items()}
    if set(shown) != set(expected_items) or any(same(shown[number]) != item for number, item in expected_items.items()):
        raise SystemExit('VOID: a packet item differs from the item its send gives, or the packets do not hold every item once')
    if json.loads(Path(plants_path).read_text()) != reading_split.plants()[2]:
        raise SystemExit('VOID: the plants\' expected marks are not the ones reading_split.py builds')
    key, item_of, outcomes, readers, problems = collector.read_rows(reading, key_path)
    for reader in collector.FAMILIES:
        for send in outcomes:
            row = readers[reader].get(send)
            if row is not None and any(row.get(field) not in FIELD_VALUES for field in FIELDS):
                problems[reader]['rows'].append((item_of[send], send, f'BY and LQ are each one of {FIELD_VALUES}'))
    bad = {reader: found['rows'] or found['unreadable lines'] for reader, found in problems.items() if found['rows'] or found['unreadable lines']}
    if bad:
        raise SystemExit(f'VOID: rows missing or not valid: {bad}')
    expected = json.loads(Path(plants_path).read_text())
    if set(expected) != set(reading_split.PLANTS) or any((plant, 1) not in outcomes for plant in expected):
        raise SystemExit('VOID: the plants are not the ones reading_split.py builds')
    missed = [(plant, reader) for plant, entry in expected.items() for reader in collector.FAMILIES
              if readers[reader][(plant, 1)][entry['field']] != entry['expected']]
    if missed:
        raise SystemExit(f'VOID: a plant was missed: {missed}')
    both = sorted(collector.FAMILIES.values())
    families = collector.third_reader_families(reading)
    if collector.disputes_of(outcomes, readers) and families != both:
        raise SystemExit(f'VOID: differences need both third-reader families; found {families}')
    read = {family: collector.read_rulings(reading, item_of, outcomes, readers, family) for family in families}
    if any(found[1] for found in read.values()):
        raise SystemExit(f'VOID: third-reader rulings missing: { {family: found[1] for family, found in read.items() if found[1]} }')
    given = field_rulings(reading)
    missing = [f'{item_of[send]}-{field}' for send, field in field_points(outcomes, readers, item_of)
               if len(given.get(f'{item_of[send]}-{field}', {})) < 2]
    if missing:
        raise SystemExit(f'VOID: BY or LQ rulings missing for {missing}')
    return outcomes, readers, item_of, {family: found[0] for family, found in read.items()}, families, given


def settled_field(values, ruled, unresolved_as):
    if len(set(values)) == 1 and values[0] != 'cannot_tell':
        return values[0]
    third = set(ruled.values())
    if len(ruled) == 2 and len(third) == 1 and 'cannot_tell' not in third:
        return next(iter(third))
    return 'yes' if unresolved_as == 'fails' else 'no'


def faults_of(send, outcome, readers, of_family, families, given, item, unresolved_as):
    rows = [readers[reader][send] for reader in collector.FAMILIES]
    empty = {'marks': {}, 'W': {}}
    ruling, _ = accounting.rulings_of_two(of_family[families[0]].get(send, empty), of_family[families[-1]].get(send, empty), unresolved_as)
    faults = set()
    for mark in accounting.marks_that_apply(accounting.kind_of(outcome)):
        value = rows[0][mark] if rows[0][mark] == rows[1][mark] else ruling['marks'].get(mark, unresolved_as)
        if mark in HARD and value == 'fails':
            faults.add(mark)
    for field in FIELDS:
        if settled_field([rows[0][field], rows[1][field]], given.get(f'{item}-{field}', {}), unresolved_as) == 'yes':
            faults.add(field)
    return faults


def vetoes(outcomes, readers, item_of, of_family, families, given, unresolved_as):
    groups = reading_split.group_of()
    faults = {send: faults_of(send, outcome, readers, of_family, families, given, item_of[send], unresolved_as)
              for send, outcome in outcomes.items() if not send[0].startswith('plant|')}
    frozen_faults = {}
    for (case, _), found in faults.items():
        arm, topic = case.split('|', 1)
        if arm == 'frozen':
            frozen_faults.setdefault(topic, set()).update(found & set(HARD))
    found_vetoes = []
    for (case, pass_number), found in sorted(faults.items()):
        arm, topic = case.split('|', 1)
        topic = topic.split('@', 1)[0]
        if arm != 'split' or not found:
            continue
        if groups[topic] in reading_split.READ_YEARLY:
            found_vetoes.append((case, pass_number, sorted(found)))
        else:
            new = (found & set(FIELDS)) | (found & set(HARD)) - frozen_faults.get(topic, set())
            if new:
                found_vetoes.append((case, pass_number, sorted(new)))
    return found_vetoes


def verdict(probe_folder, key_folder):
    counted = counts(probe_folder)
    print(json.dumps(counted, indent=1))
    if not counted['pass']:
        return 'negative', counted, None
    try:
        loaded = load_reading(probe_folder, Path(probe_folder) / 'reading', Path(key_folder) / 'key.json', Path(key_folder) / 'plants-expected.json')
    except SystemExit as stop:
        if str(stop).startswith('VOID'):
            print(stop)
            return 'void', counted, None
        raise
    found = {unresolved_as: vetoes(*loaded, unresolved_as) for unresolved_as in ('holds', 'fails')}
    for unresolved_as, listed in found.items():
        print(f'vetoes, unresolved counted as {unresolved_as}: {listed}')
    if not found['holds'] and not found['fails']:
        return 'lead', counted, found
    if found['holds'] and found['fails']:
        return 'negative', counted, found
    return 'inconclusive', counted, found


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    decision, _, _ = verdict(sys.argv[1], sys.argv[2])
    print(f'VERDICT: {decision}')
