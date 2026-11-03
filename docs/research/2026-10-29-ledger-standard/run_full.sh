#!/bin/zsh
# One simultaneous full run (page §9.3; D245/D246 practice): every named configuration sent together on the development gold
# (118) and the test gold (30), three draws; draw d of every configuration runs at the same time, a completed answer is never
# re-sent. Stores: docs/research/2026-10-29-analyst-standard/loop-2026-10-29/<PREFIX>-v<N>-d<d>/answers.sqlite, scored by
# final-2026-10-30/final_scores.py PREFIX v<control> v<arm>. Launch detached with a log and pid file (AGENTS §9); no edit to
# src/ or prompts while it runs.
#
#   zsh run_full.sh Q poc/config/poc-v67.json poc/config/poc-v68.json > run-Q.log 2>&1 &; echo $! > run-Q.pid
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
HERE=$ROOT/docs/research/2026-10-29-ledger-standard
PREFIX=$1; shift
IDS=(${(f)"$(python3 -c "
import json
for name in ('golden-v3/golden-v3-signed.json', 'test-set/golden-test-signed.json'):
    for a in json.load(open('$HERE/' + name))['articles']:
        print(a['input_id'])")"})
echo "articles ${#IDS[@]}"
cd $ROOT/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do
  for cfg in "$@"; do
    v=$(python3 -c "import json; print(json.load(open('$ROOT/$cfg'))['extraction']['T1']['prompt_version'].rpartition('-')[2])")
    PYTHONPATH=$ROOT/src:$ROOT/poc:$PWD python3 loop.py send $PREFIX-$v-d$d $ROOT/$cfg $IDS &
  done
  wait
  echo "draw $d done"
done
echo RUN-$PREFIX-DONE
