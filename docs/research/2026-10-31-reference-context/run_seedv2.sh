#!/bin/zsh
# R1 seeds v2 (design-seed-v2.md), one draw: poc-v83 over 2026-07-01..07-14, NVDA only, the 23 seed questions of
# poc/seeds/nvda-2026-07-01-v2.json, 8 workers, cap 3 USD. The same arguments as the three launchers that stopped on
# 2026-10-31 (Jev HTTP 402), with every path taken from this file's location, so it runs in any checkout.
#
#   zsh docs/research/2026-10-31-reference-context/run_seedv2.sh <draw 1|2|3> [items database]
#
# Writes poc/data/e2e-v83-seedv2-d<draw>/{views.sqlite,archive.sqlite,replay.log,run.out,run.pid}. An existing folder resumes
# after its last completed day (scripts/replay.py); an empty folder starts the window. The items database defaults to
# poc/data/items-nvda-2026-07-01-10-27.sqlite (D256, sha256 57bc2544…), the cleaned corpus every run of this phase reads.
set -e
REPOSITORY_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
DRAW="${1:?draw number 1, 2 or 3}"
ITEMS_DATABASE="${2:-$REPOSITORY_ROOT/poc/data/items-nvda-2026-07-01-10-27.sqlite}"
RUN_FOLDER="$REPOSITORY_ROOT/poc/data/e2e-v83-seedv2-d$DRAW"
test -f "$ITEMS_DATABASE" || { echo "items database not found: $ITEMS_DATABASE" >&2; exit 2 }
test -f "$HOME/.config/hivemind/credentials.json" || { echo "credentials file missing: ~/.config/hivemind/credentials.json" >&2; exit 2 }
mkdir -p "$RUN_FOLDER"
cd "$REPOSITORY_ROOT"
echo $$ > "$RUN_FOLDER/run.pid"
python3 scripts/replay.py --from 2026-07-01 --until 2026-07-14 --only NVDA --config poc/config/poc-v83.json \
    --views "$RUN_FOLDER/views.sqlite" --archive "$RUN_FOLDER/archive.sqlite" --testdb "$ITEMS_DATABASE" \
    --cap 3 --workers 8 --seed poc/seeds/nvda-2026-07-01-v2.json >> "$RUN_FOLDER/run.out" 2>&1
echo RUN-E2E-DONE >> "$RUN_FOLDER/run.out"
