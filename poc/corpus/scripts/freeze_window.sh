#!/bin/zsh
# Freeze a window of the corpus into a new dated source database, cleaned (D351).
#
#   poc/corpus/scripts/freeze_window.sh <name> <from-day> <until-day>
#   e.g. poc/corpus/scripts/freeze_window.sh items-nvda-2026-07-01-10-27 2026-07-01 2026-10-27
#
# Steps, each into a new file (nothing a run has used is touched):
#   1. assemble.py   raw harvest -> poc/corpus/items.sqlite (whole-page text, labels)
#   2. relabel.py    -> poc/data/<name>.page.sqlite  (the frozen window, whole pages as fetched)
#   3. GDELT listings dropped (harvested for six July days only; Google News RSS is the listing source the window shares)
#   4. check_corpus  -> poc/reports/<name>.page.check.md
#   5. clean_pages.py -> poc/data/<name>.sqlite  (the cleaned source every script reads by default; pages kept in text_page)
#   6. check_corpus and sweep_pages over the cleaned database -> poc/reports/<name>.check.md, <name>.sweep.md
# Requires: pip3 install -r poc/corpus/scripts/requirements.txt
set -eu
NAME=$1; FROM=$2; UNTIL=$3
export HIVEMIND_WINDOW_START=$FROM
export HIVEMIND_WINDOW_END=$UNTIL
cd /Users/lchingen/hivemind
S=poc/corpus/scripts; L=poc/corpus/logs; CHECK=/Users/lchingen/hivemind-admission-v12-2026-10-26/docs/research/2026-10-27-nvda-3m/check_corpus.py
PAGE=poc/data/$NAME.page.sqlite; CLEAN=poc/data/$NAME.sqlite
test ! -e $PAGE && test ! -e $CLEAN
echo "$(date '+%H:%M:%S') freeze $NAME start" >> $L/backfill.log
python3 $S/assemble.py >> $L/backfill-assemble.log 2>&1
python3 $S/relabel.py --in poc/corpus/items.sqlite --out $PAGE >> $L/backfill-freeze.log 2>&1
python3 - "$PAGE" <<'PY'
import sqlite3, sys
conn = sqlite3.connect(sys.argv[1])
n = conn.execute("select count(*) from items where channel='GDELT listing'").fetchone()[0]
conn.execute("delete from items where channel='GDELT listing'"); conn.commit(); conn.execute('vacuum')
print('GDELT listings dropped from the frozen database:', n)
PY
python3 $CHECK --db $PAGE --from $FROM --until $UNTIL > poc/reports/$NAME.page.check.md 2>&1 || true
python3 $S/clean_pages.py --in $PAGE --out $CLEAN > poc/reports/$NAME.clean-census.txt 2>&1
python3 $CHECK --db $CLEAN --from $FROM --until $UNTIL > poc/reports/$NAME.check.md 2>&1 || true
python3 $S/sweep_pages.py --db $CLEAN --from $FROM --until $UNTIL > poc/reports/$NAME.sweep.md 2>&1 || true
echo "$(date '+%H:%M:%S') freeze $NAME done: $PAGE $CLEAN" >> $L/backfill.log
