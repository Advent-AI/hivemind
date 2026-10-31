#!/bin/zsh
set -e
R=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context
(cd $R && shasum -a 256 -c predictions-v68.sha256)
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28
for arm in v68a v68b; do for d in 1 2 3; do python3 $R/sequential_arm.py run-$arm $d > $R/run-${arm}-d$d.log 2>&1 & done; done
wait
echo RUN-V68-DONE
