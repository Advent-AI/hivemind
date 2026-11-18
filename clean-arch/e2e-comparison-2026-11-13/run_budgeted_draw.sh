#!/bin/zsh
# One production draw (poc-v118, no seed) through budget_replay.py, with a manifest, a log and a pid file (AGENTS §9).
#   zsh run_budgeted_draw.sh <run folder> <ledger> <from day> <until day> <cap usd>
set -e
RUN_FOLDER=$1; LEDGER=$2; FROM=$3; UNTIL=$4; CAP=$5
ROOT=/Users/lchingen/hivemind
CONFIG=$ROOT/poc/config/poc-v118.json
ITEMS=$ROOT/poc/data/items-nvda-2026-07-01-10-27.sqlite
[[ -e "$RUN_FOLDER" ]] && { echo "run folder exists: refused"; exit 1; }
mkdir -p "$RUN_FOLDER"
echo $$ > "$RUN_FOLDER/run.pid"
cd $ROOT
python3 - "$RUN_FOLDER/manifest.json" "$CONFIG" "$ITEMS" "$LEDGER" "$FROM" "$UNTIL" "$CAP" <<'PY'
import hashlib, json, subprocess, sys, datetime, pathlib
out, config, items, ledger, start, until, cap = sys.argv[1:]
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
git = lambda *a: subprocess.run(['git', *a], capture_output=True, text=True).stdout.strip()
files = ['clean-arch/e2e-comparison-2026-11-13/budget_replay.py', 'src/hivemind/replay.py', 'src/hivemind/model.py', 'src/hivemind/jev.py']
manifest = {'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), 'config': config, 'config_sha256': sha(config),
            'items_database': items, 'items_sha256': sha(items), 'window': [start, until], 'only': 'NVDA', 'seed_file': None,
            'ledger': ledger, 'cap_usd': float(cap), 'code_commit': git('rev-parse', 'HEAD'),
            'tree_dirty_files': len([l for l in git('status', '--short').splitlines() if l.strip()]),
            'code_sha256': {f: sha(f) for f in files}}
pathlib.Path(out).write_text(json.dumps(manifest, indent=1) + '\n'); print('manifest written:', out)
PY
python3 clean-arch/e2e-comparison-2026-11-13/budget_replay.py --ledger "$LEDGER" --from "$FROM" --until "$UNTIL" --config "$CONFIG" \
    --testdb "$ITEMS" --views "$RUN_FOLDER/views.sqlite" --archive "$RUN_FOLDER/archive.sqlite" --only NVDA --cap "$CAP" >> "$RUN_FOLDER/run.out" 2>&1
python3 - "$RUN_FOLDER/manifest.json" <<'PY'
import json, sys, datetime, pathlib
p = pathlib.Path(sys.argv[1]); m = json.loads(p.read_text())
m['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'); p.write_text(json.dumps(m, indent=1) + '\n')
PY
