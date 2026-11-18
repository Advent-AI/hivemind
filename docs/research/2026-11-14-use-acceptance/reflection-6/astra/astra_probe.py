"""The astra screen (DESIGN.md, council round 13): gpt-6-astra against a fresh gpt-6.1-sol arm on the unchanged request, on 12 of the
26 topics drawn by a fixed seed, three interleaved draws each, read blind together. A screen: "promising" leads to a separate decision.

  python3 astra_probe.py check                          # $0: the sample, requests, controls, spend; writes check-passed.json
  python3 astra_probe.py send <new run folder>          # sol d1, astra d1 (its first request alone), sol d2, astra d2, sol d3, astra d3
  python3 astra_probe.py reading <run folder> <key folder>
  python3 astra_probe.py score <run folder> <key folder>
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
sys.path[:0] = [str(HERE.parent / 'reference-control'), str(HERE.parents[1] / 'splitting')]
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

SETTINGS = {'sol': dataclasses.replace(stage_a.SETTING, model='gpt-6.1-sol'), 'astra': dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')}
ORDER = [('sol', 1), ('astra', 1), ('sol', 2), ('astra', 2), ('sol', 3), ('astra', 3)]
CONTROL, CANDIDATE = 'sol', 'astra'
CAPS = {'sol': 1.20, 'astra': 5.50}     # $6.70 in all, within what remains of D439's $40 (about $9.0)
WORKERS = {'sol': 2, 'astra': 1}        # worst-case reserves about $0.21 (sol) and $1.04 (astra) an attempt
SAMPLE_SIZE, SAMPLE_SEED = 12, 20261123
RECORD = HERE / 'check-passed.json'
CODE_FILES = [Path(__file__), Path(refcontrol.__file__), refcontrol.LADDER / 'ladder_step.py', refcontrol.LADDER / 'candidate-system.txt',
              refcontrol.LADDER / 'candidate-closing.txt', refcontrol.LADDER / 'candidate-schema.json', refcontrol.STAGE_A / 'stage_a.py']
NEW_CONTROLS = {'control|unlisted-part': ('c2/clean-1', 'L'), 'control|unjustified-refusal': ('c2/clean-4', 'N')}
HARD = refcontrol.HARD
SHUFFLE_SEED = 20261122


def sample():
    """The 12 topics, drawn from the 26 by a fixed seed over their sorted names, blind to any result: (source, name, case, stored)."""
    population = refcontrol.population()
    names = sorted(f'{source}:{name}' for source, name, _, _ in population)
    chosen = set(random.Random(SAMPLE_SEED).sample(names, SAMPLE_SIZE))
    return [entry for entry in population if f'{entry[0]}:{entry[1]}' in chosen]


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
    rl = refcontrol.research_list()
    failures, shas = [], {CONTROL: {}, CANDIDATE: {}}
    for source, name, case, stored in sample():
        frozen = built(case, stage_a.SETTING, rl)
        control, candidate = built(case, SETTINGS[CONTROL], rl), built(case, SETTINGS[CANDIDATE], rl)
        same_as_stored = model.request_identity(frozen)[1] == stored['requests'][0]['request_sha256']
        sent_frozen = json.dumps(frozen, ensure_ascii=False)                      # the bytes as sent: only the model differs
        only_model = sent_frozen.count('"model": "gpt-6-luna"') == 1 and \
            json.dumps(control, ensure_ascii=False) == sent_frozen.replace('"model": "gpt-6-luna"', '"model": "gpt-6.1-sol"') and \
            json.dumps(candidate, ensure_ascii=False) == sent_frozen.replace('"model": "gpt-6-luna"', '"model": "gpt-6-astra"')
        if not (same_as_stored and only_model):
            failures.append(f'{source}:{name} stored {same_as_stored} only-model {only_model}')
        shas[CONTROL][f'{source}:{name}'] = model.request_identity(control)[1]
        shas[CANDIDATE][f'{source}:{name}'] = model.request_identity(candidate)[1]
    built_controls = controls()
    worst = {arm: max(budget.worst_cost(built(case, SETTINGS[arm], rl)) for *_, case, _ in sample()) for arm in SETTINGS}
    print(f'the sample: {sorted(shas[CONTROL])}')
    print(f'{len(shas[CONTROL])} topics: each frozen request equals its stored first request, and the sol and astra requests differ from it '
          f'only in their model: {not failures}; controls {len(built_controls)}; worst-case reserve of one attempt '
          f'{{{", ".join(f"{a}: ${w:.2f}" for a, w in worst.items())}}}; caps {CAPS}; in flight {WORKERS}')
    if failures:
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'code_sha256': code_digest(), 'requests': shas}, indent=1) + '\n')
    print('check passed')


def run_arm(cases, folder, cap_usd, setting, rl, transport=None, workers=8, first_alone=False, after_first=None):
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
        refused = after_first(folder / 'spend.jsonl') if after_first else None
        if refused:
            limit.stop(refused)
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
    population = sample()
    for arm in SETTINGS:
        now = {f'{source}:{name}': model.request_identity(built(case, SETTINGS[arm], rl))[1] for source, name, case, _ in population}
        if now != record['requests'][arm]:
            raise SystemExit('REFUSED: the requests differ from the checked record')
    folder, guard = Path(folder), probe_split.BreachGuard(transport)
    spent, costliest = collections.Counter(), collections.Counter()
    worst = {arm: max(budget.worst_cost(built(case, SETTINGS[arm], rl)) for *_, case, _ in population) for arm in SETTINGS}
    sends = len(population) * len([1 for arm, _ in ORDER if arm == CANDIDATE])

    def projection(ledger):
        """The first astra request, sent alone, priced for every astra send: refuse the rest when that and the attempts in flight pass the cap."""
        known, in_full, _ = stage_a.ledger_total(ledger)
        projected = (known + in_full) * sends
        print(f'the first astra request cost ${known + in_full:.4f}: ${projected:.2f} projected for {sends} sends', flush=True)
        if projected + WORKERS[CANDIDATE] * worst[CANDIDATE] > CAPS[CANDIDATE]:
            return (f'projected ${projected:.2f} plus ${WORKERS[CANDIDATE] * worst[CANDIDATE]:.2f} in flight passes the '
                    f'${CAPS[CANDIDATE]:.2f} cap: refused before the rest')
        return None
    for arm, draw in ORDER:
        cap = CAPS[arm] - spent[arm]
        if costliest[arm] + WORKERS[arm] * worst[arm] > cap:      # a draw that cannot finish is not started
            raise SystemExit(f'{arm} d{draw} STOPPED before sending: the costliest {arm} draw (${costliest[arm]:.4f}) and the attempts in '
                             f'flight pass the ${cap:.4f} left. NOT MEASURED.')
        cases = [dict(case, case=f'{arm}-d{draw}|{source}:{name}') for source, name, case, _ in population]
        first = (arm, draw) == (CANDIDATE, 1)
        written, limit = run_arm(cases, folder / f'{arm}-d{draw}', cap, SETTINGS[arm], rl, transport=guard, workers=WORKERS[arm],
                                 first_alone=first, after_first=projection if first else None)
        known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
        spent[arm] += known + in_full
        costliest[arm] = max(costliest[arm], known + in_full)
        over = probe_split.over_reserve(folder / f'{arm}-d{draw}' / 'spend.jsonl')
        print(f'{arm} d{draw}: {len(written)} of {len(population)} written; spent ${known + in_full:.4f}; over reserve {len(over)}', flush=True)
        if over or guard.breaches or limit.stopped or len(written) != len(population):
            raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or over or guard.breaches}. NOT MEASURED.')
    print(f'spent {dict(spent)}')


def reading(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    rl = refcontrol.research_list()
    population = {f'{source}:{name}': case for source, name, case, _ in sample()}
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
        if any(sum(counter.values()) != 3 * SAMPLE_SIZE for counter in statuses.values()):
            raise SystemExit(f'NOT SCORED: an arm does not hold {3 * SAMPLE_SIZE} sends: {statuses}')
        unreadable = {arm: sum(any('could not be read' in str(request.get('error') or '') for request in row['requests'])
                               for row in sends[arm].values()) for arm in SETTINGS}
        lost = {arm: statuses[arm]['no ladder: refused'] for arm in SETTINGS}         # refused twice by code: not read, counted as failed
        for arm in SETTINGS:
            for case, row in sends[arm].items():
                if row['status'] == 'no ladder: refused':
                    faulted[arm][case.split('|', 1)[1]] += 1
        failed = {arm: items[arm] + lost[arm] for arm in SETTINGS}
        unjustified = {arm: 0 for arm in SETTINGS}
        for send, outcome in outcomes.items():
            arm = send[0].split('-d')[0]
            if arm in SETTINGS and accounting.kind_of(outcome) == 'refusal':
                if refcontrol.settled([readers[reader][send] for reader in collector.FAMILIES], 'N', unresolved_as) == 'fails':
                    unjustified[arm] += 1
        new_harm = [topic for topic, count in faulted[CANDIDATE].items() if count >= 2 and faulted[CONTROL][topic] == 0]
        report[unresolved_as] = {'failed sends (agreed hard-line faults plus sends refused twice by code)': failed,
                                 'faulted items read': items, 'sends refused twice by code': lost,
                                 'model refusals': {arm: statuses[arm]['no ladder'] for arm in SETTINGS}, 'unreadable answers': unreadable,
                                 'unjustified refusals': unjustified,
                                 'new harm topics': new_harm, 'failed per topic': {arm: dict(counter) for arm, counter in faulted.items()}}
    key_name = 'failed sends (agreed hard-line faults plus sends refused twice by code)'
    agreed, strict = report['holds'], report['fails']
    control, candidate = agreed[key_name][CONTROL], agreed[key_name][CANDIDATE]
    no_harm = not agreed['new harm topics'] and agreed['unjustified refusals'][CANDIDATE] <= agreed['unjustified refusals'][CONTROL] and \
        agreed['unreadable answers'][CANDIDATE] - agreed['unreadable answers'][CONTROL] <= 2
    strict_too = strict[key_name][CANDIDATE] < strict[key_name][CONTROL]     # the advantage must not rest on disputed marks
    if candidate >= 3:
        verdict = 'closes this candidate under this test'
    elif control < 2:
        verdict = 'inconclusive (the sol arm fails fewer than 2 sends: too little to test against)'
    elif candidate <= 1 and candidate < control and no_harm and strict_too:
        verdict = 'promising (a screen: a separate decision follows)'
    elif candidate >= control:
        verdict = 'closes this candidate under this test'
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
