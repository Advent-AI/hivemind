#!/bin/zsh
# Freeze the NVDA window database for the three-month run (2026-10-27): whole-page text from every raw HTML, assemble the
# corpus for 2026-07-01..2026-10-27, relabel into a new dated database, drop the GDELT listings (harvested for six July days
# only, so they would make those days heavier than the rest; Google News RSS is the one listing source the whole window
# shares), then the clean checks. Nothing here touches a database a run has used.
set -eu
export HIVEMIND_WINDOW_START=2026-07-01
export HIVEMIND_WINDOW_END=2026-10-27
cd /Users/lchingen/hivemind
S=poc/corpus/scripts; L=poc/corpus/logs
OUT=poc/data/items-nvda-2026-07-01-10-27.sqlite
test ! -e $OUT
echo "$(date '+%H:%M:%S') freeze start" >> $L/backfill.log
python3 $S/regenerate_text.py >> $L/backfill-freeze.log 2>&1
python3 $S/assemble.py >> $L/backfill-assemble.log 2>&1
python3 $S/relabel.py --in poc/corpus/items.sqlite --out $OUT >> $L/backfill-freeze.log 2>&1
python3 - "$OUT" <<'PY'
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1])
n = conn.execute("select count(*) from items where channel='GDELT listing'").fetchone()[0]
conn.execute("delete from items where channel='GDELT listing'"); conn.commit(); conn.execute('vacuum')
print('GDELT listings dropped from the frozen database:', n)
PY
python3 /Users/lchingen/hivemind-admission-v12-2026-10-26/docs/research/2026-10-27-nvda-3m/check_corpus.py --db $OUT --from 2026-07-01 --until 2026-10-27 > poc/reports/items-nvda-2026-07-01-10-27.check.md 2>&1 || true
python3 $S/review.py >> $L/backfill-review.log 2>&1 || true
echo "$(date '+%H:%M:%S') freeze done" >> $L/backfill.log
