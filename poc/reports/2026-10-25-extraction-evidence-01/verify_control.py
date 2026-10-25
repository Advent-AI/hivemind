"""D161 positive control: ignoring the explicit control role must fail the entry-point assertion."""
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
source = root / 'poc/hierarchy_study/ohio_sequence.py'
code = source.read_text().replace("sample_role = role_text if label.startswith('grouped') else control_role_text", "sample_role = role_text if label.startswith('grouped') else None")
assert code != source.read_text()
launcher = '''import sys, types, pytest
module = types.ModuleType('ohio_sequence')
module.__file__ = sys.argv[1]
sys.modules['ohio_sequence'] = module
exec(compile(sys.stdin.read(), module.__file__, 'exec'), module.__dict__)
raise SystemExit(pytest.main(['-q', sys.argv[2], '-k', 'prepared_role and True']))
'''
result = subprocess.run([sys.executable, '-c', launcher, str(source), str(root/'poc/hierarchy_study/test_ohio_sequence.py')], input=code, text=True, capture_output=True)
(Path(__file__).parent/'mutant-control.txt').write_text(result.stdout+result.stderr)
assert result.returncode == 1 and 'AssertionError' in result.stdout and 'expected_role' in result.stdout, result.stdout
print('Ignored control role caught by exact request-content assertion.')
