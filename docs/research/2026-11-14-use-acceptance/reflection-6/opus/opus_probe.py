"""Alex's Opus trial (2026-11-16, "你试试看opus"): gpt-6-luna against claude-opus-5-5 on the same ladder request, the 26 topics outside the
44, one interleaved draw each, read blind by both families. Claude goes through `anthropic_adapter.route`; production code is unchanged.

One draw each: a direction on 26 topics, labelled one draw, not a total between arms (AGENTS §7.2).

  python3 opus_probe.py check                          # $0: requests, the adapter's translation, controls, spend; writes check-passed.json
  python3 opus_probe.py send <new run folder>          # luna d1, then opus d1 (its first request alone, as a compatibility check)
  python3 opus_probe.py reading <run folder> <key folder>
  python3 opus_probe.py score <run folder> <key folder>
"""
import collections
import concurrent.futures
import copy
import dataclasses
import hashlib
import json
import os
import random
import sys
import threading
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE), str(HERE.parent / 'reference-control'), str(HERE.parents[1] / 'splitting')]
import refcontrol  # noqa: E402   (puts Stage A, the ladder step and src on the path)
import probe_split  # noqa: E402
import accounting  # noqa: E402
import budget  # noqa: E402
import build_reader_packets  # noqa: E402
import collect_readings as collector  # noqa: E402
import ladder_step  # noqa: E402
import model_calls  # noqa: E402
import stage_a  # noqa: E402
from hivemind import model  # noqa: E402

SETTINGS = {'luna': stage_a.SETTING, 'opus': dataclasses.replace(stage_a.SETTING, model='claude-opus-5-5')}
ORDER = [('luna', 1), ('opus', 1)]
CAPS = {'luna': 0.14, 'opus': 2.09}     # together within D439's remaining ~$2.23 (after run-1's $0.026)
EXPECTED_SPEND = {'luna': 0.04, 'opus': 0.0}   # luna: run-1 spent $0.0262 on 21 written topics; opus is held by the first-topic projection
WORKERS = {'luna': 8, 'opus': 1}         # opus's worst-case reserve is about $0.45 an attempt: one in flight leaves the cap for spending
CONTROL, CANDIDATE = 'luna', 'opus'
SENDS = 26 * len([1 for arm, _ in ORDER if arm == CONTROL])
RECORD = HERE / 'check-passed.json'
CODE_FILES = [Path(__file__), Path(refcontrol.__file__), refcontrol.LADDER / 'ladder_step.py', refcontrol.LADDER / 'candidate-system.txt',
              refcontrol.LADDER / 'candidate-closing.txt', refcontrol.LADDER / 'candidate-schema.json', refcontrol.STAGE_A / 'stage_a.py',
              HERE / 'anthropic_adapter.py']
DRAWS = {arm: sum(1 for named, _ in ORDER if named == arm) for arm in ('luna', 'opus')}
NEW_CONTROLS = {'control|unlisted-part': ('c2/clean-1', 'L'), 'control|unjustified-refusal': ('c2/clean-4', 'N')}
HARD = refcontrol.HARD
SHUFFLE_SEED = 20261132


