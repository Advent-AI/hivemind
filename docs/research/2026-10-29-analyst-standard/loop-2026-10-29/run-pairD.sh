#!/bin/zsh
# Four versions at the same time, interleaved, all 118 development articles, three draws each: v29, v42, v45 (A11), v46 (A11 + A12).
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send D-v29-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v45.json &
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send D-v42-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v58.json &
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send D-v45-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v61.json &
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send D-v46-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v62.json &
  wait
done
echo PAIR-DONE
