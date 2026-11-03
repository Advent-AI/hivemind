#!/bin/zsh
# One draw of one end-to-end arm over the loop's window (2026-07-01..07-14, NVDA), with the record the loop needs: the run
# folder arms/<arm>/d<draw>/ holds views.sqlite, archive.sqlite, replay.log, run.out, run.pid and manifest.json (the code
# commit and whether the tree was clean, the configuration and its sha256, every prompt file the configuration names with its
# sha256, the seed file and the items database with theirs, the window, cap and workers, start and end times). A folder that
# already holds a ledger resumes (scripts/replay.py); pass a new arm name for a new measurement.
#
#   zsh docs/research/2026-11-01-e2e-loop/harness/run_arm.sh <arm> <draw 1|2|3> <poc config> [seed file | -]
#
# Environment: HIVEMIND_ITEMS_DB (default poc/data/items-nvda-2026-07-01-10-27.sqlite), HIVEMIND_WINDOW_FROM / _UNTIL (default
# 2026-07-01 / 2026-07-14), HIVEMIND_CAP_USD (default 3), HIVEMIND_WORKERS (default 8). Credentials stay in
# ~/.config/hivemind/credentials.json; nothing here prints or copies them.
set -e
ARM="${1:?arm name, e.g. r1-seeds-v2}"; DRAW="${2:?draw 1, 2 or 3}"; CONFIG="${3:?poc config, e.g. poc/config/poc-v83.json}"; SEED="${4:--}"
REPOSITORY_ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
LOOP_DIR="$REPOSITORY_ROOT/docs/research/2026-11-01-e2e-loop"
RUN_FOLDER="$LOOP_DIR/arms/$ARM/d$DRAW"
ITEMS_DATABASE="${HIVEMIND_ITEMS_DB:-$REPOSITORY_ROOT/poc/data/items-nvda-2026-07-01-10-27.sqlite}"
WINDOW_FROM="${HIVEMIND_WINDOW_FROM:-2026-07-01}"; WINDOW_UNTIL="${HIVEMIND_WINDOW_UNTIL:-2026-07-14}"
CAP="${HIVEMIND_CAP_USD:-3}"; WORKERS="${HIVEMIND_WORKERS:-16}"
cd "$REPOSITORY_ROOT"
test -f "$CONFIG" || { echo "config not found: $CONFIG" >&2; exit 2 }
test -f "$ITEMS_DATABASE" || { echo "items database not found: $ITEMS_DATABASE" >&2; exit 2 }
test -f "$HOME/.config/hivemind/credentials.json" || { echo "credentials file missing" >&2; exit 2 }
if [[ "$SEED" != "-" ]]; then test -f "$SEED" || { echo "seed file not found: $SEED" >&2; exit 2 }; fi
mkdir -p "$RUN_FOLDER"
sha() { shasum -a 256 "$1" | cut -c1-64 }
PROMPT_FILES=$(python3 - "$CONFIG" <<'PY'
# Every prompt file the configuration names: a string value that is a file stem under src/hivemind/prompts (placement-narrow-v2,
# judging-v5 ...), or an extraction prompt version T*-v<N>, which names role-v<N>, categories-v<N> and review-v<N> where present.
import json, re, sys, pathlib
PROMPTS = pathlib.Path('src/hivemind/prompts'); names = set()
def walk(x):
    if isinstance(x, dict):
        for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
    elif isinstance(x, str):
        if len(x) > 60 or any(c in x for c in ' /\n'):
            return   # prose (the _note) or a path, not a prompt stem
        for ext in ('txt', 'json'):
            p = PROMPTS / f'{x}.{ext}'
            if p.exists(): names.add(str(p))
        m = re.fullmatch(r'T\d+-v(\d+[a-z]?)', x)    # a letter suffix is a text variant of the number's behaviour (D255 arm)
        if m:
            for stem in ('role', 'categories', 'review'):
                for ext in ('txt', 'json'):
                    p = PROMPTS / f'{stem}-v{m.group(1)}.{ext}'
                    if p.exists(): names.add(str(p))
walk(json.load(open(sys.argv[1])))
print('\n'.join(sorted(names)))
PY
)
python3 - "$RUN_FOLDER/manifest.json" "$ARM" "$DRAW" "$CONFIG" "$SEED" "$ITEMS_DATABASE" "$WINDOW_FROM" "$WINDOW_UNTIL" "$CAP" "$WORKERS" "$PROMPT_FILES" <<'PY'
import json, sys, subprocess, hashlib, datetime, pathlib
out, arm, draw, config, seed, items, w_from, w_until, cap, workers, prompt_files = sys.argv[1:12]
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
git = lambda *a: subprocess.run(['git', *a], capture_output=True, text=True).stdout.strip()
manifest = {'arm': arm, 'draw': int(draw), 'started_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
            'code_commit': git('rev-parse', 'HEAD'), 'code_branch': git('rev-parse', '--abbrev-ref', 'HEAD'),
            'tree_dirty_files': [l for l in git('status', '--short').splitlines() if l.strip()],
            'config': config, 'config_sha256': sha(config),
            'prompt_files': {p: sha(p) for p in prompt_files.split('\n') if p},
            'seed_file': None if seed == '-' else seed, 'seed_sha256': None if seed == '-' else sha(seed),
            'items_database': items, 'items_sha256': sha(items), 'window': [w_from, w_until], 'only': 'NVDA',
            'cap_usd': float(cap), 'workers': int(workers)}
pathlib.Path(out).write_text(json.dumps(manifest, indent=1) + '\n')
print('manifest written:', out)
PY
echo $$ > "$RUN_FOLDER/run.pid"
SEED_ARGS=(); if [[ "$SEED" != "-" ]]; then SEED_ARGS=(--seed "$SEED"); fi
python3 scripts/replay.py --from "$WINDOW_FROM" --until "$WINDOW_UNTIL" --only NVDA --config "$CONFIG" \
    --views "$RUN_FOLDER/views.sqlite" --archive "$RUN_FOLDER/archive.sqlite" --testdb "$ITEMS_DATABASE" \
    --cap "$CAP" --workers "$WORKERS" "${SEED_ARGS[@]}" >> "$RUN_FOLDER/run.out" 2>&1
python3 - "$RUN_FOLDER/manifest.json" <<'PY'
import json, sys, datetime, pathlib
p = pathlib.Path(sys.argv[1]); m = json.loads(p.read_text())
m['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
p.write_text(json.dumps(m, indent=1) + '\n')
PY
echo RUN-ARM-DONE >> "$RUN_FOLDER/run.out"
