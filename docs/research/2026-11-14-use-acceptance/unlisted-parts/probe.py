"""DESIGN.md's probe of arm A.

`check` ($0) builds every topic's control and changed request with the production builder and requires:
- the control equal in content to its stored first request (the archive's sha256 over sorted keys);
- the changed request equal to the control with exactly the arm's replacements;
- every stored first answer that wrote answer choices, parsed from the model's own text as the step parses it, accepted by the
  step's code checks (an empty list of reasons); a mutant answer refused; a synthetic answer that follows the changed request accepted.
It then writes a record binding the arm files, the population and every request's sha256.

`send` rebuilds every request from the same loaded cases and texts, refuses the send unless each equals the record, and then sends
the unchanged and the changed requests, three passes each, through Stage A's runner and spending limit. An answer whose cost is
above its attempt's reserve stops every later attempt at once (BreachGuard); after each arm the ledger is read too, and either
finding stops the probe as a breach.

  python3 probe.py [--arm a2] check
  python3 probe.py [--arm a2] send <new data folder>
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE_A = ROOT / 'clean-arch/step4-2026-11-10/stage_a'
sys.path[:0] = [str(HERE), str(STAGE_A), str(ROOT / 'clean-arch/step4-2026-11-10/ladder'), str(ROOT / 'src'), str(ROOT / 'clean-arch/e2e-2026-11-09')]
import ladder_step  # noqa: E402
import make_arm  # noqa: E402
import make_arm2  # noqa: E402
import make_arm3  # noqa: E402
import stage_a  # noqa: E402
from hivemind import extraction, model, universe  # noqa: E402

DATA = ROOT / 'poc/data'
SOURCES = {   # source: (its cases files, its stored Stage A folder)
    'fortnight': ([DATA / 'clean-carried-run-2026-11-16/c1/cases/cases.json'], DATA / 'clean-carried-run-2026-11-16/stage-a'),
    'week-10-06': ([DATA / 'clean-second-week-2026-11-15/week-continued/c1/cases/cases.json'], DATA / 'clean-second-week-2026-11-15/week-continued/stage-a'),
    'july': ([DATA / f'clean-e2e-full-2026-11-13/c{n}/cases/cases.json' for n in (1, 2, 3)], DATA / 'clean-e2e-full-2026-11-13/stage-a'),
}
TOPICS_A = {
    'motivating': [('fortnight', 'c1/clean-6'), ('fortnight', 'c1/clean-7'), ('fortnight', 'c1/clean-13'), ('week-10-06', 'c1/clean-1'),
                   ('week-10-06', 'c1/clean-3'), ('july', 'c1/clean-5'), ('july', 'c3/clean-7')],
    'regression watch': [('fortnight', 'c1/clean-2'), ('fortnight', 'c1/clean-3'), ('fortnight', 'c1/clean-5'), ('fortnight', 'c1/clean-9'),
                         ('july', 'c1/clean-6')],
    'harm control': [('fortnight', f'c1/clean-{n}') for n in (1, 4, 8, 10, 11, 12)],
}
ARMS = ('control', 'changed')
TOPICS_A2 = {**TOPICS_A,   # DESIGN-A2.md v2: the blind D436 reading's groups (d436-reading/RESULT.md)
             'refusal control': [('week-10-06', 'c1/clean-4'), ('week-10-06', 'c1/clean-12'), ('july', 'c2/clean-6'), ('july', 'c1/clean-13')],
             'recovery': [('july', 'c1/clean-11'), ('july', 'c1/clean-2'), ('july', 'c2/clean-10'), ('week-10-06', 'c1/clean-13')],
             'disputed': [('july', 'c1/clean-15'), ('july', 'c3/clean-3')]}
CONFIGURATIONS = {'a': {'dir': 'arm-a', 'replacements': make_arm.REPLACEMENTS, 'topics': TOPICS_A, 'record': 'check-passed.json'},
                  'a2': {'dir': 'arm-a2', 'replacements': make_arm2.REPLACEMENTS, 'topics': TOPICS_A2, 'record': 'check-passed-a2.json'},
                  'a3': {'dir': 'arm-a3', 'replacements': make_arm3.REPLACEMENTS, 'topics': TOPICS_A2, 'record': 'check-passed-a3.json',
                         'arms': ('control', 'a2', 'changed')}}   # DESIGN-A3.md v11: A2 re-sent the same day beside A3
CAP_PER_ARM = 0.25
PASSES = [1, 2, 3]
ARM = 'a'
TOPICS = TOPICS_A
RECORD = HERE / 'check-passed.json'


def configure(arm):
    """Point the probe at one arm: its files, its exact replacements, its topics and its check record."""
    global ARM, TOPICS, RECORD, ARMS
    ARM, TOPICS, RECORD = arm, CONFIGURATIONS[arm]['topics'], HERE / CONFIGURATIONS[arm]['record']
    ARMS = CONFIGURATIONS[arm].get('arms', ('control', 'changed'))
SYNTHETIC_PART = {'part': 'Whether MIIT caps the quantities approved',
                  'why': 'The outcome names approval with capped quantities against full approval; Yes does not separate them.'}


def config_of(arm):
    """The configuration whose files an arm sends: 'a2' names arm A2 when it is sent beside another arm; 'changed' the configured arm."""
    return 'a2' if arm == 'a2' else ARM


def arm_texts(configuration=None):
    folder = HERE / CONFIGURATIONS[configuration or ARM]['dir']
    return {'system': (folder / 'candidate-system.txt').read_text(), 'closing': (folder / 'candidate-closing.txt').read_text().strip(),
            'schema': json.loads((folder / 'candidate-schema.json').read_text())}


def texts_of(arm):
    return stage_a.request_texts() if arm == 'control' else arm_texts(config_of(arm))


def arm_digest():
    """The sha256 over every sent arm's three files, in the order of ARMS."""
    folders = [HERE / CONFIGURATIONS[config_of(arm)]['dir'] for arm in ARMS if arm != 'control']
    return hashlib.sha256(b''.join((folder / name).read_bytes() for folder in folders
                                   for name in ('candidate-system.txt', 'candidate-closing.txt', 'candidate-schema.json'))).hexdigest()


