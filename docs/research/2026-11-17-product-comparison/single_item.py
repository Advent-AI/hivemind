"""python3 single_item.py <draw folder> <failed step1 folder> <input id> <out folder> <ledger>

Completes one Step 1 item that failed its format check twice (Alex, 2026-11-19: "just look at this single article what the fuck is wrong
and just do it individually"). The item is run alone through Step 1's own `run`, with the open theses it met in the stopped trace
(its row's before_state) as the initial theses, so the request is the one the run built; the script refuses unless the new request is
byte-identical to the stored one. The send is charged on its own small ledger. Prints the outcome and whether the item opened theses."""
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
sys.path[:0] = [str(ROOT / 'clean-arch/step1'), str(ROOT / 'src')]
from live import LiveTransport  # noqa: E402
from runner import run  # noqa: E402
import importlib.util  # noqa: E402

draw, failed, input_id, out, ledger_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4]), sys.argv[5]
stored = sqlite3.connect(f'file:{failed / "trace.sqlite"}?mode=ro', uri=True)
sequence, before, request = stored.execute('select sequence, before_state, request from trace where input_id=? and status=?',
                                           (input_id, 'failed')).fetchone()
manifest = json.loads((failed / 'manifest.json').read_text())
manifest = dict(manifest, item_ids=[input_id], item_limit=1)
settings = json.loads((failed / 'settings.json').read_text())
limits = json.loads((failed / 'limits.json').read_text())
settings['live_limits'] = limits
spec = importlib.util.spec_from_file_location('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
budget_replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget_replay)
ledger = budget_replay.SharedLedger(ledger_path)
budget_replay.install_stop_gate(ledger)
out.mkdir(parents=True, exist_ok=False)
(out / 'manifest.json').write_text(json.dumps(manifest, indent=1))
(out / 'initial.json').write_text(before)
items_db = json.loads((draw / 'run.json').read_text())['identity']['options']['items']
result = run(items_db, out / 'trace.sqlite', manifest, json.loads(before), settings, LiveTransport(limits, ledger=ledger),
             ROOT / 'clean-arch/PRD.md')
new = sqlite3.connect(f'file:{out / "trace.sqlite"}?mode=ro', uri=True)
new_request, status, after, retry = new.execute('select request, status, after_state, retry_reason from trace').fetchone()
next_before = stored.execute('select before_state from trace where sequence=?', (sequence + 1,)).fetchone()
print(json.dumps({'sequence in the stopped trace': sequence, 'request identical': new_request == request, 'outcome': result,
                  'status': status, 'retry': retry, 'opened theses': len(json.loads(after)) - len(json.loads(before)),
                  'after_state equals the next row before_state': next_before is not None and after == next_before[0]}, indent=1))
