"""The paired exposed verification of the narrow D436 passage (deep council D653, rounds 1 to 5): astra on the frozen ladder request against
astra on the request with the audited passage (`edit.json`), on four targets astra declined against D436 (acc/clean-8, acc/clean-9 and
u3/clean-10, three of the six theses put to Alex before D436, and pool-17), six decline controls, and one share-centred control (u3/clean-11,
whose outcome tracks the share itself), read blind by both families with planted controls, and each written answer of the edited arm on a
target or on the share control reviewed against its source by two reviewers. Exposed: the 44's targets informed the edit; this verifies that the
step carries Alex's ruling, not general performance.

  python3 paired_probe.py check                         # $0: the requests, the one inserted passage, the shared cap; writes check-passed.json
  python3 paired_probe.py send <new run folder>         # frozen and edited interleaved: d1, d2 on all 11 topics; d3 on the 4 targets
  python3 paired_probe.py reading <run folder> <key folder>
  python3 paired_probe.py score <run folder> <key folder> <review codex rows> <review claude rows>

The rule, fixed before the send (council rounds 2 and 4):
- exercised: the frozen arm's own declines ("no ladder", not answers refused twice by code) are at least 5 of its 9 target sends and fall on
  at least 2 of the 3 targets; otherwise INCONCLUSIVE;
- PASS when all hold, otherwise FAIL (council round 5: strict throughout):
  - every edited target send (12) is a question with no hard-line fault marked by either family;
  - no edited target or share-control answer carries a material defect of kinds (i) to (iii) of `review-brief.md` marked by either reviewer;
  - every edited decline-control send (10) is a decline that neither family marks unjustified;
  - each edited share-control send does not ask the total (D654's check): a question with no kind (i) from either reviewer, or a decline,
    and no hard-line fault (N for a decline) marked by either family; asking either of u3/clean-11's two splits is allowed (council round 6);
  - no edited send is lost (refused twice by code), on any of the 26 edited sends, reported topics included (council round 6);
- u2/clean-10 is sent and reported, not deciding (its decline is defensible but ambiguous: council round 5);
- u3/clean-10 is sent in all three draws and reported, not deciding: the passage carries D654's three shapes in D654's words only, and
  whether "capacity added ... easing the shortage" falls under them is read differently by the two auditor families (audits v5.1 to v5.4);
- due-day defects (kind iv) are the separate D636 class: reported for both arms, not deciding; a pass is not a claim that the questions are
  sound production questions;
- a stopped draw or a missed planted control reads NOT MEASURED.
"""
import collections
import dataclasses
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE.parents[1] / 'reflection-6' / 'opus')]
import opus_probe as base  # noqa: E402   (the trial harness: run_arm, the planted controls, Stage A, the ladder step, the readers' tools)
from opus_probe import (accounting, budget, build_reader_packets, collector, ladder_step, model, probe_split, refcontrol,  # noqa: E402
                        stage_a)

ASTRA = dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')
EDIT = json.loads((HERE / 'edit.json').read_text())
ANCHOR, INSERTED = EDIT['anchor'], EDIT['insert']
MORE = EDIT.get('more', [])          # the same exception's pointers where the request restates the decline case
ARMS = ('frozen', 'edited')
ORDER = [('frozen', 1), ('edited', 1), ('frozen', 2), ('edited', 2), ('frozen', 3), ('edited', 3)]
TARGETS = ('acc/clean-8', 'acc/clean-9', 'pool-17')
CONTROLS = ('week-10-06:c1/clean-4', 'week-10-06:c1/clean-12', 'fortnight:c1/clean-8', 'pool-19', 'u1/clean-9')
REPORTED = ('u2/clean-10', 'u3/clean-10')
SHARE = ('u3/clean-11',)
WORKERS = 1
EXPECTED_SPEND = 1.20            # 26 sends an arm at up to about $0.045 a send (astra measured $0.033 to $0.047; D633-D649)
TOTAL_CAP = 3.60                 # one cap shared by both arms: in-flight room (~$1.19) plus both arms' expected spend; within Alex's remaining ~$4.34.
                                 # Priced from stored astra tokens on these topics (mean input 5,187, output 196): ~$2.15 with the system text
                                 # cached, ~$3.2 uncached; an estimate from means, not a bound. The first-request projection runs at edited d1
                                 # only; the shared limit applies to every draw, and a draw it stops reads NOT MEASURED.
