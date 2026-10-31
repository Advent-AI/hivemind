#!/bin/zsh
# design-seq.md: three independent sequential cold-start runs of the arm (each builds its own ledger day by day); the control reuses REF-v53.
set -e
R=/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-31-reference-context
(cd $R && shasum -a 256 -c predictions-seq.sha256)
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28
for d in 1 2 3; do python3 $R/sequential_arm.py run $d > $R/run-SEQ-d$d.log 2>&1 & done
wait
echo RUN-SEQ-DONE
