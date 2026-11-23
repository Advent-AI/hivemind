"""The second-side diagnostic (council rounds 40 to 42, D651): astra on the frozen ladder request against astra on the same request with D436's
two sentences, on 11 topics outside the 44 (6 targets with a main figure or event plus a second side, 5 decline controls), 2 fresh
draws per arm, read blind by both families with planted controls.

  python3 second_side_probe.py check                          # $0: the requests, the one inserted passage, the caps; writes check-passed.json
  python3 second_side_probe.py send <new run folder>          # frozen d1, edited d1, frozen d2, edited d2
  python3 second_side_probe.py reading <run folder> <key folder>
  python3 second_side_probe.py score <run folder> <key folder> <classification codex> <classification claude> <classification key>

The rule, fixed before the send (round 42, with round 42's three corrections):
- counted targets and controls: the topics both blind classifiers call "write" and "decline", before any answer is seen;
- exercised: a counted target the frozen arm declines in at least one of its 2 draws; fewer than 3 exercised reads INCONCLUSIVE;
- a recovery: both edited sends of an exercised target are questions with no hard-line fault marked by either family;
- PASS when at least 80% of the exercised targets recover, every counted control is declined in both edited sends with no family marking
  the decline unjustified, and on no counted topic does the edited arm have more failed sends than the frozen arm under either counting
  (hard-line faults plus sends refused twice by code); otherwise FAIL. A stopped draw or a missed planted control reads NOT MEASURED.
"""
import collections
import dataclasses
import hashlib
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path[:0] = [str(HERE.parent / 'reflection-6' / 'opus')]
import opus_probe as base  # noqa: E402   (the trial harness: run_arm, the planted controls, Stage A, the ladder step, the readers' tools)
from opus_probe import (accounting, budget, build_reader_packets, collector, ladder_step, model, probe_split, refcontrol,  # noqa: E402
                        stage_a)

ASTRA = dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')
ANCHOR = "in not_judged, each with one sentence on why it is not the one tracked."
INSERTED = (" A second side of the same bet stays in the one question as context: list it in not_judged. A second side is not by itself a"
            " reason to decline; decline only when no part is the main one, or when the main part itself meets a case below.")
ARMS = ('frozen', 'edited')
ORDER = [('frozen', 1), ('edited', 1), ('frozen', 2), ('edited', 2)]
WORKERS = 1
EXPECTED_SPEND = 1.10            # 22 sends an arm at up to $0.05 a send (astra measured $0.033 to $0.047; D633-D649), plus retries
CAPS = {'frozen': 2.60, 'edited': 2.60}
RECORD = HERE / 'check-passed.json'
SELECTION = HERE / 'fresh-selection.json'
TOPICS = HERE / 'topics-11.json'
HARD = refcontrol.HARD
SHUFFLE_SEED = 20261135
CODE_FILES = [Path(__file__), Path(base.__file__), SELECTION, TOPICS, refcontrol.LADDER / 'ladder_step.py', refcontrol.LADDER / 'candidate-system.txt',
              refcontrol.LADDER / 'candidate-closing.txt', refcontrol.LADDER / 'candidate-schema.json', refcontrol.STAGE_A / 'stage_a.py']


FROZEN_TEXTS = stage_a.request_texts          # held here: `send` re-points stage_a.request_texts at an arm's texts during its draws


def frozen_texts():
    return FROZEN_TEXTS()


def edited_texts():
    texts = frozen_texts()
    if texts['system'].count(ANCHOR) != 1:
        raise SystemExit('the anchor sentence is not found once in the frozen system text')
    return dict(texts, system=texts['system'].replace(ANCHOR, ANCHOR + INSERTED))


TEXTS = {'frozen': frozen_texts, 'edited': edited_texts}


