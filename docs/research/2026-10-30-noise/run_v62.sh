#!/bin/zsh
# role-v61 (poc-v77) against role-v62 (poc-v78), sent together, three draws, the articles of key-v62.json (frozen before this send).
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
O=$ROOT/docs/research/2026-10-30-noise
IDS=(${(f)"$(python3 -c "import json; print('\n'.join(json.load(open('$O/key-v62.json'))['articles']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send Z2-v61-d$d $ROOT/poc/config/poc-v77.json $IDS &
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send Z2-v62-d$d $ROOT/poc/config/poc-v78.json $IDS &
  wait
  echo "draw $d done"
done
echo RUN-Z2-DONE
