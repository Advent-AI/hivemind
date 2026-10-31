#!/bin/zsh
# Small sample of the field class (fields-2026-10-30): role-v51 and role-v52 sent together, three draws, 17 development articles.
set -e
ROOT=/Users/lchingen/hivemind-extraction-quality-2026-10-28
L=$ROOT/docs/research/2026-10-29-analyst-standard
IDS=(gnews:085b1e1a1543437edb9756d6 gnews:2957e5c79a365952140c8cce gnews:c6445931955f107b551cce85 gnews:c2924b0380602940d68de7ff
     gnews:1eeceeb212a2c82c2e75e806 gnews:c3e020d179ab025bf3ba56b0 gnews:022516991251df7f1af4d7cb gnews:9e0d5b0d6b3e603c60340128
     gnews:31e1a1a229667bbb0eeb4518 gnews:2a41a34c16f5280b624481fb gnews:aad624be9de524b95e766c96 gnews:784c556d2e58ed09dd8aa7fc
     gnews:d1a7a7f18dce5c8ae5e4d0ae gnews:f0d529209a91c7a237e117f1 gnews:bf158d067256a39f02f7c7ce
     nvblog:nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout edgar:NVDA:0001045810-26-000060:nvda-20260628.htm)
echo "articles ${#IDS[@]}"
for d in 1 2 3; do
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send F1-v51-d$d $ROOT/poc/config/poc-v67.json $IDS &
  PYTHONPATH=$ROOT/src:$ROOT/poc:$L python3 $L/loop.py send F1-v52-d$d $ROOT/poc/config/poc-v68.json $IDS &
  wait
  echo "draw $d done"
done
echo RUN-F1-DONE
