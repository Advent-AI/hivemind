#!/bin/zsh
# Drive the corpus build to completion without supervision:
# 1. wait for the topic headline harvest to finish;
# 2. resolve Google News links (resumable) until nothing is pending;
# 3. let the body fetcher drain (it polls every 60 s on its own; start it if it died);
# 4. regenerate whole-page text, assemble items.sqlite, write manifest.md and sample.md.
# Every step is resumable, so re-running this script is safe.
set -u
cd /Users/lchingen/hivemind || exit 1
LOG=poc/corpus/logs/overnight.log
S=poc/corpus/scripts
echo "$(date '+%H:%M:%S') overnight driver start" >> $LOG

until ! pgrep -f "scripts/harvest_gnews_topics.py" > /dev/null; do sleep 60; done
echo "$(date '+%H:%M:%S') topic harvest finished" >> $LOG

# resolve in rounds until a round finds nothing to do (the resolver builds its queue at start)
for round in 1 2 3 4 5 6; do
  until ! pgrep -f "scripts/resolve_gnews.py" > /dev/null; do sleep 60; done
  python3 $S/resolve_gnews.py >> poc/corpus/logs/gnews-resolve.log 2>&1
  pending=$(tail -n 50 poc/corpus/logs/gnews-resolve.log | grep -o "to resolve: [0-9]*" | tail -1 | awk '{print $3}')
  echo "$(date '+%H:%M:%S') resolve round $round, pending was ${pending:-?}" >> $LOG
  [ "${pending:-1}" = "0" ] && break
done

# keep the fetcher alive until it reports finished
for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do
  if ! pgrep -f "scripts/fetch_bodies.py" > /dev/null; then
    python3 $S/fetch_bodies.py --once >> poc/corpus/logs/pages.log 2>&1
  fi
  pending=$(tail -n 200 poc/corpus/logs/pages.log | grep -o "pass: pending [0-9]*" | tail -1 | awk '{print $3}')
  echo "$(date '+%H:%M:%S') fetch attempt $attempt, last pending ${pending:-?}" >> $LOG
  sleep 120
  if ! pgrep -f "scripts/fetch_bodies.py" > /dev/null && [ "${pending:-1}" = "0" ]; then break; fi
done

until ! pgrep -f "scripts/harvest_edgar_peers.py|scripts/harvest_official.py|scripts/harvest_nvidianews.py|scripts/harvest_nvblog.py" > /dev/null; do sleep 60; done
python3 $S/regenerate_text.py >> $LOG 2>&1
python3 $S/assemble.py >> $LOG 2>&1
python3 $S/review.py >> $LOG 2>&1
echo "$(date '+%H:%M:%S') overnight driver done" >> $LOG