RECORD = HERE / 'check-passed.json'
SELECTION = HERE.parents[1] / 'reflection-7' / 'fresh-selection.json'
HARD = refcontrol.HARD
SHUFFLE_SEED = 20261136
CODE_FILES = [Path(__file__), Path(base.__file__), SELECTION, HERE / 'edit.json', refcontrol.LADDER / 'ladder_step.py', refcontrol.LADDER / 'candidate-system.txt',
              refcontrol.LADDER / 'candidate-closing.txt', refcontrol.LADDER / 'candidate-schema.json', refcontrol.STAGE_A / 'stage_a.py']


FROZEN_TEXTS = stage_a.request_texts          # held here: `send` re-points stage_a.request_texts at an arm's texts during its draws


def frozen_texts():
    return FROZEN_TEXTS()


def edited_texts():
    texts = frozen_texts()
    if texts['system'].count(ANCHOR) != 1:
        raise SystemExit('the anchor sentence is not found once in the frozen system text')
    closing, schema = texts['closing'], json.loads(json.dumps(texts['schema']))
    for edit in MORE:
        if edit['where'] == 'closing':
            if closing.count(edit['anchor']) != 1:
                raise SystemExit('a closing anchor is not found once')
            closing = closing.replace(edit['anchor'], edit['anchor'] + edit['insert'])
        elif edit['where'] == 'schema_no_ladder':
            description = schema['properties']['no_ladder']['description']
            if description.count(edit['anchor']) != 1:
                raise SystemExit('the no_ladder anchor is not found once')
            schema['properties']['no_ladder']['description'] = description.replace(edit['anchor'], edit['anchor'] + edit['insert'])
        else:
            raise SystemExit(f"unknown place {edit['where']}")
    return dict(texts, system=texts['system'].replace(ANCHOR, ANCHOR + INSERTED), closing=closing, schema=schema)


TEXTS = {'frozen': frozen_texts, 'edited': edited_texts}


def population():
    """{name: case} for the 4 targets and 8 controls."""
    pool = json.loads(SELECTION.read_text())['pool']
    the_26 = {f'{source}:{name}': case for source, name, case, _ in refcontrol.population()}
    the_44 = {case['case']: case for case in json.loads((refcontrol.STAGE_A / 'cases.json').read_text())}
    out = {}
    for name in TARGETS + CONTROLS + REPORTED + SHARE:
        out[name] = pool[int(name.split('-')[1])]['case'] if name.startswith('pool-') else the_26.get(name) or the_44[name]
    if len(out) != 11:
        raise SystemExit(f'{len(out)} topics, not 11')
    return out


def topics_of(draw):
    return TARGETS + CONTROLS + REPORTED + SHARE if draw in (1, 2) else TARGETS + ('u3/clean-10',)


