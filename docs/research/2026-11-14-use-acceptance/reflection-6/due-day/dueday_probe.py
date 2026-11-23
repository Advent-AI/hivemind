"""The due-day probe (council rounds 19 and 20): astra on the frozen request against astra on the request whose binding-obligation clause
is narrowed to amounts (`candidate-system-v2.txt`), on nine topics covering the due-day cases, two interleaved draws each.

  python3 dueday_probe.py check                  # $0: the requests differ only in the clause; spend; writes check-passed.json
  python3 dueday_probe.py send <new run folder>  # frozen d1, v2 d1, frozen d2, v2 d2
  python3 dueday_probe.py tally <run folder>     # each topic's stored due days per arm
  python3 dueday_probe.py reading <run folder> <key folder>      # the blind review packet of both arms
  python3 dueday_probe.py final <run folder> <key folder> <review files...>   # the verdict fixed before
"""
import collections
import dataclasses
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE.parent / 'astra'), str(HERE.parents[4] / 'clean-arch' / 'step4-2026-11-10' / 'stage_a')]
import astra_probe as base  # noqa: E402   (Stage A's runner, the limit, the breach guard, the population)
from astra_probe import budget, model, probe_split, refcontrol, stage_a  # noqa: E402

FROZEN_CLAUSE = 'for an obligation already taken on, its next annual filing;'
V2_CLAUSE = 'for the amount of an obligation already taken on, its next annual filing;'
V2_SYSTEM = HERE / 'candidate-system-v2.txt'
ASTRA = dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')
ARMS = ('frozen', 'v2')
ORDER = [('frozen', 1), ('v2', 1), ('frozen', 2), ('v2', 2)]
CAP_USD = 3.20                     # both arms, 36 sends at about $0.04 measured; about $5.3 remains of D439's $40
WORKERS = 1
RECORD = HERE / 'check-passed.json'
TOPICS = {   # topic: the case it covers and the due day each arm must give (`stated`, `period_end`, `annual_filing` or `any`)
    'fortnight:c1/clean-6': ('a signed deal completing, stated check date 24 March 2028', '2028-03-24'),
    'week-10-06:c1/clean-5': ('the same deal, its closing window the first half of 2027', '2027-06-30'),
    'fortnight:c1/clean-12': ('a guarantee becoming final, stated check date 3 April 2028', '2028-04-03'),
    'fortnight:c1/clean-2': ('purchase commitments: an amount at the next annual filing', 'annual_filing'),
    'week-10-06:c1/clean-1': ('a guarantee amount at the next annual filing', 'annual_filing'),
    'week-10-06:c1/clean-8': ('a loss-coverage amount at the next annual filing', 'annual_filing'),
    'week-10-06:c1/clean-11': ('an unsigned acquisition', 'any'),
    'fortnight:c1/clean-4': ('an event at the fiscal year-end', 'any'),
    'fortnight:c1/clean-7': ('an approval event by a stated day', 'any'),
}
ALLOWED = {   # the outcomes every stored draw gave on the event controls (D629 and both screens, census of 2026-11-16)
    'week-10-06:c1/clean-11': {'decline', '2028-04-10'},
    'fortnight:c1/clean-4': {'2027-01-31', '2027-02-28'},
    'fortnight:c1/clean-7': {'2027-01-31'},
}


def texts_of(arm):
    texts = stage_a.request_texts()
    if arm == 'v2':
        texts = dict(texts, system=V2_SYSTEM.read_text())
    return texts


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
    return hashlib.sha256(Path(__file__).read_bytes() + V2_SYSTEM.read_bytes()).hexdigest()


