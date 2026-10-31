#!/bin/zsh
# Small sample 3 (fields-2026-10-30): role-v53, role-v54 and role-v55 sent together, three draws: the 17 articles of the field and
# tier keys and the 12 random guard articles of key-tier.json.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
O=$ROOT/docs/research/2026-10-29-ledger-standard/fields-2026-10-30
IDS=(${(f)"$(python3 -c "
import json
k = json.load(open('$O/key-small.json'))
ids = list(dict.fromkeys([r[1] for r in k['rows']] + k['tier_watch'] + k['company_guard'] + json.load(open('$O/key-tier.json'))['random_guard']))
print('\n'.join(ids))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  for pair in "v53 poc-v69" "v54 poc-v70" "v55 poc-v71"; do
    set -- ${=pair}
    PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send F3-$1-d$d $ROOT/poc/config/$2.json $IDS &
  done
  wait
  echo "draw $d done"
done
echo RUN-F3-DONE
