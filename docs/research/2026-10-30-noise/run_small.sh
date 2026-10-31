#!/bin/zsh
# Noise small sample (docs/research/2026-10-30-noise/key-small.json, frozen before this send, sha256 in key-small.sha256):
# role-v53 (control), role-v57 (keep rule) and role-v58 (keep rule, no empty-answer line) sent together, three draws, 40 dev articles.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
O=$ROOT/docs/research/2026-10-30-noise
IDS=(${(f)"$(python3 -c "import json; print('\n'.join(json.load(open('$O/key-small.json'))['articles']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  for pair in "v53 poc-v69" "v57 poc-v73" "v58 poc-v74"; do
    set -- ${=pair}
    PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send N1-$1-d$d $ROOT/poc/config/$2.json $IDS &
  done
  wait
  echo "draw $d done"
done
echo RUN-N1-DONE
