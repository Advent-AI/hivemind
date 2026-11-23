"""python3 probe.py <out folder> <ledger> <draws>

Cheap probe of one Step 1 arm (arm-system.txt, arm-closing.txt, arm-schema.json): each listed item is run alone through Step 1's own
`run`, with the open theses new-2 had when it read that item (its stored before_state), once per draw, under the arm. Prints, per item
and draw, the new theses proposed (opens_as and question) beside what new-2 stored for the same item. Charged on its own ledger."""
import json
import random
import sqlite3
import sys
from pathlib import Path

ROOT = Path('/Users/lchingen/hivemind')
HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT / 'clean-arch/step1'), str(ROOT / 'src')]
from live import LiveTransport  # noqa: E402
from runner import run  # noqa: E402
import importlib.util  # noqa: E402

MOTIVATING = ['gnews:af6e4910e877d5682a773d4b', 'gnews:92c7e54d38dc2916aa185568', 'gnews:25d0b1d2a9dfe0bb99432e1a',
              'gnews:1b5a3359dd0644861c0fce42', 'gnews:49f225cd79fb22132f3b9ee4', 'gnews:03f49670bc6aa3ce8c653170']
DRAW = ROOT / 'poc/data/comparison-2026-11-17/run/new-2'

out, ledger_path, draws = Path(sys.argv[1]), sys.argv[2], int(sys.argv[3])
stored = sqlite3.connect(f'file:{DRAW / "step1/trace.sqlite"}?mode=ro', uri=True)
july = [r[0] for r in stored.execute("select input_id from trace where status='complete' and result not like '%\"new_theses\": [{%' "
                                     "and input_id in (select input_id from trace) order by sequence")]
rows = {iid: (seq, before, result) for iid, seq, before, result in
        stored.execute('select input_id, sequence, before_state, result from trace')}
july = [i for i in july if i not in MOTIVATING and rows[i][0] <= 420]           # roughly July: the first 420 items in source order
guards = random.Random(20261119).sample(july, 6)
manifest_base = json.loads((DRAW / 'step1/manifest.json').read_text())
settings = json.loads((DRAW / 'step1/settings.json').read_text())
limits = json.loads((DRAW / 'step1/limits.json').read_text())
settings['live_limits'] = limits
texts = ((HERE / 'arm-system.txt').read_text(), (HERE / 'arm-closing.txt').read_text())
schema = json.loads((HERE / 'arm-schema.json').read_text())
spec = importlib.util.spec_from_file_location('budget_replay', ROOT / 'clean-arch/e2e-comparison-2026-11-13/budget_replay.py')
budget_replay = importlib.util.module_from_spec(spec)
spec.loader.exec_module(budget_replay)
ledger = budget_replay.SharedLedger(ledger_path)
budget_replay.install_stop_gate(ledger)
items_db = json.loads((DRAW / 'run.json').read_text())['identity']['options']['items']
out.mkdir(parents=True, exist_ok=False)
report = []
for kind, ids in (('motivating', MOTIVATING), ('guard', guards)):
    for iid in ids:
        seq, before, stored_result = rows[iid]
        stored_new = [t.get('question') or t.get('description') for t in (json.loads(stored_result or '{}').get('new_theses') or [])]
        for d in range(1, draws + 1):
            folder = out / f'{kind}-{seq}-d{d}'
            folder.mkdir()
            manifest = dict(manifest_base, item_ids=[iid], item_limit=1)
            result = run(items_db, folder / 'trace.sqlite', manifest, json.loads(before), settings, LiveTransport(limits, ledger=ledger),
                         ROOT / 'clean-arch/PRD.md', texts, schema)
            new = sqlite3.connect(f'file:{folder / "trace.sqlite"}?mode=ro', uri=True)
            res = new.execute('select result, status from trace').fetchone()
            theses = (json.loads(res[0]).get('new_theses') or []) if res[0] else []
            report.append({'kind': kind, 'item': iid, 'sequence': seq, 'draw': d, 'status': res[1],
                           'opened': [(t.get('opens_as'), t.get('question') or t.get('description')) for t in theses],
                           'new-2 stored opened': stored_new})
            print(json.dumps(report[-1], ensure_ascii=False), flush=True)
(out / 'report.json').write_text(json.dumps(report, indent=1, ensure_ascii=False))
print('spent', json.loads(Path(ledger_path).read_text())['spent'])