def load_topics():
    """The configured topics as (group, source, stored case name, case). Refuses a topic that is missing or found twice."""
    found = []
    for group, entries in TOPICS.items():
        for source, name in entries:
            cases = [case for path in SOURCES[source][0] for case in json.loads(path.read_text()) if case['case'] == name]
            if len(cases) != 1:
                raise SystemExit(f'{source} {name}: {len(cases)} cases found, not one')
            found.append((group, source, name, cases[0]))
    return found


def arm_cases(topics, arm):
    """Each arm's cases under names unique across the two arms ('<arm>|<source>:<case>'); the name is a label only, never sent."""
    return [dict(case, case=f'{arm}|{source}:{name}') for _, source, name, case in topics]


def stored_first(source, name):
    rows = [json.loads(line) for line in (SOURCES[source][1] / 'send-1/outcomes.jsonl').read_text().splitlines() if line]
    rows = [row for row in rows if row['case'] == name and row['pass'] == 1]
    if len(rows) != 1:
        raise SystemExit(f'{source} {name}: {len(rows)} stored first sends, not one')
    return rows[0]


def built(case, texts, research_list):
    user = ladder_step.user_text(stage_a.payload_for(case, research_list), texts['closing'])
    return model.build_request(stage_a.SETTING, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def key_order(value):
    """Every object's keys in order, nested: the part of a request a sorted-key sha256 cannot see."""
    if isinstance(value, dict):
        return [(key, key_order(item)) for key, item in value.items()]
    if isinstance(value, list):
        return [key_order(item) for item in value]
    return None


def exact_answer(stored):
    """The stored send's final answer as the step parses the model's own text (every number its exact decimal)."""
    return ladder_step.parse_exactly(stored['requests'][-1]['answer_text'])


def reasons_of(answer, case, research_list):
    reasons, _ = ladder_step.check_answer(copy.deepcopy(answer), thesis=case['thesis'], article=case['item'], company=stage_a.COMPANY,
                                          research_list=research_list, repair_quote=extraction.repair_quote, normalise=extraction.normalise,
                                          quote_tokens=extraction._quote_tokens, beyond_next_year=extraction.beyond_next_year,
                                          binding_horizon_days=extraction.BINDING_HORIZON_DAYS)
    return reasons


def request_shas(topics, research_list):
    return {arm: {case['case']: model.request_identity(built(case, texts_of(arm), research_list))[1] for case in arm_cases(topics, arm)}
            for arm in ARMS}


def check():
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    frozen = stage_a.request_texts()
    sent = [arm for arm in ARMS if arm != 'control']
    if any(key_order(texts_of(arm)['schema']) != key_order(frozen['schema']) for arm in sent):
        raise SystemExit('an arm schema does not keep the frozen schema keys in their order')
    topics = load_topics()
    failures, answers_judged = [], 0
    for group, source, name, case in topics:
        control = built(case, frozen, research_list)
        stored = stored_first(source, name)
        same = model.request_identity(control)[1] == stored['requests'][0]['request_sha256']
        exact = True
        for arm in sent:
            expected = json.dumps(control, ensure_ascii=False)
            for old, new in (pair for pairs in CONFIGURATIONS[config_of(arm)]['replacements'].values() for pair in pairs):
                expected = expected.replace(old, new) if expected is not None and expected.count(old) == 1 else None
            exact = exact and expected is not None and expected == json.dumps(built(case, texts_of(arm), research_list), ensure_ascii=False)
        answer_state = f"not judged: the stored send was '{stored['status']}'"
        if stored['status'] == 'ladder':
            reasons = reasons_of(exact_answer(stored), case, research_list)
            answers_judged += 1
            answer_state = 'accepted' if reasons == [] else f'REFUSED: {reasons}'
        print(f'{group:16} {source}:{name:12} control equals the stored request: {same}; each arm equals control plus its replacements: {exact}; stored answer: {answer_state}')
        if not same or not exact or answer_state.startswith('REFUSED'):
            failures.append(f'{source}:{name}')
    by_name = {f'{source}:{name}': (case, stored_first(source, name)) for _, source, name, case in topics}
    case, stored = by_name['fortnight:c1/clean-7']
    synthetic = exact_answer(stored)
    synthetic['ladder']['not_judged'] = list(synthetic['ladder']['not_judged']) + [SYNTHETIC_PART]
    synthetic_reasons = reasons_of(synthetic, case, research_list)
    mutant = exact_answer(stored)
    mutant['no_ladder'] = 'declined as well'
    mutant_reasons = reasons_of(mutant, case, research_list)
    print(f'synthetic answer following the changed request (clean-7, the cap listed): {synthetic_reasons or "accepted"}')
    print(f'mutant answer (answer choices and a refusal at once): {mutant_reasons or "ACCEPTED"}')
    if synthetic_reasons or not mutant_reasons:
        failures.append('synthetic or mutant answer')
    worst = sum(stage_a.budget.worst_cost(built(case, texts_of(a), research_list)) for a in ARMS for *_, case in topics) * len(PASSES)
    print(f'topics {len(topics)}; stored answers judged {answers_judged}; sends {len(topics) * len(PASSES) * len(ARMS)}; the sum of one worst-case '
          f'reserve a send ${worst:.4f}; each arm held to ${CAP_PER_ARM:.2f} by reservation before every attempt')
    if failures or len(topics) != sum(len(entries) for entries in TOPICS.values()):
        raise SystemExit(f'CHECK FAILED: {failures}')
    RECORD.write_text(json.dumps({'arm_sha256': arm_digest(), 'requests': request_shas(topics, research_list)}, indent=1) + '\n')
    print(f'check passed; record {RECORD.name}')
    return 0


class BreachGuard:
    """Wraps the transport the limit calls for each attempt (production's single attempt by default). An answer whose reported cost
    is above the attempt's worst-case reserve is returned as it came, so the ledger charges it, and from then on no new attempt is
    sent: each raises `stage_a.Stopped`, which the runner treats as a stop. Attempts already in flight (at most the runner's
    concurrency) finish."""

    def __init__(self, transport=None):
        self.transport = transport or (lambda provider, request: model.openai_transport(provider, request, max_attempts=1))
        self.breaches = []
        self.lock = __import__('threading').Lock()

    def __call__(self, provider, request):
        with self.lock:
            if self.breaches:
                raise stage_a.Stopped('a breach of an attempt reserve was seen')
        response = self.transport(provider, request)
        charged, reserve = stage_a.budget.cost(request, response), stage_a.budget.worst_cost(request)
        if charged is not None and charged > reserve:
            with self.lock:
                self.breaches.append((round(charged, 6), round(reserve, 6)))
        return response


def breaches(spend_path):
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
    if record is None or record['arm_sha256'] != arm_digest():
        raise SystemExit('no check record for these arm files: run `check` first')
    research_list = universe.load(str(ROOT / 'poc' / 'universe.json'))
    topics = load_topics()
    texts = {arm: texts_of(arm) for arm in ARMS}
    cases = {arm: arm_cases(topics, arm) for arm in ARMS}
    now = {arm: {case['case']: model.request_identity(built(case, texts[arm], research_list))[1] for case in cases[arm]} for arm in ARMS}
    if now != record['requests']:
        differing = [name for arm in ARMS for name in set(now[arm]) | set(record['requests'].get(arm, {}))
                     if now[arm].get(name) != record['requests'].get(arm, {}).get(name)]
        raise SystemExit(f'REFUSED: the requests differ from the checked record: {sorted(differing)}')
    folder = Path(folder)
    guarded = BreachGuard(transport)
    for arm in ARMS:
        written, limit, job_count = stage_a.run(cases[arm], PASSES, folder / arm, CAP_PER_ARM, research_list=research_list, texts=texts[arm],
                                                transport=guarded)
        (folder / arm / 'cases.json').write_text(json.dumps(cases[arm], ensure_ascii=False, indent=1) + '\n')
        known, in_full, _ = stage_a.ledger_total(folder / arm / 'spend.jsonl')
        over = breaches(folder / arm / 'spend.jsonl')
        print(f'{arm}: {len(written)} of {job_count} sends have an outcome; spent ${known + in_full:.4f}; attempts charged above their reserve: {len(over)}')
        if over or guarded.breaches:
            raise SystemExit(f'{arm} BREACH: ledger {over}; seen at the transport {guarded.breaches}')
        if limit.stopped or len(written) != job_count:
            raise SystemExit(f'{arm} STOPPED: {limit.stop_reason}. NOT MEASURED.')
    return 0


if __name__ == '__main__':
    arguments = sys.argv[1:]
    if arguments[:1] == ['--arm']:
        configure(arguments[1])
        arguments = arguments[2:]
    mode = arguments[0] if arguments else ''
    sys.exit(check() if mode == 'check' else send(arguments[1]) if mode == 'send' and len(arguments) == 2 else f'usage: {__doc__}')
