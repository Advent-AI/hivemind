#!/bin/zsh
# T2: role-v53's request with the T2 review (review-core-t2.txt) at the very end and the closing empty-answer condition removed, one call;
# sent together with a plain role-v53 control (N2), the 40 articles of key-small.json, three draws.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
O=$ROOT/docs/research/2026-10-30-noise
IDS=(${(f)"$(python3 -c "import json; print('\n'.join(json.load(open('$O/key-small.json'))['articles']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send N2-v53-d$d $ROOT/poc/config/poc-v69.json $IDS &
  python3 $O/send_field.py T2-v53T-d$d $ROOT/poc/config/poc-v69.json --tail2 $IDS &
  wait
  echo "draw $d done"
done
echo RUN-T2-DONE
