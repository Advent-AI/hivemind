#!/bin/zsh
# D244: role-v29 baseline on the development set (118 articles), three fresh draws, same bytes as production (poc-v45).
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send base-v29-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v45.json || exit 1
done
echo BASELINE-DONE