def built(case, setting, rl):
    texts = stage_a.request_texts()
    user = ladder_step.user_text(stage_a.payload_for(case, rl), texts['closing'])
    return model.build_request(setting, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def code_digest():
    return hashlib.sha256(b''.join(path.read_bytes() for path in CODE_FILES)).hexdigest()


def controls():
    """The reference control's four, and two new planted-wrong ones (an unlisted part, an unjustified refusal)."""
    out = refcontrol.controls()
    stored = {row['case']: row for row in map(json.loads, refcontrol.JULY_STORED.read_text().splitlines()) if row['pass'] == 1}
    for control, (name, mark) in NEW_CONTROLS.items():
        row, case = copy.deepcopy(stored[name]), refcontrol.july_case(name)
        if mark == 'L':
            parts = row['answer']['ladder']['not_judged']
            if not parts or 'material' not in parts[0]['part']:
                raise SystemExit(f'{control}: the stored first listed part of {name} is not the materiality part')
            row['answer']['ladder']['not_judged'] = parts[1:]
        else:
            reason = 'the topic has no main figure or event: it names several with none of them the main one'
            row = dict(row, status='no ladder', reason=reason, answer={'no_ladder': reason, 'ladder': None}, passage=None, view=None)
        out.append((dict(row, case=control, **{'pass': 1}), case, {mark: 'fails'}))
    return out


def check():
    import anthropic_adapter
    rl = refcontrol.research_list()
    failures, shas = [], {CONTROL: {}, CANDIDATE: {}}
    for source, name, case, stored in refcontrol.population():
        control, candidate = built(case, SETTINGS[CONTROL], rl), built(case, SETTINGS[CANDIDATE], rl)
        same_as_stored = model.request_identity(control)[1] == stored['requests'][0]['request_sha256']
        sent_control, sent_candidate = json.dumps(control, ensure_ascii=False), json.dumps(candidate, ensure_ascii=False)   # the bytes as sent
        only_model = sent_control.count('"model": "gpt-6-luna"') == 1 and \
            sent_candidate == sent_control.replace('"model": "gpt-6-luna"', '"model": "claude-opus-5-5"')
        translated = anthropic_adapter.to_anthropic(candidate)
        same_texts = translated['system'] == candidate['messages'][0]['content'] and \
            translated['messages'] == [candidate['messages'][1]] and translated['max_tokens'] == candidate['max_completion_tokens'] and \
            translated['output_config']['effort'] == candidate['reasoning_effort'] and \
            translated['output_config']['format']['schema'] == anthropic_adapter.api_schema(candidate['response_format']['json_schema']['schema'])
        if not (same_as_stored and only_model and same_texts):
            failures.append(f'{source}:{name} stored {same_as_stored} only-model {only_model} same-texts {same_texts}')
        shas[CONTROL][f'{source}:{name}'] = model.request_identity(control)[1]
        shas[CANDIDATE][f'{source}:{name}'] = model.request_identity(candidate)[1]
    built_controls = controls()
    worst = {arm: DRAWS[arm] * 2 * budget.ATTEMPTS * sum(budget.worst_cost(built(case, SETTINGS[arm], rl)) for *_, case, _ in refcontrol.population())
             for arm in SETTINGS}
    print(f'26 topics: each luna request equals its stored first request, each opus request differs only in its model, and the adapter '
          f'sends the same texts, cap, effort and schema less its patterns (checked client-side by model.call): '
          f'{not failures}; controls {len(built_controls)}; most attempts an arm {26 * DRAWS[CANDIDATE] * 2 * budget.ATTEMPTS}; the sum of worst-case '
          f'reserves if every attempt were at its worst {{{", ".join(f"{a}: ${w:.2f}" for a, w in worst.items())}}}; caps {CAPS}')
    for arm in SETTINGS:
        room = WORKERS[arm] * max(budget.worst_cost(built(case, SETTINGS[arm], rl)) for *_, case, _ in refcontrol.population())
        if CAPS[arm] < room + EXPECTED_SPEND[arm]:
            failures.append(f'{arm}: the cap ${CAPS[arm]:.2f} is below {WORKERS[arm]} attempts in flight at their worst (${room:.3f}) '
                            f'plus the expected spend ${EXPECTED_SPEND[arm]:.2f}')
        print(f'{arm}: cap ${CAPS[arm]:.2f}; in-flight room ${room:.3f}; expected spend ${EXPECTED_SPEND[arm]:.2f}')
    if failures:
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'code_sha256': code_digest(), 'requests': shas}, indent=1) + '\n')
    print('check passed')


