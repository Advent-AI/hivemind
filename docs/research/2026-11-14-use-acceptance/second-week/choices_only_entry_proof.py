"""With the matching and the judge held as not run, does the unchanged runner write the topics and go on to the answer choices,
on the shared ledger, and nothing else? ($0; the council's round of 2026-11-15 on the ledger left after the first step.)

A draw is prepared on the stored fresh week's merged trace (the split proof's) with the first step completed in two parts and
the matching and the judge recorded as skipped. The ledger is as it is after a first step: a ceiling of $1 of which all but a
millionth is already charged, so the answer-choice step's own cap (the ledger's ceiling) does not bind and the shared ledger
must. The unchanged `run_fresh.py`, a real process with placeholder keys only, must not start the first step or the matching, must write topics equal to the stored
unbroken run's, and must stop on the ledger at the first reservation of the answer choices. Registered expectations; non-zero
exit when one fails. Mutant: ENTRY_MUTANT=no-skips (the record holds no skipped step: the matching then starts and is refused,
and no topic is written).

  python3 choices_only_entry_proof.py <scratch folder> <merged trace of the split proof>
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
RUNNER = ROOT / 'clean-arch/e2e-comparison-2026-11-13/run_fresh.py'
MANIFEST = ROOT / 'docs/research/2026-11-14-use-acceptance/fresh-week-manifest.json'
STORED_TOPICS = ROOT / 'poc/data/clean-lean-week-2026-11-14/week-r2/c1/cases/cases.json'
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
    subprocess.run([sys.executable, str(RUNNER.parent / 'budget_replay.py'), '--init-ledger', str(ledger), '--ceiling', '1.0'], check=True, capture_output=True)
    spec = importlib.util.spec_from_file_location('budget_replay', RUNNER.parent / 'budget_replay.py')
    budget_replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(budget_replay)
    spent_before = 0.999999
    first_step = budget_replay.SharedLedger(ledger)
    assert first_step.reserve(spent_before)
    first_step.settle(spent_before, spent_before)                      # what a first step charged before the later steps start
    prepare_continued_draw.prepare(root, 'c1', ledger, MANIFEST, 3, merged_trace, {'note': 'the split proof: the stored fresh week cut after article 120'},
                                   not_run=() if MUTANT == 'no-skips' else ('step2', 'judge'), reason='the proof of the answer choices alone')
    launched = subprocess.run([sys.executable, str(RUNNER), 'clean', '--root', str(root), '--label', 'c1', '--ledger', str(ledger), '--manifest', str(MANIFEST),
                               '--passes', '3'], cwd=ROOT, capture_output=True, text=True, env=dict(os.environ, HOME=str(home)))
    record = json.loads((root / 'c1/run.json').read_text())
    state = json.loads(ledger.read_text())
    components = record['components']
    print('runner exit', launched.returncode, '|', str(record.get('stopped'))[:170])
    expect('the first step and the matching were not run', len(components['step1']['attempts']) == 1 and not components.get('step2', {}).get('attempts')
           and not (root / 'c1/step2').exists() and not (root / 'c1/step1-redo').exists())
    topics_path = root / 'c1/cases/cases.json'
    expect("the topics were written and equal the stored unbroken run's", components.get('cases', {}).get('state') == 'completed' and topics_path.exists()
           and json.loads(topics_path.read_text()) == json.loads(STORED_TOPICS.read_text()),
           f"{len(json.loads(topics_path.read_text())) if topics_path.exists() else 0} topics")
    ladder = components.get('ladder', {})
    expect("the answer choices were started and stopped on the shared ledger's refusal",
           len(ladder.get('attempts', [])) == 1 and ladder['attempts'][-1]['state'] == 'stopped' and 'ledger' in str(ladder['attempts'][-1].get('reason')),
           str(ladder.get('attempts', [{}])[-1].get('reason'))[:150] if ladder.get('attempts') else 'not started')
    expect('nothing further was charged, a reservation was refused and the ledger is stopped',
           abs(state['spent'] - spent_before) < 1e-12 and state['refused'] >= 1 and state['stopped'],
           f"spent {state['spent']}, refused {state['refused']}, {str(state.get('stop_reason'))[:90]}")
    expect('the judge was not run', components.get('judge', {}).get('state') == 'skipped' and not (root / 'c1/judge').exists())
    expect('the record says why the two steps were not run', all('not run:' in str(components.get(name, {}).get('note')) for name in ('step2', 'judge')))
    failed = [name for name, holds in EXPECTATIONS if not holds]
    print(f'{len(EXPECTATIONS)} expectations, {len(failed)} failed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