def built(case, arm, rl):
    texts = TEXTS[arm]()
    user = ladder_step.user_text(stage_a.payload_for(case, rl), texts['closing'])
    return model.build_request(ASTRA, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def code_digest():
    return hashlib.sha256(b''.join(path.read_bytes() for path in CODE_FILES)).hexdigest()


def check():
    rl = refcontrol.research_list()
    failures, shas = [], {arm: {} for arm in ARMS}
    for name, case in population().items():
        frozen, edited = built(case, 'frozen', rl), built(case, 'edited', rl)
        sent_frozen, sent_edited = json.dumps(frozen), json.dumps(edited)      # the transport's serialization
        expected, only_insert = sent_frozen, True
        for anchor_text, insert_text in [(ANCHOR, INSERTED)] + [(edit['anchor'], edit['insert']) for edit in MORE]:
            anchor = json.dumps(anchor_text)[1:-1]
            only_insert = only_insert and expected.count(anchor) == 1
            expected = expected.replace(anchor, anchor + json.dumps(insert_text)[1:-1])
        only_insert = only_insert and sent_edited == expected
        if not only_insert or frozen['model'] != 'gpt-6-astra':
            failures.append(name)
        for arm, request in (('frozen', frozen), ('edited', edited)):
            shas[arm][name] = model.request_identity(request)[1]
    room = WORKERS * max(budget.worst_cost(built(case, 'edited', rl)) for case in population().values())
    print(f'11 topics: each edited request is the frozen astra request with only the audited passage and its {len(MORE)} pointers inserted: {not failures}')
    print(f'shared cap ${TOTAL_CAP:.2f}; in-flight room ${room:.3f}; expected spend ${2 * EXPECTED_SPEND:.2f} for both arms')
    if TOTAL_CAP < room + 2 * EXPECTED_SPEND:
        failures.append('the shared cap is below the room plus both arms\' expected spend')
    if failures:
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'code_sha256': code_digest(), 'requests': shas}, indent=1) + '\n')
    print('check passed')


def send(folder, *, transport=None):
    record = json.loads(RECORD.read_text()) if RECORD.exists() else None
    if record is None or record['code_sha256'] != code_digest():
        raise SystemExit('no check record for these files: run `check` first')
    rl = refcontrol.research_list()
    topics = population()
    for arm in ARMS:
        if {name: model.request_identity(built(case, arm, rl))[1] for name, case in topics.items()} != record['requests'][arm]:
            raise SystemExit('REFUSED: the requests differ from the checked record')
    folder = Path(folder)
    guard = probe_split.BreachGuard(transport or (lambda provider, request: model.openai_transport(provider, request, max_attempts=1)))
    room = WORKERS * max(budget.worst_cost(built(case, 'edited', rl)) for case in topics.values())
    spent = collections.Counter()
    original = stage_a.request_texts
    try:
        for arm, draw in ORDER:
            stage_a.request_texts = TEXTS[arm]          # base.run_arm reads the step's texts from Stage A for every call
            cases = [dict(topics[name], case=f'{arm}-d{draw}|{name}') for name in topics_of(draw)]
            written, limit = base.run_arm(cases, folder / f'{arm}-d{draw}', TOTAL_CAP - sum(spent.values()), ASTRA, rl, transport=guard,
                                          workers=WORKERS, first_alone=(arm, draw) == ('edited', 1), room=room)
            known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            spent[arm] += known + in_full
            print(f'{arm} d{draw}: {len(written)} of {len(cases)} written; spent ${known + in_full:.4f}', flush=True)
            if guard.breaches or limit.stopped or len(written) != len(cases):
                raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or guard.breaches}. NOT MEASURED.')
    finally:
        stage_a.request_texts = original
    print(f'spent {dict(spent)}')