def run_arm(cases, folder, cap_usd, setting, rl, transport=None, workers=8, first_alone=False, room=0.0):
    """One arm-draw: Stage A's runner with the setting given (its model, effort and cap)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    limit = stage_a.StageALimit(cap_usd, folder / 'spend.jsonl', attempt=transport)
    texts = stage_a.request_texts()
    checksum = hashlib.sha256(json.dumps([setting.model, setting.reasoning_effort, setting.max_output_tokens]).encode()).hexdigest()[:16]
    call_config = SimpleNamespace(provider='openai', version=f'clean-ladder-model-{setting.model}', checksum=checksum)
    archive = model.Archive(str(folder / 'archive.sqlite'))
    write_lock, written = threading.Lock(), []

    def work(case):
        labelled = SimpleNamespace(request_number=0)
        labelled.send = lambda provider, request: limit.send_labelled(f"{case['case']}|{labelled.request_number}", provider, request)
        call_model = model_calls.model_caller(model, archive, call_config, setting, labelled)

        def counted(system_text, user_text, schema):
            labelled.request_number += 1
            return call_model(system_text, user_text, schema)
        try:
            outcome = ladder_step.ladder_for_thesis(stage_a.payload_for(case, rl), system_text=texts['system'], closing_text=texts['closing'],
                                                    schema=texts['schema'], call_model=counted, check=refcontrol.check_of(case, rl))
            view = None
            if outcome['status'] == 'ladder':
                view = ladder_step.write_view(outcome['answer']['ladder'], outcome['passage'], thesis=case['thesis'],
                                              article_day=case['item']['publication_date'], company=stage_a.COMPANY, research_list=rl)
            row = {'case': case['case'], 'pass': 1, 'status': outcome['status'], 'reason': outcome['reason'], 'requests': outcome['requests'],
                   'answer': outcome['answer'], 'passage': outcome['passage'], 'view': view}
            with write_lock:
                with (folder / 'outcomes.jsonl').open('a') as handle:
                    handle.write(ladder_step.as_json(row) + '\n')
                    handle.flush()
                    os.fsync(handle.fileno())
                written.append(case['case'])
        except (stage_a.Stopped, budget.OverBudget):
            return
        except Exception as error:
            limit.stop(f"{case['case']}: {type(error).__name__}: {error}")
    if first_alone:                       # a compatibility check: the first request alone, kept as part of the draw and not inspected
        work(cases[0])
        if not written:
            limit.stop(limit.stop_reason or 'the first request alone wrote no outcome')
            return written, limit
        known, in_full, _ = stage_a.ledger_total(folder / 'spend.jsonl')
        projected = (known + in_full) * len(cases)
        print(f'the first topic alone cost ${known + in_full:.4f}; the arm projects to ${projected:.2f}, plus ${room:.2f} of attempts in '
              f'flight at their worst, against its cap ${cap_usd:.2f}', flush=True)
        if projected + room > cap_usd:
            limit.stop(f'the projection ${projected:.2f} plus ${room:.2f} in flight is above the cap ${cap_usd:.2f}: no further send')
            return written, limit
        cases = cases[1:]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(work, cases))
    return written, limit


def send(folder, *, transport=None):
    record = json.loads(RECORD.read_text()) if RECORD.exists() else None
    if record is None or record['code_sha256'] != code_digest():
        raise SystemExit('no check record for these files: run `check` first')
    rl = refcontrol.research_list()
    population = refcontrol.population()
    for arm in SETTINGS:
        now = {f'{source}:{name}': model.request_identity(built(case, SETTINGS[arm], rl))[1] for source, name, case, _ in population}
        if now != record['requests'][arm]:
            raise SystemExit('REFUSED: the requests differ from the checked record')
    import anthropic_adapter
    folder, guard = Path(folder), probe_split.BreachGuard(transport or anthropic_adapter.route)
    spent = collections.Counter()
    for arm, draw in ORDER:
        cases = [dict(case, case=f'{arm}-d{draw}|{source}:{name}') for source, name, case, _ in population]
        cap = CAPS[arm] - spent[arm]
        room = WORKERS[arm] * max(budget.worst_cost(built(case, SETTINGS[arm], rl)) for *_, case, _ in population)
        written, limit = run_arm(cases, folder / f'{arm}-d{draw}', cap, SETTINGS[arm], rl, transport=guard, workers=WORKERS[arm],
                                 first_alone=(arm, draw) == (CANDIDATE, 1), room=room)
        known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
        spent[arm] += known + in_full
        over = probe_split.over_reserve(folder / f'{arm}-d{draw}' / 'spend.jsonl')
        print(f'{arm} d{draw}: {len(written)} of 26 written; spent ${known + in_full:.4f}; over reserve {len(over)}', flush=True)
        if over or guard.breaches or limit.stopped or len(written) != 26:
            raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or over or guard.breaches}. NOT MEASURED.')
    print(f'spent {dict(spent)}')


def reading(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    rl = refcontrol.research_list()
    population = {f'{source}:{name}': case for source, name, case, _ in refcontrol.population()}
    rows, cases = [], {}
    for arm, draw in ORDER:
        for row in map(json.loads, (run_folder / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()):
            if row['status'] not in ('ladder', 'no ladder'):
                continue
            rows.append(row)
            cases[row['case']] = dict(population[row['case'].split('|', 1)[1]], case=row['case'])
    expected = {}
    for row, case, marks in controls():
        rows.append(row)
        cases[row['case']] = dict(case, case=row['case'])
        expected[row['case']] = marks
    reading_folder = run_folder / 'reading'
    (reading_folder / 'send-1').mkdir(parents=True)
    (reading_folder / 'send-1' / 'outcomes.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    order = sorted(rows, key=lambda row: row['case'])
    random.Random(SHUFFLE_SEED).shuffle(order)
    (reading_folder / 'readers').mkdir()
    key, packets = {}, []
    for number, row in enumerate(order, start=1):
        key[str(number)] = [row['case'], 1]
        if (number - 1) % build_reader_packets.ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(row, cases[row['case']], rl)})
    for packet_number, packet in enumerate(packets, start=1):
        (reading_folder / 'readers' / f'packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'controls-expected.json').write_text(json.dumps(expected, indent=1) + '\n')
    print(f'{len(rows)} items in {len(packets)} packets')


def score(run_folder, key_folder):
    reading_folder = Path(run_folder) / 'reading'
    key, item_of, outcomes, readers, problems = collector.read_rows(reading_folder, Path(key_folder) / 'key.json')
    if any(found['rows'] or found['unreadable lines'] for found in problems.values()):
        raise SystemExit(f'VOID: rows missing or not valid: {problems}')
    for control, marks in json.loads((Path(key_folder) / 'controls-expected.json').read_text()).items():
        for mark, value in marks.items():
            if mark != 'all' and any(readers[reader][(control, 1)][mark] != value for reader in collector.FAMILIES):
                raise SystemExit(f'VOID: a family missed the planted {control} ({mark})')
            if mark == 'all' and all(any(readers[reader][(control, 1)].get(hard) == 'fails' for hard in HARD) for reader in collector.FAMILIES):
                raise SystemExit(f'VOID: both families fail a hard line on the sound {control}: the reading is too harsh')
    sends = {arm: {} for arm in SETTINGS}
    for arm, draw in ORDER:
        for row in map(json.loads, (Path(run_folder) / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines()):
            sends[arm][row['case']] = row
    report = {}
    for unresolved_as in ('holds', 'fails'):
        faulted = {arm: collections.Counter() for arm in SETTINGS}
        items = {arm: 0 for arm in SETTINGS}
        for send, outcome in outcomes.items():
            arm = send[0].split('-d')[0]
            if arm not in SETTINGS:
                continue
            rows = [readers[reader][send] for reader in collector.FAMILIES]
            found = {mark for mark in accounting.marks_that_apply(accounting.kind_of(outcome)) if mark in HARD
                     and refcontrol.settled(rows, mark, unresolved_as) == 'fails'}
            if found:
                items[arm] += 1
                faulted[arm][send[0].split('|', 1)[1]] += 1
        statuses = {arm: collections.Counter(row['status'] for row in sends[arm].values()) for arm in SETTINGS}
        if any(sum(counter.values()) != SENDS for counter in statuses.values()):
            raise SystemExit(f'NOT SCORED: an arm does not hold {SENDS} sends: {statuses}')
        unreadable = {arm: sum(any('could not be read' in str(request.get('error') or '') for request in row['requests'])
                               for row in sends[arm].values()) for arm in SETTINGS}
        lost = {arm: statuses[arm]['no ladder: refused'] for arm in SETTINGS}         # refused twice by code: not read, counted as failed
        for arm in SETTINGS:
            for case, row in sends[arm].items():
                if row['status'] == 'no ladder: refused':
                    faulted[arm][case.split('|', 1)[1]] += 1
        failed = {arm: items[arm] + lost[arm] for arm in SETTINGS}
        new_harm = [topic for topic, count in faulted[CANDIDATE].items() if count >= DRAWS[CANDIDATE] and faulted[CONTROL][topic] == 0]
        report[unresolved_as] = {'failed sends (agreed hard-line faults plus sends refused twice by code)': failed,
                                 'faulted items read': items, 'sends refused twice by code': lost,
                                 'model refusals': {arm: statuses[arm]['no ladder'] for arm in SETTINGS}, 'unreadable answers': unreadable,
                                 'new harm topics': new_harm, 'failed per topic': {arm: dict(counter) for arm, counter in faulted.items()}}
    key_name = 'failed sends (agreed hard-line faults plus sends refused twice by code)'
    agreed, strict = report['holds'], report['fails']
    luna_failed, opus_failed = agreed[key_name][CONTROL], agreed[key_name][CANDIDATE]
    improvement = opus_failed * 2 <= luna_failed and luna_failed - opus_failed >= 3
    no_harm = not agreed['new harm topics'] and agreed['model refusals'][CANDIDATE] - agreed['model refusals'][CONTROL] <= 2 and \
        agreed['unreadable answers'][CANDIDATE] - agreed['unreadable answers'][CONTROL] <= 2
    same_direction = strict[key_name][CANDIDATE] < strict[key_name][CONTROL]
    if luna_failed < 3:
        verdict = 'inconclusive (the luna arm fails fewer than 3 sends: too little to test against)'
    elif improvement and no_harm and same_direction:
        verdict = 'moves the candidate'
    elif opus_failed >= luna_failed - 1:
        verdict = 'closes it'
    else:
        verdict = 'inconclusive'
    print(json.dumps(report, indent=1))
    print(f'VERDICT: {verdict}')
    return verdict, report


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'check':
        check()
    elif command == 'send':
        send(sys.argv[2])
    elif command == 'reading':
        reading(*sys.argv[2:4])
    elif command == 'score':
        score(*sys.argv[2:4])
    else:
        sys.exit(__doc__)
