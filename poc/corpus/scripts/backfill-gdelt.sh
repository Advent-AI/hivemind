#!/bin/zsh
# GDELT article lists for the two backfill ranges (direct publisher URLs, no link resolution), then one fetch pass.
set -u
cd /Users/lchingen/hivemind || exit 1
S=poc/corpus/scripts; L=poc/corpus/logs
HIVEMIND_WINDOW_START=2026-07-01 HIVEMIND_WINDOW_END=2026-07-23 python3 $S/harvest_gdelt.py >> $L/backfill-gdelt.log 2>&1
HIVEMIND_WINDOW_START=2026-10-23 HIVEMIND_WINDOW_END=2026-10-27 python3 $S/harvest_gdelt.py >> $L/backfill-gdelt.log 2>&1
echo "$(date '+%H:%M:%S') gdelt done" >> $L/backfill.log
HIVEMIND_WINDOW_START=2026-07-01 HIVEMIND_WINDOW_END=2026-10-27 python3 $S/fetch_bodies.py --once >> $L/backfill-pages.log 2>&1
echo "$(date '+%H:%M:%S') fetch pass 1 done" >> $L/backfill.log
