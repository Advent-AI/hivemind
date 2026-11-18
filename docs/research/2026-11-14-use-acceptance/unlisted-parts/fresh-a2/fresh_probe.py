"""FRESH-A2-DESIGN.md v4's answer-choice send ($0 check, then the send): the frozen request (control) and arm A2, three sends each,
on the fresh cases in population (a), through the probe's own machinery (`../probe.py`: the production builder, Stage A's runner and
spending limit, BreachGuard, the check record bound to every request's sha256).

  python3 fresh_probe.py check <cases.json> <population-a.json>
  python3 fresh_probe.py send <cases.json> <population-a.json> <new data folder>

`check` requires, for every case: A2's request equal to the control with exactly A2's replacements, A2's schema keeping the frozen key
order, and a mutant answer refused by the step's code (a stored answer with both answer choices and a refusal). The fresh cases have
no stored request or answer, so the probes' "control equals the stored request" and "stored answer accepted" checks have nothing to
judge here; the frozen build is today's production builder, which the probes' checks proved against 46 stored requests.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import probe  # noqa: E402

RECORD = HERE / 'check-passed-fresh.json'


def configure(cases_path, population_path):
    """Point the probe at A2 and at the fresh cases of population (a)."""
    probe.configure('a2')
    probe.RECORD = RECORD
    names = json.loads(Path(population_path).read_text())['population_a']
    cases = {case['case']: case for case in json.loads(Path(cases_path).read_text())}
    if not names or any(name not in cases for name in names):
        raise SystemExit('population (a) names a case not in the cases file, or is empty')
    topics = [('fresh', 'fresh', name, cases[name]) for name in names]
    probe.TOPICS = {'fresh': [('fresh', name) for name in names]}
    probe.load_topics = lambda: topics
    return topics


def check(cases_path, population_path):
    topics = configure(cases_path, population_path)
    research_list = probe.universe.load(str(probe.ROOT / 'poc' / 'universe.json'))
    frozen, arm = probe.stage_a.request_texts(), probe.texts_of('changed')
    if probe.key_order(arm['schema']) != probe.key_order(frozen['schema']):
        raise SystemExit('A2\'s schema does not keep the frozen schema keys in their order')
    failures = []
    for _, _, name, case in topics:
        control = probe.built(case, frozen, research_list)
        expected = json.dumps(control, ensure_ascii=False)
        for old, new in (pair for pairs in probe.CONFIGURATIONS['a2']['replacements'].values() for pair in pairs):
            expected = expected.replace(old, new) if expected is not None and expected.count(old) == 1 else None
        exact = expected is not None and expected == json.dumps(probe.built(case, arm, research_list), ensure_ascii=False)
        print(f'{name:16} A2 equals the control plus exactly A2\'s replacements: {exact}')
        if not exact:
            failures.append(name)
    stored = probe.SOURCES['fortnight']
    probe_case = next(case for path in stored[0] for case in json.loads(path.read_text()) if case['case'] == 'c1/clean-7')
    mutant = probe.exact_answer(probe.stored_first('fortnight', 'c1/clean-7'))
    mutant['no_ladder'] = 'declined as well'
    mutant_reasons = probe.reasons_of(mutant, probe_case, research_list)
    print(f'mutant answer (answer choices and a refusal at once): {mutant_reasons or "ACCEPTED"}')
    if failures or not mutant_reasons:
        raise SystemExit(f'CHECK FAILED: {failures or "the mutant was accepted"}')
    RECORD.write_text(json.dumps({'arm_sha256': probe.arm_digest(), 'requests': probe.request_shas(topics, research_list)}, indent=1) + '\n')
    print(f'check passed: {len(topics)} cases, {len(topics) * 6} sends; record {RECORD.name}')
    return 0


def send(cases_path, population_path, folder, transport=None):
    configure(cases_path, population_path)
    return probe.send(folder, transport=transport)


if __name__ == '__main__':
    command, arguments = sys.argv[1], sys.argv[2:]
    sys.exit(check(*arguments) if command == 'check' else send(*arguments))
