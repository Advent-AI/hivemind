#!/bin/zsh
# role-v59 (poc-v75) against role-v60 (poc-v76), sent together, three draws, the 56 articles of key-v60.json (frozen before this send).
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
O=$ROOT/docs/research/2026-10-30-noise
IDS=(${(f)"$(python3 -c "import json; print('\n'.join(json.load(open('$O/key-v60.json'))['articles']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send Z-v59-d$d $ROOT/poc/config/poc-v75.json $IDS &
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send Z-v60-d$d $ROOT/poc/config/poc-v76.json $IDS &
  wait
  echo "draw $d done"
done
echo RUN-Z-DONE
