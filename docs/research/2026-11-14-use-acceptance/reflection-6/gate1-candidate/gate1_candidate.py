"""The gate-1 handoff (council round 36): Stage A on Alex's 44 topics, three passes, with one of two configurations, prepared and inert.
Nothing is sent until Alex authorizes one configuration and a cap (D426: a fifth Stage A is his launch).

  python3 gate1_candidate.py preflight                           # $0: the fourth Stage A's stored answers through the current checks
  python3 gate1_candidate.py check <config>                     # $0: the request bytes, the stored first requests, the price
  python3 gate1_candidate.py launch <config> <new run folder>   # refuses unless authorization.json names this config and its cap

Configurations:
  astra-frozen   gpt-6-astra on the frozen ladder request, unchanged
  astra-a2-v2    gpt-6-astra on the frozen request with A2's recorded edits (D639, closing aligned) and v2's clause (D636)
"""
import dataclasses
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path[:0] = [str(HERE.parent / 'astra-a2'), str(HERE.parent / 'due-day')]
import a2_probe  # noqa: E402   (A2's recorded edits, the frozen texts, Stage A, the model module)
import dueday_probe  # noqa: E402   (v2's clause)
from a2_probe import budget, model, stage_a  # noqa: E402

CASES = ROOT / 'clean-arch' / 'step4-2026-11-10' / 'stage_a' / 'cases.json'
PASSES = [1, 2, 3]
ASTRA = dataclasses.replace(stage_a.SETTING, model='gpt-6-astra')
CONFIGS = ('astra-frozen', 'astra-a2-v2')
MEASURED_PER_SEND = (0.037, 0.050)     # astra's measured cost a send on outside topics (D633 $0.037, D634 $0.043, D636 $0.047, D639 $0.033)
AUTHORIZATION = HERE / 'authorization.json'


def texts_for(config):
    frozen = a2_probe.FROZEN_TEXTS()
    if config == 'astra-frozen':
        return frozen
    if config != 'astra-a2-v2':
        raise SystemExit(f'unknown configuration {config!r}: one of {CONFIGS}')
    texts = a2_probe.a2_texts()
    if texts['system'].count(dueday_probe.FROZEN_CLAUSE) != 1:
        raise SystemExit("v2's clause is not found once in A2's system text")
    return dict(texts, system=texts['system'].replace(dueday_probe.FROZEN_CLAUSE, dueday_probe.V2_CLAUSE))


def edits_for(config):
    """The exact replacements, as JSON-escaped text, that turn the frozen request's sent bytes into this configuration's."""
    if config == 'astra-frozen':
        return []
    pairs = [pair for name in ('system', 'closing') for pair in a2_probe.EDITS[name]] + a2_probe.SCHEMA_EDITS + \
        [(dueday_probe.FROZEN_CLAUSE, dueday_probe.V2_CLAUSE)]
    return [(json.dumps(old)[1:-1], json.dumps(new)[1:-1]) for old, new in pairs]


def built(case, setting, texts, research_list):
    user = a2_probe.base.ladder_step.user_text(stage_a.payload_for(case, research_list), texts['closing'])
    return model.build_request(setting, texts['system'], user, texts['schema'], 'clean_ladder', 'openai')


def check(config):
    """$0: every one of the 44 requests is the frozen one with only this configuration's model and recorded edits; the price."""
    cases = json.loads(CASES.read_text())
    research_list = stage_a.universe.load(str(ROOT / 'poc' / 'universe.json'))
    frozen_texts, texts = a2_probe.FROZEN_TEXTS(), texts_for(config)
    failures, worst = [], 0.0
    for case in cases:
        frozen = json.dumps(built(case, stage_a.SETTING, frozen_texts, research_list))           # the transport's serialization
        expected = frozen.replace('"model": "gpt-6-luna"', '"model": "gpt-6-astra"')
        for old, new in edits_for(config):
            expected = expected.replace(old, new)
        request = built(case, ASTRA, texts, research_list)
        if json.dumps(request) != expected:
            failures.append(case['case'])
        worst = max(worst, budget.worst_cost(request))
    sends = len(cases) * len(PASSES)
    low, high = (round(sends * rate, 2) for rate in MEASURED_PER_SEND)
    print(f'{config}: {len(cases)} topics x {len(PASSES)} passes = {sends} sends; each request is the frozen one with only the model'
          f'{" and the recorded edits" if config != "astra-frozen" else ""} changed: {not failures}')
    print(f'price: about ${low} to ${high} at astra\'s measured cost a send, before retries; worst-case reserve ${worst:.2f} an attempt '
          f'in flight; a cap of at least ${high + 2 * worst:.2f} lets two attempts be in flight to the end')
    if failures:
        raise SystemExit(f'CHECK FAILED: {failures}')
    return {'sends': sends, 'low': low, 'high': high, 'worst': worst}