def check():
    frozen_text, v2_text = stage_a.request_texts()['system'], V2_SYSTEM.read_text()
    if frozen_text.count(FROZEN_CLAUSE) != 1 or v2_text != frozen_text.replace(FROZEN_CLAUSE, V2_CLAUSE):
        raise SystemExit('CHECK FAILED: the v2 system text is not the frozen one with the one clause changed')
    rl = refcontrol.research_list()
    failures, shas = [], {arm: {} for arm in ARMS}
    for source, name, case, stored in population():
        frozen = built(case, 'frozen', rl)
        luna = model.build_request(stage_a.SETTING, frozen_text, frozen['messages'][1]['content'], stage_a.request_texts()['schema'],
                                   'clean_ladder', 'openai')
        if model.request_identity(luna)[1] != stored['requests'][0]['request_sha256']:
            failures.append(f'{source}:{name}: the frozen request is not the stored one')
        sent_frozen, sent_v2 = json.dumps(frozen, ensure_ascii=False), json.dumps(built(case, 'v2', rl), ensure_ascii=False)
        if sent_v2 != sent_frozen.replace(FROZEN_CLAUSE, V2_CLAUSE):
            failures.append(f'{source}:{name}: the v2 request differs in more than the clause')
        for arm in ARMS:
            shas[arm][f'{source}:{name}'] = model.request_identity(built(case, arm, rl))[1]
    worst = max(budget.worst_cost(built(case, 'frozen', rl)) for *_, case, _ in population())
    print(f'{len(TOPICS)} topics; the requests are the stored frozen ones and differ only in the clause: {not failures}; '
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
    spent = 0.0
    original = stage_a.request_texts
    try:
        for arm, draw in ORDER:
            stage_a.request_texts = lambda arm=arm: texts_of_frozen_or_v2(original, arm)
            cases = [dict(case, case=f'{arm}-d{draw}|{source}:{name}') for source, name, case, _ in entries]
            written, limit = base.run_arm(cases, folder / f'{arm}-d{draw}', CAP_USD - spent, ASTRA, rl, transport=guard, workers=WORKERS)
            known, in_full, _ = stage_a.ledger_total(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            spent += known + in_full
            over = probe_split.over_reserve(folder / f'{arm}-d{draw}' / 'spend.jsonl')
            print(f'{arm} d{draw}: {len(written)} of {len(entries)} written; spent ${known + in_full:.4f}; over reserve {len(over)}', flush=True)
            if over or guard.breaches or limit.stopped or len(written) != len(entries):
                raise SystemExit(f'{arm} d{draw} STOPPED: {limit.stop_reason or over or guard.breaches}. NOT MEASURED.')
    finally:
        stage_a.request_texts = original
    print(f'spent ${spent:.4f}')


def texts_of_frozen_or_v2(original, arm):
    texts = original()
    return dict(texts, system=V2_SYSTEM.read_text()) if arm == 'v2' else texts


RENDERED = {   # the day the product stores (the view's due_day, code-set for a year's figure by D414) that each arm must give
    'fortnight:c1/clean-6': '2028-03-24', 'week-10-06:c1/clean-5': '2027-06-30', 'fortnight:c1/clean-12': '2028-04-03',
    'fortnight:c1/clean-2': '2027-04-01', 'week-10-06:c1/clean-1': '2027-04-01', 'week-10-06:c1/clean-8': '2027-04-01',
}
AMOUNTS = ('fortnight:c1/clean-2', 'week-10-06:c1/clean-1', 'week-10-06:c1/clean-8')
COMPLETION = ('fortnight:c1/clean-6', 'week-10-06:c1/clean-5')
REVIEW_SEED = 20261128


def outcomes(folder):
    rows = {}
    for arm, draw in ORDER:
        for line in (Path(folder) / f'{arm}-d{draw}' / 'outcomes.jsonl').read_text().splitlines():
            row = json.loads(line)
            rows[row['case']] = row
    return rows


def stored_day(row):
    """The day the product stores for a send; `decline` for the model's decline; `lost` for an answer code refused twice."""
    if row['status'] == 'no ladder: refused':
        return 'lost'
    return 'decline' if row['status'] != 'ladder' else row['view']['due_day']


def tally(folder):
    """Each topic's stored days per arm, and the date conditions of the verdict: (mechanism seen, completion fixed, controls kept,
    new declines as (arm-draw case, matched frozen topic) pairs)."""
    rows = outcomes(folder)
    days = {(topic, arm): [stored_day(rows[f'{arm}-d{draw}|{topic}']) for draw in (1, 2)] for topic in TOPICS for arm in ARMS}
    mechanism = any(day[:7] in ('2027-02', '2027-03') for day in days[('fortnight:c1/clean-6', 'frozen')])
    fixed = all(days[(topic, 'v2')] == [RENDERED[topic]] * 2 for topic in COMPLETION)
    kept = all(days[(topic, arm)] == [RENDERED[topic]] * 2 for topic in ('fortnight:c1/clean-12',) + AMOUNTS for arm in ARMS) and all(
        rows[f'{arm}-d{draw}|{topic}']['answer']['ladder']['due_day_basis'] == 'expected_publication'
        for topic in AMOUNTS for arm in ARMS for draw in (1, 2) if rows[f'{arm}-d{draw}|{topic}']['status'] == 'ladder')
    kept = kept and all(set(days[(topic, 'v2')]) <= ALLOWED[topic] for topic in ALLOWED)
    new_declines = [f'v2-d{draw}|{topic}' for topic in TOPICS for draw in (1, 2)
                    if days[(topic, 'v2')][draw - 1] == 'decline' and days[(topic, 'v2')].count('decline') > days[(topic, 'frozen')].count('decline')]
    new_losses = [topic for topic in TOPICS if days[(topic, 'v2')].count('lost') > days[(topic, 'frozen')].count('lost')]
    for (topic, arm), stored in days.items():
        print(f'{topic:24} {arm:6} {stored}')
    return {'mechanism': mechanism, 'fixed': fixed, 'kept': kept, 'new_declines': new_declines, 'new_losses': new_losses, 'days': days}


CONTROLS = {   # stored answers outside the probe's sends, each with the verdict both reviewers must give (or the reading is void)
    'control|completion-at-filing': ('clean-astra-rest-2026-11-16', 'sol-d1|fortnight:c1/clean-6', 'material'),
    'control|unjustified-decline': ('clean-model-probe-2026-11-16', 'sol-d2|week-10-06:c1/clean-5', 'material'),
    'control|sound-stated-date': ('clean-astra-rest-2026-11-16', 'astra-d1|fortnight:c1/clean-12', 'sound'),
    'control|justified-decline': ('clean-astra-screen-2026-11-16', 'astra-d1|week-10-06:c1/clean-12', 'sound'),
}
VERDICTS, CLASSES = {'sound', 'defect'}, {None, 'unjustified_decline', 'period_changed', 'measure_invented', 'measure_changed',
                                           'condition_lost', 'condition_added', 'choices_unusable', 'other'}
READERS = ('codex', 'claude')


def control_rows():
    rows = {}
    for control, (run, send, _) in CONTROLS.items():
        found = [json.loads(line) for line in (base.ROOT / 'poc' / 'data' / run / send.split('|')[0] / 'outcomes.jsonl').read_text().splitlines()
                 if json.loads(line)['case'] == send]
        if len(found) != 1:
            raise SystemExit(f'{control}: the stored send {send} is not found once')
        rows[control] = dict(found[0], case=control)
    return rows


def reading(folder, key_folder):
    """The blind review packet: the 36 sends of both arms and the four controls in a fixed shuffle, each as the gate's readers see an
    item (the topic with opens_as, the article, the fiscal-year note, the question and rungs as the product shows them, the stored due
    day, the other fields); the key outside the repository."""
    import random
    import build_reader_packets
    folder, key_folder = Path(folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(base.ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    cases = {f'{s}:{n}': c for s, n, c, _ in refcontrol.population()}
    sent = {send: row for send, row in outcomes(folder).items() if row['status'] != 'no ladder: refused'}     # a lost answer is not read
    rows = sent | control_rows()
    sources = {send: send.split('|', 1)[1] for send in sent} | {control: CONTROLS[control][1].split('|', 1)[1] for control in CONTROLS}
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
    print(f'{len(items)} items ({len(CONTROLS)} controls)')


def material(review_files, key):
    """{send: [True for a material defect, per reviewer]} over the 36 sends, after checking two complete valid readings and the
    controls; refuses anything else."""
    if len(review_files) != len(READERS):
        raise SystemExit(f'NOT SCORED: {len(READERS)} review files are needed, got {len(review_files)}')
    marks = {}
    for path in review_files:
        rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
        items = [row.get('item') for row in rows]
        if sorted(items) != list(range(1, len(key) + 1)):
            raise SystemExit(f'NOT SCORED: {path} does not hold each of the {len(key)} items once')
        for row in rows:
            if row.get('verdict') not in VERDICTS or not isinstance(row.get('material'), bool) or row.get('class') not in CLASSES:
                raise SystemExit(f'NOT SCORED: {path} item {row.get("item")} is not a valid row')
            send = key[str(row['item'])]
            flagged = row['verdict'] == 'defect' and row['material']
            if send in CONTROLS and flagged != (CONTROLS[send][2] == 'material'):
                raise SystemExit(f'VOID: {path} misses the {send}')
            marks.setdefault(send, []).append(flagged)
    return {send: values for send, values in marks.items() if send not in CONTROLS}


def final(folder, key_folder, review_files):
    """The verdict fixed before the send (council rounds 20 and 21)."""
    dates = tally(folder)
    key = json.loads((Path(key_folder) / 'key.json').read_text())
    marks = material(review_files, key)
    verdicts = {}
    for counting in ('agreed', 'either'):
        flagged = {send for send, values in marks.items() if (all(values) if counting == 'agreed' else any(values))}
        per_topic = all(sum(f'v2-d{d}|{topic}' in flagged for d in (1, 2)) <= sum(f'frozen-d{d}|{topic}' in flagged for d in (1, 2))
                        for topic in TOPICS)
        completion_sound = not any(f'v2-d{d}|{topic}' in flagged for topic in COMPLETION for d in (1, 2))
        declines_justified = not any(send in flagged for send in dates['new_declines'])
        if not dates['mechanism']:
            verdicts[counting] = 'inconclusive (the frozen arm did not date the signed completion at the annual filing)'
        elif dates['fixed'] and dates['kept'] and per_topic and completion_sound and declines_justified:   # a lost v2 answer fails `fixed` or `kept`: no topic lists `lost`
            verdicts[counting] = 'moves'
        else:
            verdicts[counting] = 'closes'
    verdict = verdicts['agreed'] if verdicts['agreed'] == verdicts['either'] else 'inconclusive (the reviewers disagree on a deciding item)'
    print(f'mechanism {dates["mechanism"]}; completion fixed {dates["fixed"]}; controls kept {dates["kept"]}; new declines {dates["new_declines"]}; '
          f'new losses {dates["new_losses"]}')
    print(f'by counting: {verdicts}')
    print(f'VERDICT: {verdict}')
    return verdict


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'check':
        check()
    elif command == 'send':
        send(sys.argv[2])
    elif command == 'tally':
        tally(sys.argv[2])
    elif command == 'reading':
        reading(*sys.argv[2:4])
    elif command == 'final':
        final(sys.argv[2], sys.argv[3], sys.argv[4:])
    else:
        sys.exit(__doc__)
