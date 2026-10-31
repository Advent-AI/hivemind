#!/bin/zsh
# design-v67.md: three independent sequential cold-start runs of the reshaped role (SEQ-v67-d1..3); controls REF-v53 and SEQ-v53R exist.
set -e
R=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context
(cd $R && shasum -a 256 -c predictions-v67.sha256)
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28
for d in 1 2 3; do python3 $R/sequential_arm.py run-v67 $d > $R/run-V67-d$d.log 2>&1 & done
wait
echo RUN-V67-DONE