def authorized(config):
    """(cap) when authorization.json names this configuration and a cap; refuses otherwise."""
    if not AUTHORIZATION.exists():
        raise SystemExit('NOT AUTHORIZED: Stage A on the 44 is Alex\'s launch (D426); no authorization.json')
    record = json.loads(AUTHORIZATION.read_text())
    if record.get('config') != config or not isinstance(record.get('cap_usd'), (int, float)) or record.get('by') != 'Alex':
        raise SystemExit(f'NOT AUTHORIZED: authorization.json does not name {config!r}, a cap and Alex')
    return float(record['cap_usd'])


def launch(config, folder, *, transport=None):
    cap = authorized(config)
    price = check(config)
    if cap < price['high']:
        raise SystemExit(f'REFUSED: the authorized cap ${cap:.2f} is below the expected ${price["high"]:.2f}')
    cases = json.loads(CASES.read_text())
    research_list = stage_a.universe.load(str(ROOT / 'poc' / 'universe.json'))
    original = stage_a.SETTING
    stage_a.SETTING = ASTRA                       # the runner reads the module's setting for every call
    try:
        written, limit, jobs = stage_a.run(cases, PASSES, folder, cap, research_list=research_list, texts=texts_for(config),
                                           transport=transport, workers=2)
    finally:
        stage_a.SETTING = original
    print(f'{len(written)} of {jobs} sends have an outcome; stopped: {limit.stopped} {limit.stop_reason or ""}')
    if limit.stopped or len(written) != jobs:                    # as Stage A's own entry point (stage_a.main)
        raise SystemExit(f'STOPPED: {limit.stop_reason}. The result reads NOT MEASURED; this folder is not started again.')
    return written, limit, jobs


STORED_RUN = ROOT / 'poc' / 'data' / 'clean-ladder-stage-a-2026-11-10' / 'run-4'


def preflight():
    """$0: every stored answer of the fourth Stage A (the 44, three passes, every attempt) read and checked by the current code as
    the step does, beside its stored verdict. It reads the stored answers; it changes neither configuration."""
    import collections
    cases = {case['case']: case for case in json.loads(CASES.read_text())}
    research_list = stage_a.universe.load(str(ROOT / 'poc' / 'universe.json'))
    judged, refused, differs, reasons = 0, 0, [], collections.Counter()
    for path in sorted(STORED_RUN.glob('send-*/outcomes.jsonl')):
        for row in map(json.loads, path.read_text().splitlines()):
            case = cases[row['case']]
            for request in row['requests']:
                if request.get('answer_text') is None:
                    continue
                judged += 1
                try:
                    found, _ = a2_probe.refcontrol.check_of(case, research_list)(a2_probe.base.ladder_step.parse_exactly(request['answer_text']))
                except (ValueError, RecursionError) as error:
                    found = [f'could not be read: {type(error).__name__}']
                refused += bool(found)
                for reason in found:
                    reasons[reason[:90]] += 1
                if bool(found) != (request.get('result') == 'refused'):
                    differs.append((row['case'], row['pass'], request.get('result')))
    print(f'the fourth Stage A\'s stored attempts: judged {judged}; refused by the current checks {refused}; '
          f'verdicts that differ from the stored ones {len(differs)} {differs[:5]}')
    for reason, count in reasons.most_common():
        print(f'  {count} x {reason}')
    if judged == 0:
        raise SystemExit(f'PREFLIGHT REFUSED: no stored attempt found under {STORED_RUN}')
    if differs:
        raise SystemExit(f'PREFLIGHT REFUSED: {len(differs)} stored verdicts differ from the current checks; diagnose before any launch')
    return judged, refused, differs


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'preflight':
        preflight()
    elif len(sys.argv) == 3 and sys.argv[1] == 'check':
        check(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == 'launch':
        launch(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
