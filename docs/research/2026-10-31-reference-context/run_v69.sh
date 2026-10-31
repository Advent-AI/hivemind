#!/bin/zsh
set -e
R=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context
(cd $R && shasum -a 256 -c predictions-v69.sha256)
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28
for d in 1 2 3; do python3 $R/sequential_arm.py run-v69b $d > $R/run-v69b-d$d.log 2>&1 & done
wait
echo RUN-V69-DONE