def reading(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    rl = refcontrol.research_list()
    topics = population()
    rows, cases, expected = [], {}, {}
    for arm, draw in ORDER:
        for row in map(json.loads, (run_folder / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()):
            if row['status'] in ('ladder', 'no ladder'):
                rows.append(row)
                cases[row['case']] = dict(topics[row['case'].split('|', 1)[1]], case=row['case'])
    for row, case, marks in base.controls():
        rows.append(row)
        cases[row['case']] = dict(case, case=row['case'])
        expected[row['case']] = marks
    folder = run_folder / 'reading'
    (folder / 'readers').mkdir(parents=True)
    order = sorted(rows, key=lambda row: row['case'])
    random.Random(SHUFFLE_SEED).shuffle(order)
    key, packets = {}, []
    for number, row in enumerate(order, start=1):
        key[str(number)] = [row['case'], 1]
        if (number - 1) % build_reader_packets.ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(row, cases[row['case']], rl)})
    (folder / 'send-1').mkdir()
    (folder / 'send-1' / 'outcomes.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    for number, packet in enumerate(packets, start=1):
        (folder / 'readers' / f'packet-{number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'controls-expected.json').write_text(json.dumps(expected, indent=1) + '\n')
    review_rows = [row for row in rows if row['case'].split('|', 1)[0].startswith('edited') and row['status'] == 'ladder'
                   and row['case'].split('|', 1)[1] in TARGETS + SHARE + ('u3/clean-10',)]
    review_rows += [row for row in rows if row['case'].split('|', 1)[0].startswith('frozen') and row['status'] == 'ladder'
                    and row['case'].split('|', 1)[1] in TARGETS + SHARE + ('u3/clean-10',)]           # the frozen arm's written answers, mixed in so the reviewer cannot tell arms
    random.Random(SHUFFLE_SEED + 1).shuffle(review_rows)
    review_key, review_items = {}, []
    for number, row in enumerate(review_rows, start=1):
        review_key[str(number)] = row['case']
        review_items.append({'item': number, **build_reader_packets.item_of(row, cases[row['case']], rl)})
    (folder / 'review').mkdir()
    (folder / 'review' / 'packet.json').write_text(json.dumps(review_items, indent=1, ensure_ascii=False) + '\n')
    (key_folder / 'review-key.json').write_text(json.dumps(review_key, indent=1) + '\n')
    print(f'{len(rows)} items in {len(packets)} packets; {len(review_items)} answers for the source review')


def score(run_folder, key_folder, review_codex, review_claude):
    folder = Path(run_folder) / 'reading'
    key, item_of, outcomes, readers, problems = collector.read_rows(folder, Path(key_folder) / 'key.json')
    if any(found['rows'] or found['unreadable lines'] for found in problems.values()):
        raise SystemExit(f'NOT MEASURED: rows missing or not valid: {problems}')
    for control, marks in json.loads((Path(key_folder) / 'controls-expected.json').read_text()).items():
        for mark, value in marks.items():
            if mark != 'all' and any(readers[reader][(control, 1)][mark] != value for reader in collector.FAMILIES):
                raise SystemExit(f'NOT MEASURED: a family missed the planted {control} ({mark})')
    review_key = json.loads((Path(key_folder) / 'review-key.json').read_text())
    reviews = {}
    for family, path in (('codex', review_codex), ('claude', review_claude)):
        rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        if sorted(row['item'] for row in rows) != list(range(1, len(review_key) + 1)):
            raise SystemExit(f'NOT MEASURED: the {family} review does not hold each of the {len(review_key)} answers once')
        for row in rows:
            defects = row.get('defects')
            if not isinstance(defects, list) or any(kind not in ('i', 'ii', 'iii', 'iv') for kind in defects):
                raise SystemExit(f'NOT MEASURED: the {family} review row {row.get("item")} has no valid defects list')
            reviews.setdefault(review_key[str(row['item'])], {})[family] = set(defects)
    sends = {}
    for arm, draw in ORDER:
        for row in map(json.loads, (Path(run_folder) / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()):
            sends[row['case']] = row

    def faults(send_name, row):
        if row['status'] == 'no ladder: refused':
            return {'agreed': True, 'strict': True, 'marks': ['refused twice']}
        marks = [readers[reader][(send_name, 1)] for reader in collector.FAMILIES]
        applying = [mark for mark in accounting.marks_that_apply(accounting.kind_of(outcomes[(send_name, 1)])) if mark in HARD]
        failing = sorted({mark for mark in applying for m in marks if m.get(mark) == 'fails'})
        return {'agreed': any(all(m.get(mark) == 'fails' for m in marks) for mark in applying), 'strict': bool(failing), 'marks': failing}
    table = collections.defaultdict(dict)
    for send_name, row in sends.items():
        arm_draw, topic = send_name.split('|', 1)
        table[topic][arm_draw] = (row['status'], faults(send_name, row))
    declines = {t: sum(table[t][f'frozen-d{d}'][0] == 'no ladder' for d in (1, 2, 3)) for t in TARGETS}
    material = {name: sorted(set.union(*[by_family.get(f, set()) for f in ('codex', 'claude')]) & {'i', 'ii', 'iii'})
                for name, by_family in reviews.items()}          # strict: marked by either reviewer
    material_agreed = {name: sorted(set.intersection(*[by_family.get(f, set()) for f in ('codex', 'claude')]) & {'i', 'ii', 'iii'})
                       for name, by_family in reviews.items()}
    due_day = {name: sorted({f for f, kinds in by_family.items() if 'iv' in kinds}) for name, by_family in reviews.items()}
    edited_targets_ok = {t: [table[t][f'edited-d{d}'][0] == 'ladder' and not table[t][f'edited-d{d}'][1]['strict']
                             and not material.get(f'edited-d{d}|{t}') for d in (1, 2, 3)] for t in TARGETS}
    edited_controls_ok = {t: [table[t][f'edited-d{d}'][0] == 'no ladder' and not table[t][f'edited-d{d}'][1]['strict'] for d in (1, 2)] for t in CONTROLS}
    edited_share_ok = {t: [not table[t][f'edited-d{d}'][1]['strict']                      # a lost answer is strict too
                           and (table[t][f'edited-d{d}'][0] == 'no ladder'                # a decline neither family marks unjustified
                                or 'i' not in material.get(f'edited-d{d}|{t}', []))       # or a question that does not ask the total
                           for d in (1, 2)] for t in SHARE}                               # D654: it checks only that the total is not asked
    lost_edited = sorted(name for name, row in sends.items() if name.startswith('edited') and row['status'] == 'no ladder: refused')
    print(json.dumps({'frozen declines per target (of 3)': declines, 'edited targets sound': edited_targets_ok,
                      'edited controls held': edited_controls_ok, 'edited share control sound': edited_share_ok, 'edited sends lost': lost_edited,
                      'material defects (i-iii), either reviewer': {k: v for k, v in material.items() if v},
                      'material defects (i-iii), both reviewers': {k: v for k, v in material_agreed.items() if v},
                      'reported, not deciding': {t: {ad: [st, f['strict'], material.get(f'{ad}|{t}', [])] for ad, (st, f) in sorted(table[t].items())} for t in REPORTED},
                      'due-day defects (iv), reported only': {k: v for k, v in due_day.items() if v},
                      'per topic [status, agreed, strict, marks]': {t: {ad: [st, f['agreed'], f['strict'], f['marks']] for ad, (st, f) in sorted(v.items())}
                                                                    for t, v in sorted(table.items())}}, indent=1))
    if lost_edited:
        verdict = f'FAIL: edited answers lost (refused twice by code): {lost_edited}'
    elif sum(declines.values()) < 5 or sum(count > 0 for count in declines.values()) < 2:
        verdict = f'INCONCLUSIVE: the frozen arm declines {sum(declines.values())} target sends on {sum(c > 0 for c in declines.values())} targets'
    elif all(all(v) for group in (edited_targets_ok, edited_controls_ok, edited_share_ok) for v in group.values()):
        verdict = 'PASS'
    else:
        verdict = 'FAIL'
    print(f'VERDICT: {verdict}')
    return verdict


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'check':
        check()
    elif command == 'send':
        send(sys.argv[2])
    elif command == 'reading':
        reading(*sys.argv[2:4])
    elif command == 'score':
        score(*sys.argv[2:6])
    else:
        sys.exit(__doc__)
