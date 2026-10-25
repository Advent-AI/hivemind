"""D158: two deliberate defects on isolated copies, never edits the working tree."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
cases = [
    ('event', 'src/hivemind/extraction.py',
     "if c.get('measure') not in ('event', 'policy_event') and year_match and", 'if year_match and',
     'tests/test_event_horizon.py', "assert [c['id'] for c in candidates] == ['c2']"),
    ('role', 'poc/hierarchy_study/ohio_sequence.py',
     'transport, role_text=sample_role)', 'transport)',
     'poc/hierarchy_study/test_ohio_sequence.py::test_d158_prepared_role_experiment_runs_two_grouped_arms',
     "assert requests[0]['messages'][0]['content'] == expected_role"),
]
results = []
with tempfile.TemporaryDirectory() as name:
    root = Path(name)
    for relative in ('src', 'tests', 'poc/hierarchy_study'):
        shutil.copytree(ROOT / relative, root / relative, ignore=shutil.ignore_patterns('__pycache__'))
    for relative in ('docs', 'poc/data', 'poc/config', 'poc/reports', 'poc/universe.json'):
        (root / relative).symlink_to(ROOT / relative)
    for label, relative, old, new, test, decisive in cases:
        path = root / relative
        original = path.read_text()
        assert original.count(old) == 1
        for mutant in (False, True):
            path.write_text(original.replace(old, new) if mutant else original)
            run = subprocess.run([sys.executable, '-m', 'pytest', '-q', str(root / test)], cwd=root,
                                 capture_output=True, text=True)
            log = run.stdout + run.stderr
            (OUT / f'mutation-{label}-{mutant}.txt').write_text(log)
            assert run.returncode == (1 if mutant else 0), log
            if mutant:
                assert decisive in log and 'AssertionError' in log, log
            results.append({'case': label, 'mutant': mutant, 'returncode': run.returncode})
        path.write_text(original)
(OUT / 'mutations.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results))
