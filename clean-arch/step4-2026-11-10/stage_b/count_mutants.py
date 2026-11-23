"""Mutants of Stage B's count and control count, each run in a mirrored scratch tree; the made-up-reading check must fail on each.

  python3 clean-arch/step4-2026-11-10/stage_b/count_mutants.py <scratch folder>
"""
import shutil, subprocess, sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]; S = Path(sys.argv[1])
MUTANTS = {
  'control: no packet comparison': ('control_theses.py', "    for name in sorted(set(on_disk) | set(expected)):\n        if on_disk.get(name) != expected.get(name):\n            problems.append(f'controls/", "    for name in []:\n        if on_disk.get(name) != expected.get(name):\n            problems.append(f'controls/", 'controls: a control packet changed'),
  'control: a ruling where the readers agree is accepted': ('control_theses.py', "            if name not in disagreements:\n", "            if False:\n", 'controls: a ruling where the readers agree'),
  'control: a missing ruling is not refused': ('control_theses.py', "        problems += [f'{family} third reader: no ruling on {name}'", "        problems += [] and [f'{family} third reader: no ruling on {name}'", 'controls: a disagreement with no ruling'),
  'count: planted-in-use.json not checked against the trial': ('stage_b_count.py', "    if json.loads(in_use_file.read_text()) != derived:", "    if False:", "count: planted-in-use.json not the trial's result"),
  'trial: a test left uncovered is accepted': ('stage_b_trial.py', "    if uncovered:\n        problems.append", "    if False:\n        problems.append", 'count: a test left without a planted answer'),
  'trial: an incomplete row is accepted (the trial path)': ('stage_b_trial.py', "        if set(row) != FORM_FIELDS:", "        if False:", 'count: a trial row with a field missing'),
  'trial: an incomplete row is accepted (the reading path)': ('stage_b_trial.py', "        if set(row) != FORM_FIELDS:", "        if False:", 'count: a reading row with a field missing'),
  'trial: a rung that is text is accepted': ('stage_b_trial.py', "        if rung is not None and not (type(rung) is int and 1 <= rung <= entry['rung_count']):", "        if False:", 'count: a rung that is text on a SUPPORTED row'),
  'control: a ruling with no reason is accepted': ('control_theses.py', "or not (isinstance(row['why'], str) and row['why'].strip()):", "or False:", 'controls: a ruling with no reason'),
  'builder: no trial gate (the trial is not derived)': ('build_stage_b.py', "        derived, problems = stage_b_trial.trial_result(folder, json.loads(Path(sys.argv[4]).read_text()))", "        derived, problems = json.loads((folder / 'planted-in-use.json').read_text()), []", 'the builder built the reading packets although the trial did not pass'),
  'trial: no session record required': ('stage_b_trial.py', "            if not sound:", "            if False:", 'count: a trial without its session record'),
  'control: an unresolved item hides a confirmed missing one': ('control_theses.py', "        material = 'not shown' if 'not_shown' in marks else ('unresolved' if 'unresolved' in marks else 'shown')", "        material = 'unresolved' if 'unresolved' in marks else ('not shown' if 'not_shown' in marks else 'shown')", 'controls: a missing item beside a disputed one'),
  'count: no void on a zero denominator': ('stage_b_count.py', "        if counter['SUPPORTED'] + counter['UNSUPPORTED'] == 0:\n            void.append(f'NOT MEASURED: {name} has no decided", "        if False:\n            void.append(f'NOT MEASURED: {name} has no decided", 'count: every yes/no judgement INSUFFICIENT'),
}
def mirror(where):
    shutil.rmtree(where, ignore_errors=True)
    stage = where / 'clean-arch/step4-2026-11-10/stage_b'
    shutil.copytree(R / 'clean-arch/step4-2026-11-10/stage_b', stage, ignore=shutil.ignore_patterns('__pycache__'))
    for link in ('src', 'poc', 'docs', 'clean-arch/unseeded-2026-11-10', 'clean-arch/step4-2026-11-10/ladder'):
        (where / link).symlink_to(R / link)
    return stage
for name, (file, old, new, case) in [('control (unmutated)', (None, None, None, None))] + list(MUTANTS.items()):
    stage = mirror(S / 'mirror')
    if file:
        text = (stage / file).read_text(); assert text.count(old) == 1, name
        (stage / file).write_text(text.replace(old, new))
    run = subprocess.run([sys.executable, str(stage / 'check_stage_b_count.py'), str(S / 'mutant-readings')], capture_output=True, text=True, env={'PYTHONDONTWRITEBYTECODE': '1', 'PATH': '/usr/bin:/bin'})
    lines = run.stdout.splitlines()
    failing = [line for line in lines if line.startswith('FAIL')]
    if file is None:
        print(f"{name}: exit {run.returncode}; {lines[-1] if lines else run.stderr[-300:]}")
    else:
        hit = [line for line in failing if case in line] or ([case] if run.returncode != 0 and case in run.stdout + run.stderr else [])
        print(f"{name}: {'caught' if hit else 'NOT CAUGHT'} by '{case}'; failing cases {len(failing)}" )
