"""After a continued first step, do the later steps run through the unchanged runner, and does the shared ledger bound them?
($0; D551, condition 4.)

A draw folder is prepared as the real continuation will prepare it: the merged trace as the draw's first step, and a record that
holds the first step as completed in two parts. The unchanged runner (`run_fresh.py`, a real process) is then launched on it with
a ledger too small for any reservation and a HOME that holds placeholder keys only, so no real credential can be read. Registered
expectations; the exit status is non-zero when one fails. Mutant: ENTRY_MUTANT=other-ledger (the prepared record names another
ledger; the runner must refuse the launch, so the expectations on the matching step fail).

  python3 later_steps_entry_proof.py <scratch folder> <merged trace of the split proof>
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
RUNNER = ROOT / 'clean-arch/e2e-comparison-2026-11-13/run_fresh.py'
MANIFEST = ROOT / 'docs/research/2026-11-14-use-acceptance/fresh-week-manifest.json'
MUTANT = os.environ.get('ENTRY_MUTANT')
sys.path.insert(0, str(HERE))
import prepare_continued_draw  # noqa: E402

EXPECTATIONS = []


def expect(name, holds, detail=''):
    EXPECTATIONS.append((name, bool(holds)))
    print(('  ok    ' if holds else '  FAIL  ') + name + (f' | {detail}' if detail else ''))


def main(scratch, merged_trace):
    scratch = Path(scratch)
    if scratch.exists():
        raise SystemExit(f'{scratch} exists')
    home = scratch / 'home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    root = scratch / 'week'
    ledger = root / 'ledger.json'
    root.mkdir()
    subprocess.run([sys.executable, str(RUNNER.parent / 'budget_replay.py'), '--init-ledger', str(ledger), '--ceiling', '0.000001'], check=True, capture_output=True)
    manifest = json.loads(MANIFEST.read_text())
    recorded_ledger = scratch / 'another-ledger.json' if MUTANT == 'other-ledger' else ledger
    prepare_continued_draw.prepare(root, 'c1', recorded_ledger, MANIFEST, 3, merged_trace,
                                   {'note': 'the split proof: the stored fresh week cut after article 120'})
    launched = subprocess.run([sys.executable, str(RUNNER), 'clean', '--root', str(root), '--label', 'c1', '--ledger', str(ledger), '--manifest', str(MANIFEST),
                               '--passes', '3'], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, HOME=str(home)))
    record = json.loads((root / 'c1/run.json').read_text())
    state = json.loads(ledger.read_text())
    step1, step2 = record['components'].get('step1', {}), record['components'].get('step2', {})
    print('runner exit', launched.returncode, '|', (launched.stderr or launched.stdout).strip()[-200:].replace('\n', ' '))
    expect('the runner did not run the first step again', step1.get('state') == 'completed' and len(step1.get('attempts', [])) == 1
           and not (root / 'c1/step1-redo').exists(), json.dumps(step1)[:160])
    expect('it went on to the matching step', len(step2.get('attempts', [])) == 1, json.dumps(step2)[:200])
    expect("the matching step stopped on the shared ledger's refusal",
           bool(step2.get('attempts')) and step2['attempts'][-1]['state'] == 'stopped' and 'ledger' in str(step2['attempts'][-1].get('reason')),
           str(record.get('stopped'))[:160])
    expect('nothing was charged, a reservation was refused and the ledger is stopped', state['spent'] == 0 and state['refused'] >= 1 and state['stopped'],
           f"spent {state['spent']}, refused {state['refused']}, stopped {state['stopped']}")
    expect('no later step started', not any((root / 'c1' / name).exists() for name in ('cases', 'ladder', 'judge')) and record['state'] == 'stopped')
    expect('the first step of the record names its two parts', 'continued' in json.dumps(step1) and (root / 'c1/step1/continuation.json').exists())
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
