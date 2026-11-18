"""Gate 1's reading measured with a blinded reference control outside the 44 (DESIGN.md, D623). $0 in API calls: the writers and
readers are read-only subscription sessions.

  python3 refcontrol.py inputs                                   # the writers' input files (writers/)
  python3 refcontrol.py accept <writer> <source> <answers.jsonl>  # check a writer's answers; prints refusals to send back once
  python3 refcontrol.py reading <run folder> <key folder>         # the blind reading folder (a Stage A run folder) and its key
  python3 refcontrol.py score <run folder> <key folder>           # per arm, settled faults per line both ways; the review list
"""
import collections
import copy
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
STAGE_A = ROOT / 'clean-arch/step4-2026-11-10/stage_a'
LADDER = ROOT / 'clean-arch/step4-2026-11-10/ladder'
sys.path[:0] = [str(STAGE_A), str(LADDER), str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
import accounting  # noqa: E402
import build_reader_packets  # noqa: E402
import collect_readings as collector  # noqa: E402
import ladder_step  # noqa: E402
import stage_a  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

DATA = ROOT / 'poc/data'
SOURCES = {'fortnight': (DATA / 'clean-carried-run-2026-11-16/c1/cases/cases.json', DATA / 'clean-carried-run-2026-11-16/stage-a'),
           'week-10-06': (DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json',
                          DATA / 'clean-second-week-2026-11-15/week-continued/stage-a')}
WRITERS = ('ref-codex', 'ref-claude')
ARMS = ('frozen',) + WRITERS
SOUND = [('july', 'c3/clean-5'), ('july', 'c1/clean-7')]           # both families marked clean on every mark (split probe reading)
SOUND_RUN = DATA / 'clean-split-probe-2026-11-16/frozen/send-1/outcomes.jsonl'
JULY_STORED = DATA / 'clean-e2e-full-2026-11-13/stage-a/send-1/outcomes.jsonl'
JULY_CASES = [DATA / f'clean-e2e-full-2026-11-13/c{n}/cases/cases.json' for n in (1, 2, 3)]
WRONG = {   # planted-wrong controls: (stored July case, the edit, the mark a reader must fail)
    'control|gap': ('c2/clean-8', 'gap', 'R'),
    'control|other-question': ('c3/clean-13', 'other question', 'Q'),
}
SHUFFLE_SEED = 20261119
HARD = ('Q', 'L', 'R', 'N')                                        # gate 1's lines 1 to 4


def research_list():
    return universe.load(str(ROOT / 'poc' / 'universe.json'))


def population():
    """[(source, name, case, stored first send)] for every topic of the two sources; refuses one that is among the 44."""
    the_44 = {case['thesis']['description'] for case in json.loads((STAGE_A / 'cases.json').read_text())}
    out = []
    for source, (cases_path, folder) in SOURCES.items():
        stored = {row['case']: row for row in map(json.loads, (folder / 'send-1/outcomes.jsonl').read_text().splitlines()) if row['pass'] == 1}
        for case in json.loads(cases_path.read_text()):
            if case['thesis']['description'] in the_44:
                raise SystemExit(f"{source}:{case['case']} is among the 44 (D426)")
            out.append((source, case['case'], case, stored[case['case']]))
    if len(out) != 26:
        raise SystemExit(f'{len(out)} topics, not 26')
    return out


def check_of(case, rl):
    def check(answer):
        return ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=stage_a.COMPANY, research_list=rl,
                                        repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                        beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
    return check


def inputs():
    """writers/<source>.md: the step's system text and schema once, then each topic's user message exactly as the step sends it."""
    texts, rl = stage_a.request_texts(), research_list()
    folder = HERE / 'writers'
    folder.mkdir(exist_ok=True)
    by_source = collections.defaultdict(list)
    for source, name, case, _ in population():
        by_source[source].append((name, ladder_step.user_text(stage_a.payload_for(case, rl), texts['closing'])))
    for source, topics in by_source.items():
        parts = ['# The answer-choice step\'s requests for 13 topics', '', '## The system text (the same for every topic)', '', texts['system'],
                 '', '## The answer schema (strict JSON; the same for every topic)', '', json.dumps(texts['schema'], ensure_ascii=False, indent=1), '']
        for name, user in topics:
            parts += [f'## Topic {name}: the user message', '', user, '']
        (folder / f'{source}.md').write_text('\n'.join(parts))
    print({source: len(topics) for source, topics in by_source.items()})


def accepted(answer_obj, case, rl):
    """(row or None, reasons): a writer's answer through the schema check and the step's checks, rendered as the step renders it."""
    text = json.dumps(answer_obj, ensure_ascii=False)
    schema_errors = model.check_schema(json.loads(text), stage_a.request_texts()['schema'])
    if schema_errors:
        return None, [f'the answer does not fit the schema: {error}' for error in schema_errors]
    answer = ladder_step.parse_exactly(text)
    reasons, passage = check_of(case, rl)(answer)
    if reasons:
        return None, reasons
    if answer.get('no_ladder') is not None:
        return {'status': 'no ladder', 'reason': answer['no_ladder'], 'answer': answer, 'passage': None, 'view': None}, []
    view = ladder_step.write_view(answer['ladder'], passage, thesis=case['thesis'], article_day=case['item']['publication_date'],
                                  company=stage_a.COMPANY, research_list=rl)
    return json.loads(ladder_step.as_json({'status': 'ladder', 'reason': None, 'answer': answer, 'passage': passage, 'view': view})), []


def accept(writer, source, answers_path):
    """Writes writers/accepted-<writer>-<source>.json ({topic: row}) and prints the refusals (to send back once)."""
    rl = population_cases = None
    rl = research_list()
    cases = {name: case for src, name, case, _ in population() if src == source}
    given = {}
    for line in Path(answers_path).read_text().splitlines():
        line = line.strip()
        if line.startswith('{'):
            entry = json.loads(line)
            given[entry['topic']] = entry['answer']
    if set(given) != set(cases):
        raise SystemExit(f'answers for {sorted(given)}; topics are {sorted(cases)}')
    out_path = HERE / 'writers' / f'accepted-{writer}-{source}.json'
    out = json.loads(out_path.read_text()) if out_path.exists() else {}
    refused = {}
    for name, answer in given.items():
        if name in out:
            continue
        row, reasons = accepted(answer, cases[name], rl)
        if row is None:
            refused[name] = reasons
        else:
            out[name] = row
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(f'{writer} {source}: accepted {len(out)} of 13; refused {len(refused)}')
    for name, reasons in refused.items():
        print(f'  {name}: {reasons}')
    return refused


def july_case(name):
    return next(case for path in JULY_CASES for case in json.loads(path.read_text()) if case['case'] == name)


def controls():
    """[(row, case, expected)]: the two sound controls as stored, and the two planted-wrong ones (stored July ladders, edited once)."""
    out = []
    stored_sound = {row['case']: row for row in map(json.loads, SOUND_RUN.read_text().splitlines())}
    for _, name in SOUND:
        row = copy.deepcopy(stored_sound[f'frozen|july:{name}'])
        out.append((dict(row, case=f'control|sound-{name.split("/")[1]}', **{'pass': 1}), july_case(name), {'all': 'holds'}))
    stored = {row['case']: row for row in map(json.loads, JULY_STORED.read_text().splitlines()) if row['pass'] == 1}
    for control, (name, edit, mark) in WRONG.items():
        row = copy.deepcopy(stored[name])
        if row['status'] != 'ladder':
            raise SystemExit(f'{control}: the stored send of {name} wrote no ladder')
        case = july_case(name)
        answer = ladder_step.parse_exactly(row['requests'][-1]['answer_text'])        # the stored answer, every number exact
        if edit == 'gap':
            if not answer['ladder'].get('figure'):
                raise SystemExit(f'{control}: {name} is not a figure')
            ranges = answer['ladder']['figure']['ranges']
            ranges[2]['lo'] = ranges[2]['lo'] + (ranges[2]['hi'] - ranges[2]['lo']) / 2   # a gap between the second and the middle rung
        else:
            answer['ladder']['question'] = 'Will NVIDIA announce a new chief executive officer before the due day?'
        view = ladder_step.write_view(answer['ladder'], row['passage'], thesis=case['thesis'], article_day=case['item']['publication_date'],
                                      company=stage_a.COMPANY, research_list=research_list())        # rendered as the step renders it
        row = json.loads(ladder_step.as_json(dict(row, answer=answer, view=view)))
        out.append((dict(row, case=control, **{'pass': 1}), case, {mark: 'fails'}))
    return out


def reading(run_folder, key_folder):
    run_folder, key_folder = Path(run_folder), Path(key_folder)
    if key_folder.resolve().is_relative_to(ROOT.resolve()):
        raise SystemExit('the key folder must sit outside the repository')
    rl = research_list()
    rows, cases = [], {}
    for source, name, case, stored in population():
        for arm in ARMS:
            if arm == 'frozen':
                row = stored
            else:
                accepted_rows = json.loads((HERE / 'writers' / f'accepted-{arm}-{source}.json').read_text())
                if name not in accepted_rows:
                    continue                                           # refused twice: the writer's failure, not read
                row = accepted_rows[name]
            label = f'{arm}|{source}:{name}'
            rows.append(dict(row, case=label, **{'pass': 1}))
            cases[label] = dict(case, case=label)
    expected = {}
    for row, case, marks in controls():
        rows.append(row)
        cases[row['case']] = dict(case, case=row['case'])
        expected[row['case']] = marks
    run_folder.mkdir(parents=True, exist_ok=False)
    (run_folder / 'send-1').mkdir()
    (run_folder / 'send-1' / 'outcomes.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    (run_folder / 'cases.json').write_text(json.dumps(list(cases.values()), ensure_ascii=False, indent=1) + '\n')
    order = sorted(rows, key=lambda row: row['case'])
    random.Random(SHUFFLE_SEED).shuffle(order)
    (run_folder / 'readers').mkdir()
    key, packets = {}, []
    for number, row in enumerate(order, start=1):
        key[str(number)] = [row['case'], 1]
        if (number - 1) % build_reader_packets.ITEMS_A_PACKET == 0:
            packets.append([])
        packets[-1].append({'item': number, **build_reader_packets.item_of(row, cases[row['case']], rl)})
    for packet_number, packet in enumerate(packets, start=1):
        (run_folder / 'readers' / f'packet-{packet_number}.json').write_text(json.dumps(packet, indent=1, ensure_ascii=False) + '\n')
    key_folder.mkdir(parents=True, exist_ok=True)
    (key_folder / 'key.json').write_text(json.dumps(key, indent=1) + '\n')
    (key_folder / 'controls-expected.json').write_text(json.dumps(expected, indent=1) + '\n')
    counts = collections.Counter(row['case'].split('|')[0] for row in rows)
    print(f'{len(rows)} items in {len(packets)} packets: {dict(counts)}')


def settled(rows, mark, unresolved_as):
    """A mark from the two families: their value where they agree, else counted as `unresolved_as`."""
    values = [row[mark] for row in rows]
    return values[0] if values[0] == values[1] else unresolved_as


def score(run_folder, key_folder):
    key_path = Path(key_folder) / 'key.json'
    key, item_of, outcomes, readers, problems = collector.read_rows(run_folder, key_path)
    if any(found['rows'] or found['unreadable lines'] for found in problems.values()):
        raise SystemExit(f'VOID: rows missing or not valid: {problems}')
    expected = json.loads((Path(key_folder) / 'controls-expected.json').read_text())
    for control, marks in expected.items():
        rows = [readers[reader][(control, 1)] for reader in collector.FAMILIES]
        for mark, value in marks.items():
            if mark != 'all' and any(row[mark] != value for row in rows):
                raise SystemExit(f'VOID: a family missed the planted {control} ({mark})')
    report = {}
    for unresolved_as in ('holds', 'fails'):
        faults = {}
        for send, outcome in outcomes.items():
            rows = [readers[reader][send] for reader in collector.FAMILIES]
            applicable = accounting.marks_that_apply(accounting.kind_of(outcome))
            faults[send[0]] = {mark for mark in applicable if settled(rows, mark, unresolved_as) == 'fails'}
        per_arm = {arm: collections.Counter(mark for case, found in faults.items() if case.startswith(f'{arm}|') for mark in found)
                   for arm in ARMS}
        topics = sorted({case.split('|', 1)[1] for case in faults if not case.startswith('control|')})
        hard = lambda arm, topic: bool(faults.get(f'{arm}|{topic}', {'missing'}) & set(HARD + ('missing',)))
        favour = [topic for topic in topics if hard('frozen', topic) and not hard('ref-codex', topic) and not hard('ref-claude', topic)]
        against = [topic for topic in topics if not hard('frozen', topic) and hard('ref-codex', topic) and hard('ref-claude', topic)]
        sound_faults = {case: sorted(found) for case, found in faults.items() if case.startswith('control|sound') and found}
        reference_faults = {case: sorted(found & set(HARD)) for case, found in faults.items()
                            if case.split('|')[0] in WRITERS and found & set(HARD)}
        report[unresolved_as] = {'faults per arm': {arm: dict(counter) for arm, counter in per_arm.items()},
                                 'topics favouring the references': favour, 'topics against them': against,
                                 'sound controls with settled faults': sound_faults, 'reference items with settled hard-line faults': reference_faults}
    print(json.dumps(report, indent=1))
    return report


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else ''
    if command == 'inputs':
        inputs()
    elif command == 'accept':
        accept(*sys.argv[2:5])
    elif command == 'reading':
        reading(*sys.argv[2:4])
    elif command == 'score':
        score(*sys.argv[2:4])
    else:
        sys.exit(__doc__)
