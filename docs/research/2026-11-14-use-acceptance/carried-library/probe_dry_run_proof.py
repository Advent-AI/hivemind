"""$0 proof of the small comparison's path, ledger and stopping rule: the real driver and the real launcher run under the
proof trap (`clean-arch/e2e-comparison-2026-11-13/proof_end_to_end.py`), which answers a first-step send from the stored
October answer of the same article and refuses any send not under a live reservation. The answers were written for another
library, so nothing here is a result: only the path is judged.

  python3 probe_dry_run_proof.py <scratch folder>

  D1  22 reads planned and done, 22 sends seen by the trap, every one under a live reservation;
  D2  every read stored its request, with no open question in the empty condition and the seven carried ones in the other;
      the bytes sent for the article that production itself read from empty equal the stored bytes sent;
  D3  the ledger ends with 22 attempts, none refused, nothing reserved, not stopped, under its ceiling;
  D4  with a ceiling below one reservation, the first read is refused, the probe stops, and the trap sees no send.
PROBE_MUTANT=no-stop must fail D4.
"""
import importlib.util
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
E2E = ROOT / 'clean-arch/e2e-comparison-2026-11-13'
OCTOBER_TRACE = ROOT / 'poc/data/clean-second-week-2026-11-15/week-continued/merged-step1.sqlite'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def trap(scratch, name):
    proof = load('proof_end_to_end_for_probe', E2E / 'proof_end_to_end.py')
    site = scratch / f'{name}-site'
    site.mkdir(parents=True)
    (site / 'sitecustomize.py').write_text(proof.SITECUSTOMIZE)
    counts = scratch / f'{name}-counts.jsonl'
    (scratch / f'{name}-embeddings.json').write_text('{}')
    (scratch / f'{name}-config.json').write_text(json.dumps({'src': str(ROOT / 'src'), 'counts': str(counts), 'delay': 0.0, 'step1_trace': str(OCTOBER_TRACE),
                                                              'embeddings': str(scratch / f'{name}-embeddings.json'), 'archives': []}))
    home = scratch / f'{name}-home'
    (home / '.config/hivemind').mkdir(parents=True)
    (home / '.config/hivemind/credentials.json').write_text(json.dumps(
        {key: 'proof-placeholder-not-a-credential' for key in ('OPENAI_API_KEY', 'DEEPSEEK_API_KEY', 'TYPESAFE_API_KEY')}))
    os.chmod(home / '.config/hivemind/credentials.json', 0o600)
    return {'PYTHONPATH': str(site), 'HIVEMIND_PROOF_TRAP': str(scratch / f'{name}-config.json'), 'HOME': str(home)}, counts


def drive(scratch, name, ceiling):
    environment, counts = trap(scratch, name)
    ledger = scratch / f'{name}-ledger.json'
    load('budget_replay_for_probe', E2E / 'budget_replay.py').SharedLedger.init(ledger, ceiling)
    completed = subprocess.run([sys.executable, str(HERE / 'run_probe.py'), '--root', str(scratch / name), '--ledger', str(ledger)],
                               capture_output=True, text=True, env=dict(os.environ, **environment))
    seen = [json.loads(line) for line in counts.read_text().splitlines()] if counts.exists() else []
    outcomes = [json.loads(line) for line in (scratch / name / 'outcomes.jsonl').read_text().splitlines()]
    return completed, seen, outcomes, json.loads(ledger.read_text())


def stored_row(path, where='', arguments=()):
    connection = sqlite3.connect(f'file:{path}?mode=ro&immutable=1', uri=True)
    connection.row_factory = sqlite3.Row
    try:
        return dict(connection.execute(f'select * from trace {where}', arguments).fetchone())
    finally:
        connection.close()


def main(scratch):
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=False)
    failures = []

    def expect(condition, message):
        print(('ok   ' if condition else 'FAIL ') + message)
        if not condition:
            failures.append(message)

    carried = json.loads((HERE / 'inputs/initial-carried.json').read_text())
    shown = [{key: thesis[key] for key in ('id', 'description', 'outcome', 'period')} for thesis in carried]
    completed, seen, outcomes, ledger = drive(scratch, 'whole', 1.00)
    expect(len(outcomes) == 22 and json.loads(completed.stdout.strip().splitlines()[-1])['read'] == 22, f'D1 22 reads planned and done ({len(outcomes)})')
    expect(len(seen) == 22 and all(entry.get('live') and 'miss' not in entry for entry in seen), f'D1 the trap saw 22 sends, each under a live reservation and answered ({len(seen)})')
    judged = 0
    for row in outcomes:
        trace = stored_row(scratch / 'whole' / f"{row['sequence']:03d}-{row['condition']}" / 'trace.sqlite')
        payload = json.JSONDecoder().raw_decode(json.loads(trace['request'])['messages'][1]['content'])[0]
        judged += payload['source_item']['id'] == row['input_id'] and payload['open_theses'] == ([] if row['condition'] == 'empty' else shown)
    expect(judged == 22, f'D2 every read stored its request with the intended open questions ({judged} of 22)')
    production = stored_row(OCTOBER_TRACE, 'where sequence = ?', (9,))
    dry = stored_row(scratch / 'whole' / '009-empty' / 'trace.sqlite')
    expect(json.loads(production['before_state']) == [], 'D2 production read sequence 9 from an empty library')
    sent = lambda row: json.dumps(json.loads(row['raw_response']).get('sent_request') or json.loads(row['request']))
    expect(sent(dry) == sent(production) and 'sent_request' in json.loads(production['raw_response']), 'D2 the bytes sent for that article from empty equal the bytes production sent')
    expect(ledger['attempts'] == 22 and ledger['refused'] == 0 and not ledger['stopped'] and abs(ledger['reserved']) < 1e-9 and 0 < ledger['spent'] <= ledger['ceiling'],
           f"D3 the ledger: {ledger['attempts']} attempts, {ledger['refused']} refused, reserved {ledger['reserved']:.6f}, spent {ledger['spent']:.4f} of {ledger['ceiling']:.2f}, stopped {ledger['stopped']}")
    completed, seen, outcomes, ledger = drive(scratch, 'small-ceiling', 0.05)
    expect(len(seen) == 0, f'D4 with a ceiling below one reservation the trap saw no send ({len(seen)})')
    expect(ledger['stopped'] and ledger['refused'] >= 1 and ledger['spent'] == 0, f"D4 the ledger stopped on the refusal ({ledger['stop_reason']})")
    expect(len(outcomes) <= 2 and completed.returncode == 1 and all('live run limit reached' in str(row['error']) for row in outcomes),
           f'D4 the probe stopped at the refusal ({len(outcomes)} reads started of 22)')
    print('ALL OK' if not failures else f'{len(failures)} FAILED')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
