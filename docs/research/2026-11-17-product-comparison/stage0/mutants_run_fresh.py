"""In-memory mutants of run_fresh.py's comparison options (plan §1.5 A, C, D, E). Each mutant is the launcher's source with one change,
executed as a fresh module and handed to the launcher tests in place of the real one; nothing is written to disk. The control (no
change) must pass; each mutant must fail the test written for it, with an assertion.

    python3 mutants_run_fresh.py
"""
import importlib.util
import subprocess
import sys
import types
from pathlib import Path

REPO = Path('/Users/lchingen/hivemind')
LAUNCHER = REPO / 'clean-arch/e2e-comparison-2026-11-13/run_fresh.py'
TESTS = REPO / 'clean-arch/e2e-comparison-2026-11-13/test_run_fresh.py'
MUTANTS = {
    'control': ([], ['test_the_given_items_limits_and_judge_end_day_reach_every_component',
                     'test_the_astra_variant_runs_the_wrapper_and_checks_every_pass', 'test_one_pass_under_another_configuration_stops_the_run']),
    'production ignores the items database': ([("            argv += ['--testdb', self.items()]", "            pass")],
                                              ['test_the_given_items_limits_and_judge_end_day_reach_every_component']),
    'Step 1 keeps the frozen limits': ([("shutil.copy(self.options.get('limits') or STAGE2 / 'stage2-limits.json'", "shutil.copy(STAGE2 / 'stage2-limits.json'")],
                                       ['test_the_given_items_limits_and_judge_end_day_reach_every_component']),
    'the judge gets no end day': ([("            inputs[self.label]['end_day'] = self.options['judge_end_day']", "            pass")],
                                  ['test_the_given_items_limits_and_judge_end_day_reach_every_component']),
    'only the first pass is checked': ([("        for pass_number in range(1, self.options['passes'] + 1):", "        for pass_number in range(1, 2):")],
                                       ['test_one_pass_under_another_configuration_stops_the_run']),
    'astra runs the frozen script': ([("        script = ASTRA_WRAPPER if variant == 'astra-frozen' else STEP4 / 'stage_a/stage_a.py'",
                                       "        script = STEP4 / 'stage_a/stage_a.py'")],
                                     ['test_the_astra_variant_runs_the_wrapper_and_checks_every_pass']),
}

RUNNER = r'''
import importlib.util, sys, types, json
from pathlib import Path
source = Path(sys.argv[1]).read_text()
for old, new in json.loads(sys.argv[2]):
    assert source.count(old) == 1, old
    source = source.replace(old, new)
mutant = types.ModuleType('run_fresh')
mutant.__file__ = sys.argv[1]
exec(compile(source, sys.argv[1], 'exec'), mutant.__dict__)
sys.modules['run_fresh_mutant'] = mutant
spec = importlib.util.spec_from_file_location('test_run_fresh_under_mutant', sys.argv[3])
tests = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tests)
tests.run_fresh = mutant
import pytest
class Swap:
    def pytest_collection_modifyitems(self, items):
        for item in items:
            item.module.run_fresh = mutant
sys.exit(pytest.main(['-q', '-p', 'no:cacheprovider', sys.argv[3], '-k', ' or '.join(json.loads(sys.argv[4]))], plugins=[Swap()]))
'''


def main():
    import json
    failures = []
    for name, (changes, tests) in MUTANTS.items():
        result = subprocess.run([sys.executable, '-c', RUNNER, str(LAUNCHER), json.dumps(changes), str(TESTS), json.dumps(tests)],
                                capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
        lines = [l for l in result.stdout.splitlines() if l.startswith('E ') or 'passed' in l or 'failed' in l]
        caught = result.returncode != 0
        expected = name != 'control'
        verdict = 'as predicted' if caught == expected else 'NOT AS PREDICTED'
        print(f'== {name}: exit {result.returncode}, {verdict}')
        for line in lines[:4]:
            print('   ', line[:200])
        if caught != expected:
            failures.append(name)
    if failures:
        raise SystemExit(f'mutants not as predicted: {failures}')


if __name__ == '__main__':
    main()
