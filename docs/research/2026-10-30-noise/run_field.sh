#!/bin/zsh
# Cheapest proof, third form (F3): v53 and v57 requests with the analyst_note verdict last in each item, "no" items discarded, three draws,
# the 9 probed articles and the 8 empty pages of key-small.json. Compared with run N1's v53 and v57 on the same articles.
set -e
O=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise
C=/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config
IDS=(${(f)"$(python3 -c "import json; k=json.load(open('$O/key-small.json')); print('\n'.join(k['probed_articles'] + k['empty_pages']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  python3 $O/send_field.py F3-v57V-d$d $C/poc-v73.json --verdict $IDS &
  python3 $O/send_field.py F3-v53V-d$d $C/poc-v69.json --verdict $IDS &
  wait
  echo "draw $d done"
done
echo RUN-F3-DONE