def population():
    """[(name, case)] for the 11 topics, in topics-11.json's order; refuses any topic among the 44."""
    pool = json.loads(SELECTION.read_text())['pool']
    the_26 = {f'{source}:{name}': case for source, name, case, _ in refcontrol.population()}
    the_44 = {case['thesis']['description'] for case in json.loads((refcontrol.STAGE_A / 'cases.json').read_text())}
    out = []
    for topic in json.loads(TOPICS.read_text()):
        case = pool[topic['id']]['case'] if topic['set'] == 'pool' else the_26[topic['id']]
        name = f"pool-{topic['id']}" if topic['set'] == 'pool' else topic['id']
        if case['thesis']['description'] in the_44:
            raise SystemExit(f'{name} is among the 44 (D426)')
        out.append((name, case))
    if len(out) != 11:
        raise SystemExit(f'{len(out)} topics, not 11')
    return out


def built(case, arm, rl):
    texts = TEXTS[arm]()
    user = ladder_step.user_text(stage_a.payload_for(case, rl), texts['closing'])
    return model.build_request(ASTRA, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def code_digest():
    return hashlib.sha256(b''.join(path.read_bytes() for path in CODE_FILES)).hexdigest()


def check():
    rl = refcontrol.research_list()
    failures, shas = [], {arm: {} for arm in ARMS}
    for name, case in population():
        frozen, edited = built(case, 'frozen', rl), built(case, 'edited', rl)
        sent_frozen, sent_edited = json.dumps(frozen), json.dumps(edited)      # the transport's serialization
        anchor = json.dumps(ANCHOR)[1:-1]
        only_insert = sent_frozen.count(anchor) == 1 and sent_edited == sent_frozen.replace(anchor, anchor + json.dumps(INSERTED)[1:-1])
        if not only_insert or frozen['model'] != 'gpt-6-astra':
            failures.append(name)
        for arm, request in (('frozen', frozen), ('edited', edited)):
            shas[arm][name] = model.request_identity(request)[1]
    room = WORKERS * max(budget.worst_cost(built(case, 'edited', rl)) for _, case in population())
    print(f'11 topics: each edited request is the frozen astra request with only the two sentences inserted: {not failures}')
    for arm in ARMS:
        print(f'{arm}: cap ${CAPS[arm]:.2f}; in-flight room ${room:.3f}; expected spend ${EXPECTED_SPEND:.2f}')
        if CAPS[arm] < room + EXPECTED_SPEND:
            failures.append(f'{arm} cap below room plus expected spend')
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
        if {name: model.request_identity(built(case, arm, rl))[1] for name, case in topics} != record['requests'][arm]:
            raise SystemExit('REFUSED: the requests differ from the checked record')
    folder = Path(folder)
    guard = probe_split.BreachGuard(transport or (lambda provider, request: model.openai_transport(provider, request, max_attempts=1)))
    room = WORKERS * max(budget.worst_cost(built(case, 'edited', rl)) for _, case in topics)
    spent = collections.Counter()
    original = stage_a.request_texts
    try:
        for arm, draw in ORDER:
            stage_a.request_texts = TEXTS[arm]          # base.run_arm reads the step's texts from Stage A for every call
            cases = [dict(case, case=f'{arm}-d{draw}|{name}') for name, case in topics]
            written, limit = base.run_arm(cases, folder / f'{arm}-d{draw}', CAPS[arm] - spent[arm], ASTRA, rl, transport=guard,
                                          workers=WORKERS, first_alone=(arm, draw) == ('edited', 1), room=room)
            known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            spent[arm] += known + in_full
            print(f'{arm} d{draw}: {len(written)} of 11 written; spent ${known + in_full:.4f}', flush=True)
            if guard.breaches or limit.stopped or len(written) != 11:
                raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or guard.breaches}. NOT MEASURED.')
    finally:
        stage_a.request_texts = original
    print(f'spent {dict(spent)}')


