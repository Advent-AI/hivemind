#!/bin/zsh
# design.md: control (poc-v69 production bytes) and arm (same + [Open questions] block) sent together, three draws, dev gold 118.
set -e
R=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context
(cd $R && shasum -a 256 -c predictions.sha256)
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28
for d in 1 2 3; do
  python3 $R/reference_arm.py send REF-v53-d$d control &
  python3 $R/reference_arm.py send REF-v53R-d$d arm &
  wait
  echo "draw $d done"
done
echo RUN-REF-DONE
