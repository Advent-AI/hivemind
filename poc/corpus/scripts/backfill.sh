#!/bin/zsh
# Backfill the NVDA corpus to 2026-07-01..2026-10-27 (Alex, 2026-10-27): every harvester is resumable, so this only adds the
# days and pages not on disk. Order: Google News headlines -> resolve links -> fetch bodies; the company, EDGAR and TrueNorth
# harvests run beside them. Then whole-page text, assemble, review. Logs in poc/corpus/logs/backfill-*.log.
set -u
export HIVEMIND_WINDOW_START=2026-07-01
export HIVEMIND_WINDOW_END=2026-10-27
cd /Users/lchingen/hivemind || exit 1
S=poc/corpus/scripts
L=poc/corpus/logs
echo "$(date '+%H:%M:%S') backfill start $HIVEMIND_WINDOW_START..$HIVEMIND_WINDOW_END" >> $L/backfill.log
python3 $S/harvest_nvblog.py >> $L/backfill-nvblog.log 2>&1 &
python3 $S/harvest_nvidianews.py >> $L/backfill-nvidianews.log 2>&1 &
python3 $S/harvest_edgar.py >> $L/backfill-edgar.log 2>&1 &
python3 /Users/lchingen/tn-hivemind/scripts/with_credentials.py --only TRUENORTH_MCP_TOKEN -- python3 $S/harvest_truenorth.py >> $L/backfill-truenorth.log 2>&1 &
python3 $S/harvest_gnews.py >> $L/backfill-gnews.log 2>&1
echo "$(date '+%H:%M:%S') headlines done" >> $L/backfill.log
for round in 1 2 3; do
  python3 $S/resolve_gnews.py >> $L/backfill-resolve.log 2>&1
  pending=$(tail -n 50 $L/backfill-resolve.log | grep -o "to resolve: [0-9]*" | tail -1 | awk '{print $3}')
  echo "$(date '+%H:%M:%S') resolve round $round, pending was ${pending:-?}" >> $L/backfill.log
  [ "${pending:-1}" = "0" ] && break
done
python3 $S/fetch_bodies.py --once >> $L/backfill-pages.log 2>&1
echo "$(date '+%H:%M:%S') pages pass 1 done" >> $L/backfill.log
python3 $S/fetch_bodies.py --once >> $L/backfill-pages.log 2>&1
echo "$(date '+%H:%M:%S') pages pass 2 done" >> $L/backfill.log
wait
python3 $S/regenerate_text.py >> $L/backfill.log 2>&1
python3 $S/assemble.py >> $L/backfill-assemble.log 2>&1
python3 $S/review.py >> $L/backfill-review.log 2>&1
echo "$(date '+%H:%M:%S') backfill done" >> $L/backfill.log
