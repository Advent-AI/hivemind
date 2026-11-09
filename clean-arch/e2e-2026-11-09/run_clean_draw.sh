#!/bin/zsh
# Stage 2 of D392, clean arm, one draw: c8 Step 1 forward over v108's 243 items with the 22 seeds, then Steps 2-3, then the list of
# clean-opened theses the scorer's q23 rule would find. Judging (adapter.py live) is a separate command, run after a reader has checked
# any q23 candidate. The Step 1 invocation is pinned: no candidate prompt or schema, so the PRD's c8 request is sent (test_runner.py).
set -e
DRAW="${1:?draw 1, 2 or 3}"
REPOSITORY_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
HERE="$REPOSITORY_ROOT/clean-arch/e2e-2026-11-09"
RUN_FOLDER="$REPOSITORY_ROOT/poc/data/clean-e2e-2026-11-09/stage2-clean-d$DRAW"
ITEMS_DATABASE="$REPOSITORY_ROOT/poc/data/items-nvda-2026-07-01-10-27.sqlite"
cd "$REPOSITORY_ROOT"
test -e "$RUN_FOLDER" && { echo "run folder exists: $RUN_FOLDER" >&2; exit 2 }
test -f "$HOME/.config/hivemind/credentials.json" || { echo "credentials file missing" >&2; exit 2 }
(cd "$HERE" && shasum -a 256 -c stage2-frozen.sha256 >/dev/null) || { echo "a frozen Stage 2 file changed" >&2; exit 2 }
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider clean-arch/step1/test_runner.py -k adopted_c8 >/dev/null || { echo "the PRD request is not c8" >&2; exit 2 }
mkdir -p "$RUN_FOLDER"
cp "$HERE"/stage2-manifest.json "$RUN_FOLDER"/manifest.json
cp "$HERE"/stage2-initial.json "$RUN_FOLDER"/initial.json
cp "$HERE"/stage2-settings.json "$RUN_FOLDER"/settings.json
cp "$HERE"/stage2-limits.json "$RUN_FOLDER"/limits.json
(cd "$RUN_FOLDER" && shasum -a 256 manifest.json initial.json settings.json limits.json "$REPOSITORY_ROOT"/clean-arch/PRD.md > SHA256SUMS)
echo $$ > "$RUN_FOLDER/run.pid"
PYTHONDONTWRITEBYTECODE=1 python3 clean-arch/step1/run_live.py --source "$ITEMS_DATABASE" --output "$RUN_FOLDER/trace.sqlite" \
  --manifest "$RUN_FOLDER/manifest.json" --initial "$RUN_FOLDER/initial.json" --settings "$RUN_FOLDER/settings.json" \
  --limits "$RUN_FOLDER/limits.json" > "$RUN_FOLDER/run.log" 2>&1
PYTHONDONTWRITEBYTECODE=1 python3 clean-arch/step2/run_forward.py "$RUN_FOLDER/trace.sqlite" "$RUN_FOLDER/step2" > "$RUN_FOLDER/step2.log" 2>&1
(cd "$RUN_FOLDER" && shasum -a 256 trace.sqlite step2/library.json > step2/inputs.sha256)
PYTHONDONTWRITEBYTECODE=1 python3 "$HERE/adapter.py" candidates "$RUN_FOLDER/trace.sqlite" "$RUN_FOLDER/step2" > "$RUN_FOLDER/q23-candidates.json"
echo "steps 1-3 done" >> "$RUN_FOLDER/run.log"
