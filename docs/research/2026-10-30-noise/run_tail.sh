#!/bin/zsh
# T1 (Alex, 2026-10-30): role-v53's request with the review text (review-core-r3.txt) appended at the very end of the user message, one
# call, schema unchanged; the 40 articles of key-small.json, three draws. Compared with N1-v53 (control, sent earlier) and R2/R3.
set -e
O=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-30-noise
C=/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config
IDS=(${(f)"$(python3 -c "import json; print('\n'.join(json.load(open('$O/key-small.json'))['articles']))")"})
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  python3 $O/send_field.py T1-v53T-d$d $C/poc-v69.json --tail $IDS
  echo "draw $d done"
done
echo RUN-T1-DONE
