"""The period split's probe (DESIGN.md v4 §3 and §0c item 4; D616–D620): the frozen answer-choice step and the split version, three
sends each, on 13 stored topics. Nothing here judges a ladder; `score_split.py` applies the counts and the reading's verdict.

`check` ($0) builds every request with the production builder and requires:
- the population as fixed below, C1 derived again from the two-year census by its written rule;
- each control request equal to the topic's stored first request (sha256 over sorted keys) and its keys in the stored order;
- each split first request equal to the control except the schema's `no_ladder` and the system text's decline list (exactly
  `ladder_split.SYSTEM_REPLACEMENTS`), and each yearly re-ask equal to the split first
  request except the yearly line after the closing text;
- every stored control answer that wrote answer choices accepted by the step's checks; a synthetic split refusal of each T topic
  accepted, and mutants (an ended year, a split named again in a yearly re-ask, stray periods) refused;
- the spend: the most calls the arms can make, the sum of their worst-case reserves, the stored charges of the same step, and each
  arm's cap (together $0.40).
It then writes a record binding the code and request files, the population and every request's sha256.

`send` rebuilds every request, refuses unless each equals the record, and sends the frozen arm through Stage A's runner and the split
arm through `run_split` (the same runner with the split step), each under its own cap of the answer-choice runner's limit, behind a
guard that stops every later attempt once an answer costs more than its reserve.

  python3 probe_split.py check
  python3 probe_split.py send <new data folder>
"""
import concurrent.futures
import copy
import hashlib
import json
import os
import sys
import threading
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE_A = ROOT / 'clean-arch/step4-2026-11-10/stage_a'
LADDER = ROOT / 'clean-arch/step4-2026-11-10/ladder'
sys.path[:0] = [str(STAGE_A), str(LADDER), str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
import budget  # noqa: E402
import ladder_split  # noqa: E402
import ladder_step  # noqa: E402
import model_calls  # noqa: E402
import stage_a  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

DATA = ROOT / 'poc/data'
SOURCES = {   # source: (its cases files, its stored Stage A folder holding the frozen step's sends of those cases); none is the 44 (D426)
    'fortnight': ([DATA / 'clean-carried-run-2026-11-16/c1/cases/cases.json'], DATA / 'clean-carried-run-2026-11-16/stage-a'),
    'week-10-06': ([DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json'], DATA / 'clean-second-week-2026-11-15/week-continued/stage-a'),
    'july': ([DATA / f'clean-e2e-full-2026-11-13/c{n}/cases/cases.json' for n in (1, 2, 3)], DATA / 'clean-e2e-full-2026-11-13/stage-a'),
}
THE_44 = STAGE_A / 'cases.json'          # the theses D426 stopped tuning the step on: no topic of the probe is one of them
# The population (DESIGN.md v4 §3, narrowed by round 162 to topics outside the 44), fixed before any send:
# - T: the two stored topics asking one quantity for two open years, declined in every stored send (DESIGN-REVIEW.md, "The cases");
# - C1: by the rule in `c1_by_rule` (stored topics outside the 44 naming exactly two years, every stored send a ladder for one of
#   them, most stored sends first), at least two of them with both years open on the item's day;
# - C2: the two topics outside the 44 that both blind readers of the D436 reading called one bet with a second side
#   (unlisted-parts/d436-reading/RESULT.md: commodity DRAM with the shortage and graphics memory; custom-ASIC against GPU purchases);
# - C3: the guards, the Intel stake and Firmus.
# - M (the several-products memory topic) is left out: its only stored instance is one of the 44.
TOPICS = {
    'T': [('week-10-06', 'c1/clean-12'), ('week-10-06', 'c1/clean-4')],
    'C1': [('fortnight', 'c1/clean-11'), ('fortnight', 'c1/clean-9'), ('fortnight', 'c1/clean-13'), ('july', 'c3/clean-5'),
           ('july', 'c2/clean-5'), ('july', 'c1/clean-7')],
    'C2': [('july', 'c3/clean-7'), ('july', 'c2/clean-10')],
    'C3': [('july', 'c1/clean-2'), ('july', 'c1/clean-11')],
}
CENSUS = HERE / 'two-year-topics.jsonl'
ARMS = ('frozen', 'split')
PASSES = [1, 2, 3]
CAPS = {'frozen': 0.15, 'split': 0.25}          # together the probe's ceiling, $0.40 (DESIGN.md v4 §0c item 4)
RECORD = HERE / 'check-passed.json'
CODE_FILES = [LADDER / 'ladder_split.py', LADDER / 'ladder_step.py', LADDER / 'candidate-system.txt', LADDER / 'candidate-closing.txt',
              LADDER / 'candidate-schema.json', STAGE_A / 'stage_a.py', Path(__file__)]


def descriptions_of_the_44():
    return {case['thesis']['description'] for case in json.loads(THE_44.read_text())}


def c1_by_rule():
    """C1's written rule over the two-year census: topics outside the 44 naming exactly two years whose every stored send wrote a
    ladder (a figure or an event), most stored sends first (ties in census order), each found once in the probe's sources; the
    first six."""
    excluded, candidates = descriptions_of_the_44(), []
    for order, line in enumerate(CENSUS.read_text().splitlines()):
        topic = json.loads(line)
        if topic['description'] in excluded:
            continue
        if len(topic['years']) == 2 and {send['kind'] for send in topic['sends']} <= {'figure', 'event'}:
            candidates.append((-len(topic['sends']), order, topic['description']))
    chosen = []
    for _, _, description in sorted(candidates):
        found = [(source, case['case']) for source, (paths, _) in SOURCES.items() for path in paths
                 for case in json.loads(path.read_text()) if case['thesis']['description'] == description]
        if len(found) != 1:
            raise SystemExit(f'C1: {len(found)} stored cases carry "{description[:60]}", not one')
        chosen.append(found[0])
    return chosen[:6]


def open_years(case, research_list):
    """This year and next as of the item's day, written as a calendar year (the step's own year rules)."""
    this = int(case['item']['publication_date'][:4])
    return [str(this), str(this + 1)]


def load_topics():
    """(group, source, stored case name, case) for every topic; refuses a topic missing or found twice."""
    found = []
    for group, entries in TOPICS.items():
        for source, name in entries:
            cases = [case for path in SOURCES[source][0] for case in json.loads(path.read_text()) if case['case'] == name]
            if len(cases) != 1:
                raise SystemExit(f'{source} {name}: {len(cases)} cases found, not one')
            found.append((group, source, name, cases[0]))
    return found


def arm_cases(topics, arm):
    """Each arm's cases under names unique across arms ('<arm>|<source>:<case>'); the name is a label only, never sent."""
    return [dict(case, case=f'{arm}|{source}:{name}') for _, source, name, case in topics]


def texts_of(arm):
    frozen = stage_a.request_texts()
    return frozen if arm == 'frozen' else dict(frozen, system=ladder_split.split_system(frozen['system']),
                                                 schema=ladder_split.split_schema(frozen['schema']))


def built(case, texts, research_list, closing=None):
    user = ladder_step.user_text(stage_a.payload_for(case, research_list), texts['closing'] if closing is None else closing)
    return model.build_request(stage_a.SETTING, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def yearly_closing(texts, year, other):
    return texts['closing'] + '\n\n' + ladder_split.RESTRICTION.format(year=year, other=other)


def key_order(value):
    if isinstance(value, dict):
        return [(key, key_order(item)) for key, item in value.items()]
    if isinstance(value, list):
        return [key_order(item) for item in value]
    return None


def stored_first(source, name):
    rows = [json.loads(line) for line in (SOURCES[source][1] / 'send-1/outcomes.jsonl').read_text().splitlines() if line]
    rows = [row for row in rows if row['case'] == name and row['pass'] == 1]
    if len(rows) != 1:
        raise SystemExit(f'{source} {name}: {len(rows)} stored first sends, not one')
    return rows[0]


def frozen_check(case, research_list):
    def check(answer):
        return ladder_step.check_answer(answer, thesis=case['thesis'], article=case['item'], company=stage_a.COMPANY, research_list=research_list,
                                        repair_quote=extraction.repair_quote, normalise=extraction.normalise, quote_tokens=extraction._quote_tokens,
                                        beyond_next_year=extraction.beyond_next_year, binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
    return check


def split_check_for(case, research_list):
    return lambda year: ladder_split.checker(frozen_check(case, research_list), article_day=case['item']['publication_date'],
                                             company=stage_a.COMPANY, research_list=research_list, year=year)


def requests_of(topics, research_list):
    """Every request the arms can send first: the frozen request, the split first request and each yearly re-ask, by sha256."""
    texts = {arm: texts_of(arm) for arm in ARMS}
    out = {'frozen': {}, 'split': {}, 'yearly': {}}
    for _, source, name, case in topics:
        out['frozen'][f'{source}:{name}'] = model.request_identity(built(case, texts['frozen'], research_list))[1]
        out['split'][f'{source}:{name}'] = model.request_identity(built(case, texts['split'], research_list))[1]
        this, following = open_years(case, research_list)
        for year, other in ((this, following), (following, this)):
            closing = yearly_closing(texts['split'], year, other)
            out['yearly'][f'{source}:{name}@{year}'] = model.request_identity(built(case, texts['split'], research_list, closing))[1]
    return out


def code_digest():
    return hashlib.sha256(b''.join(path.read_bytes() for path in CODE_FILES)).hexdigest()


def check():
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    texts = {arm: texts_of(arm) for arm in ARMS}
    failures = []
    derived = c1_by_rule()
    if derived != TOPICS['C1']:
        failures.append(f'C1 by its rule is {derived}, not the fixed list')
    topics = load_topics()
    in_44 = [f'{source}:{name}' for _, source, name, case in topics if case['thesis']['description'] in descriptions_of_the_44()]
    if in_44:
        failures.append(f'topics that are among the 44 (D426): {in_44}')
    census = {json.loads(line)['description']: json.loads(line)['years'] for line in CENSUS.read_text().splitlines()}
    both_open = [name for group, _, name, case in topics if group == 'C1' and census[case['thesis']['description']] == open_years(case, research_list)]
    print(f'C1 whose two named years are both open on the item\'s day (census years): {both_open}')
    if len(both_open) < 2:
        failures.append('fewer than two C1 topics with an open base year')
    judged = 0
    for group, source, name, case in topics:
        control, split = built(case, texts['frozen'], research_list), built(case, texts['split'], research_list)
        stored = stored_first(source, name)
        same = model.request_identity(control)[1] == stored['requests'][0]['request_sha256']
        without = [copy.deepcopy(request) for request in (control, split)]
        for request in without:
            del request['response_format']['json_schema']['schema']['properties']['no_ladder']
        frozen_system = texts['frozen']['system']
        system_index = next(i for i, message in enumerate(control['messages']) if message['content'] == frozen_system)
        without[1]['messages'][system_index]['content'] = frozen_system if split['messages'][system_index]['content'] == ladder_split.split_system(frozen_system) else None
        only_schema = (without[0] == without[1] and key_order(without[0]) == key_order(without[1]) and texts['split']['system'] != frozen_system
                       and split['response_format']['json_schema']['schema']['properties']['no_ladder'] == texts['split']['schema']['properties']['no_ladder'])
        this, following = open_years(case, research_list)
        yearly_ok = True
        for year, other in ((this, following), (following, this)):
            yearly = built(case, texts['split'], research_list, yearly_closing(texts['split'], year, other))
            first_user, yearly_user = split['messages'][-1]['content'], yearly['messages'][-1]['content']
            line = '\n\n' + ladder_split.RESTRICTION.format(year=year, other=other)
            body = copy.deepcopy(yearly)
            body['messages'][-1]['content'] = first_user
            yearly_ok = yearly_ok and body == split and first_user.count(texts['split']['closing']) == 1 and \
                yearly_user == first_user.replace(texts['split']['closing'], texts['split']['closing'] + line)
        answer_state = f"stored send '{stored['status']}'"
        if stored['status'] == 'ladder':
            reasons, _ = frozen_check(case, research_list)(ladder_step.parse_exactly(stored['requests'][-1]['answer_text']))
            judged += 1
            answer_state = 'stored ladder accepted' if reasons == [] else f'STORED LADDER REFUSED: {reasons}'
        print(f'{group:3} {source}:{name:13} control equals stored: {same}; split differs only in no_ladder and the system decline list: {only_schema}; '
              f'yearly re-asks differ only by the line: {yearly_ok}; {answer_state}')
        if not (same and only_schema and yearly_ok) or 'REFUSED' in answer_state:
            failures.append(f'{source}:{name}')
    for _, source, name, case in (t for t in topics if t[0] == 'T'):
        check_for = split_check_for(case, research_list)
        this, following = open_years(case, research_list)

        def answer(no_ladder):
            return ladder_step.parse_exactly(json.dumps({'no_ladder': no_ladder, 'ladder': None}))
        synthetic = answer({'case': ladder_split.SPLIT_CASE, 'reason': 'one quantity for each year', 'periods': [this, following]})
        valid = model.check_schema(json.loads(json.dumps(synthetic, default=float)), texts['split']['schema']) + check_for(None)(synthetic)[0]
        ended = check_for(None)(answer({'case': ladder_split.SPLIT_CASE, 'reason': 'x', 'periods': [str(int(this) - 1), this]}))[0]
        again = check_for(this)(answer({'case': ladder_split.SPLIT_CASE, 'reason': 'x', 'periods': [this, following]}))[0]
        stray = check_for(None)(answer({'case': 'no_main', 'reason': 'x', 'periods': [this, following]}))[0]
        print(f'T {source}:{name}: synthetic split {valid or "accepted"}; mutants refused: ended year {bool(ended)}, '
              f'split again in a yearly re-ask {bool(again)}, stray periods {bool(stray)}')
        if valid or not (ended and again and stray):
            failures.append(f'synthetic or mutant answers of {source}:{name}')
    sends = len(topics) * len(PASSES)
    calls = {'frozen': sends * 2, 'split': sends * 2 * 3}          # a send and its one resend; the split adds two yearly re-asks, each resent
    attempts = {arm: count * budget.ATTEMPTS for arm, count in calls.items()}   # each call tried up to three times on a transport failure
    output_bytes = 4 * stage_a.SETTING.max_output_tokens          # an estimate of the previous answer a resend carries (4 bytes a token)
    rate_in = model.PRICES[stage_a.SETTING.model][0]

    def worst_first_and_resend(request):
        first = budget.worst_cost(request)
        return first + first + output_bytes * rate_in / 1e6       # the resend: the same request, the previous answer and its reasons appended
    worst = {'frozen': 0.0, 'split': 0.0}
    for *_, case in topics:
        worst['frozen'] += worst_first_and_resend(built(case, texts['frozen'], research_list))
        worst['split'] += worst_first_and_resend(built(case, texts['split'], research_list))
        this, following = open_years(case, research_list)
        for year, other in ((this, following), (following, this)):
            worst['split'] += worst_first_and_resend(built(case, texts['split'], research_list, yearly_closing(texts['split'], year, other)))
    worst = {arm: value * len(PASSES) * budget.ATTEMPTS for arm, value in worst.items()}
    print(f'topics {len(topics)}; stored ladders judged {judged}; sends {sends} an arm; most calls {calls}, most attempts with transport '
          f'retries {attempts}; the sum of worst-case reserves if every attempt were made at its worst (resends estimated with an answer '
          f'of {stage_a.SETTING.max_output_tokens} tokens at 4 bytes a token) {{{", ".join(f"{a}: ${w:.2f}" for a, w in worst.items())}}}; '
          f'caps {CAPS} (${sum(CAPS.values()):.2f}). Every attempt is reserved at its own worst cost before it is sent, so an arm stops '
          f'at its cap (NOT MEASURED), and the caps hold while every charge stays within its reserve')
    if failures or len(topics) != sum(len(entries) for entries in TOPICS.values()):
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'code_sha256': code_digest(), 'requests': requests_of(topics, research_list)}, indent=1) + '\n')
    print(f'check passed; record {RECORD.name}')
    return 0


def run_split(cases, passes, folder, cap_usd, *, research_list, texts, transport=None, workers=8):
    """`stage_a.run` with the split step: the same folder layout, limit, archives, labels and outcome rows; a split send's row adds
    `periods` and `children` (each year's outcome with its view, built as Stage A builds one)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    limit = stage_a.StageALimit(cap_usd, folder / 'spend.jsonl', attempt=transport)
    checksum = hashlib.sha256(json.dumps({'system': texts['system'], 'closing': texts['closing'], 'schema': texts['schema'],
                                          'setting': [stage_a.SETTING.model, stage_a.SETTING.reasoning_effort, stage_a.SETTING.max_output_tokens]},
                                         ensure_ascii=False).encode()).hexdigest()[:16]
    call_config = SimpleNamespace(provider='openai', version='clean-ladder-split-probe', checksum=checksum)
    archives, outcome_files = {}, {}
    for pass_number in passes:
        (folder / f'send-{pass_number}').mkdir()
        archives[pass_number] = model.Archive(str(folder / f'send-{pass_number}' / 'archive.sqlite'))
        outcome_files[pass_number] = folder / f'send-{pass_number}' / 'outcomes.jsonl'
    write_lock, written = threading.Lock(), []

    def view_of(outcome, case):
        if outcome['status'] != 'ladder':
            return None
        return ladder_step.write_view(outcome['answer']['ladder'], outcome['passage'], thesis=case['thesis'],
                                      article_day=case['item']['publication_date'], company=stage_a.COMPANY, research_list=research_list)

    def work(job):
        case, pass_number = job
        labelled = SimpleNamespace(request_number=0)
        labelled.send = lambda provider, request: limit.send_labelled(f"{case['case']}|{pass_number}|{labelled.request_number}", provider, request)
        call_model = model_calls.model_caller(model, archives[pass_number], call_config, stage_a.SETTING, labelled)

        def counted_call(system_text, user_text, schema):
            labelled.request_number += 1
            return call_model(system_text, user_text, schema)
        try:
            outcome = ladder_split.ladder_for_thesis_split(stage_a.payload_for(case, research_list), system_text=texts['system'],
                                                           closing_text=texts['closing'], schema=texts['schema'], call_model=counted_call,
                                                           check_for=split_check_for(case, research_list))
            row = {'case': case['case'], 'pass': pass_number, 'status': outcome['status'], 'reason': outcome['reason'],
                   'requests': outcome['requests'], 'answer': outcome['answer'], 'passage': outcome['passage'], 'view': view_of(outcome, case)}
            if outcome['status'] == 'split':
                row['periods'] = outcome['periods']
                row['children'] = {year: dict(child, view=view_of(child, case)) for year, child in outcome['children'].items()}
            with write_lock:
                with outcome_files[pass_number].open('a') as handle:
                    handle.write(ladder_step.as_json(row) + '\n')
                    handle.flush()
                    os.fsync(handle.fileno())
                written.append((case['case'], pass_number, outcome['status']))
        except (stage_a.Stopped, budget.OverBudget):
            return
        except Exception as error:                      # not an answer's own fault: stop every worker
            limit.stop(f"{case['case']} pass {pass_number}: {type(error).__name__}: {error}")
            return

    jobs = [(case, pass_number) for pass_number in passes for case in cases]
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        list(pool.map(work, jobs))
    return written, limit, len(jobs)


class BreachGuard:
    """The transport each attempt goes through. An answer whose reported cost is above its attempt's worst-case reserve is returned
    (so the ledger charges it), and no new attempt is sent after it: each raises `stage_a.Stopped`."""

    def __init__(self, transport=None):
        self.transport = transport or (lambda provider, request: model.openai_transport(provider, request, max_attempts=1))
        self.breaches, self.lock = [], threading.Lock()

    def __call__(self, provider, request):
        with self.lock:
            if self.breaches:
                raise stage_a.Stopped('a breach of an attempt reserve was seen')
        response = self.transport(provider, request)
        charged, reserve = budget.cost(request, response), budget.worst_cost(request)
        if charged is not None and charged > reserve:
            with self.lock:
                self.breaches.append((round(charged, 6), round(reserve, 6)))
        return response


def over_reserve(spend_path):
    reserves, out = {}, []
    for line in Path(spend_path).read_text().splitlines():
        entry = json.loads(line)
        if 'reserve' in entry:
            reserves[entry['attempt']] = entry['reserve']
        elif entry['charge'] > reserves[entry['attempt']] + 1e-12:
            out.append((entry['attempt'], entry['charge'], reserves[entry['attempt']]))
    return out


def send(folder, *, transport=None):
    record = json.loads(RECORD.read_text()) if RECORD.exists() else None
    if record is None or record['code_sha256'] != code_digest():
        raise SystemExit('no check record for these files: run `check` first')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    topics = load_topics()
    if requests_of(topics, research_list) != record['requests']:
        raise SystemExit('REFUSED: the requests differ from the checked record')
    folder, guard = Path(folder), BreachGuard(transport)
    for arm in ARMS:
        cases, texts = arm_cases(topics, arm), texts_of(arm)
        runner = stage_a.run if arm == 'frozen' else run_split
        written, limit, job_count = runner(cases, PASSES, folder / arm, CAPS[arm], research_list=research_list, texts=texts, transport=guard)
        (folder / arm / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False, indent=1) + '\n')
        known, in_full, _ = stage_a.ledger_total(folder / arm / 'spend.jsonl')
        over = over_reserve(folder / arm / 'spend.jsonl')
        print(f'{arm}: {len(written)} of {job_count} sends have an outcome; spent ${known + in_full:.4f}; attempts charged above their reserve: {len(over)}')
        if over or guard.breaches:
            raise SystemExit(f'{arm} BREACH: ledger {over}; seen at the transport {guard.breaches}')
        if limit.stopped or len(written) != job_count:
            raise SystemExit(f'{arm} STOPPED: {limit.stop_reason}. NOT MEASURED.')
    return 0


if __name__ == '__main__':
    arguments = sys.argv[1:]
    mode = arguments[0] if arguments else ''
    sys.exit(check() if mode == 'check' else send(arguments[1]) if mode == 'send' and len(arguments) == 2 else f'usage: {__doc__}')
