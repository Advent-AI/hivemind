"""D157: break one registered contract at a time on a scratch module."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
ROOT = Path('/Users/lchingen/hivemind')
SOURCE = ROOT / 'poc/hierarchy_study/ohio_sequence.py'
OUT = Path(__file__).resolve().parent
PYTHON = '/Users/lchingen/.pyenv/versions/3.10.10/bin/python'
changes = {
 'control': None,
 'lose_members': ("for c in candidates for ref in c['thread_ids']", "for c in [] for ref in c['thread_ids']", 'test_d157_sequential_theme_evidence_and_history'),
 'wrong_reference': ("raise Refused(f'{c[\"id\"]}: invalid group references')", "pass", 'test_d157_unknown_reference_refuses_before_write'),
 'early_commit': ("bindings, affected = [], []", "conn.commit()\n            bindings, affected = [], []", 'test_d157_group_failure_rolls_back_view_and_evidence'),
 'ignore_budget': ("len(budget['attempts']) >= MAX_REQUESTS", "False", 'test_d157_budget_refuses_before_network'),
}
results = {}
for label, change in changes.items():
 with tempfile.TemporaryDirectory(prefix='ohio-mutant-') as temporary:
  target = Path(temporary) / 'ohio_sequence.py'
  source = SOURCE.read_text().replace("ROOT = Path(__file__).resolve().parents[2]", "ROOT = Path(" + repr(str(ROOT)) + ")")
  if change:
   assert source.count(change[0]) == 1, label
   source = source.replace(change[0], change[1])
  target.write_text(source)
  runner = Path(temporary) / 'run.py'
  runner.write_text("import sys\nimport pytest\nsys.path[:0] = [" + repr(temporary) + ", " + repr(str(ROOT / 'poc/hierarchy_study')) + "]\nimport ohio_sequence\nraise SystemExit(pytest.main(sys.argv[1:]))\n")
  selector = str(ROOT / 'poc/hierarchy_study/test_ohio_sequence.py') + ('::' + change[2] if change else '')
  done = subprocess.run([PYTHON, str(runner), '-q', selector], cwd=temporary, capture_output=True, text=True)
  (OUT / (label + '-test.txt')).write_text(done.stdout + done.stderr)
  results[label] = {'exit_code': done.returncode, 'expected': 0 if change is None else 1}
(OUT / 'mutations.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
if any(v['exit_code'] != v['expected'] for v in results.values()):
 raise SystemExit(1)
