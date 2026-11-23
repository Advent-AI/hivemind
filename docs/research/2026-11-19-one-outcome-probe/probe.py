"""python3 probe.py <out folder> <ledger> <sends>

Probe of the one-outcome closing check (arm-closing.txt): for each target case (a new thesis the frozen ladder refused as bundled, plus
one guard the ladder accepted), the Step 1 item that opened it is re-run alone through Step 1's own `run`, with that draw's open theses at
that item (its stored before_state), `sends` times under the arm. Every new thesis it returns becomes a ladder case (thesis + the stored
case's item), and the frozen ladder (stage_a_astra.py, one pass) is run on all of them. Prints, per case, the theses proposed and whether
each got a ladder. Charged on its own ledger."""
import json
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'clean-arch/step1'), str(ROOT / 'src')]
from live import LiveTransport  # noqa: E402
from runner import run  # noqa: E402
import importlib.util  # noqa: E402

RUN = ROOT / 'poc/data/comparison-2026-11-17/run'
TARGETS = [('new-2', 'clean-5', 'capex M04'), ('new-3', 'clean-4', 'capex M04'), ('new-2', 'clean-43', 'Anthropic M17'),
           ('new-3', 'clean-34', 'Anthropic M17'), ('new-3', 'clean-58', 'Anthropic M17'), ('new-2', 'clean-41', 'Hugging Face M19'),
           ('new-2', 'clean-2', 'guard: accepted product question')]

out, ledger_path, sends = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
spec = importlib.util.spec_from_file_location('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
budget_replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget_replay)
ledger = budget_replay.SharedLedger(ledger_path)
budget_replay.install_stop_gate(ledger)
texts = ((HERE / 'arm-system.txt').read_text(), (HERE / 'arm-closing.txt').read_text())
out.mkdir(parents=True, exist_ok=False)
ladder_cases, origin = [], {}
for draw, case_id, label in TARGETS:
    stored = sqlite3.connect(f'file:{RUN / draw / "step1/trace.sqlite"}?mode=ro', uri=True)
    seq, iid, before = next((s, i, b) for s, i, b, r in stored.execute('select sequence, input_id, before_state, result from trace')
                            if r and case_id in (json.loads(r).get('new_thesis_ids') or {}).values())
    case = next(c for c in json.loads((RUN / draw / 'cases/cases.json').read_text()) if c['case'] == f'{draw}/{case_id}')
    settings = json.loads((RUN / draw / 'step1/settings.json').read_text())
    limits = json.loads((RUN / draw / 'step1/limits.json').read_text())
    settings['live_limits'] = limits
    manifest = dict(json.loads((RUN / draw / 'step1/manifest.json').read_text()), item_ids=[iid], item_limit=1)
    items_db = json.loads((RUN / draw / 'run.json').read_text())['identity']['options']['items']
    for s in range(1, sends + 1):
        folder = out / f'{draw}-{case_id}-s{s}'
        folder.mkdir()
        run(items_db, folder / 'trace.sqlite', manifest, json.loads(before), settings, LiveTransport(limits, ledger=ledger),
            ROOT / 'clean-arch/PRD.md', texts)
        res = sqlite3.connect(f'file:{folder / "trace.sqlite"}?mode=ro', uri=True).execute('select result from trace').fetchone()[0]
        answer = json.loads(res) if res else {}
        opened = set((answer.get('new_thesis_ids') or {}).keys())          # the local ids Step 1 actually opened
        theses = [t for t in (answer.get('new_theses') or []) if t.get('local_id') in opened]
        print(json.dumps({'target': label, 'draw': draw, 'case': case_id, 'send': s, 'stored thesis': case['thesis']['description'][:140],
                          'arm theses': [t.get('description', '')[:160] for t in theses]}, ensure_ascii=False), flush=True)
        for k, t in enumerate(theses):
            cid = f'probe/{draw}-{case_id}-s{s}-t{k}'
            thesis = {f: t.get(f) for f in ('description', 'outcome', 'period', 'opens_as', 'settled_by')}
            ladder_cases.append({'case': cid, 'thesis': dict(thesis, id=f'{case_id}-s{s}-t{k}'), 'item': case['item']})
            origin[cid] = label
(out / 'cases.json').write_text(json.dumps(ladder_cases, indent=1, ensure_ascii=False))
subprocess.run([sys.executable, str(ROOT / 'docs/research/2026-11-17-product-comparison/stage0/stage_a_astra.py'), '--folder', str(out / 'ladder'),
                '--cap', '3', '--passes', '1', '--cases-file', str(out / 'cases.json'), '--shared-ledger', ledger_path], check=False)
for line in (out / 'ladder/send-1/outcomes.jsonl').read_text().splitlines():
    r = json.loads(line)
    print(json.dumps({'target': origin.get(r['case']), 'case': r['case'], 'status': r['status'], 'reason': (r.get('reason') or '')[:160]},
                     ensure_ascii=False))
print('spent', json.loads(Path(ledger_path).read_text())['spent'])