def reading(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    rl = refcontrol.research_list()
    topics = dict(population())
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
    print(f'{len(rows)} items in {len(packets)} packets')


def counted(codex_file, claude_file, classification_key):
    """(targets, controls): topic names both blind classifiers call write, and decline."""
    key = json.loads(Path(classification_key).read_text())
    calls = {}
    for path in (codex_file, claude_file):
        for row in (json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()):
            topic = key[str(row['item'])]
            name = f"pool-{topic['id']}" if topic['set'] == 'pool' else topic['id']
            calls.setdefault(name, []).append(row['call'])
    if any(len(both) != 2 for both in calls.values()) or len(calls) != 11:
        raise SystemExit(f'NOT SCORED: the classifications do not hold each topic once per classifier: {calls}')
    return ({name for name, both in calls.items() if both == ['write', 'write']},
            {name for name, both in calls.items() if both == ['decline', 'decline']}, calls)


def score(run_folder, key_folder, codex_file, claude_file, classification_key):
    targets, controls_counted, calls = counted(codex_file, claude_file, classification_key)
    folder = Path(run_folder) / 'reading'
    key, item_of, outcomes, readers, problems = collector.read_rows(folder, Path(key_folder) / 'key.json')
    if any(found['rows'] or found['unreadable lines'] for found in problems.values()):
        raise SystemExit(f'NOT MEASURED: rows missing or not valid: {problems}')
    for control, marks in json.loads((Path(key_folder) / 'controls-expected.json').read_text()).items():
        for mark, value in marks.items():
            if mark != 'all' and any(readers[reader][(control, 1)][mark] != value for reader in collector.FAMILIES):
                raise SystemExit(f'NOT MEASURED: a family missed the planted {control} ({mark})')
    sends = {}
    for arm, draw in ORDER:
        for row in map(json.loads, (Path(run_folder) / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()):
            sends[row['case']] = row
    faults = {}                                                      # send -> {'agreed': bool, 'strict': bool}
    for send_name, row in sends.items():
        if row['status'] == 'no ladder: refused':
            faults[send_name] = {'agreed': True, 'strict': True}
            continue
        marks = [readers[reader][(send_name, 1)] for reader in collector.FAMILIES]
        applying = [mark for mark in accounting.marks_that_apply(accounting.kind_of(outcomes[(send_name, 1)])) if mark in HARD]
        faults[send_name] = {'agreed': any(all(m.get(mark) == 'fails' for m in marks) for mark in applying),
                             'strict': any(any(m.get(mark) == 'fails' for m in marks) for mark in applying)}
    by_topic = collections.defaultdict(dict)
    for send_name, row in sends.items():
        arm_draw, topic = send_name.split('|', 1)
        by_topic[topic][arm_draw] = (row['status'], faults[send_name])
    exercised = sorted(t for t in targets if any(by_topic[t][f'frozen-d{d}'][0] != 'ladder' for d in (1, 2)))
    recovered = sorted(t for t in exercised if all(by_topic[t][f'edited-d{d}'][0] == 'ladder' and not by_topic[t][f'edited-d{d}'][1]['strict']
                                                    for d in (1, 2)))
    controls_held = {t: all(by_topic[t][f'edited-d{d}'][0] != 'ladder' and not by_topic[t][f'edited-d{d}'][1]['strict'] for d in (1, 2))
                     for t in sorted(controls_counted)}
    worse = []
    for topic in sorted(targets | controls_counted):
        for counting in ('agreed', 'strict'):
            failed = {arm: sum(by_topic[topic][f'{arm}-d{d}'][1][counting] for d in (1, 2)) for arm in ARMS}
            if failed['edited'] > failed['frozen']:
                worse.append((topic, counting, failed))
    table = {topic: {arm_draw: [status, faults_of['agreed'], faults_of['strict']] for arm_draw, (status, faults_of) in sorted(arms.items())}
             for topic, arms in sorted(by_topic.items())}
    print(json.dumps({'classifier calls': calls, 'counted targets': sorted(targets), 'counted controls': sorted(controls_counted),
                      'exercised': exercised, 'recovered': recovered, 'controls held': controls_held, 'edited worse on a topic': worse,
                      'per topic [status, agreed fault, strict fault]': table}, indent=1))
    if len(exercised) < 3:
        verdict = f'INCONCLUSIVE: the frozen arm declines {len(exercised)} counted targets, fewer than 3'
    elif len(recovered) >= 0.8 * len(exercised) and all(controls_held.values()) and not worse:
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
        score(*sys.argv[2:7])
    else:
        sys.exit(__doc__)
