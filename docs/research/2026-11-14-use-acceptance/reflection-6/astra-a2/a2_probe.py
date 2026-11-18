"""Astra with arm A2's request against astra with the frozen request (council round 29): a diagnostic on 12 exposed topics outside
the 44, two interleaved draws, read twice blind (the gate form with the H field; a source-backed product review), and the verdict
fixed before. A2 is the frozen request plus D436's second-side sentences, with "the topic's wording" read as its description and outcome.

  python3 a2_probe.py check                                  # $0: A2 differs from the frozen request only by its recorded edits
  python3 a2_probe.py send <new run folder>                  # frozen d1, a2 d1, frozen d2, a2 d2
  python3 a2_probe.py gate-reading <run folder> <key folder> # the gate form's packets (+ six controls)
  python3 a2_probe.py review-reading <run folder> <key folder>   # the product review's packet (+ four controls)
  python3 a2_probe.py final <run folder> <gate key folder> <review key folder> <review files...>
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
sys.path[:0] = [str(HERE.parent / 'astra'), str(HERE.parent / 'due-day'), str(ROOT / 'clean-arch' / 'step4-2026-11-10' / 'stage_a')]
import astra_probe as base  # noqa: E402
from astra_probe import budget, collector, model, probe_split, refcontrol, stage_a  # noqa: E402
import build_reader_packets  # noqa: E402
import dueday_probe  # noqa: E402   (the product review's controls and row checks)

A2 = ROOT / 'docs' / 'research' / '2026-11-14-use-acceptance' / 'unlisted-parts' / 'arm-a2'
EDITS = {   # file: the exact replacements that turn the frozen text into A2's (checked byte for byte)
    'system': [
        ("- A topic's wording may ask about more than one thing.", "- A topic's description and outcome together may ask about more than one thing."),
        ("List every other part of the topic's wording that the question leaves out, a second figure or event, a condition or a comparison, in not_judged, each with one sentence on why it is not the one tracked.",
         "List every other part of the topic's description and outcome that the question leaves out, a second figure or event, a condition or a comparison, in not_judged, each with one sentence on why it is not the one tracked. A second side of the same bet, for example a market's tightness beside the volume shipped, a share beside the total it is part of, or capacity beside the demand it serves, stays in the one question as context: list it in not_judged. A second side is not by itself a reason to decline; decline only when no part is the main one, or when the main part itself meets a case below."),
        ("when the topic's wording names it, list it in not_judged.", "when the topic's description or outcome names it, list it in not_judged."),
    ],
    'closing': [("is every other part of the topic's wording listed in not_judged?",
                 "is every other part of the topic's description and outcome that the question leaves out listed in not_judged?")],
}
SCHEMA_EDITS = [("the topic's wording that the question leaves out", "the topic's description and outcome that the question leaves out"),
                ('the question leaves nothing of the wording out', 'the question leaves nothing of either out')]
CLOSING_ALIGNMENT = ("is every other part of the topic's description and outcome listed in not_judged?",
                     "is every other part of the topic's description and outcome that the question leaves out listed in not_judged?")
# the blind audit (audit.md): A2's closing check keeps wider than its own system text and schema ("that the question leaves out");
# aligned to them, nothing added
ASTRA = dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')
ARMS = ('frozen', 'a2')
ORDER = [('frozen', 1), ('a2', 1), ('frozen', 2), ('a2', 2)]
CAP_USD = 3.40                     # 40 sends at about $0.05 measured; D439 (about $36.43 used) then at most about $39.83 of $40
WORKERS = 1
RECORD = HERE / 'check-passed.json'
TARGETS = ('week-10-06:c1/clean-6', 'week-10-06:c1/clean-3')                                   # astra's agreed failures (H20, memory)
DISPUTED = ('week-10-06:c1/clean-11', 'week-10-06:c1/clean-13', 'fortnight:c1/clean-3', 'fortnight:c1/clean-13')
RECOVERED = ('week-10-06:c1/clean-5',)                                                         # Hugging Face: astra writes it
JUSTIFIED = ('week-10-06:c1/clean-4', 'week-10-06:c1/clean-12', 'fortnight:c1/clean-8')         # declines both families justify
TOPICS = TARGETS + DISPUTED + RECOVERED + JUSTIFIED
HARD = refcontrol.HARD
H_VALUES, H_HARM = ('part', 'already_judged', 'settlement', 'cannot_tell'), ('already_judged', 'settlement')
GATE_SEED, REVIEW_SEED = 20261129, 20261130
FROZEN_TEXTS = stage_a.request_texts          # held here: `send` re-points stage_a.request_texts at a2_texts during A2's draws


def a2_texts():
    frozen = FROZEN_TEXTS()
    system, closing = frozen['system'], frozen['closing']
    for old, new in EDITS['system']:
        system = system.replace(old, new)
    for old, new in EDITS['closing']:
        closing = closing.replace(old, new)
    return dict(frozen, system=system, closing=closing, schema=json.loads((A2 / 'candidate-schema.json').read_text()))


def texts_of(arm):
    return FROZEN_TEXTS() if arm == 'frozen' else a2_texts()


def population():
    entries = [entry for entry in refcontrol.population() if f'{entry[0]}:{entry[1]}' in TOPICS]
    if len(entries) != len(TOPICS):
        raise SystemExit('a probe topic is not in the population')
    return entries


def built(case, arm, rl):
    texts = texts_of(arm)
    user = base.ladder_step.user_text(stage_a.payload_for(case, rl), texts['closing'])
    return model.build_request(ASTRA, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def code_digest():
    return hashlib.sha256(Path(__file__).read_bytes() + b''.join((A2 / name).read_bytes() for name in
                                                                  ('candidate-system.txt', 'candidate-closing.txt', 'candidate-schema.json'))).hexdigest()


def check():
    frozen, a2 = FROZEN_TEXTS(), a2_texts()
    failures = []
    for name in ('system', 'closing'):
        if any(frozen[name].count(old) != 1 for old, _ in EDITS[name]):
            failures.append(f'an edit of the {name} text is not found once in the frozen text')
        stored = (A2 / f'candidate-{name}.txt').read_text()
        if name == 'closing':           # the step strips the closing check as it loads it; the audit's alignment (CLOSING_ALIGNMENT)
            stored = stored.strip().replace(*CLOSING_ALIGNMENT)
        if a2[name] != stored:
            failures.append(f"the {name} text with A2's recorded edits is not A2's stored file")
    schema_edit = json.dumps(frozen['schema'])
    for old, new in SCHEMA_EDITS:
        schema_edit = schema_edit.replace(old, new)
    if json.loads(schema_edit) != a2['schema']:
        failures.append("A2's schema is not the frozen schema with its recorded not_judged description")
    rl = refcontrol.research_list()
    shas = {arm: {} for arm in ARMS}
    replacements = [(json.dumps(old)[1:-1], json.dumps(new)[1:-1]) for name in ('system', 'closing') for old, new in EDITS[name]] + \
        [(json.dumps(old)[1:-1], json.dumps(new)[1:-1]) for old, new in SCHEMA_EDITS]
    for source, name, case, stored in population():
        sent_frozen = json.dumps(built(case, 'frozen', rl)).encode('utf-8')        # the bytes the transport sends (model.openai_transport)
        expected = sent_frozen.decode('utf-8')
        for old, new in replacements:
            expected = expected.replace(old, new)
        if json.dumps(built(case, 'a2', rl)).encode('utf-8') != expected.encode('utf-8'):
            failures.append(f'{source}:{name}: the A2 request differs from the frozen one in more than the recorded edits')
        luna = model.build_request(stage_a.SETTING, frozen['system'], built(case, 'frozen', rl)['messages'][1]['content'], frozen['schema'],
                                   'clean_ladder', 'openai')
        if model.request_identity(luna)[1] != stored['requests'][0]['request_sha256']:
            failures.append(f'{source}:{name}: the frozen request is not the stored one')
        for arm in ARMS:
            shas[arm][f'{source}:{name}'] = model.request_identity(built(case, arm, rl))[1]
    worst = max(budget.worst_cost(built(case, 'a2', rl)) for *_, case, _ in population())
    print(f'{len(TOPICS)} topics; A2 is the frozen request with its recorded edits, the frozen requests are the stored ones: {not failures}; '
          f'worst-case reserve of one attempt ${worst:.2f}; cap ${CAP_USD:.2f}')
    if failures:
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'code_sha256': code_digest(), 'requests': shas}, indent=1) + '\n')
    print('check passed')


def send(folder, *, transport=None):
    record = json.loads(RECORD.read_text()) if RECORD.exists() else None
    if record is None or record['code_sha256'] != code_digest():
        raise SystemExit('no check record for these files: run `check` first')
    rl = refcontrol.research_list()
    entries = population()
    for arm in ARMS:
        if {f'{s}:{n}': model.request_identity(built(c, arm, rl))[1] for s, n, c, _ in entries} != record['requests'][arm]:
            raise SystemExit('REFUSED: the requests differ from the checked record')
    folder, guard = Path(folder), probe_split.BreachGuard(transport)
    spent, last = 0.0, {}
    worst = max(budget.worst_cost(built(c, 'a2', rl)) for *_, c, _ in entries)
    original = stage_a.request_texts
    try:
        for arm, draw in ORDER:
            if last.get(arm, 0.0) + WORKERS * worst > CAP_USD - spent:        # the same arm's last draw estimates this one
                raise SystemExit(f'{arm} d{draw} STOPPED before sending: the arm\'s last draw and the attempt in flight pass what is left. NOT MEASURED.')
            stage_a.request_texts = original if arm == 'frozen' else a2_texts
            cases = [dict(case, case=f'{arm}-d{draw}|{source}:{name}') for source, name, case, _ in entries]
            written, limit = base.run_arm(cases, folder / f'{arm}-d{draw}', CAP_USD - spent, ASTRA, rl, transport=guard, workers=WORKERS)
            stage_a.request_texts = original
            known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            spent += known + in_full
            last[arm] = known + in_full
            over = probe_split.over_reserve(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            print(f'{arm} d{draw}: {len(written)} of {len(entries)} written; spent ${known + in_full:.4f}; over reserve {len(over)}', flush=True)
            if over or guard.breaches or limit.stopped or len(written) != len(entries):
                raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or over or guard.breaches}. NOT MEASURED.')
    finally:
        stage_a.request_texts = original
    print(f'spent ${spent:.4f}')


def outcomes(folder):
    rows = {}
    for arm, draw in ORDER:
        for line in (Path(folder) / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            rows[row['case']] = row
    return rows


def readable(folder):
    return {send: row for send, row in outcomes(folder).items() if row['status'] != 'no ladder: refused'}


H_CONTROL = ('control|listings', ROOT / 'poc' / 'data' / 'clean-dueday-probe-2026-11-16' / 'v2-d1' / 'outcomes.jsonl', 'week-10-06:c1/clean-5')
H_PLANTED = [   # appended to the stored Hugging Face question's two true parts; both families must classify all four
    {'part': 'Nvidia or Hugging Face formally terminating the signed acquisition before it closes.',
     'why': 'The question tracks completion, not termination.'},
    {'part': "Nvidia's closing announcement and regulatory filings that will report the outcome.",
     'why': 'The filings are where the answer will be known.'},
]
H_EXPECTED = ['part', 'part', 'already_judged', 'settlement']


def listing_control():
    """(row, case, expected marks): a stored Hugging Face question with two true parts and two planted listings, one its own
    ruled-out outcome (already judged) and one a settlement route."""
    name, path, topic = H_CONTROL
    row = next(json.loads(line) for line in path.read_text().splitlines() if json.loads(line)['case'].endswith('|' + topic))
    if row['status'] != 'ladder' or len(row['answer']['ladder']['not_judged']) != 2:
        raise SystemExit('the listing control is not the stored two-part Hugging Face question')
    row = json.loads(json.dumps(row))
    row['answer']['ladder']['not_judged'] += H_PLANTED
    case = next(c for s, n, c, _ in refcontrol.population() if f'{s}:{n}' == topic)
    return dict(row, case=name), case, {'H': H_EXPECTED}


def gate_reading(folder, key_folder):
    """The gate form's blind packets: every readable send and the six known controls of the model comparison, as Stage A's readers
    see an item; the key and the controls' expected marks outside the repository."""
    folder, key_folder = Path(folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    cases = {f'{s}:{n}': c for s, n, c, _ in population()}
    rows, item_cases, expected = dict(readable(folder)), {}, {}
    for send in rows:
        item_cases[send] = cases[send.split('|', 1)[1]]
    for row, case, marks in base.controls() + [listing_control()]:
        rows[row['case']], item_cases[row['case']], expected[row['case']] = row, case, marks
    order = sorted(rows)
    random.Random(GATE_SEED).shuffle(order)
    rl = refcontrol.research_list()
    reading = folder / 'gate-reading'
    (reading / 'send-1').mkdir(parents=True)
    (reading / 'send-1' / 'outcomes.jsonl').write_text(''.join(json.dumps(dict(rows[send], **{'pass': 1}), ensure_ascii=False) + '\n' for send in order))
    (reading / 'readers').mkdir()
    key, packets = {}, []
    for number, send in enumerate(order, start=1):
        key[str(number)] = [send, 1]
        if (number - 1) % build_reader_packets.ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(rows[send], item_cases[send], rl)})
    for number, packet in enumerate(packets, start=1):
        (reading / 'readers' / f'packet-{number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'controls-expected.json').write_text(json.dumps(expected, indent=1) + '\n')
    print(f'{len(order)} items in {len(packets)} packets')


def gate_marks(folder, key_folder):
    """{counting: {send: True for a hard-line fault}} and {counting: {send: number of harmful listings}}, after the controls."""
    reading = Path(folder) / 'gate-reading'
    key, item_of, outcomes_read, readers, problems = collector.read_rows(reading, Path(key_folder) / 'key.json')
    if any(found['rows'] or found['unreadable lines'] for found in problems.values()):
        raise SystemExit(f'VOID: rows missing or not valid: {problems}')
    for control, marks in json.loads((Path(key_folder) / 'controls-expected.json').read_text()).items():
        for mark, value in marks.items():
            if mark != 'all' and any(readers[reader][(control, 1)][mark] != value for reader in collector.FAMILIES):
                raise SystemExit(f'VOID: a family missed the planted {control} ({mark})')
            if mark == 'all' and all(any(readers[reader][(control, 1)].get(hard) == 'fails' for hard in HARD) for reader in collector.FAMILIES):
                raise SystemExit(f'VOID: both families fail a hard line on the sound {control}')
    faults, harm = {}, {}
    for counting in ('holds', 'fails'):
        faults[counting], harm[counting] = {}, {}
        for send_key, outcome in outcomes_read.items():
            send = send_key[0]
            if send.startswith('control|'):
                continue
            rows = [readers[reader][send_key] for reader in collector.FAMILIES]
            kind = base.accounting.kind_of(outcome)
            faults[counting][send] = any(refcontrol.settled(rows, mark, counting) == 'fails'
                                         for mark in base.accounting.marks_that_apply(kind) if mark in HARD)
            listed = len(outcome['answer']['ladder']['not_judged']) if outcome['status'] == 'ladder' else 0
            for row in rows:
                if not isinstance(row.get('H'), list) or len(row['H']) != listed or any(value not in H_VALUES for value in row['H']):
                    raise SystemExit(f'VOID: an H list of {send} does not hold one value for each of its {listed} listed parts')
            values = list(zip(*[row['H'] for row in rows])) if listed else []
            harm[counting][send] = sum((all(v in H_HARM for v in pair) if counting == 'holds' else any(v in H_HARM for v in pair)) for pair in values)
    return faults, harm


def review_reading(folder, key_folder):
    """The product review's blind packet: every readable send and the due-day probe's four known controls."""
    folder, key_folder = Path(folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    cases = {f'{s}:{n}': c for s, n, c, _ in refcontrol.population()}
    rows = readable(folder) | dueday_probe.control_rows()
    sources = {send: send.split('|', 1)[1] for send in readable(folder)} | \
        {control: dueday_probe.CONTROLS[control][1].split('|', 1)[1] for control in dueday_probe.CONTROLS}
    order = sorted(rows)
    random.Random(REVIEW_SEED).shuffle(order)
    rl = refcontrol.research_list()
    items, key = [], {}
    for number, send in enumerate(order, start=1):
        key[str(number)] = send
        items.append({'item': number, **build_reader_packets.item_of(rows[send], cases[sources[send]], rl)})
    (folder / 'review').mkdir(exist_ok=False)
    (folder / 'review' / 'packet.json').write_text(json.dumps(items, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    print(f'{len(items)} items')


def final(folder, gate_keys, review_keys, review_files):
    """The verdict fixed before the send (council round 29)."""
    rows = outcomes(folder)
    faults, harm = gate_marks(folder, gate_keys)
    paths = [Path(path).resolve() for path in review_files]
    if len(set(paths)) != len(paths) or len({path.read_bytes() for path in paths}) != len(paths):
        raise SystemExit('NOT SCORED: the review files are not two distinct readings')
    review = dueday_probe.material(review_files, json.loads((Path(review_keys) / 'key.json').read_text()))
    verdicts = {}
    for counting, review_rule in (('holds', all), ('fails', any)):
        failed = {send: rows[send]['status'] == 'no ladder: refused' or faults[counting].get(send, False) for send in rows}
        flagged = {send for send, values in review.items() if review_rule(values)}
        total = {arm: sum(failed[f'{arm}-d{d}|{t}'] for t in TOPICS for d in (1, 2)) for arm in ARMS}
        per_topic = all(sum(failed[f'a2-d{d}|{t}'] for d in (1, 2)) <= sum(failed[f'frozen-d{d}|{t}'] for d in (1, 2)) for t in TOPICS)
        justified_kept = all(rows[f'a2-d{d}|{t}']['status'] == 'no ladder' for t in JUSTIFIED for d in (1, 2))
        harm_total = {arm: sum(harm[counting].get(f'{arm}-d{d}|{t}', 0) for t in TOPICS for d in (1, 2)) for arm in ARMS}
        replacements = [f'a2-d{d}|{t}' for t in TOPICS for d in (1, 2)
                        if rows[f'a2-d{d}|{t}']['status'] == 'ladder' and rows[f'frozen-d{d}|{t}']['status'] != 'ladder']
        replacements_sound = not any(send in flagged for send in replacements)
        material_per_topic = all(sum(f'a2-d{d}|{t}' in flagged for d in (1, 2)) <= sum(f'frozen-d{d}|{t}' in flagged for d in (1, 2)) for t in TOPICS)
        improved = total['a2'] <= total['frozen'] - 2
        if improved and per_topic and justified_kept and harm_total['a2'] <= harm_total['frozen'] + 1 and replacements_sound and material_per_topic:
            verdicts[counting] = 'moves (a diagnostic on exposed topics)'
        elif total['a2'] >= total['frozen'] or not justified_kept or harm_total['a2'] > harm_total['frozen'] + 1 or not replacements_sound:
            verdicts[counting] = 'closes'
        else:
            verdicts[counting] = 'inconclusive'
        print(f'{counting}: failed sends {total}; per topic {per_topic}; justified declines kept {justified_kept}; harmful listings {harm_total}; '
              f'replacements {len(replacements)}, sound {replacements_sound}; material per topic {material_per_topic} -> {verdicts[counting]}')
    verdict = verdicts['holds'] if verdicts['holds'] == verdicts['fails'] else 'inconclusive (the countings disagree)'
    print(f'VERDICT: {verdict}')
    return verdict


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'check':
        check()
    elif command == 'send':
        send(sys.argv[2])
    elif command == 'gate-reading':
        gate_reading(*sys.argv[2:4])
    elif command == 'review-reading':
        review_reading(*sys.argv[2:4])
    elif command == 'final':
        final(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])
    else:
        sys.exit(__doc__)
