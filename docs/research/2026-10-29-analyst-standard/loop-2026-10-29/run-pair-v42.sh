#!/bin/zsh
# role-v42 against a simultaneous v29 control, all 118 development articles, three draws each, interleaved.
cd /Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard
for d in 1 2 3; do
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send pairB-v29-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v45.json &
  PYTHONPATH=/Users/lchingen/hivemind-extraction-quality-2026-10-28/src:/Users/lchingen/hivemind-extraction-quality-2026-10-28/poc:/Users/lchingen/hivemind-extraction-quality-2026-10-28/docs/research/2026-10-29-analyst-standard python3 loop.py send pairB-v42-d$d /Users/lchingen/hivemind-extraction-quality-2026-10-28/poc/config/poc-v58.json &
  wait
done
echo PAIR-DONE
